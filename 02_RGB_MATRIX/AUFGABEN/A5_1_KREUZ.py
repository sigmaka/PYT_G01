from abbts_blp.rgb import RgbFpga
import time


def create_matrix(matrix, zeit=0.5):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse RgbFpga
    :param zeit: Verzögerung für den dynamischen Ablauf, Standardwert = 0.5s
    """
    for i in range(0, 8, 1):
        matrix.rgb_matrix[i][0] = [5, 0, 0]
        matrix.rgb_matrix[0][i] = [5, 0, 0]
        matrix.rgb_matrix[i][7] = [5, 0, 0]
        matrix.rgb_matrix[7][i] = [5, 0, 0]

        # für dynamische Bilder muss innerhalb dieser Funktion auf RGB-Matrix geschrieben werden
        matrix.write()
        time.sleep(zeit)  # warten für schrittweisen Ablauf

    for i in range(1, 7, 1):
        matrix.rgb_matrix[i][i] = [0, 5, 0]
        matrix.rgb_matrix[i][7 - i] = [0, 5, 0]

        # für dynamische Bilder muss innerhalb dieser Funktion auf RGB-Matrix geschrieben werden
        matrix.write()
        time.sleep(zeit)  # warten für schrittweisen Ablauf


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    rgb.open()
    create_matrix(matrix=rgb, zeit=0.25)
    rgb.close()
