from abbts_blp.rgb import RgbFpga


def create_matrix(matrix):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    """
    for i in range(0, 8, 1):
        matrix.rgb_matrix[i][0] = [1, 0, 0]  # 1. Spalte füllen
        matrix.rgb_matrix[0][i] = [1, 0, 0]  # 1. Zeile füllen
        matrix.rgb_matrix[i][-1] = [1, 0, 0]  # letzte Spalte füllen, Indexierung letzter Eintrag in einer Liste mit -1
        matrix.rgb_matrix[-1][i] = [1, 0, 0]  # letzte Zeile füllen
    for i in range(1, 7, 1):  # Die vier Ecken sollen nicht von dieser Schleife überschrieben werden → Startindex = 1!
        matrix.rgb_matrix[i][i] = [0, 1, 0]  # Hauptdiagonale: links oben nach rechts unten
        matrix.rgb_matrix[i][-1 - i] = [0, 1, 0]  # Diagonale von rechts oben nach links unten
. .

if __name__ == '__main__':

    rgb = RgbFpga(port='COM15')
    rgb.open()
    create_matrix(matrix=rgb)
    rgb.write()
    rgb.close()
