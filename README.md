# 🎯 Betting Tracker

A desktop application for tracking sports bets, built in Python with a clean layered architecture and a custom dark-themed UI.

> Personal project by **Florian** — built from scratch as a portfolio piece.

---

## Features

- **Bet tracking** — log single bets and accumulators with full details
- **Accumulator builder** — dedicated popup for building multi-leg accumulators
- **Bank management** — track your starting bank, deposits, withdrawals, and current balance
- **API-based predictions** — fetches match predictions from an external sports API
- **Statistics & charts** — visualize profit/loss over time using matplotlib
- **Dark themed UI** — custom titlebar, no default OS window decorations (`overrideredirect`)
- **Persistent storage** — data saved locally in JSON files

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Python `tkinter` |
| Charts | `matplotlib` |
| Data | JSON (local storage) |
| Predictions | External sports API |
| Build | PyInstaller |

---

## Architecture

The project follows a **layered architecture**:

```
ui/           → all tkinter windows and widgets
repository/   → data access (read/write JSON files)
domain/       → data models (Bet, Accumulator, Bank)
business/     → logic layer (statistics, filtering, validation)
main.py       → entry point
```

This separation keeps the UI layer completely independent from business logic — changes to one layer don't affect the others.

---

## Getting Started

**Requirements:** Python 3.10+

```bash
# Clone the repo
git clone https://github.com/7l0r1an/betting-tracker.git
cd betting-tracker

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

## Build (standalone .exe)

```bash
pyinstaller BettingTracker.spec
```

Output will be in the `dist/` folder.

---

## Project Structure

```
betting-tracker/
├── ui/                  # tkinter windows & widgets
├── repository/          # JSON data access
├── domain/              # data models
├── business/            # logic & statistics
├── main.py              # entry point
├── bank.json            # bank state (demo data)
├── pariuri.json         # bets (demo data)
├── accumulatori.json    # accumulators (demo data)
└── requirements.txt
```

---

## Author

**Florian** — [github.com/7l0r1an](https://github.com/7l0r1an)
