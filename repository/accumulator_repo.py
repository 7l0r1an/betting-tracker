import json
from domain.accumulator import Accumulator

FILENAME = "accumulatori.json"

def load_accumulators():
    """
    Ce face:
        Incarca acumulatorii din fisierul JSON si ii transforma in obiecte
        Accumulator.

    Variabile:
        FILENAME: numele fisierului de stocare.
        data: continutul JSON deserializat (lista de dictionare).

    Erori:
        Daca fisierul nu exista returneaza lista goala. Ridica KeyError daca un
        dictionar nu contine cheile obligatorii (matches, odds_list, stake,
        result). Propaga JSONDecodeError daca fisierul e corupt.
    """
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        return [Accumulator(
            d["matches"], d["odds_list"], d["stake"],
            d["result"], d.get("match_results"),
            d.get("match_types"), d.get("date")
        ) for d in data]
    except FileNotFoundError:
        return []

def save_accumulators(accumulators):
    """
    Ce face:
        Serializeaza lista de acumulatori si o scrie in fisierul JSON.

    Variabile:
        accumulators: lista de obiecte Accumulator de salvat.
        data: reprezentarea lor ca lista de dictionare.

    Erori:
        Propaga erorile de I/O la scrierea fisierului.
    """
    data = [
        {
            "matches":       a.matches,
            "odds_list":     a.odds_list,
            "stake":         a.stake,
            "result":        a.result,
            "match_results": a.match_results,
            "match_types":   a.match_types,
            "date":          a.date
        }
        for a in accumulators
    ]
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def delete_accumulator(index):
    """
    Ce face:
        Sterge acumulatorul de la pozitia index si rescrie fisierul.

    Variabile:
        index: pozitia acumulatorului de sters.
        accs: lista curenta de acumulatori.

    Erori:
        Daca index este in afara intervalului nu se face nimic (fara exceptie).
    """
    accs = load_accumulators()
    if 0 <= index < len(accs):
        accs.pop(index)
        save_accumulators(accs)
