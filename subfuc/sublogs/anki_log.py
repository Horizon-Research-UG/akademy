import inspect

# create_log_file

dateiname = "anki_logn.txt"

def create_log_file():
    try:
        with open(dateiname, "x") as file:
            file.write("Anki log\n")
            file.write("=====================\n")
    except FileExistsError:
        pass

create_log_file()

# prepend new entries (newest at top)
import datetime
from itertools import count
import time
def count_calls():
    try:
        with open(dateiname, "r") as file:
            lines = file.readlines()
            count = len(lines) - 2  # Subtract header lines
    except FileNotFoundError:
        print("Datei nicht gefunden")
        time.sleep(2)  # Kurze Pause, um sicherzustellen, dass die Datei erstellt wird
        count = 0
        lines = []
    
    count += 1
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # old: new_entry = f"Aufruf: {count} - Datum: {date}\n"

### 
# bei new entry - add calling script
    # Gehe 2 Ebenen zurück: count_calls() <- run() <- eigentliches_programm.py
    calling_script = inspect.getframeinfo(inspect.currentframe().f_back.f_back).filename
    #what = #only the last name of the skript
    what = calling_script.split("/")[-1].split("\\")[-1]  # Handle
    new_entry = f"call: {count} - date: {date} - what: {what} - Script: {calling_script}\n"

    # Neue Einträge OBEN einfügen (nach Header)
    if len(lines) >= 2:
        # Header behalten, neuen Eintrag nach Header einfügen
        header = lines[:2]  # "Log Datei" und "============="
        old_entries = lines[2:]  # Alte Einträge
        new_content = header + [new_entry] + old_entries
    else:
        # Falls keine Header da sind
        new_content = [new_entry]
    
    # Datei komplett neu schreiben
    with open(dateiname, "w") as file:
        file.writelines(new_content)
    
    return count

def run():
    """Hauptfunktion zum Starten des Logging"""
    create_log_file()
    count_calls()
    
# Nur ausführen wenn Datei direkt gestartet wird
if __name__ == "__main__":
    run()

run()

import time
print("Anki tast check")
time.sleep(3)