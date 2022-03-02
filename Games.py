from anytree import AnyNode
from Board import Board, Player
from Config import Config

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
        self.root = AnyNode(board=Board(config), turn=Player.WHITE, turn_num=1)
        
        def build_tree(root: AnyNode) :
            """
            Recursively adds the children to the passed
            game node, terminating when the game is over.
            """
            children = []
            for moves in root.board.legal_moves(children
