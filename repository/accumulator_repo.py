# accumulator_repo.py
import json
from domain.accumulator import Accumulator

FILENAME = "accumulatori.json"

def load_accumulators():
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        return [Accumulator(
            d["matches"], d["odds_list"], d["stake"],
            d["result"], d.get("match_results"),
            d.get("match_types"), d.get("date")
        ) for d in data]
    except FileNotFoundError:
        return []

def save_accumulators(accumulators):
    data = [
        {
            "matches":       a.matches,
            "odds_list":     a.odds_list,
            "stake":         a.stake,
            "result":        a.result,
            "match_results": a.match_results,
            "match_types":   a.match_types,
            "date":          a.date
        }
        for a in accumulators
    ]
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def delete_accumulator(index):
    accs = load_accumulators()
    if 0 <= index < len(accs):
        accs.pop(index)
        save_accumulators(accs)