from abbts_blp.rgb import RgbFpga
import time  # wird benötigt für zeitliche Aspekte


def create_matrix(matrix, zeit=0.5, anzahl_durchlaeufe=2, laenge_snake=4, farbe_snake=(5, 5, 5), farbe_spur=(0, 0, 0)):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse RgbFpga
    :param zeit: Zeitvorgabe Durchlauf (je höher, desto langsamer), Standard = 0.5s
    :param anzahl_durchlaeufe: Vorgabe Anzahl Gesamt-Durchläufe, Standard = 2
    :param laenge_snake: Vorgabe Anzahl RGB's für Schlange, Standard = 4 (<= 64)
    :param farbe_snake: Farbton Schlange, Standard = (5, 5, 5)
    :param farbe_spur: Farbton Schlangenspur, Standard = (0, 0, 0)
    Konzept:
    Zwei Schlangen die einander hinterher kriechen. Start der zweiten Schlange ist um die Länge der ersten Schlange
    verzögert.
    """
    anzahl_rgb_total = 64  # Anzahl RGB pro Matrix

    for n in range(anzahl_durchlaeufe):

        for i in range(0, anzahl_rgb_total, 1):  # komplette Anzahl RBG's durchlaufen -> RBG leuchten
            m = i % anzahl_rgb_total
            zeilennummer = m // 8  # Ganzzahlquotient
            spaltennummer = m % 8  # Rest
            if zeilennummer % 2 == 0:
                matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe_snake  # v.l.n.r.
            else:
                matrix.rgb_matrix[zeilennummer][-(spaltennummer + 1)] = farbe_snake  # v.r.n.l.

            matrix.write()

            # Start des Ausschaltens um Länge der Schlange verzögern
            if m - laenge_snake < 0:
                time.sleep(zeit)
            # Schlaufe 2: hinterstes RGB umschalten
            # Prinzip: Nachlaufende Schlange der Länge 1
            if m - laenge_snake >= 0:
                j = m - laenge_snake
                zeilennummer = j // 8
                spaltennummer = j % 8
                if zeilennummer % 2 == 0:
                    matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe_spur
                else:
                    matrix.rgb_matrix[zeilennummer][-(spaltennummer + 1)] = farbe_spur

                matrix.write()
                time.sleep(zeit)

        # Auslaufen der Schlange am Ende der RGB
        for k in range(anzahl_rgb_total - laenge_snake, anzahl_rgb_total, 1):
            zeilennummer = k // 8
            spaltennummer = k % 8
            if zeilennummer % 2 == 0:

                matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe_spur
            else:
                matrix.rgb_matrix[zeilennummer][-(spaltennummer + 1)] = farbe_spur

            matrix.write()
            time.sleep(zeit)


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    rgb.open()
    create_matrix(matrix=rgb, zeit=0.1, farbe_spur=(1, 0, 0))
    rgb.close()
