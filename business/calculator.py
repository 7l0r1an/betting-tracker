def odds_to_probability(odds):
    """
    Ce face:
        Converteste o cota in probabilitatea implicita (in procente).

    Variabile:
        odds: cota bookmakerului.

    Erori:
        Daca odds este 0 ridica ZeroDivisionError.
    """
    return round(1/odds*100,1)

def has_value(your_probability, bookmaker_odds):
    """
    Ce face:
        Verifica daca un pariu are value comparand probabilitatea ta estimata
        cu probabilitatea implicita a cotei. Returneaza (diferenta, are_value).

    Variabile:
        your_probability: sansa estimata de tine ca pariul castiga (0-100).
        bookmaker_odds: cota oferita de bookmaker.
        implied_probability: probabilitatea derivata din cota.
        value: diferenta dintre estimarea ta si probabilitatea implicita.

    Erori:
        Propaga ZeroDivisionError daca bookmaker_odds este 0.
    """
    implied_probability = odds_to_probability(bookmaker_odds)
    value = your_probability - implied_probability
    return value, value > 0

def expected_value(stake, your_probability, bookmaker_odds):
    """
    Ce face:
        Calculeaza valoarea asteptata (EV) a pariului pe termen lung. EV pozitiv
        indica un pariu bun statistic.

    Variabile:
        stake: miza pariata.
        your_probability: sansa estimata de castig (0-100).
        bookmaker_odds: cota bookmakerului.
        win_chance: probabilitatea de castig ca fractie (0-1).
        lose_chance: probabilitatea de pierdere (1 - win_chance).
        profit_if_win: profitul net in caz de castig.
        ev: valoarea asteptata.

    Erori:
        Nu ridica erori proprii; valori nevalide produc un EV nesemnificativ.
    """
    win_chance = your_probability / 100
    lose_chance = 1-win_chance
    profit_if_win = stake * bookmaker_odds - stake
    ev = (win_chance * profit_if_win) - (lose_chance * stake)
    return round(ev,2)
