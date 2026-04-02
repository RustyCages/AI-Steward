import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from pathlib import Path

# --- CONFIGURATION ---
BG_COLOR = "#212121"
FG_COLOR = "#E0E0E0"
ACCENT_BLUE = "#2196F3"
ACCENT_GREEN = "#4CAF50"
BUTTON_GRAY = "#424242"
WHITE_CLEAN = "#FFFFFF"

class AISwitchboard:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Steward Manager")
        self.root.geometry("320x520")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-topmost", True)

        # Header
        tk.Label(root, text="AI STEWARD", font=('Segoe UI', 14, 'bold'), 
                 bg=BG_COLOR, fg=ACCENT_BLUE).pack(pady=15)

        # 1. SNAPSHOT / HANDOVER SECTION
        tk.Button(root, text="📸 1. COPY HANDOVER PROMPT", command=self.copy_prompt, 
                  bg=BUTTON_GRAY, fg=WHITE_CLEAN, font=('Segoe UI', 9, 'bold'), 
                  width=30, height=2, relief="flat").pack(pady=5)
        
        tk.Label(root, text="Updates CLAUDE.md & prepares handover", 
                 bg=BG_COLOR, fg="#888", font=('Segoe UI', 8)).pack()

        # 2. SENTRY SECTION (TIMER)
        tk.Frame(root, height=1, bg="#333").pack(fill="x", padx=30, pady=15)
        
        tk.Label(root, text="COOLDOWN TIMER (H:M):", bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 9)).pack()
        self.time_entry = tk.Entry(root, width=12, justify='center', bg="#333", fg=WHITE_CLEAN, 
                                   insertbackground=WHITE_CLEAN, relief="flat")
        self.time_entry.insert(0, "0:00")
        self.time_entry.pack(pady=8)

        tk.Button(root, text="⏳ 2. ACTIVATE SENTRY", command=self.start_sentry, 
                  bg=BUTTON_GRAY, fg=WHITE_CLEAN, width=30, relief="flat").pack(pady=5)

        # 3. AGENT SWITCHING SECTION
        tk.Label(root, text="--- SWITCH AGENT ---", bg=BG_COLOR, fg="#888", font=('Segoe UI', 8, 'bold')).pack(pady=15)

        tk.Button(root, text="GEMINI (WITH MNEMO/CONTEXT)", command=lambda: self.migrate("gemini"), 
                  bg="#1A73E8", fg=WHITE_CLEAN, width=30, height=2, relief="flat").pack(pady=5)
        
        tk.Button(root, text="AIDER (WITH MNEMO/CONTEXT)", command=lambda: self.migrate("aider"), 
                  bg=ACCENT_GREEN, fg=WHITE_CLEAN, width=30, height=2, relief="flat").pack(pady=5)

        # Footer Status Bar
        self.status_label = tk.Label(root, text="System Ready", bg="#111", fg="#666", font=('Consolas', 8))
        self.status_label.pack(side="bottom", fill="x")

    def get_smart_context(self):
        """Attempts to retrieve memory from Mnemo Cortex, fallback to CLAUDE.md"""
        try:
            # Check for Mnemo Cortex CLI memory
            result = subprocess.check_output(["mnemo", "recall", "--last"], text=True)
            self.status_label.config(text="Status: Mnemo Cortex Active", fg=ACCENT_GREEN)
            return result.replace('"', '\\"').replace('\n', ' ')
        except:
            # Fallback to manual file
            path = Path("CLAUDE.md")
            if path.exists():
                self.status_label.config(text="Status: Manual Context (CLAUDE.md)", fg="#FFA500")
                with open(path, "r", encoding="utf-8") as f:
                    return f.read().replace('"', '\\"').replace('\n', ' ')
            self.status_label.config(text="Status: No Context Found", fg="#FF5252")
            return "No previous context found."

    def copy_prompt(self):
        prompt = (
            "Please update the 'Current Status' in CLAUDE.md with our progress and next steps. "
            "Then prepare a context snapshot for handover to the next agent."
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        messagebox.showinfo("AI Steward", "Handover prompt copied to clipboard!")

    def start_sentry(self):
        t = self.time_entry.get()
        if ":" in t:
            try:
                # Force Python 3.12 for Sentry logic
                subprocess.Popen(["py", "-3.12", "sentry.py", t])
                self.status_label.config(text=f"Sentry active: Trigger in {t}", fg=ACCENT_BLUE)
            except Exception as e:
                messagebox.showerror("Error", f"Could not start sentry.py: {e}")
        else:
            messagebox.showwarning("Input Error", "Please use H:M format (e.g. 2:50)")

    def migrate(self, agent):
        context = self.get_smart_context()
        msg = f"CONTINUE SESSION. CONTEXT: {context}"
        
        if agent == "gemini":
            # Using Aider with the Gemini engine
            cmd = f"aider --model gemini/gemini-2.0-flash --message \"{msg}\""
        else:
            # Standard Aider (default model)
            cmd = f"aider --message \"{msg}\""

        # Launch in a new Windows terminal
        os.system(f"start cmd /k \"{cmd}\"")

if __name__ == "__main__":
    root = tk.Tk()
    app = AISwitchboard(root)
    root.mainloop()
