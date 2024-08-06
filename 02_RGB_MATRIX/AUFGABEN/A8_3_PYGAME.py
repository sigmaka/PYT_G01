import sys
import os
import pygame
from pygame.locals import *
from abbts_blp.rgb import RgbFpga
import cv2 as cv2

RED = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE = [0, 0, 100]
WHITE = [100, 100, 100]
GREY = [50, 50, 50]
BLACK = [0, 0, 0]


def get_event(offset):
    """
    Eventhandler
    """
    # global offset
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            print("exit")
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                offset += 1
                if offset > 24:
                    offset = 24
            elif event.key == K_UP:
                offset -= 1
                if offset < 0:
                    offset = 0
    return offset


def read_image(filename=''):
    """
    Einlesen der Grafikdatei
    """
    im = cv2.imread(filename)
    height, width = im.shape[0:2]
    print(width, height)
    image_matrix = []
    for i in range(0, height, 1):
        led = []
        for j in range(0, width, 1):
            farbe = []
            for k in range(0, 3, 1):
                farbe.extend([0])
            led.extend([rgb])
        image_matrix.extend([led])
    for i in range(0, height, 1):
        for j in range(0, width, 1):
            b, g, r = im[i][j]  # BGR-Farbraum!
            image_matrix[i][j] = [r, g, b]
    print(len(image_matrix))
    return image_matrix


def draw(canvas, image_matrix, offset):
    """
    Zeichnen des GUI's
    """
    canvas.fill(BLACK)
    for i in range(30, 240, 30):
        pygame.draw.line(canvas, GREY, (i, 0), (i, 960), 1)
    for i in range(30, 960, 30):
        pygame.draw.line(canvas, GREY, (0, i), (960, i), 1)
    for i in range(0, 32, 1):
        for j in range(0, 8, 1):
            pygame.draw.circle(canvas, image_matrix[i][j], ((j * 30) + 15, (i * 30) + 15), 12, 0)
    pygame.draw.rect(canvas, WHITE, (0, offset * 30, 240, 240), 2)


def main(matrix, filename='', offset=0, max_leuchtkraft=5, window_position=(1, 30)):
    """
    Hauptfunktion
    """
    x = window_position[0]
    y = window_position[1]
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    end = False
    fps = 50  # frames per second
    pygame.init()
    canvas = pygame.display.set_mode((480, 480))  # Fenstergrösse
    clock = pygame.time.Clock()
    image_matrix = read_image(filename=filename)

    while not end:
        for i in range(0, 8, 1):
            for j in range(offset, (offset + 8), 1):
                r, g, b = image_matrix[j][i]
                # Dämpfung der Leuchtstärke
                if r > max_leuchtkraft:
                    r = max_leuchtkraft
                if g > max_leuchtkraft:
                    g = max_leuchtkraft
                if b > 2 * max_leuchtkraft:
                    b = 2 * max_leuchtkraft
                matrix.rgb_matrix[j - offset][i] = [r, g, b]
        matrix.write()
        draw(canvas, image_matrix, offset)
        offset = get_event(offset)
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption("_FINAL_AUFGABE_8_3.py | fps: " + "{:.1f}".format(clock.get_fps()))


if __name__ == '__main__':
    rgb = RgbFpga(port='COM4')
    grafikdatei = '../IMG/aufgabe_6_2.png'
    rgb.open()
    main(matrix=rgb, filename=grafikdatei)
    rgb.close()
