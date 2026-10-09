# Project - Mad Libs

## Overview
A mad lib is a story with holes in it. You ask the player for random words, then read the story back with their words dropped in - usually to ridiculous effect.

It is the perfect first project: mostly `input()` and f-strings, and when you are done a friend can actually play it.

Your file lives at:

    ~/pycoach-work/projects/project-01/story.py

Read each step, write the code, then press **[r] run the check**. If it fails, read the message - it tells you what the test expected.

Recommended first: lessons 1 to 5.

## Step 1: Say hello and ask for an adjective
Start with a header line that is printed **exactly** like this:

    Welcome to Mad Libs!

Then ask the player for the first word. Your prompt must contain the word "adjective" so they know what to type, for example:

    Give me an adjective:

`input()` shows the question and waits - store what comes back in a variable called `adjective`.

### File
```
story.py
```

### Starter
```python
# Mad Libs - built up one step at a time
print("Welcome to Mad Libs!")

# TODO: ask for an adjective and keep the answer
```

### Check
```python
STDIN = "silly\ncat\ndanced\n"

out, code = run_main()
check(code == 0, "your program stopped with an error - read the traceback above")
low = out.lower()
check("welcome to mad libs!" in low,
      "print this line exactly: Welcome to Mad Libs!")
check("adjective" in low,
      "your first question should contain the word 'adjective'")
```

### Hints
- `adjective = input("Give me an adjective: ")` asks and stores in one line.
- The welcome line needs its capital W and its exclamation mark.

## Step 2: Collect a noun and a verb too
Ask two more questions, in this order, storing the answers in `noun` and `verb`:

1. an adjective - prompt contains "adjective"
2. a noun - prompt contains "noun"
3. a verb - prompt contains "verb"

Keep the welcome line at the top. Nothing is printed with these words yet - that comes next.

### File
```
story.py
```

### Starter
```python
# Mad Libs - built up one step at a time
print("Welcome to Mad Libs!")

adjective = input("Give me an adjective: ")
noun = input("Give me a noun: ")
verb = input("Give me a verb: ")

# TODO: step 3 - put them into a story
```

### Check
```python
STDIN = "silly\ncat\ndanced\n"

out, code = run_main()
check(code == 0, "your program stopped with an error - read the traceback above")
low = out.lower()
for word in ("adjective", "noun", "verb"):
    check(word in low, "ask the player for a %s as well" % word)
check(low.index("adjective") < low.index("noun") < low.index("verb"),
      "ask for them in this order: adjective, noun, verb")
```

### Hints
- Three `input()` lines, each stored in its own variable.
- The order the questions appear in the output is the order you wrote them in.

## Step 3: Tell the story
Finally, print the finished story as the last line of output. It must read exactly:

    The silly cat danced!

That is: `The `, your adjective, a space, the noun, a space, the verb, then `!`. Build it with an f-string:

    print(f"The {adjective} {noun} {verb}!")

Try it for real with **[x] run it** and type some words in yourself.

### File
```
story.py
```

### Starter
```python
# Mad Libs - built up one step at a time
print("Welcome to Mad Libs!")

adjective = input("Give me an adjective: ")
noun = input("Give me a noun: ")
verb = input("Give me a verb: ")

# TODO: print the story using an f-string
```

### Check
```python
STDIN = "silly\ncat\ndanced\n"
out, code = run_main()
check(code == 0, "your program stopped with an error - read the traceback above")
check("The silly cat danced!" in out,
      "the finished story should be exactly: The silly cat danced!")

out2, code2 = run_main("brave\ndog\nbarked\n")
check(code2 == 0, "a second run should work just as well")
check("The brave dog barked!" in out2,
      "it must use the words the player typed, not hard-coded ones")
check("The silly cat danced!" not in out2,
      "the story has to change when the answers change")
```

### Hints
- One `print(f"...")` line using the three variables.
- The second part of the check runs your program again with different words - so the story has to be built from the variables, not typed in as a fixed sentence.
