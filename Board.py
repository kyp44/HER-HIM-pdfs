from enum import Enum
from dataclasses import dataclass, replace, field
import itertools as it
from os import linesep as endl
from typing import Optional, Tuple, List, Set, Dict
import math
from Config import Config

class Player(Enum) :
    """
    Represents a particular player.
    """
    WHITE = "White"
    BLACK = "Black"

    def __neg__(self) :
        return Player.BLACK if self is Player.WHITE else Player.WHITE

@dataclass
class Pawn :
    """
    Defines a pawn on the board for either player.
    """
    player: Player
    x: int
    y: int

    def __lt__(self, other: "Pawn") -> bool :
        """
        Implements an order by x position so that the
        pawn lists can be sorted.
        """
        return self.x < other.x

    def __hash__(self) -> int :
        """
        Make hashable so they can be stored in a set.
        """
        return hash((self.player, self.x, self.y))

@dataclass
class Move :
    """
    Represents a pawn potentially making a move.
    """
    pawn: Pawn
    x: int
    y: int

@dataclass    
class Board :
    """
    Represents a single position of the board.
    """
    config: Config
    pawns: Dict[Player, Set[Pawn]] = field(default_factory=lambda : {player : [Pawn(player, x, 0 if player is Player.WHITE else 2) for x in range(3)] for player in Player})
    turn: Player = Player.WHITE
    turn_num: int = 1
    
    def space(self, x: int, y: int) -> Optional[Pawn] :
        """
        Returns whether the given space is occupied by a
        player's pawn or not.
        """
        for pawns in self.pawns.values() :
            space_pawns = [p for p in pawns if (p.x, p.y) == (x, y)]
            if space_pawns :
                return space_pawns[0]
        return None

    def valid_position(self, x: int, y: int) -> bool :
        """
        Returns whether a given space is valid
        (i.e. is actually on the board)
        """
        return 0 <= x <= 2 and 0 <= y <= 2
        
    def legal_moves(self) -> List[Move] :
        """
        Returns list of legal moves for the current
        player's turn.
        """
        dy = 1 if self.turn is Player.WHITE else -1
        moves = []
        for p in sorted(self.pawns[self.turn]) :
            # Is this pawn necessary given symmetry?
            if p.x == 2 and self == self.mirror() :
                continue
            
            # Move forward
            new_pos = (p.x, p.y + dy)
            if self.valid_position(*new_pos) and self.space(*new_pos) is None :
                moves.append(Move(p, *new_pos))

            # Captures
            for dx in (-1, 1) :
                new_pos = (p.x + dx, p.y + dy)
                space = self.space(*new_pos)
                if self.valid_position(*new_pos) and space is not None and space.player is -self.turn :
                    moves.append(Move(p, *new_pos))
        
        return moves

    def make_move(self, move: Move) -> "Board" :
        """
        Makes a legal move and and returns the new Board.
        Behavior for illegal moves is undefined.
        """
        # Move the pawn
        assert move.pawn.player is self.turn, "Tried to make a move when it's not your turn!"
        def proc_pawn(pawn: Pawn) -> Pawn :
            if pawn == move.pawn :
                return Pawn(self.turn, move.x, move.y)
            return replace(pawn)

        player_pawns = set(map(proc_pawn, self.pawns[self.turn]))
        opponent_pawns = set(map(lambda p : replace(p), filter(lambda p : p.x != move.x or p.y != move.y, self.pawns[-self.turn])))
        
        return Board(self.config, pawns={self.turn : player_pawns, -self.turn : opponent_pawns}, turn=-self.turn, turn_num=self.turn_num + 1)

    def winner(self) -> Optional[Player] :
        """
        Return whether the other player won on after
        their last move.
        """
        # The current player has no more moves
        if len(self.legal_moves()) == 0 :
            return -self.turn

        # Opposite player made it to the third row on the last turn
        third_row = 2 if -self.turn is Player.WHITE else 0
        for pawn in self.pawns[-self.turn] :
            if pawn.y == third_row :
                return -self.turn

        # Are all the current player's pieces captured?
        if len(self.pawns[self.turn]) == 0 :
            return -self.turn

        return None

    def mirror(self) -> "Board" :
        """
        Returns the mirror image of the board, which
        is useful for detecting symmetry.
        """
        def pawn_mirror(pawn: Pawn) -> Pawn :
            return replace(pawn, x=2 - pawn.x)
        return replace(self, pawns={player : set(map(pawn_mirror, self.pawns[player])) for player in Player})
        
    def draw(self) -> str :
        """
        Generates a TikZ picture for the board state
        with available moves for the current player.
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
        moves = self.legal_moves()
        assert len(moves) <= len(self.config.colors), "Need at least " + str(len(moves)) + " colors, but only " + str(len(self.config.colors)) + " are defined!"
        for move, color in zip(moves, self.config.colors) :
            # Draw a nice thick arrow with an outline
            dx = (move.x - move.pawn.x) * s
            dy = (move.y - move.pawn.y) * s
            theta = math.atan2(dy, dx)
            mag = math.hypot(dx, dy)*0.6
            center = ((move.pawn.x + 0.5)*s +  dx/2, (move.pawn.y + 0.5)*s + dy/2)
                        
            out += (r"\node[single arrow, draw=black, fill=" + color + ", inner sep=" + self.config.units(1)
                    + ", single arrow head extend=3pt, minimum height=" +
                    self.config.units(mag) + ", shift={" + pt_units(*center) +"}, rotate=" + str(math.degrees(theta)) + "] {};" + endl)

        # Draw turn number
        out += r"\draw " + pt_units(self.config.width/2, -3) + " node {Move: " + str(self.turn_num) + "};" + endl

        out += r"\end{tikzpicture}"
        return out
