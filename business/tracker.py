from repository import file_repo

def add_bet(match, stake, odds, bet_type=None):
    bets = file_repo.load_bets()
    from domain.bet import Bet
    new_bet = Bet(stake, match, odds, bet_type=bet_type)
    bets.append(new_bet)
    file_repo.save_bets(bets)

def update_result(index, result):
    bets = file_repo.load_bets()
    if 0<=index<len(bets):
        bets[index].result = result
        file_repo.save_bets(bets)
    else:
        print("Index invalid")

def get_all_bets():
    return file_repo.load_bets()

def delete_bet(index):
    file_repo.delete_bet(index)

def get_stats():
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