import tkinter
import random
from constants import *
from pieces import *
import pygame
from board import Board
import copy
from square import Square
from move import Move


class ChessAi:
    def __init__(self):
        self.ai_color = ""
        self.ai_pieces = {}
        self.player_pieces = {}
        self.ai_moves = []
        self.player_moves = []
        self.board = Board()
        self.selected_piece = None

    # Get the all the pieces currently on the board
    def get_pieces(self, squares):

        # Delete the pieces which are already captured
        def delete_captured(dict_pieces, ai=False):
            delete = []
            for piece in dict_pieces:
                if piece.captured:
                    delete.append(piece)

            if ai:
                for piece in delete:
                    del self.ai_pieces[piece]
            else:
                for piece in delete:
                    del self.player_pieces[piece]

        for row in range(TABLE_ROWS):
            for col in range(TABLE_COLUMNS):
                piece = squares[row][col].piece

                try:
                    if piece.color == self.ai_color:
                        if not piece.captured:
                            self.ai_pieces[piece] = [row, col]
                        else:
                            pass
                    else:
                        self.player_pieces[piece] = [row, col]
                except AttributeError:
                    pass

        delete_captured(self.ai_pieces, True)
        delete_captured(self.player_pieces, False)

    # Make Move method
    def make_move(self):
        best_move = None
        while best_move is None:
            self.selected_piece = self.best_piece()
            row = self.ai_pieces[self.selected_piece][0]  # Get the row of the best piece
            col = self.ai_pieces[self.selected_piece][1]  # Get the col of the best piece
            self.selected_piece.clear_moves()
            self.board.calc_moves(self.selected_piece, row, col, True, True)  # Find the moves of that pieces

            best_move = self.find_best_move(self.selected_piece, self.selected_piece.valid_moves, row, col)

        self.ai_pieces.clear()
        self.player_pieces.clear()

        return best_move

    # Select the best piece to move
    def best_piece(self):
        dict_best = {}
        for piece in self.ai_pieces:
            self.board.find_moves(piece, self.ai_pieces)
            print(piece.valid_moves)

            dict_best[piece] = self.find_value(piece, piece.valid_moves)

        return self.select_best(dict_best)

    # Find the best value for the piece to be selected
    def find_value(self, piece, moves):
        value = piece.piece_value * 0.5  # Value of the piece
        value += len(moves) * 10       # Number of moves it has

        # if len(moves) == 0:        # If a piece doesn't have any move, make its value -ve
        #     value -= 100
        return value

    def select_best(self, best):  # Among all the pieces with the score, select the piece with the highest value(score)
        score = 0
        for piece in best:
            if score < best[piece]:
                score = best[piece]
        return self.get_key_from_value(best, score)

    def get_key_from_value(self, dict, value):  # Return the piece which has the best value
        for k, v in dict.items():
            if v == value:
                return k
        return None

    def correct_pawns(self, piece, moves):
        # print(piece.game_name)

        for move in moves:  # Testing Code
            for i in range(move.initial.row + 1, move.final.row + 1):
                print(i, move.final.col)
                if self.board.squares[i][move.final.col].has_team_piece(piece.color):
                    print("Yes")

                else:
                    print("No")

                for p in self.ai_pieces:
                    row = self.ai_pieces[p][0]
                    col = self.ai_pieces[p][1]
                    if row == i and col == move.final.col:
                        moves.clear()
        return moves

    def find_best_move(self, piece, moves, row=None, col=None):
        if piece.name == "pawn":
            moves = self.correct_pawns(piece, moves)
            if len(moves) == 0:
                piece.valid_moves.clear()
                del self.ai_pieces[piece]
                self.selected_piece = None
                return None

        dict_moves = {}
        for move in moves:
            score = 0
            for pl_piece in self.player_pieces:  # for all the player pieces
                row = self.player_pieces[pl_piece][0]  # get its row
                col = self.player_pieces[pl_piece][1]  # get its col

                # check if any of the piece has same row and col
                if row == move.final.row and col == move.final.col:
                    score += 1

                    # if the opponent piece value is more than the Ai piece, increment the score by 1
                    if pl_piece.piece_value > piece.piece_value:
                        score += 1

            score += self.board.simulate_move(piece, move)

            dict_moves[piece] = {score: move}


        score = 0
        move = None
        for piece in dict_moves:
            for scr in dict_moves[piece]:
                if scr >= score:
                    score = scr
                    move = dict_moves[piece][score]

        return move

        # best_move = Move(move.initial, move.final)
        # return best_move

            # if score <= dict_moves[piece][0]:
            #     score = dict_moves[piece][0]

        # print(score)





