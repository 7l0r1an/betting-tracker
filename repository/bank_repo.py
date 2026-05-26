# bank_repo.py
import json

FILENAME = "bank.json"

def load_bank():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"buget_initial": 0, "tranzactii": []}

def save_bank(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def set_buget(suma):
    data = load_bank()
    data["buget_initial"] = suma
    save_bank(data)

def add_tranzactie(descriere, suma):
    data = load_bank()
    data["tranzactii"].append({
        "descriere": descriere,
        "suma": suma
    })
    save_bank(data)

def get_buget_curent():
    data = load_bank()
    total = data["buget_initial"]
    for t in data["tranzactii"]:
        total += t["suma"]
    return round(total, 2)