# import pieces


class Square:

    def __init__(self, row=None, col=None, piece=None, name=None):
        self.row = row
        self.col = col
        self.piece = piece

        if name is not None:
            self.name = name

    def has_pieces(self):
        if self.piece is not None:
            return self.piece

        # return self.piece != None

    @staticmethod  # checking if move is in_rage of the board
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    def is_empty_or_rival(self, color):
        return self.is_empty() or self.has_rival(color)

    def is_empty(self):
        return not self.has_pieces()

    def has_rival(self, color):
        return self.has_pieces() and self.piece.color != color

    def has_team_piece(self, color):
        return self.has_pieces() and self.piece.color == color

    def diagonal_has_team_piece(self, color):
        if self.piece == None:
            return True
        else:
            return self.has_pieces() and self.piece.color == color

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]
