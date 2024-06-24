from abbts_blp.rgb import RgbFpga


rgb = RgbFpga(port='COM15')

for i in range(8):  # Zeile
    for j in range(8):  # Spalte
        if (i + j) % 2 == 0:
            rgb.rgb_matrix[i][j] = [1, 1, 1]

rgb.open()
rgb.write()
rgb.close()
