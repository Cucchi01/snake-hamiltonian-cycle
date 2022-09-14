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
from copy import copy
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

TIME_SLEEP_HAMILTONIAN = 0.05
CLOCK_TICK = 6


class Direction:
    UP_DIR, RIGHT_DIR, DOWN_DIR, LEFT_DIR = 1, 2, 3, 4


# Position is used to define a cell in the grid
class Position:
    def __init__(self, row=0, col=0) -> None:
        self.row = row
        self.col = col

    def isEqual(self, otherPosition) -> bool:
        return self.row == otherPosition.row and self.col == otherPosition.col


# Point is used to define a pixel in the screen
class Point:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def isEqual(self, otherPoint) -> bool:
        return self.x == otherPoint.x and self.y == otherPoint.y


Point2 = namedtuple("Point", "row col")
StackFrameHam = namedtuple("StackFrame", "position n_remaining_cells direction_to_try")


clock = pygame.time.Clock()

# endregion


def gameLoop() -> None:
    global directions, old_snake_list, game_over, has_lost, point_head
    while 1:
        manageEvents()
        directions = getChangeInPosition(point_head)

        pygame.draw.rect(
            screen,
            BACKGROUND_GRID_COLOR,
            [MARGIN_LEFT, MARGIN_TOP, WIDTH_GRID, HEIGHT_GRID],
        )

        old_snake_list = list(snake_list)
        point_head = updateSnake()

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

    global point_head, score, snake_list, game_over, apple_point, has_lost, path

    point_head = Point(
        x=NUM_OF_COLUMNS // 2 * DIMENTION_OF_A_CELL,
        y=NUM_OF_ROWS // 2 * DIMENTION_OF_A_CELL,
    )
    score = 1
    snake_list = [copy(point_head)]
    game_over = False
    has_lost = False
    pygame.draw.rect(screen, BACKGROUND_COLOR, [0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT])
    path = generation_hamiltonian_cycle(snake_list[0])

    gamePause(5)

    apple_point = generate_apple_position(snake_list)

    return


def gamePause(seconds: float) -> None:
    startTime = time.time()
    while time.time() - startTime < seconds:
        manageEvents()


def generate_apple_position(snake: list) -> Point:
    apple_point = Point(
        random.randint(0, NUM_OF_COLUMNS - 1) * DIMENTION_OF_A_CELL,
        random.randint(0, NUM_OF_ROWS - 1) * DIMENTION_OF_A_CELL,
    )

    while isPointInSnake(apple_point, snake):
        apple_point = Point(
            random.randint(0, NUM_OF_COLUMNS - 1) * DIMENTION_OF_A_CELL,
            random.randint(0, NUM_OF_ROWS - 1) * DIMENTION_OF_A_CELL,
        )

    return apple_point


def getChangeInPosition(point_head: Point) -> Direction:
    position_head = getPositionFromPoint(point_head)

    match path[position_head.row][position_head.col]:
        case Direction.UP_DIR:
            directions = [0, -1]
        case Direction.RIGHT_DIR:
            directions = [1, 0]
        case Direction.DOWN_DIR:
            directions = [0, +1]
        case Direction.LEFT_DIR:
            directions = [-1, 0]
    return directions


def generation_hamiltonian_cycle(start_point: Point) -> list:
    start_pos = getPositionFromPoint(start_point)

    grid = emptyMatrix()

    cells_to_fill_remaining = NUMBER_OF_CELLS

    stack = []
    stack.append(StackFrameHam(copy(start_pos), cells_to_fill_remaining, 1))

    while True and stack:
        gamePause(TIME_SLEEP_HAMILTONIAN)

        manageEvents()
        drawGridHamiltonian(start_pos, grid)

        # region manage last position in the path
        pos: Position
        pos, cells_to_fill_remaining, direction_to_try = stack[-1]

        if cells_to_fill_remaining == 0:
            if pos.isEqual(start_pos):
                break
            else:
                # it does not complete the cycle
                removeTheLeaf(stack, grid, pos)
                continue

        grid[pos.row][pos.col] = direction_to_try

        next_pos: Position
        next_pos: Position
        next_pos, end_possible_directions = getNextPosition(
            pos, direction_to_try, grid, cells_to_fill_remaining, start_pos
        )

        if end_possible_directions == True:
            removeTheLeaf(stack, grid, pos)
            continue

        prepareFollowingStepInCurrentCell(
            stack, StackFrameHam(pos, cells_to_fill_remaining, direction_to_try + 1)
        )
        if next_pos.isEqual(pos) == False:
            addLeafToPath(
                stack, StackFrameHam(next_pos, cells_to_fill_remaining - 1, 1)
            )

        # endregion

    return grid


def emptyMatrix(
    n_rows: "int" = NUM_OF_ROWS, n_cols: "int" = NUM_OF_COLUMNS, def_value: "int" = 0
) -> "list":
    grid = []
    for i in range(n_rows):
        grid.append([])
        for _ in range(n_cols):
            grid[i].append(def_value)

    return grid


def removeTheLeaf(stack: list, grid: list, pos: Position) -> None:
    stack.pop()
    grid[pos.row][pos.col] = 0


def prepareFollowingStepInCurrentCell(stack: list, stackFrame: StackFrameHam) -> None:
    stack.pop()
    stack.append(stackFrame)


def addLeafToPath(stack: list, stackFrame: StackFrameHam) -> None:
    stack.append(stackFrame)


def drawGridHamiltonian(start_pos: Position, grid: "list") -> None:
    for row in range(NUM_OF_ROWS):
        for col in range(NUM_OF_COLUMNS):
            drawCellHam(row, col, start_pos, grid)

    pygame.display.update()


def drawCellHam(row: "int", col: "int", start_pos: Position, grid: "list") -> None:
    drawEmptyCellHam(row, col)
    if Position(row=row, col=col).isEqual(start_pos):
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
    pos: Position,
    direction_to_try: Direction,
    grid: list,
    cells_to_fill_remaining: int,
    start_pos: Position,
) -> tuple:
    next_pos = copy(pos)
    end_possible_dir = False

    match direction_to_try:
        case Direction.UP_DIR:
            if isMovementUpPossibleHam(pos, grid, start_pos, cells_to_fill_remaining):
                next_pos.row -= 1
        case Direction.RIGHT_DIR:
            if isMovementRightPossibleHam(
                pos, grid, start_pos, cells_to_fill_remaining
            ):
                next_pos.col += 1
        case Direction.DOWN_DIR:
            if isMovementDownPossibleHam(pos, grid, start_pos, cells_to_fill_remaining):
                next_pos.row += 1
        case Direction.LEFT_DIR:
            if isMovementLeftPossibleHam(pos, grid, start_pos, cells_to_fill_remaining):
                next_pos.col -= 1
        case _:
            end_possible_dir = True

    return next_pos, end_possible_dir


def isMovementUpPossibleHam(
    pos: Position, grid: list, start_pos: Position, cells_to_fill_remaining: int
) -> bool:
    return pos.row > 0 and (
        grid[pos.row - 1][pos.col] == 0
        or (
            cells_to_fill_remaining == 1
            and Position(pos.row - 1, pos.col).isEqual(start_pos)
        )
    )


def isMovementRightPossibleHam(
    pos: Position, grid: list, start_pos: Position, cells_to_fill_remaining: int
) -> bool:
    return pos.col < NUM_OF_COLUMNS - 1 and (
        grid[pos.row][pos.col + 1] == 0
        or (
            cells_to_fill_remaining == 1
            and Position(pos.row, pos.col + 1).isEqual(start_pos)
        )
    )


def isMovementDownPossibleHam(
    pos: Position, grid: list, start_pos: Position, cells_to_fill_remaining: int
) -> bool:
    return pos.row < NUM_OF_ROWS - 1 and (
        grid[pos.row + 1][pos.col] == 0
        or (
            cells_to_fill_remaining == 1
            and Position(pos.row + 1, pos.col).isEqual(start_pos)
        )
    )


def isMovementLeftPossibleHam(
    pos: Position, grid: list, start_pos: Position, cells_to_fill_remaining: int
) -> bool:
    return pos.col > 0 and (
        grid[pos.row][pos.col - 1] == 0
        or (
            cells_to_fill_remaining == 1
            and Position(pos.row, pos.col - 1).isEqual(start_pos)
        )
    )


def updateSnake() -> Point:
    global game_over, has_lost, snake_list, score, apple_point
    point_head.x += DIMENTION_OF_A_CELL * directions[0]
    point_head.y += DIMENTION_OF_A_CELL * directions[1]

    snake_list.append(copy(point_head))

    if point_head.isEqual(apple_point):
        score += 1
        if NUMBER_OF_CELLS == score:
            game_over = True
            has_lost = False
        else:
            apple_point = generate_apple_position(snake_list)

    else:
        snake_list.pop(0)

    return point_head


def isGameLost() -> bool:
    return (
        point_head.x >= WIDTH_GRID
        or point_head.x < 0
        or point_head.y >= HEIGHT_GRID
        or point_head.y < 0
        or point_head in old_snake_list
        and not game_over
    )


def drawGridGame() -> None:
    for col in range(0, NUM_OF_COLUMNS):
        for row in range(0, NUM_OF_ROWS):
            drawCellGame(row, col)

    pygame.display.update()


def drawCellGame(row: int, col: int) -> None:
    position = Position(row, col)
    point = getPointFromPosition(Position(row, col))
    if point.isEqual(apple_point):
        drawApple(row, col)
    elif isPointInSnake(point, snake_list) == False:
        drawEmptyCellGame(row, col)
    else:
        drawSnakeCell(position)


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


def drawSnakeCell(new_pos_grid: Position) -> None:
    old_pos_grid = getOldPosGrid(new_pos_grid)
    imgToInsert = getCorrispondingImage(old_pos_grid, new_pos_grid)
    screen.blit(
        imgToInsert,
        (
            MARGIN_LEFT + new_pos_grid.col * DIMENTION_OF_A_CELL,
            MARGIN_TOP + new_pos_grid.row * DIMENTION_OF_A_CELL,
        ),
    )


def getCorrispondingImage(
    old_pos_grid: Position, new_pos_grid: Position
) -> pygame.image:
    if old_pos_grid == None:
        match path[new_pos_grid.row][new_pos_grid.col]:
            case Direction.UP_DIR:
                imgToInset = SNAKE_TOP_BOTTOM.copy()
            case Direction.RIGHT_DIR:
                imgToInset = SNAKE_LEFT_RIGHT.copy()
            case Direction.DOWN_DIR:
                imgToInset = SNAKE_TOP_BOTTOM.copy()
            case Direction.LEFT_DIR:
                imgToInset = SNAKE_LEFT_RIGHT.copy()
    else:
        entering_left = new_pos_grid.col - old_pos_grid.col == 1
        entering_right = new_pos_grid.col - old_pos_grid.col == -1
        entering_top = new_pos_grid.row - old_pos_grid.row == 1
        entering_bottom = new_pos_grid.row - old_pos_grid.row == -1

        leaving_top = False
        leaving_right = False
        leaving_bottom = False
        leaving_left = False

        match path[new_pos_grid.row][new_pos_grid.col]:
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


def getOldPosGrid(new_pos: Position) -> Position:
    old_pos_grid = None
    row = new_pos.row
    col = new_pos.col
    point = Point(x=col * DIMENTION_OF_A_CELL, y=row * DIMENTION_OF_A_CELL)
    if isSnakeFromTop(row, col, point):
        old_pos_grid = Position(row - 1, col)
    elif isSnakeFromBottom(row, col, point):
        old_pos_grid = Position(row + 1, col)
    elif isSnakeFromLeft(row, col, point):
        old_pos_grid = Position(row, col - 1)
    elif isSnakeFromRight(row, col, point):
        old_pos_grid = Position(row, col + 1)

    return old_pos_grid


def isSnakeFromTop(row: int, col: int, point: Point) -> bool:
    return (
        row - 1 >= 0
        and isPointInSnake(Point(point.x, point.y - DIMENTION_OF_A_CELL), snake_list)
        and path[row - 1][col] == Direction.DOWN_DIR
    )


def isSnakeFromBottom(row: int, col: int, point: Point) -> bool:
    return (
        row + 1 < NUM_OF_ROWS
        and isPointInSnake(Point(point.x, point.y + DIMENTION_OF_A_CELL), snake_list)
        and path[row + 1][col] == Direction.UP_DIR
    )


def isSnakeFromLeft(row: int, col: int, point: Point) -> bool:
    return (
        col - 1 >= 0
        and isPointInSnake(Point(point.x - DIMENTION_OF_A_CELL, point.y), snake_list)
        and path[row][col - 1] == Direction.RIGHT_DIR
    )


def isSnakeFromRight(row: int, col: int, point: Point) -> bool:
    return (
        col + 1 < NUM_OF_COLUMNS
        and isPointInSnake(Point(point.x + DIMENTION_OF_A_CELL, point.y), snake_list)
        and path[row][col + 1] == Direction.LEFT_DIR
    )


def isPointInSnake(pos: Position, snake: list) -> bool:
    for el in snake:
        if pos.isEqual(el):
            return True

    return False


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


def getPointFromPosition(position: Position) -> Point:
    return Point(
        x=position.col * DIMENTION_OF_A_CELL, y=position.row * DIMENTION_OF_A_CELL
    )


def getPositionFromPoint(point: Point) -> Position:
    return Position(
        row=int(point.y // DIMENTION_OF_A_CELL), col=int(point.x // DIMENTION_OF_A_CELL)
    )


restart()
gameLoop()
