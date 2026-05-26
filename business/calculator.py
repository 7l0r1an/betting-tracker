def odds_to_probability(odds):
    return round(1/odds*100,1)

def has_value(your_probability, bookmaker_odds):
    """
    Verifica daca un pariu are value
    your_probability = ce crezi tu ca sunt sansele (0-100)
    bookmaker_odds = cota oferita de bookmaker
    """
    implied_probability = odds_to_probability(bookmaker_odds)
    value = your_probability - implied_probability
    return value, value > 0

def expected_value(stake, your_probability, bookmaker_odds):
    """
    Calculeaza profitul asteptat pe termen lung
    EV pozitiv = pariu bun pe termen lung
    """
    win_chance = your_probability / 100
    lose_chance = 1-win_chance
    profit_if_win = stake * bookmaker_odds - stake
    ev = (win_chance * profit_if_win) - (lose_chance * stake)
    return round(ev,2)