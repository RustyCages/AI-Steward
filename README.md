🚀 AI-Steward: The Claude-Code Safety Net
AI-Steward is a lightweight, cross-platform control panel designed to solve the "AI Cooldown" problem. When Claude Code hits its credit limit or rate limits, AI-Steward helps you seamlessly transition your work to Gemini or Aider without losing context.

✨ Features
🔄 Agent Switcher: Instantly jump from Claude to Gemini (via Aider) while carrying over your project's current state.

🧠 Smart Context: Automatically retrieves context from Mnemo Cortex or falls back to your CLAUDE.md file.

⏳ AI-Sentry: A built-in cooldown timer that monitors your rate limits and notifies you exactly when your preferred agent is ready to work again.

📸 Snapshot Prompt: One-click copy for handover instructions to ensure your next AI session starts exactly where the last one ended.

🖥️ Stay-on-Top UI: A clean, dark-mode dashboard that stays visible while you code.

🛠️ Installation
1. Prerequisites
Python 3.12+ (Stable version recommended)

Node.js (For Claude Code)

Aider (pip install aider-chat)

2. Setup
Clone the repository to your local machine:

PowerShell
git clone https://github.com/YOUR_USERNAME/AI-Steward.git
cd AI-Steward
3. Configure Environment
Set your Google API Key for Gemini access:

PowerShell
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your_key_here', 'User')
(Restart your terminal/IDE after setting the variable)

🚀 How to Use
Start the Steward: Run python switchboard.py (or use the provided .bat shortcut).

During AI Cooldown: If Claude hits a limit, click "COPY HANDOVER PROMPT" and paste it into Claude to save your progress.

The Handover: Click "GEMINI (WITH CONTEXT)". A new terminal will open with Aider/Gemini pre-loaded with your latest project details.

The Sentry: Set your reset time (e.g., 2:50) and click "ACTIVATE SENTRY". You can now focus on other tasks until the notification pings you at 19:00.

🧩 Planned Integrations
[ ] Full Mnemo Cortex semantic memory support.

[ ] Automated git-commit snapshots during handover.

[ ] Multiple model profiles (Flash vs. Pro).

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
