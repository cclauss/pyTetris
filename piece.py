__author__ = 'luiz'

import pygame
import numpy as np

SMALL_BLOCK = 10
BIG_BLOCK = 20


class Piece:
    def __init__(self, shape, number, color, dim=(2, 3)):
        self.shape = np.array(shape)
        self.color = color
        self.working_shape = self.shape[:]

        self.dimensions = dim
        self.working_dim = dim

        self.number = number

    def reset(self):
        self.working_shape = self.shape
        self.working_dim = self.dimensions

    def draw_piece(self, x, y, surface):
        for i, _ in enumerate(self.working_shape):
            for j, _ in enumerate(self.working_shape[i]):
                if self.working_shape[i][j]:
                    pygame.draw.rect(surface, self.color, pygame.Rect(x + j * BIG_BLOCK, y + i * BIG_BLOCK,
                                                                      BIG_BLOCK - 1, BIG_BLOCK - 1))

    def draw_icon(self, x, y, surface):
        for i, _ in enumerate(self.shape):
            for j, _ in enumerate(self.shape[i]):
                if self.shape[i][j]:
                    pygame.draw.rect(surface, self.color, pygame.Rect(x + j * BIG_BLOCK, y + i * BIG_BLOCK,
                                                                      BIG_BLOCK - 1, BIG_BLOCK - 1))

    def rotate(self):
        self.working_shape = np.rot90(self.working_shape)
        self.working_dim = (self.working_dim[1], self.working_dim[0])

    def get_number(self):
        return self.number

    def get_dimensions(self):
        return self.working_dim

    def get_rotated_dimensions(self):
        # 1 is subtracted from x because the piece will rotate over the cursor position, which
        # matches with the 1st column of the sprite
        return (self.working_dim[1], self.working_dim[0])


