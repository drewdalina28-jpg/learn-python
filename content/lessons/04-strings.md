# Lesson 4 - Working with strings

## Objectives
- Reach into a string with indexing and slicing
- Measure text with `len()`
- Reshape text with string methods

## Lesson
Strings are sequences of characters, so you can point at particular ones by their position - starting from **0**:

```python
word = "Python"
word[0]      # 'P'
word[5]      # 'n'
word[-1]     # 'n'   (negative counts from the end)
```

**Slicing** takes a piece: `word[a:b]` means "from a up to, but not including, b".

```python
word[0:3]    # 'Pyt'
word[3:]     # 'hon'
word[:]      # 'Python'  (a copy of the whole thing)
```

Ask how long something is with `len()`:

```python
len("Python")    # 6
```

**Methods** are functions that belong to the value itself - you call them with a dot:

```python
"  hi there  ".strip()      # 'hi there'   (removes spaces at both ends)
"hi there".upper()          # 'HI THERE'
"HI THERE".lower()          # 'hi there'
"a,b,c".split(",")          # ['a', 'b', 'c']  - a list of pieces
" - ".join(['a', 'b'])      # 'a - b'          - glues a list together
"hello".replace("l", "L")   # 'heLLo'
```

A string never changes by itself: `s.strip()` **returns** a new string, so you must do `s = s.strip()` to keep the result.

Two more useful tricks:

```python
"hello".startswith("he")    # True
"price: 9.99" in "the price: 9.99 today"   # True  - "is this piece in there?"
```

## Exercise
Write two small functions.

`shout(text)` - strips the spaces off both ends, shouts it in capitals, and adds three exclamation marks:

    >>> shout("  hey there  ")
    'HEY THERE!!!'

`middle(text)` - returns everything except the first and last character:

    >>> middle("hello")
    'ell'
    >>> middle("py")
    ''

## Hints
- `strip()` only removes spaces at the ends - you still have to call `.upper()` and add the `!`.
- Slicing starts at 1 and stops before -1: `text[1:-1]`.
- For a one or two character string, `[1:-1]` already gives you an empty string - no special case needed.

## Starter
```python
# Lesson 4 - string surgery
def shout(text):
    """Strip it, shout it, add !!!"""
    return text


def middle(text):
    """Everything except the first and last character"""
    return text
```

## Tests
```python
check(shout("  hey there  ") == "HEY THERE!!!",
      "shout('  hey there  ') should give 'HEY THERE!!!'")
check(shout("ok") == "OK!!!",
      "shout('ok') should give 'OK!!!'")
check(shout("PyThOn") == "PYTHON!!!",
      "shout should work whatever the input looks like")
check(middle("hello") == "ell",
      "middle('hello') should give 'ell'")
check(middle("py") == "",
      "middle('py') should give an empty string")
check(middle("!") == "",
      "middle('!') should give an empty string")
```

## Quiz
Q: If `word = "Python"`, what is `word[1]`?
A) P
B) y
C) Py
D) h
ANSWER: B
WHY: positions start at 0, so word[0] is P and word[1] is y.

Q: What is `word[0:3]` when word = "Python"?
A) pyt
B) Pyt
C) Pyth
D) Pytho
ANSWER: B
WHY: slicing takes characters 0, 1 and 2 - the end index is never included.

Q: `"  hi  ".strip()` returns...
A) 'hi'
B) '  hi  '
C) None
D) ' hi '
ANSWER: A
WHY: strip() removes spaces at both ends. Nothing changes until you use the value it returns.

Q: Which line turns "a,b,c" into ['a', 'b', 'c']?
A) "a,b,c".split(",")
B) "a,b,c".join(",")
C) "a,b,c".replace(",")
D) "a,b,c".cut(",")
ANSWER: A
WHY: split() chops one string into a list of pieces using your separator.

Q: How many characters are in `"Termux"`?
A) 5
B) 6
C) 7
D) 12
ANSWER: B
WHY: len("Termux") is 6 - the quotes are not part of the string.
