#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
import argparse
import numpy as np
from Board import Board, Player
from Config import Config

# Parse command line arguments
parser = argparse.ArgumentParser(description="Builds LaTeX source file for positions required to build a HER (default) or HIM hexapawns learning system.")
parser.add_argument("--him", "-i", action="store_true", help="Generate LaTeX source file for HIM instead of HER.")
args = parser.parse_args()

# Load the config file
config = Config()

# Just for initial development, show the starting position
with open("base.tex", "r") as bfile :
    for line in bfile :
        line = line.strip()
        if line != "%TIKZ" :
            print(line)
            continue

        print(r"\setboardfontsize{" + config.units(config.space_size) + "}")
        board = Board(config)
        turn = Player.WHITE
        while True :
            print(board.draw(turn))
            moves = board.legal_moves(turn)
            if board.winner(turn) is not None :
                break
            board = board.make_move(moves[-1])
            turn = -turn
