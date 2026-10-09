#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
"""pycoach - a friendly Python learning coach for your Termux terminal.

Run with no arguments for the interactive menu, or use a subcommand:

    pycoach               interactive main menu
    pycoach next          jump straight to the next unfinished lesson
    pycoach lessons       list every lesson with your status
    pycoach lesson 3      open lesson 3
    pycoach quiz          quiz on the next unfinished lesson
    pycoach quiz 3        retake the quiz for lesson 3
    pycoach projects      list the guided projects
    pycoach project 1     start project 1
    pycoach progress      show your progress report
    pycoach reset         erase your saved progress
    pycoach help          show this help
"""

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

# --------------------------------------------------------------------- paths

HOME = Path.home()
BASE = Path(__file__).resolve().parent
LESSON_DIR = BASE / "content" / "lessons"
PROJECT_DIR = BASE / "content" / "projects"
WORK_DIR = HOME / "pycoach-work"
PROJECT_WORK_DIR = WORK_DIR / "projects"
STATE_DIR = HOME / ".pycoach"
STATE_FILE = STATE_DIR / "progress.json"
RUNNER = BASE / "_runner.py"

# ------------------------------------------------------------------- colours

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(code, text):
    return "\033[%sm%s\033[0m" % (code, text) if USE_COLOR else str(text)


def bold(t):
    return _c("1", t)


def dim(t):
    return _c("2", t)


def red(t):
    return _c("31", t)


def green(t):
    return _c("32", t)


def yellow(t):
    return _c("33", t)


def cyan(t):
    return _c("36", t)


def magenta(t):
    return _c("35", t)


WIDTH = max(50, min(94, shutil.get_terminal_size((80, 24)).columns - 2))


# --------------------------------------------------------------- small utils

def ask(prompt="> "):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


def pause(prompt="Press Enter to continue..."):
    try:
        input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()


def header(text):
    print()
    print(bold(cyan(text)))
    print(dim("." * min(WIDTH, len(text) + 12)))
    print()


def bullet_lines(text, prefix="  - "):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(("-", "*")):
            out.append(prefix + line[1:].strip())
        elif line:
            out.append(prefix + line)
    return out


def fence(text):
    """Return the contents of the first ``` code block in text."""
    match = re.search(r"```[a-zA-Z0-9_+-]*\n(.*?)```", text or "", re.S)
    return match.group(1) if match else ""


# ------------------------------------------------------------ markdown render

def _inline(text):
    parts = text.split("`")
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(cyan(part))
        else:
            part = re.sub(r"\*\*(.+?)\*\*", lambda m: bold(m.group(1)), part)
            out.append(part)
    return "".join(out)


def _print_code(lines):
    for line in lines:
        if line.strip():
            print("  " + dim("|") + " " + cyan(line))
        else:
            print("  " + dim("|"))


def render(text):
    """Render a friendly subset of markdown: headings, code blocks, lists,
    quotes, and **bold** / `code` inline."""
    if not text:
        return
    in_code = False
    buf = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("```"):
            if in_code:
                _print_code(buf)
                buf = []
            in_code = not in_code
            continue
        if in_code:
            buf.append(raw.rstrip("\n"))
            continue
        s = line.rstrip()
        if not s.strip():
            print()
        elif s.startswith("### "):
            print(bold(_inline(s[4:].strip())))
        elif s.startswith("## "):
            print(bold(yellow(s[3:].strip())))
        elif s.startswith("# "):
            print(bold(cyan(s[2:].strip())))
        elif s.startswith("> "):
            print("  " + dim(">") + " " + green(_inline(s[2:].strip())))
        elif re.match(r"^\s*[-*]\s+\S", s):
            body = re.sub(r"^\s*[-*]\s+", "", s)
            wrapped = textwrap.fill(_inline(body), WIDTH - 4,
                                    initial_indent="  " + bullet_char() + " ",
                                    subsequent_indent="    ")
            print(wrapped)
        elif re.match(r"^\s*\d+\.\s+\S", s):
            num = re.match(r"^\s*(\d+)\.", s).group(1)
            body = re.sub(r"^\s*\d+\.\s+", "", s)
            print(textwrap.fill(_inline(body), WIDTH - 4,
                                initial_indent="  %s. " % num,
                                subsequent_indent="     "))
        elif s.startswith("    "):
            print("  " + dim("|") + " " + cyan(s[4:]))
        else:
            print(textwrap.fill(_inline(s), WIDTH))
    if in_code and buf:
        _print_code(buf)


def bullet_char():
    return "*" if USE_COLOR else "-"


# ------------------------------------------------------------ content loading

def parse_doc(path):
    """Split a markdown file into (title, {section: body})."""
    title = ""
    sections = {}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = []
        elif line.startswith("# ") and current is None:
            title = line[2:].strip()
        elif current is not None:
            sections[current].append(line)
    return title, {k: "\n".join(v).strip() for k, v in sections.items()}


def parse_subsections(body):
    subs = {}
    current = None
    for line in body.splitlines():
        if line.startswith("### "):
            current = line[4:].strip().lower()
            subs[current] = []
        elif current is not None:
            subs[current].append(line)
    return {k: "\n".join(v).strip() for k, v in subs.items()}


def parse_quiz(text):
    questions = []
    current = None
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line[:2].upper() == "Q:":
            current = {"q": line[2:].strip(), "choices": [], "answer": None, "why": ""}
            questions.append(current)
        elif current is None:
            continue
        elif re.match(r"^[A-H]\)", line, re.I):
            current["choices"].append(re.sub(r"^[A-H]\)\s*", "", line, flags=re.I).strip())
        elif line[:7].upper() == "ANSWER:":
            current["answer"] = line.split(":", 1)[1].strip().upper()[:1]
        elif line[:4].upper() == "WHY:":
            current["why"] = line.split(":", 1)[1].strip()
        else:
            current["q"] += " " + line
    for q in questions:
        if q["answer"] and q["answer"].isalpha():
            q["index"] = ord(q["answer"]) - 65
        else:
            q["index"] = -1
    return [q for q in questions if 0 <= q["index"] < len(q["choices"])]


def load_lessons():
    lessons = []
    for path in sorted(LESSON_DIR.glob("*.md")):
        title, secs = parse_doc(path)
        lessons.append({
            "n": int(path.name.split("-")[0]),
            "title": title,
            "objectives": bullet_lines(secs.get("objectives", "")),
            "body": secs.get("lesson", ""),
            "exercise": secs.get("exercise", ""),
            "hints": bullet_lines(secs.get("hints", ""), prefix=""),
            "starter": fence(secs.get("starter", "")),
            "tests": fence(secs.get("tests", "")),
            "quiz": parse_quiz(secs.get("quiz", "")),
            "path": path,
        })
    return lessons


def load_projects():
    projects = []
    for path in sorted(PROJECT_DIR.glob("*.md")):
        title, secs = parse_doc(path)
        steps = []
        for name, body in secs.items():
            match = re.match(r"^step\s+(\d+)\s*[:\-]\s*(.+)$", name)
            if not match:
                continue
            subs = parse_subsections(body)
            filename = fence(subs.get("file", "")).strip() or "program.py"
            hints = bullet_lines(subs.get("hints", ""), prefix="")
            steps.append({
                "n": int(match.group(1)),
                "title": match.group(2).strip(),
                "body": body.split("###", 1)[0].strip(),
                "filename": filename,
                "starter": fence(subs.get("starter", "")),
                "check": fence(subs.get("check", "")),
                "hints": hints,
            })
        steps.sort(key=lambda s: s["n"])
        projects.append({
            "n": int(path.name.split("-")[0]),
            "title": title,
            "overview": secs.get("overview", ""),
            "steps": steps,
            "path": path,
        })
    return projects


# -------------------------------------------------------------------- state

def load_state():
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    state.setdefault("lessons", {})
    state.setdefault("projects", {})
    return state


def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def lesson_state(state, n):
    return state["lessons"].setdefault(str(n), {})


# -------------------------------------------------------------- test running

def run_tests(code_path, tests):
    """Run the tests for a solution file. Returns (status, message, output)."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".py", prefix="pycoach-tests-",
                                     delete=False, encoding="utf-8") as handle:
        handle.write(tests)
        tests_path = Path(handle.name)
    try:
        proc = subprocess.run(
            [sys.executable, str(RUNNER), str(code_path), str(tests_path)],
            capture_output=True,
            text=True,
            timeout=25,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return ("error", "Your program took longer than 25 seconds. "
                         "Look for a loop that never ends.", "")
    except OSError as exc:
        return ("error", "Could not run the tests: %s" % exc, "")
    finally:
        try:
            tests_path.unlink()
        except OSError:
            pass

    raw = proc.stdout
    if not raw.strip():
        detail = (proc.stderr or "").strip().splitlines()
        detail = detail[-6:] if detail else ["no output at all"]
        return ("error", "The test runner itself failed:\n    " + "\n    ".join(detail), "")

    lines = raw.splitlines()
    status_line = lines[0]
    body = "\n".join(lines[1:])

    def cut(tag, end_tag):
        nonlocal body
        if tag in body:
            head, rest = body.split(tag, 1)
            if end_tag in rest:
                inner, body = rest.split(end_tag, 1)
            else:
                inner, body = rest, ""
            body = head + body
            return inner
        return ""

    output = cut("---OUTPUT---", "---ENDOUTPUT---").strip("\n")
    error = cut("---ERROR---", "---ENDERROR---").strip("\n")
    message = body.strip()

    if status_line == "RESULT:PASS":
        return ("pass", "", output)
    if status_line == "RESULT:FAIL":
        return ("fail", message or "A test didn't pass yet.", output)
    return ("error", message or "Your code ran into an error.", (error + "\n" + output).strip("\n"))


def show_tests(status, message, output):
    if status == "pass":
        print("  " + green("OK") + "  All tests passed. Nice work!")
        return
    if status == "fail":
        print("  " + red("x") + "  Not quite yet:")
        for line in message.splitlines() or ["a test didn't pass"]:
            print(textwrap.fill(line, WIDTH - 6, initial_indent="      ",
                                subsequent_indent="      "))
        if output.strip():
            print()
            print(dim("      what your program printed:"))
            for line in output.splitlines()[-8:]:
                print(dim("      | " + line))
        print()
        return
    print("  " + red("!") + "  Something in your code raised an error:")
    for line in (message or "").splitlines():
        if "File \"" in line and "site-packages" in line:
            continue
        print("      " + line.replace(os.sep + "pycoach-work" + os.sep, "~/pycoach-work/"))
    if output.strip():
        print(dim("      (what it printed before that: %r)" % output.strip()[-120:]))
    print()


# ------------------------------------------------------------------- editing

def open_editor(path):
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR") or "nano"
    cmd = shlex.split(editor) + [str(path)]
    try:
        subprocess.call(cmd)
    except (FileNotFoundError, OSError):
        print(yellow("  Couldn't start '%s' - falling back to nano." % editor))
        subprocess.call(["nano", str(path)])


def show_file(path, limit=None):
    print()
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    if limit:
        lines = lines[:limit]
    for i, line in enumerate(lines, 1):
        print(dim("  %3d | " % i) + line)
    print()


def run_learner_program(path):
    print()
    print(dim("  Running your program - use Ctrl+C to stop it."))
    print(dim("  " + "-" * (WIDTH - 4)))
    try:
        subprocess.call([sys.executable, str(path)])
    except KeyboardInterrupt:
        print()
    print(dim("  " + "-" * (WIDTH - 4)))


# ------------------------------------------------------------ exercise loop

def exercise_loop(title, prompt, code_path, tests, starter, hints,
                  printable=None, show_run=False):
    """Drive the edit / test / hint loop. Returns True when tests pass."""
    if not code_path.exists():
        code_path.parent.mkdir(parents=True, exist_ok=True)
        code_path.write_text(starter, encoding="utf-8")
    used_hints = 0
    while True:
        options = ["[e] edit", "[r] check my answer"]
        if show_run:
            options.append("[x] run it for real")
        if hints:
            options.append("[h] hint")
        options += ["[v] view my code", "[p] show the task again",
                    "[s] skip", "[q] quit"]
        print()
        print(dim("  " + "   ".join(options)))
        choice = ask("  > ").lower()

        if choice == "e":
            open_editor(code_path)
        elif choice == "x":
            if show_run:
                run_learner_program(code_path)
            else:
                print(dim("  Running is only useful for programs that print or ask "
                          "for input - this one is tested through its functions."))
        elif choice == "r":
            print()
            status, message, output = run_tests(code_path, tests)
            show_tests(status, message, output)
            if status == "pass":
                return True
        elif choice == "h":
            if used_hints < len(hints):
                print()
                print("  " + yellow("HINT") + " " + dim("(%d of %d)" % (used_hints + 1, len(hints))))
                render("  " + hints[used_hints])
                used_hints += 1
            else:
                print("  " + dim("No more hints for this one. You've got this!"))
        elif choice == "v":
            show_file(code_path)
        elif choice == "p":
            print()
            render(printable if printable is not None else prompt)
        elif choice == "s":
            return False
        elif choice == "q":
            return None
        else:
            print(dim("  Please type one of: e, r, h, v, p, s, q"))


# ----------------------------------------------------------------- lesson flow

def lesson_flow(lessons, state, index, quiet=False):
    lesson = lessons[index]
    if not quiet:
        header(lesson["title"])
        if lesson["objectives"]:
            print(bold("  What you'll learn"))
            for line in lesson["objectives"]:
                print("  " + _inline(line))
            print()
        render(lesson["body"])

    code_path = WORK_DIR / ("lesson-%02d.py" % lesson["n"])
    print()
    print(bold(yellow("  Exercise")))
    render(lesson["exercise"])

    ok = exercise_loop(lesson["title"], lesson["exercise"], code_path,
                       lesson["tests"], lesson["starter"], lesson["hints"],
                       show_run=(lesson["n"] == 1 or "run_main" in lesson["tests"]))
    if ok is None:
        print(dim("\n  Saved. Come back with `pycoach` anytime.\n"))
        sys.exit(0)
    if not ok:
        print(dim("\n  Skipped - it'll be here when you're ready (`pycoach lesson %d`)."
                  % lesson["n"]))
        return False

    entry = lesson_state(state, lesson["n"])
    entry["done"] = True
    save_state(state)

    print()
    print(green("  Lesson %d complete!" % lesson["n"]))
    if lesson["quiz"]:
        answer = ask("  Take the quick quiz now? [Y/n] ").lower()
        if answer not in ("n", "no", "q"):
            quiz_flow(lessons, state, index)
    nxt = next((l for l in lessons if not state["lessons"].get(str(l["n"]), {}).get("done")), None)
    if nxt:
        print(dim("\n  Next up: %s  (`pycoach next`)" % nxt["title"]))
    else:
        print(magenta("\n  You've finished every lesson. Try a project! (`pycoach projects`)"))
    print()
    return True


def next_lesson_index(lessons, state):
    for i, lesson in enumerate(lessons):
        if not state["lessons"].get(str(lesson["n"]), {}).get("done"):
            return i
    return None


# ----------------------------------------------------------------- quiz flow

def quiz_flow(lessons, state, index):
    lesson = lessons[index]
    questions = lesson["quiz"]
    if not questions:
        print("  This lesson has no quiz yet.")
        return
    header("Quiz - %s" % lesson["title"])
    correct = 0
    for number, q in enumerate(questions, 1):
        print(bold("  %d. %s" % (number, q["q"])))
        for i, choice in enumerate(q["choices"]):
            print("     %s) %s" % (chr(65 + i), choice))
        while True:
            answer = ask("     your answer: ").lower()
            if answer == "q":
                print(dim("  Quiz abandoned - your progress so far was not saved."))
                return
            if len(answer) == 1 and answer.isalpha() and \
                    ord(answer.upper()) - 65 < len(q["choices"]):
                break
            print(dim("     Please type %s-%s, or q to quit."
                      % ("A", chr(64 + len(q["choices"])))))
        if ord(answer.upper()) - 65 == q["index"]:
            correct += 1
            print("     " + green("Correct!"))
        else:
            print("     " + red("Not this time - the answer is %s." % q["answer"]))
        if q["why"]:
            print(textwrap.fill(_inline("  " + q["why"]), WIDTH,
                                initial_indent="     ", subsequent_indent="     "))
        print()

    entry = lesson_state(state, lesson["n"])
    entry["quiz_total"] = len(questions)
    entry["quiz_best"] = max(entry.get("quiz_best", 0), correct)
    save_state(state)

    pct = 100 * correct // len(questions)
    print(bold("  Score: %d/%d (%d%%)" % (correct, len(questions), pct)))
    if pct == 100:
        print(green("  Perfect. You clearly get it."))
    elif pct >= 70:
        print(green("  Solid - you know this material."))
    else:
        print(yellow("  Worth another look: `pycoach lesson %d`" % lesson["n"]))
    print()


# -------------------------------------------------------------- project flow

def project_flow(projects, state, index):
    project = projects[index]
    entry = state["projects"].setdefault(str(project["n"]), {})
    done_steps = set(entry.get("steps", []))

    header(project["title"])
    render(project["overview"])

    for step in project["steps"]:
        code_path = PROJECT_WORK_DIR / ("project-%02d" % project["n"]) / step["filename"]
        if not code_path.exists() and step["starter"]:
            code_path.parent.mkdir(parents=True, exist_ok=True)
            code_path.write_text(step["starter"], encoding="utf-8")

        if step["n"] in done_steps:
            status = run_tests(code_path, step["check"])[0] if step["check"] else "pass"
            if status == "pass":
                print()
                print(dim("  Step %d of %d (%s) is already done."
                          % (step["n"], len(project["steps"]), step["title"])))
                if ask("  Work on it again? [y/N] ").lower() not in ("y", "yes"):
                    continue
            else:
                print()
                print(yellow("  Step %d needs another look - its check no longer passes."
                             % step["n"]))
            done_steps.discard(step["n"])
            entry["steps"] = sorted(done_steps)
            save_state(state)

        print()
        print(bold(yellow("  Step %d of %d: %s"
                          % (step["n"], len(project["steps"]), step["title"]))))
        print()
        render(step["body"])
        print()
        print(dim("  File: %s" % code_path))
        print(dim("  [e] edit   [r] run the check   [h] hint   [v] view   "
                  "[x] try it   [n] next step   [q] quit"))
        hints_used = 0
        while True:
            choice = ask("  > ").lower()
            if choice == "e":
                open_editor(code_path)
            elif choice == "x":
                run_learner_program(code_path)
            elif choice == "r":
                print()
                status, message, output = run_tests(code_path, step["check"])
                show_tests(status, message, output)
                if status == "pass":
                    done_steps.add(step["n"])
                    entry["steps"] = sorted(done_steps)
                    save_state(state)
                    break
            elif choice == "h":
                if hints_used < len(step["hints"]):
                    print()
                    render("  " + step["hints"][hints_used])
                    hints_used += 1
                else:
                    print("  " + dim("That's every hint for this step."))
            elif choice == "v":
                show_file(code_path)
            elif choice == "n":
                print(dim("  Moving on - the check will be waiting for you."))
                break
            elif choice == "q":
                print(dim("\n  Progress saved. Resume with `pycoach project %d`.\n"
                          % project["n"]))
                save_state(state)
                sys.exit(0)
            else:
                print(dim("  Please type one of: e, r, h, v, x, n, q"))

    total = len(project["steps"])
    if len(done_steps) >= total:
        entry["done"] = True
        save_state(state)
        print()
        print(magenta("  Project %d finished - you built a real program. "
                      "Try changing it, breaking it, making it yours." % project["n"]))
        print()
    else:
        save_state(state)
        print(dim("\n  %d of %d steps checked off. Resume with `pycoach project %d`.\n"
                  % (len(done_steps), total, project["n"])))


# -------------------------------------------------------------- progress

def load_progress_numbers(state, lessons, projects):
    done = sum(1 for l in lessons
               if state["lessons"].get(str(l["n"]), {}).get("done"))
    quiz_scores = [v for v in state["lessons"].values() if "quiz_best" in v]
    quiz_total = sum(v.get("quiz_total", 0) for v in quiz_scores)
    quiz_best = sum(v.get("quiz_best", 0) for v in quiz_scores)
    proj_done = sum(1 for p in projects
                    if state["projects"].get(str(p["n"]), {}).get("done"))
    return done, quiz_best, quiz_total, proj_done


def bar(done, total, width=18):
    total = max(total, 1)
    filled = int(round(width * done / total))
    return green("#" * filled) + dim("." * (width - filled))


def show_progress(state, lessons, projects):
    done, quiz_best, quiz_total, proj_done = load_progress_numbers(state, lessons, projects)
    header("Progress report")
    print("  lessons      %s  %d/%d" % (bar(done, len(lessons)), done, len(lessons)))
    print("  projects     %s  %d/%d" % (bar(proj_done, len(projects)), proj_done, len(projects)))
    if quiz_total:
        print("  quiz best    %s  %d/%d (%d%%)"
              % (bar(quiz_best, quiz_total), quiz_best, quiz_total,
                 100 * quiz_best // quiz_total))
    print()
    print(bold("  Lessons"))
    for lesson in lessons:
        entry = state["lessons"].get(str(lesson["n"]), {})
        mark = green("[done]") if entry.get("done") else dim("[  -  ]")
        score = ""
        if "quiz_best" in entry:
            score = dim("  quiz %d/%d" % (entry["quiz_best"], entry.get("quiz_total", 0)))
        print("   %s  %s%s" % (mark, lesson["title"], score))
    print()
    print(bold("  Projects"))
    for project in projects:
        entry = state["projects"].get(str(project["n"]), {})
        steps = entry.get("steps", [])
        mark = green("[done]") if entry.get("done") else \
            (yellow("[%2d/%d]" % (len(steps), len(project["steps"]))) if steps else dim("[  -  ]"))
        print("   %s  %s" % (mark, project["title"]))
    print()


# --------------------------------------------------------------------- menus

def main_menu(lessons, projects, state):
    done, quiz_best, quiz_total, proj_done = load_progress_numbers(state, lessons, projects)
    header("PYCOACH  -  learn Python one small step at a time")
    print("  lessons      %s  %d/%d" % (bar(done, len(lessons)), done, len(lessons)))
    print("  projects     %s  %d/%d" % (bar(proj_done, len(projects)), proj_done, len(projects)))
    if quiz_total:
        print("  quiz best    %s  %d/%d" % (bar(quiz_best, quiz_total), quiz_best, quiz_total))
    print()
    print("  [1] learn - continue with the next lesson")
    print("  [2] lessons - browse everything")
    print("  [3] quiz - test what you know")
    print("  [4] projects - build a real program")
    print("  [5] progress - your report card")
    print("  [h] help")
    print("  [q] quit")
    while True:
        choice = ask().lower()
        if choice in ("q", "quit", "exit"):
            print(dim("\n  Keep practicing. See you next time.\n"))
            return
        elif choice in ("1", "l", "learn", "n", "next"):
            index = next_lesson_index(lessons, state)
            if index is None:
                print(magenta("\n  Every lesson is done. Head to [4] projects!"))
            else:
                lesson_flow(lessons, state, index)
        elif choice in ("2", "lessons", "list"):
            lessons_menu(lessons, state)
        elif choice in ("3", "quiz"):
            quiz_menu(lessons, state)
        elif choice in ("4", "p", "projects", "project"):
            projects_menu(projects, state)
        elif choice in ("5", "progress", "stats"):
            show_progress(state, lessons, projects)
        elif choice in ("h", "help", "?"):
            help_text()
        else:
            print(dim("  Pick one of: 1 2 3 4 5 h q"))


def lessons_menu(lessons, state):
    header("Lessons")
    for lesson in lessons:
        entry = state["lessons"].get(str(lesson["n"]), {})
        mark = green("[done]") if entry.get("done") else dim("[  -  ]")
        print("  %2d. %s  %s" % (lesson["n"], lesson["title"], mark))
    print()
    answer = ask("Which lesson? (number, or Enter to go back) ")
    if not answer:
        return
    index = lesson_index(lessons, answer)
    if index is None:
        print("  No lesson numbered '%s'." % answer)
        return
    lesson_flow(lessons, state, index)


def lesson_index(lessons, answer):
    try:
        number = int(answer)
    except ValueError:
        return None
    for i, lesson in enumerate(lessons):
        if lesson["n"] == number:
            return i
    return None


def quiz_menu(lessons, state):
    header("Quiz")
    for lesson in lessons:
        entry = state["lessons"].get(str(lesson["n"]), {})
        if "quiz_best" in entry:
            score = dim("  best %d/%d" % (entry["quiz_best"], entry.get("quiz_total", 0)))
        else:
            score = dim("  not taken")
        print("  %2d. %s%s" % (lesson["n"], lesson["title"], score))
    print()
    answer = ask("Which quiz? (number, or Enter for the next unfinished lesson) ")
    if not answer:
        index = next_lesson_index(lessons, state)
        if index is None:
            index = 0
    else:
        index = lesson_index(lessons, answer)
        if index is None:
            print("  No lesson numbered '%s'." % answer)
            return
    quiz_flow(lessons, state, index)


def projects_menu(projects, state):
    header("Projects")
    for project in projects:
        entry = state["projects"].get(str(project["n"]), {})
        steps = entry.get("steps", [])
        if entry.get("done"):
            mark = green("[done]")
        elif steps:
            mark = yellow("[%d/%d]" % (len(steps), len(project["steps"])))
        else:
            mark = dim("[  -  ]")
        print("  %d. %s  %s" % (project["n"], project["title"], mark))
    print()
    answer = ask("Which project? (number, or Enter to go back) ")
    if not answer:
        return
    try:
        number = int(answer)
    except ValueError:
        print("  Type a project number.")
        return
    for i, project in enumerate(projects):
        if project["n"] == number:
            project_flow(projects, state, i)
            return
    print("  No project numbered '%s'." % answer)


def help_text():
    header("Help")
    print("""  Commands you can type anywhere:

    pycoach                open this menu
    pycoach next           jump to the next unfinished lesson
    pycoach lessons        list the lessons
    pycoach lesson 3       open lesson 3
    pycoach quiz           take a quiz
    pycoach quiz 3         retake the quiz for lesson 3
    pycoach projects       list the guided projects
    pycoach project 1      start project 1
    pycoach progress       show your progress report
    pycoach reset          erase your saved progress
    pycoach help           this text

  While working on an exercise:

    [e] edit your code in your editor ($EDITOR, nano by default)
    [r] run the automatic checks
    [h] ask for a hint (one at a time)
    [v] view your code
    [x] run your program for real (where offered)
    [p] show the task again
    [s] skip it for now
    [q] quit - your code is always kept

  Your files live in ~/pycoach-work/, so you can edit them any time.""")


# ---------------------------------------------------------------- entrypoint

def usage():
    print(__doc__.strip())


def main(argv):
    lessons = load_lessons()
    projects = load_projects()
    state = load_state()
    command = argv[0] if argv else ""

    if command in ("help", "-h", "--help"):
        usage()
    elif command in ("", "menu"):
        if not lessons:
            print("No lessons found in %s" % LESSON_DIR)
            return 1
        main_menu(lessons, projects, state)
    elif command == "next":
        index = next_lesson_index(lessons, state)
        if index is None:
            print("Every lesson is finished. Try `pycoach projects`.")
        else:
            lesson_flow(lessons, state, index)
    elif command in ("lessons", "list"):
        lessons_menu(lessons, state)
    elif command == "lesson":
        index = lesson_index(lessons, argv[1]) if len(argv) > 1 else None
        if index is None:
            print("Usage: pycoach lesson <number>")
            return 1
        lesson_flow(lessons, state, index)
    elif command == "quiz":
        if len(argv) > 1:
            index = lesson_index(lessons, argv[1])
            if index is None:
                print("No lesson numbered '%s'." % argv[1])
                return 1
        else:
            index = next_lesson_index(lessons, state) or 0
        quiz_flow(lessons, state, index)
    elif command in ("projects", "project"):
        if len(argv) > 1:
            try:
                number = int(argv[1])
            except ValueError:
                number = -1
            for i, project in enumerate(projects):
                if project["n"] == number:
                    project_flow(projects, state, i)
                    return 0
            print("No project numbered '%s'." % argv[1])
            return 1
        projects_menu(projects, state)
    elif command in ("progress", "stats"):
        show_progress(state, lessons, projects)
    elif command == "reset":
        if len(argv) > 1 and argv[1] in ("-y", "--yes"):
            confirmed = True
        else:
            confirmed = ask("Erase all saved progress? [y/N] ").lower() in ("y", "yes")
        if confirmed:
            save_state({"lessons": {}, "projects": {}})
            print("Progress cleared. Your code files in %s were kept." % WORK_DIR)
        else:
            print("Cancelled.")
    else:
        print("Unknown command: %s" % command)
        usage()
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("\n")
        sys.exit(130)
