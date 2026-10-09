# Lesson 5 - Making decisions

## Objectives
- Compare values with `==`, `<`, `>=` and friends
- Branch your program with `if`, `elif` and `else`
- Combine questions with `and`, `or` and `not`

## Lesson
A program that always does the same thing is boring. `if` lets it choose:

```python
temperature = 30

if temperature > 25:
    print("It is warm")
elif temperature > 10:
    print("It is mild")
else:
    print("It is cold")
```

Python checks the conditions from top to top, and runs **only the first one that is true**. The block under it is indented by four spaces - that indentation is how Python knows what belongs to the `if`.

Comparisons you can use:

```python
==   !=   <   >   <=   >=
5 == 5      # True
5 != 4      # True
5 >= 10     # False
```

Careful: `=` assigns, `==` asks a question.

Answers come back as **booleans**: `True` or `False` (capital letters).

Combine questions:

```python
if age >= 18 and has_ticket:
    print("Come in")

if day == "Sat" or day == "Sun":
    print("Weekend!")

if not is_raining:
    print("No umbrella needed")
```

You can also test numbers directly - Python treats non-empty text and any non-zero number as true:

```python
if age:                 # true as long as age is not 0
    print("You exist")
```

`in` is a lovely shortcut for "is this in there?":

```python
if day in ("Sat", "Sun"):
    print("Weekend!")
```

## Exercise
Two functions this time.

`ticket(age)` decides the price group and returns one word:

    ticket(3)   -> 'free'     (under 5)
    ticket(7)   -> 'child'    (5 up to, but not including, 18)
    ticket(30)  -> 'adult'    (18 up to, but not including, 65)
    ticket(70)  -> 'senior'   (65 and over)

`is_weekend(day)` returns the boolean `True` when day is `"Sat"` or `"Sun"`, and `False` otherwise. Note: `True` and `False`, not `"yes"` and `"no"`.

## Hints
- Order matters: check the youngest group first with `if`, then `elif` for the rest.
- `ticket(5)` must be 'child' - so write `age < 18`, not `age <= 18`.
- For the weekend, `day in ("Sat", "Sun")` returns exactly the True/False you need.

## Starter
```python
# Lesson 5 - decide!
def ticket(age):
    """Return 'free', 'child', 'adult' or 'senior'"""
    return ""


def is_weekend(day):
    """True for Sat and Sun, False otherwise"""
    return False
```

## Tests
```python
cases = [(3, "free"), (4, "free"), (5, "child"), (17, "child"),
         (18, "adult"), (64, "adult"), (65, "senior"), (90, "senior")]
for age, want in cases:
    got = ticket(age)
    check(got == want,
          "ticket(%d) should return %r but returned %r" % (age, want, got))

check(is_weekend("Sat") is True, "is_weekend('Sat') should return True")
check(is_weekend("Sun") is True, "is_weekend('Sun') should return True")
check(is_weekend("Mon") is False, "is_weekend('Mon') should return False")
check(is_weekend("Friday") is False, "is_weekend('Friday') should return False")
```

## Quiz
Q: Which symbol asks "are these two values equal"?
A) =
B) ==
C) !=
D) =>
ANSWER: B
WHY: a single = stores a value; == compares two values and answers True or False.

Q: In `if x > 5:` the indented lines below run when...
A) x is less than 5
B) x is exactly 5
C) x is greater than 5
D) never
ANSWER: C
WHY: the indented block belongs to the condition directly above it, and runs only when it is True.

Q: What does `10 >= 10` give?
A) True
B) False
C) 10
D) an error
ANSWER: A
WHY: >= means "greater than or equal to", and 10 is equal to 10.

Q: If day = "Tue", what is `day in ("Sat", "Sun")`?
A) "Tue"
B) True
C) False
D) an error
ANSWER: C
WHY: in asks whether the value appears in the group. Tuesday does not, so the answer is False.

Q: Which one is spelled correctly in Python?
A) if x == 5 then print("yes")
B) if x == 5: print("yes")
C) if x == 5 { print("yes") }
D) if x = 5: print("yes")
ANSWER: B
WHY: Python wants a colon at the end of the if line and indentation instead of braces.
