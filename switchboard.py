import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from pathlib import Path

# Neutral färgpalett
BG_COLOR = "#212121"
FG_COLOR = "#E0E0E0"
ACCENT_BLUE = "#2196F3"
ACCENT_GREEN = "#4CAF50"
BUTTON_GRAY = "#424242"
WHITE_CLEAN = "#FFFFFF"

class AISwitchboard:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Manager")
        self.root.geometry("320x480")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-topmost", True)

        # Header
        tk.Label(root, text="AI SESSION MANAGER", font=('Segoe UI', 12, 'bold'), 
                 bg=BG_COLOR, fg=ACCENT_BLUE).pack(pady=20)

        # 1. SNAPSHOT SEKTION
        tk.Button(root, text="📸 1. COPY HANDOVER PROMPT", command=self.copy_prompt, 
                  bg=BUTTON_GRAY, fg=WHITE_CLEAN, font=('Segoe UI', 9, 'bold'), 
                  width=30, height=2, relief="flat").pack(pady=5)
        
        tk.Label(root, text="Updates CLAUDE.md & creates snapshot", 
                 bg=BG_COLOR, fg="#888", font=('Segoe UI', 8)).pack()

        # 2. SENTRY SEKTION
        tk.Frame(root, height=1, bg="#333").pack(fill="x", padx=30, pady=20)
        
        tk.Label(root, text="RESET TIME (H:M):", bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 9)).pack()
        self.time_entry = tk.Entry(root, width=12, justify='center', bg="#333", fg=WHITE_CLEAN, 
                                   insertbackground=WHITE_CLEAN, relief="flat")
        self.time_entry.pack(pady=8)

        tk.Button(root, text="⏳ 2. ACTIVATE SENTRY", command=self.start_sentry, 
                  bg=BUTTON_GRAY, fg=WHITE_CLEAN, width=30, relief="flat").pack(pady=5)

        # 3. MIGRATION SEKTION
        tk.Label(root, text="--- SWITCH AGENT ---", bg=BG_COLOR, fg="#888", font=('Segoe UI', 8, 'bold')).pack(pady=15)

        tk.Button(root, text="GEMINI (WITH CONTEXT)", command=lambda: self.migrate("gemini"), 
                  bg="#1A73E8", fg=WHITE_CLEAN, width=30, height=2, relief="flat").pack(pady=5)
        
        tk.Button(root, text="AIDER (WITH CONTEXT)", command=lambda: self.migrate("aider"), 
                  bg=ACCENT_GREEN, fg=WHITE_CLEAN, width=30, height=2, relief="flat").pack(pady=5)

    def copy_prompt(self):
        prompt = (
            "Please update the 'Current Status' in CLAUDE.md with our progress and next steps. "
            "Then create a context_snapshot.md with technical details for the next agent."
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        messagebox.showinfo("Clipboard", "Handover prompt copied to clipboard!")

    def get_context(self):
        path = Path("CLAUDE.md")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return f.read().replace('"', '\\"').replace('\n', ' ')
        return "No CLAUDE.md found."

    def start_sentry(self):
        t = self.time_entry.get()
        if ":" in t:
            try:
                # Vi tvingar den att använda Python 3.12 som vi just installerade
                subprocess.Popen(["py", "-3.12", "sentry.py", t])
                messagebox.showinfo("Sentry", f"Monitoring started for {t}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not start sentry.py: {e}")
        else:
            messagebox.showwarning("Input Error", "Please use H:M format (e.g. 3:45)")

    def migrate(self, agent):
        context = self.get_context()
        # Vi skickar med kontexten direkt i start-kommandot
        msg = f"CONTEXT FROM CLAUDE.MD: {context}"
        
        if agent == "gemini":
            # Startar Aider med Gemini-modell direkt
            cmd = f"aider --model gemini/gemini-2.0-flash --message \"{msg}\""
        else:
            cmd = f"aider --message \"{msg}\""

        os.system(f"start cmd /k \"{cmd}\"")

if __name__ == "__main__":
    root = tk.Tk()
    app = AISwitchboard(root)
    root.mainloop()