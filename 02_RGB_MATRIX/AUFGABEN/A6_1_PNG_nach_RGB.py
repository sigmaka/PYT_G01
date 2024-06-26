from abbts_blp.rgb import RgbFpga
import cv2 as cv2


def create_matrix(matrix, filename='', max_leuchtkraft=5):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    Zusätzlich werden die beiden Module cv2 und numpy benötigt. cv2 für die zusätzlichen Farbräume und numpy für den
    Datentyp array. Dieser wird innerhalb cv2 verwendet.
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param filename: Dateiname (Pfad) der Grafikdatei als String
    :param max_leuchtkraft: Definition der maximalen Leuchtkraft pro Farbe, Standard = 5
    """
    im = cv2.imread(filename)  # ACHTUNG: OpenCV benutzt den BGR- anstelle des RGB-Farbraums
    # Ist auf der Webseite (siehe Link unten) in einer Warning-Box im unteren Bereich der Webseite beschrieben.
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html?highlight=imread%20rgb
    height, width = im.shape[0:2]  # Bildgrösse auslesen (Höhe x Breite)

    for i in range(0, height, 1):
        for j in range(0, width, 1):
            b, g, r = im[i][j]  # BGR-Farbraum!
            # Dämpfung der Leuchtstärke
            if r > max_leuchtkraft:
                r = max_leuchtkraft
            if g > max_leuchtkraft:
                g = max_leuchtkraft
            if b > 2 * max_leuchtkraft:  # bewusst höhere Leuchtkraft gesetzt, da weniger hell wirkt
                b = 2 * max_leuchtkraft
            matrix.rgb_matrix[i][j] = [r, g, b]
    matrix.write()


if __name__ == '__main__':
    rgb = RgbFpga(port='COM4')
    grafikdatei = 'png/aufgabe_6_1.png'
    maximale_leuchtkraft = 2
    rgb.open()
    create_matrix(matrix=rgb, filename=grafikdatei, max_leuchtkraft=maximale_leuchtkraft)
    rgb.close()
