# Lesson 3 - Numbers and f-strings

## Objectives
- Do arithmetic with Python's operators
- Tell `int` and `float` apart
- Build tidy text with f-strings

## Lesson
Python is a calculator first. These all work:

```python
7 + 3      # 10
7 - 3      # 4
7 * 3      # 21
7 / 3      # 2.333...  (always a decimal)
7 // 3     # 2          (division that throws the remainder away)
7 % 3      # 1          (the remainder - "mod")
7 ** 3     # 343        (7 to the power of 3)
```

Two kinds of number:
- **int** - whole numbers: `30`, `-4`, `1000`
- **float** - decimals: `3.14`, `-0.5`, `2.0`

Mixing them in a calculation gives a float. `%` (the remainder) is surprisingly useful - it answers "is this even?" (`n % 2 == 0`) and wraps numbers around a clock (`(14 + 10) % 24`).

**f-strings** are the nice way to build text out of values. Put an `f` before the quote and drop values inside braces:

```python
name = "Ada"
age = 30
print(f"Hi {name}, you are {age} years old.")
```

They can contain real expressions, not just names:

```python
print(f"In five years you will be {age + 5}.")
```

And they can format numbers, for example always showing two decimal places:

```python
price = 12
print(f"Total: {price:.2f}")     # Total: 12.00
```

## Exercise
Write a function `receipt(item, price, quantity)` that returns one line of a shop receipt, always with two decimals.

For example:

    >>> receipt("Apple", 1.75, 2)
    '2 x Apple = $3.50'
    >>> receipt("Book", 12, 1)
    '1 x Book = $12.00'
    >>> receipt("Pen", 0.5, 10)
    '10 x Pen = $5.00'

Build it with an f-string - the `:.2f` part is what forces two decimal places.

## Hints
- First work out the total: `price * quantity`.
- Then one f-string: `f"{quantity} x {item} = ${total:.2f}"`.
- The dollar sign sits outside the braces, and there is a space on each side of the `x`.

## Starter
```python
# Lesson 3 - build a receipt line
def receipt(item, price, quantity):
    """Return a line like: 2 x Apple = $3.50"""
    total = 0
    return f"TODO {item}"
```

## Tests
```python
check(receipt("Apple", 1.75, 2) == "2 x Apple = $3.50",
      "2 apples at 1.75 should give: 2 x Apple = $3.50")
check(receipt("Book", 12, 1) == "1 x Book = $12.00",
      "prices need two decimals even when they are whole: 1 x Book = $12.00")
check(receipt("Pen", 0.5, 10) == "10 x Pen = $5.00",
      "10 pens at 0.5 should give: 10 x Pen = $5.00")
```

## Quiz
Q: What is `7 / 2`?
A) 3
B) 3.5
C) 4
D) an error
ANSWER: B
WHY: a single slash always performs true division and gives a float.

Q: What is `7 // 2`?
A) 3.5
B) 3
C) 4
D) 7
ANSWER: B
WHY: double slash divides and throws the remainder away, leaving a whole number.

Q: `13 % 5` is...
A) 1
B) 2
C) 3
D) 6.5
ANSWER: C
WHY: 5 goes into 13 twice (10), and 13 - 10 leaves a remainder of 3. The % operator gives you that remainder.

Q: What does `f"{price:.2f}"` do?
A) Prints the variable named price:.2f
B) Shows price with exactly two decimal places
C) Multiplies price by 2
D) Rounds price to 2
ANSWER: B
WHY: the part after the colon is a format specification - .2f means two decimals, as a float.

Q: `3 + 4 * 2` equals...
A) 14
B) 11
C) 20
D) 9
ANSWER: B
WHY: multiplication happens before addition, so 4*2 is done first.
