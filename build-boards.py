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

width = 30

# Calculated sizes
space_width = width / 3

# Put units on points
units = lambda v : str(v) + "mm"
pt_units = lambda p : "(" + units(p[0]) + ", " + units(p[1]) + ")"

# Just for initial development, show the starting position
with open("base.tex", "r") as bfile :
    for line in bfile :
        line = line.strip()
        if line != "%TIKZ" :
            print(line)
            continue

        print(r"\begin{tikzpicture}")
        print(r"\setboardfontsize{" + units(space_width) + "}")
        for (x, y) in it.product(range(3), repeat=2) :
            lower_left = space_width * np.array((x, y))
            upper_right = lower_left + space_width * np.array((1, 1))
            print(r"\draw[thick]", pt_units(lower_left), "rectangle", pt_units(upper_right) + ";")
            print(r"\draw",  pt_units((lower_left + upper_right)/2), "node {\LARGE\BlackPawnOnWhite};")

        print(r"\end{tikzpicture}")
