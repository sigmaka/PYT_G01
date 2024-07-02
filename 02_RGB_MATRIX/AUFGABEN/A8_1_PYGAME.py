import sys
import pygame
from pygame.locals import *
from abbts_blp.rgb import RgbFpga

RED = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE = [0, 0, 100]
GREY = [50, 50, 50]

FPS = 30


def get_event(row, column, color):
    stop = False
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            stop = True
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                column -= 1
                if column < 0:
                    column = 0
            elif event.key == K_RIGHT:
                column += 1
                if column > 7:
                    column = 7
            elif event.key == K_DOWN:
                row += 1
                if row > 7:
                    row = 7
            elif event.key == K_UP:
                row -= 1
                if row < 0:
                    row = 0
            elif event.key == K_r:  # Taste R
                color = RED
            elif event.key == K_g:  # Taste G
                color = GREEN
            elif event.key == K_b:  # Taste B
                color = BLUE
    return row, column, color, stop


def draw(canvas, row, column, color):
    canvas.fill((0, 0, 0))
    for i in range(60, 480, 60):
        pygame.draw.line(canvas, GREY, (0, i), (480, i), 1)
        pygame.draw.line(canvas, GREY, (i, 0), (i, 480), 1)
    pygame.draw.circle(canvas, color, ((column * 60) + 30, (row * 60) + 30), 25, 0)


def main(matrix, startpunkt=(0, 0)):
    row = startpunkt[0]
    column = startpunkt[1]
    color = GREEN

    end = False
    pygame.init()
    canvas = pygame.display.set_mode((480, 480))  # Fenstergrösse
    clock = pygame.time.Clock()

    while not end:
        matrix.rgb_matrix = matrix.init_rgb_matrix()  # resetting der Matrix auf [0, 0, 0]
        matrix.rgb_matrix[row][column] = color
        draw(canvas, row, column, color)
        row, column, color, end = get_event(row, column, color)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    main(matrix=rgb, startpunkt=[5, 5])
