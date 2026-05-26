from repository.api_repo import get_upcoming_matches, get_recent_matches, LEAGUES

for name, code in LEAGUES.items():
    print(f"\n=== {name} - Urmatoarele meciuri ===")
    for m in get_upcoming_matches(code):
        print(m)

