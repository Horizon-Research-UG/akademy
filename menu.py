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
import log
import subfuc.luh.luh1a1 as test1a1
log.run()


def run():
    while True:
        print("_______________________________")
        print("Hauptmenü - Wähle ein Modul:")
        print("1. Ausmalbuch")
        print("2. Minus vor der Klammer")
        print("3. Klammerrechnung")
        print("4. 1a1")
        print("z. Beenden")
        auswahl = input("Gib die Zahl deiner Wahl ein: ")

        if auswahl == '1':
            ausmalbuch.run()
        elif auswahl == '2':
            minus_vor_der_klammer.run()
        elif auswahl == '3':
            klammerrechnung.run()
        elif auswahl == '4':
            test1a1.run()
        elif auswahl == 'z':
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe, bitte versuche es erneut.")
        print("_______________________________")
        time.sleep(3)