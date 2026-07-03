from repository import accumulator_repo
from domain.accumulator import Accumulator

def add_accumulator(matches, odds_list, stake, match_types=None):
    """
    Ce face:
        Creeaza un acumulator nou si il salveaza in fisierul de stocare.

    Variabile:
        matches: lista cu numele meciurilor.
        odds_list: lista cu cotele individuale.
        stake: miza totala pariata pe bilet.
        match_types: lista cu tipul de pariu al fiecarui meci (optional).
        accumulators: lista curenta de acumulatori incarcata din stocare.
        new_acc: acumulatorul nou creat.

    Erori:
        Propaga erorile de I/O de la incarcarea/salvarea fisierului. Nu
        valideaza continutul argumentelor.
    """
    accumulators = accumulator_repo.load_accumulators()
    new_acc = Accumulator(matches, odds_list, stake, match_types=match_types)
    accumulators.append(new_acc)
    accumulator_repo.save_accumulators(accumulators)

def update_result(index,result):
    """
    Ce face:
        Seteaza rezultatul intregului acumulator de la pozitia index si salveaza.

    Variabile:
        index: pozitia acumulatorului in lista.
        result: rezultatul de setat ("win" / "lose").
        accumulators: lista curenta de acumulatori.

    Erori:
        Daca index este in afara intervalului nu modifica nimic si afiseaza
        "Index invalid!".
    """
    accumulators = accumulator_repo.load_accumulators()
    if 0 <= index < len(accumulators):
        accumulators[index].result = result
        accumulator_repo.save_accumulators(accumulators)
    else:
        print("Index invalid!")

def update_match_result(acc_index, match_index, result):
    """
    Ce face:
        Actualizeaza rezultatul unui singur meci dintr-un acumulator, apoi
        salveaza. Rezultatul biletului se recalculeaza automat in obiect.

    Variabile:
        acc_index: pozitia acumulatorului in lista.
        match_index: pozitia meciului in interiorul acumulatorului.
        result: rezultatul meciului ("win" / "lose").
        accumulators: lista curenta de acumulatori.

    Erori:
        Daca acc_index este in afara intervalului nu face nimic (fara mesaj).
        Un match_index invalid ridica IndexError din obiectul Accumulator.
    """
    accumulators = accumulator_repo.load_accumulators()
    if 0 <= acc_index < len(accumulators):
        accumulators[acc_index].update_match_result(match_index, result)
        accumulator_repo.save_accumulators(accumulators)

def get_all():
    """
    Ce face:
        Returneaza toti acumulatorii salvati.

    Variabile:
        Fara parametri.

    Erori:
        Propaga erorile de incarcare din stocare (in mod normal returneaza
        lista goala daca fisierul nu exista).
    """
    return accumulator_repo.load_accumulators()

def delete_accumulator(index):
    """
    Ce face:
        Sterge acumulatorul de la pozitia index din stocare.

    Variabile:
        index: pozitia acumulatorului de sters.

    Erori:
        Daca index este invalid, operatia este ignorata la nivelul repository-ului.
    """
    accumulator_repo.delete_accumulator(index)

def get_stats():
    """
    Ce face:
        Calculeaza statisticile pe acumulatorii finalizati (numar, castiguri,
        win rate, profit total, ROI) si le returneaza ca text formatat.

    Variabile:
        accumulators: toti acumulatorii din stocare.
        finished: acumulatorii cu rezultat setat.
        wins: acumulatorii castigati.
        total_profit: suma profiturilor.
        total_staked: suma mizelor.
        win_rate: procentul de castiguri.
        roi: randamentul investitiei (profit / miza * 100).

    Erori:
        Daca nu exista acumulatori finalizati returneaza mesaj informativ.
        Daca total_staked este 0 calculul ROI ridica ZeroDivisionError.
    """
    accumulators = accumulator_repo.load_accumulatotrs()
    finished = [a for a in accumulators if a.result is not None]
    if not finished:
        return "Nu ai acumulatori finalizati"
    wins = [a for a in finished if a.result == "win"]
    total_profit = sum(a.profit for a in finished)
    total_staked = sum(a.stake for a in finished)
    win_rate = len(wins) / len(finished) * 100
    roi = total_profit / total_staked * 100

    return (
        f"Acumulatori finalizati: {len(finished)}\n"
        f"Castigati: {len(wins)}\n"
        f"Win rate: {win_rate:.1f}%\n"
        f"Profit total: {total_profit:.2f} RON\n"
        f"ROI: {roi:.1f}%"
    )
