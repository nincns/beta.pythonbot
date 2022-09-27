#from bot_scanning import MoveServoX, CamScan

import sys


def menu():
    while True:
        print(
            "Selbstcheck",
            "Geände vermessen"
            "Umgebung erkunden",
            "Geräusche erkennen",
            "Beenden",
            sep="\n"
        )
        choice = int(input("Ihre Wahl? "))
        if choice == 1:
            print("Selbstcheck ok")
        elif choice == 2:
            print("starte Vermessung")
        elif choice == 3:
            print("Starte Erkundung")
        elif choice == 4:
            print("höre auf Geräusche")
        elif choice ==5:
            sys.exit(0)
        else:
            print("Bitte nur Zahlen zwischen 1 und 5 eingeben!")