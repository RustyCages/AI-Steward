import time
import sys
import os
from pathlib import Path

FLAG_FILE = Path.home() / ".claude_ready_flag"

def send_notification(message):
    title = "AI Sentry: Claude Update"
    if sys.platform == "darwin": # macOS
        os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')
    elif sys.platform == "win32": # Windows
        os.system(f'powershell -Command "New-BurntToastNotification -Text \'{title}\', \'{message}\'"')

def start_timer(time_str):
    try:
        hours, minutes = map(int, time_str.split(':'))
        total_seconds = (hours * 3600) + (minutes * 60)
        print(f"[*] Bevakar Claude... Återställning om {hours}h {minutes}m.")
        time.sleep(total_seconds)
        FLAG_FILE.touch()
        send_notification("Claude har fyllt på sina krediter! Dags att byta tillbaka?")
    except Exception as e:
        print(f"Fel: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_timer(sys.argv[1])