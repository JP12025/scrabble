# Scrabble

![scrabble](https://upload.wikimedia.org/wikipedia/commons/9/99/Scrabble.jpg)

# What to Do
In the game of Scrabble, players create words to score points, and the number of points is the sum of the point values of each letter in the word.

| A | B | C | D | E | F | G | H | I | J | K  | L | M |
| - | - | - | - | - | - | - | - | - | - | -- | - | - |
| 1 | 3 | 3 | 2 | 1 | 4 | 2 | 4 | 1 | 8 | 10 | 1 | 2 |

| N | O | P | Q | R | S | T | U | V | W  | X  | Y  | Z  |
| - | - | - | - | - | - | - | - | - | -- | -- | -- | -- |
| 1 | 1 | 3 | 8 | 1 | 1 | 1 | 1 | 4 | 10 | 10 | 10 | 10 |

For example, if we wanted to score the word “CODE”, we would note that the ‘C’ is worth 3 points, the ‘O’ is worth 1 point, the ‘D’ is worth 2 points, and the ‘E’ is worth 1 point. Summing these, we get that “CODE” is worth 7 points.

In a python script called `scrabble`, implement a program that determines the winner of a short Scrabble-like game. Your program should prompt for input twice: once for “Player 1” to input their word and once for “Player 2” to input their word. Then, depending on which player scores the most points, your program should either print “Player 1 wins!”, “Player 2 wins!”, or “Tie!” (in the event the two players score equal points). There is an infinite number of each letter.

> [!Note]
> Your program should be executable. Do you remember what's needed?

The main difficulty is to store and retreive scores for each letter. 
Among your class, those who already know python will probably use a dictionary for this task.

It may be a little bit too difficult for others. 
Instead, simply store scores in a list in alphbetical order.
Thus, score of letter A (`1`) will be at position `0`, B (`3`) at position `1` ... Z (`10`) at position `25`.

Now, ask yourself: what is the position of `B` in string `ABCDEFGHIJKLMNOPQRSTUVWXYZ`? 
Is there a function to search for a letter in a string that returns its position (a.k.a. index)? (spoiler: yes there is)

# When to Do it

By Sunday, january 19, 2025 at 11:59 PM

# How to Test

Test your script with command `./check scrabble`

Your program should behave per the examples below.
```bash
$ ./scrabble
Player 1: Question?
Player 2: Question!
Tie!
```

> [!Note]
> Ask yourself: What do I do with punctuation marks?


```bash
$ ./scrabble
Player 1: red
Player 2: wheelbarrow
Player 2 wins!
```
```bash
$ ./scrabble
Player 1: COMPUTER
Player 2: science
Player 1 wins!
```
```bash
$ ./scrabble
Player 1: Scrabble
Player 2: wiNNeR
Player 2 wins!
```

> [!TIP]
> Your program should not be case-sensitive. You'll need `upper` or `lower` function from `str`. 
> Read the Doc!

# How to Submit

Once you're done with all tasks, submit all your python files for the week on Moodle.

# Licence

This course is freely inspird from [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/2025/) Harvard. It is licensed under a [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. 
