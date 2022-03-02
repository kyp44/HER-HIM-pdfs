#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
import argparse
import numpy as np
from Config import Config
from Games import Games
from Board import Player

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

        # Build game tree
        games = Games(config)
        
        # Now draw all positions
        player = Player.WHITE if args.him else Player.BLACK
        def new_line() :
            #print(r"\newline")
            print(r"\vspace{" + config.units(config.board_spacing) + "}")
            print(r"\newline")

        n = 0
        for turn_num, boards in games.all_player_positions(player).items() :
            shown_boards = []
            for board in boards :
                if board not in shown_boards and board.mirror() not in shown_boards and board.winner() is None :
                    if n > 0 and n % config.boards_per_row == 0 :
                        new_line()
                    print(board.draw())
                    print(r"\hspace{" + config.units(config.board_spacing) + "}")
                    shown_boards.append(board)
                    n += 1
