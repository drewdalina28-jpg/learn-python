# Lesson 9 - Functions

## Objectives
- Package logic into `def` and call it anywhere
- Return a value instead of only printing
- Give parameters default values

## Lesson
A function is a named piece of logic you can run as many times as you like:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Ada")     # Hello, Ada!
greet("Grace")   # Hello, Grace!
```

The line under `def` is where the work happens - **return** hands a value back to the caller:

```python
def double(n):
    return n * 2

answer = double(21)    # 42
```

`return` and `print()` are not the same thing:
- `print()` just shows text on the screen and gives back nothing.
- `return` gives a value to whoever called the function, so you can use it.

A function with no `return` gives back `None`.

**Parameters** are the names in the brackets; **arguments** are what you pass in:

```python
def area(width, height):
    return width * height

area(3, 4)      # 12
```

Parameters can have **default values**, which are used when the caller leaves them out:

```python
def tip(bill, percent=15):
    return bill * percent / 100

tip(100)        # 15.0   - the default kicks in
tip(100, 20)    # 20.0   - the default is overridden
```

Rules worth learning early:
- Parameters with defaults must come last: `def f(a, b=2, c=3)` is fine, `def f(a=1, b)` is not.
- Names inside a function are local - changing them there does not touch the outside.
- Keep functions small and give them one clear job. If you cannot say what it does in a sentence, it is doing too much.

## Exercise
A tiny tip calculator.

`tip_amount(bill, percent=15)` returns the tip, rounded to 2 decimals:

    tip_amount(100)         -> 15.0     (15% by default)
    tip_amount(100, 20)     -> 20.0
    tip_amount(33.5, 10)    -> 3.35

`total_with_tip(bill, percent=15)` uses `tip_amount()` to work out the bill including the tip:

    total_with_tip(100)     -> 115.0
    total_with_tip(50, 10)  -> 55.0

Round with the built-in `round(number, 2)`.

## Hints
- The tip is `bill * percent / 100` - wrap it in `round(..., 2)`.
- `total_with_tip` should not repeat the maths: call `tip_amount(bill, percent)` and add it to the bill.
- Remember to write `percent=15` in **both** functions, so the default works for each of them.

## Starter
```python
# Lesson 9 - functions
def tip_amount(bill, percent=15):
    """The tip, rounded to 2 decimals"""
    return 0


def total_with_tip(bill, percent=15):
    """The bill plus the tip, rounded to 2 decimals"""
    return 0
```

## Tests
```python
check(tip_amount(100) == 15.0,
      "the default is 15%: tip_amount(100) should be 15.0")
check(tip_amount(100, 20) == 20.0,
      "tip_amount(100, 20) should be 20.0")
check(tip_amount(33.5, 10) == 3.35,
      "tip_amount(33.5, 10) should be 3.35")
check(tip_amount(80, 0) == 0.0,
      "a 0% tip is 0")

check(total_with_tip(100) == 115.0,
      "total_with_tip(100) should be 115.0")
check(total_with_tip(50, 10) == 55.0,
      "total_with_tip(50, 10) should be 55.0")
check(total_with_tip(9.99) == 11.49,
      "total_with_tip(9.99) should be 11.49 (9.99 + 1.50)")
```

## Quiz
Q: Which keyword defines a function?
A) func
B) def
C) function
D) define
ANSWER: B
WHY: def short for "define" - the name and brackets follow immediately.

Q: What is the difference between print(x) and return x?
A) They are identical
B) print shows x on screen; return hands x back to the caller
C) return shows x on screen
D) print can only take one argument
ANSWER: B
WHY: a returned value can be stored and reused; printed text is only for looking at.

Q: In `def tip(bill, percent=15)`, what does `tip(200)` give?
A) An error - percent is missing
B) percent is 15, so 15% of 200
C) percent is 0
D) 200
ANSWER: B
WHY: a parameter with a default is optional - when it is left out, the default is used.

Q: Where must parameters with default values go?
A) First
B) Last
C) Anywhere
D) Outside the brackets
ANSWER: B
WHY: otherwise Python could not tell which missing argument belongs to which parameter.

Q: A variable created inside a function is...
A) Visible everywhere in the program
B) Local - it only exists while the function runs
C) Deleted immediately
D) Always global
ANSWER: B
WHY: the function gets its own copy of the name, so the rest of the program is unaffected.
