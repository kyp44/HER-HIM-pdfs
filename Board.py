from enum import Enum
from dataclasses import dataclass, replace
from Config import Config
import itertools as it
from os import linesep as endl
from typing import Optional, Tuple, List, Dict

class Player(Enum) :
    WHITE = "White"
    BLACK = "Black"

    def __neg__(self) :
        return Player.BLACK if self is Player.WHITE else Player.WHITE

@dataclass
class Pawn :
    player: Player
    x: int
    y: int

@dataclass
class Move :
    pawn: Pawn
    x: int
    y: int
    
class Board :
    """
    Represents a single position of the board.
    """
    def __init__(self, config: Config, pawns: Optional[Dict[Player, List[Pawn]]] = None) :
        self.config = config
        if pawns is None :
            self.pawns = {player : [Pawn(player, x, 0 if player is Player.WHITE else 2) for x in range(3)] for player in Player}
        else :
            self.pawns = pawns

    def space(self, x: int, y: int) -> Optional[Pawn] :
        for pawns in self.pawns.values() :
            space_pawns = [p for p in pawns if (p.x, p.y) == (x, y)]
            if space_pawns :
                return space_pawns[0]
        return None

    def valid_position(self, x: int, y: int) -> bool :
        return 0 <= x <= 2 and 0 <= y <= 2
        
    def legal_moves(self, player: Player) -> List[Move] :
        """
        Returns list of legal moves for the given
        player's turn.
        """
        dy = 1 if player is Player.WHITE else -1
        moves = []
        for p in self.pawns[player] :
            # Move forward
            new_pos = (p.x, p.y + dy)
            if self.valid_position(*new_pos) and self.space(*new_pos) is None :
                moves.append(Move(p, *new_pos))

            # Captures
            for dx in (-1, 1) :
                new_pos = (p.x + dx, p.y + dy)
                space = self.space(*new_pos)
                if self.valid_position(*new_pos) and space is not None and space.player is -player :
                    moves.append(Move(p, *new_pos))
        
        return moves

    def make_move(self, move: Move) -> "Board" :
        """
        Makes a legal move and and returns the new Board.
        Behavior for illegal moves is undefined.
        """
        # Move the pawn
        player = move.pawn.player
        def proc_pawn(pawn: Pawn) -> Pawn :
            if pawn == move.pawn :
                return Pawn(player, move.x, move.y)
            return replace(pawn)

        player_pawns = list(map(proc_pawn, self.pawns[player]))
        opponent_pawns = list(map(lambda p : replace(p), filter(lambda p : p.x != move.x or p.y != move.y, self.pawns[-player])))
        
        return Board(self.config, pawns={player : player_pawns, -player : opponent_pawns})

    def winner(self, player: Player) -> Optional[Player] :
        """
        Given a player's turn, returns whether the other player
        won on after their last move.
        """
        # The current player has no more moves
        if len(self.legal_moves(player)) == 0 :
            return -player

        # Opposite player made it to the third row on the last turn
        third_row = 2 if -player is Player.WHITE else 0
        for pawn in self.pawns[-player] :
            if pawn.y == third_row :
                return -player

        # Are all the current player's peices captured?
        if len(self.pawns[player]) == 0 :
            return -player

        return None
        
        
    def draw(self, player: Player) -> str :
        """
        Generates a TikZ picture for the board state
        with available moves for the specified player.
        """
        # Put units on points
        pt_units = lambda x, y : "(" + self.config.units(x) + ", " + self.config.units(y) + ")"
        
        out = r"\begin{tikzpicture}" + endl

        # Draw pieces and empty squares
        for (y, x) in it.product(range(3), repeat=2) :
            # Is the space black or white?
            space = Player.WHITE if (x + y) % 2 == 1 else Player.BLACK

            # Is there a pawn there?
            pawn = self.space(x, y)

            # Draw piece or black square
            s = self.config.space_size
            center = lambda x, y : pt_units((x+0.5)*s, (y+0.5)*s)
            char = None
            if pawn is None :
                if space is Player.BLACK :
                    char = "BlackEmptySquare"
            else :
                char = pawn.player.value + "PawnOn" + space.value
            if char is not None :
                out += r"\draw " +  center(x, y) + " node {\\" + char + "};" + endl

            # Draw space border
            out += r"\draw[thick] " + pt_units(x*s, y*s) + " rectangle " + pt_units((x+1)*s, (y+1)*s) + ";" + endl

        # Draw available moves
        for move, color in zip(self.legal_moves(player), self.config.colors) :
            out += r"\draw [line width=0.6mm, " + color + ", -{Stealth[scale=1]}] " + center(move.pawn.x, move.pawn.y) + " -- " + center(move.x, move.y) + ";" + endl

        out += r"\end{tikzpicture}"
        return out

        
