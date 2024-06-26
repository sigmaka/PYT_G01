from abbts_blp.rgb import RgbFpga
import numpy as np
import time
import cv2 as cv2
# https://pypi.org/project/opencv-contrib-python/


def create_matrix(matrix, zeit=0.1):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    Zusätzlich werden die beiden Module cv2 und numpy benötigt. cv2 für die zusätzlichen Farbräume und numpy für den
    Datentyp array. Dieser wird innerhalb cv2 verwendet.
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param zeit: Zeitvorgabe Durchlauf (je höher, desto langsamer), Standard = 0.1s
    """
    # Verschiedene Farbräume und entsprechende Transformationen
    # color_RGB = np.uint8([[farbe_1, farbe_2]])
    # color_HSV = cv2.cvtColor(color_RGB, cv2.COLOR_RGB2HSV)
    # color_LAB = cv2.cvtColor(color_RGB, cv2.COLOR_RGB2LAB)
    # color_GRAYSCALE = cv2.cvtColor(color_RGB, cv2.COLOR_RGB2GRAY)

    # LÖSUNG: Diese Aufgabe lässt sich viel einfacher im Farbraum HSV realisieren.
    # Die anschliessende Transformation in den Farbraum RGB kann leicht via cv2 erfolgen
    # Farbdefinitionen HSV mit Skalierung mit Faktor 2 (Floor-Division) -> siehe unten
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html?highlight=hsv
    # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
    # Different softwares use different scales. So if you are comparing OpenCV values with them,
    # you need to normalize these ranges.

    # https://wisotop.de/hsv-und-hsl-farbmodell.php
    v = 20  # Hellwert (value), 0 -> keine Helligkeit, 100 -> volle Helligkeit
    # Farbtöne (hue)
    rot = 0 // 2
    orange = 30 // 2
    gelb = 60 // 2
    gruen = 120 // 2
    cyan = 180 // 2
    blau = 240 // 2
    violett = 270 // 2
    magenta = 300 // 2

    while True:
        # Vorwärts
        for i in range(0, 255, 8):  # i entspricht der Farbsättigung (saturation)
            color_hsv = np.uint8([[[rot, i, v], [orange, i, v], [gelb, i, v], [gruen, i, v],
                                   [cyan, i, v], [blau, i, v], [violett, i, v], [magenta, i, v]]])
            color_rgb = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2RGB)
            for j in range(len(color_rgb[0])):
                for k in range(0, 8, 1):
                    matrix.rgb_matrix[k][j] = color_rgb[0][j]
                matrix.write()
            time.sleep(zeit)

        # Rückwärts
        for i in range(255, 0, -8):
            color_hsv = np.uint8([[[rot, i, v], [orange, i, v], [gelb, i, v], [gruen, i, v],
                                   [cyan, i, v], [blau, i, v], [violett, i, v], [magenta, i, v]]])
            color_rgb = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2RGB)
            for j in range(len(color_rgb[0])):
                for k in range(0, 8, 1):
                    matrix.rgb_matrix[k][j] = color_rgb[0][j]
                matrix.write()
            time.sleep(zeit)


if __name__ == '__main__':
    print('_START_AUFGABE_5_6.py => __main__')
    rgb = RgbFpga(port='COM4')
    rgb.open()
    create_matrix(matrix=rgb)
    rgb.close()
