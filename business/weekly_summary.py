from datetime import datetime, timedelta
from repository import file_repo, accumulator_repo
from repository.bank_repo import load_bank

def get_last_week_range():
    """
    Ce face:
        Calculeaza intervalul saptamanii trecute (luni 00:00:00 - duminica
        23:59:59) raportat la data curenta.

    Variabile:
        today: data si ora curente.
        last_monday: lunea saptamanii trecute.
        last_sunday: duminica saptamanii trecute.

    Erori:
        Nu ridica erori proprii.
    """
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    last_monday = last_monday.replace(hour=0, minute=0, second=0)
    last_sunday = last_sunday.replace(hour=23, minute=59, second=59)
    return last_monday, last_sunday

def is_monday():
    """
    Ce face:
        Returneaza True daca ziua curenta este luni.

    Variabile:
        Fara parametri.

    Erori:
        Nu ridica erori proprii.
    """
    return datetime.now().weekday() == 0

def was_summary_shown_today():
    """
    Ce face:
        Verifica daca rezumatul saptamanal a fost deja afisat astazi, comparand
        data din fisierul de urmarire cu data curenta.

    Variabile:
        last: data ultimei afisari citita din fisier.

    Erori:
        Daca fisierul "summary_last_shown.txt" nu exista returneaza False.
    """
    try:
        with open("summary_last_shown.txt", "r") as f:
            last = f.read().strip()
            return last == datetime.now().strftime("%Y-%m-%d")
    except FileNotFoundError:
        return False

def mark_summary_shown():
    """
    Ce face:
        Marcheaza rezumatul ca afisat astazi, scriind data curenta in fisierul
        de urmarire.

    Variabile:
        Fara parametri.

    Erori:
        Propaga erorile de I/O daca fisierul nu poate fi scris.
    """
    with open("summary_last_shown.txt", "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))

def get_weekly_summary():
    """
    Ce face:
        Construieste rezumatul pariurilor si acumulatorilor finalizati (numar,
        castiguri, win rate, profit, cel mai bun/rau pariu, evolutia bankului).
        Nota: intrarile nu sunt filtrate strict pe saptamana (nu exista data
        salvata per intrare), asa ca se iau toate cele finalizate.

    Variabile:
        start / end: intervalul saptamanii trecute (pentru afisare).
        bets / accs: pariurile si acumulatorii.
        finished_bets / finished_accs: intrarile finalizate.
        all_finished: lista unificata a intrarilor finalizate.
        total_profit / total_staked / wins / win_rate: agregatele.
        best / worst: intrarea cu cel mai mare, respectiv cel mai mic profit.
        buget_initial / buget_curent: bankul la inceput si dupa profit.

    Erori:
        Daca nu exista intrari finalizate returneaza None. Ridica KeyError daca
        fisierul bank nu contine "buget_initial".
    """
    start, end = get_last_week_range()

    bets = file_repo.load_bets()
    accs = accumulator_repo.load_accumulators()

    finished_bets = [b for b in bets if b.result is not None]
    finished_accs = [a for a in accs if a.result is not None]

    all_finished = []
    for b in finished_bets:
        all_finished.append({
            "match": b.match,
            "profit": b.profit,
            "odds": b.odds,
            "stake": b.stake,
            "result": b.result,
            "type": "simple"
        })
    for a in finished_accs:
        all_finished.append({
            "match": f"Acumulator ({len(a.matches)} meciuri)",
            "profit": a.profit,
            "odds": a.total_odds,
            "stake": a.stake,
            "result": a.result,
            "type": "acumulator"
        })

    if not all_finished:
        return None

    total_profit  = round(sum(e["profit"] for e in all_finished), 2)
    total_staked  = round(sum(e["stake"]  for e in all_finished), 2)
    wins          = [e for e in all_finished if e["result"] == "win"]
    win_rate      = round(len(wins) / len(all_finished) * 100, 1)
    best          = max(all_finished, key=lambda e: e["profit"])
    worst         = min(all_finished, key=lambda e: e["profit"])

    bank_data     = load_bank()
    buget_initial = bank_data["buget_initial"]
    buget_curent  = round(buget_initial + total_profit, 2)

    return {
        "total":        len(all_finished),
        "wins":         len(wins),
        "win_rate":     win_rate,
        "profit":       total_profit,
        "staked":       total_staked,
        "best":         best,
        "worst":        worst,
        "buget_initial": buget_initial,
        "buget_curent":  buget_curent,
        "week_start":   start.strftime("%d %b"),
        "week_end":     end.strftime("%d %b"),
    }
