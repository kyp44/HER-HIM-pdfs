#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
import argparse
import itertools as it
import numpy as np

# Parse command line arguments
parser = argparse.ArgumentParser(description="Builds LaTeX source file for positions required to build a HER (default) or HIM hexapawns learning system.")
parser.add_argument("--him", "-i", action="store_true", help="Generate LaTeX source file for HIM instead of HER.")
args = parser.parse_args()

width = 50

# Calculated sizes
space_width = width / 3

# Put units on points
units = lambda p : "(" + str(p[0]) + "mm, " + str(p[1]) + "mm)"

# Just for initial development, show the starting position
with open("base.tex", "r") as bfile :
    for line in bfile :
        line = line.strip()
        if line != "%TIKZ" :
            print(line)
            continue

        print(r"\begin{tikzpicture}")
        for (x, y) in it.product(range(3), repeat=2) :
            lower_left = space_width * np.array((x, y))
            upper_right = lower_left + space_width * np.array((1, 1))
            print(r"\draw[thick]", units(lower_left), "rectangle", units(upper_right), ";")
        print(r"\end{tikzpicture}")
