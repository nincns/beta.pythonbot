def add_entry(): 
    print("Eintrag wird hinzugefügt")

def search_entry(): 
    print("Eintrag wird gesucht")

def remove_entry(): 
    print("Eintrag wird gelöscht")

def quit(): 
    print("Beende das Programm")

def load(): 
    print("Datensatz wird geladen")

def save(): 
    print("Datensatz wird gespeichert")

def handle_menu(menu):
    while True:
        for index, item in enumerate(menu, 1):
            print("{}  {}".format(index, item[0]))
        choice = int(input("Ihre Wahl? ")) - 1
        if 0 <= choice < len(menu):
            menu[choice][1]()
        else:
            print("Bitte nur Zahlen im Bereich 1 - {} eingeben".format(
                                                                    len(menu)))

menu = [
    ["Eintrag hinzufügen", add_entry],
    ["Eintrag löschen", remove_entry],
    ["Eintrag suchen", search_entry],
    ["Telefonbuch laden", load],
    ["Telefonbuch speichern", save],
    ["Beenden", quit]
]

handle_menu(menu)