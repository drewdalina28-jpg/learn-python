# Project - Number guessing game

## Overview
The computer picks a number from 1 to 10, you keep guessing, and it tells you whether you are too high or too low until you get it.

This project teaches `random`, `while` loops and comparing numbers - and because the program accepts an extra command-line argument for practice mode, the tests can play it in a completely predictable way.

Your file lives at:

    ~/pycoach-work/projects/project-02/guess.py

Recommended first: lessons 5, 6 and 9.

## Step 1: Pick a secret number
Set up the program like this:

- If a number was passed on the command line (`python3 guess.py 7`), use **that** as the secret - this is our practice mode, and it is how the checker plays you fairly.
- Otherwise pick one at random with `random.randint(1, 10)`.
- Print, exactly: `I'm thinking of a number between 1 and 10.`

You will need `import random` and `import sys` at the top. `sys.argv[1]` is the first extra argument.

### File
```
guess.py
```

### Starter
```python
# Number guessing game
import random
import sys

if len(sys.argv) > 1:
    secret = int(sys.argv[1])
else:
    secret = random.randint(1, 10)

print("I'm thinking of a number between 1 and 10.")
```

### Check
```python
out, code = run_main("1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n", timeout=15)
check(code == 0, "running it with no arguments should work - read the traceback above")
low = out.lower()
check("thinking of a number between 1 and 10" in low,
      "print this line exactly: I'm thinking of a number between 1 and 10.")

out2, code2 = run_main("7\n", args=["7"])
check(code2 == 0,
      "it must also run in practice mode: python3 guess.py 7")
```

### Hints
- `if len(sys.argv) > 1:` is how you ask "did I get an argument?"
- `int(sys.argv[1])` - the argument arrives as text, so convert it.

## Step 2: Ask for a guess
Ask the player for their guess using this prompt, word for word:

    Your guess? 

Store what they type and turn it into a number with `int()` - you will need it for comparing in the next step.

### File
```
guess.py
```

### Starter
```python
# Number guessing game
import random
import sys

if len(sys.argv) > 1:
    secret = int(sys.argv[1])
else:
    secret = random.randint(1, 10)

print("I'm thinking of a number between 1 and 10.")

guess = int(input("Your guess? "))
print("You typed", guess)
```

### Check
```python
out, code = run_main("5\n7\n", args=["7"])
check(code == 0,
      "it should ask a question, read the number, and finish cleanly")
low = out.lower()
check("your guess?" in low,
      "your prompt must be exactly: Your guess? ")
check("thinking of a number between 1 and 10" in low,
      "keep the welcome line from step 1")
```

### Hints
- `guess = int(input("Your guess? "))` does the asking and the converting in one go.
- The starter prints what you typed - replace that line when you move to step 3.

## Step 3: Give hints until they get it
Now compare the guess with the secret, over and over, printing exactly one of these after every guess:

    Too high!
    Too low!
    Correct!

Keep asking until they guess the secret - then stop. The game must ask **exactly three times** for the sequence 9, 5, 7 when the secret is 7: no question after "Correct!".

A `while True:` loop with a `break` on a correct guess is the natural shape here.

### File
```
guess.py
```

### Starter
```python
# Number guessing game
import random
import sys

if len(sys.argv) > 1:
    secret = int(sys.argv[1])
else:
    secret = random.randint(1, 10)

print("I'm thinking of a number between 1 and 10.")

while True:
    guess = int(input("Your guess? "))
    # TODO: compare guess with secret, print a hint,
    # and break out of the loop when they match
    break
```

### Check
```python
out, code = run_main("9\n5\n7\n", args=["7"])
check(code == 0, "the game should finish cleanly - read the traceback above")
low = out.lower()
check("too high" in low,
      "guessing 9 when the secret is 7 should print: Too high!")
check("too low" in low,
      "guessing 5 when the secret is 7 should print: Too low!")
check("correct" in low,
      "guessing 7 should print: Correct!")
check(low.count("your guess?") == 3,
      "it should ask exactly 3 times for the guesses 9, 5 and 7 "
      "(found %d questions)" % low.count("your guess?"))
```

### Hints
- Two comparisons and an `else`: `if guess > secret:` ... `elif guess < secret:` ... `else:` is the match.
- The `break` belongs where you print "Correct!" - the loop is what keeps asking.

## Step 4: Play a real game
Remove any leftover debugging print, then make sure a **real** game works: no argument, a secret from `random.randint`, and guesses until the player lands on it.

Use **[x] run it** and play a few rounds yourself. Then let the checker verify that a full set of guesses always ends the game.

### File
```
guess.py
```

### Starter
```python
# Number guessing game
import random
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
```

### Check
```python
guesses = "7\n3\n9\n1\n5\n10\n2\n8\n4\n6\n"
out, code = run_main(guesses, timeout=15)
check(code == 0,
      "guessing numbers until you hit the secret must end the game cleanly")
low = out.lower()
check("thinking of a number between 1 and 10" in low, "keep the welcome line")
check("correct" in low,
      "somewhere in those guesses it should print: Correct!")
asked = low.count("your guess?")
check(1 <= asked <= 10,
      "it should ask once per guess and stop on a correct one - found %d questions"
      % asked)
```

### Hints
- Your `while True:` loop must stop on the correct guess - check that `break` really is inside the `else:` branch.
- Press [x] to play it yourself: type a number, press Enter, keep going.
