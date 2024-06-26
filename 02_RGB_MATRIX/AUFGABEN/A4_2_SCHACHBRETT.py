from abbts_blp.rgb import RgbFpga
import time


def create_matrix(matrix):
    """Hier wird die RGB-Matrix manipuliert
    matrix: rgb_matrix"""
    for i in range(8):  # Zelle
        for j in range(8):  # Spalte
            if (i + j) % 2 == 0:
                matrix.rgb_matrix[i][j] = [10, 10, 10]
                matrix.write()
                time.sleep(0.1)


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    rgb.open()
    create_matrix(matrix=rgb)
    rgb.close()
