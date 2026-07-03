import json
from domain.bet import Bet

FILENAME = "pariuri.json"

def load_bets():
    """
    Ce face:
        Incarca pariurile simple din fisierul JSON si le transforma in obiecte Bet.

    Variabile:
        FILENAME: numele fisierului de stocare.
        data: continutul JSON deserializat (lista de dictionare).

    Erori:
        Daca fisierul nu exista returneaza lista goala. Ridica KeyError daca un
        dictionar nu contine "stake"/"match"/"odds"/"result" sau ValueError daca
        stake/odds nu pot fi convertite in float. Propaga JSONDecodeError.
    """
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        return [Bet(float(d["stake"]), d["match"], float(d["odds"]),
                    d["result"], d.get("bet_type"), d.get("date")) for d in data]
    except FileNotFoundError:
        return []

def save_bets(bets):
    """
    Ce face:
        Serializeaza lista de pariuri si o scrie in fisierul JSON.

    Variabile:
        bets: lista de obiecte Bet de salvat.
        data: reprezentarea lor ca lista de dictionare.

    Erori:
        Propaga erorile de I/O la scrierea fisierului.
    """
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
    """
    Ce face:
        Sterge pariul de la pozitia index si rescrie fisierul.

    Variabile:
        index: pozitia pariului de sters.
        bets: lista curenta de pariuri.

    Erori:
        Daca index este in afara intervalului nu sterge nimic si afiseaza
        "Index invalid!".
    """
    bets = load_bets()
    if 0 <= index < len(bets):
        bets.pop(index)
        save_bets(bets)
    else:
        print("Index invalid!")
