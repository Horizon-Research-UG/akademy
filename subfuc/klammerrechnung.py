########################################
# start log 
########################################

import log
log.run()

########################################
# ende log 
########################################



import time
import random

def run():
    runden = int(input("Wie viele Runden möchtest du spielen? "))
    mana = int(input("Gib dein Mana ein (Zahl): "))
    for _ in range(runden): 
        quest1(mana)
        quest2(mana)
        quest3(mana)
        print(f"Runde {_ + 1} abgeschlossen!")
        print("_______________________________")
        time.sleep(1)



#############################################
# anfang Klammerrechnung Quest 1
##############################################


def quest1(mana):
    print("Spiel 2 - Klammer 1 - (a+b)*e")
    import time
    time.sleep(4)
    a = random.randint(-mana, mana)
    b = random.randint(-mana, mana)
    e = random.randint(-mana, mana)
    x = (a + b) * e

    if input(f"Was ist ({a} + {b}) * {e} ? ") == str(x):
        print("Richtig")
    else:
        print("Falsch, die richtige Antwort ist:", x)

#############################################
# Ende Klammerrechnung Quest 1
#############################################


# quest  2 - klammerrechnung 2
def quest2(mana):
    print("Klammer 2 - (a+b)*(e+f)")
    a = random.randint(-mana, mana)
     #mit der einfach gerechnet werden kann
    b = random.randint(-mana, mana)
    e = random.randint(-mana, mana)
    f = random.randint(-mana, mana)
    x = (a + b) * (e + f)

    if input(f"Was ist ({a} + {b}) * ({e} + {f}) ? ") == str(x):
        print("Richtig")
    else:
        print("Falsch, die richtige Antwort ist:", x)   
#############################################
# Ende Klammerrechnung Quest 2







#############################################
# quest  3 - klammerrechnung mit einer variablen a
def quest3(mana):
    print("Klammer 3 - (a+b)*a")
    a = random.randint(-mana, mana)
    b = random.randint(-mana, mana)
    x = (a + b) * a

    if input(f"Was ist ({a} + {b}) * {a} ? ") == str(x):
        print("Richtig")
    else:
        print("Falsch, die richtige Antwort ist:", x)




#############################################
# Ende Hauptprogramm
#############################################

if __name__ == "__main__":
    run()