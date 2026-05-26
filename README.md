# pomodoro-canvas
一個任務倒數計時的時鐘

# ⏱️ Prompt-Based Pomodoro Canvas

> **A Minimalist, Keyboard-Driven Desktop Pomodoro Timer Featuring Dynamic Auto-Topmost Window Scaling.**

Pomodoro Canvas is a geek-centric desktop productivity app designed for developers, researchers, and students who thrive on terminal-like workflows. Built to combat workspace clutter, this app eliminates standard UI clutter in favor of a **pure command-prompt interaction model**. The moment you start a focus session, the canvas automatically morphs into an ultra-compact, always-on-top sticker, keeping you locked in without invading your desktop estate.

---

## ✨ Key Features

* **⌨️ Pure Command-Line Control**: No clumsy buttons. Drive your entire focus workflow through fluid text commands (`/todo [task] [min]`, `/p` to pause, `/r` to resume, `/reset`).
* **📐 Dynamic Window Scaling (UX Magic)**: 
  * *Large Dashboard Mode (820x500)*: Review your monthly big-data analytics and setup tasks.
  * *Mini Sticker Mode (220x80)*: Instantly compresses upon timer ignition, hiding all clutter and focusing solely on a large, glowing countdown clock.
* **🔒 Context-Aware Auto-Topmost Lock**: The application remains non-intrusive and can be covered by browsers or IDEs while idle. However, the exact millisecond a timer begins, it triggers a system-level `-topmost` shield to guarantee visibility.
* **📊 Macaron Analytics Dashboard**: Automatically logs completed sessions to a local encrypted JSON cache (`pomo_stats.json`) and streams them into vibrant, smooth-rendering visual progress tracks.

---

## ⌨️ Command cheat sheet

| Command | Action | Visual Reaction |
| :--- | :--- | :--- |
| `/todo [task] [min]` | Initiates a customized focus block | Scales window to `220x80`, engages topmost shield |
| `/p` or `/pause` | Freezes the active countdown clock | Shifts clock typography to safety-orange `PAUSE` |
| `/r` or `/resume` | Resumes the countdown sequence | Restores macaron-yellow clock state |
| `/reset` | Aborts current timer and resets clock | Restores dashboard size, unlocks topmost shield |
| `/clear` | Wipes entire data metrics history | Prompts double-confirmation security dialog |

---

## 🛠️ Tech Stack & Architecture

* **GUI Engine**: `CustomTkinter` (Python 3.10+)
* **State Management**: Built-in Asynchronous Thread Throttling via Tkinter `.after()` loop pooling.
* **Persistence Layer**: Lightweight, automated flat-file `JSON` serialization with structural error recovery.

---

## 🚀 Getting Started

### Prerequisites

Ensure `customtkinter` is accessible within your current Python instance:

```bash
pip install customtkinter
```

## 介面
<img width="1027" height="665" alt="image" src="https://github.com/user-attachments/assets/e7ecc7ae-5644-43ce-a27a-e58318057893" />
