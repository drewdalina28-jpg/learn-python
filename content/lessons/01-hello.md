# Lesson 1 - Hello, world!

## Objectives
- Know what a Python file is
- Use `print()` to show text on the screen
- Fix and run your very first program

## Lesson
A Python program is just a text file whose name ends in `.py`. Python reads it from the top and does what it says, one line after another.

The most famous first line is `print()`. It shows something on the screen:

```python
print("Hello, world!")
```

Everything between the quote marks is a **string** - a piece of text. You can use double quotes (`"`) or single quotes (`'`); Python treats them the same.

You can print as many lines as you like - each `print()` starts a new line:

```python
print("Good morning")
print("Good afternoon")
print("Good evening")
```

That program would show three lines.

To run a file yourself in Termux:

    python3 hello.py

Strings can also be joined with `+`, which is handy when you want one line made of several pieces:

```python
print("My name is " + "Ada")
```

## Exercise
The file waiting for you prints the **wrong** greeting. Change it so that running the file prints exactly one line:

    Hello, world!

Rules:
- Exactly one line of output
- Starts with a capital H, ends with `!`
- No extra spaces before or after

Use **[x] run it for real** to see what your program does right now, then fix it.

## Hints
- The wrong line is already there - only the text inside the quote marks needs to change.
- Watch the punctuation: `Hello, world!` has a comma and an exclamation mark, nothing else.

## Starter
```python
# Lesson 1 - make this print exactly one line: Hello, world!
print("Goodbye, world.")
```

## Tests
```python
text = OUTPUT.strip()
check(text == "Hello, world!",
      "your file should print exactly: Hello, world!")
check(len(text.splitlines()) == 1,
      "print it just once - right now you are printing %d lines" % len(text.splitlines()))
```

## Quiz
Q: What does `print("Hi")` do?
A) It stores the text "Hi" for later
B) It shows Hi on the screen
C) It asks the user to type something
D) It deletes the text
ANSWER: B
WHY: print() sends its argument to the terminal so you can see it.

Q: Which of these is a string?
A) 42
B) "42"
C) hello
D) print
ANSWER: B
WHY: A string is text wrapped in quote marks. Without quotes, hello would be a name Python has never heard of.

Q: Which command runs a file called game.py?
A) open game.py
B) python3 game.py
C) run game.py
D) .game.py
ANSWER: B
WHY: you hand the file to the python3 program, which reads and executes it.

Q: Every `print()` starts a new line.
A) True
B) False
ANSWER: A
WHY: that is exactly what print() is for - one call, one new line of output.
