__author__ = 'luiz'

import pygame
import sys
import numpy as np
from random import randint

import piece
import gui


class pyTetris:
    CLOCK_DELAY = 200 # milisseconds
    FPS = 30
    SCREEN_W = 400
    SCREEN_H = 580

    def __init__(self):
        # pygame preamble
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        pygame.display.set_caption("PyTetris")

        # game setup
        self.gui_manager = gui.GUI(self.screen)

        self.DISPLAY_W = self.gui_manager.AREA_W / piece.BIG_BLOCK
        self.DISPLAY_H = self.gui_manager.AREA_H / piece.BIG_BLOCK

        print "Working on yx: %d x %d" % (self.DISPLAY_H, self.DISPLAY_W)

        # the logic
        self.display = np.zeros(shape=(self.DISPLAY_H, self.DISPLAY_W), dtype=np.int8)

        # setting FPS
        self.clock = pygame.time.Clock()

        # positioning the cursor on the screen and on the matrix
        self.colors = []
        self._reset_cursor()

        # generate first and seconds pieces
        self._init_pieces()

        # self.current_piece = self.pieces[randint(0, len(self.pieces) - 1)]

        self.current_piece = self.pieces[6]

        self.next_piece = self.pieces[randint(0, len(self.pieces) - 1)]

        # time of the last update. 0 because it never happened. If it is set to now, it will take some time for the
        # first update happen
        self.last_update = 0

        self.gameOver = False

    def _init_pieces(self):
        # yellow, violet, green, cyan, white, gold, magenta (almost)
        self.colors = [(255, 255, 0), (204, 0, 255), (0, 255, 0), (0, 255, 239), (255, 255, 255), (255, 165, 0),
                       (244, 21, 140)]

        J = piece.Piece([[1, 0, 0], [1, 1, 1]], 1, self.colors[0])
        L = piece.Piece([[0, 0, 1], [1, 1, 1]], 2, self.colors[1])
        T = piece.Piece([[0, 1, 0], [1, 1, 1]], 3, self.colors[2])
        S = piece.Piece([[0, 1, 1], [1, 1, 0]], 4, self.colors[3])
        Z = piece.Piece([[1, 1, 0], [0, 1, 1]], 5, self.colors[4])
        O = piece.Piece([[1, 1], [1, 1]], 6, self.colors[5], (2, 2))
        I = piece.Piece([[1], [1], [1], [1]], 7, self.colors[6], (4, 1))

        self.pieces = [J, L, T, S, Z, O, I]

    def _reset_cursor(self):
        # the matrix is 0-indexed, subtract 1 from digitl_x
        self.digital_x = self.gui_manager.AREA_MIDDLE / piece.BIG_BLOCK - 1
        self.digital_y = 0

        self.cursor_x = self.gui_manager.AREA_MIDDLE
        self.cursor_y = self.gui_manager.MARGIN_TOP + 1   # added 1 because there is the rectangle's border

    def paint_matrix(self):
        for y in range(self.display.shape[0]):
            for x in range(self.display.shape[1]):
                if self.display[y][x] > 0:
                    # the + 1 is to consider the 1 pixel space used by the upper border
                    # the + 11 is +1 for the left border too and +10 to make the center of the screen be
                    # a multiple of 20, which is the size of each square. This value is defined on gui.py

                    pygame.draw.rect(self.screen, self.colors[self.display[y][x] - 1],
                                     pygame.Rect(self.gui_manager.MARGIN_RIGHT + 10 + x  * piece.BIG_BLOCK,
                                                 self.gui_manager.MARGIN_TOP + 1 + y * piece.BIG_BLOCK,
                                     piece.BIG_BLOCK - 1, piece.BIG_BLOCK - 1))

    def _intersects(self, x, y, piece):
        for i in range(piece.get_dimensions()[0]):
            for j in range (piece.get_dimensions()[1]):
                if self.display[y + i][x + j] != 0:
                    if piece.working_shape[i][j] != 0:
                        return True

    def update(self):
        while not self.gameOver:
            # erase previous state' screen and redraws GUI

            self.screen.fill((0, 0, 0))
            self.gui_manager.refresh(0, 0, self.next_piece)
            self.paint_matrix()
            self.current_piece.draw_piece(self.cursor_x, self.cursor_y, self.screen)

            # events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # there is no need to multiply the piece's size by its size, since the cursor is on the top-lefr
                    # corner of the object and moving to left is shifting one (free) unit to the right

                    if event.key == pygame.K_LEFT and self.digital_x - 1 >= 0 and not \
                            self._intersects(self.digital_x - 1, self.digital_y, self.current_piece):
                        self.cursor_x -= piece.BIG_BLOCK
                        self.digital_x -= 1

                    # fix for many pieces
                    if event.key == pygame.K_RIGHT and self.digital_x + self.current_piece.get_dimensions()[1] < \
                            self.DISPLAY_W and not self._intersects(self.digital_x + 1,
                                                                    self.digital_y, self.current_piece):
                        self.cursor_x += piece.BIG_BLOCK
                        self.digital_x += 1

                    # improve
                    if event.key == pygame.K_UP:
                        if self.cursor_x + piece.BIG_BLOCK * self.current_piece.get_rotated_dimensions()[1] <= self.gui_manager.AREA_LIMIT_X \
                            and self.cursor_y + piece.BIG_BLOCK * self.current_piece.get_rotated_dimensions()[0] <= self.gui_manager.AREA_LIMIT_Y:
                                self.current_piece.rotate()


            if pygame.time.get_ticks() - self.last_update > self.CLOCK_DELAY:
                # checking if this piece can fall
                moving = True

                if self.digital_y + self.current_piece.get_dimensions()[0] + 1 > self.DISPLAY_H:
                    moving = False
                else:
                    print '>> %d, %d' % (self.current_piece.get_dimensions()[0], self.current_piece.get_dimensions()[1])
                    print '$$ %d, %d' % (self.digital_x, self.digital_y)

                    for i in range(self.current_piece.get_dimensions()[0]):
                        for j in range(self.current_piece.get_dimensions()[1]):
                            if self.current_piece.working_shape[i][j] != 0 and \
                                            self.display[self.digital_y + i + 1][self.digital_x + j] != 0:
                                moving = False

                if moving:
                    self.cursor_y += piece.BIG_BLOCK
                    self.digital_y += 1
                else:
                    # mark the occupied slots on the matrix
                    tag = self.current_piece.get_number()

                    for i in range(self.current_piece.get_dimensions()[0]):
                        for j in range(self.current_piece.get_dimensions()[1]):
                            if (self.current_piece.working_shape[i][j] != 0):
                                self.display[self.digital_y + i][self.digital_x + j] = tag

                    # print self.display

                    self.current_piece.reset()

                    self._reset_cursor()
                    self.current_piece = self.next_piece
                    self.next_piece = self.pieces[randint(0, len(self.pieces) - 1)]

                self.last_update = pygame.time.get_ticks()

            self.clock.tick(self.FPS)
            pygame.display.flip()