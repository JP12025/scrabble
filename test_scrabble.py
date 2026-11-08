"""Acceptance tests for the Scrabble exercise.

Each test runs your program as a whole, exactly as a user would: it types
a word for Player 1 and a word for Player 2, then checks what your program
prints and tries to explain what is wrong.

Run the tests from the exercise folder with:

    python test_scrabble.py
"""

import os
import subprocess
import sys
from pathlib import Path

EXERCISE_DIR = Path(__file__).resolve().parent
SCRIPT = "scrabble.py"
PROMPTS = ["Player 1: ", "Player 2: "]
RESULTS = ["Player 1 wins!", "Player 2 wins!", "Tie!"]
TIMEOUT = 5  # seconds

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Values of the instructions (those of the French Scrabble).
POINTS = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 10, 1, 2,
          1, 1, 3, 8, 1, 1, 1, 1, 4, 10, 10, 10, 10]
# Values of the English Scrabble (found on many websites, CS50 included).
ENGLISH_POINTS = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3,
                  1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]

# Each test case: (what is checked, word of Player 1, word of Player 2).
# The expected result is computed by the score() function below.
CASES = [
    ("Question? / Question! (example of the instructions)",
     "Question?", "Question!"),
    ("red / wheelbarrow (example of the instructions)",
     "red", "wheelbarrow"),
    ("COMPUTER / science (example of the instructions)",
     "COMPUTER", "science"),
    ("Scrabble / wiNNeR (example of the instructions)",
     "Scrabble", "wiNNeR"),
    ("Cthulhu / AXolotl", "Cthulhu", "AXolotl"),
    ("one letter each: A / B", "A", "B"),
    ("tie between two different words: cat / dog", "cat", "dog"),
    ("few letters can beat many letters: kiwi / BANANA", "kiwi", "BANANA"),
    ("K and W are worth 10 points: zoo / kiwi", "zoo", "kiwi"),
    ("a punctuation mark is worth 0 points: Hi! / Hit", "Hi!", "Hit"),
    ("a space is worth 0 points: ice cream / icecream",
     "ice cream", "icecream"),
    ("an empty word is worth 0 points: (empty) / a", "", "a"),
]

# Frequent mistakes: (parameters of score() reproducing the mistake,
# way of comparing the scores, explanation). After all the tests, the
# explanations of the mistakes that give exactly the results printed by
# the program are shown.
FIND_HINT = ("str.find() returns -1 when the character is not found, and "
             "points[-1] is the LAST value of your list (Z = 10): check "
             "that the character is a letter before using its position.")
SHIFT_HINT = ("Your values seem shifted by one position: the value of A "
              "must be at index 0 of your list, the value of Z at index 25 "
              "(indexes start at 0).")
TIE_HINT = ("When both words are worth the same number of points, your "
            "program should print 'Tie!': check your comparisons "
            "(> versus >=) and your else.")
MISTAKES = [
    ({"ignore_case": False}, "normal",
     "Lowercase letters seem to be worth 0 points: your program should not "
     "be case-sensitive (use str.upper() or str.lower())."),
    ({"ignore_case": False, "unknown": 10}, "normal",
     "Lowercase letters and punctuation marks seem to be worth 10 points. "
     "Your program should not be case-sensitive (use str.upper() or "
     "str.lower()). Moreover, " + FIND_HINT),
    ({"unknown": 10}, "normal",
     "Characters that are not letters seem to be worth 10 points instead "
     "of 0. " + FIND_HINT),
    ({"points": ENGLISH_POINTS}, "normal",
     "Your values look like those of the English Scrabble (K = 5, W = 4, "
     "...): use the values of the instructions (K = 10, W = 10, ...)."),
    ({"points": [1] * 26}, "normal",
     "Your program seems to compare the number of letters of the words "
     "instead of their points."),
    ({"points": [1] * 26, "unknown": 1}, "normal",
     "Your program seems to compare the lengths of the words instead of "
     "their points."),
    ({"shift": 1}, "normal", SHIFT_HINT),
    ({"shift": -1}, "normal", SHIFT_HINT),
    ({}, "inverted",
     "Player 1 and Player 2 seem inverted: check your comparisons "
     "(< versus >) and which message goes with which test."),
    ({}, "tie_player_1", TIE_HINT),
    ({}, "tie_player_2", TIE_HINT),
]


# ---------------------------------------------------------------------------
# Expected results
# ---------------------------------------------------------------------------

def score(word, points=POINTS, ignore_case=True, unknown=0, shift=0):
    """Return the score of a word.

    The optional parameters reproduce frequent mistakes:
    - points: the values of the letters, from A to Z;
    - ignore_case: if False, lowercase letters are not recognized;
    - unknown: points given to a character that is not recognized;
    - shift: the values are read `shift` positions too far.
    Return None if the mistake would make the program crash.
    """
    total = 0
    for char in word:
        if ignore_case:
            char = char.upper()
        if char in LETTERS:
            position = LETTERS.index(char) + shift
            if position >= len(points):
                return None  # IndexError
            total += points[position]
        else:
            total += unknown
    return total


def winner(score_1, score_2, comparison="normal"):
    """Return the line to print, or None if a score is None.

    comparison reproduces frequent mistakes: "inverted" swaps the players,
    "tie_player_1" and "tie_player_2" give the victory to a player in case
    of a tie.
    """
    if score_1 is None or score_2 is None:
        return None
    if comparison == "inverted":
        score_1, score_2 = score_2, score_1
    if score_1 > score_2:
        return "Player 1 wins!"
    if score_2 > score_1:
        return "Player 2 wins!"
    if comparison == "tie_player_1":
        return "Player 1 wins!"
    if comparison == "tie_player_2":
        return "Player 2 wins!"
    return "Tie!"


# ---------------------------------------------------------------------------
# Running the student's program
# ---------------------------------------------------------------------------

def run_program(words):
    """Run the program, typing the words one per line.

    Return (stdout, stderr, return code), or None if the program
    did not stop in time.
    """
    try:
        # sys.executable is the Python running the tests,
        # so "python" vs "python3" does not matter.
        result = subprocess.run(
            [sys.executable, SCRIPT],
            input="\n".join(words) + "\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=EXERCISE_DIR,
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None
    stdout = result.stdout.replace("\r\n", "\n")
    return stdout, result.stderr.strip(), result.returncode


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def show(text):
    """Indent the lines of a text, with each line between quotes."""
    lines = text.splitlines()
    if not lines:
        return "    (nothing)"
    return "\n".join(f"    {line!r}" for line in lines)


def plural(number, word):
    """Return e.g. '1 point' or '3 points'."""
    return f"{number} {word}" if number == 1 else f"{number} {word}s"


def last_lines(text, nb_lines=4):
    """Return the last lines of a text, indented."""
    lines = text.split("\n")[-nb_lines:]
    return "\n".join("    " + line for line in lines)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_crash(stderr, return_code):
    """Return an error message if the program crashed, else None."""
    if return_code == 0:
        return None
    if "EOFError" in stderr:
        return ("Your program asked for more than two words: it should "
                "ask once for Player 1 and once for Player 2.\n"
                f"{last_lines(stderr)}")
    message = f"Your program crashed:\n{last_lines(stderr)}"
    if "substring not found" in stderr:
        message += ("\nstr.index() fails when the character is not in the "
                    "string (a punctuation mark, a space, a lowercase "
                    "letter...): check the character first (e.g. with "
                    "the operator in) before looking for its position.")
    elif "IndexError" in stderr:
        message += ("\nA list of 26 values has indexes 0 to 25: the value "
                    "of A must be at index 0, the value of Z at index 25 "
                    "(indexes start at 0).")
    elif "KeyError" in stderr:
        message += ("\nA character is not a key of your dictionary (a "
                    "punctuation mark, a space, a lowercase letter...): "
                    "check that the key exists (operator in, or the method "
                    "get) before using it.")
    return message


def check_questions(stdout):
    """Check that the program asks the two questions.

    Return (error message or None, rest of the output after the questions).
    """
    printed = "Your program printed:\n" + show(stdout)
    rest = stdout
    for number, prompt in enumerate(PROMPTS, start=1):
        if rest.startswith((prompt + "\n", prompt.strip() + "\n")):
            message = (f"The word must be typed on the same line as the "
                       f"question: use input({prompt!r}) instead of print().")
        elif rest.startswith(prompt):
            rest = rest[len(prompt):]
            continue
        elif rest.startswith(prompt.strip()):
            message = (f"The question must be exactly {prompt!r}, "
                       f"with a space after the colon.")
        elif number == 1:
            message = f"Your program should start by asking {prompt!r}."
        else:
            message = (f"After the word of Player 1, your program should "
                       f"ask {prompt!r}.")
        return f"{message}\n{printed}", rest
    return None, rest


def check_result_line(rest):
    """Check that only one valid result line is printed after the questions.

    Return (error message or None, line printed).
    """
    lines = rest.splitlines()
    printed = ("After the questions, your program printed:\n" + show(rest))
    if not lines:
        return ("Your program printed nothing after the questions: it "
                "should print who wins."), None
    if len(lines) > 1:
        return ("After the questions, your program should print only one "
                "line (the result). Remove your extra print() (scores, "
                f"debugging...).\n{printed}"), None

    line = lines[0]
    if line in RESULTS:
        return None, line
    expected_lines = " or ".join(repr(result) for result in RESULTS)
    if line.strip() in RESULTS:
        message = (f"The result should be {line.strip()!r}, without spaces "
                   f"before or after.")
    elif line.lower().rstrip("!.").strip() in [
            result.lower().rstrip("!") for result in RESULTS]:
        message = (f"The result must be written exactly as {expected_lines}"
                   f" (capital letters, exclamation mark).")
    else:
        message = f"The result should be {expected_lines}."
    return f"{message}\n{printed}", None


def explain_wrong_result(word_1, word_2, given, expected):
    """Explain that the program printed `given` instead of `expected`."""
    return (f"Your program printed {given!r}, but the result should be "
            f"{expected!r}:\n"
            f"    Player 1: {word_1!r} is worth "
            f"{plural(score(word_1), 'point')}\n"
            f"    Player 2: {word_2!r} is worth "
            f"{plural(score(word_2), 'point')}")


def diagnose(observations):
    """Explain the wrong results, using all the results of the program.

    observations: list of (word 1, word 2, line printed by the program).
    Return the explanations of the frequent mistakes that give exactly
    the same results as the program.
    """
    causes = []
    for parameters, comparison, explanation in MISTAKES:
        consistent = True
        for word_1, word_2, given in observations:
            predicted = winner(score(word_1, **parameters),
                               score(word_2, **parameters), comparison)
            if predicted != given:
                consistent = False
        if consistent and explanation not in causes:
            causes.append(explanation)
    return causes


def check_case(word_1, word_2):
    """Run one test case.

    Return (error message or None if the test passes,
            result line printed by the program or None if not valid).
    """
    result = run_program([word_1, word_2])
    if result is None:
        return ("Your program did not stop (infinite loop?). Check that "
                "the variables tested by your while loops change at each "
                "turn."), None
    stdout, stderr, return_code = result

    message = check_crash(stderr, return_code)
    if message is not None:
        return message, None
    message, rest = check_questions(stdout)
    if message is not None:
        return message, None
    message, given = check_result_line(rest)
    if message is not None:
        return message, None

    expected = winner(score(word_1), score(word_2))
    if given != expected:
        return explain_wrong_result(word_1, word_2, given, expected), given
    return None, given


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(errors="replace")
    use_colors = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ)
    green = "\033[32m" if use_colors else ""
    red = "\033[31m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""

    if not (EXERCISE_DIR / SCRIPT).is_file():
        print(f"No {SCRIPT} found in {EXERCISE_DIR}")
        return 1

    nb_ok = 0
    observations = []  # (word 1, word 2, result printed by the program)
    nb_wrong_results = 0
    for description, word_1, word_2 in CASES:
        message, given = check_case(word_1, word_2)
        if given is not None:
            observations.append((word_1, word_2, given))
            if message is not None:
                nb_wrong_results += 1
        if message is None:
            nb_ok += 1
            print(f"{green}✔{reset} {description}")
        else:
            print(f"{red}✗{reset} {description}")
            print(f"    Words typed: {word_1!r}, {word_2!r}")
            print("    " + message.replace("\n", "\n    ") + "\n")

    if nb_wrong_results > 0:
        causes = diagnose(observations)
        if not causes:
            print("To find your mistake, compute the score of each word by "
                  "hand, then print the scores computed by your program to "
                  "compare them (and remove these print() afterwards).\n")
        else:
            title = "Probable cause" if len(causes) == 1 else "Possible causes"
            print(f"{title} of the wrong results, considering all the tests:")
            for cause in causes:
                print("  - " + cause)
            print()

    color = green if nb_ok == len(CASES) else red
    print(f"Validated: {color}{nb_ok}/{len(CASES)}{reset}")
    return 0 if nb_ok == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
