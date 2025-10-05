#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TimeQuest NeuroGames - Game of Three v0.1
Active Recall + Spaced Repetition + Feedback Loop System
Zauberhafte Lern-Software für 26-Jährige
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
from PIL import Image, ImageTk, ImageGrab
import random

# Log-System importieren
try:
    from log import log
except ImportError:
    def log(nachricht):
        print(f"[LOG] {nachricht}")

class NeuroGameItem:
    """Ein einzelnes Lern-Item mit allen Daten"""
    def __init__(self, prompt="", answer="", image_path=""):
        self.id = f"item_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}"
        self.prompt = prompt  # Frage/Aufgabe
        self.answer = answer  # Antwort/Lösung
        self.image_path = image_path  # Pfad zum Bild (optional)
        self.last_review = None  # Letztes Review-Datum
        self.interval_days = 1  # Wiederholungsintervall in Tagen
        self.ease_factor = 2.5  # SM2 Algorithmus Faktor
        self.repetitions = 0  # Anzahl erfolgreicher Wiederholungen
        self.feedback_log = []  # Liste aller Bewertungen
        self.created_at = datetime.now().isoformat()
        
    def to_dict(self):
        """Konvertiert Item zu Dictionary für JSON-Speicherung"""
        return {
            'id': self.id,
            'prompt': self.prompt,
            'answer': self.answer,
            'image_path': self.image_path,
            'last_review': self.last_review.isoformat() if self.last_review else None,
            'interval_days': self.interval_days,
            'ease_factor': self.ease_factor,
            'repetitions': self.repetitions,
            'feedback_log': self.feedback_log,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Erstellt Item aus Dictionary"""
        item = cls(data['prompt'], data['answer'], data.get('image_path', ''))
        item.id = data['id']
        item.last_review = datetime.fromisoformat(data['last_review']) if data['last_review'] else None
        item.interval_days = data.get('interval_days', 1)
        item.ease_factor = data.get('ease_factor', 2.5)
        item.repetitions = data.get('repetitions', 0)
        item.feedback_log = data.get('feedback_log', [])
        item.created_at = data.get('created_at', datetime.now().isoformat())
        return item
    
    def is_due(self):
        """Prüft ob Item zur Wiederholung fällig ist"""
        if not self.last_review:
            return True  # Neues Item ist immer fällig
        
        due_date = self.last_review + timedelta(days=self.interval_days)
        return datetime.now() >= due_date
    
    def update_after_review(self, feedback_score):
        """Aktualisiert Item nach Review (SM2 Algorithmus Light)
        feedback_score: 1=Schwer, 2=Mittel, 3=Gut, 4=Sehr gut
        """
        self.last_review = datetime.now()
        self.feedback_log.append({
            'timestamp': datetime.now().isoformat(),
            'score': feedback_score,
            'interval_before': self.interval_days
        })
        
        if feedback_score >= 3:  # Gut oder Sehr gut
            self.repetitions += 1
            if self.repetitions == 1:
                self.interval_days = 1
            elif self.repetitions == 2:
                self.interval_days = 6
            else:
                self.interval_days = int(self.interval_days * self.ease_factor)
                
            # Ease Factor anpassen
            if feedback_score == 4:  # Sehr gut
                self.ease_factor = min(self.ease_factor + 0.1, 3.0)
            
        else:  # Schwer oder Mittel
            self.repetitions = 0
            self.interval_days = max(1, int(self.interval_days * 0.6))
            if feedback_score == 1:  # Schwer
                self.ease_factor = max(self.ease_factor - 0.2, 1.3)


class TimeQuestNeuroGame:
    """Hauptklasse für die TimeQuest NeuroGame Software"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.items = []  # Liste aller Lern-Items
        self.current_item = None  # Aktuell zu lernendes Item
        self.data_file = "neurogame_data.json"
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Erstellt die Benutzeroberfläche"""
        self.root.title("🎮 TimeQuest NeuroGames - Game of Three v0.1")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Style konfigurieren
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#1a1a2e', foreground='#eee')
        style.configure('Prompt.TLabel', font=('Arial', 12), background='#1a1a2e', foreground='#eee')
        style.configure('Magic.TButton', font=('Arial', 10, 'bold'))
        
        # Haupt-Container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titel
        title_label = ttk.Label(self.main_frame, 
                               text="🧠⚡ TIMEQUEST NEUROGAMES ⚡🧠", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Haupt-Menü Frame
        self.menu_frame = ttk.Frame(self.main_frame)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_menu_ui()
        
        # Lern-Session Frame (versteckt)
        self.session_frame = ttk.Frame(self.main_frame)
        
        # Dashboard Frame (versteckt)
        self.dashboard_frame = ttk.Frame(self.main_frame)
        
    def create_menu_ui(self):
        """Erstellt das Hauptmenü"""
        # Status-Info
        status_text = f"📚 Items gespeichert: {len(self.items)}\n"
        due_items = [item for item in self.items if item.is_due()]
        status_text += f"⏰ Zur Wiederholung fällig: {len(due_items)}"
        
        status_label = ttk.Label(self.menu_frame, text=status_text, style='Prompt.TLabel')
        status_label.pack(pady=20)
        
        # Buttons
        button_frame = ttk.Frame(self.menu_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="➕ Neues Item hinzufügen", 
                  command=self.show_add_item_dialog, style='Magic.TButton').pack(pady=10, fill=tk.X)
        
        ttk.Button(button_frame, text="🧠 Lern-Session starten", 
                  command=self.start_learning_session, style='Magic.TButton').pack(pady=10, fill=tk.X)
        
        ttk.Button(button_frame, text="📊 Dashboard anzeigen", 
                  command=self.show_dashboard, style='Magic.TButton').pack(pady=10, fill=tk.X)
        
        ttk.Button(button_frame, text="💾 Daten speichern", 
                  command=self.save_data, style='Magic.TButton').pack(pady=10, fill=tk.X)
    
    def show_add_item_dialog(self):
        """Dialog zum Hinzufügen neuer Items"""
        dialog = tk.Toplevel(self.root)
        dialog.title("✨ Neues Lern-Item erstellen")
        dialog.geometry("600x500")
        dialog.configure(bg='#1a1a2e')
        
        # Prompt/Frage
        ttk.Label(dialog, text="🎯 Frage/Aufgabe:", style='Prompt.TLabel').pack(pady=10)
        prompt_text = tk.Text(dialog, height=3, width=60, font=('Arial', 10))
        prompt_text.pack(pady=5)
        
        # Antwort
        ttk.Label(dialog, text="✅ Antwort/Lösung:", style='Prompt.TLabel').pack(pady=10)
        answer_text = tk.Text(dialog, height=4, width=60, font=('Arial', 10))
        answer_text.pack(pady=5)
        
        # Bild-Upload
        image_path_var = tk.StringVar()
        ttk.Label(dialog, text="🖼️ Bild (optional):", style='Prompt.TLabel').pack(pady=10)
        
        image_frame = ttk.Frame(dialog)
        image_frame.pack(pady=5)
        
        ttk.Entry(image_frame, textvariable=image_path_var, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(image_frame, text="📁 Durchsuchen", 
                  command=lambda: self.select_image(image_path_var)).pack(side=tk.LEFT, padx=2)
        ttk.Button(image_frame, text="📋 Aus Zwischenablage", 
                  command=lambda: self.paste_from_clipboard(image_path_var)).pack(side=tk.LEFT, padx=2)
        
        # Bild-Vorschau Frame
        preview_frame = ttk.Frame(dialog)
        preview_frame.pack(pady=10)
        
        self.preview_label = ttk.Label(preview_frame, text="📷 Bild-Vorschau erscheint hier")
        self.preview_label.pack()
        
        # Callback für Entry-Änderungen, um Vorschau zu aktualisieren
        image_path_var.trace('w', lambda *args: self.update_image_preview(image_path_var.get()))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def save_item():
            prompt = prompt_text.get(1.0, tk.END).strip()
            answer = answer_text.get(1.0, tk.END).strip()
            image_path = image_path_var.get().strip()
            
            if not prompt or not answer:
                messagebox.showerror("Fehler", "Bitte Frage und Antwort eingeben!")
                return
            
            item = NeuroGameItem(prompt, answer, image_path)
            self.items.append(item)
            self.save_data()
            
            log(f"Neues Item erstellt: {item.id}")
            messagebox.showinfo("Erfolg", "✨ Item erfolgreich erstellt!")
            dialog.destroy()
            self.refresh_menu()
        
        ttk.Button(button_frame, text="💾 Speichern", command=save_item).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ Abbrechen", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def select_image(self, var):
        """Datei-Dialog für Bildauswahl"""
        filename = filedialog.askopenfilename(
            title="Bild auswählen",
            filetypes=[("Bilder", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if filename:
            var.set(filename)
    
    def paste_from_clipboard(self, var):
        """Fügt Bild aus Zwischenablage ein"""
        try:
            # Bild aus Zwischenablage holen
            clipboard_image = ImageGrab.grabclipboard()
            
            if clipboard_image is None:
                messagebox.showwarning("Zwischenablage leer", 
                                     "❌ Kein Bild in der Zwischenablage gefunden!\n\n💡 Tipp: Kopieren Sie ein Bild (Strg+C) und versuchen Sie es erneut.")
                return
            
            # Temporären Ordner für Clipboard-Bilder erstellen
            clipboard_dir = "clipboard_images"
            if not os.path.exists(clipboard_dir):
                os.makedirs(clipboard_dir)
            
            # Dateiname generieren
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{clipboard_dir}/clipboard_{timestamp}.png"
            
            # Bild speichern
            clipboard_image.save(filename, "PNG")
            var.set(filename)
            
            messagebox.showinfo("Erfolg", f"✅ Bild aus Zwischenablage eingefügt!\n📁 Gespeichert als: {filename}")
            log(f"Bild aus Zwischenablage eingefügt: {filename}")
            
        except Exception as e:
            log(f"Fehler beim Einfügen aus Zwischenablage: {e}")
            messagebox.showerror("Fehler", f"❌ Fehler beim Einfügen:\n{e}\n\n💡 Stellen Sie sicher, dass sich ein Bild in der Zwischenablage befindet.")
    
    def update_image_preview(self, image_path):
        """Aktualisiert die Bildvorschau"""
        try:
            if image_path and os.path.exists(image_path):
                # Bild laden und Vorschau erstellen
                image = Image.open(image_path)
                
                # Größe für Vorschau anpassen (max 200x150)
                image.thumbnail((200, 150))
                photo = ImageTk.PhotoImage(image)
                
                # Vorschau anzeigen
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo  # Referenz behalten
                
            else:
                # Keine Vorschau
                self.preview_label.config(image="", text="📷 Bild-Vorschau erscheint hier")
                
        except Exception as e:
            self.preview_label.config(image="", text="❌ Bild konnte nicht geladen werden")
            log(f"Fehler bei Bildvorschau: {e}")
    
    def start_learning_session(self):
        """Startet eine Lern-Session mit fälligen Items"""
        due_items = [item for item in self.items if item.is_due()]
        
        if not due_items:
            messagebox.showinfo("Info", "🎉 Alle Items sind gelernt! Keine Wiederholungen fällig.")
            return
        
        self.learning_queue = due_items.copy()
        random.shuffle(self.learning_queue)  # Zufällige Reihenfolge
        
        self.menu_frame.pack_forget()
        self.create_session_ui()
        self.session_frame.pack(fill=tk.BOTH, expand=True)
        
        self.next_item()
    
    def create_session_ui(self):
        """Erstellt die Lern-Session Oberfläche"""
        # Session-Titel
        self.session_title = ttk.Label(self.session_frame, 
                                      text="🧠 ACTIVE RECALL SESSION", 
                                      style='Title.TLabel')
        self.session_title.pack(pady=20)
        
        # Progress-Info
        self.progress_label = ttk.Label(self.session_frame, text="", style='Prompt.TLabel')
        self.progress_label.pack(pady=10)
        
        # Item-Anzeige Frame
        self.item_display_frame = ttk.Frame(self.session_frame)
        self.item_display_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Bild-Label (falls vorhanden)
        self.image_label = ttk.Label(self.item_display_frame)
        
        # Prompt/Frage-Label
        self.prompt_label = ttk.Label(self.item_display_frame, text="", 
                                     style='Prompt.TLabel', wraplength=600)
        
        # Antwort-Frame (versteckt)
        self.answer_frame = ttk.Frame(self.item_display_frame)
        self.answer_label = ttk.Label(self.answer_frame, text="", 
                                     style='Prompt.TLabel', wraplength=600)
        self.answer_label.pack(pady=20)
        
        # Feedback-Buttons (versteckt)
        self.feedback_frame = ttk.Frame(self.item_display_frame)
        self.create_feedback_buttons()
        
        # Action-Button
        self.action_button = ttk.Button(self.item_display_frame, 
                                       text="🔮 Antwort anzeigen", 
                                       command=self.show_answer,
                                       style='Magic.TButton')
        
        # Zurück-Button
        ttk.Button(self.session_frame, text="🏠 Zurück zum Menü", 
                  command=self.back_to_menu).pack(pady=20)
    
    def create_feedback_buttons(self):
        """Erstellt die Feedback-Bewertungsbuttons"""
        ttk.Label(self.feedback_frame, text="🎯 Wie schwer war das für Sie?", 
                 style='Prompt.TLabel').pack(pady=10)
        
        button_frame = ttk.Frame(self.feedback_frame)
        button_frame.pack(pady=10)
        
        # Feedback-Buttons mit Emojis und Farben
        feedback_buttons = [
            ("🔴 Schwer", 1, "#ff4757"),
            ("🟠 Mittel", 2, "#ffa502"),
            ("🟢 Gut", 3, "#2ed573"),
            ("🔵 Sehr gut", 4, "#1e90ff")
        ]
        
        for text, score, color in feedback_buttons:
            btn = tk.Button(button_frame, text=text, 
                           command=lambda s=score: self.give_feedback(s),
                           bg=color, fg='white', font=('Arial', 10, 'bold'),
                           relief=tk.RAISED, bd=3)
            btn.pack(side=tk.LEFT, padx=5, pady=5, ipadx=10, ipady=5)
    
    def next_item(self):
        """Zeigt das nächste Item der Lern-Session"""
        if not self.learning_queue:
            self.finish_session()
            return
        
        self.current_item = self.learning_queue.pop(0)
        self.show_question_phase()
        
        # Progress aktualisieren
        remaining = len(self.learning_queue)
        total = len([item for item in self.items if item.is_due()])
        progress_text = f"📊 Fortschritt: {total - remaining}/{total} Items"
        self.progress_label.config(text=progress_text)
    
    def show_question_phase(self):
        """Zeigt die Frage-Phase (Active Recall)"""
        # Frames zurücksetzen
        self.answer_frame.pack_forget()
        self.feedback_frame.pack_forget()
        
        # Bild anzeigen (falls vorhanden)
        if self.current_item.image_path and os.path.exists(self.current_item.image_path):
            try:
                image = Image.open(self.current_item.image_path)
                image.thumbnail((400, 300))
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Referenz behalten
                self.image_label.pack(pady=10)
            except:
                self.image_label.pack_forget()
        else:
            self.image_label.pack_forget()
        
        # Frage anzeigen
        self.prompt_label.config(text=f"❓ {self.current_item.prompt}")
        self.prompt_label.pack(pady=20)
        
        # Action-Button konfigurieren
        self.action_button.config(text="🔮 Antwort anzeigen", command=self.show_answer)
        self.action_button.pack(pady=20)
    
    def show_answer(self):
        """Zeigt die Antwort und Feedback-Optionen"""
        # Antwort anzeigen
        self.answer_label.config(text=f"✅ {self.current_item.answer}")
        self.answer_frame.pack(pady=20)
        
        # Feedback-Buttons anzeigen
        self.feedback_frame.pack(pady=20)
        
        # Action-Button verstecken
        self.action_button.pack_forget()
    
    def give_feedback(self, score):
        """Verarbeitet Feedback und geht zum nächsten Item"""
        self.current_item.update_after_review(score)
        self.save_data()
        
        # Feedback-Log
        score_texts = {1: "Schwer", 2: "Mittel", 3: "Gut", 4: "Sehr gut"}
        log(f"Feedback für {self.current_item.id}: {score_texts[score]} - Nächstes Intervall: {self.current_item.interval_days} Tage")
        
        self.next_item()
    
    def finish_session(self):
        """Beendet die Lern-Session"""
        messagebox.showinfo("Session beendet", "🎉 Gratulation! Alle fälligen Items wiederholt!")
        self.back_to_menu()
    
    def show_dashboard(self):
        """Zeigt das Dashboard mit Statistiken"""
        self.menu_frame.pack_forget()
        self.create_dashboard_ui()
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_dashboard_ui(self):
        """Erstellt das Dashboard"""
        # Dashboard-Titel
        ttk.Label(self.dashboard_frame, text="📊 NEUROGAME DASHBOARD", 
                 style='Title.TLabel').pack(pady=20)
        
        # Statistiken
        stats_frame = ttk.Frame(self.dashboard_frame)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Berechne Statistiken
        total_items = len(self.items)
        due_items = len([item for item in self.items if item.is_due()])
        total_reviews = sum(len(item.feedback_log) for item in self.items)
        
        stats_text = f"""
📚 Gesamt Items: {total_items}
⏰ Fällige Items: {due_items}
🔄 Gesamt Reviews: {total_reviews}
🧠 Memory Vault: {total_items - due_items} Items stabilisiert
        """
        
        ttk.Label(stats_frame, text=stats_text, style='Prompt.TLabel').pack(pady=20)
        
        # Item-Liste
        if self.items:
            ttk.Label(stats_frame, text="📋 Ihre Items:", style='Prompt.TLabel').pack(pady=10)
            
            # Scrollbare Liste
            list_frame = ttk.Frame(stats_frame)
            list_frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                               font=('Arial', 10), height=10)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=listbox.yview)
            
            for item in self.items:
                status = "🔴 Fällig" if item.is_due() else f"✅ Nächste Wiederholung in {item.interval_days} Tagen"
                listbox.insert(tk.END, f"{item.prompt[:50]}... - {status}")
        
        # Zurück-Button
        ttk.Button(self.dashboard_frame, text="🏠 Zurück zum Menü", 
                  command=self.back_to_menu).pack(pady=20)
    
    def back_to_menu(self):
        """Kehrt zum Hauptmenü zurück"""
        self.session_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        
        # Dashboard-UI löschen für Refresh
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        
        self.refresh_menu()
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
    
    def refresh_menu(self):
        """Aktualisiert das Hauptmenü"""
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        self.create_menu_ui()
    
    def save_data(self):
        """Speichert alle Daten in JSON-Datei"""
        try:
            data = {
                'items': [item.to_dict() for item in self.items],
                'last_save': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            log(f"Daten gespeichert: {len(self.items)} Items")
            
        except Exception as e:
            log(f"Fehler beim Speichern: {e}")
            messagebox.showerror("Fehler", f"Speichern fehlgeschlagen: {e}")
    
    def load_data(self):
        """Lädt Daten aus JSON-Datei"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.items = [NeuroGameItem.from_dict(item_data) 
                             for item_data in data.get('items', [])]
                
                log(f"Daten geladen: {len(self.items)} Items")
        
        except Exception as e:
            log(f"Fehler beim Laden: {e}")
            messagebox.showerror("Fehler", f"Laden fehlgeschlagen: {e}")
    
    def run(self):
        """Startet die Anwendung"""
        log("TimeQuest NeuroGames gestartet")
        self.root.mainloop()


def main():
    """Hauptfunktion"""
    try:
        app = TimeQuestNeuroGame()
        app.run()
    except Exception as e:
        log(f"Kritischer Fehler: {e}")
        print(f"❌ Kritischer Fehler: {e}")


if __name__ == "__main__":
    main()