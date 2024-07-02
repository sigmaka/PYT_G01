def read_file(file_name):
    """
    Funktion für das Einlesen von Text-files.
    :param file_name: Dateiname
    """
    with open(file=file_name, mode='r') as fobj:
        lines = fobj.readlines()
    return lines


if __name__ == '__main__':
    dateiname = 'data/rgb_data.txt'
    zeilen = read_file(file_name=dateiname)
    print('Zeilen der Datei: ', zeilen)
    print('Datentyp: ', type(zeilen))
    # Jede einzelne Zeile aus Zeilen-Liste ausgeben
    i = 1
    for zeile in zeilen:
        # print('Zeile {0}: {1}'.format(i, zeile))
        i += 1

    # nützliche String-Methoden
    text = '    {   MATRIX_ 1324}\n'
    print('text (inkl. Zeilenwechsel): ', text)
    # strip entfernt standardmässig Leerzeichen und z.B. Zeilenvorschub \n am Anfang und am Ende
    text_strip = text.strip()
    print('strip: ', text_strip)
    text_replace = text.replace(' ', '')  # z.B. entfernen von allen Leerzeichen
    print('replace: ', text_replace)
    text_lower = text.lower()  # Unwandlung in Kleinbuchstaben
    print('lower: ', text_lower)
    print('find: ', text.find('_'))  # suchen von Zeichen, falls nicht vorhanden -> -1
    print('split: ', text.split())  # trennt String in eine Liste von Einzelstrings auf,
    # Standardtrennzeichen: Leerzeichen, kann aber auch parametriert werden '_'

    # Einige Weblinks
    # https://www.python-kurs.eu/python3_dateien.php
    # https://www.w3schools.com/python/python_file_handling.asp
    # https://docs.python.org/3/library/functions.html#open
    # https://codefather.tech/blog/python-with-open/
    # https://realpython.com/python-with-statement/#using-the-python-with-statement
    # https://www.geeksforgeeks.org/with-statement-in-python/