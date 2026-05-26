from repository import accumulator_repo
from domain.accumulator import Accumulator

def add_accumulator(matches, odds_list, stake, match_types=None):
    accumulators = accumulator_repo.load_accumulators()
    new_acc = Accumulator(matches, odds_list, stake, match_types=match_types)
    accumulators.append(new_acc)
    accumulator_repo.save_accumulators(accumulators)

def update_result(index,result):
    accumulators = accumulator_repo.load_accumulators()
    if 0 <= index < len(accumulators):
        accumulators[index].result = result
        accumulator_repo.save_accumulators(accumulators)
    else:
        print("Index invalid!")

def update_match_result(acc_index, match_index, result):
    # asta e cea noua - pentru un meci individual din acumulator
    accumulators = accumulator_repo.load_accumulators()
    if 0 <= acc_index < len(accumulators):
        accumulators[acc_index].update_match_result(match_index, result)
        accumulator_repo.save_accumulators(accumulators)

def get_all():
    return accumulator_repo.load_accumulators()

def delete_accumulator(index):
    accumulator_repo.delete_accumulator(index)

def get_stats():
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
