import time
import tkinter
from tkinter import messagebox
import pygame
import sys
import os

from constants import *
from square import Square
from game import Game
from homepage import Button
from login import Login
from move import Move
from chess_ai import ChessAi
import board

new_game = True    # Enables or Disables Login page depending on the Boolean value
game_paused = False  # Signifies whether the game is paused or not


class ChessMain:
    def __init__(self):
        self.player_color = ""
        self.ai_activated = False
        global game_paused

        if new_game:
            self.login = Login()  # Generates a login page
            self.login_check()

        pygame.init()
        icon = pygame.image.load("C:/Users/dilip/PycharmProjects/chessGameAi/assets/images/imgs-128px/white_king.png")
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Chess")

        self.ai = ChessAi()

        self.homepage()  # Calls the homepage function for Main Menu

        self.screen = pygame.display.set_mode((800, 800))  # Change screen size for gameplay
        self.game = Game()
        self.font = pygame.font.SysFont('arialblack', 40)
        self.piece = None
        self.game_ended = False
        game_paused = False

    def login_check(self):
        if self.login.return_failed_login():
            pygame.quit()
            sys.exit()

    def mainloop(self):
        global game_paused
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        game.next_player = self.player_color

        while True:
            if self.ai_activated:
                game.next_player = self.player_color
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if self.game_ended:
                if board.checked_color == "black":
                    messagebox.showinfo("Check Mate", f"White Wins through CheckMate")
                else:
                    messagebox.showinfo("Check Mate", f"Black Wins through CheckMate")
                self.game_ended = False
                self.game_over()
                game = self.game
                board = self.game.board
                dragger = self.game.dragger


            if dragger.dragging:
                dragger.update_blit(self.screen)

            # Check for promotion of the pawns. If the pawns are at either 7th or 0th row, promotes them.
            clicked_row = dragger.mouseY // BOARD
            clicked_col = dragger.mouseX // BOARD

            if board.squares[clicked_row][clicked_col].has_pieces():
                piece = board.squares[clicked_row][clicked_col].piece
                board.check_promotion(piece, clicked_row, clicked_col)  # Function to promote
                # board.king_is_range(piece, clicked_row, clicked_col)


            # Event Handler starts here for handling all the events in the game.
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:  # Get the position of the mouse on the screen
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // BOARD
                    clicked_col = dragger.mouseX // BOARD

                    # checking if a square has a piece on it
                    if board.squares[clicked_row][clicked_col].has_pieces():

                        if board.is_check:   # Checking if the King is in check
                            self.game_ended = board.check_mate()

                        # if yes then assign that piece to variable - piece
                        piece = board.squares[clicked_row][clicked_col].piece

                        # Next Turn (color)
                        if piece.color == game.next_player:  # Change the turn to the next player
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # dragging
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // BOARD
                    motion_col = event.pos[0] // BOARD

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                    #  Mouse button released
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // BOARD
                        released_col = dragger.mouseX // BOARD

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured_piece = board.squares[released_row][released_col].has_pieces()

                            board.move(dragger.piece, move)
                            self.piece = dragger.piece

                            game.play_sound(captured_piece, released_row, released_col)

                            game.show_background(screen)
                            game.show_pieces(screen)

                            # Change to next player
                            game.next_turn()

                            game.is_captured(captured_piece, released_row, released_col)

                            # AI Code not being used in this version of the project.

                            # board.move(dragger.piece, move)
                            # if self.ai_activated:
                            #     # game.next_turn()
                            #     self.ai.get_pieces(board.squares)
                            #     move = self.ai.make_move()
                            #     captured_piece = board.squares[move.final.row][move.final.col].has_pieces()
                            #     board.move(self.ai.selected_piece, move)
                            #     self.piece = self.ai.selected_piece
                            #     game.play_sound(captured_piece, released_row, released_col)
                            #     game.show_background(screen)
                            #     game.show_pieces(screen)
                            #     # Change to next player
                            #     game.next_turn()
                            #     game.is_captured(captured_piece, released_row, released_col)

                    dragger.undrag_piece()
                    # game.reset_names()

                elif event.type == pygame.KEYDOWN:

                    # changing themes
                    if event.key == pygame.K_t and pygame.K_LCTRL:
                        game.change_theme()

                    # Reset Game
                    if event.key == pygame.K_r and pygame.K_LCTRL:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        self.player_color = "white"

                    # Save Game
                    if event.key == pygame.K_s and pygame.K_LCTRL:
                        game.save(self.login.return_uid())

                    # Quit Game
                    if event.key == pygame.K_x and pygame.K_LCTRL:
                        pygame.quit()
                        sys.exit()

                    # Pause Game
                    if event.key == pygame.K_ESCAPE:
                        if not game_paused:
                            self.pause_menu()

                # Event to handle action when clicked on X button in game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            board.clear_moves()
            pygame.display.update()

    # ----------------------------------------------------------------------------------------------#

    # Homepage code
    def homepage(self):
        # The commented code inside this block is for AI which isn't used in this version of the game
        clock = pygame.time.Clock()
        play_button = Button('Play', 200, 40, (300, 400), 5)
        # play_ai_button = Button('Play vs Ai', 200, 40, (300, 500), 5)
        load_button = Button('Load', 200, 40, (300, 500), 5)
        exit_button = Button('Exit', 200, 40, (300, 600), 5)

        while True:  # Event handler checking for mouse click
            self.screen.fill("white")

            logo = pygame.image.load("C:/Users/dilip/PycharmProjects/chessGameAi/assets/images/background/logoMain.png")
            self.screen.blit(logo, (200, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            is_clicked_play = play_button.draw(self.screen)
            # is_clicked_play_ai = play_ai_button.draw(self.screen)
            is_clicked_load = load_button.draw(self.screen)
            is_clicked_exit = exit_button.draw(self.screen)

            pygame.display.update()
            clock.tick(60)

            if is_clicked_play:
                self.ai_activated = False
                self.player_color = "white"
                return 0
            # elif is_clicked_play_ai:
            #     self.select_color()
            #     self.ai_activated = True
            #     return 0

            elif is_clicked_load:
                self.ai_activated = False
                self.player_color = "white"
                board.change_load_state(self.login.return_uid())
                # board.change_load_state(1)
                break
            elif is_clicked_exit:
                exit()

    # Section of the game to select the color of the Player's piece (Used only for AI)
    def select_color(self):
        clock = pygame.time.Clock()
        play_black = Button('Black', 200, 40, (100, 500), 5)
        play_white = Button('White', 200, 40, (500, 500), 5)

        while True:  # Event handler checking for mouse click
            self.screen.fill("white")

            logo = pygame.image.load("C:/Users/dilip/PycharmProjects/chessGameAi/assets/images/background/logoMain.png")
            self.screen.blit(logo, (200, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            is_clicked_play_black = play_black.draw(self.screen)
            is_clicked_play_white = play_white.draw(self.screen)

            pygame.display.update()
            clock.tick(60)

            if is_clicked_play_black:
                self.ai.ai_color = "white"
                self.player_color = "black"
                return 0
            elif is_clicked_play_white:
                self.ai.ai_color = "black"
                self.player_color = "white"
                return 0

    # Function to handle when the Game over
    def game_over(self):
        clock = pygame.time.Clock()
        restart_button = Button('Restart', 200, 40, (300, 450), 5)
        exit_button = Button('Exit', 200, 40, (300, 550), 5)

        while True:  # Event handler checking for mouse click
            self.screen.fill("white")

            logo = pygame.image.load("C:/Users/dilip/PycharmProjects/chessGameAi/assets/images/background/logoMain.png")
            self.screen.blit(logo, (200, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            is_clicked_restart = restart_button.draw(self.screen)
            is_clicked_exit = exit_button.draw(self.screen)

            pygame.display.update()
            clock.tick(60)
            if is_clicked_restart:
                return self.game.reset()
            elif is_clicked_exit:
                exit()

    # Pause Menu module code
    def pause_menu(self):
        global new_game, game_paused
        game_paused = True
        clock = pygame.time.Clock()
        resume_button = Button('Resume', 200, 40, (300, 330), 5)
        menu_button = Button('Main Menu', 200, 40, (300, 430), 5)
        save_button = Button('Save', 200, 40, (300, 530), 5)
        theme_button = Button('Change Theme', 200, 40, (300, 630), 5)
        exit_button = Button('Exit', 200, 40, (300, 730), 5)

        while True:  # Event handler checking for mouse click
            self.screen.fill("white")

            logo = pygame.image.load("C:/Users/dilip/PycharmProjects/chessGameAi/assets/images/background/logoMain.png")
            self.screen.blit(logo, (200, -20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            is_clicked_resume = resume_button.draw(self.screen)
            is_clicked_menu = menu_button.draw(self.screen)
            is_clicked_save = save_button.draw(self.screen)
            is_clicked_theme = theme_button.draw(self.screen)
            is_clicked_exit = exit_button.draw(self.screen)

            pygame.display.update()
            clock.tick(60)
            if is_clicked_resume:
                game_paused = False
                break
            elif is_clicked_menu:
                game_paused = False
                new_game = False
                return self.homepage()
            elif is_clicked_save:
                game_paused = False
                board.change_load_state(self.login.return_uid())
                # board.change_load_state(1)
                break
            elif is_clicked_theme:
                game_paused = False
                self.game.change_theme()
                break
            elif is_clicked_exit:
                exit()

    # --------------------------------------------------------------------------------------------------------------#


# ChessMain is the main class which calls all the other classes
chess = ChessMain()

# Calling the mainloop() function where the game loop starts
chess.mainloop()
