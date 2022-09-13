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
from collections import namedtuple

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

TIME_SLEEP_HAMILTONIAN = 0  # 0.05
CLOCK_TICK = 6


class Direction:
    UP_DIR, RIGHT_DIR, DOWN_DIR, LEFT_DIR = 1, 2, 3, 4


Point = namedtuple("Point", "row col")


clock = pygame.time.Clock()

# endregion


def gameLoop() -> None:
    global directions, old_snake_list, game_over, has_lost, position_head
    while 1:
        manageEvents()
        directions = getChangeInPosition(position_head)

        pygame.draw.rect(
            screen,
            BACKGROUND_GRID_COLOR,
            [MARGIN_LEFT, MARGIN_TOP, WIDTH_GRID, HEIGHT_GRID],
        )

        old_snake_list = list(snake_list)
        position_head = updateSnake()

        if isGameLost():
            game_over = True
            has_lost = True

        if not game_over:
            drawGridGame()
        else:
            drawGameOver()

        if game_over:
            restart()

        clock.tick(CLOCK_TICK)


def manageEvents() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def restart() -> None:
    global position_head, score, snake_list, game_over, apple_position, has_lost, path

    position_head = [
        NUM_OF_COLUMNS // 2 * DIMENTION_OF_A_CELL,
        NUM_OF_ROWS // 2 * DIMENTION_OF_A_CELL,
    ]
    score = 1
    snake_list = [[position_head[0], position_head[1]]]
    game_over = False
    has_lost = False
    pygame.draw.rect(screen, BACKGROUND_COLOR, [0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT])
    path = generation_hamiltonian_cycle(snake_list[0][::-1])

    gamePause(5)

    apple_position = generate_apple_position(snake_list)

    return


def gamePause(seconds: float) -> None:
    startTime = time.time()
    while time.time() - startTime < seconds:
        manageEvents()


def generate_apple_position(snake: list) -> list:
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


def getChangeInPosition(position_head: "Point") -> Direction:
    col, row = int(position_head[0] / DIMENTION_OF_A_CELL), int(
        position_head[1] / DIMENTION_OF_A_CELL
    )

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


def generation_hamiltonian_cycle(start_pos: "Point") -> list:
    start_pos[0] //= DIMENTION_OF_A_CELL
    start_pos[1] //= DIMENTION_OF_A_CELL
    grid = emptyMatrix()

    cells_to_fill_remaining = NUMBER_OF_CELLS

    StackFrame = namedtuple("StackFrame", "position n_remaining_cells direction_to_try")

    stack = []
    stack.append(StackFrame(list(start_pos), cells_to_fill_remaining, 1))
    while True and stack:
        gamePause(TIME_SLEEP_HAMILTONIAN)
        manageEvents()

        drawGridHamiltonian(start_pos, grid)

        pos, cells_to_fill_remaining, direction_to_try = stack[-1]

        if cells_to_fill_remaining == 0:
            if pos == start_pos:
                break
            else:
                stack.pop()
                grid[pos[0]][pos[1]] = 0
                continue

        grid[pos[0]][pos[1]] = direction_to_try

        next_pos, end_possible_directions = getNextPosition(
            pos, direction_to_try, grid, cells_to_fill_remaining, start_pos
        )

        if end_possible_directions == True:
            stack.pop()
            grid[pos[0]][pos[1]] = 0
            continue

        stack.pop()
        stack.append(StackFrame(pos, cells_to_fill_remaining, direction_to_try + 1))
        if next_pos != pos:
            stack.append((next_pos, cells_to_fill_remaining - 1, 1))

    return grid


def emptyMatrix(
    n_rows: "int" = NUM_OF_ROWS, n_cols: "int" = NUM_OF_COLUMNS, def_value: "int" = 0
) -> "list":
    grid = []
    for i in range(n_rows):
        grid.append([])
        for k in range(n_cols):
            grid[i].append(def_value)

    return grid


def drawGridHamiltonian(start_pos: "Point", grid: "list") -> None:
    for row in range(NUM_OF_ROWS):
        for col in range(NUM_OF_COLUMNS):
            drawCellHam(row, col, start_pos, grid)

    pygame.display.update()


def drawCellHam(row: "int", col: "int", start_pos: "Point", grid: "list") -> None:
    drawEmptyCellHam(row, col)
    if [row, col] == start_pos:
        drawStartHamCycle(row, col)
    elif grid[row][col] != 0:
        drawDirectionCell(row, col, grid)


def drawStartHamCycle(row: "int", col: "int") -> None:
    screen.blit(
        HAM_IMG_START.copy(),
        (
            MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
            MARGIN_TOP + row * DIMENTION_OF_A_CELL,
        ),
    )


def drawDirectionCell(row: int, col: int, grid: list):
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


def drawEmptyCellHam(row: int, col: int) -> None:
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


def getNextPosition(
    pos: "Point",
    direction_to_try: Direction,
    grid: list,
    cells_to_fill_remaining: int,
    start_pos: "Point",
) -> tuple:
    next_pos = list(pos)
    end_possible_dir = False

    match direction_to_try:
        case Direction.UP_DIR:
            if isMovementUpPossibleHam(pos, grid, start_pos, cells_to_fill_remaining):
                next_pos = [next_pos[0] - 1, next_pos[1]]
        case Direction.RIGHT_DIR:
            if isMovementRightPossibleHam(
                pos, grid, start_pos, cells_to_fill_remaining
            ):
                next_pos = [next_pos[0], next_pos[1] + 1]
        case Direction.DOWN_DIR:
            if isMovementDownPossibleHam(pos, grid, start_pos, cells_to_fill_remaining):
                next_pos = [next_pos[0] + 1, next_pos[1]]
        case Direction.LEFT_DIR:
            if isMovementLeftPossibleHam(pos, grid, start_pos, cells_to_fill_remaining):
                next_pos = [next_pos[0], next_pos[1] - 1]
        case _:
            end_possible_dir = True

    return next_pos, end_possible_dir


def isMovementUpPossibleHam(
    pos: "Point", grid: list, start_pos: "Point", cells_to_fill_remaining: int
) -> bool:
    return pos[0] > 0 and (
        grid[pos[0] - 1][pos[1]] == 0
        or (cells_to_fill_remaining == 1 and [pos[0] - 1, pos[1]] == start_pos)
    )


def isMovementRightPossibleHam(
    pos: "Point", grid: list, start_pos: "Point", cells_to_fill_remaining: int
) -> bool:
    return pos[1] < NUM_OF_COLUMNS - 1 and (
        grid[pos[0]][pos[1] + 1] == 0
        or (cells_to_fill_remaining == 1 and [pos[0], pos[1] + 1] == start_pos)
    )


def isMovementDownPossibleHam(
    pos: "Point", grid: list, start_pos: "Point", cells_to_fill_remaining: int
) -> bool:
    return pos[0] < NUM_OF_ROWS - 1 and (
        grid[pos[0] + 1][pos[1]] == 0
        or (cells_to_fill_remaining == 1 and [pos[0] + 1, pos[1]] == start_pos)
    )


def isMovementLeftPossibleHam(
    pos: "Point", grid: list, start_pos: "Point", cells_to_fill_remaining: int
) -> bool:
    return pos[1] > 0 and (
        grid[pos[0]][pos[1] - 1] == 0
        or (cells_to_fill_remaining == 1 and [pos[0], pos[1] - 1] == start_pos)
    )


def updateSnake() -> "Point":
    global game_over, has_lost, snake_list, score, apple_position
    position_head[0] += DIMENTION_OF_A_CELL * directions[0]
    position_head[1] += DIMENTION_OF_A_CELL * directions[1]
    snake_list.append(list(position_head))

    if position_head == apple_position:
        score += 1
        if NUMBER_OF_CELLS == score:
            game_over = True
            has_lost = False
        else:
            apple_position = generate_apple_position(snake_list)

    else:
        snake_list.pop(0)

    return position_head


def isGameLost() -> bool:
    return (
        position_head[0] >= WIDTH_GRID
        or position_head[0] < 0
        or position_head[1] >= HEIGHT_GRID
        or position_head[1] < 0
        or [position_head[0], position_head[1]] in old_snake_list
        and not game_over
    )


def drawGridGame() -> None:
    for col in range(0, NUM_OF_COLUMNS):
        for row in range(0, NUM_OF_ROWS):
            drawCellGame(row, col)

    pygame.display.update()


def drawCellGame(row: int, col: int) -> None:
    position_col = col * DIMENTION_OF_A_CELL
    position_row = row * DIMENTION_OF_A_CELL
    if [position_col, position_row] == apple_position:
        drawApple(row, col)
    elif [position_col, position_row] not in snake_list:
        drawEmptyCellGame(row, col)
    else:
        drawSnakeCell(row, col)


def drawApple(row: int, col: int) -> None:
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


def drawEmptyCellGame(row: int, col: int) -> None:
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


def drawSnakeCell(row: int, col: int) -> None:
    new_pos_grd = (row, col)
    old_pos_grid = getOldPosGrid(row, col)
    imgToInsert = getCorrispondingImage(old_pos_grid, new_pos_grd)
    screen.blit(
        imgToInsert,
        (
            MARGIN_LEFT + col * DIMENTION_OF_A_CELL,
            MARGIN_TOP + row * DIMENTION_OF_A_CELL,
        ),
    )


def getCorrispondingImage(old_pos_grid: "Point", new_pos_grid: "Point") -> pygame.image:
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


def getOldPosGrid(row: int, col: int) -> "Point":
    old_pos_grid = None
    position_row = row * DIMENTION_OF_A_CELL
    position_col = col * DIMENTION_OF_A_CELL
    if isSnakeFromTop(row, col, position_row, position_col):
        old_pos_grid = (row - 1, col)
    elif isSnakeFromBottom(row, col, position_row, position_col):
        old_pos_grid = (row + 1, col)
    elif isSnakeFromLeft(row, col, position_row, position_col):
        old_pos_grid = (row, col - 1)
    elif isSnakeFromRight(row, col, position_row, position_col):
        old_pos_grid = (row, col + 1)

    return old_pos_grid


def isSnakeFromTop(row: int, col: int, position_row: int, position_col: int) -> bool:
    return (
        row - 1 >= 0
        and [position_col, position_row - DIMENTION_OF_A_CELL] in snake_list
        and path[row - 1][col] == Direction.DOWN_DIR
    )


def isSnakeFromBottom(row: int, col: int, position_row: int, position_col: int) -> bool:
    return (
        row + 1 < NUM_OF_ROWS
        and [position_col, position_row + DIMENTION_OF_A_CELL] in snake_list
        and path[row + 1][col] == Direction.UP_DIR
    )


def isSnakeFromLeft(row: int, col: int, position_row: int, position_col: int) -> bool:
    return (
        col - 1 >= 0
        and [position_col - DIMENTION_OF_A_CELL, position_row] in snake_list
        and path[row][col - 1] == Direction.RIGHT_DIR
    )


def isSnakeFromRight(row: int, col: int, position_row: int, position_col: int) -> bool:
    return (
        col + 1 < NUM_OF_COLUMNS
        and [position_col + DIMENTION_OF_A_CELL, position_row] in snake_list
        and path[row][col + 1] == Direction.LEFT_DIR
    )


def drawGameOver() -> None:
    pygame.draw.rect(screen, BACKGROUND_COLOR, [0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT])
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


restart()
gameLoop()
