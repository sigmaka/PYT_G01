from abbts_blp.rgb import RgbFpga
import time  # wird benötigt für zeitliche Aspekte
import random  # wird benötigt für Zufallszahlen


def create_matrix(matrix, zeit=0.5, anzahl_durchlaeufe=4, max_leuchtkraft=10, anzahl_diagonalen=15):
    """
    Funktion für das Erstellen der gewünschten Lichtbilder auf der RGB-Matrix.
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param zeit: Verzögerung für den dynamischen Ablauf, Standard = 0.5 s
    :param anzahl_durchlaeufe: Vorgabe Anzahl Gesamt-Durchläufe, Standard = 4
    :param max_leuchtkraft: Vorgabe der maximalen Leuchtkraft, Standard = 10
    :param anzahl_diagonalen: Vorgabe Anzahl zu durchlaufende Diagonalen pro Durchlauf, Standard = 15

   Konzept:
                 [0,0]  --> Summe Indices = 0
               [1,0][0,1]  --> Summe Indices = 1
             [2,0][1,1][0,2]  --> Summe Indices = 2
           [3,0][2,1][1,2][0,3]  --> Summe Indices = 3
         [4,0][3,1][2,2][1,3][0,4]  --> Summe Indices = 4
       [5,0][4,1][3,2][2,3][1,4][0,5]  --> Summe Indices = 5
     [6,0][5,1][4,2][3,3][2,4][1,5][0,6]  --> Summe Indices = 6
   [7,0][6,1][5,2][4,3][3,4][2,5][1,6][0,7]  --> Summe Indices = 7
     [7,1][6,2][5,3][4,4][3,5][2,6][1,7]  --> Summe Indices = 8
       [7,2][6,3][5,4][3,5][2,6][1,7]  --> Summe Indices = 9
         [7,3][6,4][5,5][4,6][3,7]  --> Summe Indices = 10
           [7,4][6,5][5,6][4,7]  --> Summe Indices = 11
             [7,5][6,4][5,7]  --> Summe Indices = 12
               [7,5][6,7]  --> Summe Indices = 13
                 [7,7]  --> Summe Indices = 14
    """
    # Abfangen unzulässiger Werte
    zeit = check_limits(zeit, 0.01, 10, 0.1)
    anzahl_durchlaeufe = check_limits(anzahl_durchlaeufe, 1, 10, 4)
    max_leuchtkraft = check_limits(max_leuchtkraft, 1, 50, 10)
    anzahl_diagonalen = check_limits(anzahl_diagonalen, 0, 15, 15)

    # Erstellen der Farbliste
    farben = create_farbliste(anzahl_durchlaeufe, max_leuchtkraft)

    for k in range(anzahl_durchlaeufe):
        summe = 0
        for r in range(0, anzahl_diagonalen, 1):  # Hauptschleife für komplette Anzahl Durchläufe der Matrix
            # unterlagerte Schleife, welche jeweils die komplette Matrix durchläuft -> Optimierungspotential!
            for i in range(0, 8, 1):
                for j in range(0, 8, 1):
                    if i + j == summe:  # siehe Konzept: konstante Summe entspricht einer Diagonalen
                        matrix.rgb_matrix[i][j] = farben[k]
            summe += 1  # siehe Konzept: Summe inkrementieren entspricht der nächsten Diagonalen
            matrix.write()
            time.sleep(zeit)


def create_farbliste(anzahl_durchlaeufe, max_leuchtkraft):
    """
    Funktion für das Erstellen einer Farbliste für die unterschiedlichen Durchläufe.
    Durchlauf:1          2           3             4     usw.
              |          |           |             |      |
    [[rot,grün,blau], [0,0,0], [rot,grün,blau], [0,0,0], ...]
    Die Farbwerte [rot,grün,blau] sind jeweils zufallsbasiert, aber keine Mischfarben
    :param anzahl_durchlaeufe: Vorgabe Anzahl Gesamt-Durchläufe
    :param max_leuchtkraft: Vorgabe der maximalen Leuchtkraft
    :return farben: Liste mit Farbwerten pro Durchlauf
    """
    farben = []  # leere Liste für das Befüllen der konkreten Farbwerte, abhängig vom Durchlauf
    # Farbvektor in entsprechender Anzahl Durchläufe erstellen
    for i in range(anzahl_durchlaeufe):
        if i % 2 == 0:  # setzen der entsprechenden Farbgebung
            rgb_farbe = [0, 0, 0]  # Rücksetzen der Farbe
            farbe = random.randint(1, 3) - 1  # Rot, Grün oder Blau -> entspricht Index der Liste RGB, keine Mischfarben
            leuchtkraft = random.randint(1, max_leuchtkraft)  # Leuchtkraft definieren
            rgb_farbe[farbe] = leuchtkraft
        else:
            rgb_farbe = [0, 0, 0]  # jeder 2. Durchgang wird Matrix zurückgesetzt
        farben.append(rgb_farbe)
    return farben


def check_limits(variable, minimum, maximum, standard):
    """
    Funktion für das Begrenzen von Variablen.
    :param variable: Variable, welche begrenzt werden soll
    :param minimum: Vorgabe Minimalwert für diese Variable
    :param maximum: Vorgabe Maximalwert für diese Variable
    :param standard: Definition eines Standardwertes für diese Variable
    :return variable: begrenzter Variablenwert
    """
    if minimum <= variable <= maximum:
        variable = variable
    else:
        variable = standard
    return variable


if __name__ == '__main__':
    rgb = RgbFpga(port='COM15')
    rgb.open()
    create_matrix(matrix=rgb, zeit=0.1)
    rgb.close()
