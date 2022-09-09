

#  Summary of the idea behind the code:
#  The game is created with pygame, but we also need the library random and time.
#  You can easily change the dimensions of the grid by modifying the number of rows and colons or the size of the cells.
#  The positions occupied by the snake are saved in a list. The position of the apple is chosen in generate_apple_position, which generates random numbers until the position is not on the snake.
#  The core of the game is in the infinite loop. There the game doesn't start until the user press one of the directions.
#  Then every cycle of the loop the position of the snake is modified according to the direction chosen. The direction is saved in the list named
#  directions([1,0] is right, [-1,0] is left, [0,1] is down and [0,-1] is up).
#  Every time it is removed the tail of the snake and added to the new position of the head in "snake_list", except when the new position is on an apple.
#  When the head of the snake is on the apple the score is incremented by one and when is equal to the number of cells the user has won. Otherwise, the game ends when
#  the head of the snake is outside the borders or it is on the body of the snake.


# region import
import sys
import pygame
import pygame.freetype
import random
import time
# endregion

# region initial definition
pygame.init()

font_style = pygame.font.SysFont(None, 50)

pygame.display.set_caption("Snake")

DIMENTION_OF_A_CELL = 25
NUM_OF_ROWS = 25
NUM_OF_COLUMNS = 33
SIZE = WIDTH, HEIGHT = DIMENTION_OF_A_CELL * \
    NUM_OF_COLUMNS, DIMENTION_OF_A_CELL*NUM_OF_ROWS
NUMBER_OF_CELLS = NUM_OF_ROWS*NUM_OF_COLUMNS

screen = pygame.display.set_mode(SIZE)

directions = [1, 0]
green = (0, 150, 0)
red = (211, 0, 0)
dark_yellow = (255, 198, 26)
blue = 50, 168, 164

clock = pygame.time.Clock()

# endregion


def generate_apple_position(snake):
    apple_position = [random.randint(0, NUM_OF_COLUMNS-1)*DIMENTION_OF_A_CELL,
                      random.randint(0, NUM_OF_ROWS-1)*DIMENTION_OF_A_CELL]

    while (apple_position in snake):
        apple_position = [random.randint(0, NUM_OF_COLUMNS-1)*DIMENTION_OF_A_CELL,
                          random.randint(0, NUM_OF_ROWS-1)*DIMENTION_OF_A_CELL]

    return apple_position


has_lost = False


def restart():
    global position, score, snake_list, game_over, game_started, apple_position, has_lost
    position = [NUM_OF_COLUMNS//2*DIMENTION_OF_A_CELL,
                NUM_OF_ROWS//2*DIMENTION_OF_A_CELL]
    score = 1
    snake_list = [[position[0], position[1]]]
    game_started = False
    game_over = False
    apple_position = generate_apple_position(snake_list)

    return


restart()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game_started = True
                directions = [-1, 0]
            if event.key == pygame.K_RIGHT:
                game_started = True
                directions = [+1, 0]
            if event.key == pygame.K_DOWN:
                game_started = True
                directions = [0, 1]
            if event.key == pygame.K_UP:
                game_started = True
                directions = [0, -1]

    pygame.draw.rect(screen, blue, [0, 0, WIDTH, HEIGHT])

    if (game_started):
        old_snake = list(snake_list)
        position[0] += DIMENTION_OF_A_CELL*directions[0]
        position[1] += DIMENTION_OF_A_CELL*directions[1]
        snake_list.append(list(position))

        if (position == apple_position):
            score += 1
            if (NUMBER_OF_CELLS == score):
                game_over = True
                has_lost = False
            else:
                apple_position = generate_apple_position(snake_list)

        else:
            snake_list.pop(0)

        if (position[0] >= WIDTH or position[0] < 0 or position[1] >= HEIGHT or position[1] < 0 or [position[0], position[1]] in old_snake and not game_over):
            game_over = True
            has_lost = True
    if not game_over:
        for i in range(0, NUM_OF_COLUMNS):
            for k in range(0, NUM_OF_ROWS):
                if ([i*DIMENTION_OF_A_CELL, k*DIMENTION_OF_A_CELL] == apple_position):
                    pygame.draw.rect(screen, red, [
                        i*DIMENTION_OF_A_CELL, k*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL])
                elif ([i*DIMENTION_OF_A_CELL, k*DIMENTION_OF_A_CELL] not in snake_list):
                    pygame.draw.rect(screen, dark_yellow, [
                        i*DIMENTION_OF_A_CELL, k*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL], 1)
                else:
                    pygame.draw.rect(screen, green, [
                        i*DIMENTION_OF_A_CELL, k*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL])

        pygame.display.flip()

    else:
        pygame.draw.rect(screen, blue, [0, 0, WIDTH, HEIGHT])
        if (has_lost):
            mesg = font_style.render("You lost :(", True, red)
        else:
            mesg = font_style.render("You won!!", True, (50, 168, 164))

        screen.blit(mesg, [WIDTH/2, HEIGHT/2])
        pygame.display.flip()
        time.sleep(2)

    if game_over:
        restart()

    clock.tick(9)
