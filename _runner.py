#!/data/data/com.termux/files/usr/bin/python3
"""pycoach's internal test runner. You don't need to run this directly.

It loads your solution file, then runs the exercise's tests against it.

    python3 _runner.py your_solution.py tests.py

Output protocol (read by pycoach.py):
    RESULT:PASS | RESULT:FAIL | RESULT:ERROR
    <message>
    ---OUTPUT---
    <whatever your program printed>
    ---ENDOUTPUT---
"""

import ast
import contextlib
import io
import os
import re
import subprocess
import sys
import traceback

STUDENT = None
STDIN_TEXT = ""


def check(condition, message=""):
    """Helper available inside every test: check(value, 'what should be true')."""
    if not condition:
        raise AssertionError(message or "That test didn't pass yet.")
    return True


def run_main(stdin=None, timeout=10, args=None):
    """Helper: run your file as a real program.

    Returns (text_output, exit_code). It runs inside the folder your file
    lives in, so relative paths like "todo.txt" land next to your program.
    If stdin is None, the tests' STDIN value is used. Your program's
    traceback is included in the output.
    """
    text = STDIN_TEXT if stdin is None else stdin
    try:
        proc = subprocess.run(
            [sys.executable, str(STUDENT)] + list(args or []),
            input=text,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(os.path.dirname(os.path.abspath(STUDENT))),
        )
    except subprocess.TimeoutExpired:
        raise AssertionError(
            "Your program did not finish within %d seconds - "
            "does a loop never stop?" % timeout
        )
    return proc.stdout + proc.stderr, proc.returncode


def _report(status, message, output, load_error=None):
    print("RESULT:" + status)
    if message:
        print(message)
    if load_error:
        print("---ERROR---")
        sys.stdout.write(load_error)
        print("---ENDERROR---")
    print("---OUTPUT---")
    sys.stdout.write(output)
    print("")
    print("---ENDOUTPUT---")


def main():
    global STUDENT, STDIN_TEXT

    # Everything runs from the folder the learner's file lives in, so relative
    # paths like "todo.txt" land next to their program (and not in pycoach's
    # own folder).
    STUDENT = os.path.abspath(sys.argv[1])
    tests_path = os.path.abspath(sys.argv[2])
    os.chdir(os.path.dirname(STUDENT))

    with open(tests_path, encoding="utf-8") as fh:
        tests = fh.read()

    # The tests file may start with:  STDIN = "Alice\n30\n"
    # That text is fed to your program when it is loaded, and to run_main().
    match = re.search(r"^\s*STDIN\s*=\s*(.+)$", tests, re.M)
    if match:
        try:
            STDIN_TEXT = ast.literal_eval(match.group(1).strip())
        except Exception:
            pass

    namespace = {
        "__name__": "__learner__",
        "check": check,
        "run_main": run_main,
        "HERE": os.path.dirname(os.path.abspath(STUDENT)),
    }
    printed = io.StringIO()
    load_error = None

    real_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(STDIN_TEXT)
        with contextlib.redirect_stdout(printed):
            with open(STUDENT, encoding="utf-8") as fh:
                source = fh.read()
            exec(compile(source, STUDENT, "exec"), namespace)
    except SystemExit:
        pass
    except BaseException:
        load_error = traceback.format_exc()
    finally:
        sys.stdin = real_stdin

    namespace["OUTPUT"] = printed.getvalue()
    namespace["OUTPUT_LINES"] = printed.getvalue().splitlines()

    try:
        with contextlib.redirect_stdout(printed):
            exec(compile(tests, "<pycoach tests>", "exec"), namespace)
    except AssertionError as exc:
        _report("FAIL", str(exc) or "A test didn't pass.", printed.getvalue(), load_error)
        return 2
    except BaseException:
        _report("ERROR", "A test itself went wrong:", printed.getvalue(), traceback.format_exc())
        return 1

    _report("PASS", "", printed.getvalue(), load_error)
    return 0


if __name__ == "__main__":
    sys.exit(main())
