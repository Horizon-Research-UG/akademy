########################################
# TIMELINE GENERATOR
########################################
# Erstellt eine Timeline mit zufällig verteilten Formen
# - Keine Überschneidungen der Kreise
# - Zufällige Anordnung in der Mitte
# - Weiße Kreise zum Ausmalen
# - Nummern bleiben zur Orientierung
########################################

import time
import os
import platform
import subprocess
import datetime

# Log-System aktivieren
import log
log.run()

########################################
# BENUTZEREINGABE
########################################

def frage_nach_timeline_details():
    """
    Fragt den Benutzer nach Anzahl Kreise und Überschrift.
    Gibt ein Dictionary mit beiden Werten zurück.
    """
    print("\n" + "="*60)
    print("� ERSTELLEN SIE IHRE PERSÖNLICHE TIMELINE!")
    print("="*60)
    
    # Schritt 1: Überschrift abfragen
    print("📝 SCHRITT 1: Wie soll Ihre Timeline heißen?")
    print("💡 Beispiele: 'Meine Träume', 'Heute machbar', 'Meine Ziele'")
    
    while True:
        ueberschrift = input("\n➤ Überschrift: ").strip()
        if len(ueberschrift) >= 2:
            print(f"✅ Schöne Überschrift: '{ueberschrift}'!")
            break
        else:
            print("⚠️  Bitte mindestens 2 Zeichen eingeben!")
    
    # Schritt 2: Anzahl Kreise abfragen  
    print("\n🎯 SCHRITT 2: Wie viele Kreise möchten Sie?")
    print("💡 Empfehlungen:")
    print("   🟢 5-15 Kreise   → Schnell & entspannt")
    print("   🟡 16-30 Kreise  → Mittlere Herausforderung") 
    print("   🔴 31-50 Kreise  → Viele Kreise (kann länger dauern)")
    print("\n📝 TIPP: Weniger Kreise = mehr Platz zum Ausmalen!")
    
    while True:
        try:
            eingabe = input("\n➤ Anzahl Kreise (5-50): ").strip()
            anzahl = int(eingabe)
            
            if 5 <= anzahl <= 50:
                print(f"✅ Perfekt! Erstelle {anzahl} Kreise für Sie!")
                break
            elif anzahl < 5:
                print("⚠️  Mindestens 5 Kreise! Versuchen Sie es nochmal.")
            elif anzahl > 50:
                print("⚠️  Maximal 50 Kreise! Mehr wird zu eng.")
            else:
                print("❌ Bitte eine Zahl zwischen 5 und 50 eingeben.")
                
        except ValueError:
            print("❌ Bitte eine gültige Zahl eingeben!")
    
    return {
        'ueberschrift': ueberschrift,
        'anzahl_kreise': anzahl
    }

########################################
# HAUPTPROGRAMM
########################################

def run():
    """Startet den Timeline-Generator."""
    print("📅 Timeline-Generator startet...")
    
    # Benutzer nach Überschrift und Anzahl fragen
    timeline_details = frage_nach_timeline_details()
    ueberschrift = timeline_details['ueberschrift']
    anzahl_kreise = timeline_details['anzahl_kreise']
    
    # Eindeutigen Dateinamen erstellen
    zeitstempel = datetime.datetime.now().strftime("%H%M%S")
    # Dateiname sicher machen (keine Sonderzeichen)
    safe_titel = "".join(c for c in ueberschrift if c.isalnum() or c in (' ', '-', '_')).strip()[:20]
    html_name = f"timeline_{safe_titel}_{anzahl_kreise}kreise_{zeitstempel}.html"
    
    print(f"📄 Erstelle Timeline '{ueberschrift}' mit {anzahl_kreise} Kreisen: {html_name}")
    
    # HTML-Timeline erstellen
    erfolg = erstelle_html_timeline(html_name, anzahl_kreise, ueberschrift)
    
    if erfolg:
        # HTML öffnen
        oeffne_datei(html_name)
        print("✅ Timeline wurde erstellt und geöffnet!")
        print("🖨️  Drücken Sie Strg+P zum Drucken!")
        zeige_einfache_optionen(html_name)
    else:
        print("❌ Es gab ein Problem beim Erstellen der Timeline.")

########################################
# HTML-TIMELINE ERSTELLEN
########################################

def erstelle_html_timeline(dateiname, anzahl_kreise, ueberschrift):
    """
    Erstellt eine HTML-Timeline mit der gewünschten Anzahl Kreise und Überschrift.
    Kreise überschneiden sich nicht und sind zufällig verteilt!
    """
    try:
        import random
        import math
        
        print(f"📅 Erstelle Timeline mit {anzahl_kreise} perfekt verteilten Kreisen (OHNE Überschneidungen)...")
        
        # PERFEKTE Positionen ohne Überschneidungen berechnen
        kreise = []
        kreis_radius = 30  # Tatsächlicher Kreis-Radius in Pixeln
        
        # Intelligenter Mindestabstand basierend auf Anzahl
        if anzahl_kreise <= 15:
            mindest_abstand = 120  # Viel Platz für wenige Kreise
        elif anzahl_kreise <= 30:
            mindest_abstand = 100  # Mittlerer Platz
        else:
            mindest_abstand = 80   # Weniger Platz für viele Kreise
            
        bereich_breite = 800  # Verfügbare Breite
        bereich_hoehe = 600   # Verfügbare Höhe
        
        print(f"🎯 Berechne {anzahl_kreise} perfekte Positionen OHNE Überschneidungen...")
        print(f"📏 Mindestabstand: {mindest_abstand} Pixel")
        
        for nummer in range(1, anzahl_kreise + 1):
            position_gefunden = False
            versuche = 0
            max_versuche = 2000  # Mehr Versuche
            
            while not position_gefunden and versuche < max_versuche:
                # Zufällige Position mit großem Rand
                x = random.randint(mindest_abstand, bereich_breite - mindest_abstand)
                y = random.randint(mindest_abstand, bereich_hoehe - mindest_abstand)
                
                # Prüfen ob Position WIRKLICH frei ist
                position_ist_frei = True
                for bestehender_kreis in kreise:
                    # Berechne exakten Abstand zwischen Mittelpunkten
                    abstand = math.sqrt((x - bestehender_kreis['x'])**2 + (y - bestehender_kreis['y'])**2)
                    
                    # GROSSER Mindestabstand = garantiert keine Überschneidung
                    if abstand < mindest_abstand:
                        position_ist_frei = False
                        break
                
                if position_ist_frei:
                    kreise.append({'x': x, 'y': y, 'nummer': nummer})
                    position_gefunden = True
                    print(f"✅ Kreis {nummer} platziert bei ({x}, {y})")
                
                versuche += 1
            
            if not position_gefunden:
                print(f"⚠️  Kreis {nummer} - Position schwer zu finden, platziere vorsichtig...")
                # Suche systematisch eine freie Position
                for test_x in range(mindest_abstand, bereich_breite - mindest_abstand, 50):
                    for test_y in range(mindest_abstand, bereich_hoehe - mindest_abstand, 50):
                        position_ist_frei = True
                        for bestehender_kreis in kreise:
                            abstand = math.sqrt((test_x - bestehender_kreis['x'])**2 + (test_y - bestehender_kreis['y'])**2)
                            if abstand < mindest_abstand:
                                position_ist_frei = False
                                break
                        if position_ist_frei:
                            kreise.append({'x': test_x, 'y': test_y, 'nummer': nummer})
                            position_gefunden = True
                            break
                    if position_gefunden:
                        break
        
        # HTML-Code erstellen (ohne f-String für CSS)
        html_inhalt = """
<!DOCTYPE html>
<html>
<head>
    <title>Timeline - """ + str(anzahl_kreise) + """ Kreise</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0;
            padding: 20px;
            background: white;
            position: relative;
        }
        .titel { 
            text-align: center; 
            font-size: 28px; 
            margin-bottom: 30px;
            color: black;
            font-weight: bold;
        }
        .timeline-container {
            position: relative;
            width: 1000px;
            height: 800px;
            margin: 0 auto;
            border: 2px solid #ccc;
            background: #f9f9f9;
        }
        .kreis-element {
            position: absolute;
            text-align: center;
        }
        .nummer {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 5px;
            color: black;
        }
        .kreis {
            width: 60px;
            height: 60px;
            border: 3px solid black;
            border-radius: 50%;
            background-color: white;
            display: inline-block;
        }
        @media print {
            body { margin: 0; padding: 10px; }
            .timeline-container { width: 95%; height: 90vh; }
        }
    </style>
</head>
<body>
    <div class="titel">📅 """ + ueberschrift + """ - """ + str(anzahl_kreise) + """ Kreise 📅</div>
    <div class="timeline-container">
"""
        
        # Alle Kreise an zufälligen Positionen platzieren
        for kreis in kreise:
            html_inhalt += f'''        <div class="kreis-element" style="left: {kreis['x']}px; top: {kreis['y']}px;">
            <div class="nummer">{kreis['nummer']}</div>
            <div class="kreis"></div>
        </div>
'''
        
        # HTML abschließen
        html_inhalt += """    </div>
</body>
</html>"""
        
        # HTML-Datei schreiben
        with open(dateiname, 'w', encoding='utf-8') as datei:
            datei.write(html_inhalt)
        
        print(f"✅ HTML-Timeline '{dateiname}' erfolgreich erstellt!")
        print(f"📅 {anzahl_kreise} Kreise perfekt verteilt - GARANTIERT ohne Überschneidungen!")
        print("🎯 Jeder Kreis hat genug Platz zum entspannten Ausmalen!")
        print("🖨️  Öffnet sich im Browser - einfach Strg+P zum Drucken!")
        return True
        
    except Exception as fehler:
        print(f"❌ Fehler: {fehler}")
        return False

########################################
# DATEI-FUNKTIONEN
########################################

def oeffne_datei(dateiname):
    """Öffnet die HTML-Datei im Standard-Browser."""
    try:
        if platform.system() == "Windows":
            os.startfile(dateiname)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", dateiname])
        else:  # Linux
            subprocess.call(["xdg-open", dateiname])
    except:
        print(f"📁 Bitte öffnen Sie '{dateiname}' manuell in Ihrem Browser")

def oeffne_ordner_im_explorer(ordner_pfad):
    """Öffnet den Ordner im Datei-Explorer."""
    try:
        if platform.system() == "Windows":
            os.startfile(ordner_pfad)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", ordner_pfad])
        else:  # Linux
            subprocess.call(["xdg-open", ordner_pfad])
    except:
        print("📁 Ordner konnte nicht geöffnet werden")

########################################
# EINFACHES BENUTZER-MENÜ
########################################

def zeige_einfache_optionen(dateiname):
    """Zeigt einfache Optionen nach der Erstellung."""
    print("\n" + "="*50)
    print("📅 IHRE TIMELINE IST FERTIG!")
    print("="*50)
    print("Was möchten Sie tun?")
    print("1 - 📁 Ordner öffnen")
    print("2 - 🌐 Timeline nochmal öffnen") 
    print("3 - 🔄 Neue Timeline erstellen")
    print("0 - ✅ Fertig")
    
    wahl = input("\nIhre Wahl (0-3): ").strip()
    
    if wahl == "1":
        print("📁 Öffne Ordner...")
        oeffne_ordner_im_explorer(os.getcwd())
        print("💡 Tipp: Rechtsklick auf HTML → Öffnen mit → Browser → Drucken!")
        
    elif wahl == "2":
        print("🌐 Öffne Timeline...")
        oeffne_datei(dateiname)
        
    elif wahl == "3":
        print("🔄 Erstelle neue Timeline...")
        neue_details = frage_nach_timeline_details()
        neue_ueberschrift = neue_details['ueberschrift']
        neue_anzahl = neue_details['anzahl_kreise']
        neue_zeit = datetime.datetime.now().strftime("%H%M%S")
        safe_titel = "".join(c for c in neue_ueberschrift if c.isalnum() or c in (' ', '-', '_')).strip()[:20]
        neuer_name = f"timeline_{safe_titel}_{neue_anzahl}kreise_{neue_zeit}.html"
        if erstelle_html_timeline(neuer_name, neue_anzahl, neue_ueberschrift):
            oeffne_datei(neuer_name)
            print("✅ Neue Timeline erstellt!")
        
    elif wahl == "0":
        print("🎉 Viel Spaß beim Ausmalen!")
    else:
        print("❌ Bitte 0, 1, 2 oder 3 eingeben")

########################################
# PROGRAMM-START
########################################

if __name__ == "__main__":
    run()