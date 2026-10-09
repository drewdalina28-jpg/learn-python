# Lesson 6 - Loops

## Objectives
- Repeat work with `for` and `range()`
- Keep going with `while`
- Escape early with `break` and `continue`

## Lesson
When you want to do something many times, you loop.

```python
for letter in "abc":
    print(letter)
```

`range()` gives you a run of numbers:

```python
range(5)      # 0, 1, 2, 3, 4   (it stops before the end number)
range(2, 6)   # 2, 3, 4, 5
range(0, 10, 2)   # 0, 2, 4, 6, 8   (the third number is the step)
```

```python
for n in range(3):
    print("Attempt", n)
```

**while** repeats as long as a condition stays true. Use it when you do not know how many rounds you need:

```python
n = 100
while n > 0:
    print(n)
    n = n // 2      # 100, 50, 25, 12, 6, 3, 1
```

If you never change `n`, that loop would run forever - a very common bug.

Two ways to steer:
- `break` - leave the loop immediately
- `continue` - skip to the next round

```python
for n in range(10):
    if n == 3:
        continue        # this round stops here
    if n == 6:
        break           # the whole loop stops
    print(n)            # 0, 1, 2, 4, 5
```

A `for` loop walks over anything that is a sequence: a string, a list, a range.

## Exercise
Three functions, all built from loops.

`total(n)` adds up every whole number from 1 to n:

    total(5)   -> 15      (1+2+3+4+5)
    total(10)  -> 55
    total(1)   -> 1

`count_vowels(text)` counts the vowels a e i o u (either case):

    count_vowels("hello world")  -> 3
    count_vowels("xyz")          -> 0

`countdown(n)` builds a string of the numbers falling to 1, then a lift-off:

    countdown(3)  -> '3 2 1 Liftoff!'
    countdown(1)  -> '1 Liftoff!'

## Hints
- `total`: keep a running sum in a variable, then add each number to it inside the loop.
- `count_vowels`: check `if letter in "aeiouAEIOU"` for every letter, and add 1 to a counter when it matches.
- `countdown`: start with an empty string, add `str(n) + " "` while n is above 0, then `strip()` off the trailing space and add `" Liftoff!"`.

## Starter
```python
# Lesson 6 - loops!
def total(n):
    """Add up every whole number from 1 to n"""
    return 0


def count_vowels(text):
    """Count a, e, i, o, u in any case"""
    return 0


def countdown(n):
    """'3 2 1 Liftoff!' for n = 3"""
    return ""
```

## Tests
```python
check(total(1) == 1, "total(1) should be 1")
check(total(5) == 15, "total(5) should be 15")
check(total(10) == 55, "total(10) should be 55")
check(total(100) == 5050, "total(100) should be 5050")

check(count_vowels("hello world") == 3,
      "count_vowels('hello world') should be 3 (e, o, o)")
check(count_vowels("xyz") == 0,
      "count_vowels('xyz') should be 0")
check(count_vowels("AEIOU aeiou") == 10,
      "upper and lower case vowels both count - should be 10")

check(countdown(3) == "3 2 1 Liftoff!",
      "countdown(3) should give '3 2 1 Liftoff!'")
check(countdown(1) == "1 Liftoff!",
      "countdown(1) should give '1 Liftoff!'")
check(countdown(5) == "5 4 3 2 1 Liftoff!",
      "countdown(5) should give '5 4 3 2 1 Liftoff!'")
```

## Quiz
Q: How many times does `for n in range(4)` run?
A) 3
B) 4
C) 5
D) it never stops
ANSWER: B
WHY: range(4) is 0, 1, 2, 3 - four numbers, starting at zero.

Q: What is the output of `for n in range(0, 10, 5): print(n)`?
A) 0 5
B) 5 10
C) 0 5 10
D) 5
ANSWER: A
WHY: it starts at 0, steps by 5, and stops before reaching 10 - so 0 and 5.

Q: When does a `while` loop stop?
A) After exactly 10 rounds
B) When its condition becomes False
C) When you call print()
D) Never on its own
ANSWER: B
WHY: it re-checks the condition before every round. If the condition never turns False, the loop runs forever.

Q: What does `break` do?
A) Skips to the next round
B) Ends the loop immediately
C) Ends the program
D) Repeats the current round
ANSWER: B
WHY: break jumps out of the whole loop. continue only abandons the current round.

Q: A loop that never ends is called...
A) a fast loop
B) an infinite loop
C) a nested loop
D) a broken syntax
ANSWER: B
WHY: usually a condition that never becomes False - check that something inside the loop changes.
