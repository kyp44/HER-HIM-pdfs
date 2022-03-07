class Config :
    """
    Configuration class
    """
    def __init__(self) :
        """
        Parses the config file.
        """
        # Width of each board (in mm).
        self.width = 34
        # Colors to use for the moves, only 4 are needed.
        # These can be any LaTeX colors including mixes using xcolor.
        # For more info see: https://en.wikibooks.org/wiki/LaTeX/Colors
        self.colors = ["violet!80!white", "green!50!black", "yellow", "pink"]
        # Space between boards (in mm) on the page.
        self.board_spacing = 8
        # Number of boards to show per row on the page.
        self.boards_per_row = 4

        # Calculated sizes
        self.space_size = self.width / 3

    def units(self, v) :
        return str(v) + "mm"
