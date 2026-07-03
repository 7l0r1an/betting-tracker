from repository.api_repo import get_recent_form_detailed, get_head_to_head, get_standings

def predict_match(home_team_id, away_team_id, league_code):
    """
    Ce face:
        Estimeaza probabilitatile de rezultat (victorie gazde / egal / victorie
        oaspeti) pentru un meci, combinand forma recenta, pozitia in clasament si
        istoricul direct (head to head). Returneaza un raport text detaliat.

    Variabile:
        home_team_id / away_team_id: id-urile echipelor.
        league_code: codul ligii (pentru clasament).
        home_form / away_form: forma recenta a fiecarei echipe.
        h2h: meciurile directe recente.
        standings: clasamentul ligii, indexat pe id de echipa.
        home_score / away_score: scorurile de forta calculate.
        pos_diff / bonus: diferenta de pozitie in clasament si bonusul aplicat gazdelor.
        h2h_home_score / h2h_away_score: castigurile directe ale fiecarei echipe.
        total / total_prob: sume folosite pentru normalizarea probabilitatilor.
        home_prob / draw_prob / away_prob: probabilitatile finale normalizate.

    Erori:
        Daca lipseste forma pentru vreo echipa returneaza "Nu sunt suficiente date."
        Clasamentul si h2h se aplica doar daca sunt disponibile. Propaga erorile
        de retea/API din apelurile subiacente.
    """
    home_form = get_recent_form_detailed(home_team_id)
    away_form = get_recent_form_detailed(away_team_id)
    h2h = get_head_to_head(home_team_id, away_team_id)
    standings = get_standings(league_code)

    if not home_form or not away_form:
        return "Nu sunt suficiente date."

    home_score, home_breakdown = calculate_score(home_form, is_home=True)
    away_score, away_breakdown = calculate_score(away_form, is_home=False)

    standing_breakdown = ""
    if home_team_id in standings and away_team_id in standings:
        home_pos = standings[home_team_id]["position"]
        away_pos = standings[away_team_id]["position"]
        home_pts = standings[home_team_id]["points"]
        away_pts = standings[away_team_id]["points"]

        pos_diff = away_pos - home_pos
        bonus = pos_diff * 0.3
        home_score += bonus

        standing_breakdown = (
            f"\n--- Clasament ---\n"
            f"  Gazde: locul {home_pos} ({home_pts} puncte)\n"
            f"  Oaspeti: locul {away_pos} ({away_pts} puncte)\n"
            f"  Bonus gazde din clasament: {bonus:+.1f}\n"
        )

    h2h_breakdown = "\n--- Head to Head ---\n"
    h2h_home_score = 0
    h2h_away_score = 0
    if not h2h:
        h2h_breakdown += "  Nu exista meciuri directe recente.\n"
    else:
        for match in h2h:
            hs = match["home_score"]
            as_ = match["away_score"]
            home_won = (match["home_id"] == home_team_id and hs > as_) or \
                       (match["away_id"] == home_team_id and as_ > hs)
            away_won = (match["home_id"] == away_team_id and hs > as_) or \
                       (match["away_id"] == away_team_id and as_ > hs)

            if home_won:
                h2h_home_score += 1
                h2h_breakdown += f"  {hs}-{as_} → Gazde au castigat\n"
            elif away_won:
                h2h_away_score += 1
                h2h_breakdown += f"  {hs}-{as_} → Oaspeti au castigat\n"
            else:
                h2h_breakdown += f"  {hs}-{as_} → Egal\n"

        home_score += h2h_home_score * 0.5
        away_score += h2h_away_score * 0.5
        h2h_breakdown += f"  Bonus gazde: +{h2h_home_score * 0.5:.1f} | Bonus oaspeti: +{h2h_away_score * 0.5:.1f}\n"

    total = home_score + away_score
    home_prob = round(home_score / total * 100, 1)
    away_prob = round(away_score / total * 100, 1)

    diff = abs(home_prob - away_prob)
    draw_prob = round(max(0, 35 - diff), 1)

    total_prob = home_prob + away_prob + draw_prob
    home_prob = round(home_prob / total_prob * 100, 1)
    away_prob = round(away_prob / total_prob * 100, 1)
    draw_prob = round(100 - home_prob - away_prob, 1)

    return (
        f"\n--- Analiza Gazde ---\n{home_breakdown}"
        f"\n--- Analiza Oaspeti ---\n{away_breakdown}"
        f"{standing_breakdown}"
        f"{h2h_breakdown}"
        f"\n--- Probabilitati finale ---\n"
        f"  Victorie gazde:   {home_prob}%\n"
        f"  Egal:             {draw_prob}%\n"
        f"  Victorie oaspeti: {away_prob}%"
    )

def calculate_score(form, is_home):
    """
    Ce face:
        Calculeaza un scor de forta pentru o echipa pe baza formei recente
        (puncte din rezultat, bonus goluri marcate, penalizare goluri primite) si
        aplica un bonus de teren propriu pentru gazde. Returneaza (scor, breakdown).

    Variabile:
        form: lista de meciuri, fiecare cu "result", "goals_scored", "goals_conceded".
        is_home: True daca echipa joaca acasa (aplica bonus x1.15).
        score: scorul cumulat.
        lines: liniile textului explicativ per meci.
        match_score: scorul unui meci individual.
        goals_bonus / goals_penalty: componentele din goluri.
        breakdown: textul detaliat al calculului.

    Erori:
        Ridica KeyError daca un meci nu contine cheile asteptate. Scorul minim
        returnat este 0.1 (nu poate fi 0 sau negativ).
    """
    score = 0
    lines = []

    for i, match in enumerate(form):
        result = match["result"]
        goals_scored = match["goals_scored"]
        goals_conceded = match["goals_conceded"]

        match_score = 0

        if result == "W":
            match_score += 3
        elif result == "D":
            match_score += 1

        goals_bonus = goals_scored * 0.5
        goals_penalty = goals_conceded * 0.3
        match_score += goals_bonus - goals_penalty

        lines.append(
            f"  Meci {i+1}: {result} | "
            f"{goals_scored}-{goals_conceded} | "
            f"Puncte rezultat: {3 if result=='W' else 1 if result=='D' else 0} | "
            f"Bonus goluri: +{goals_bonus:.1f} | "
            f"Penalizare: -{goals_penalty:.1f} | "
            f"Total meci: {match_score:.1f}"
        )

        score += match_score

    if is_home:
        lines.append(f"  Bonus teren propriu: x1.15 ({score:.1f} → {score*1.15:.1f})")
        score *= 1.15

    lines.append(f"  Scor final: {max(score, 0.1):.2f}")
    breakdown = "\n".join(lines) + "\n"

    return max(score, 0.1), breakdown
