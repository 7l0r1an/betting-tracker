from repository import bank_repo
from repository import file_repo, accumulator_repo

def set_buget_initial(suma):
    bank_repo.set_buget(suma)

def get_status():
    from repository import file_repo, accumulator_repo
    data = bank_repo.load_bank()
    buget_initial = data["buget_initial"]

    bets = file_repo.load_bets()
    accs = accumulator_repo.load_accumulators()

    profit_pariuri = sum(b.profit for b in bets if b.result is not None)
    profit_accs    = sum(a.profit for a in accs if a.result is not None)
    profit_total   = round(profit_pariuri + profit_accs, 2)
    buget_curent   = round(buget_initial + profit_total, 2)

    return {
        "buget_initial": buget_initial,
        "buget_curent":  buget_curent,
        "profit":        profit_total,
    }

def get_evolutie():
    """Returneaza evolutia bugetului in timp bazata pe pariuri finalizate"""
    bets = file_repo.load_bets()
    accs = accumulator_repo.load_accumulators()

    data = bank_repo.load_bank()
    buget_initial = data["buget_initial"]

    finished = [(b.match[:20], b.profit) for b in bets if b.result is not None]
    finished += [(a.matches[0][:20] + "+", a.profit) for a in accs if a.result is not None]

    valori = [buget_initial]
    labels = ["Start"]
    curent = buget_initial

    for label, profit in finished:
        curent += profit
        valori.append(round(curent, 2))
        labels.append(label)

    return valori, labels