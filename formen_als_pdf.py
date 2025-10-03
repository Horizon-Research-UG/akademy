########################################
# FORMEN ALS PDF - GENERATOR
########################################
# Erstellt geometrische Formen (Waben) als PDF-Dokument
# Standard-Einstellungen:
# - 100 Waben zufällig verteilt
# - A4 Format (Hochformat)
# - Schwarze Linien auf weißem Hintergrund
# - Automatische PDF-Anzeige nach Erstellung
########################################

# Import der benötigten Module
import time
import os
import platform
import subprocess

# Log-System aktivieren (protokolliert Programm-Aufrufe)
import log
log.run()

########################################
# HAUPTPROGRAMM
########################################

def run():
    """Startet das PDF-Generator Programm - einfach und direkt."""
    print("🔧 PDF-Generator startet...")
    
    # PDF-Datei erstellen und sofort öffnen
    pdf_name = "formen_als_pdf.pdf"
    print("📄 Erstelle PDF mit 100 Waben...")
    
    erstelle_waben_pdf(pdf_name)  # PDF erstellen
    oeffne_pdf_datei(pdf_name)    # PDF öffnen
    
    print("✅ Fertig! PDF wurde erstellt und geöffnet.")
    
    # Einfaches Nachfrage-Menü
    zeige_einfache_optionen(pdf_name)



########################################
# PDF-ERSTELLUNG FUNKTIONEN
########################################

def erstelle_waben_pdf(dateiname):
    """
    Erstellt eine PDF-Datei mit 100 zufällig verteilten Waben.
    
    Parameter:
    - dateiname: Name der zu erstellenden PDF-Datei
    """
    # Importiere benötigte PDF-Module
    import random
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors

    # PDF-Canvas erstellen (A4 Hochformat)
    pdf_canvas = canvas.Canvas(dateiname, pagesize=A4)
    seiten_breite, seiten_hoehe = A4

    # 100 Waben an zufälligen Positionen zeichnen
    anzahl_waben = 100
    for wabe_nummer in range(anzahl_waben):
        # Zufällige Position auf der Seite bestimmen
        zufalls_x = random.randint(50, int(seiten_breite - 50))  # Mit Rand
        zufalls_y = random.randint(50, int(seiten_hoehe - 50))   # Mit Rand
        
        # Einzelne Wabe an dieser Position zeichnen
        zeichne_einzelne_wabe(pdf_canvas, zufalls_x, zufalls_y)

    # PDF-Datei speichern und schließen
    pdf_canvas.save()
    print(f"✅ PDF '{dateiname}' erfolgreich erstellt!")

def zeichne_einzelne_wabe(canvas_objekt, x_position, y_position, waben_groesse=15):
    """
    Zeichnet eine einfache Wabe (Sechseck) an der angegebenen Position.
    
    Parameter:
    - canvas_objekt: Das PDF-Canvas zum Zeichnen
    - x_position: X-Koordinate der Wabe
    - y_position: Y-Koordinate der Wabe  
    - waben_groesse: Größe der Wabe in Punkten
    """
    # Importiere Farben für die Wabe
    from reportlab.lib import colors
    import math
    
    # Setze Farben für die Wabe
    canvas_objekt.setStrokeColor(colors.black)  # Schwarzer Rand
    canvas_objekt.setFillColor(colors.white)    # Weißer Inhalt
    canvas_objekt.setLineWidth(1)               # Dünne Linie
    
    # Berechne die 6 Eckpunkte eines Sechsecks und zeichne sie
    anzahl_ecken = 6
    
    # Starte einen neuen Pfad für das Sechseck
    pfad = canvas_objekt.beginPath()
    
    for ecke in range(anzahl_ecken + 1):  # +1 um das Sechseck zu schließen
        # Winkel für diese Ecke berechnen (360° / 6 Ecken = 60° pro Ecke)
        winkel_grad = 60 * ecke
        winkel_radians = math.radians(winkel_grad)
        
        # X- und Y-Koordinate dieser Ecke berechnen
        ecke_x = x_position + waben_groesse * math.cos(winkel_radians)
        ecke_y = y_position + waben_groesse * math.sin(winkel_radians)
        
        if ecke == 0:
            # Erste Ecke: Startpunkt setzen
            pfad.moveTo(ecke_x, ecke_y)
        else:
            # Weitere Ecken: Linie ziehen
            pfad.lineTo(ecke_x, ecke_y)
    
    # Sechseck zeichnen (mit Rand und Füllung)
    canvas_objekt.drawPath(pfad, stroke=1, fill=1)

########################################
# DATEI- UND ORDNER-FUNKTIONEN
########################################

def oeffne_pdf_datei(pdf_dateiname):
    """
    Öffnet die PDF-Datei im Standard-PDF-Viewer des Betriebssystems.
    
    Parameter:
    - pdf_dateiname: Name der zu öffnenden PDF-Datei
    """
    if platform.system() == "Windows":
        os.startfile(pdf_dateiname)  # Windows: Standardprogramm öffnen
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", pdf_dateiname])
    else:  # Linux und andere Unix-Systeme
        subprocess.call(["xdg-open", pdf_dateiname])

def oeffne_ordner_im_explorer(ordner_pfad):
    """
    Öffnet den angegebenen Ordner im Datei-Explorer des Betriebssystems.
    
    Parameter:
    - ordner_pfad: Pfad zum zu öffnenden Ordner
    """
    if platform.system() == "Windows":
        os.startfile(ordner_pfad)  # Windows Explorer öffnen
    elif platform.system() == "Darwin":  # macOS Finder
        subprocess.call(["open", ordner_pfad])
    else:  # Linux Dateimanager
        subprocess.call(["xdg-open", ordner_pfad])

########################################
# BENUTZER-INTERFACE FUNKTIONEN
########################################

def zeige_einfache_optionen(pdf_name):
    """
    Zeigt ein interaktives Menü mit Optionen für die erstellte PDF-Datei.
    
    Parameter:
    - pdf_dateiname: Name der PDF-Datei für die Optionen
    """
    aktueller_ordner = os.getcwd()  # Aktuelles Arbeitsverzeichnis ermitteln
    
    # Schöne Menü-Anzeige
    print("\n" + "="*60)
    print("🎉 PDF ERFOLGREICH ERSTELLT!")
    print("="*60)
    print(f"📄 PDF-Datei: {pdf_dateiname}")
    print(f"📁 Gespeichert in: {aktueller_ordner}")
    print("\n🔧 Was möchten Sie als nächstes tun?")
    print("-" * 40)
    print("1 - 📁 Ordner mit PDF-Datei öffnen")
    print("2 - 👀 PDF erneut anzeigen") 
    print("3 - 🔄 Neue PDF mit anderen Waben erstellen")
    print("0 - 👋 Programm beenden")
    print("-" * 40)
    
    # Endlose Schleife für Benutzereingaben
    while True:
        benutzer_wahl = input("\n➤ Ihre Wahl (0-3): ").strip()
        
        if benutzer_wahl == "1":
            print("📁 Öffne Ordner im Explorer...")
            oeffne_ordner_im_explorer(aktueller_ordner)
            print("✅ Ordner wurde geöffnet!")
            break
            
        elif benutzer_wahl == "2":
            print("� Öffne PDF erneut...")
            oeffne_pdf_datei(pdf_dateiname)
            print("✅ PDF wurde geöffnet!")
            break
            
        elif benutzer_wahl == "3":
            print("🔄 Erstelle neue PDF mit anderen Zufalls-Waben...")
            erstelle_waben_pdf(pdf_dateiname)  # Neue PDF erstellen
            oeffne_pdf_datei(pdf_dateiname)    # Sofort öffnen
            print("✅ Neue PDF erstellt und geöffnet!")
            break
            
        elif benutzer_wahl == "0":
            print("👋 Auf Wiedersehen! Programm wird beendet.")
            break
            
        else:
            print("❌ Ungültige Eingabe! Bitte wählen Sie 0, 1, 2 oder 3.")

########################################
# PROGRAMM-START
########################################

if __name__ == "__main__":
    """
    Startet das Programm nur wenn diese Datei direkt ausgeführt wird.
    (Nicht wenn sie als Modul importiert wird)
    """
    run()