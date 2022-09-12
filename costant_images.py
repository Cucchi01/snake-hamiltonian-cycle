import pygame

from costant_screen import *


HAM_IMG_UP = pygame.image.load('image/up-arrow.png')
HAM_IMG_RIGHT = pygame.image.load('image/right-arrow.png')
HAM_IMG_DOWN = pygame.image.load('image/down-arrow.png')
HAM_IMG_LEFT = pygame.image.load('image/left-arrow.png')
HAM_IMG_UP.convert()
HAM_IMG_RIGHT.convert()
HAM_IMG_DOWN.convert()
HAM_IMG_LEFT.convert()
HAM_IMG_UP = pygame.transform.scale(HAM_IMG_UP, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
HAM_IMG_RIGHT = pygame.transform.scale(HAM_IMG_RIGHT, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
HAM_IMG_DOWN = pygame.transform.scale(HAM_IMG_DOWN, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
HAM_IMG_LEFT = pygame.transform.scale(HAM_IMG_LEFT, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))



SNAKE_LEFT_RIGHT = pygame.image.load('image/cell_left_right.png')
SNAKE_LEFT_TOP = pygame.image.load('image/cell_left_up.png')
SNAKE_LEFT_BOTTOM = pygame.image.load('image/cell_left_down.png')
SNAKE_TOP_RIGHT = pygame.image.load('image/cell_up_right.png')
SNAKE_TOP_BOTTOM = pygame.image.load('image/cell_up_down.png')
SNAKE_RIGHT_BOTTOM = pygame.image.load('image/cell_right_down.png')
SNAKE_LEFT_RIGHT.convert()
SNAKE_LEFT_TOP.convert()
SNAKE_LEFT_BOTTOM.convert()
SNAKE_TOP_RIGHT.convert()
SNAKE_TOP_BOTTOM.convert()
SNAKE_RIGHT_BOTTOM.convert()
SNAKE_LEFT_RIGHT = pygame.transform.scale(SNAKE_LEFT_RIGHT, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_LEFT_TOP = pygame.transform.scale(SNAKE_LEFT_TOP, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_LEFT_BOTTOM = pygame.transform.scale(SNAKE_LEFT_BOTTOM, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_TOP_RIGHT = pygame.transform.scale(SNAKE_TOP_RIGHT, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_TOP_BOTTOM = pygame.transform.scale(SNAKE_TOP_BOTTOM, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_RIGHT_BOTTOM = pygame.transform.scale(SNAKE_RIGHT_BOTTOM, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))