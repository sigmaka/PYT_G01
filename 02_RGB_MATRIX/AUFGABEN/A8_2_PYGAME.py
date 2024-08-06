import sys
import os
import pygame
from pygame.locals import *
from abbts_blp.rgb import RgbFpga

RED = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE = [0, 0, 100]
WHITE = [100, 100, 100]
GREY = [50, 50, 50]
BLACK = [0, 0, 0]


def get_event(mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color):
    """
    Eventhandler
    """
    stop = False
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # Fenster schliessen/Taste ESCAPE
            stop = True
        elif event.type == MOUSEMOTION:  # Mausbewegung
            mouse_x, mouse_y = event.pos
        elif event.type == MOUSEBUTTONDOWN:  # Tastendruck Maus
            mouse_x_clk, mouse_y_clk = event.pos
        elif event.type == KEYDOWN:
            if event.key == K_r:
                rgb_color = RED
            elif event.key == K_g:
                rgb_color = GREEN
            elif event.key == K_b:
                rgb_color = BLUE
    return mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color, stop


def calc_zeile_spalte(x, y):
    """
    Berechnet aus Mauskoordinaten die entsprechende Zeile und Spalte, damit Kreis auf Raster passt.
    """
    zeile = int(y / 60)
    if zeile < 0:
        zeile = 0
    if zeile > 7:
        zeile = 7

    spalte = int(x / 60)
    if spalte < 0:
        spalte = 0
    if spalte > 7:
        spalte = 7
    return [zeile, spalte]


def draw(canvas, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color):
    """
    Zeichnen des GUI's
    """
    canvas.fill(BLACK)
    for i in range(60, 480, 60):
        pygame.draw.line(canvas, GREY, (0, i), (480, i), 1)
        pygame.draw.line(canvas, GREY, (i, 0), (i, 480), 1)

    farbe = GREEN
    if rgb_color == RED:
        farbe = RED
    elif rgb_color == GREEN:
        farbe = GREEN
    elif rgb_color == BLUE:
        farbe = BLUE
    zeile, spalte = calc_zeile_spalte(mouse_x, mouse_y)
    pygame.draw.circle(canvas, farbe, ((spalte * 60) + 30, (zeile * 60) + 30), 25, 0)
    if (mouse_x_clk != -1) and (mouse_y_clk != -1):
        zeile, spalte = calc_zeile_spalte(mouse_x_clk, mouse_y_clk)
        pygame.draw.circle(canvas, WHITE, ((spalte * 60) + 30, (zeile * 60) + 30), 25, 0)


def text(canvas, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk):
    """
    Text dem GUI hinzufügen
    """
    font = pygame.font.SysFont(name="arial", size=16, bold=1)
    string = font.render("x = {:d}".format(mouse_x), True, RED)
    canvas.blit(string, (10, 0))
    string = font.render("y = {:d}".format(mouse_y), True, RED)
    canvas.blit(string, (10, 20))
    string = font.render("x_clk = {:d}".format(mouse_x_clk), True, RED)
    canvas.blit(string, (10, 40))
    string = font.render("y_clk = {:d}".format(mouse_y_clk), True, RED)
    canvas.blit(string, (10, 60))


def main(matrix, startpunkt=(0, 0), window_position=(1, 30)):
    """
    Hauptfunktion
    """
    x = window_position[0]
    y = window_position[1]
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    mouse_x = startpunkt[0]
    mouse_y = startpunkt[1]
    mouse_x_clk = mouse_x
    mouse_y_clk = mouse_y
    rgb_color = GREEN

    end = False
    fps = 50  # frames per second
    pygame.init()
    canvas = pygame.display.set_mode((480, 480))  # Fenstergrösse
    clock = pygame.time.Clock()

    while not end:
        matrix.rgb_matrix = matrix.init_rgb_matrix()  # zurücksetzen der Matrix auf [0, 0, 0]
        [row, column] = calc_zeile_spalte(mouse_x, mouse_y)
        matrix.rgb_matrix[row][column] = rgb_color
        if (mouse_x_clk != -1) and (mouse_y_clk != -1):
            row, column = calc_zeile_spalte(mouse_x_clk, mouse_y_clk)
            matrix.rgb_matrix[row][column] = WHITE
        matrix.write()
        draw(canvas, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color)
        text(canvas, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk)
        mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color, end = get_event(mouse_x, mouse_y, mouse_x_clk,
                                                                               mouse_y_clk, rgb_color)
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption("_FINAL_AUFGABE_8_2.py | fps: " + "{:.1f}".format(clock.get_fps()))

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    rgb.open()
    main(matrix=rgb, startpunkt=[5, 5])
    rgb.close()
