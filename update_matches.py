import json
import os

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(DIRECTORY, 'predictions.json')

ratings = {
    "Argentina": 9.8,
    "Spain": 9.5,
    "France": 9.4,
    "England": 9.3,
    "Portugal": 8.8,
    "Germany": 8.5,
    "Brazil": 8.3,
    "Japan": 8.2,
    "Norway": 8.1,
    "Morocco": 8.0,
    "Uruguay": 7.8,
    "United States": 8.2,
    "Colombia": 7.6,
    "Egypt": 7.5,
    "Ecuador": 7.4,
    "South Korea": 7.3,
    "Netherlands": 7.2,
    "Canada": 7.2,
    "Croatia": 7.1,
    "Ivory Coast": 7.0,
    "Senegal": 6.9,
    "Switzerland": 6.8,
    "Czechia": 6.5,
    "Türkiye": 6.4,
    "Austria": 6.3,
    "Paraguay": 6.2,
    "Australia": 6.1,
    "Sweden": 6.0,
    "Bosnia & Herzegovina": 5.8,
    "Scotland": 6.2,
    "Ghana": 5.7,
    "Tunisia": 5.6,
    "Saudi Arabia": 5.5,
    "South Africa": 5.4,
    "Uzbekistan": 5.2,
    "Cape Verde": 5.1,
    "DR Congo": 5.0,
    "Iraq": 4.8,
    "Algeria": 4.7,
    "Jordan": 4.5,
    "Qatar": 4.3,
    "Panama": 4.2,
    "Curaçao": 4.0,
    "Haiti": 3.8,
    "New Zealand": 3.6,
    "Iran": 3.5,
    "Mexico": 7.5
}

def predict_winner(t_a, t_b):
    if t_a == "Netherlands" and t_b == "Japan":
        return "Japan"
    elif t_a == "Japan" and t_b == "Netherlands":
        return "Japan"
    elif t_a == "France" and t_b == "Norway":
        return "Norway or Draw"
    elif t_a == "Norway" and t_b == "France":
        return "Norway or Draw"
    elif t_a == "Brazil" and t_b == "Morocco":
        return "Morocco or Draw"
    elif t_a == "Morocco" and t_b == "Brazil":
        return "Morocco or Draw"
    
    r_a = ratings.get(t_a, 5.0)
    r_b = ratings.get(t_b, 5.0)
    diff = r_a - r_b
    if abs(diff) < 0.5:
        return "Draw"
    elif diff > 0:
        return t_a
    else:
        return t_b

raw_matches = [
    # June 11
    {"date": "June 11, 2026", "match": "Mexico vs South Africa", "group": "A", "score": "2-0"},
    {"date": "June 11, 2026", "match": "South Korea vs Czechia", "group": "A", "score": "2-1"},
    # June 12
    {"date": "June 12, 2026", "match": "Canada vs Bosnia & Herzegovina", "group": "B", "score": "1-1"},
    {"date": "June 12, 2026", "match": "United States vs Paraguay", "group": "D", "score": "4-1"},
    # June 13
    {"date": "June 13, 2026", "match": "Qatar vs Switzerland", "group": "B", "score": "1-1"},
    {"date": "June 13, 2026", "match": "Brazil vs Morocco", "group": "C", "score": "1-1"},
    {"date": "June 13, 2026", "match": "Haiti vs Scotland", "group": "C", "score": "0-1"},
    {"date": "June 13, 2026", "match": "Australia vs Türkiye", "group": "D", "score": "2-0"},
    # June 14
    {"date": "June 14, 2026", "match": "Germany vs Curaçao", "group": "E", "score": "7-1"},
    {"date": "June 14, 2026", "match": "Netherlands vs Japan", "group": "F", "score": "2-2"},
    {"date": "June 14, 2026", "match": "Ivory Coast vs Ecuador", "group": "E", "score": "1-0"},
    {"date": "June 14, 2026", "match": "Sweden vs Tunisia", "group": "F", "score": "5-1"},
    # June 15
    {"date": "June 15, 2026", "match": "Spain vs Cape Verde", "group": "H", "score": "0-0"},
    {"date": "June 15, 2026", "match": "Belgium vs Egypt", "group": "G", "score": "1-1"},
    {"date": "June 15, 2026", "match": "Saudi Arabia vs Uruguay", "group": "H", "score": "1-1"},
    {"date": "June 15, 2026", "match": "Iran vs New Zealand", "group": "G", "score": "2-2"},
    # June 16
    {"date": "June 16, 2026", "match": "France vs Senegal", "group": "I", "score": "3-1"},
    {"date": "June 16, 2026", "match": "Iraq vs Norway", "group": "I", "score": "1-4"},
    {"date": "June 16, 2026", "match": "Argentina vs Algeria", "group": "J", "score": "2-0"},
    {"date": "June 16, 2026", "match": "Austria vs Jordan", "group": "J", "score": ""},
    # June 17
    {"date": "June 17, 2026", "match": "Portugal vs DR Congo", "group": "K", "score": ""},
    {"date": "June 17, 2026", "match": "England vs Croatia", "group": "L", "score": ""},
    {"date": "June 17, 2026", "match": "Ghana vs Panama", "group": "L", "score": ""},
    {"date": "June 17, 2026", "match": "Uzbekistan vs Colombia", "group": "K", "score": ""},
    # June 18
    {"date": "June 18, 2026", "match": "Czechia vs South Africa", "group": "A", "score": ""},
    {"date": "June 18, 2026", "match": "Switzerland vs Bosnia & Herzegovina", "group": "B", "score": ""},
    {"date": "June 18, 2026", "match": "Canada vs Qatar", "group": "B", "score": ""},
    {"date": "June 18, 2026", "match": "Mexico vs South Korea", "group": "A", "score": ""},
    # June 19
    {"date": "June 19, 2026", "match": "United States vs Australia", "group": "D", "score": ""},
    {"date": "June 19, 2026", "match": "Scotland vs Morocco", "group": "C", "score": ""},
    {"date": "June 19, 2026", "match": "Brazil vs Haiti", "group": "C", "score": ""},
    {"date": "June 19, 2026", "match": "Türkiye vs Paraguay", "group": "D", "score": ""},
    # June 20
    {"date": "June 20, 2026", "match": "Netherlands vs Sweden", "group": "F", "score": ""},
    {"date": "June 20, 2026", "match": "Germany vs Ivory Coast", "group": "E", "score": ""},
    {"date": "June 20, 2026", "match": "Ecuador vs Curaçao", "group": "E", "score": ""},
    {"date": "June 20, 2026", "match": "Tunisia vs Japan", "group": "F", "score": ""},
    # June 21
    {"date": "June 21, 2026", "match": "Spain vs Saudi Arabia", "group": "H", "score": ""},
    {"date": "June 21, 2026", "match": "Belgium vs Iran", "group": "G", "score": ""},
    {"date": "June 21, 2026", "match": "Uruguay vs Cape Verde", "group": "H", "score": ""},
    {"date": "June 21, 2026", "match": "New Zealand vs Egypt", "group": "G", "score": ""},
    # June 22
    {"date": "June 22, 2026", "match": "Argentina vs Austria", "group": "J", "score": ""},
    {"date": "June 22, 2026", "match": "France vs Iraq", "group": "I", "score": ""},
    {"date": "June 22, 2026", "match": "Norway vs Senegal", "group": "I", "score": ""},
    {"date": "June 22, 2026", "match": "Jordan vs Algeria", "group": "J", "score": ""},
    # June 23
    {"date": "June 23, 2026", "match": "Portugal vs Uzbekistan", "group": "K", "score": ""},
    {"date": "June 23, 2026", "match": "England vs Ghana", "group": "L", "score": ""},
    {"date": "June 23, 2026", "match": "Panama vs Croatia", "group": "L", "score": ""},
    {"date": "June 23, 2026", "match": "Colombia vs DR Congo", "group": "K", "score": ""},
    # June 24
    {"date": "June 24, 2026", "match": "Switzerland vs Canada", "group": "B", "score": ""},
    {"date": "June 24, 2026", "match": "Bosnia & Herzegovina vs Qatar", "group": "B", "score": ""},
    {"date": "June 24, 2026", "match": "Scotland vs Brazil", "group": "C", "score": ""},
    {"date": "June 24, 2026", "match": "Morocco vs Haiti", "group": "C", "score": ""},
    {"date": "June 24, 2026", "match": "Czechia vs Mexico", "group": "A", "score": ""},
    {"date": "June 24, 2026", "match": "South Africa vs South Korea", "group": "A", "score": ""},
    # June 25
    {"date": "June 25, 2026", "match": "Ecuador vs Germany", "group": "E", "score": ""},
    {"date": "June 25, 2026", "match": "Curaçao vs Ivory Coast", "group": "E", "score": ""},
    {"date": "June 25, 2026", "match": "Tunisia vs Netherlands", "group": "F", "score": ""},
    {"date": "June 25, 2026", "match": "Japan vs Sweden", "group": "F", "score": ""},
    {"date": "June 25, 2026", "match": "Türkiye vs United States", "group": "D", "score": ""},
    {"date": "June 25, 2026", "match": "Paraguay vs Australia", "group": "D", "score": ""},
    # June 26
    {"date": "June 26, 2026", "match": "Norway vs France", "group": "I", "score": ""},
    {"date": "June 26, 2026", "match": "Senegal vs Iraq", "group": "I", "score": ""},
    {"date": "June 26, 2026", "match": "Uruguay vs Spain", "group": "H", "score": ""},
    {"date": "June 26, 2026", "match": "Cape Verde vs Saudi Arabia", "group": "H", "score": ""},
    {"date": "June 26, 2026", "match": "New Zealand vs Belgium", "group": "G", "score": ""},
    {"date": "June 26, 2026", "match": "Egypt vs Iran", "group": "G", "score": ""},
    # June 27
    {"date": "June 27, 2026", "match": "Panama vs England", "group": "L", "score": ""},
    {"date": "June 27, 2026", "match": "Croatia vs Ghana", "group": "L", "score": ""},
    {"date": "June 27, 2026", "match": "Colombia vs Portugal", "group": "K", "score": ""},
    {"date": "June 27, 2026", "match": "DR Congo vs Uzbekistan", "group": "K", "score": ""},
    {"date": "June 27, 2026", "match": "Jordan vs Argentina", "group": "J", "score": ""},
    {"date": "June 27, 2026", "match": "Algeria vs Austria", "group": "J", "score": ""}
]

processed_matches = []
match_id = 1

for raw in raw_matches:
    teams = [t.strip() for t in raw["match"].split(" vs ")]
    t_a, t_b = teams[0], teams[1]
    
    pred = predict_winner(t_a, t_b)
    
    score = raw["score"]
    status = "pending"
    
    if score:
        # Determine actual winner
        score_a, score_b = map(int, score.split("-"))
        if score_a > score_b:
            actual_winner = t_a
        elif score_b > score_a:
            actual_winner = t_b
        else:
            actual_winner = "Draw"
            
        # Match prediction
        if pred == "Draw":
            status = "pass" if actual_winner == "Draw" else "fail"
        elif "or Draw" in pred:
            main_team = pred.replace(" or Draw", "").strip()
            status = "pass" if (actual_winner == main_team or actual_winner == "Draw") else "fail"
        else:
            status = "pass" if actual_winner == pred else "fail"
            
    processed_matches.append({
        "id": f"m{match_id}",
        "group": raw["group"],
        "match": raw["match"],
        "date": raw["date"],
        "predicted_winner": pred,
        "score": score,
        "status": status
    })
    match_id += 1

# Load predictions.json
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update match list
data["key_matches"] = processed_matches

# Also update special upsets results if Netherlands vs Japan was completed
for upset in data.get("special_upsets", []):
    if upset["description"] == "Japan to beat Netherlands in Group F":
        upset["actual_result"] = "2-2 Draw"
        upset["status"] = "fail"

# Save predictions.json
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Successfully updated predictions.json with {len(processed_matches)} schedule matches and declared results for completed matches!")
