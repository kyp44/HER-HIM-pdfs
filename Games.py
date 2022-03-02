from anytree import AnyNode, LevelOrderIter
from Board import Board, Player
from Config import Config
from typing import Dict, List

class Games :
    """
    Class that solves hexapawn by creating a tree
    of possible games.
    """
    def __init__(self, config: Config) :
        """
        Creates the tree.
        """
        # Starting position
        self.root = AnyNode(board=Board(config))
        
        def build_tree(node: AnyNode) :
            """
            Recursively adds the children to the passed
            game node, terminating when the game is over.
            Simply returns the passed node with potential
            children added.
            """
            # If this node is a winning position then we're done
            if node.board.winner() is not None :
                return

            # Otherwise we need to add a child for all possible moves
            for move in node.board.legal_moves() :
                build_tree(AnyNode(board=node.board.make_move(move), parent=node))

            return

        build_tree(self.root)

    def all_player_positions(self, player: Player) -> Dict[int, List[Board]] :
        """
        Returns a dict of all the positions for a particular player,
        where the key is the turn number, and the value is the list
        of possible Board positions for that turn.
        """
        boards = dict()
        for node in LevelOrderIter(self.root) :
            board = node.board
            if board.turn == player :
                if board.turn_num in boards :
                    boards[board.turn_num].append(board)
                else :
                    boards[board.turn_num] = [board]
        return boards
