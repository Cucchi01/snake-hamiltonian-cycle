import pygame

from costant_screen import *


def getImgUsable(IMG):
    IMG.convert()
    return pygame.transform.scale(IMG, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))


HAM_IMG_START = pygame.image.load("image/start-cell.png")
HAM_IMG_START = getImgUsable(HAM_IMG_START)
HAM_IMG_UP = pygame.image.load("image/up-arrow.png")
HAM_IMG_UP = getImgUsable(HAM_IMG_UP)
HAM_IMG_RIGHT = pygame.image.load("image/right-arrow.png")
HAM_IMG_RIGHT = getImgUsable(HAM_IMG_RIGHT)
HAM_IMG_DOWN = pygame.image.load("image/down-arrow.png")
HAM_IMG_DOWN = getImgUsable(HAM_IMG_DOWN)
HAM_IMG_LEFT = pygame.image.load("image/left-arrow.png")
HAM_IMG_LEFT = getImgUsable(HAM_IMG_LEFT)


SNAKE_LEFT_RIGHT = pygame.image.load("image/cell_left_right.png")
SNAKE_LEFT_RIGHT = getImgUsable(SNAKE_LEFT_RIGHT)
SNAKE_LEFT_TOP = pygame.image.load("image/cell_left_up.png")
SNAKE_LEFT_TOP = getImgUsable(SNAKE_LEFT_TOP)
SNAKE_LEFT_BOTTOM = pygame.image.load("image/cell_left_down.png")
SNAKE_LEFT_BOTTOM = getImgUsable(SNAKE_LEFT_BOTTOM)
SNAKE_TOP_RIGHT = pygame.image.load("image/cell_up_right.png")
SNAKE_TOP_RIGHT = getImgUsable(SNAKE_TOP_RIGHT)
SNAKE_TOP_BOTTOM = pygame.image.load("image/cell_up_down.png")
SNAKE_TOP_BOTTOM = getImgUsable(SNAKE_TOP_BOTTOM)
SNAKE_RIGHT_BOTTOM = pygame.image.load("image/cell_right_down.png")
SNAKE_RIGHT_BOTTOM = getImgUsable(SNAKE_RIGHT_BOTTOM)
