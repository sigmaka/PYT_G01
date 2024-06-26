from abbts_blp.rgb import RgbFpga
import cv2 as cv2
import time


def create_matrix(matrix, filename='', max_leuchtkraft=5, zeit=0.1):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    Zusätzlich werden die beiden Module cv2 und numpy benötigt. cv2 für die zusätzlichen Farbräume und numpy für den
    Datentyp array. Dieser wird innerhalb cv2 verwendet.
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param filename: Dateiname (Pfad) der Grafikdatei als String
    :param max_leuchtkraft: Definition der maximalen Leuchtkraft pro Farbe, Standard = 5
    :param zeit: Zeitvorgabe Durchlauf (je höher, desto langsamer), Standard = 0.1s
    """
    im = cv2.imread(filename)
    height, width = im.shape[0:2]  # Bildgrösse auslesen (Höhe x Breite)

    for start in range(0, height - 8 + 1, 1):  # Startpunkt der einzelnen Ausschnitte
        for i in range(start, (start + 8), 1):  # Ausschnitt, zeilenweise durchlaufen
            for j in range(0, width, 1):  # Ausschnitt spaltenweise durchlaufen
                b, g, r = im[i][j]  # BGR-Farbraum!
                # Dämpfung der Leuchtstärke
                if r > max_leuchtkraft:
                    r = max_leuchtkraft
                if g > max_leuchtkraft:
                    g = max_leuchtkraft
                if b > 2 * max_leuchtkraft:  # bewusst höhere Leuchtkraft gesetzt, da weniger hell wirkt
                    b = 2 * max_leuchtkraft
                matrix.rgb_matrix[i - start][j] = [r, g, b]
        matrix.write()
        time.sleep(zeit)


if __name__ == '__main__':
    print('_FINAL_AUFGABE_6_3.py => __main__')
    rgb = RgbFpga(port='COM4')
    grafikdatei = 'png/aufgabe_6_2.png'
    maximale_leuchtkraft = 2
    dauer = 0.5
    rgb.open()
    create_matrix(matrix=rgb, filename=grafikdatei, max_leuchtkraft=maximale_leuchtkraft, zeit=dauer)
    rgb.close()
