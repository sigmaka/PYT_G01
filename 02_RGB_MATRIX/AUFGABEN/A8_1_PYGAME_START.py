import pygame
from pygame.locals import *
import sys


# Variablen für funktionsübergreifenden Zugriff (globale Variablen)
column = 0
row = 0
mouse_x = 0
mouse_y = 0
mouse_x_clk = -1
mouse_y_clk = -1


def get_event():
    global mouse_x, mouse_y, mouse_x_clk, mouse_y_clk
    stop = False
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            stop = True
        elif event.type == KEYDOWN:  # Event Tastatur
            if event.key == K_LEFT:  # Pfeiltaste links
                print('links')
            elif event.key == K_RIGHT:  # Pfeiltaste rechts
                print('rechts')
        elif event.type == MOUSEMOTION:  # Event Maus-Bewegung
            mouse_x, mouse_y = event.pos
        elif event.type == MOUSEBUTTONDOWN:  # Event Maus-Tasten
            mouse_x_clk, mouse_y_clk = event.pos
            print(mouse_x_clk, mouse_y_clk)
    return stop


def draw(canvas):
    canvas.fill([0, 0, 0])
    for i in range(60, 480, 60):  # Grid einzeichnen
        pygame.draw.line(canvas, [50, 50, 50], (0, i), (480, i), 1)  # horizontale Linien zeichnen
        pygame.draw.line(canvas, [50, 50, 50], (i, 0), (i, 480), 1)  # vertikale Linien zeichnen

    pygame.draw.rect(canvas, [100, 0, 0], (200, 150, 100, 50))
    pygame.draw.circle(canvas, [100, 100, 0], (300, 50), 20, 0)


def text(canvas):
    # global mouse_x, mouse_y, mouse_x_clk, mouse_y_clk

    font = pygame.font.SysFont(name="arial", size=16, bold=1)
    string = font.render("x = {:03d}".format(mouse_x), True, [100, 0, 0])
    canvas.blit(string, (10, 0))
    string = font.render("y = {:03d}".format(mouse_y), True, [100, 0, 0])
    canvas.blit(string, (10, 20))

    # siehe https://pyformat.info/ für die Formatierung von Variablen in Strings


def main():
    global mouse_x, mouse_y, mouse_x_clk, mouse_y_clk
    end = False
    fps = 50  # frames per second
    pygame.init()  # Aufruf Initialisierungsfunktion
    clock = pygame.time.Clock()
    canvas = pygame.display.set_mode((480, 480))  # Initialisierung Window mit 480 x 480 Pixel

    while not end:
        draw(canvas)
        text(canvas)
        end = get_event()  # Aufruf Eventhandler mit Rückgabewerten
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption("A8_1_PYGAME | fps: " + "{:.1f}".format(clock.get_fps()))


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()

'''
Weblinks:
- https://www.pygame.org/news
- https://inventwithpython.com/pygame/
- https://inventwithpython.com/makinggames.pdf
'''