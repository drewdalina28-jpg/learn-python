#!/data/data/com.termux/files/usr/bin/python3
"""Sanity check for pycoach's content.

Writes known-good solutions for every lesson and project, runs each check
against them, and makes sure a deliberately broken solution still fails.

    python3 selftest.py
"""

import shutil
import sys
import tempfile
from pathlib import Path

import pycoach

SOLUTIONS = {
    1: 'print("Hello, world!")\n',
    2: '''name = input("What is your name? ")
age = int(input("How old are you? "))
print(f"Hi, {name}! You are {age} years old.")
print(f"Next year you will be {age + 1}.")
''',
    3: '''def receipt(item, price, quantity):
    total = price * quantity
    return f"{quantity} x {item} = ${total:.2f}"
''',
    4: '''def shout(text):
    return text.strip().upper() + "!!!"


def middle(text):
    return text[1:-1]
''',
    5: '''def ticket(age):
    if age < 5:
        return "free"
    elif age < 18:
        return "child"
    elif age < 65:
        return "adult"
    else:
        return "senior"


def is_weekend(day):
    return day in ("Sat", "Sun")
''',
    6: '''def total(n):
    result = 0
    for number in range(1, n + 1):
        result += number
    return result


def count_vowels(text):
    count = 0
    for letter in text:
        if letter in "aeiouAEIOU":
            count += 1
    return count


def countdown(n):
    out = ""
    while n > 0:
        out += str(n) + " "
        n -= 1
    return out.strip() + " Liftoff!"
''',
    7: '''def total(numbers):
    return sum(numbers)


def biggest(numbers):
    return max(numbers)


def keep_long(words, minimum):
    result = []
    for word in words:
        if len(word) >= minimum:
            result.append(word)
    return result
''',
    8: '''def full_name(user):
    return f"{user['first']} {user['last']}"


def find_user(directory, name):
    return directory.get(name, "unknown@example.com")
''',
    9: '''def tip_amount(bill, percent=15):
    return round(bill * percent / 100, 2)


def total_with_tip(bill, percent=15):
    return round(bill + tip_amount(bill, percent), 2)
''',
    10: '''def save_notes(notes, path):
    with open(path, "w") as file:
        for note in notes:
            file.write(note + "\\n")


def read_notes(path):
    result = []
    with open(path) as file:
        for line in file:
            result.append(line.rstrip("\\n"))
    return result


def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
''',
}

PROJECT_SOLUTION = {
    1: '''print("Welcome to Mad Libs!")

adjective = input("Give me an adjective: ")
noun = input("Give me a noun: ")
verb = input("Give me a verb: ")

print(f"The {adjective} {noun} {verb}!")
''',
    2: '''import random
import sys

if len(sys.argv) > 1:
    secret = int(sys.argv[1])
else:
    secret = random.randint(1, 10)

print("I'm thinking of a number between 1 and 10.")

while True:
    guess = int(input("Your guess? "))
    if guess > secret:
        print("Too high!")
    elif guess < secret:
        print("Too low!")
    else:
        print("Correct!")
        break
''',
    3: '''import os

TASK_FILE = "todo.txt"


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    tasks = []
    with open(TASK_FILE) as file:
        for line in file:
            tasks.append(line.rstrip("\\n"))
    return tasks


def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\\n")


tasks = load_tasks()

print("My to-do list")

while True:
    print("1) add a task")
    print("2) list tasks")
    print("3) quit")
    choice = input("Choice: ")

    if choice == "1":
        task = input("New task: ")
        tasks.append(task)
        save_tasks(tasks)
        print(f"Added: {task}")
    elif choice == "2":
        if not tasks:
            print("Nothing to do!")
        for number, task in enumerate(tasks, 1):
            print(f"{number}. {task}")
    elif choice == "3":
        break
''',
}

BROKEN = {
    1: 'print("Hello world")\n',
    2: 'print("TODO - replace me")\n',
    3: 'def receipt(item, price, quantity):\n    return "TODO"\n',
    5: 'def ticket(age):\n    return ""\n\n\ndef is_weekend(day):\n    return False\n',
    9: 'def tip_amount(bill, percent=15):\n    return 0\n\n\ndef total_with_tip(bill, percent=15):\n    return 0\n',
}


def run_case(path, tests, label):
    status, message, _ = pycoach.run_tests(path, tests)
    return status, message


def main():
    failures = []
    folder = Path(tempfile.mkdtemp(prefix="pycoach-selftest-"))

    lessons = pycoach.load_lessons()
    print("=" * 60)
    print("LESSONS: %d found" % len(lessons))
    print("=" * 60)
    for lesson in lessons:
        code = folder / ("lesson-%02d.py" % lesson["n"])
        code.write_text(SOLUTIONS[lesson["n"]], encoding="utf-8")
        status, message = run_case(code, lesson["tests"], "lesson %d" % lesson["n"])
        if status == "pass":
            print("  lesson %2d  GOOD SOLUTION  ->  pass" % lesson["n"])
        else:
            failures.append("lesson %d: good solution rejected: %s" % (lesson["n"], message))
            print("  lesson %2d  GOOD SOLUTION  ->  %s (%s)" % (lesson["n"], status, message))

        if lesson["n"] in BROKEN:
            code.write_text(BROKEN[lesson["n"]], encoding="utf-8")
            status, message = run_case(code, lesson["tests"], "lesson %d broken" % lesson["n"])
            if status == "pass":
                failures.append("lesson %d: broken solution was accepted!" % lesson["n"])
                print("  lesson %2d  BROKEN SOLUTION ->  pass  <-- PROBLEM")
            else:
                print("  lesson %2d  BROKEN SOLUTION ->  rejected as it should be" % lesson["n"])
        if lesson["quiz"]:
            for q in lesson["quiz"]:
                if not (0 <= q["index"] < len(q["choices"])):
                    failures.append("lesson %d: bad quiz question %r" % (lesson["n"], q["q"]))
        else:
            failures.append("lesson %d: no quiz questions parsed" % lesson["n"])

    print()
    print("=" * 60)
    print("PROJECTS: checking every step")
    print("=" * 60)
    for project in pycoach.load_projects():
        proj_dir = folder / ("project-%02d" % project["n"])
        proj_dir.mkdir(parents=True, exist_ok=True)
        for step in project["steps"]:
            code = proj_dir / step["filename"]
            code.write_text(PROJECT_SOLUTION[project["n"]], encoding="utf-8")
            status, message = run_case(code, step["check"],
                                       "project %d step %d" % (project["n"], step["n"]))
            if status == "pass":
                print("  project %d step %d  ->  pass" % (project["n"], step["n"]))
            else:
                failures.append("project %d step %d: %s" % (project["n"], step["n"], message))
                print("  project %d step %d  ->  %s: %s"
                      % (project["n"], step["n"], status, message.splitlines()[0]))
            if not step["hints"]:
                failures.append("project %d step %d: no hints" % (project["n"], step["n"]))

    shutil.rmtree(folder, ignore_errors=True)

    print()
    if failures:
        print("PROBLEMS FOUND (%d):" % len(failures))
        for item in failures:
            print("  - " + item)
        return 1
    print("ALL CONTENT CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
