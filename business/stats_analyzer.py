from repository.api_repo import get_match_stats_history

def calculate_probabilities(values, thresholds):
    if not values:
        return {}
    result = {}
    for t in thresholds:
        over = sum(1 for v in values if v > t)
        result[f"peste {t}"] = round(over / len(values) * 100, 1)
    return result

def get_team_stats(team_id, count=10):
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