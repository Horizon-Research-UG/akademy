import log
log.run()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1x1 Klammerspiel - Basierend auf Mana-System
Generiert Klammeraufgaben mit zufälligen Zahlen basierend auf Mana-Level
"""

import random
import sys
import os



def run():
    """Hauptfunktion zum Starten des Spiels"""
    try:
        spiel = KlammerSpiel1x1()
        spiel.spiel_starten()
    except Exception as e:
        log(f"Fehler: {e}")
        print(f"❌ Ein Fehler ist aufgetreten: {e}")

# Log-System importieren
try:
    from log import log
except ImportError:
    # Falls log.py nicht gefunden wird
    def log(nachricht):
        print(f"[LOG] {nachricht}")

class KlammerSpiel1x1:
    def __init__(self):
        self.mana = 0
        self.max_mana = 10
        self.min_mana = -10
        self.runde = 1
        self.punkte = 0
        
    def frage_nach_mana(self):
        """Fragt den Benutzer nach dem gewünschten Mana-Level"""
        print("\n🎯 MANA-EINSTELLUNG")
        print("="*30)
        print("💡 Das Mana bestimmt die Zahlenrange:")
        print("   Mana = 3  → Zahlen von -3 bis +3")
        print("   Mana = 5  → Zahlen von -5 bis +5")
        print("   Mana = 10 → Zahlen von -10 bis +10")
        
        while True:
            try:
                mana_input = input("\n➤ Gewünschtes Mana-Level (1-20): ").strip()
                mana = int(mana_input)
                
                if 1 <= mana <= 20:
                    self.mana = mana
                    self.max_mana = mana
                    self.min_mana = -mana
                    print(f"✅ Mana auf {mana} gesetzt!")
                    print(f"📊 Zahlenrange: {self.min_mana} bis {self.max_mana}")
                    break
                else:
                    print("⚠️  Bitte eine Zahl zwischen 1 und 20 eingeben!")
                    
            except ValueError:
                print("❌ Bitte eine gültige Zahl eingeben!")
        
    def zeige_status(self):
        """Zeigt aktuellen Spielstatus an"""
        print("\n" + "="*50)
        print(f"🎮 KLAMMER-SPIEL 1x1 - RUNDE {self.runde}")
        print("="*50)
        print(f"⚡ Mana: {self.mana:+d} (Range: {self.min_mana} bis {self.max_mana})")
        print(f"🏆 Punkte: {self.punkte}")
        print(f"📊 Zahlen-Größe: {self.berechne_zahlen_groesse()}")
        
    def berechne_zahlen_groesse(self):
        """Berechnet die Größe der Zahlen basierend auf Mana"""
        abs_mana = abs(self.mana)
        return f"Range: -{abs_mana} bis +{abs_mana}"
    
    def generiere_zahl(self):
        """Generiert eine Zahl im Bereich von -mana bis +mana (aber nicht 0)"""
        abs_mana = abs(self.mana)
        
        # Zahl zwischen -mana und +mana generieren, aber 0 ausschließen
        while True:
            zahl = random.randint(-abs_mana, abs_mana)
            if zahl != 0:  # 0 ausschließen für bessere Aufgaben
                return zahl
    

    
    def generiere_aufgabe_typ_a(self):
        """Generiert Aufgabe vom Typ: a(b - cx)"""
        a = self.generiere_zahl()
        b = self.generiere_zahl()
        c = self.generiere_zahl()
        x_wert = random.choice(['x', 'y', 'z', 'a', 'b'])
        
        aufgabe = f"{a}({b} - {c}{x_wert})"
        loesung = f"{a * b} - {a * c}{x_wert}"
        
        return aufgabe, loesung
    
    def generiere_aufgabe_typ_b(self):
        """Generiert Aufgabe vom Typ: (ab - c)(d - ef)"""
        a = self.generiere_zahl()
        b_var = random.choice(['x', 'y', 'z', 'a', 'b'])
        c = self.generiere_zahl()
        d = self.generiere_zahl()
        e = self.generiere_zahl()
        f_var = random.choice(['x', 'y', 'z', 'a', 'b'])
        
        aufgabe = f"({a}{b_var} - {c})({d} - {e}{f_var})"
        loesung = f"{a * d}{b_var} - {a * e}{b_var}{f_var} - {c * d} + {c * e}{f_var}"
        
        return aufgabe, loesung
    
    def generiere_aufgabe_typ_c(self):
        """Generiert Aufgabe vom Typ: (ax - b)(cx + d)"""
        a = self.generiere_zahl()
        b = self.generiere_zahl()
        c = self.generiere_zahl()
        d = self.generiere_zahl()
        x_var = random.choice(['x', 'y', 'z'])
        
        aufgabe = f"({a}{x_var} - {b})({c}{x_var} + {d})"
        # Ausmultipliziert: ac*x² + ad*x - bc*x - bd
        koeff_x2 = a * c
        koeff_x = a * d - b * c
        konstante = -b * d
        
        loesung = f"{koeff_x2}{x_var}² + {koeff_x:+d}{x_var} + {konstante:+d}"
        
        return aufgabe, loesung
    
    def generiere_aufgabe_typ_d(self):
        """Generiert Aufgabe vom Typ: (a - bx)(c + dx)"""
        a = self.generiere_zahl()
        b = self.generiere_zahl()
        c = self.generiere_zahl()
        d = self.generiere_zahl()
        x_var = random.choice(['x', 'y', 'z'])
        
        aufgabe = f"({a} - {b}{x_var})({c} + {d}{x_var})"
        # Ausmultipliziert: ac + ad*x - bc*x - bd*x²
        koeff_x2 = -b * d
        koeff_x = a * d - b * c
        konstante = a * c
        
        loesung = f"{konstante} + {koeff_x:+d}{x_var} + {koeff_x2:+d}{x_var}²"
        
        return aufgabe, loesung
    
    def spiele_runde(self):
        """Spielt eine Runde des Klammerspiels"""
        self.zeige_status()
        
        # Zufälligen Aufgabentyp wählen
        aufgaben_typen = [
            ('a', self.generiere_aufgabe_typ_a),
            ('b', self.generiere_aufgabe_typ_b), 
            ('c', self.generiere_aufgabe_typ_c),
            ('d', self.generiere_aufgabe_typ_d)
        ]
        
        typ_name, generator_func = random.choice(aufgaben_typen)
        aufgabe, loesung = generator_func()
        
        print(f"\n🧮 AUFGABE (Typ {typ_name}):")
        print(f"Lösen Sie die Klammern auf: {aufgabe}")
        print("\n💡 Drücken Sie Enter um die Lösung zu sehen...")
        input()
        
        print(f"✅ LÖSUNG: {loesung}")
        
        # Bewertung durch Spieler
        print("\nWie schwer war diese Aufgabe?")
        print("1 = Sehr einfach  2 = Einfach  3 = Normal  4 = Schwer  5 = Sehr schwer")
        
        while True:
            try:
                bewertung = int(input("Bewertung (1-5): "))
                if 1 <= bewertung <= 5:
                    break
                else:
                    print("Bitte eine Zahl zwischen 1 und 5 eingeben!")
            except ValueError:
                print("Bitte eine gültige Zahl eingeben!")
        
        # Punkte basierend auf Bewertung und Mana
        if bewertung <= 2:
            self.punkte += 10
        elif bewertung == 3:
            self.punkte += 20
        else:
            self.punkte += 30
            
        print(f"🏆 +{30 if bewertung > 3 else (20 if bewertung == 3 else 10)} Punkte!")
        
        self.runde += 1
        log(f"Runde {self.runde-1} abgeschlossen - Mana: {self.mana}, Punkte: {self.punkte}")
    
    def spiel_starten(self):
        """Startet das Klammerspiel"""
        print("🎮 WILLKOMMEN ZUM KLAMMER-SPIEL 1x1!")
        print("="*50)
        print("📚 Regel: Lösen Sie Klammerausdrücke auf")
        print("⚡ Mana bestimmt die Zahlenrange der Aufgaben") 
        print("� Sie wählen Ihr Mana-Level selbst!")
        
        # Mana vom Benutzer abfragen
        self.frage_nach_mana()
        
        while True:
            try:
                self.spiele_runde()
                
                print(f"\n🎯 ZWISCHENSTAND:")
                print(f"Runden gespielt: {self.runde-1}")
                print(f"Gesamtpunkte: {self.punkte}")
                
                weiter = input("\nNoch eine Runde? (j/n): ").lower().strip()
                if weiter not in ['j', 'ja', 'y', 'yes', '']:
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Spiel beendet!")
                break
        
        print(f"\n🏁 ENDSTAND:")
        print(f"Runden gespielt: {self.runde-1}")
        print(f"Gesamtpunkte: {self.punkte}")
        print("Danke fürs Spielen! 🎮")

def main():
    """Hauptfunktion"""
    try:
        spiel = KlammerSpiel1x1()
        spiel.spiel_starten()
    except Exception as e:
        log(f"Fehler: {e}")
        print(f"❌ Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
