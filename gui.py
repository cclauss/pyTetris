__author__ = 'Luiz Felix'

import pygame
import piece


class GUI:
    # positioning constants

    # the +2 is to make space for the area's borders
    AREA_W = 15 * 20 + 2
    AREA_H = 540

    MARGIN_LEFT = 20
    MARGIN_RIGHT = 10
    MARGIN_TOP = 20

    SCORE_AREA_X = MARGIN_LEFT + AREA_W + MARGIN_RIGHT
    SCORE_AREA_Y = MARGIN_TOP + 140

    AREA_LIMIT_X = MARGIN_LEFT + AREA_W
    AREA_LIMIT_Y = MARGIN_TOP + AREA_H

    AREA_MIDDLE = (MARGIN_LEFT + AREA_W) / 2 - 1
    print AREA_MIDDLE
    
    FONT_COLOR = (251, 206, 117)

    def __init__(self, screen):
        self.std_font = pygame.font.SysFont("monospace", 20)
        # std_font = pygame.font.Font(None, 20) # optional font

        self.screen = screen

    def refresh(self, score, level, next_piece):
        self.screen.fill((0, 0, 0))

        # playable area
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.MARGIN_LEFT, self.MARGIN_TOP, self.AREA_W, self.AREA_H), 1)

        # title
        self.screen.blit(self.std_font.render("PyTetris", True, self.FONT_COLOR), ((self.AREA_W -
                                                        self.std_font.size("PyTetris")[0]) / 2 + self.MARGIN_LEFT, 0))

        # next piece
        self.screen.blit(self.std_font.render("Next", True, self.FONT_COLOR), (self.MARGIN_LEFT + self.AREA_W +
                                                                               self.MARGIN_RIGHT, self.MARGIN_TOP - 4))

        next_piece.draw_icon(self.MARGIN_LEFT + self.AREA_W + self.MARGIN_RIGHT, 50, self.screen)

        # score
        self.screen.blit(self.std_font.render("Score", True, self.FONT_COLOR), (self.SCORE_AREA_X, self.SCORE_AREA_Y))
        score_text = self.std_font.render(str(score), True, self.FONT_COLOR)

        # creates left align for the score number
        score_surface = score_text.get_rect()
        score_surface.right = self.SCORE_AREA_X + self.std_font.size("Score")[0]
        score_surface.top = self.SCORE_AREA_Y + 20

        # prints the left-aligned text
        self.screen.blit(score_text, score_surface)

        # level
        self.screen.blit(self.std_font.render("Level", True, self.FONT_COLOR), (self.SCORE_AREA_X, self.SCORE_AREA_Y + 60))
        level_text = self.std_font.render(str(level), True, self.FONT_COLOR)

        # creates left align for the score number
        level_surface = score_text.get_rect()
        level_surface.right = self.SCORE_AREA_X + self.std_font.size("Level")[0]
        level_surface.top = self.SCORE_AREA_Y + 80

        # prints the left-aligned text
        self.screen.blit(level_text, level_surface)