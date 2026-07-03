from datetime import datetime

class Bet:
    def __init__(self, stake, match, odds, result=None, bet_type=None, date=None):
        """
        Ce face:
            Construieste un pariu simplu pe un singur meci.

        Variabile:
            stake: miza pariata.
            match: numele meciului.
            odds: cota pariului.
            result: rezultatul ("win", "lose" sau None daca nu e finalizat).
            bet_type: tipul pariului (ex: "1X2", "Peste/Sub", "BTTS") sau None.
            date: data pariului (YYYY-MM-DD); daca lipseste se pune data curenta.

        Erori:
            Nu valideaza tipurile argumentelor; valorile gresite se propaga in
            calculele ulterioare fara verificari.
        """
        self.stake    = stake
        self.match    = match
        self.odds     = odds
        self.result   = result
        self.bet_type = bet_type
        self.date     = date or datetime.now().strftime("%Y-%m-%d")

    @property
    def profit(self):
        """
        Ce face:
            Returneaza profitul pariului: castig net la "win", miza pierduta la
            "lose", 0 daca nu e finalizat.

        Variabile:
            Foloseste self.result, self.stake si self.odds.

        Erori:
            Nu ridica erori; pentru orice result diferit de "win"/"lose"
            returneaza 0.
        """
        if self.result == "win":
            return round(self.stake * self.odds - self.stake, 2)
        elif self.result == "lose":
            return -self.stake
        return 0

    def __str__(self):
        """
        Ce face:
            Returneaza o reprezentare text a pariului (tip, meci, miza, cota,
            rezultat, profit).

        Variabile:
            tip: prefixul cu tipul pariului sau sir gol daca bet_type lipseste.

        Erori:
            Nu ridica erori proprii.
        """
        tip = f"[{self.bet_type}] " if self.bet_type else ""
        return f"{tip}{self.match} | Miza: {self.stake} RON | Cota: {self.odds} | Rezultat: {self.result} | Profit: {self.profit} RON"
