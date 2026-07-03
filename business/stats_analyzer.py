from repository.api_repo import get_match_stats_history

def calculate_probabilities(values, thresholds):
    """
    Ce face:
        Calculeaza, pentru fiecare prag, procentul de valori care il depasesc.
        Returneaza un dictionar {"peste <prag>": procent}.

    Variabile:
        values: lista de valori numerice observate.
        thresholds: lista de praguri de comparat.
        result: dictionarul rezultat.
        over: numarul de valori peste pragul curent.

    Erori:
        Daca values este gol returneaza un dictionar gol (evita impartirea la 0).
    """
    if not values:
        return {}
    result = {}
    for t in thresholds:
        over = sum(1 for v in values if v > t)
        result[f"peste {t}"] = round(over / len(values) * 100, 1)
    return result

def get_team_stats(team_id, count=10):
    """
    Ce face:
        Extrage istoricul recent al unei echipe si calculeaza mediile si
        probabilitatile pentru goluri totale, goluri marcate si goluri primite.

    Variabile:
        team_id: id-ul echipei.
        count: numarul de meciuri analizate (implicit 10).
        stats: istoricul brut al meciurilor.
        goals / scored / conceded: listele de valori extrase din istoric.

    Erori:
        Daca nu exista istoric returneaza None. Propaga erorile de retea/API.
    """
    stats = get_match_stats_history(team_id, count)
    if not stats:
        return None

    goals    = [s["goals"]    for s in stats]
    scored   = [s["scored"]   for s in stats]
    conceded = [s["conceded"] for s in stats]

    return {
        "goals":    {"avg": round(sum(goals)    / len(goals),    2),
                     "probs": calculate_probabilities(goals,    [0.5, 1.5, 2.5, 3.5])},
        "scored":   {"avg": round(sum(scored)   / len(scored),   2),
                     "probs": calculate_probabilities(scored,   [0.5, 1.5, 2.5])},
        "conceded": {"avg": round(sum(conceded) / len(conceded), 2),
                     "probs": calculate_probabilities(conceded, [0.5, 1.5, 2.5])},
    }

def combine_stats(home_stats, away_stats):
    """
    Ce face:
        Combina statisticile a doua echipe facand media pentru fiecare categorie
        (goluri totale, marcate, primite) si pentru fiecare prag de probabilitate.

    Variabile:
        home_stats / away_stats: statisticile celor doua echipe.
        combine: functie interna care mediaza media si probabilitatile a doua
            categorii corespunzatoare.

    Erori:
        Ridica TypeError daca home_stats sau away_stats este None. Presupune ca
        ambele au aceleasi chei si aceleasi praguri.
    """
    def combine(h, a):
        avg = round((h["avg"] + a["avg"]) / 2, 2)
        probs = {}
        for t_str in h["probs"]:
            probs[t_str] = round((h["probs"][t_str] + a["probs"][t_str]) / 2, 1)
        return {"avg": avg, "probs": probs}

    return {
        "goals":    combine(home_stats["goals"],    away_stats["goals"]),
        "scored":   combine(home_stats["scored"],   away_stats["scored"]),
        "conceded": combine(home_stats["conceded"], away_stats["conceded"]),
    }

def format_team_stats(stats, team_name):
    """
    Ce face:
        Formateaza statisticile unei echipe intr-un text cu bare de progres pentru
        goluri totale, marcate si primite.

    Variabile:
        stats: statisticile echipei (din get_team_stats).
        team_name: numele echipei pentru afisare.
        prob_bar: functie interna care deseneaza o bara text pentru un procent.
        lines: liniile textului rezultat.

    Erori:
        Daca stats este None/gol returneaza un mesaj ca nu sunt date.
    """
    if not stats:
        return f"Nu sunt date pentru {team_name}."

    def prob_bar(pct):
        filled = int(pct / 10)
        return f"[{'█' * filled}{'░' * (10 - filled)}] {pct}%"

    lines = [f"📊 {team_name} — ultimele 10 meciuri\n"]

    lines.append("⚽ GOLURI TOTALE/MECI")
    lines.append(f"   Medie: {stats['goals']['avg']}/meci")
    for t, pct in stats["goals"]["probs"].items():
        lines.append(f"   {t} goluri : {prob_bar(pct)}")

    lines.append("\n🟢 GOLURI MARCATE")
    lines.append(f"   Medie: {stats['scored']['avg']}/meci")
    for t, pct in stats["scored"]["probs"].items():
        lines.append(f"   {t} goluri marcate : {prob_bar(pct)}")

    lines.append("\n🔴 GOLURI PRIMITE")
    lines.append(f"   Medie: {stats['conceded']['avg']}/meci")
    for t, pct in stats["conceded"]["probs"].items():
        lines.append(f"   {t} goluri primite : {prob_bar(pct)}")

    return "\n".join(lines)

def format_combined_stats(combined, home_name, away_name):
    """
    Ce face:
        Formateaza statisticile combinate ale celor doua echipe intr-un text cu
        bare de progres (goluri totale estimate, marcate si primite combinate).

    Variabile:
        combined: statisticile combinate (din combine_stats).
        home_name / away_name: numele echipelor pentru titlu.
        prob_bar: functie interna care deseneaza o bara text pentru un procent.
        lines: liniile textului rezultat.

    Erori:
        Ridica KeyError daca structura combined nu contine cheile asteptate.
    """
    def prob_bar(pct):
        filled = int(pct / 10)
        return f"[{'█' * filled}{'░' * (10 - filled)}] {pct}%"

    lines = [f"\n🔀 COMBINAT ({home_name} + {away_name})\n"]

    lines.append("⚽ GOLURI TOTALE ESTIMATE")
    lines.append(f"   Medie estimată: {combined['goals']['avg']}/meci")
    for t, pct in combined["goals"]["probs"].items():
        lines.append(f"   {t} goluri : {prob_bar(pct)}")

    lines.append("\n🟢 GOLURI MARCATE COMBINATE")
    lines.append(f"   Medie estimată: {combined['scored']['avg']}/meci")
    for t, pct in combined["scored"]["probs"].items():
        lines.append(f"   {t} goluri marcate : {prob_bar(pct)}")

    lines.append("\n🔴 GOLURI PRIMITE COMBINATE")
    lines.append(f"   Medie estimată: {combined['conceded']['avg']}/meci")
    for t, pct in combined["conceded"]["probs"].items():
        lines.append(f"   {t} goluri primite : {prob_bar(pct)}")

    return "\n".join(lines)
