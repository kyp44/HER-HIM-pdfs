# Hexapawn Positions for the HER and HIM Learning Computers

## Introduction

This project will generate all the black positions and moves for a Hexapawn Educable Robot (HER) and the white positions for a Hexapawn Instructable Matchboxes (HIM) machine.

Inspired by the [MENACE](https://www.mscroggs.co.uk/blog/94) Tic-Tac-Toe (i.e. Noughts and Crossses if you aren't American) engine, these are the positions for the simpler game hexapawn, which was devised by Martin Gardner in his [1962 article](http://cs.williams.edu/~freund/cs136-073/GardnerHexapawn.pdf).
Unlike MENACE for tic-tac-toe, which requires 304 matchboxes, HER and HIM for hexapawn requires only 19 matchboxes for the black player (HER) and 18 for the white player (HIM) once symmetry is taken into account.
The PDFs for [HER]() and [HIM]() are in the repository along with a printable [game board]().

## Requirements

The project is a combination of Python and LaTeX, with a Python program generating LaTeX code that is then compiled, which was developed in a Linux environment.
Python 3 and a working LaTeX installation are required along with the [`anytree`](https://pypi.org/project/anytree/) Python module to build the game tree, and the [`chessfss`](https://ctan.org/pkg/chessfss?lang=en) LaTeX package to render the pawn symbols.

## Building

Everything above can be built by simply running `make`, or run `make help` for information about just building individual components.
Currently things are configured for my needs, but `Config.py` contains a configuration object with some parameters that can be adjusted to meet other user's specific needs.
Namely this includes changing the board sizes (for different sized matchboxes or other containers), move colors (which will depend on what color beads one has available), and parameters relating to position boards layout on the PDF pages.
See `Config.py` for more details on these paramters.
