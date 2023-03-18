
class Move:

    def __init__(self, initial, final):

        # Remember these initial and final are square. Which was its original and final square
        self.initial = initial
        self.final = final

    def __str__(self):
        k = ""
        k += f"({self.initial.col}, {self.initial.row})"
        k += f' -> ({self.final.col}, {self.final.row})'
        return k

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
