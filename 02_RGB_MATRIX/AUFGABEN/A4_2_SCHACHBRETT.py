from abbts_blp.rgb import RgbFpga


def create_matrix(matrix):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse RgbFpga
    """
    for i in range(8):  # Zeilenindex
        for j in range(8):  # Spaltenindex
            if (i + j) % 2 == 0:  # Summe von Zeilen- und Spaltenindex gerade?
                matrix.rgb_matrix[i][j] = [5, 5, 5]


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    rgb.open()
    create_matrix(matrix=rgb)
    rgb.write()
    rgb.close()
