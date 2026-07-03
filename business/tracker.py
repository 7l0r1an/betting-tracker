from repository import file_repo

def add_bet(match, stake, odds, bet_type=None):
    """
    Ce face:
        Creeaza un pariu simplu nou si il salveaza in stocare.

    Variabile:
        match: numele meciului.
        stake: miza pariata.
        odds: cota pariului.
        bet_type: tipul pariului (optional).
        bets: lista curenta de pariuri.
        new_bet: pariul nou creat.

    Erori:
        Propaga erorile de I/O de la incarcarea/salvarea fisierului.
    """
    bets = file_repo.load_bets()
    from domain.bet import Bet
    new_bet = Bet(stake, match, odds, bet_type=bet_type)
    bets.append(new_bet)
    file_repo.save_bets(bets)

def update_result(index, result):
    """
    Ce face:
        Seteaza rezultatul pariului de la pozitia index si salveaza.

    Variabile:
        index: pozitia pariului in lista.
        result: rezultatul de setat ("win" / "lose").
        bets: lista curenta de pariuri.

    Erori:
        Daca index este in afara intervalului nu modifica nimic si afiseaza
        "Index invalid".
    """
    bets = file_repo.load_bets()
    if 0<=index<len(bets):
        bets[index].result = result
        file_repo.save_bets(bets)
    else:
        print("Index invalid")

def get_all_bets():
    """
    Ce face:
        Returneaza toate pariurile simple salvate.

    Variabile:
        Fara parametri.

    Erori:
        Propaga erorile de incarcare (returneaza lista goala daca fisierul lipseste).
    """
    return file_repo.load_bets()

def delete_bet(index):
    """
    Ce face:
        Sterge pariul de la pozitia index din stocare.

    Variabile:
        index: pozitia pariului de sters.

    Erori:
        Daca index este invalid, operatia este ignorata la nivelul repository-ului.
    """
    file_repo.delete_bet(index)

def get_stats():
    """
    Ce face:
        Calculeaza statisticile pe pariurile simple finalizate (numar, castiguri,
        win rate, profit total, ROI) si le returneaza ca text formatat.

    Variabile:
        bets: toate pariurile.
        finished: pariurile cu rezultat setat.
        wins: pariurile castigate.
        total_profit: suma profiturilor.
        total_staked: suma mizelor.
        win_rate: procentul de castiguri.
        roi: randamentul investitiei (profit / miza * 100).

    Erori:
        Daca nu exista pariuri finalizate returneaza mesaj informativ.
        Daca total_staked este 0 calculul ROI ridica ZeroDivisionError.
    """
    bets = file_repo.load_bets()
    finished = [b for b in bets if b.result is not None]
    if not finished:
        return "Nu sunt pariuri finalizate"
    wins = [b for b in finished if b.result == "win"]
    total_profit = sum(b.profit for b in finished)
    total_staked = sum(b.stake for b in finished)
    win_rate = len(wins) / len(finished)*100
    roi = total_profit / total_staked * 100

    return (
        f"Pariuri castigate: {len(finished)}\n"
        f"Castigate: {len(wins)}\n"
        f"Win Rate: {win_rate:.1f}%\n"
        f"Profit total: {total_profit:.2f} RON\n"
        f"ROI: {roi:.1f}%\n"
    )
