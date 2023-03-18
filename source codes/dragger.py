import pygame
from constants import *


class Dragger:

    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.piece = None
        self.dragging = False

    # method for dragging
    def update_blit(self, surface):
        self.piece.set_texture(size=128)  # changing the image of the piece to bigger
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_cent = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_cent)
        surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos  # tuple (mouseX, mouseY)

    def save_initial(self, pos):
        self.initial_row = pos[1] // BOARD
        self.initial_col = pos[0] // BOARD

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
