from datetime import datetime

class Accumulator:
    def __init__(self, matches, odds_list, stake, result=None,
                 match_results=None, match_types=None, date=None):
        """
        Ce face:
            Construieste un acumulator (bilet cu mai multe meciuri).

        Variabile:
            matches: lista cu numele meciurilor.
            odds_list: lista cu cotele individuale, in aceeasi ordine ca matches.
            stake: miza totala pariata pe bilet.
            result: rezultatul biletului ("win", "lose" sau None daca nu e finalizat).
            match_results: lista cu rezultatul fiecarui meci; daca lipseste se
                initializeaza cu None pentru fiecare meci.
            match_types: lista cu tipul de pariu al fiecarui meci; daca lipseste
                se initializeaza cu None pentru fiecare meci.
            date: data biletului (YYYY-MM-DD); daca lipseste se pune data curenta.

        Erori:
            Nu valideaza corespondenta dintre lungimea listelor. Daca odds_list
            are mai putine elemente decat matches, calculele ulterioare pot da
            rezultate gresite fara a ridica exceptie.
        """
        self.matches       = matches
        self.odds_list     = odds_list
        self.stake         = stake
        self.result        = result
        self.match_results = match_results or [None] * len(matches)
        self.match_types   = match_types or [None] * len(matches)
        self.date          = date or datetime.now().strftime("%Y-%m-%d")

    @property
    def total_odds(self):
        """
        Ce face:
            Calculeaza cota totala a biletului inmultind toate cotele individuale.

        Variabile:
            result: acumulatorul produsului cotelor, initializat cu 1.

        Erori:
            Daca odds_list este goala returneaza 1. Daca o cota nu e numerica
            ridica TypeError la inmultire.
        """
        result = 1
        for odds in self.odds_list:
            result *= odds
        return round(result, 2)

    @property
    def profit(self):
        """
        Ce face:
            Returneaza profitul biletului in functie de rezultat: castig net la
            "win", miza pierduta la "lose", 0 daca nu e finalizat.

        Variabile:
            Foloseste self.result, self.stake si self.total_odds.

        Erori:
            Nu ridica erori; pentru orice result diferit de "win"/"lose"
            returneaza 0.
        """
        if self.result == "win":
            return round(self.stake * self.total_odds - self.stake, 2)
        elif self.result == "lose":
            return -self.stake
        return 0

    def update_match_result(self, index, result):
        """
        Ce face:
            Seteaza rezultatul unui meci din bilet si recalculeaza rezultatul
            intregului bilet: "lose" daca vreun meci e pierdut, "win" daca toate
            sunt castigate, altfel None (inca in desfasurare).

        Variabile:
            index: pozitia meciului in match_results.
            result: rezultatul meciului ("win" / "lose").

        Erori:
            Daca index este in afara intervalului ridica IndexError.
        """
        self.match_results[index] = result
        if any(r == "lose" for r in self.match_results):
            self.result = "lose"
        elif all(r == "win" for r in self.match_results):
            self.result = "win"
        else:
            self.result = None

    def __str__(self):
        """
        Ce face:
            Returneaza o reprezentare text a biletului cu meciurile, cota totala,
            miza, profitul potential si rezultatul.

        Variabile:
            matches_str: meciurile concatenate pe cate o linie fiecare.

        Erori:
            Nu ridica erori proprii.
        """
        matches_str = "\n   ".join(self.matches)
        return (
            f"Meciuri:\n   {matches_str}\n"
            f"Cota totala: {self.total_odds} | "
            f"Miza: {self.stake} RON | "
            f"Profit potential: {round(self.stake * self.total_odds - self.stake, 2)} RON | "
            f"Rezultat: {self.result}"
        )
