import requests

API_KEY = "ab07e1d2c31c4df5a1a56a1d44ffb1aa"
BASE_URL = "https://api.football-data.org/v4"

headers = {"X-Auth-Token": API_KEY}

LEAGUES = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Serie A": "SA",
    "Eredivisie": "DED",
    "Champions League": "CL",
    "Liga de Portugal": "PPL",
    "Bundesliga": "BL1",
    "Ligue 1": "FL1",
}

def get_upcoming_matches(league_code):
    """
    Ce face:
        Interogheaza API-ul pentru urmatoarele meciuri programate dintr-o liga
        si returneaza pana la 10 meciuri formatate ca "data | gazda vs oaspete".

    Variabile:
        league_code: codul ligii (ex: "PL").
        url / params: adresa si parametrii cererii HTTP.
        response / data: raspunsul brut si JSON-ul deserializat.

    Erori:
        Daca raspunsul nu contine "matches" (ex: liga indisponibila pe planul
        Free) returneaza o lista cu un mesaj explicativ. Propaga erorile de retea.
    """
    url = f"{BASE_URL}/competitions/{league_code}/matches"
    params = {"status": "SCHEDULED"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "matches" not in data:
        return [f"Liga {league_code} nu este disponibila pe planul Free."]

    matches = []
    for match in data["matches"][:10]:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        date = match["utcDate"][:10]
        matches.append(f"{date} | {home} vs {away}")

    return matches

def get_recent_matches(league_code):
    """
    Ce face:
        Interogheaza API-ul pentru ultimele meciuri incheiate dintr-o liga si
        returneaza ultimele 10 cu scor, formatate ca "data | gazda scor away".

    Variabile:
        league_code: codul ligii.
        url / params: adresa si parametrii cererii HTTP.
        response / data: raspunsul brut si JSON-ul deserializat.

    Erori:
        Ridica KeyError daca raspunsul nu contine "matches". Propaga erorile de retea.
    """
    url = f"{BASE_URL}/competitions/{league_code}/matches"
    params = {"status": "FINISHED"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    matches = []
    for match in data["matches"][-10:]:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        score_h = match["score"]["fullTime"]["home"]
        score_a = match["score"]["fullTime"]["away"]
        date = match["utcDate"][:10]
        matches.append(f"{date} | {home} {score_h}-{score_a} {away}")

    return matches

def get_recent_form_detailed(team_id, count=5):
    """
    Ce face:
        Extrage forma recenta a unei echipe: pentru fiecare meci determina
        rezultatul (W/D/L) din perspectiva echipei si golurile marcate/primite.

    Variabile:
        team_id: id-ul echipei analizate.
        count: numarul de meciuri (implicit 5).
        url / params: adresa si parametrii cererii HTTP.
        response / data: raspunsul brut si JSON-ul deserializat.
        form: lista rezultatelor cu result/goals_scored/goals_conceded.

    Erori:
        Ridica KeyError daca raspunsul nu contine "matches". Propaga erorile de retea.
    """
    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {"status": "FINISHED", "limit": count}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    form = []
    for match in data["matches"][-count:]:
        home_id = match["homeTeam"]["id"]
        home_score = match["score"]["fullTime"]["home"]
        away_score = match["score"]["fullTime"]["away"]

        if home_id == team_id:
            goals_scored = home_score
            goals_conceded = away_score
            if home_score > away_score:
                result = "W"
            elif home_score == away_score:
                result = "D"
            else:
                result = "L"
        else:
            goals_scored = away_score
            goals_conceded = home_score
            if away_score > home_score:
                result = "W"
            elif home_score == away_score:
                result = "D"
            else:
                result = "L"

        form.append({
            "result": result,
            "goals_scored": goals_scored,
            "goals_conceded": goals_conceded
        })

    return form

def get_teams(league_code):
    """
    Ce face:
        Returneaza un dictionar {nume_echipa: id} cu echipele dintr-o liga.

    Variabile:
        league_code: codul ligii.
        url / response / data: cererea HTTP si JSON-ul deserializat.
        teams: dictionarul rezultat.

    Erori:
        Ridica KeyError daca raspunsul nu contine "teams". Propaga erorile de retea.
    """
    url = f"{BASE_URL}/competitions/{league_code}/teams"
    response = requests.get(url, headers=headers)
    data = response.json()

    teams = {}
    for team in data["teams"]:
        teams[team["name"]] = team["id"]
    return teams

def get_head_to_head(team1_id, team2_id, count=5):
    """
    Ce face:
        Cauta in ultimele meciuri ale primei echipe intalnirile directe cu a doua
        echipa si returneaza pana la count meciuri directe cu scorurile lor.

    Variabile:
        team1_id / team2_id: id-urile celor doua echipe.
        count: numarul maxim de meciuri directe returnate (implicit 5).
        url / params / response / data: cererea HTTP si JSON-ul deserializat.
        h2h: lista meciurilor directe gasite.

    Erori:
        Ridica KeyError daca raspunsul nu contine "matches". Propaga erorile de retea.
    """
    url = f"{BASE_URL}/teams/{team1_id}/matches"
    params = {"status": "FINISHED", "limit": 50}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    h2h = []
    for match in data["matches"]:
        home_id = match["homeTeam"]["id"]
        away_id = match["awayTeam"]["id"]

        if (home_id == team1_id and away_id == team2_id) or \
           (home_id == team2_id and away_id == team1_id):
            home_score = match["score"]["fullTime"]["home"]
            away_score = match["score"]["fullTime"]["away"]
            h2h.append({
                "home_id": home_id,
                "away_id": away_id,
                "home_score": home_score,
                "away_score": away_score
            })

        if len(h2h) == count:
            break

    return h2h

def get_standings(league_code):
    """
    Ce face:
        Returneaza clasamentul ligii ca dictionar indexat pe id de echipa, cu
        pozitie, puncte, victorii/egaluri/infrangeri si golaveraj.

    Variabile:
        league_code: codul ligii.
        url / response / data: cererea HTTP si JSON-ul deserializat.
        standings: dictionarul rezultat.

    Erori:
        Ridica KeyError/IndexError daca raspunsul nu contine structura de
        clasament asteptata. Propaga erorile de retea.
    """
    url = f"{BASE_URL}/competitions/{league_code}/standings"
    response = requests.get(url, headers=headers)
    data = response.json()

    standings = {}
    for team in data["standings"][0]["table"]:
        standings[team["team"]["id"]] = {
            "position": team["position"],
            "points": team["points"],
            "won": team["won"],
            "draw": team["draw"],
            "lost": team["lost"],
            "goalsFor": team["goalsFor"],
            "goalsAgainst": team["goalsAgainst"]
        }
    return standings

def get_match_stats_history(team_id, count=10):
    """
    Ce face:
        Extrage istoricul de statistici al unei echipe: pentru fiecare meci
        calculeaza golurile totale si golurile marcate/primite de echipa.

    Variabile:
        team_id: id-ul echipei.
        count: numarul de meciuri (implicit 10).
        url / params / response / data: cererea HTTP si JSON-ul deserializat.
        stats: lista dictionarelor cu goals/scored/conceded.

    Erori:
        Daca raspunsul nu contine "matches" returneaza lista goala. Scorurile
        None sunt tratate ca 0. Propaga erorile de retea.
    """
    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {"status": "FINISHED", "limit": count}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "matches" not in data:
        return []

    stats = []
    for match in data["matches"]:
        home_score = match["score"]["fullTime"]["home"] or 0
        away_score = match["score"]["fullTime"]["away"] or 0
        team_id_check = match["homeTeam"]["id"]

        if team_id_check == team_id:
            scored = home_score
            conceded = away_score
        else:
            scored = away_score
            conceded = home_score

        stats.append({
            "goals": home_score + away_score,
            "scored": scored,
            "conceded": conceded,
        })

    return stats
