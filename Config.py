class Config :
    """
    Configuration class
    """
    def __init__(self) :
        """
        Parses the config file.
        """
        # Width of each board (in mm)
        self.width = 30
        # Colors to use for the moves, only 3 are needed
        self.colors = ["red", "green!50!black", "blue"] 

        # Calculated sizes
        self.space_size = self.width / 3

    def units(self, v) :
        return str(v) + "mm"
