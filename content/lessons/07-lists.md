# Lesson 7 - Lists

## Objectives
- Group values in a list
- Add, remove and inspect items
- Loop over a list and build a new one

## Lesson
A list holds many values in order, in square brackets:

```python
scores = [8, 3, 10, 3]
names = ["Ada", "Grace", "Linus"]
mixed = [1, "two", True, 3.0]     # Python does not mind
```

Positions work like strings, starting at 0:

```python
names[0]        # 'Ada'
names[-1]       # 'Linus'
len(names)      # 3
names[0:2]      # ['Ada', 'Grace']
```

Changing an existing item (assignment, not a new list):

```python
scores[1] = 4
```

Growing and shrinking:

```python
scores.append(7)        # add to the end
scores.extend([1, 2])   # add several at once
scores.remove(3)        # remove the FIRST item whose value is 3
last = scores.pop()     # remove and give back the last item
```

Useful tests and tools:

```python
3 in scores             # True - is it in there?
sorted(scores)          # a NEW sorted list, original untouched
scores.sort()           # sorts the original in place
sum(scores)             # add them all up
max(scores), min(scores)
```

Looping over a list is the most common loop of all:

```python
for name in names:
    print(name)
```

Building a **new** list while you loop is a pattern you will use forever:

```python
long_words = []
for word in words:
    if len(word) >= 5:
        long_words.append(word)
```

## Exercise
Three functions, all about lists.

`total(numbers)` adds up every number in the list - `total([])` should be `0`:

    total([1, 2, 3])      -> 6
    total([10, -4])       -> 6

`biggest(numbers)` returns the largest value:

    biggest([4, 9, 2])    -> 9
    biggest([-5, -1])     -> -1

`keep_long(words, minimum)` returns a **new list** containing only the words whose length is at least `minimum`, in their original order:

    keep_long(["cat", "horse", "dog", "rabbit"], 4)
        -> ['horse', 'rabbit']

## Hints
- `total` starts at `0` and adds each number in a loop - or use the `sum()` built-in.
- `biggest` can be one line with `max()`, or a loop that keeps the best value seen so far.
- For `keep_long`, start with `result = []`, then `result.append(word)` when `len(word) >= minimum`, and remember to `return result`.

## Starter
```python
# Lesson 7 - lists
def total(numbers):
    """Add up every number in the list"""
    return 0


def biggest(numbers):
    """Return the largest number"""
    return 0


def keep_long(words, minimum):
    """Only the words whose length is at least 'minimum'"""
    return []
```

## Tests
```python
check(total([1, 2, 3]) == 6, "total([1, 2, 3]) should be 6")
check(total([10, -4]) == 6, "total([10, -4]) should be 6")
check(total([]) == 0, "an empty list adds up to 0")
check(total([1.5, 2.5]) == 4.0, "total([1.5, 2.5]) should be 4.0")

check(biggest([4, 9, 2]) == 9, "biggest([4, 9, 2]) should be 9")
check(biggest([-5, -1]) == -1, "the biggest of two negatives is the one nearest zero")
check(biggest([7]) == 7, "a one-item list is its own biggest")

check(keep_long(["cat", "horse", "dog", "rabbit"], 4) == ["horse", "rabbit"],
      "only words of 4+ letters, in the original order")
check(keep_long(["cat", "dog"], 4) == [],
      "when nothing qualifies you get an empty list")
check(keep_long(["hello", "hi"], 2) == ["hello", "hi"],
      "the order must stay the same as the input")
```

## Quiz
Q: What is `[10, 20, 30][1]`?
A) 10
B) 20
C) 30
D) 1
ANSWER: B
WHY: list positions start at 0, so index 1 is the second item.

Q: Which line adds "pear" to the end of fruit?
A) fruit.add("pear")
B) fruit.append("pear")
C) fruit += 1
D) fruit.put("pear")
ANSWER: B
WHY: append() puts one item at the end of the list.

Q: What does `sorted(scores)` do?
A) Sorts scores in place, nothing is returned
B) Returns a new sorted list and leaves scores untouched
C) Deletes scores
D) Reverses scores
ANSWER: B
WHY: sorted() gives you a copy. Use scores.sort() if you want to change the original.

Q: Which tells you whether 42 is in numbers?
A) numbers.has(42)
B) 42 in numbers
C) numbers.contains(42)
D) is(42, numbers)
ANSWER: B
WHY: the in keyword asks whether a value appears in a sequence, and answers True or False.

Q: How do you find how many items are in a list?
A) length(numbers)
B) numbers.count()
C) len(numbers)
D) size(numbers)
ANSWER: C
WHY: len() works on strings, lists and tuples alike.
