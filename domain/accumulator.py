from datetime import datetime

class Accumulator:
    def __init__(self, matches, odds_list, stake, result=None,
                 match_results=None, match_types=None, date=None):
        self.matches       = matches
        self.odds_list     = odds_list
        self.stake         = stake
        self.result        = result
        self.match_results = match_results or [None] * len(matches)
        self.match_types   = match_types or [None] * len(matches)
        self.date          = date or datetime.now().strftime("%Y-%m-%d")

    @property
    def total_odds(self):
        result = 1
        for odds in self.odds_list:
            result *= odds
        return round(result, 2)

    @property
    def profit(self):
        if self.result == "win":
            return round(self.stake * self.total_odds - self.stake, 2)
        elif self.result == "lose":
            return -self.stake
        return 0

    def update_match_result(self, index, result):
        self.match_results[index] = result
        if any(r == "lose" for r in self.match_results):
            self.result = "lose"
        elif all(r == "win" for r in self.match_results):
            self.result = "win"
        else:
            self.result = None

    def __str__(self):
        matches_str = "\n   ".join(self.matches)
        return (
            f"Meciuri:\n   {matches_str}\n"
            f"Cota totala: {self.total_odds} | "
            f"Miza: {self.stake} RON | "
            f"Profit potential: {round(self.stake * self.total_odds - self.stake, 2)} RON | "
            f"Rezultat: {self.result}"
        )