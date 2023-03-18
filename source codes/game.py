
import pygame
from constants import *
from board import Board
from dragger import Dragger
from square import Square
from config import Config
import pandas
from database import SqlData


class Game:
    def __init__(self):

        self.board = Board()
        self.data = SqlData()
        self.next_player = ""
        self.white_data = {}
        self.black_data = {}
        self.dragger = Dragger()
        self.config = Config()
        self.hovered_sqr = None

    def show_background(self, bg):  # Function to show the background of the game on the screen
        theme = self.config.theme

        for row in range(TABLE_ROWS):
            for col in range(TABLE_COLUMNS):

                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * BOARD, row * BOARD, BOARD, BOARD)
                # blit
                pygame.draw.rect(bg, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(TABLE_ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * BOARD)
                    # blit
                    bg.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * BOARD + BOARD - 20, SCREEN_HEIGHT - 20)
                    # blit
                    bg.blit(lbl, lbl_pos)

    # Function to show pieces on the board
    def show_pieces(self, bg):
        # Checking if pieces are present on that board from square module
        for row in range(TABLE_ROWS):
            for col in range(TABLE_COLUMNS):
                if self.board.squares[row][col].has_pieces():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        # Centers the image into a given square
                        img = pygame.image.load(piece.texture)
                        img_cent = col * BOARD + BOARD // 2, row * BOARD + BOARD // 2
                        piece.texture_rect = img.get_rect(center=img_cent)
                        bg.blit(img, piece.texture_rect)

    # This function gets called when game is being saved
    def save(self, user_id):
        for row in range(TABLE_ROWS):
            for col in range(TABLE_COLUMNS):
                if self.board.squares[row][col].has_pieces():
                    piece = self.board.squares[row][col].piece

                    # data = {f"{self.board.squares[row][col].piece.game_name}", (row, col)}

                    if piece.color == "white":        # save the piece data in variable white and black data
                        self.white_data[f"{piece.game_name}"] = row, col, f"{piece.captured}"
                    else:
                        self.black_data[f"{piece.game_name}"] = row, col, f"{piece.captured}"

        self.data.save_func(self.white_data, self.black_data, user_id)

    # After moves are calculated, it is shown on the board from here
    def show_moves(self, bg):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.valid_moves:
                # color

                if Square.in_range(move.final.row, move.final.col):
                    if self.board.squares[move.final.row][move.final.col].has_rival(piece.color):
                        color = "#CD0000" if (move.final.row + move.final.col) % 2 == 0 else "#FF0000"
                    else:
                        color = MOVE_COLOR1 if (move.final.row + move.final.col) % 2 == 0 else MOVE_COLOR2
                else:
                    color = MOVE_COLOR1 if (move.final.row + move.final.col) % 2 == 0 else MOVE_COLOR2

                # rect
                rect = (move.final.col * BOARD, move.final.row * BOARD, BOARD, BOARD)
                # blit
                pygame.draw.rect(bg, color, rect)

    # Changes the playable turn to the other player
    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"
        return self.next_player

    # Displays the last moved that was played by the player
    def show_last_move(self, bg):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * BOARD, pos.row * BOARD, BOARD, BOARD)
                # blit
                pygame.draw.rect(bg, color, rect)


    def show_hover(self, bg):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * BOARD, self.hovered_sqr.row * BOARD, BOARD, BOARD)
            # blit
            pygame.draw.rect(bg, color, rect, width=3)

    # other methods

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured_piece, row=None, col=None):
        if captured_piece:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    # if the piece is captured, then change the captured value to True
    def is_captured(self, captured_piece, row, col):
        if captured_piece:
            try:  # Changes the captured value of the pieces that are captured
                captured_piece.captured = True
            except AttributeError:
                pass

            if captured_piece.color == "white":
                self.white_data[
                    f"{captured_piece.game_name}"] = row, col, f"{captured_piece.captured}"
            else:
                self.black_data[
                    f"{captured_piece.game_name}"] = row, col, f"{captured_piece.captured}"

    # Function to reset the game by calling the game class from the beginning
    def reset(self):
        self.board.reset_names()
        self.__init__()




