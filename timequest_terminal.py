#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TimeQuest NeuroGames - Terminal Version v1.0
Einfaches, modulares Active Recall System
Ohne GUI - nur Terminal
"""

import json
import os
import random
from datetime import datetime, timedelta


# =============================================================================
# DATEN-KLASSEN (Data Classes)
# =============================================================================

class LernItem:
    """Ein einzelnes Lern-Item mit Frage und Antwort"""
    
    def __init__(self, frage="", antwort=""):
        # Eindeutige ID generieren
        self.id = f"item_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}"
        
        # Inhalt
        self.frage = frage
        self.antwort = antwort
        
        # Lern-Daten
        self.letztes_review = None
        self.intervall_tage = 1
        self.wiederholungen = 0
        self.bewertungen = []  # Liste aller Bewertungen
        
        # Zeitstempel
        self.erstellt_am = datetime.now().isoformat()
    
    def ist_faellig(self):
        """Prüft ob Item zur Wiederholung fällig ist"""
        if not self.letztes_review:
            return True  # Neues Item ist immer fällig
        
        naechstes_review = self.letztes_review + timedelta(days=self.intervall_tage)
        return datetime.now() >= naechstes_review
    
    def bewerten(self, note):
        """Bewertet das Item und passt Intervall an
        note: 1=Schwer, 2=Mittel, 3=Gut, 4=Perfekt
        """
        self.letztes_review = datetime.now()
        self.bewertungen.append({
            'datum': datetime.now().isoformat(),
            'note': note
        })
        
        # Intervall anpassen basierend auf Bewertung
        if note >= 3:  # Gut oder Perfekt
            self.wiederholungen += 1
            if self.wiederholungen == 1:
                self.intervall_tage = 3
            elif self.wiederholungen == 2:
                self.intervall_tage = 7
            else:
                self.intervall_tage = int(self.intervall_tage * 2)
        else:  # Schwer oder Mittel
            self.wiederholungen = 0
            self.intervall_tage = 1
    
    def zu_dict(self):
        """Konvertiert Item zu Dictionary für Speicherung"""
        return {
            'id': self.id,
            'frage': self.frage,
            'antwort': self.antwort,
            'letztes_review': self.letztes_review.isoformat() if self.letztes_review else None,
            'intervall_tage': self.intervall_tage,
            'wiederholungen': self.wiederholungen,
            'bewertungen': self.bewertungen,
            'erstellt_am': self.erstellt_am
        }
    
    @classmethod
    def von_dict(cls, daten):
        """Erstellt Item aus Dictionary"""
        item = cls(daten['frage'], daten['antwort'])
        item.id = daten['id']
        item.letztes_review = datetime.fromisoformat(daten['letztes_review']) if daten['letztes_review'] else None
        item.intervall_tage = daten.get('intervall_tage', 1)
        item.wiederholungen = daten.get('wiederholungen', 0)
        item.bewertungen = daten.get('bewertungen', [])
        item.erstellt_am = daten.get('erstellt_am', datetime.now().isoformat())
        return item


# =============================================================================
# DATEN-MANAGER (Data Manager)
# =============================================================================

class DatenManager:
    """Verwaltet das Speichern und Laden der Lern-Items"""
    
    def __init__(self, datei_name="neurogame_daten.json"):
        self.datei_name = datei_name
        self.items = []
    
    def laden(self):
        """Lädt alle Items aus der Datei"""
        try:
            if os.path.exists(self.datei_name):
                with open(self.datei_name, 'r', encoding='utf-8') as datei:
                    daten = json.load(datei)
                    self.items = [LernItem.von_dict(item_daten) for item_daten in daten.get('items', [])]
                print(f"✅ {len(self.items)} Items geladen")
            else:
                print("📝 Neue Datenbank erstellt")
        except Exception as fehler:
            print(f"❌ Fehler beim Laden: {fehler}")
    
    def speichern(self):
        """Speichert alle Items in die Datei"""
        try:
            daten = {
                'items': [item.zu_dict() for item in self.items],
                'gespeichert_am': datetime.now().isoformat()
            }
            with open(self.datei_name, 'w', encoding='utf-8') as datei:
                json.dump(daten, datei, indent=2, ensure_ascii=False)
            print(f"✅ {len(self.items)} Items gespeichert")
        except Exception as fehler:
            print(f"❌ Fehler beim Speichern: {fehler}")
    
    def item_hinzufuegen(self, frage, antwort):
        """Fügt ein neues Item hinzu"""
        item = LernItem(frage, antwort)
        self.items.append(item)
        self.speichern()
        return item
    
    def item_loeschen(self, item_id):
        """Löscht ein Item"""
        self.items = [item for item in self.items if item.id != item_id]
        self.speichern()
    
    def item_bearbeiten(self, item_id, neue_frage, neue_antwort):
        """Bearbeitet ein vorhandenes Item"""
        for item in self.items:
            if item.id == item_id:
                item.frage = neue_frage
                item.antwort = neue_antwort
                self.speichern()
                return True
        return False
    
    def faellige_items(self):
        """Gibt alle fälligen Items zurück"""
        return [item for item in self.items if item.ist_faellig()]


# =============================================================================
# LERN-ENGINE (Learning Engine)
# =============================================================================

class LernEngine:
    """Führt Lern-Sessions durch"""
    
    def __init__(self, daten_manager):
        self.daten_manager = daten_manager
    
    def session_starten(self):
        """Startet eine Lern-Session mit fälligen Items"""
        faellige = self.daten_manager.faellige_items()
        
        if not faellige:
            print("\n🎉 Gratulation! Keine Items zur Wiederholung fällig!")
            return
        
        print(f"\n🧠 LERN-SESSION GESTARTET")
        print(f"📚 {len(faellige)} Items zu wiederholen")
        print("="*50)
        
        # Items zufällig mischen
        random.shuffle(faellige)
        
        for index, item in enumerate(faellige, 1):
            print(f"\n📊 Item {index}/{len(faellige)}")
            self.item_abfragen(item)
        
        print("\n🎉 Session beendet! Alle Items wiederholt!")
        self.daten_manager.speichern()
    
    def item_abfragen(self, item):
        """Fragt ein einzelnes Item ab (Active Recall)"""
        print(f"\n❓ FRAGE:")
        print(f"   {item.frage}")
        print("\n💭 Denken Sie über die Antwort nach...")
        
        input("   👉 Drücken Sie Enter wenn Sie bereit sind...")
        
        print(f"\n✅ ANTWORT:")
        print(f"   {item.antwort}")
        
        # Bewertung abfragen
        while True:
            print(f"\n🎯 Wie war das für Sie?")
            print("   1 = Schwer (nicht gewusst)")
            print("   2 = Mittel (unsicher)")
            print("   3 = Gut (gewusst)")
            print("   4 = Perfekt (sehr sicher)")
            
            try:
                bewertung = int(input("   👉 Ihre Bewertung (1-4): "))
                if 1 <= bewertung <= 4:
                    break
                else:
                    print("   ❌ Bitte eine Zahl zwischen 1 und 4 eingeben!")
            except ValueError:
                print("   ❌ Bitte eine gültige Zahl eingeben!")
        
        # Item bewerten und speichern
        item.bewerten(bewertung)
        
        bewertung_texte = {1: "Schwer", 2: "Mittel", 3: "Gut", 4: "Perfekt"}
        print(f"   ✅ Bewertet als: {bewertung_texte[bewertung]}")
        print(f"   ⏰ Nächste Wiederholung in {item.intervall_tage} Tagen")


# =============================================================================
# MENU-SYSTEM (Menu System)
# =============================================================================

class MenuSystem:
    """Verwaltet das Haupt-Menü und Navigation"""
    
    def __init__(self):
        self.daten_manager = DatenManager()
        self.lern_engine = LernEngine(self.daten_manager)
        
        # Daten laden
        self.daten_manager.laden()
        
        # Test-Item hinzufügen falls leer
        if not self.daten_manager.items:
            self.test_items_erstellen()
    
    def test_items_erstellen(self):
        """Erstellt Test-Items zum Ausprobieren"""
        print("📝 Erstelle Test-Items...")
        
        test_items = [
            ("Was ist Active Recall?", "Aktives Abrufen von Wissen aus dem Gedächtnis ohne Hilfsmittel"),
            ("Was bedeutet Spaced Repetition?", "Wiederholung in optimalen Zeitabständen basierend auf Vergessenskurve"),
            ("Was ist der Hauptvorteil von Feedback-Schleifen?", "Anpassung der Lernintervalle basierend auf Schwierigkeit"),
            ("Warum funktioniert TimeQuest so gut?", "Kombination aus Active Recall, Spaced Repetition und Gamification")
        ]
        
        for frage, antwort in test_items:
            self.daten_manager.item_hinzufuegen(frage, antwort)
        
        print(f"✅ {len(test_items)} Test-Items erstellt!")
    
    def haupt_menu(self):
        """Zeigt das Haupt-Menü"""
        while True:
            self.status_anzeigen()
            
            print("\n🎮 TIMEQUEST NEUROGAMES - TERMINAL VERSION")
            print("="*50)
            print("1 = 🧠 Lern-Session starten")
            print("2 = ➕ Neues Item hinzufügen")
            print("3 = 📋 Alle Items anzeigen")
            print("4 = ✏️  Item bearbeiten")
            print("5 = 🗑️  Item löschen")
            print("6 = 📊 Statistiken anzeigen")
            print("7 = 💾 Daten speichern")
            print("0 = 🚪 Beenden")
            print("="*50)
            
            wahl = input("👉 Ihre Wahl: ").strip()
            
            if wahl == "1":
                self.lern_engine.session_starten()
            elif wahl == "2":
                self.neues_item_menu()
            elif wahl == "3":
                self.items_anzeigen()
            elif wahl == "4":
                self.item_bearbeiten_menu()
            elif wahl == "5":
                self.item_loeschen_menu()
            elif wahl == "6":
                self.statistiken_anzeigen()
            elif wahl == "7":
                self.daten_manager.speichern()
            elif wahl == "0":
                print("\n👋 Auf Wiedersehen!")
                break
            else:
                print("\n❌ Ungültige Eingabe!")
            
            input("\n👉 Drücken Sie Enter um fortzufahren...")
    
    def status_anzeigen(self):
        """Zeigt aktuellen Status an"""
        total = len(self.daten_manager.items)
        faellig = len(self.daten_manager.faellige_items())
        
        print(f"\n📊 STATUS:")
        print(f"   📚 Gesamt Items: {total}")
        print(f"   ⏰ Zur Wiederholung fällig: {faellig}")
        print(f"   ✅ Gelernt: {total - faellig}")
    
    def neues_item_menu(self):
        """Menü für neues Item"""
        print(f"\n➕ NEUES ITEM ERSTELLEN")
        print("="*30)
        
        frage = input("❓ Frage eingeben: ").strip()
        if not frage:
            print("❌ Frage darf nicht leer sein!")
            return
        
        antwort = input("✅ Antwort eingeben: ").strip()
        if not antwort:
            print("❌ Antwort darf nicht leer sein!")
            return
        
        item = self.daten_manager.item_hinzufuegen(frage, antwort)
        print(f"✅ Item erstellt! ID: {item.id}")
    
    def items_anzeigen(self):
        """Zeigt alle Items an"""
        if not self.daten_manager.items:
            print("\n📝 Keine Items vorhanden!")
            return
        
        print(f"\n📋 ALLE ITEMS ({len(self.daten_manager.items)})")
        print("="*50)
        
        for index, item in enumerate(self.daten_manager.items, 1):
            status = "🔴 Fällig" if item.ist_faellig() else f"✅ OK ({item.intervall_tage}d)"
            print(f"\n{index}. [{status}] {item.frage[:40]}...")
            print(f"   💬 {item.antwort[:40]}...")
            print(f"   🔄 Wiederholungen: {item.wiederholungen}")
            print(f"   📅 ID: {item.id}")
    
    def item_bearbeiten_menu(self):
        """Menü für Item-Bearbeitung"""
        if not self.daten_manager.items:
            print("\n📝 Keine Items vorhanden!")
            return
        
        self.items_anzeigen()
        
        item_id = input("\n✏️  Item-ID zum Bearbeiten: ").strip()
        
        # Item finden
        item = None
        for i in self.daten_manager.items:
            if i.id == item_id:
                item = i
                break
        
        if not item:
            print("❌ Item nicht gefunden!")
            return
        
        print(f"\n📝 ITEM BEARBEITEN")
        print(f"Aktuelle Frage: {item.frage}")
        print(f"Aktuelle Antwort: {item.antwort}")
        
        neue_frage = input("\n❓ Neue Frage (Enter = unverändert): ").strip()
        neue_antwort = input("✅ Neue Antwort (Enter = unverändert): ").strip()
        
        if neue_frage:
            item.frage = neue_frage
        if neue_antwort:
            item.antwort = neue_antwort
        
        self.daten_manager.speichern()
        print("✅ Item aktualisiert!")
    
    def item_loeschen_menu(self):
        """Menü für Item-Löschung"""
        if not self.daten_manager.items:
            print("\n📝 Keine Items vorhanden!")
            return
        
        self.items_anzeigen()
        
        item_id = input("\n🗑️  Item-ID zum Löschen: ").strip()
        
        bestaetigung = input(f"❗ Wirklich löschen? (ja/nein): ").strip().lower()
        if bestaetigung in ['ja', 'j', 'yes', 'y']:
            self.daten_manager.item_loeschen(item_id)
            print("✅ Item gelöscht!")
        else:
            print("❌ Löschung abgebrochen!")
    
    def statistiken_anzeigen(self):
        """Zeigt detaillierte Statistiken"""
        if not self.daten_manager.items:
            print("\n📝 Keine Items vorhanden!")
            return
        
        total = len(self.daten_manager.items)
        faellig = len(self.daten_manager.faellige_items())
        total_bewertungen = sum(len(item.bewertungen) for item in self.daten_manager.items)
        
        print(f"\n📊 DETAILLIERTE STATISTIKEN")
        print("="*40)
        print(f"📚 Gesamt Items: {total}")
        print(f"⏰ Fällige Items: {faellig}")
        print(f"✅ Gelernte Items: {total - faellig}")
        print(f"🔄 Gesamt Reviews: {total_bewertungen}")
        
        if total_bewertungen > 0:
            durchschnitt = total_bewertungen / total
            print(f"📈 Durchschnitt Reviews/Item: {durchschnitt:.1f}")
        
        # Intervall-Verteilung
        print(f"\n⏱️ WIEDERHOLUNGS-INTERVALLE:")
        intervalle = {}
        for item in self.daten_manager.items:
            tage = item.intervall_tage
            intervalle[tage] = intervalle.get(tage, 0) + 1
        
        for tage in sorted(intervalle.keys()):
            print(f"   {tage} Tage: {intervalle[tage]} Items")


# =============================================================================
# HAUPT-PROGRAMM (Main Program)
# =============================================================================

def main():
    """Haupt-Funktion - Programmstart"""
    print("🎮 TimeQuest NeuroGames wird gestartet...")
    
    try:
        menu = MenuSystem()
        menu.haupt_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Programm beendet!")
    except Exception as fehler:
        print(f"\n❌ Unerwarteter Fehler: {fehler}")


if __name__ == "__main__":
    main()