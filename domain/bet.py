from datetime import datetime

class Bet:
    def __init__(self, stake, match, odds, result=None, bet_type=None, date=None):
        self.stake    = stake
        self.match    = match
        self.odds     = odds
        self.result   = result
        self.bet_type = bet_type
        self.date     = date or datetime.now().strftime("%Y-%m-%d")

    @property
    def profit(self):
        if self.result == "win":
            return round(self.stake * self.odds - self.stake, 2)
        elif self.result == "lose":
            return -self.stake
        return 0

    def __str__(self):
        tip = f"[{self.bet_type}] " if self.bet_type else ""
        return f"{tip}{self.match} | Miza: {self.stake} RON | Cota: {self.odds} | Rezultat: {self.result} | Profit: {self.profit} RON"