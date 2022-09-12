

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
BACKGROUND_GRID_COLOR =(50, 168, 164)
BACKGROUND_COLOR = (26, 26, 0)

class Direction:
    UP_DIR, RIGHT_DIR, DOWN_DIR, LEFT_DIR = 1, 2, 3, 4

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
    global position, score, snake_list, game_over, game_started, apple_position, has_lost, path
    
    position = [NUM_OF_COLUMNS//2*DIMENTION_OF_A_CELL,
                NUM_OF_ROWS//2*DIMENTION_OF_A_CELL]
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
    start_pos[0]//=DIMENTION_OF_A_CELL
    start_pos[1]//=DIMENTION_OF_A_CELL
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
                
                pygame.draw.rect(screen, BACKGROUND_GRID_COLOR, [
                     MARGIN_LEFT + col*DIMENTION_OF_A_CELL, MARGIN_TOP + row*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL])
                pygame.draw.rect(screen, BORDER_GRID_COLOR, [
                    MARGIN_LEFT + col*DIMENTION_OF_A_CELL, MARGIN_TOP + row*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL], 2)
                if (grid[row][col] != 0):                    
                    match grid[row][col]:                        
                        case Direction.UP_DIR:
                            imgToInset = HAM_IMG_UP.copy()
                        case Direction.RIGHT_DIR:                            
                            imgToInset = HAM_IMG_RIGHT.copy()
                        case Direction.DOWN_DIR:
                            imgToInset = HAM_IMG_DOWN.copy()
                        case Direction.LEFT_DIR:
                            imgToInset = HAM_IMG_LEFT.copy()
                        
                    
                    screen.blit(imgToInset, (MARGIN_LEFT+col*DIMENTION_OF_A_CELL,  MARGIN_TOP+ row*DIMENTION_OF_A_CELL))
                
        pygame.display.update()
        
        pos, cont, i = stack[-1]  
        if cont == 0:
            if pos == start_pos:
                break
            else:          
                stack.pop()
                grid[pos[0]][pos[1]] = 0
                continue
        
        if min_cont[0]> cont:
            min_cont[0] = cont
        
        grid[pos[0]][pos[1]] = i
        next_pos = list(pos)
        #1 up, 2 right, 3 down, 4 left
        match i:
            case Direction.UP_DIR:
                if next_pos[0]>0 and (grid[next_pos[0]-1][next_pos[1]] ==0 or (cont == 1 and [next_pos[0]-1, next_pos[1]] == start_pos)):
                    next_pos = [next_pos[0]-1, next_pos[1]]
            case Direction.RIGHT_DIR:
                if next_pos[1]<NUM_OF_COLUMNS-1 and (grid[next_pos[0]][next_pos[1]+1] ==0  or (cont == 1 and [next_pos[0], next_pos[1]+1] == start_pos)):
                    next_pos = [next_pos[0], next_pos[1]+1]
            case Direction.DOWN_DIR:
                if pos[0]<NUM_OF_ROWS-1 and (grid[next_pos[0]+1][next_pos[1]] ==0  or (cont == 1 and [next_pos[0]+1, next_pos[1]] == start_pos)):
                    next_pos = [next_pos[0]+1, next_pos[1]]
            case Direction.LEFT_DIR:
                if pos[1]>0 and (grid[next_pos[0]][next_pos[1]-1] ==0  or (cont == 1 and [next_pos[0], next_pos[1]-1] == start_pos)):
                    next_pos = [next_pos[0], next_pos[1]-1]      
            case _:
                stack.pop()                
                grid[pos[0]][pos[1]] = 0
                continue

        stack.pop()
        stack.append((pos, cont, i+1))
        if next_pos!=pos:
            stack.append((next_pos, cont-1, 1))

    return grid
                




restart()

game_started = True


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    x_Pos, y_Pos = int(position[0]/DIMENTION_OF_A_CELL), int(position[1]/DIMENTION_OF_A_CELL)
    match path[y_Pos][x_Pos]:
        case 1:                    
            directions = [0, -1]
        case 2:                  
            directions = [1, 0]
        case 3:                    
            directions = [0, +1]
        case 4:                  
            directions = [-1, 0]
            

    pygame.draw.rect(screen, BACKGROUND_GRID_COLOR, [MARGIN_LEFT, MARGIN_TOP, WIDTH_GRID, HEIGHT_GRID])
    

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

        if (position[0] >= WIDTH_GRID or position[0] < 0 or position[1] >= HEIGHT_GRID or position[1] < 0 or [position[0], position[1]] in old_snake and not game_over):
            game_over = True
            has_lost = True
    if not game_over:
        for i in range(0, NUM_OF_COLUMNS):
            for k in range(0, NUM_OF_ROWS):
                if ([i*DIMENTION_OF_A_CELL, k*DIMENTION_OF_A_CELL] == apple_position):
                    pygame.draw.rect(screen, APPLE_COLOR, [
                        MARGIN_LEFT + i*DIMENTION_OF_A_CELL, MARGIN_TOP + k*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL])
                elif ([i*DIMENTION_OF_A_CELL, k*DIMENTION_OF_A_CELL] not in snake_list):
                    pygame.draw.rect(screen, BORDER_GRID_COLOR, [
                        MARGIN_LEFT + i*DIMENTION_OF_A_CELL, MARGIN_TOP + k*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL], 1)
                else:
                    pygame.draw.rect(screen, SNAKE_COLOR, [
                        MARGIN_LEFT+i*DIMENTION_OF_A_CELL, MARGIN_TOP+k*DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL, DIMENTION_OF_A_CELL])

        pygame.display.update()

    else:
        pygame.draw.rect(screen, BACKGROUND_COLOR, [0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT])
        if (has_lost):
            mesg = font_style.render("You lost :(", True, APPLE_COLOR)
        else:
            mesg = font_style.render("You won!!", True, TEXT_COLOR_VICTORY)
        
        

        screen.blit(mesg, [DISPLAY_WIDTH/2 - mesg.get_rect().width/2, DISPLAY_HEIGHT/2-mesg.get_rect().height/2])
        pygame.display.flip()
        time.sleep(2)

    if game_over:
        restart()
        game_started = True

    clock.tick(9)
