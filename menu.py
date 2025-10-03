# funktionen zur auswahl welches modol laufen soll
## zB ausmalbuch, klammerrechnung, minus_vor_der_klammer

import os
import platform
import subprocess
import time
import sys
import ausmalbuch_einfach as ausmalbuch
import subfuc.klammerrechnung as klammerrechnung
import subfuc.minus_vor_der_klammer as minus_vor_der_klammer


def run():
    while True:
        print("_______________________________")
        print("Hauptmenü - Wähle ein Modul:")
        print("1. Ausmalbuch")
        print("2. Minus vor der Klammer")
        print("3. Klammerrechnung")
        print("4. Beenden")
        auswahl = input("Gib die Zahl deiner Wahl ein: ")

        if auswahl == '1':
            ausmalbuch.run()
        elif auswahl == '2':
            minus_vor_der_klammer.run()
        elif auswahl == '3':
            klammerrechnung.run()
        elif auswahl == '4':
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe, bitte versuche es erneut.")
        print("_______________________________")
        time.sleep(3)