# pycoach

**A friendly Python learning coach that runs in your terminal.**

Ten lessons, fifty quiz questions and three guided projects, with every exercise
checked automatically. No internet, no accounts, no setup. Built for Termux on
Android, but it runs anywhere Python 3 does.

```
PYCOACH  -  learn Python one small step at a time
.........................................................

  lessons      ###############.....  8/10
  projects     ######............  1/3
  quiz best    ##################  38/40

  [1] learn - continue with the next lesson
  [2] lessons - browse everything
  [3] quiz - test what you know
  [4] projects - build a real program
  [5] progress - your report card
  [q] quit
```

## What you get

- **10 lessons** for a complete beginner: printing, variables, numbers,
  strings, decisions, loops, lists, dictionaries, functions, files & errors.
- **50 quiz questions** with a short explanation after every answer, and your
  best score remembered.
- **3 projects** you build step by step:
  - **Mad Libs** - input, strings, f-strings
  - **Number guessing game** - loops, conditionals, `random`
  - **To-do list** - menus, lists, and saving to a file
- **Instant feedback.** Write some code, press `r`, and get told exactly what
  was expected - and why it failed.
- **Resume any time.** Your code and progress are saved automatically; close
  the terminal and pick up right where you stopped.
- **Hints, not spoilers.** Ask for one nudge at a time.

## Install

### Termux (Android)

```bash
pkg install python git
git clone https://github.com/drewdalina28-jpg/pycoach.git
cd pycoach
./install.sh
pycoach
```

### Linux, macOS, WSL

```bash
git clone https://github.com/drewdalina28-jpg/pycoach.git
cd pycoach
./install.sh
pycoach
```

### Without installing anything

```bash
git clone https://github.com/drewdalina28-jpg/pycoach.git
cd pycoach
python3 pycoach.py
```

Requirements: Python 3.8+ and a terminal. Nothing else.

## Using it

```bash
pycoach               # the main menu
pycoach next          # jump to your next unfinished lesson
pycoach lesson 3      # open lesson 3
pycoach quiz 3        # take lesson 3's quiz
pycoach project 1     # start a project
pycoach progress      # your report card
pycoach reset         # clear saved progress (your code is kept)
pycoach help          # command summary
```

While you are inside an exercise:

| key | what it does |
| --- | --- |
| `e` | edit your code in `$EDITOR` (`nano` by default) |
| `r` | run the automatic checks |
| `x` | run your program for real (script-style exercises) |
| `h` | reveal one hint |
| `v` | view your code without leaving pycoach |
| `p` | show the task again |
| `s` | skip for now |
| `q` | quit - nothing is ever lost |

## Where things live

```
pycoach/                    this repository
  pycoach.py                the CLI
  _runner.py                the test harness
  selftest.py               checks that every lesson and step still works
  install.sh                puts the `pycoach` command on your PATH
  bin/pycoach               the launcher
  content/lessons/*.md      the ten lessons
  content/projects/*.md     the three projects

~/pycoach-work/             your code, one file per lesson
  lesson-01.py ... lesson-10.py
  projects/project-01/story.py
  projects/project-02/guess.py
  projects/project-03/todo.py

~/.pycoach/progress.json    which lessons and steps you have finished
```

Your code and progress live in your home folder, never in the repository, so
pulling updates can never overwrite your work.

## Running the checks

```bash
python3 selftest.py
```

It writes a known-good solution for every lesson and project step, runs each
check against them, and confirms that broken solutions are still rejected.
Handy after editing any content.

## Adding your own lesson

Create `content/lessons/11-your-topic.md`:

````markdown
# Lesson 11 - Your title

## Objectives
- One thing you will learn
- Another thing

## Lesson
The teaching part. A friendly subset of markdown renders nicely:
`code`, **bold**, bullets, > tips, and fenced code blocks.

## Exercise
What the reader has to write.

## Hints
- A nudge, revealed one at a time

## Starter
```python
the code the learner starts from
```

## Tests
```python
check(some_function(2) == 4, "a message shown when it fails")
```

## Quiz
Q: A question?
A) first choice
B) second choice
C) third choice
ANSWER: B
WHY: one line explaining the answer.
````

Tests are ordinary Python that runs in the same namespace as the learner's
file. You can call their functions, inspect `OUTPUT` (what their file printed),
or use `run_main("input\nhere")` to run the whole program and get
`(output, exit_code)` back. `HERE` is the folder of the learner's file.

Projects use the same idea, split into `## Step N: title` sections, each with
`### File`, `### Starter`, `### Check` and `### Hints`.

## Contributing

Issues and pull requests are welcome - new lessons, better hints, clearer
error messages, translations. If you add content, run `python3 selftest.py`
first and make sure it stays green.

## License

MIT - see [LICENSE](LICENSE).
