from repository import file_repo, accumulator_repo

BET_TYPES = ["1X2", "Peste/Sub", "BTTS"]

def get_stats_by_type():
    bets = file_repo.load_bets()
    accs = accumulator_repo.load_accumulators()

    # pariuri simple finalizate cu tip
    all_entries = []
    for b in bets:
        if b.result is not None and b.bet_type is not None:
            all_entries.append({
                "type":   b.bet_type,
                "result": b.result,
                "odds":   b.odds,
                "stake":  b.stake,
                "profit": b.profit
            })

    # meciuri individuale din acumulatori
    for a in accs:
        for i, (match, odds, result, bet_type) in enumerate(zip(
            a.matches, a.odds_list, a.match_results, a.match_types
        )):
            if result is not None and bet_type is not None:
                profit = round(odds - 1, 2) if result == "win" else -1
                all_entries.append({
                    "type":   bet_type,
                    "result": result,
                    "odds":   odds,
                    "stake":  1,  # normalizat
                    "profit": profit
                })

    stats = {}
    for bet_type in BET_TYPES:
        type_entries = [e for e in all_entries if e["type"] == bet_type]
        if not type_entries:
            stats[bet_type] = None
            continue

        wins         = [e for e in type_entries if e["result"] == "win"]
        total_profit = round(sum(e["profit"] for e in type_entries), 2)
        total_staked = round(sum(e["stake"]  for e in type_entries), 2)
        win_rate     = round(len(wins) / len(type_entries) * 100, 1)
        roi          = round(total_profit / total_staked * 100, 1) if total_staked else 0

        stats[bet_type] = {
            "total":    len(type_entries),
            "wins":     len(wins),
            "profit":   total_profit,
            "staked":   total_staked,
            "win_rate": win_rate,
            "roi":      roi,
        }

    return stats