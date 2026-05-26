# file_repo.py
import json
from domain.bet import Bet

FILENAME = "pariuri.json"

def load_bets():
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        return [Bet(float(d["stake"]), d["match"], float(d["odds"]),
                    d["result"], d.get("bet_type"), d.get("date")) for d in data]
    except FileNotFoundError:
        return []

def save_bets(bets):
    data = [
        {
            "match":    b.match,
            "stake":    b.stake,
            "odds":     b.odds,
            "result":   b.result,
            "bet_type": b.bet_type,
            "date":     b.date
        }
        for b in bets
    ]
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def delete_bet(index):
    bets = load_bets()
    if 0 <= index < len(bets):
        bets.pop(index)
        save_bets(bets)
    else:
        print("Index invalid!")