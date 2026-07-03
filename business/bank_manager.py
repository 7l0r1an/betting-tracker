from repository import bank_repo
from repository import file_repo, accumulator_repo

def set_buget_initial(suma):
    """
    Ce face:
        Seteaza bugetul initial in stocare.

    Variabile:
        suma: valoarea bugetului initial.

    Erori:
        Propaga erorile de I/O de la salvarea fisierului bank.
    """
    bank_repo.set_buget(suma)

def get_status():
    """
    Ce face:
        Calculeaza starea curenta a bankului: buget initial, profit total din
        pariuri simple si acumulatori finalizati, si bugetul curent.

    Variabile:
        data: continutul fisierului bank.
        buget_initial: bugetul initial salvat.
        bets: pariurile simple.
        accs: acumulatorii.
        profit_pariuri: suma profiturilor pariurilor finalizate.
        profit_accs: suma profiturilor acumulatorilor finalizati.
        profit_total: profitul cumulat, rotunjit.
        buget_curent: buget_initial + profit_total.

    Erori:
        Ridica KeyError daca fisierul bank nu contine cheia "buget_initial".
        Propaga erorile de incarcare a fisierelor.
    """
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
    """
    Ce face:
        Construieste evolutia bugetului in timp, adaugand cumulat profitul
        fiecarui pariu/acumulator finalizat peste bugetul initial.

    Variabile:
        bets: pariurile simple.
        accs: acumulatorii.
        buget_initial: bugetul de pornire.
        finished: lista de perechi (eticheta, profit) pentru intrarile finalizate.
        valori: lista valorilor bugetului dupa fiecare pas (incepe cu bugetul initial).
        labels: etichetele corespunzatoare fiecarei valori (incepe cu "Start").
        curent: bugetul acumulat pe parcurs.

    Erori:
        Un acumulator finalizat fara meciuri ridica IndexError la a.matches[0].
        Propaga erorile de incarcare a fisierelor.
    """
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
