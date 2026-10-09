# Project - To-do list

## Overview
A command-line to-do list: you add tasks, list them, and they are still there tomorrow because they get saved to a file.

It is the project that pulls together everything from the course - a menu built from `input()`, a list that grows, a loop that prints it, and a file that keeps it.

Your file lives at:

    ~/pycoach-work/projects/project-03/todo.py

The tasks are saved in `todo.txt` **in that same folder**, which is what the checker looks at.

Recommended first: lessons 1 to 8 (files help too, but lesson 10 is not required).

## Step 1: The header and the menu
Start your program with a header line printed exactly like this:

    My to-do list

Then show a menu, and ask for a choice. This is the flow the rest of the project expects:

    1) add a task
    2) list tasks
    3) quit
    Choice: 

Reading the choice and quitting straight away should end the program cleanly.

### File
```
todo.py
```

### Starter
```python
# My to-do list
print("My to-do list")

# TODO: show the menu and read the choice
choice = input("Choice: ")
```

### Check
```python
STDIN = "3\n"

out, code = run_main()
check(code == 0, "choosing 3 should quit cleanly - read the traceback above")
low = out.lower()
check("my to-do list" in low,
      "print this line exactly: My to-do list")
check("add" in low and "list" in low,
      "show a menu with an 'add a task' option and a 'list tasks' option")
check("choice" in low,
      "ask for a choice - the word 'choice' should be in your prompt")
```

### Hints
- `print()` the two menu lines, then `choice = input("Choice: ")`.
- Nothing needs to happen for choice 3 yet - finishing without an error is enough.

## Step 2: Add a task
When the player picks `1`, ask them for the task with a prompt that contains the word "task", store it in a list, and confirm it with a line containing the word "added" and the task itself:

    Added: buy milk

Start with an empty list at the top of your file - `tasks = []`. After adding, go back to showing the menu so they can carry on. A `while True:` loop around the menu is the usual shape, with `break` when they choose 3.

The checker will pick 1, type `buy milk`, then pick 3.

### File
```
todo.py
```

### Starter
```python
# My to-do list
tasks = []

print("My to-do list")

while True:
    print("1) add a task")
    print("2) list tasks")
    print("3) quit")
    choice = input("Choice: ")

    if choice == "1":
        # TODO: ask for the task, append it, confirm with "Added: ..."
        pass
    elif choice == "3":
        break
```

### Check
```python
import os

task_file = os.path.join(HERE, "todo.txt")
if os.path.exists(task_file):
    os.remove(task_file)

STDIN = "1\nbuy milk\n3\n"
out, code = run_main()
check(code == 0, "add a task, then quit - read the traceback above")
low = out.lower()
check("task" in low, "ask the player for the task - the word 'task' should be in your prompt")
check("added" in low, "confirm the addition with a line containing: Added")
check("buy milk" in out, "echo the task back: Added: buy milk")
```

### Hints
- Inside `if choice == "1":` you need `task = input("New task: ")`, `tasks.append(task)`, then `print(f"Added: {task}")`.
- The menu must appear again after adding - that means the menu lives inside a loop.

## Step 3: List the tasks
When the player picks `2`, print every task numbered, one per line, in exactly this format:

    1. buy milk
    2. walk dog

That is the number, a dot, a space, then the task. If there is nothing in the list, say so with a line containing "nothing" - for example: `Nothing to do!`

The checker will add `buy milk`, add `walk dog`, then list them.

### File
```
todo.py
```

### Starter
```python
# My to-do list
tasks = []

print("My to-do list")

while True:
    print("1) add a task")
    print("2) list tasks")
    print("3) quit")
    choice = input("Choice: ")

    if choice == "1":
        task = input("New task: ")
        tasks.append(task)
        print(f"Added: {task}")
    elif choice == "2":
        # TODO: print every task as: 1. buy milk
        pass
    elif choice == "3":
        break
```

### Check
```python
import os

task_file = os.path.join(HERE, "todo.txt")
if os.path.exists(task_file):
    os.remove(task_file)

STDIN = "1\nbuy milk\n1\nwalk dog\n2\n3\n"
out, code = run_main()
check(code == 0, "add two tasks, list them, quit - read the traceback above")
check("1. buy milk" in out,
      "print the first task as exactly: 1. buy milk")
check("2. walk dog" in out,
      "print the second task as exactly: 2. walk dog")
```

### Hints
- A `for` loop with `enumerate(tasks, 1)` gives you the number and the task together:
  `for number, task in enumerate(tasks, 1):`
- Then `print(f"{number}. {task}")`.

## Step 4: Remember the tasks
Right now everything is lost when the program stops. Fix that:

- When a task is added, save the whole list to `todo.txt` in your program's own folder (overwriting it each time).
- When the program starts, load `todo.txt` back into `tasks` - and if the file does not exist yet, start with an empty list instead of crashing.

`with open("todo.txt", "w") as file:` writes, `with open("todo.txt") as file:` reads, and `line.rstrip("\n")` takes the newline back off each line as it comes in.

Then play it for real with **[x] run it**: add something, quit, run it again - it should still be there.

### File
```
todo.py
```

### Starter
```python
# My to-do list
import os

TASK_FILE = "todo.txt"

def load_tasks():
    """Everything saved in todo.txt, or an empty list."""
    if not os.path.exists(TASK_FILE):
        return []
    tasks = []
    with open(TASK_FILE) as file:
        for line in file:
            tasks.append(line.rstrip("\n"))
    return tasks


def save_tasks(tasks):
    """Write the whole list back to todo.txt."""
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")


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
        for number, task in enumerate(tasks, 1):
            print(f"{number}. {task}")
    elif choice == "3":
        break
```

### Check
```python
import os

task_file = os.path.join(HERE, "todo.txt")
if os.path.exists(task_file):
    os.remove(task_file)

# 1. add something, then quit
out, code = run_main("1\nbuy milk\n3\n")
check(code == 0, "adding a task should work - read the traceback above")
check(os.path.exists(task_file),
      "the tasks must be saved to a file called todo.txt next to your program")

# 2. a brand new run should still see it
out2, code2 = run_main("2\n3\n")
check(code2 == 0, "listing on a fresh run should work")
check("buy milk" in out2,
      "the saved task should still be there on the next run")

# 3. no file at all must not crash
os.remove(task_file)
out3, code3 = run_main("3\n")
check(code3 == 0,
      "running when todo.txt does not exist must not crash - start with an empty list")
```

### Hints
- Call `save_tasks(tasks)` right after `tasks.append(task)`.
- `load_tasks()` returning `[]` when the file is missing is what stops the crash - test it by deleting todo.txt and running again.
