from business import tracker

def print_menu():
    print("\n=== Betting Tracker ===")
    print("1. Adauga pariu")
    print("2. Vezi toate pariurile")
    print("3. Actualizeaza rezultat")
    print("4. Vezi statistici")
    print("5. Vezi meciuri viitoare")
    print("6. Value Bet Calculator")
    print("7. Adauga acumulator")
    print("8. Vezi acumulatori")
    print("9. Actualizeaza rezultat acumulator")
    print("10. Statistici acumulatori")
    print("11. Predictie meci")
    print("12. Grafic profit")
    print("13. Sterge pariu")
    print("0. Iesire")

def add_bet_ui():
    match = input("Meci: ")
    stake = float(input("Miza: "))
    odds = float(input("Cota: "))
    tracker.add_bet(match,stake,odds)
    print("Pariu adaugat!")

def view_bets_ui():
    bets = tracker.get_all_bets()
    if not bets:
        print("Fara pariuri salvate")
        return
    for i, bet in enumerate(bets):
        print(f"{i}.{bet}")

def update_result_ui():
    view_bets_ui()
    index = int(input("Index pariu:"))
    result = input("Rezultat: ").strip().lower()
    tracker.update_result(index,result)
    print("Actualizat!")

def view_upcoming_matches_ui():
    from repository.api_repo import get_upcoming_matches, LEAGUES
    print("\nAlege liga: ")
    leagues_list = list(LEAGUES.items())
    for i, (name, code) in enumerate(leagues_list):
        print(f"{i}. {name}")

    choice = int(input("> "))
    name, code = leagues_list[choice]

    print(f"\n=== {name} - Urmatoarele meciuri ===")
    matches = get_upcoming_matches(code)
    for i, m in enumerate(matches):
        print(f"{i}. {m}")

    add = input("\nVrei sa adaugi un pariu? (y/n): ").strip().lower()
    if add == "y":
        index = int(input("Index meci:"))
        match_str = matches[index].split(" | ")[1]
        stake = float(input("Miza: "))
        odds = float(input("Cota: "))
        tracker.add_bet(match_str,stake,odds)
        print("Pariu adaugat!")

def value_bet_ui():
    from business.calculator import odds_to_probability, has_value, expected_value
    print("\n=== Value Bet Calculator ===")
    your_prob = float(input("Sansa ta estimata ca echipa castiga (%): "))
    bookmaker_odds = float(input("Cota bookmakerului: "))
    stake = float(input("Miza (RON): "))

    implied = odds_to_probability(bookmaker_odds)
    value, is_value = has_value(your_prob, bookmaker_odds)
    ev = expected_value(stake, your_prob, bookmaker_odds)

    print(f"\nProbabilitate implicita bookmaker: {implied}%")
    print(f"Probabilitatea ta: {your_prob}%")
    print(f"Value: {value:+.1f}%")
    print(f"Expected Value: {ev:+.2f} RON")

    if is_value:
        print("✓ Pariu cu VALUE - merita!")
    else:
        print("✗ Fara value - skip!")

def add_accumulator_ui():
    from business import accumulator_tracker

    matches = []
    odds_list = []

    print("\n=== Adauga Acumulator ===")
    print("Adauga meciuri (scrie 'gata' cand ai terminat)")

    while True:
        match = input("Meci (ex: Real Madrid vs Barcelona): ").strip()
        if match.lower() == "gata":
            if len(matches) < 2:
                print("Un acumulator trebuie sa aiba minim 2 meciuri!")
                continue
            break
        odds = float(input(f"Cota pentru {match}: "))
        matches.append(match)
        odds_list.append(odds)

    stake = float(input("Miza totala (RON): "))

    # calculeaza cota totala
    total_odds = 1
    for o in odds_list:
        total_odds *= o
    total_odds = round(total_odds, 2)

    print(f"\nCota totala: {total_odds}")
    print(f"Castig potential: {round(total_odds * stake - stake, 2)} RON")
    confirm = input("Confirmi? (y/n): ").strip().lower()

    if confirm == "y":
        accumulator_tracker.add_accumulator(matches, odds_list, stake)
        print("Acumulator adaugat!")

def view_accumulators_ui():
    from business import accumulator_tracker

    accumulators = accumulator_tracker.get_all()
    if not accumulators:
        print("Nu ai niciun acumulator salvat.")
        return
    for i, acc in enumerate(accumulators):
        print(f"\n--- Acumulator {i} ---")
        print(acc)

def update_accumulator_result_ui():
    from business import accumulator_tracker

    view_accumulators_ui()
    index = int(input("Index acumulator: "))
    result = input("Rezultat (win/lose): ").strip().lower()
    accumulator_tracker.update_result(index, result)
    print("Rezultat actualizat!")

def predict_match_ui():
    from repository.api_repo import get_teams, LEAGUES
    from business.predictor import predict_match

    print("\nAlege liga:")
    leagues_list = list(LEAGUES.items())
    for i, (name, code) in enumerate(leagues_list):
        print(f"{i}. {name}")

    choice = int(input("Optiune: "))
    name, code = leagues_list[choice]

    print(f"\nSe incarca echipele din {name}...")
    teams = get_teams(code)

    for i, team_name in enumerate(teams.keys()):
        print(f"{i}. {team_name}")

    home_index = int(input("\nIndex echipa gazda: "))
    away_index = int(input("Index echipa oaspeti: "))

    teams_list = list(teams.items())
    home_name, home_id = teams_list[home_index]
    away_name, away_id = teams_list[away_index]

    print(f"\n=== {home_name} vs {away_name} ===")
    print(predict_match(home_id, away_id, code))

def show_chart_ui():
    from business.chart import show_profit_chart
    show_profit_chart()

def delete_bet_ui():
    view_bets_ui()
    index = int(input("Index pariu de sters: "))
    confirm = input("Esti sigur? (y/n): ").strip().lower()
    if confirm == "y":
        tracker.delete_bet(index)
        print("Pariu sters!")

def run():
    while True:
        print_menu()
        choice = input("> ").strip()
        if choice == "1":
            add_bet_ui()
        elif choice == "2":
            view_bets_ui()
        elif choice == "3":
            update_result_ui()
        elif choice == "4":
            print(tracker.get_stats())
        elif choice == "5":
            view_upcoming_matches_ui()
        elif choice == "6":
            value_bet_ui()
        elif choice == "7":
            add_accumulator_ui()
        elif choice == "8":
            view_accumulators_ui()
        elif choice == "9":
            update_accumulator_result_ui()
        elif choice == "10":
            from business import accumulator_tracker
            print(accumulator_tracker.get_stats())
        elif choice == "11":
            predict_match_ui()
        elif choice == "12":
            show_chart_ui()
        elif choice == "13":
            delete_bet_ui()
        elif choice == "0":
            print("Pa!")
            break
        else:
            print("Optiune invalida")