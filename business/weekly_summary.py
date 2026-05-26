from datetime import datetime, timedelta
from repository import file_repo, accumulator_repo
from repository.bank_repo import load_bank

def get_last_week_range():
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    last_monday = last_monday.replace(hour=0, minute=0, second=0)
    last_sunday = last_sunday.replace(hour=23, minute=59, second=59)
    return last_monday, last_sunday

def is_monday():
    return datetime.now().weekday() == 0

def was_summary_shown_today():
    try:
        with open("summary_last_shown.txt", "r") as f:
            last = f.read().strip()
            return last == datetime.now().strftime("%Y-%m-%d")
    except FileNotFoundError:
        return False

def mark_summary_shown():
    with open("summary_last_shown.txt", "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))

def get_weekly_summary():
    start, end = get_last_week_range()

    bets = file_repo.load_bets()
    accs = accumulator_repo.load_accumulators()

    # filtram pariurile din saptamana trecuta
    # folosim indexul ca nu avem data salvata — luam toate finalizate
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