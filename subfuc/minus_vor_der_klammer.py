import sys
import os
# Füge das übergeordnete Verzeichnis zum Python-Pfad hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#import log
#log.run()

import time
import random

def run():
    print("Minus vor der Klammer Spiel!")
    print("_______________________________")
    import time
    time.sleep(2)
    global runden, mana
    mana = int(input("Gib dein Mana ein (Zahl): "))
    runden = int(input("Wie viele Runden möchtest du spielen? "))
    for _ in range(runden):
        quest1(mana)
        quest2(mana)
        #quest3()
        print(f"Runde {_ + 1} abgeschlossen!")
        print("_______________________________")
        time.sleep(1)
#############################################
# anfang Minus vor der Klammer Quest 1
#############################################
def quest1(mana):
    print("Minus vor der Klammer 1 - -(a+b)")
    for _ in range(runden):
        a = random.randint(-mana, mana)
        b = random.randint(-mana, mana)
        x = -(a + b)

        if input(f"Was ist -({a} + {b}) ? ") == str(x):
            print("Richtig")
        else:
            print("Falsch, die richtige Antwort ist:", x)
        mana += 1  # Erhöhe das Mana nach jeder Frage
#############################################
# Ende Minus vor der Klammer Quest 1
#############################################

# quest  2 - Minus vor der Klammer - schwieriger
def quest2(mana):
    print("Minus vor der Klammer 2")
    time.sleep(1)
    a = random.randint(-mana, mana)
    b = random.randint(-mana, mana)
    c = random.randint(-mana, mana)
    x = -(a - b * c)

    if input(f"Was ist -({a} - {b} * {c}) ? ") == str(x):
        print("Richtig")
    else:
        print("Falsch, die richtige Antwort ist:", x)
