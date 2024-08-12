from abbts_blp.rgb import RgbFpga
import sys


def rgb_file_read(file_name=''):
    """
    Funktion für das Einlesen von Textdateien
    :param file_name: Dateiname (Pfad) der Textdatei
    :return line: Inhalt der Textdatei (zeilenweise)
    """
    # https://www.w3schools.com/python/python_try_except.asp
    try:
        with open(file=file_name, mode='r') as fobj:
            line = fobj.readlines()
    except Exception as e:
        print('Datei existiert nicht!', e)
        sys.exit()
    return line


def rgb_value_string_to_number(val_str):
    """
    Funktion für das Umwandeln von Strings in Ganzzahlen
    :param val_str: Zeichenkette (String) zur Umwandlung
    :return value: Ganzzahl
    """
    if val_str.isdigit():
        # Dezimalzahl vorgegeben
        try:
            value = int(val_str, 10)  # value ist in 10er-System
        except ValueError:
            value = 0  # im Fehlerfall value = 0 setzen
    else:
        value = 0
        print('Definition unbekannt: Wert = 0 gesetzt!')

    return value


def rgb_farbe(farben):
    """
    Funktion zur Auslesung der Farbdefinition
    2 mögliche Definitionen: [0, 1, 0] oder <r=0, g=1, b=0>
    :param farben: Zeichenkette (String) zur Umwandlung
    :return rgb_value: korrekte Farbdefinition
    """
    rgb_value = [0, 0, 0]
    eintraege = farben[1:-1].split(',')  # String in Einzelstrings mit Trennzeichen auftrennen
    if eintraege[0].isdigit():  # Variante []
        rgb_value[0] = rgb_value_string_to_number(eintraege[0])
        rgb_value[1] = rgb_value_string_to_number(eintraege[1])
        rgb_value[2] = rgb_value_string_to_number(eintraege[2])
    elif '=' in eintraege[0]:  # Variante <>
        for eintrag in eintraege:
            gleich_r = eintrag.find('r=')  # falls Teilstring nicht enthalten ist, wird -1 zurückgegeben
            gleich_g = eintrag.find('g=')
            gleich_b = eintrag.find('b=')
            if gleich_r != (-1):
                rgb_value[0] = rgb_value_string_to_number(eintrag[(gleich_r + 2):])
            if gleich_g != (-1):
                rgb_value[1] = rgb_value_string_to_number(eintrag[(gleich_g + 2):])
            if gleich_b != (-1):
                rgb_value[2] = rgb_value_string_to_number(eintrag[(gleich_b + 2):])
    else:
        print('Definition unbekannt')
    return rgb_value


def parser_rgb_file(matrix, filename):
    """
    Hauptfunktion zur Bearbeitung der Textdatei (zeilenweise).
    :param matrix: Matrix-Objekt der Klasse RGB_FPGA
    :param filename: Dateiname (Pfad) der Textdatei als String
    """
    zeilen = rgb_file_read(file_name=filename)
    file_cmd = None
    for line in zeilen:
        line = line.strip()  # entferne unerwünschte Steuer- und Leerzeichen am Anfang und Ende der Zeile
        line = line.replace(' ', '')  # entferne Leerzeichen
        line = line.lower()  # Umwandlung in Kleinbuchstaben

        # Auswertung Schlüsselwörter
        if line == '{datei}':
            file_cmd = 'DATEI'
        elif line == '{default}':
            file_cmd = 'DEFAULT'
        elif line == '{matrix}':
            file_cmd = 'MATRIX'

        # Auswertung Schlüsselwort DATEI fehlt noch
        if file_cmd == 'DEFAULT' and (line.find('<') == 0 or line.find('[') == 0):  # Auswertung Schlüsselwort DEFAULT
            rgb_value = rgb_farbe(line)
            for i in range(8):
                for j in range(8):
                    rgb.rgb_matrix[i][j] = rgb_value
            matrix.write()  # Beschreiben der Standardfarbe
        elif file_cmd == 'MATRIX' and line.find('[') == 0:  # Auswertung Schlüsselwort MATRIX
            # Auslesen der Koordinate, ACHTUNG: nur 0-8 möglich
            zeile = int(line[1:2])
            spalte = int(line[4:5])
            index_gleich = line.find('=')
            rgb_value = rgb_farbe(line[index_gleich + 1:])  # alles nach Gleichheitszeichen auslesen
            matrix.rgb_matrix[zeile][spalte] = rgb_value  # Punktuell die Ausnahmefälle in rgb_matrix schreiben
    matrix.write()


if __name__ == '__main__':
    rgb = RgbFpga(port='COM5')
    textdatei = '../DATA/rgb_data.txt'
    rgb.open()
    parser_rgb_file(matrix=rgb, filename=textdatei)
    rgb.close()
