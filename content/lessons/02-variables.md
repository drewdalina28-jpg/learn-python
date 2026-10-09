# Lesson 2 - Variables and input

## Objectives
- Store values in variables
- Read what the user types with `input()`
- Turn text into numbers with `int()`

## Lesson
A **variable** is a name that points at a value so you can use it later:

```python
name = "Ada"
age = 30
```

Now `name` always means `"Ada"` until you reassign it. Variable names should be descriptive and use underscores instead of spaces: `user_name`, `high_score`.

Python has no problem reusing a name:

```python
score = 0
score = score + 1   # score is now 1
```

**Reading the user.** `input()` pauses the program and waits for the person at the keyboard:

```python
name = input("What is your name? ")
print("Hello, " + name)
```

Whatever they type comes back as a **string**, even if they type digits. That is why this surprises beginners:

```python
age = input("How old are you? ")
print(age + 1)      # ERROR: you cannot add a number to text
```

Wrap it in `int()` to get a real number:

```python
age = int(input("How old are you? "))
print(age + 1)      # works
```

`int()` turns `"30"` into `30`. The reverse is `str()`, which turns `30` into `"30"` - Python will not do that for you silently.

## Exercise
Write a short program that asks for a name and an age, then prints two lines.

For an input of `Ada` and `30` the last two lines of output should be:

    Hi, Ada! You are 30 years old.
    Next year you will be 31.

Your prompts (`input("What is your name? ")`) are free to print whatever you like - only the last two lines are checked.

You will need `int()` for the "next year" line: text plus 1 is an error, a number plus 1 works.

## Hints
- The prompts can say anything, but the final two lines must match exactly, including punctuation.
- Read the age as a number: `age = int(input("How old are you? "))`.
- `age + 1` gives you next year - then it has to go back into text with an f-string: `f"Next year you will be {age + 1}."`

## Starter
```python
# Lesson 2 - introduce the user properly
name = input("What is your name? ")
age = input("How old are you? ")

# TODO: turn age into a number with int()
# TODO: print  Hi, <name>! You are <age> years old.
# TODO: print  Next year you will be <age + 1>.

print("TODO - replace me")
```

## Tests
```python
STDIN = "Ada\n30\n"

out, code = run_main()
check(code == 0,
      "your program ended with an error - read the traceback in the output above")
check("Hi, Ada! You are 30 years old." in out,
      "print a line reading exactly: Hi, Ada! You are 30 years old.")
check("Next year you will be 31." in out,
      "and a line reading exactly: Next year you will be 31.")

# run it again with someone else's details - nothing may be hard-coded
out2, code2 = run_main("Grace\n40\n")
check(code2 == 0,
      "a second run with different answers should work just as well")
check("Hi, Grace! You are 40 years old." in out2,
      "with the answers Grace and 40 you should print: Hi, Grace! You are 40 years old.")
check("Next year you will be 41." in out2,
      "and: Next year you will be 41.")
```

## Quiz
Q: What does `age = 30` do?
A) Prints the number 30
B) Makes the name age point at the value 30
C) Asks the user for 30
D) Deletes the number 30
ANSWER: B
WHY: the equals sign is assignment - the name on the left starts referring to the value on the right.

Q: `input()` always gives you...
A) a number
B) a string
C) a list
D) whatever the last variable was
ANSWER: B
WHY: even if the user types 30, input() returns the text "30". Convert it with int() when you need arithmetic.

Q: Which line reads a number from the user?
A) age = int(input("Age? "))
B) age = input("Age? ") + 1
C) print(input("Age? "))
D) age = number("Age? ")
ANSWER: A
WHY: input() gives text, and int() turns that text into a number in one go.

Q: What is wrong with `"5" + 1`?
A) Nothing, it gives 6
B) It gives "51"
C) It is an error - you cannot add text and a number
D) It gives 5.0
ANSWER: C
WHY: Python refuses to guess. Convert the text first with int("5").

Q: Which is the best variable name for a user's high score?
A) x
B) High Score
C) high_score
D) 2nd_place
ANSWER: C
WHY: readable, no spaces, and it does not start with a digit.
