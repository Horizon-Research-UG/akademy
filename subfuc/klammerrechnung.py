########################################
# start log 
########################################

import sys
import os
# Füge das übergeordnete Verzeichnis zum Python-Pfad hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import log
log.run()

########################################
# ende log 
########################################



import time
import random

def run():
    runden = int(input("Spiel 1: (runden)goal: "))
    mana = int(input("Gib dein Mana ein (Zahl): "))
    for _ in range(runden): 
        quest1(mana)
        quest2(mana)
        quest3(mana)
        print(f"main loop - Runde {_ + 1} abgeschlossen!")
        print("_______________________________")
        time.sleep(3)


#############################################
# Ende Hauptprogramm
#############################################
# run quests



#############################################
# anfang Klammerrechnung Quest 1
##############################################


def quest1(mana):
    print("s1.1 - Klammer 1 - (a+b)*e")
    import time
    time.sleep(4)
    a = random.randint(-mana, mana)
    b = random.randint(-mana, mana)
    e = random.randint(-mana, mana)
    x = (a + b) * e

    if input(f"Was ist ({a} + {b}) * {e} ? ") == str(x):
        print("s1.1 - Richtig")
    else:
        print("s1.1 - Falsch, die richtige Antwort ist:", x)

#############################################
# Ende Klammerrechnung Quest 1
#############################################


# quest  2 - klammerrechnung 2
def quest2(mana):
    print("s1.2 - Klammer 2 - (a+b)*(e+f)")
    a = random.randint(-mana, mana)
     #mit der einfach gerechnet werden kann
    b = random.randint(-mana, mana)
    e = random.randint(-mana, mana)
    f = random.randint(-mana, mana)
    x = (a + b) * (e + f)

    if input(f"Was ist ({a} + {b}) * ({e} + {f}) ? ") == str(x):
        print("s1.2 - Richtig")
    else:
        print("s1.2 - Falsch, die richtige Antwort ist:", x)
#############################################
# Ende Klammerrechnung Quest 2







#############################################
# quest  3 - klammerrechnung mit einer variablen a
def quest3(mana):
    print("s1.3 - Klammer 3 - (a+b)*a")
    a = random.randint(-mana, mana)
    b = random.randint(-mana, mana)
    x = (a + b) * a

    if input(f"Was ist ({a} + {b}) * {a} ? ") == str(x):
        print("s1.3 - Richtig")
    else:
        print("s1.3 - Falsch, die richtige Antwort ist:", x)




#############################################
# Ende Hauptprogramm
#############################################

if __name__ == "__main__":
    run()