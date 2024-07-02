from abbts_blp.rgb import RgbFpga


def create_matrix(matrix):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse RgbFpga
    """
    for i in range(0, 8, 1):  # Zeilenindex
        if i % 2 == 0:  # nur gerade Zeilen berücksichtigen mittels Modulo-Operator
            for j in range(0, 8, 1):  # jede Spalte berücksichtigen
                matrix.rgb_matrix[i][j] = [0, 5, 0]


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    rgb.open()
    create_matrix(matrix=rgb)
    rgb.write()
    rgb.close()
