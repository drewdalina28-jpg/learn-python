# Lesson 10 - Files and errors

## Objectives
- Read and write text files safely
- Handle mistakes with `try` / `except`
- Write code that fails gracefully

## Lesson
Your programs forget everything when they stop. Files are how data survives.

```python
with open("notes.txt", "w") as file:
    file.write("buy milk\n")
    file.write("walk the dog\n")
```

The second argument is the mode: `"w"` writes (creating or **overwriting**), `"a"` appends, `"r"` reads. Always use `with` - it closes the file for you, even if something goes wrong halfway.

Reading gives you one line at a time:

```python
with open("notes.txt") as file:
    for line in file:
        print(line.strip())
```

Call `.strip()` or `.rstrip("\n")` - every line from a file arrives with a newline hanging off the end.

**Errors.** Ordinary mistakes stop your program with a traceback. You can catch them:

```python
try:
    number = int(input("Pick a number: "))
except ValueError:
    print("That was not a number!")
except ZeroDivisionError:
    print("No dividing by zero")
else:
    print("All good")
finally:
    print("This runs no matter what")
```

The important habit: catch the error you actually expect (`ValueError`, `FileNotFoundError`, `ZeroDivisionError`) instead of a bare `except:` that hides every problem.

Opening a file that does not exist raises `FileNotFoundError`, which you can test for yourself:

```python
import os
os.path.exists("notes.txt")    # True or False, no error raised
```

## Exercise
Three functions.

`save_notes(notes, path)` writes one line per item into a file:

    save_notes(["buy milk", "walk the dog"], "notes.txt")

`read_notes(path)` reads that file back into a list of strings, without the newline characters:

    read_notes("notes.txt")  ->  ['buy milk', 'walk the dog']

`safe_divide(a, b)` divides, but returns `None` instead of crashing when `b` is zero:

    safe_divide(10, 2)   -> 5.0
    safe_divide(10, 0)   -> None

## Hints
- Write with `open(path, "w")` inside a `with`, looping over the notes and adding `"\n"` to each one.
- Read with `open(path)` inside a `with`, and build a list with `.append(line.rstrip("\n"))`.
- `safe_divide` is a `try:` around `return a / b` with an `except ZeroDivisionError:` that returns `None`.

## Starter
```python
# Lesson 10 - files and errors
def save_notes(notes, path):
    """Write each note on its own line"""
    pass


def read_notes(path):
    """Read the file back into a list of lines"""
    return []


def safe_divide(a, b):
    """a / b, or None when b is zero"""
    return None
```

## Tests
```python
import os
import tempfile

check(safe_divide(10, 2) == 5.0, "safe_divide(10, 2) should be 5.0")
check(safe_divide(9, 3) == 3.0, "safe_divide(9, 3) should be 3.0")
check(safe_divide(10, 0) is None,
      "safe_divide(10, 0) should return None instead of raising an error")

folder = tempfile.mkdtemp()
path = os.path.join(folder, "notes.txt")

save_notes(["buy milk", "walk the dog"], path)
check(os.path.exists(path), "save_notes should create the file at that path")

lines = read_notes(path)
check(isinstance(lines, list), "read_notes should return a list")
check(lines == ["buy milk", "walk the dog"],
      "read_notes should give back exactly the lines that were saved, got %r" % (lines,))
check("\n" not in "".join(lines),
      "strip the newline characters off each line")

save_notes(["one"], path)
check(read_notes(path) == ["one"],
      "writing again should replace the old contents, not add to them")
```

## Quiz
Q: What does open("data.txt", "w") do?
A) Reads the file
B) Creates or overwrites the file for writing
C) Deletes the file
D) Checks whether the file exists
ANSWER: B
WHY: w means write - it starts the file empty, so old contents are lost. Use "a" to append instead.

Q: Why is `with` used around file operations?
A) It makes the code shorter only
B) It closes the file automatically, even if an error happens
C) It opens the file twice
D) It encrypts the file
ANSWER: B
WHY: the file is guaranteed to be closed when the block ends, which prevents lost data and locked files.

Q: Which error does `int("hello")` raise?
A) FileNotFoundError
B) ValueError
C) ZeroDivisionError
D) TypeError
ANSWER: B
WHY: the text cannot be turned into a number, and that is what ValueError means.

Q: What does this return when b is 0?

    try:
        return a / b
    except ZeroDivisionError:
        return None
A) It crashes
B) None
C) 0
D) False
ANSWER: B
WHY: the exception is caught, so the except block runs and None is handed back.

Q: Which line asks "does this file exist?" without risking an error?
A) open(path)
B) os.path.exists(path)
C) read(path)
D) path.is_there()
ANSWER: B
WHY: exists() simply answers True or False, while open() would raise FileNotFoundError.
