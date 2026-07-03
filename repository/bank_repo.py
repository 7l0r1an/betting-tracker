import json

FILENAME = "bank.json"

def load_bank():
    """
    Ce face:
        Incarca datele bankului din fisierul JSON.

    Variabile:
        FILENAME: numele fisierului de stocare.

    Erori:
        Daca fisierul nu exista returneaza o structura implicita
        {"buget_initial": 0, "tranzactii": []}. Propaga JSONDecodeError daca
        fisierul e corupt.
    """
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"buget_initial": 0, "tranzactii": []}

def save_bank(data):
    """
    Ce face:
        Scrie datele bankului in fisierul JSON.

    Variabile:
        data: dictionarul cu datele bankului.

    Erori:
        Propaga erorile de I/O la scrierea fisierului.
    """
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def set_buget(suma):
    """
    Ce face:
        Seteaza bugetul initial in bank si salveaza.

    Variabile:
        suma: noua valoare a bugetului initial.
        data: datele curente ale bankului.

    Erori:
        Propaga erorile de I/O la salvare.
    """
    data = load_bank()
    data["buget_initial"] = suma
    save_bank(data)

def add_tranzactie(descriere, suma):
    """
    Ce face:
        Adauga o tranzactie (descriere + suma) in lista de tranzactii si salveaza.

    Variabile:
        descriere: textul tranzactiei.
        suma: valoarea tranzactiei.
        data: datele curente ale bankului.

    Erori:
        Ridica KeyError daca datele bankului nu contin cheia "tranzactii".
    """
    data = load_bank()
    data["tranzactii"].append({
        "descriere": descriere,
        "suma": suma
    })
    save_bank(data)

def get_buget_curent():
    """
    Ce face:
        Calculeaza bugetul curent adunand la bugetul initial toate sumele
        tranzactiilor.

    Variabile:
        data: datele bankului.
        total: bugetul acumulat.

    Erori:
        Ridica KeyError daca lipsesc "buget_initial" sau "tranzactii".
    """
    data = load_bank()
    total = data["buget_initial"]
    for t in data["tranzactii"]:
        total += t["suma"]
    return round(total, 2)
