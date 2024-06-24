from abbts_blp.rgb import RgbFpga
import time  # wird benötigt für zeitliche Aspekte
import random


def check_position(matrix, new_position, farbe):
    """
    Funktion überprüft die Gültigkeit der neuen Position betreffend den folgenden Rahmenbedingungen:
    - Physikalische Grenzen (8x8)
    - Farbgebung
    :param new_position: Zeilen- und Spaltennummer der zur überprüfenden neuen Position, [i, j]
    :param farbe: Farbkodierung RGB, [R, G, B]
    :param matrix: aktuell bearbeitete Matrix, wird für Farbgebungs-Überprüfung verwendet
    :return: new_position_ok, Bool
    '"""
    new_position_ok = False

    if 0 <= new_position[0] <= 7:  # physikalische Grenzen Zeilen
        if 0 <= new_position[1] <= 7:  # physikalische Grenzen Spalten
            if matrix.rgb_matrix[new_position[0]][new_position[1]] != farbe:  # bereits besetzte Position
                new_position_ok = True

    return new_position_ok


def listen_operationen(liste_1, liste_2, operation='+'):
    """
    Funktion zur elementweisen Addition und Subtraktion von zwei Listen (Zeilen- oder Spaltenvektoren)
    mit gleicher Dimension.
    INFO: Bei Verwendung von + werden Listen konkateniert.
    :param liste_1: 1. Operand, []
    :param liste_2: 2. Operand, []
    :param operation: '+' oder '-', Standard: '+'
    :return: liste_neu, Ergebnis der Operation, Dimension dieser Liste entspricht derjenigen der Operanden, []
    """
    liste_neu = []
    if len(liste_1) == len(liste_2):
        if operation == '+':
            for k in range(len(liste_1)):
                liste_neu.append(liste_1[k] + liste_2[k])
        elif operation == '-':
            for j in range(len(liste_1)):
                liste_neu.append(liste_1[j] - liste_2[j])
        else:
            print('Operation nicht definiert')
            liste_neu = []
    else:
        print('Dimensionen der Listen stimmen nicht überein')

    return liste_neu


def main(matrix, zeit=0.1, farbe=(0, 10, 0), startpunkt=(5, 3), startrichtung=(0, 0, 1, 0)):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param zeit: Zeitvorgabe Durchlauf (je höher, desto langsamer), Standard = 0.1s
    :param farbe: Farbton, Standard = [1, 0, 0]
    :param startpunkt: Startpunkt der Linie, Standard = [2, 3] (Zeile und Spalte)
    :param startrichtung: Startrichtung der Linie, Standard = [0, 0, 1, 0] [Nord, Ost, Süd, West]
    """
    # Startwert und Startrichtung setzen
    zeilennummer = startpunkt[0]
    spaltennummer = startpunkt[1]
    richtung = startrichtung  # [Nord, Ost, Süd, West]

    # Liste richtungsschritt wird basierend auf richtung definiert und zur Addition/Subtraktion
    # mit den Positionen verwendet
    richtungsschritt = [1, 0]  # Richtungsvektor
    kurve_rechts = False
    weiterfahren = True  # Variable für die Freigabe der Weiterfahrt
    anzahl_checks = 0  # Zähler für die Anzahl Aufrufe der Überprüfungsfunktion
    # Startpunkt auf RGB-Matrix schreiben
    matrix.rgb_matrix[zeilennummer][spaltennummer] = farbe
    matrix.write()
    time.sleep(zeit)

    aktuelle_position = [zeilennummer, spaltennummer]
    neue_moegliche_position = aktuelle_position

    while weiterfahren:
        # aufgrund Richtung, entsprechender Richtungsvektor bestimmen
        if richtung[0]:
            richtungsschritt = [-1, 0]
        elif richtung[1]:
            richtungsschritt = [0, 1]
        elif richtung[2]:
            richtungsschritt = [1, 0]
        elif richtung[3]:
            richtungsschritt = [0, -1]
        # neue mögliche Position, aufgrund aktueller Richtung, berechnen
        neue_moegliche_position = listen_operationen(aktuelle_position, richtungsschritt)
        # Gültigkeit dieser neuen möglichen Position prüfen
        neue_position_ok = check_position(matrix, neue_moegliche_position, farbe)

        if neue_position_ok:
            anzahl_checks = 0
            matrix.rgb_matrix[neue_moegliche_position[0]][neue_moegliche_position[1]] = farbe
            matrix.write()
            time.sleep(zeit)
            aktuelle_position = neue_moegliche_position

        else:
            anzahl_checks += 1
            # neue mögliche Position wieder rückgängig machen, da Richtungsschritt zu einer ungültigen Position führte
            neue_moegliche_position = listen_operationen(aktuelle_position, richtungsschritt, operation='-')
            # Richtungsvektor gemäss Kurvenvorgabe drehen
            richtung_neu = [0, 0, 0, 0]
            for i in range(len(richtung)):
                if kurve_rechts:
                    richtung_neu[(i + 1) % 4] = richtung[i]  # Shift right
                else:
                    richtung_neu[i] = richtung[(i + 1) % 4]  # Shift left
            richtung = richtung_neu
        # nach dreimaligem, an gleicher Ursprungsposition, durchgeführtem, erfolglosen Überprüfen der neuen möglichen
        # Position wird Weiterfahrt abgebrochen, da Weiterfahrt unmöglich ist.
        if anzahl_checks > 2:  # >2, aufgrund möglichem Spezialfall: Start [7,7], richtung [0,1,0,0], kurve_rechts=True
            weiterfahren = False


if __name__ == '__main__':

    rgb = RgbFpga(port='COM15')
    rgb.open()
    rgb.write()
    time.sleep(2)
    main(matrix=rgb, startpunkt=(random.randint(0,7), random.randint(0,7)))
    rgb.close()
