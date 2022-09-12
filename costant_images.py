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
SNAKE_LEFT_UP = pygame.image.load('image/cell_left_up.png')
SNAKE_LEFT_DOWN = pygame.image.load('image/cell_left_down.png')
SNAKE_UP_RIGHT = pygame.image.load('image/cell_up_right.png')
SNAKE_UP_DOWN = pygame.image.load('image/cell_up_down.png')
SNAKE_RIGHT_DOWN = pygame.image.load('image/cell_right_down.png')
SNAKE_LEFT_RIGHT.convert()
SNAKE_LEFT_UP.convert()
SNAKE_LEFT_DOWN.convert()
SNAKE_UP_RIGHT.convert()
SNAKE_UP_DOWN.convert()
SNAKE_RIGHT_DOWN.convert()
SNAKE_LEFT_UP = pygame.transform.scale(HAM_IMG_UP, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
HAM_IMG_UP = pygame.transform.scale(HAM_IMG_UP, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_LEFT_DOWN = pygame.transform.scale(HAM_IMG_UP, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_UP_RIGHT = pygame.transform.scale(HAM_IMG_RIGHT, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_UP_DOWN = pygame.transform.scale(HAM_IMG_DOWN, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))
SNAKE_RIGHT_DOWN = pygame.transform.scale(HAM_IMG_LEFT, (DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL))