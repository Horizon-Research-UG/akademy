import inspect
import os




# 1. "Wo bin ich?" - Finde das Hauptverzeichnis (akademy/)
script_dir = os.path.dirname(os.path.abspath(__file__))  # aktueller Ordner: sublogs/
parent_dir = os.path.dirname(script_dir)                 # ein Ordner höher: subfuc/
main_dir = os.path.dirname(parent_dir)                   # noch ein Ordner höher: akademy/

# 2. "Baue den Pfad zum logs-Ordner"
logs_dir = os.path.join(main_dir, "logs")

# 3. "Baue den kompletten Pfad zur Log-Datei"
dateiname = os.path.join(logs_dir, "anki_logn.txt")

# 4. "Falls der logs-Ordner nicht da ist, erstelle ihn"
os.makedirs(logs_dir, exist_ok=True)


def create_log_file():
    try:
        with open(dateiname, "x", encoding='utf-8') as file:
            file.write("Anki log\n")
            file.write("=====================\n")
    except FileExistsError:
        pass

# prepend new entries (newest at top)
import datetime
from itertools import count
import time
def count_calls():
    try:
        # Versuche erst UTF-8, dann Windows-Encoding als Fallback
        try:
            with open(dateiname, "r", encoding='utf-8') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            print("UTF-8 failed, trying Windows encoding...")
            with open(dateiname, "r", encoding='cp1252') as file:
                lines = file.readlines()
        count = len(lines) - 2  # Subtract header lines
    except FileNotFoundError:
        print("Anki-Log-Datei nicht gefunden, erstelle neue...")
        create_log_file()  # Erstelle die Datei erst jetzt
        count = 0
        lines = ["Anki log\n", "=====================\n"]
    
    count += 1
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ### 
    # SICHERER Aufruf - verhindere Crash bei fehlendem f_back
    try:
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            calling_script = inspect.getframeinfo(frame.f_back.f_back).filename
        else:
            calling_script = "unknown"
    except:
        calling_script = "error_getting_caller"
    
    # Nur den Dateinamen extrahieren
    what = os.path.basename(calling_script)
    new_entry = f"call: {count} - date: {date} - what: {what} - Script: {calling_script}\n"

    # Neue Einträge OBEN einfügen (nach Header)
    if len(lines) >= 2:
        # Header behalten, neuen Eintrag nach Header einfügen
        header = lines[:2]  # "Anki log" und "============="
        old_entries = lines[2:]  # Alte Einträge
        new_content = header + [new_entry] + old_entries
    else:
        # Falls keine Header da sind
        new_content = [new_entry]
    
    # Datei komplett neu schreiben MIT UTF-8 ENCODING
    with open(dateiname, "w", encoding='utf-8') as file:
        file.writelines(new_content)
    
    return count

def run():
    """Hauptfunktion zum Starten des Logging"""
    create_log_file()
    count_calls()
    
# Nur ausführen wenn Datei direkt gestartet wird
if __name__ == "__main__":
    run()

import time
print("Anki task 2 check")
time.sleep(3)