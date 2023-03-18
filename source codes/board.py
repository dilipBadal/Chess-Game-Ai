import math
import pandas
import copyreg
from tkinter import messagebox
import random
from constants import *
from square import Square
from pieces import *
from move import Move
import copy
from login import Login
from database import SqlData

game_load = False
no_save = False
game_loaded = False
uid = 0


def change_load_state(user_id):
    global game_load, uid
    game_load = True
    uid = user_id


class Board:

    def __init__(self):
        global uid, game_load
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(TABLE_COLUMNS)]
        self.create()  # Calling this function creates the board for the game
        self.last_move = None
        self.all_moves = []
        self.is_check = False
        self.checked_piece = None
        self.checked_color = None
        self.var = 0
        self.piece_moves = []
        self.ai_moves = []
        self.player_moves = []

        if game_load:
            self.data = SqlData()
            self.data.load_data("white", uid)
            self.data.load_data("black", uid)
            self.load_pieces("white")
            self.load_pieces("black")
            game_load = False
            del self.data

            if no_save and not game_loaded:   # If there is no save file, a new game will be loaded
                messagebox.showerror("No Save File", "No Save detected. \nStaring a new game")
                self.add_pieces("white")
                self.add_pieces("black")
        else:
            self.add_pieces("white")  # Calling add pieces to add white pieces to the board
            self.add_pieces("black")  # Calling add pieces to add black pieces to the board

    def create(self):
        for row in range(TABLE_ROWS):
            for col in range(TABLE_COLUMNS):
                self.squares[row][col] = Square(row, col)  # creates a 2-D Table of objects from 0,0 to 7,7

    def load_pieces(self, color):
        global no_save, game_loaded
        try:
            data_black = pandas.read_csv(f"../../data/{color}_data.csv")
            dic_black = data_black.to_dict()

            for i in range(1, 9, +1):   # Block to load Pawns both white and black

                try:
                    st_row = dic_black[f"pawn{i}"][0]
                    st_col = dic_black[f"pawn{i}"][1]
                except KeyError as e:
                    game_loaded = False
                    no_save = True
                    return 0

                row = int(st_row)
                col = int(st_col)

                if dic_black[f"pawn{i}"][2] == 1:
                    self.squares[row][col] = Square(row, col, Pawns(color), "pawns")
                else:
                    continue

            for i in range(1, 3, +1):  # To load Knights both white and black
                try:

                    st_row = dic_black[f"knight{i}"][0]
                    st_col = dic_black[f"knight{i}"][1]
                except KeyError:
                    game_loaded = False
                    no_save = True
                    return 0

                row = int(st_row)
                col = int(st_col)

                if dic_black[f"knight{i}"][2] == 1:
                    self.squares[row][col] = Square(row, col, Knight(color), "knight")
                else:
                    continue


            for i in range(1, 3, +1):  # To load Rook both white and black
                try:
                    st_row = dic_black[f"rook{i}"][0]
                    st_col = dic_black[f"rook{i}"][1]
                except KeyError:
                    game_loaded = False
                    no_save = True
                    return 0

                row = int(st_row)
                col = int(st_col)

                if dic_black[f"rook{i}"][2] == 1:
                    self.squares[row][col] = Square(row, col, Rook(color), "rook")
                else:
                    continue

            for i in range(1, 3, +1):  # To load Bishop both white and black
                try:
                    st_row = dic_black[f"bishop{i}"][0]
                    st_col = dic_black[f"bishop{i}"][1]
                except KeyError:
                    game_loaded = False
                    no_save = True
                    return 0

                row = int(st_row)
                col = int(st_col)

                if dic_black[f"bishop{i}"][2] == 1:
                    self.squares[row][col] = Square(row, col, Bishop(color), "bishop")
                else:
                    continue

            #  To load the Queen Pieces
            for i in range(1, 2, +1):
                try:
                    st_row = dic_black[f"queen{1}"][0]
                    st_col = dic_black[f"queen{1}"][1]
                except KeyError:
                    game_loaded = False
                    no_save = True
                    return 0

                row = int(st_row)
                col = int(st_col)

                if dic_black[f"queen{1}"][2] == 1:
                    self.squares[row][col] = Square(row, col, Queen(color), "queen")
                else:
                    pass

            #  To Load the King pieces
            for i in range(1, 2, +1):
                try:

                    st_row = dic_black[f"king{1}"][0]
                    st_col = dic_black[f"king{1}"][1]
                except KeyError:
                    game_loaded = False
                    no_save = True
                    return 0

                row = int(st_row)
                col = int(st_col)

                if dic_black[f"king{1}"][2] == 1:
                    self.squares[row][col] = Square(row, col, King(color), "king")
                else:
                    pass

            game_loaded = True

        except FileNotFoundError:
            no_save = True


    def add_pieces(self, color):
        # Assigning the rows of white and black pawns and other pieces
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        for col in range(TABLE_COLUMNS):
            # Calls Pawn class to set the pawns in their position acc to their color
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawns(color), "pawns")

        # knights
        # Here 1 and 6 are the columns where Knights actually start their position
        self.squares[row_other][1] = Square(row_other, 1, Knight(color), "knights")
        self.squares[row_other][6] = Square(row_other, 6, Knight(color), "kinghts")

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color), "bishops")
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color), "bishops")

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color), "rooks")
        self.squares[row_other][7] = Square(row_other, 7, Rook(color), "rooks")

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color), "queen")

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color), "king")

    def check_promotion(self, piece, row, col):
        if piece.color == "white" and row == 0 and piece.name == "pawn":
            self.squares[row][col] = Square(7, 3, Queen(piece.color))
        elif piece.color == "black" and row == 7 and piece.name == "pawn":
            self.squares[row][col] = Square(6, 3, Queen(piece.color))

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        # move the piece on the deep copy of the board
        temp_board.move(temp_piece, move)

        # check if any rival pieces can capture the king
        for row in range(TABLE_ROWS):
            for col in range(TABLE_COLUMNS):
                if temp_board.squares[row][col].has_rival(piece.color):
                    p = temp_board.squares[row][col].piece

                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.valid_moves:
                        if isinstance(m.final.piece, King):
                            self.is_check = True
                            self.checked_piece = m.final.piece
                            self.checked_color = m.final.piece.color
                            return True

        self.is_check = False
        return False

    def calc_moves(self, piece=None, row=None, col=None, bool=True, ai=False, ply=None):
        self.ai_moves = []
        self.player_moves = []

        def pawn_moves():
            # Checking if a pawn has already moved
            steps = 1 if piece.moved else 2

            # Vertical Moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # then creating new move
                        move = Move(initial, final)

                        # if bool and piece.color == "black" and ai:
                        #     print(f"These are the moves {move.final.row}, {move.final.col}, {piece.game_name}")

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                    else:  # Cannot move if the first square is empty
                        break
                else:  # Not in range to move forward
                    break

            # Diagonal Moves (only while Capturing other pieces)
            move_row = row + piece.dir
            move_cols = (col-1, col+1)

            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)
                        # then creating new move
                        move = Move(initial, final)
                        # append new move
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)


        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col-2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
                (row-1, col+2),

            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(color=piece.color):
                        initial = Square(row, col)  # Square that we are in right now
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)  # Piece = Piece, square we will be once we move
                        # Move
                        move = Move(initial, final)

                        # appending new valid moves
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                                    self.all_moves.append(move)
                            else:
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_rival(piece.color):
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                                    self.all_moves.append(move)
                            else:
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def move_straight(move_row, move_col, addone=None, subone=None, actual_value_1=None, actual_value_2=None,
                          our_row=0, our_col=0):

            for rows in range(move_row + subone, our_row + actual_value_1, -1):  # Check for upper side
                if Square.in_range(rows):
                    if self.squares[rows][move_col].is_empty():
                        initial = Square(move_row, move_col)
                        final_piece = self.squares[rows][move_col].piece
                        final = Square(rows, move_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)

                    elif self.squares[rows][move_col].has_rival(color=piece.color):
                        initial = Square(move_row, move_col)
                        final = Square(rows, move_col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break

                    elif self.squares[rows][move_col].has_team_piece(color=piece.color):
                        break

            for rows in range(move_row + addone, our_row + actual_value_2, +1):  # Checks for pieces in the lower side  8
                if Square.in_range(rows):
                    if self.squares[rows][move_col].is_empty():
                        initial = Square(move_row, move_col)
                        final_piece = self.squares[rows][move_col].piece
                        final = Square(rows, move_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)

                    elif self.squares[rows][move_col].has_rival(color=piece.color):
                        initial = Square(move_row, move_col)
                        final_piece = self.squares[rows][move_col].piece
                        final = Square(rows, move_col, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break

                    elif self.squares[rows][move_col].has_team_piece(color=piece.color):
                        break

            for cols in range(move_col + addone, our_col + actual_value_2, +1):   # Checks for pieces to the right side
                if cols <= 7:
                    if self.squares[move_row][cols].is_empty():
                        initial = Square(move_row, move_col)
                        final_piece = self.squares[move_row][cols].piece
                        final = Square(move_row, cols, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)

                    elif self.squares[move_row][cols].has_rival(color=piece.color):
                        initial = Square(move_row, move_col)
                        final_piece = self.squares[move_row][cols].piece
                        final = Square(move_row, cols, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break

                    elif self.squares[move_row][cols].has_team_piece(color=piece.color):
                        break
                else:
                    break

            for cols in range(move_col + subone, our_col + actual_value_1, -1):   # Checks for pieces to the left side
                if cols >= 0:
                    if self.squares[move_row][cols].is_empty():
                        initial = Square(move_row, move_col)
                        final_piece = self.squares[move_row][cols].piece
                        final = Square(move_row, cols, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)

                    elif self.squares[move_row][cols].has_rival(color=piece.color):
                        initial = Square(move_row, move_col)
                        final_piece = self.squares[move_row][cols].piece
                        final = Square(move_row, cols, final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break
                    elif self.squares[move_row][cols].has_team_piece(color=piece.color):
                        break
                else:
                    break

        # def rook_move():  # Function to check Rook's Move
        #     move_straight(move_row=row, move_col=col, actual_value_1=-1, actual_value_2=8, addone=1, subone=-1)

        def move_diagonal(current_row, current_col):
            initial = Square(current_row, current_col)

            # Checking for top left side
            rows = current_row
            cols = current_col
            encountered = False
            while not encountered:
                rows -= 1
                cols -= 1
                if Square.in_range(rows, cols):
                    if self.squares[rows][cols].is_empty():
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)

                    elif self.squares[rows][cols].has_team_piece(piece.color):
                        encountered = True
                        break

                    elif self.squares[rows][cols].has_rival(piece.color):
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break
                    else:
                        break
                else:
                    break

            # checking for top right
            rows = current_row
            cols = current_col
            while True:
                rows -= 1  # to move up
                cols += 1  # to move to right
                if Square.in_range(rows, cols):
                    if self.squares[rows][cols].is_empty():
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                    elif self.squares[rows][cols].has_team_piece(piece.color):
                        encountered = True
                        break

                    elif self.squares[rows][cols].has_rival(piece.color):
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break
                    else:
                        break
                else:
                    break

            # Check for bottom left
            rows = current_row
            cols = current_col
            while True:
                rows += 1
                cols -= 1
                if Square.in_range(rows, cols):
                    if self.squares[rows][cols].is_empty():
                        initial = Square(rows, cols)
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                    elif self.squares[rows][cols].has_team_piece(piece.color):
                        encountered = True
                        break

                    elif self.squares[rows][cols].has_rival(piece.color):
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break
                    else:
                        break
                else:
                    break

            #  Check for bottom right
            rows = current_row
            cols = current_col
            while True:
                rows += 1
                cols += 1
                if Square.in_range(rows, cols):
                    if self.squares[rows][cols].is_empty():
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                    elif self.squares[rows][cols].has_team_piece(piece.color):
                        encountered = True
                        break

                    elif self.squares[rows][cols].has_rival(piece.color):
                        final_piece = self.squares[rows][cols].piece
                        final = Square(rows, cols, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                                self.all_moves.append(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)
                            self.all_moves.append(move)
                        break
                    else:
                        break
                else:
                    break

        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                pass
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_pieces():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_pieces():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        if isinstance(piece, Pawns):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1),  # left
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1)  # left
            ])

        elif isinstance(piece, King):
            king_moves()

        if ai and bool:
            self.ai_moves = piece.valid_moves

        if ai and ply and bool:
            self.player_moves = piece.valid_moves

        self.var = 1

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None

        if final.row > 7 or final.col > 7:
            pass
        else:
            self.squares[final.row][final.col].piece = piece

        # move
        try:
            piece.moved = True
        except AttributeError:
            pass

        # set last move
        self.last_move = move
        self.piece_moves = piece.valid_moves
        piece.clear_moves()

    def check_mate(self):
        for row in range(TABLE_ROWS):
            for col in range(TABLE_COLUMNS):
                p = self.squares[row][col].piece

                try:
                    p_color = p.color
                except AttributeError:
                    p_color = None

                if p_color == self.checked_color and p is not None:
                    self.calc_moves(p, row, col, bool=True)
                    self.all_moves.append(p.valid_moves)

        length = 0

        try:
            for moves in self.all_moves:
                length += len(moves)
            if length == 0:
                return True
            else:
                return False
        except Exception as e:
            pass

        self.all_moves.clear()
        return False

    def valid_move(self, piece, move):
        return move in piece.valid_moves

    def clear_moves(self):
        self.all_moves.clear()

    def simulate_move(self, piece, move):
        score = 0
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        # move the piece on the deep copy of the board
        temp_board.move(temp_piece, move)

        for row in range(TABLE_ROWS):     # Check if any piece can capture the current piece
            for col in range(TABLE_COLUMNS):
                if temp_board.squares[row][col].has_rival(piece.color):
                    p = temp_board.squares[row][col].piece

                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.valid_moves:
                        if isinstance(m.final.piece, type(piece)):
                            score -= 1
                        else:
                            score += 1
        return score

    def find_moves(self, piece, all_pieces):
        row = all_pieces[piece][0]
        col = all_pieces[piece][1]
        self.calc_moves(piece, row, col, bool=True, ai=True)

    def reset_names(self):
        Pieces.reset_names()

