########################################
# AUSMALBUCH-GENERATOR 🎨
########################################
# Erstellt ein perfektes Ausmalbuch als PDF-Dokument
# - 50 weiße Kreise zum Ausmalen
# - Nummern von oben nach unten (1-50)
# - Nummern stehen ÜBER den Kreisen (nicht drin!)
# - A4 Format, perfekt zum Ausdrucken und Ausmalen!
########################################

import time
import os
import platform
import subprocess

# Log-System aktivieren
import log
log.run()

########################################
# HAUPTPROGRAMM
########################################

def run():
    """Startet das Ausmalbuch-Generator Programm."""
    print("🎨 Ausmalbuch-Generator startet...")
    
    # Eindeutigen Dateinamen erstellen
    import datetime
    zeitstempel = datetime.datetime.now().strftime("%H%M%S")
    pdf_name = f"ausmalbuch_{zeitstempel}.pdf"
    
    print(f"📄 Erstelle Ausmalbuch: {pdf_name}")
    
    # PDF erstellen
    erfolg = erstelle_kreise_pdf(pdf_name)
    
    if erfolg:
        # PDF öffnen
        oeffne_pdf_datei(pdf_name)
        print("✅ Ausmalbuch wurde erstellt und geöffnet!")
        print("🖍️  Jetzt können Sie die weißen Kreise ausmalen!")
        
        # Einfache Optionen anzeigen
        zeige_einfache_optionen(pdf_name)
    else:
        print("❌ Es gab ein Problem beim Erstellen des PDFs.")

########################################
# PDF-ERSTELLUNG (VEREINFACHT)
########################################

def erstelle_kreise_pdf(dateiname):
    """
    Erstellt eine PDF-Datei mit weißen Kreisen zum Ausmalen.
    Nummern sind von oben nach unten sortiert - perfekt zum Ausmalen!
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors

        print(f"📝 Erstelle Ausmalbuch-PDF: {dateiname}")
        
        # PDF erstellen
        pdf_canvas = canvas.Canvas(dateiname, pagesize=A4)
        breite, hoehe = A4
        
        print("🎨 Zeichne 50 weiße Kreise zum Ausmalen...")

        # Kreise in Reihen anordnen (von oben nach unten)
        kreise_pro_reihe = 5  # 5 Kreise pro Reihe
        reihen = 10           # 10 Reihen = 50 Kreise total
        
        kreis_nummer = 1
        radius = 25           # Größere Kreise zum einfacheren Ausmalen
        
        for reihe in range(reihen):
            for spalte in range(kreise_pro_reihe):
                # Position berechnen (gleichmäßig verteilt)
                x = 100 + spalte * 100  # Horizontal verteilt
                y = hoehe - 100 - reihe * 70  # Von oben nach unten
                
                # WEISSEN Kreis zeichnen (perfekt zum Ausmalen!)
                pdf_canvas.setStrokeColor(colors.black)  # Schwarzer Rand
                pdf_canvas.setFillColor(colors.white)    # WEIßER Inhalt zum Ausmalen!
                pdf_canvas.circle(x, y, radius, stroke=2, fill=1)  # Dickerer Rand
                
                # Nummer AUSSERHALB des Kreises schreiben (damit man den Kreis frei ausmalen kann)
                pdf_canvas.setFillColor(colors.black)
                pdf_canvas.setFont("Helvetica-Bold", 14)  # Größere, gut lesbare Schrift
                
                # Nummer ÜBER dem Kreis platzieren
                text_x = x - 7  # Zentriert
                text_y = y + radius + 5  # ÜBER dem Kreis
                pdf_canvas.drawString(text_x, text_y, str(kreis_nummer))
                
                kreis_nummer += 1

        pdf_canvas.save()
        print(f"✅ Ausmalbuch-PDF '{dateiname}' mit 50 weißen Kreisen erstellt!")
        print("🖍️  Kreise sind weiß und bereit zum Ausmalen!")
        print("🔢 Nummern sind von oben nach unten angeordnet (1-50)")
        return True
        
    except Exception as fehler:
        print(f"❌ Fehler beim Erstellen der PDF: {fehler}")
        return False

########################################
# DATEI-FUNKTIONEN
########################################

def oeffne_pdf_datei(pdf_name):
    """Öffnet die PDF-Datei im Standard-Viewer."""
    if platform.system() == "Windows":
        os.startfile(pdf_name)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", pdf_name])
    else:  # Linux
        subprocess.call(["xdg-open", pdf_name])

def oeffne_ordner_im_explorer(ordner_pfad):
    """Öffnet den Ordner im Datei-Explorer."""
    if platform.system() == "Windows":
        os.startfile(ordner_pfad)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", ordner_pfad])
    else:  # Linux
        subprocess.call(["xdg-open", ordner_pfad])

########################################
# EINFACHES BENUTZER-MENÜ
########################################

def zeige_einfache_optionen(pdf_name):
    """Zeigt einfache Optionen nach der PDF-Erstellung."""
    print("\n" + "="*50)
    print("🎨 IHR AUSMALBUCH IST FERTIG!")
    print("="*50)
    print("Was möchten Sie tun?")
    print("1 - 📁 Ordner öffnen (zum Drucken)")
    print("2 - 👀 PDF nochmal anzeigen") 
    print("3 - 🔄 Neues Ausmalbuch erstellen")
    print("0 - ✅ Fertig")
    
    wahl = input("\nIhre Wahl (0-3): ").strip()
    
    if wahl == "1":
        print("📁 Öffne Ordner zum Drucken...")
        oeffne_ordner_im_explorer(os.getcwd())
        print("💡 Tipp: Rechtsklick auf PDF → Drucken!")
        
    elif wahl == "2":
        print("� Öffne Ausmalbuch...")
        oeffne_pdf_datei(pdf_name)
        
    elif wahl == "3":
        print("🔄 Erstelle neues Ausmalbuch...")
        import datetime
        neue_zeit = datetime.datetime.now().strftime("%H%M%S")
        neuer_name = f"ausmalbuch_{neue_zeit}.pdf"
        if erstelle_kreise_pdf(neuer_name):
            oeffne_pdf_datei(neuer_name)
            print("✅ Neues Ausmalbuch erstellt!")
        
    elif wahl == "0":
        print("🎉 Viel Spaß beim Ausmalen!")
    else:
        print("❌ Bitte 0, 1, 2 oder 3 eingeben")

########################################
# PROGRAMM-START
########################################

if __name__ == "__main__":
    run()