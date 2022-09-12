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
from msilib.schema import Class
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

from costant_screen import *

screen = pygame.display.set_mode(SIZE)

from costant_images import *

directions = [1, 0]
SNAKE_COLOR = (179, 134, 0)
TEXT_COLOR_VICTORY = (140, 217, 179)
TEXT_COLOR_DEFEAT = (255, 51, 51)
APPLE_COLOR = (211, 0, 0)
BORDER_GRID_COLOR = (255, 198, 26)
BACKGROUND_GRID_COLOR = (50, 168, 164)
BACKGROUND_COLOR = (26, 26, 0)


class Direction:
    UP_DIR, RIGHT_DIR, DOWN_DIR, LEFT_DIR = 1, 2, 3, 4


clock = pygame.time.Clock()

# endregion


def generate_apple_position(snake):
    apple_position = [
        random.randint(0, NUM_OF_COLUMNS - 1) * DIMENTION_OF_A_CELL,
        random.randint(0, NUM_OF_ROWS - 1) * DIMENTION_OF_A_CELL,
    ]

    while apple_position in snake:
        apple_position = [
            random.randint(0, NUM_OF_COLUMNS - 1) * DIMENTION_OF_A_CELL,
            random.randint(0, NUM_OF_ROWS - 1) * DIMENTION_OF_A_CELL,
        ]

    return apple_position


has_lost = False


def restart():
    global position, score, snake_list, game_over, game_started, apple_position, has_lost, path

    position = [
        NUM_OF_COLUMNS // 2 * DIMENTION_OF_A_CELL,
        NUM_OF_ROWS // 2 * DIMENTION_OF_A_CELL,
    ]
    score = 1
    snake_list = [[position[0], position[1]]]
    game_started = False
    game_over = False
    pygame.draw.rect(screen, BACKGROUND_COLOR, [0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT])
    path = generate_hamiltonian_cycle(snake_list[0][::-1])
    time.sleep(5)
    print(path)
    apple_position = generate_apple_position(snake_list)

    return


def generate_hamiltonian_cycle(start_pos):
    start_pos[0] //= DIMENTION_OF_A_CELL
    start_pos[1] //= DIMENTION_OF_A_CELL
    grid = []
    for i in range(NUM_OF_ROWS):
        grid.append([])
        for k in range(NUM_OF_COLUMNS):
            grid[i].append(0)

    cont = NUMBER_OF_CELLS
    min_cont = [NUMBER_OF_CELLS]

    stack = []
    stack.append((list(start_pos), cont, 1))
    while True and stack:
        for row in range(NUM_OF_ROWS):
            for col in range(NUM_OF_COLUMNS):

                pygame.draw.rect(
                    screen,
                    BACKGROUND_GRID_COLOR,
                    [
                        MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
                        MARGIN_TOP + row * DIMENTION_OF_A_CELL,
                        DIMENTION_OF_A_CELL,
                        DIMENTION_OF_A_CELL,
                    ],
                )
                pygame.draw.rect(
                    screen,
                    BORDER_GRID_COLOR,
                    [
                        MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
                        MARGIN_TOP + row * DIMENTION_OF_A_CELL,
                        DIMENTION_OF_A_CELL,
                        DIMENTION_OF_A_CELL,
                    ],
                    2,
                )
                if grid[row][col] != 0:
                    match grid[row][col]:
                        case Direction.UP_DIR:
                            imgToInset = HAM_IMG_UP.copy()
                        case Direction.RIGHT_DIR:
                            imgToInset = HAM_IMG_RIGHT.copy()
                        case Direction.DOWN_DIR:
                            imgToInset = HAM_IMG_DOWN.copy()
                        case Direction.LEFT_DIR:
                            imgToInset = HAM_IMG_LEFT.copy()

                    screen.blit(
                        imgToInset,
                        (
                            MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
                            MARGIN_TOP + row * DIMENTION_OF_A_CELL,
                        ),
                    )

        pygame.display.update()

        pos, cont, i = stack[-1]
        if cont == 0:
            if pos == start_pos:
                break
            else:
                stack.pop()
                grid[pos[0]][pos[1]] = 0
                continue

        if min_cont[0] > cont:
            min_cont[0] = cont

        grid[pos[0]][pos[1]] = i
        next_pos = list(pos)
        # 1 up, 2 right, 3 down, 4 left
        match i:
            case Direction.UP_DIR:
                if next_pos[0] > 0 and (
                    grid[next_pos[0] - 1][next_pos[1]] == 0
                    or (cont == 1 and [next_pos[0] - 1, next_pos[1]] == start_pos)
                ):
                    next_pos = [next_pos[0] - 1, next_pos[1]]
            case Direction.RIGHT_DIR:
                if next_pos[1] < NUM_OF_COLUMNS - 1 and (
                    grid[next_pos[0]][next_pos[1] + 1] == 0
                    or (cont == 1 and [next_pos[0], next_pos[1] + 1] == start_pos)
                ):
                    next_pos = [next_pos[0], next_pos[1] + 1]
            case Direction.DOWN_DIR:
                if pos[0] < NUM_OF_ROWS - 1 and (
                    grid[next_pos[0] + 1][next_pos[1]] == 0
                    or (cont == 1 and [next_pos[0] + 1, next_pos[1]] == start_pos)
                ):
                    next_pos = [next_pos[0] + 1, next_pos[1]]
            case Direction.LEFT_DIR:
                if pos[1] > 0 and (
                    grid[next_pos[0]][next_pos[1] - 1] == 0
                    or (cont == 1 and [next_pos[0], next_pos[1] - 1] == start_pos)
                ):
                    next_pos = [next_pos[0], next_pos[1] - 1]
            case _:
                stack.pop()
                grid[pos[0]][pos[1]] = 0
                continue

        stack.pop()
        stack.append((pos, cont, i + 1))
        if next_pos != pos:
            stack.append((next_pos, cont - 1, 1))

    return grid


def getChangeInPosition(row, col):
    match path[row][col]:
        case Direction.UP_DIR:
            directions = [0, -1]
        case Direction.RIGHT_DIR:
            directions = [1, 0]
        case Direction.DOWN_DIR:
            directions = [0, +1]
        case Direction.LEFT_DIR:
            directions = [-1, 0]
    return directions


def getCorrispondingImage(old_pos_grid, new_pos_grid):
    if old_pos_grid == None:
        match path[new_pos_grid[0]][new_pos_grid[1]]:
            case Direction.UP_DIR:
                imgToInset = SNAKE_TOP_BOTTOM.copy()
            case Direction.RIGHT_DIR:
                imgToInset = SNAKE_LEFT_RIGHT.copy()
            case Direction.DOWN_DIR:
                imgToInset = SNAKE_TOP_BOTTOM.copy()
            case Direction.LEFT_DIR:
                imgToInset = SNAKE_LEFT_RIGHT.copy()
    else:
        entering_left = new_pos_grid[1] - old_pos_grid[1] == 1
        entering_right = new_pos_grid[1] - old_pos_grid[1] == -1
        entering_top = new_pos_grid[0] - old_pos_grid[0] == 1
        entering_bottom = new_pos_grid[0] - old_pos_grid[0] == -1

        leaving_top = False
        leaving_right = False
        leaving_bottom = False
        leaving_left = False

        match path[new_pos_grid[0]][new_pos_grid[1]]:
            case Direction.UP_DIR:
                leaving_top = True
            case Direction.RIGHT_DIR:
                leaving_right = True
            case Direction.DOWN_DIR:
                leaving_bottom = True
            case Direction.LEFT_DIR:
                leaving_left = True

        if (entering_left and leaving_top) or (entering_top and leaving_left):
            imgToInset = SNAKE_LEFT_TOP.copy()
        elif (entering_left and leaving_right) or (entering_right and leaving_left):
            imgToInset = SNAKE_LEFT_RIGHT.copy()
        elif (entering_left and leaving_bottom) or (entering_bottom and leaving_left):
            imgToInset = SNAKE_LEFT_BOTTOM.copy()
        elif (entering_top and leaving_right) or (entering_right and leaving_top):
            imgToInset = SNAKE_TOP_RIGHT.copy()
        elif (entering_top and leaving_bottom) or (entering_bottom and leaving_top):
            imgToInset = SNAKE_TOP_BOTTOM.copy()
        elif (entering_right and leaving_bottom) or (entering_bottom and leaving_right):
            imgToInset = SNAKE_RIGHT_BOTTOM.copy()

    return imgToInset


restart()

game_started = True

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    x_Pos, y_Pos = int(position[0] / DIMENTION_OF_A_CELL), int(
        position[1] / DIMENTION_OF_A_CELL
    )
    directions = getChangeInPosition(y_Pos, x_Pos)

    pygame.draw.rect(
        screen,
        BACKGROUND_GRID_COLOR,
        [MARGIN_LEFT, MARGIN_TOP, WIDTH_GRID, HEIGHT_GRID],
    )

    if game_started:
        old_snake = list(snake_list)
        position[0] += DIMENTION_OF_A_CELL * directions[0]
        position[1] += DIMENTION_OF_A_CELL * directions[1]
        snake_list.append(list(position))

        if position == apple_position:
            score += 1
            if NUMBER_OF_CELLS == score:
                game_over = True
                has_lost = False
            else:
                apple_position = generate_apple_position(snake_list)

        else:
            snake_list.pop(0)

        if (
            position[0] >= WIDTH_GRID
            or position[0] < 0
            or position[1] >= HEIGHT_GRID
            or position[1] < 0
            or [position[0], position[1]] in old_snake
            and not game_over
        ):
            game_over = True
            has_lost = True
    if not game_over:
        for col in range(0, NUM_OF_COLUMNS):
            for row in range(0, NUM_OF_ROWS):
                if [
                    col * DIMENTION_OF_A_CELL,
                    row * DIMENTION_OF_A_CELL,
                ] == apple_position:
                    pygame.draw.rect(
                        screen,
                        APPLE_COLOR,
                        [
                            MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
                            MARGIN_TOP + row * DIMENTION_OF_A_CELL,
                            DIMENTION_OF_A_CELL,
                            DIMENTION_OF_A_CELL,
                        ],
                    )
                elif [
                    col * DIMENTION_OF_A_CELL,
                    row * DIMENTION_OF_A_CELL,
                ] not in snake_list:
                    pygame.draw.rect(
                        screen,
                        BORDER_GRID_COLOR,
                        [
                            MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
                            MARGIN_TOP + row * DIMENTION_OF_A_CELL,
                            DIMENTION_OF_A_CELL,
                            DIMENTION_OF_A_CELL,
                        ],
                        1,
                    )
                else:
                    old_pos_grid = None
                    new_pos_grd = (row, col)
                    col_px = col * DIMENTION_OF_A_CELL
                    row_px = row * DIMENTION_OF_A_CELL
                    if (
                        row - 1 >= 0
                        and [col_px, row_px - DIMENTION_OF_A_CELL] in snake_list
                        and path[row - 1][col] == Direction.DOWN_DIR
                    ):
                        old_pos_grid = (row - 1, col)
                    elif (
                        row + 1 < NUM_OF_ROWS
                        and [col_px, row_px + DIMENTION_OF_A_CELL] in snake_list
                        and path[row + 1][col] == Direction.UP_DIR
                    ):
                        old_pos_grid = (row + 1, col)
                    elif (
                        col - 1 >= 0
                        and [col_px - DIMENTION_OF_A_CELL, row_px] in snake_list
                        and path[row][col - 1] == Direction.RIGHT_DIR
                    ):
                        old_pos_grid = (row, col - 1)
                    elif (
                        col + 1 < NUM_OF_COLUMNS
                        and [col_px + DIMENTION_OF_A_CELL, row_px] in snake_list
                        and path[row][col + 1] == Direction.LEFT_DIR
                    ):
                        old_pos_grid = (row, col + 1)

                    imgToInsert = getCorrispondingImage(old_pos_grid, new_pos_grd)
                    screen.blit(
                        imgToInsert,
                        (
                            MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
                            MARGIN_TOP + row * DIMENTION_OF_A_CELL,
                        ),
                    )

        pygame.display.update()

    else:
        pygame.draw.rect(
            screen, BACKGROUND_COLOR, [0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT]
        )
        if has_lost:
            mesg = font_style.render("You lost :(", True, APPLE_COLOR)
        else:
            mesg = font_style.render("You won!!", True, TEXT_COLOR_VICTORY)

        screen.blit(
            mesg,
            [
                DISPLAY_WIDTH / 2 - mesg.get_rect().width / 2,
                DISPLAY_HEIGHT / 2 - mesg.get_rect().height / 2,
            ],
        )
        pygame.display.flip()
        time.sleep(2)

    if game_over:
        restart()
        game_started = True

    clock.tick(15)
