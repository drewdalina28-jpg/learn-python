# Lesson 8 - Dictionaries

## Objectives
- Pair up keys and values in a dictionary
- Read, add and update entries safely with `.get()`
- Walk through a dictionary with `.items()`

## Lesson
A list finds things by position. A **dictionary** finds things by name:

```python
user = {
    "name": "Ada",
    "age": 30,
    "city": "London",
}
```

The left side of each pair is the **key** (almost always text), the right side is the **value** (anything at all).

```python
user["name"]        # 'Ada'
user["age"] = 31    # update an existing key
user["email"] = "ada@example.com"   # add a new key
len(user)           # 4
```

Asking for a key that is not there raises an error, so use `.get()` when it might be missing:

```python
user.get("age")           # 31
user.get("nickname")      # None - no crash
user.get("nickname", "n/a")   # 'n/a'  - supply your own fallback
```

Testing membership looks at the **keys**:

```python
"name" in user        # True
"nickname" in user    # False
```

To see everything, loop over `.items()`, which hands you both halves:

```python
for key, value in user.items():
    print(key, "=", value)
```

Other handy views: `user.keys()` and `user.values()`.

Real programs use dictionaries everywhere - a settings file, a scoreboard, one row of data. Lists of dictionaries are the standard way to hold "many records":

```python
players = [
    {"name": "Ada", "score": 12},
    {"name": "Grace", "score": 9},
]
```

## Exercise
Two functions.

`full_name(user)` glues the `"first"` and `"last"` keys together with one space:

    full_name({"first": "Ada", "last": "Lovelace"})
        -> 'Ada Lovelace'

`find_user(directory, name)` looks up a name in a dictionary of names to email addresses. When the name is missing, return the string `"unknown@example.com"` instead of crashing:

    find_user({"ada": "ada@lovelace.dev"}, "ada")
        -> 'ada@lovelace.dev'
    find_user({"ada": "ada@lovelace.dev"}, "bob")
        -> 'unknown@example.com'

## Hints
- `full_name` is one f-string: `f"{user['first']} {user['last']}"`.
- `find_user` is one line if you use `.get(name, "unknown@example.com")`.

## Starter
```python
# Lesson 8 - dictionaries
def full_name(user):
    """'Ada Lovelace' from {'first': 'Ada', 'last': 'Lovelace'}"""
    return ""


def find_user(directory, name):
    """The email for this name, or 'unknown@example.com'"""
    return ""
```

## Tests
```python
check(full_name({"first": "Ada", "last": "Lovelace"}) == "Ada Lovelace",
      "join first and last with a single space")
check(full_name({"first": "Grace", "last": "Hopper"}) == "Grace Hopper",
      "full_name should work for any pair of names")

check(find_user({"ada": "ada@lovelace.dev"}, "ada") == "ada@lovelace.dev",
      "a name that exists should give its email")
check(find_user({"ada": "ada@lovelace.dev", "bob": "bob@py.dev"}, "bob") == "bob@py.dev",
      "it should pick the right entry out of the dictionary")
check(find_user({"ada": "ada@lovelace.dev"}, "zed") == "unknown@example.com",
      "a missing name must return 'unknown@example.com' rather than raising an error")
```

## Quiz
Q: How do you read the "city" key from user?
A) user["city"]
B) user(city)
C) get user.city
D) user->"city"
ANSWER: A
WHY: square brackets look up a key - the same syntax as a list, but with a name inside.

Q: What is the difference between a list and a dictionary?
A) Nothing, they are the same
B) A list finds items by position, a dictionary by key
C) A dictionary can only hold numbers
D) A list must be sorted
ANSWER: B
WHY: keys are labels you choose yourself, instead of positions 0, 1, 2...

Q: What does `settings.get("theme", "dark")` return if "theme" is missing?
A) None
B) An error
C) "dark"
D) "theme"
ANSWER: C
WHY: the second argument to get() is the fallback value used when the key is absent.

Q: `"age" in user` checks...
A) whether the value "age" exists anywhere
B) whether the key "age" exists
C) whether user is a number
D) whether user has 3 letters
ANSWER: B
WHY: in looks at the keys of a dictionary.

Q: How do you loop over both keys and values?
A) for key in user
B) for key, value in user.items()
C) for key, value in user
D) for item in user.list()
ANSWER: B
WHY: items() gives one (key, value) pair per round, which unpacks neatly into two names.
