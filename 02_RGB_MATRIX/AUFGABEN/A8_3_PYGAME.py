import sys
import pygame
from pygame.locals import *
from abbts_blp.rgb import RgbFpga
import add_ons.pygame_color as pgc
import os
import cv2 as cv2


def eventhandling(offset):
    """
    Eventhandler
    :param offset: aktueller Zeilenoffset für die Darstellung von Bildern mit mehr als 8 Zeilen
    :return offset
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
    :param filename: Dateiname (Pfad) der Grafikdatei als String
    :return image_matrix
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


def draw(displaysurf, image_matrix, offset):
    """
    Zeichnen des GUI's
    :param displaysurf: aktuelle Zeichenfläche
    :param image_matrix: aktueller Ausschnitt der Grafik zur Darstellung auf der RGB-Matrix
    :param offset: aktueller Zeilenoffset für die Darstellung von Bildern mit mehr als 8 Zeilen
    """
    displaysurf.fill(pgc.BGCOLOR)
    for i in range(30, 240, 30):
        pygame.draw.line(displaysurf, pgc.GRAY, (i, 0), (i, 960), 1)
    for i in range(30, 960, 30):
        pygame.draw.line(displaysurf, pgc.GRAY, (0, i), (960, i), 1)
    for i in range(0, 32, 1):
        for j in range(0, 8, 1):
            pygame.draw.circle(displaysurf, image_matrix[i][j], ((j * 30) + 15, (i * 30) + 15), 12, 0)
    pygame.draw.rect(displaysurf, pgc.WHITE, (0, offset * 30, 240, 240), 2)


def main(matrix, filename='', offset=0, max_leuchtkraft=5, window_position=(1, 30)):
    """
    Hauptfunktion
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param filename: Dateiname (Pfad) der Grafikdatei als String
    :param offset: Zeilenoffset für die Darstellung von Bildern mit mehr als 8 Zeilen, Standard = 0
    :param max_leuchtkraft: Definition der maximalen Leuchtkraft pro Farbe, Standard = 5
    :param window_position: Position GUI-Window (oben-rechts), Standard = [1, 30] (x und y)
    """
    x = window_position[0]
    y = window_position[1]
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    fps = 50  # frames per second
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((240, 960), 0, 32)
    image_matrix = read_image(filename=filename)
    while True:
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
        draw(displaysurf, image_matrix, offset)
        offset = eventhandling(offset)
        pygame.display.update()
        fpsclock.tick(fps)
        pygame.display.set_caption("_FINAL_AUFGABE_8_3.py | fps: " + "{:.1f}".format(fpsclock.get_fps()))


if __name__ == '__main__':
    print('_FINAL_AUFGABE_8_3.py => __main__')
    rgb = RgbFpga(port='COM4')
    grafikdatei = 'png/aufgabe_6_2.png'
    rgb.open()
    main(matrix=rgb, filename=grafikdatei)
    rgb.close()
