import sys
import pygame
from pygame.locals import *
from abbts_blp.rgb import RgbFpga
import add_ons.pygame_color as pgc
import os


def eventhandling(mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color):
    """
    Eventhandler
    :param mouse_x: aktuelle Mausposition x
    :param mouse_y: aktuelle Mausposition y
    :param mouse_x_clk: aktuelle Mausposition x beim letzten Links-Click
    :param mouse_y_clk: aktuelle Mausposition x beim letzten Links-Click
    :param rgb_color: aktuelle Farbe
    :return mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color
    """
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            print("exit")
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x_clk, mouse_y_clk = event.pos
        elif event.type == KEYDOWN:
            if event.key == K_r:
                rgb_color = pgc.LED_RED
            elif event.key == K_g:
                rgb_color = pgc.LED_GREEN
            elif event.key == K_b:
                rgb_color = pgc.LED_BLUE
    return mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color


def calc_zeile_spalte(x, y):
    """
    Berechnet aus Mauskoordinaten die entsprechende Zeile und Spalte, damit Kreis auf Raster passt.
    :param x: aktuelle Mausposition x
    :param y: aktuelle Mausposition y
    :return [zeile, spalte]
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


def draw(displaysurf, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color):
    """
    Zeichnen des GUI's
    :param displaysurf: aktuelle Zeichenfläche
    :param mouse_x: aktuelle Mausposition x
    :param mouse_y: aktuelle Mausposition y
    :param mouse_x_clk: aktuelle Mausposition x beim letzten Links-Click
    :param mouse_y_clk: aktuelle Mausposition x beim letzten Links-Click
    :param rgb_color: aktuelle Farbe
    """
    displaysurf.fill(pgc.BGCOLOR)
    for i in range(60, 480, 60):
        pygame.draw.line(displaysurf, pgc.GRAY, (0, i), (480, i), 1)
        pygame.draw.line(displaysurf, pgc.GRAY, (i, 0), (i, 480), 1)

    farbe = pgc.GREEN
    if rgb_color == pgc.LED_RED:
        farbe = pgc.RED
    elif rgb_color == pgc.LED_GREEN:
        farbe = pgc.GREEN
    elif rgb_color == pgc.LED_BLUE:
        farbe = pgc.BLUE
    zeile, spalte = calc_zeile_spalte(mouse_x, mouse_y)
    pygame.draw.circle(displaysurf, farbe, ((spalte * 60) + 30, (zeile * 60) + 30), 25, 0)
    if (mouse_x_clk != -1) and (mouse_y_clk != -1):
        zeile, spalte = calc_zeile_spalte(mouse_x_clk, mouse_y_clk)
        pygame.draw.circle(displaysurf, pgc.WHITE, ((spalte * 60) + 30, (zeile * 60) + 30), 25, 0)


def text(displaysurf, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk):
    """
    Text dem GUI hinzufügen
    :param displaysurf: aktuelle Zeichenfläche
    :param row: aktuelle Zeile
    :param column: aktuelle Spalte
    """
    font = pygame.font.SysFont(name="arial", size=16, bold=1)
    string = font.render("x = {:d}".format(mouse_x), True, pgc.RED)
    displaysurf.blit(string, (10, 0))
    string = font.render("y = {:d}".format(mouse_y), True, pgc.RED)
    displaysurf.blit(string, (10, 20))
    string = font.render("x_clk = {:d}".format(mouse_x_clk), True, pgc.RED)
    displaysurf.blit(string, (10, 40))
    string = font.render("y_clk = {:d}".format(mouse_y_clk), True, pgc.RED)
    displaysurf.blit(string, (10, 60))


def main(matrix, startpunkt=(0, 0), window_position=(1, 30)):
    """
    Hauptfunktion
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param startpunkt: Startpunkt der Linie, Standard = [0, 0] (Zeile und Spalte)
    :param window_position: Position GUI-Window (oben-rechts), Standard = [1, 30] (x und y)
    """
    x = window_position[0]
    y = window_position[1]
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    mouse_x = startpunkt[0]
    mouse_y = startpunkt[1]
    mouse_x_clk = mouse_x
    mouse_y_clk = mouse_y
    rgb_color = pgc.LED_GREEN
    fps = 50  # frames per second
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((480, 480), 0, 32)

    while True:
        matrix.rgb_matrix = matrix.init_rgb_matrix()  # resetieren der Matrix auf [0, 0, 0]
        [row, column] = calc_zeile_spalte(mouse_x, mouse_y)
        matrix.rgb_matrix[row][column] = rgb_color
        if (mouse_x_clk != -1) and (mouse_y_clk != -1):
            row, column = calc_zeile_spalte(mouse_x_clk, mouse_y_clk)
            matrix.rgb_matrix[row][column] = pgc.LED_WHITE
        matrix.write()
        draw(displaysurf, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color)
        text(displaysurf, mouse_x, mouse_y, mouse_x_clk, mouse_y_clk)
        mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color = eventhandling(mouse_x, mouse_y, mouse_x_clk, mouse_y_clk, rgb_color)
        pygame.display.update()
        fpsclock.tick(fps)
        pygame.display.set_caption("_FINAL_AUFGABE_8_2.py | fps: " + "{:.1f}".format(fpsclock.get_fps()))


if __name__ == '__main__':
    print('_FINAL_AUFGABE_8_2.py => __main__')
    rgb = RgbFpga(port='COM4')
    start = [5, 5]
    rgb.open()
    main(matrix=rgb, startpunkt=start)
    rgb.close()
