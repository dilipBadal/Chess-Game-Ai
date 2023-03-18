
import math
import os.path
pawn_nWhite = 1
pawn_nBlack = 1

Knight_nWhite = 1
Knight_nBlack = 1

Bishop_nWhite = 1
Bishop_nBlack = 1

Rook_nWhite = 1
Rook_nBlack = 1

Queen_nWhite = 1
Queen_nBlack = 1

King_nWhite = 1
King_nBlack = 1


class Pieces:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        global pawn_nWhite, pawn_nBlack, King_nWhite, King_nBlack, Knight_nWhite, Knight_nBlack, Queen_nBlack, Queen_nWhite
        global Bishop_nBlack, Bishop_nWhite, Rook_nWhite, Rook_nBlack

        self.piece_value = value
        self.name = name
        self.color = color
        self.value_sign = 1 if color == "white" else -1
        self.value = value * self.value_sign
        self.texture = texture
        self.set_texture()
        self.valid_moves = []
        self.moved = False
        self.texture_rect = texture_rect
        self.captured = False

        if name == "pawn" and color == "white":
            self.game_name = f"{name}{pawn_nWhite}"

            if pawn_nWhite >= 9:   # if the pawn number is over 8 then subtract it by 8, so it gets reset.
                self.game_name = f"{name}{pawn_nWhite-8}"
            pawn_nWhite += 1

        elif name == "pawn" and color == "black":
            self.game_name = f"{name}{pawn_nBlack}"
            if pawn_nBlack >= 9:
                self.game_name = f"{name}{pawn_nBlack-8}"
            pawn_nBlack += 1

        if name == "knight" and color == "white":
            self.game_name = f"{name}{Knight_nWhite}"
            if Knight_nWhite >= 3:
                self.game_name = f"{name}{Knight_nWhite - 2}"
            Knight_nWhite += 1
        elif name == "knight" and color == "black":
            self.game_name = f"{name}{Knight_nBlack}"
            if Knight_nBlack >= 3:
                self.game_name = f"{name}{Knight_nBlack - 2}"
            Knight_nBlack += 1

        if name == "bishop" and color == "white":
            self.game_name = f"{name}{Bishop_nWhite}"
            if Bishop_nWhite >= 3:
                self.game_name = f"{name}{Bishop_nWhite - 2}"
            Bishop_nWhite += 1
        elif name == "bishop" and color == "black":
            self.game_name = f"{name}{Bishop_nBlack}"
            if Bishop_nBlack >= 3:
                self.game_name = f"{name}{Bishop_nBlack - 2}"
            Bishop_nBlack += 1

        if name == "rook" and color == "white":
            self.game_name = f"{name}{Rook_nWhite}"
            if Rook_nWhite >= 3:
                self.game_name = f"{name}{Rook_nWhite - 2}"
            Rook_nWhite += 1
        elif name == "rook" and color == "black":
            self.game_name = f"{name}{Rook_nBlack}"
            if Rook_nBlack >= 3:
                self.game_name = f"{name}{Rook_nBlack - 2}"
            Rook_nBlack += 1

        if name == "queen" and color == "white":
            self.game_name = f"{name}{Queen_nWhite}"

            if Queen_nWhite >= 2:
                self.game_name = f"{name}{Queen_nWhite - 1}"
            Queen_nWhite += 1
        elif name == "queen" and color == "black":
            self.game_name = f"{name}{Queen_nBlack}"
            if Queen_nBlack >= 2:
                self.game_name = f"{name}{Queen_nBlack - 1}"
            Queen_nBlack += 1

        if name == "king" and color == "white":
            self.game_name = f"{name}{King_nWhite}"
            if King_nWhite >= 2:
                self.game_name = f"{name}{King_nWhite - 1}"
            King_nWhite += 1
        elif name == "king" and color == "black":
            self.game_name = f"{name}{King_nBlack}"
            if King_nBlack >= 2:
                self.game_name = f"{name}{King_nBlack - 1}"
            King_nBlack += 1

    @staticmethod
    def reset_names():  # Reset names when the game is reset
        global pawn_nWhite, pawn_nBlack, Knight_nBlack, Knight_nWhite, Bishop_nWhite, Bishop_nBlack, Rook_nBlack
        global Rook_nWhite, Queen_nWhite, Queen_nBlack, King_nWhite, King_nBlack
        pawn_nWhite = 1
        pawn_nBlack = 1

        Knight_nWhite = 1
        Knight_nBlack = 1

        Bishop_nWhite = 1
        Bishop_nBlack = 1

        Rook_nWhite = 1
        Rook_nBlack = 1

        Queen_nWhite = 1
        Queen_nBlack = 1

        King_nWhite = 1
        King_nBlack = 1

    def set_texture(self, size=80):
        self.texture = os.path.join(f"C:/Users/dilip/PycharmProjects/chessAi/assets/images/imgs-{size}px/{self.color}_{self.name}.png")   # images path in our project folder
    
    def add_move(self, move):
        self.valid_moves.append(move)

    def clear_moves(self):
        self.valid_moves = []



class Pawns(Pieces):

    def __init__(self, color):
        self.dir = -1 if color == "white" else 1  # sets the direction of the pawns
        super().__init__(name="pawn", color=color, value=1.0)


class Knight(Pieces):
    def __init__(self, color):
        super().__init__(name="knight", color=color, value=3.0)


class Bishop(Pieces):
    def __init__(self, color):
        super().__init__(name="bishop", color=color, value=3.001)


class Rook(Pieces):
    def __init__(self, color):
        super().__init__(name="rook", color=color, value=5)


class Queen(Pieces):
    def __init__(self, color):
        super().__init__(name="queen", color=color, value=9)


class King(Pieces):
    def __init__(self, color):
        super().__init__(name="king", color=color, value=10)

