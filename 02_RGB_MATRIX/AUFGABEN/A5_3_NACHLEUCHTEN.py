from abbts_blp.rgb import RgbFpga
import time


def create_matrix(matrix, zeit=0.5, horizontal=True, anzahl_rgb_durchlaufen=64,
                  farbe=(0, 10, 0), leuchtabschwaechung=0.1):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse Rgb_Fpga
    :param zeit: Zeitvorgabe Durchlauf (je höher, desto langsamer), Standard = 0.5s
    :param horizontal: Umschaltung horizontaler vs. vertikaler Verlauf, Standard: True (horizontal)
    :param anzahl_rgb_durchlaufen: Vorgabe Anzahl RGB's, Standard = 64 (komplette Matrix)
    :param farbe: Farbton, Standard = [0, 10, 0]
    :param leuchtabschwaechung: Faktor zur Reduktion der nachlaufenden RGB's, Standard = 0.1
    """
    anzahl_rgb_total = 64  # Anzahl RGB pro Matrix
    farbe_reduzierte_leuchtkraft = []
    for wert in farbe:
        farbe_reduzierte_leuchtkraft.append(int(wert * leuchtabschwaechung))

    for i in range(0, anzahl_rgb_durchlaufen, 1):  # komplette Anzahl RBG's durchlaufen -> RBG leuchten
        m = i % anzahl_rgb_total  # Vorbereitung Anzahl Durchläufe = 0 ... anzahl_rgb_komplett-1

        # vorderstes RGB setzen
        # Unterscheidung Orientierung: horizontal vs. vertikal
        if horizontal:
            zeilennummer = m // 8  # int(m / 8)  # Ganzzahlquotient
            spaltennummer = m % 8  # Rest
        else:
            zeilennummer = m % 8
            spaltennummer = m // 8  # int(m / 8)
        matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe

        # nachlaufende RGB's abschwächen
        # Strategie: jeweils RGB des letzten Durchlaufs abschwächen: ACHTUNG beim Spalten- bzw. Zeilenübergang
        if m > 0:
            if zeilennummer == 0 and not horizontal:  # Spaltenübergang im vertikalen Verlauf
                zeilennummer = -1  # letzte Zeile setzen
                spaltennummer -= 1
                matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe_reduzierte_leuchtkraft
            elif spaltennummer == 0 and horizontal:  # Zeilenübergang im horizontalen Verlauf
                zeilennummer -= 1
                spaltennummer = -1  # letzte Spalte setzen
                matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe_reduzierte_leuchtkraft
            else:  # Standardfall, falls weder ein Spalten- noch Zeilenübergang anliegt
                if horizontal:
                    spaltennummer -= 1
                else:
                    zeilennummer -= 1
                matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe_reduzierte_leuchtkraft
        matrix.write()
        time.sleep(zeit)


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    anzahl_RGB = 64  # wie viele RGB sollen durchlaufen werden?
    rgb.open()
    create_matrix(matrix=rgb, anzahl_rgb_durchlaufen=anzahl_RGB, zeit=0.1)
    rgb.close()
