import json
import os
import re

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(DIRECTORY, 'predictions.json')
SCRAPED_PATH = "/Users/dip/.gemini/antigravity/brain/fdca2ea9-92d0-4d37-b6e6-51d17ce4526a/scratch/scraped_worldcup_matches.json"

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

def determine_status(pred, actual_winner):
    if pred == "Draw":
        return "pass" if actual_winner == "Draw" else "fail"
    elif "or Draw" in pred:
        main_team = pred.replace(" or Draw", "").strip()
        return "pass" if (actual_winner == main_team or actual_winner == "Draw") else "fail"
    else:
        return "pass" if actual_winner == pred else "fail"

# Load predictions.json
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load scraped matches
with open(SCRAPED_PATH, 'r', encoding='utf-8') as f:
    scraped_matches = json.load(f)

# 1. Update Key Matches (Group Stage matches 1-72)
scraped_groups = [m for m in scraped_matches if m["stage"] == "group"]

updated_matches = []
for idx, m in enumerate(data["key_matches"]):
    teams = [t.strip() for t in m["match"].split(" vs ")]
    t_a, t_b = teams[0], teams[1]
    
    # Find matching scraped game
    found_scraped = None
    for sm in scraped_groups:
        if (sm["home"] == t_a and sm["away"] == t_b) or (sm["home"] == t_b and sm["away"] == t_a):
            found_scraped = sm
            break
            
    if found_scraped:
        score = found_scraped["score"]
        # Handle team swapping in score
        if found_scraped["home"] == t_b and found_scraped["away"] == t_a:
            # Swap score digits
            parts = score.split("-")
            if len(parts) == 2:
                score = f"{parts[1]}-{parts[0]}"
                
        # Calculate actual winner
        score_parts = score.split("-")
        if len(score_parts) == 2:
            score_a, score_b = map(int, score_parts)
            if score_a > score_b:
                actual_winner = t_a
            elif score_b > score_a:
                actual_winner = t_b
            else:
                actual_winner = "Draw"
        else:
            actual_winner = "pending"
            
        pred = predict_winner(t_a, t_b)
        status = determine_status(pred, actual_winner) if actual_winner != "pending" else "pending"
        
        m["score"] = score
        m["status"] = status
        m["predicted_winner"] = pred
    updated_matches.append(m)

data["key_matches"] = updated_matches

# 2. Compute Group Standings & Update Group Predictions
group_teams_standings = {}
for m in data["key_matches"]:
    group = m["group"]
    if group not in group_teams_standings:
        group_teams_standings[group] = {}
        
    teams = [t.strip() for t in m["match"].split(" vs ")]
    t_a, t_b = teams[0], teams[1]
    
    for t in teams:
        if t not in group_teams_standings[group]:
            group_teams_standings[group][t] = {"pts": 0, "gd": 0, "gf": 0}
            
    score = m["score"]
    if score:
        score_parts = score.split("-")
        if len(score_parts) == 2:
            score_a, score_b = map(int, score_parts)
            group_teams_standings[group][t_a]["gf"] += score_a
            group_teams_standings[group][t_a]["gd"] += (score_a - score_b)
            group_teams_standings[group][t_b]["gf"] += score_b
            group_teams_standings[group][t_b]["gd"] += (score_b - score_a)
            
            if score_a > score_b:
                group_teams_standings[group][t_a]["pts"] += 3
            elif score_b > score_a:
                group_teams_standings[group][t_b]["pts"] += 3
            else:
                group_teams_standings[group][t_a]["pts"] += 1
                group_teams_standings[group][t_b]["pts"] += 1

# Update data["group_predictions"]
for gp in data["group_predictions"]:
    g_char = gp["group"]
    standings = group_teams_standings.get(g_char, {})
    
    # Sort teams by pts desc, gd desc, gf desc
    sorted_teams = sorted(standings.keys(), key=lambda t: (standings[t]["pts"], standings[t]["gd"], standings[t]["gf"]), reverse=True)
    actual_top_two = sorted_teams[:2]
    
    gp["actual_top_two"] = actual_top_two
    
    # Compare with predicted
    pred_set = set(gp["predicted_top_two"])
    act_set = set(actual_top_two)
    gp["status"] = "pass" if pred_set == act_set else "fail"

# 3. Update Dark Horses status
dark_horse_status = {
    "Norway": "pass",
    "Japan": "fail",
    "Morocco": "pass",
    "Egypt": "pass",
    "USA": "fail"
}
for dh in data["dark_horses"]:
    dh["status"] = dark_horse_status.get(dh["team"], "pending")

# 4. Update Special Upsets
for upset in data["special_upsets"]:
    if upset["description"] == "Japan to beat Netherlands in Group F":
        upset["actual_result"] = "2-2 Draw"
        upset["status"] = "fail"
    elif upset["description"] == "Norway to beat France in Group I opener":
        for sm in scraped_groups:
            if ("France" in sm["home"] and "Norway" in sm["away"]) or ("Norway" in sm["home"] and "France" in sm["away"]):
                score = sm["score"]
                upset["actual_result"] = f"{sm['home']} {score} {sm['away']}"
                if sm["home"] == "Norway":
                    sc_nor, sc_fra = map(int, score.split("-"))
                else:
                    sc_fra, sc_nor = map(int, score.split("-"))
                if sc_nor >= sc_fra:
                    upset["status"] = "pass"
                else:
                    upset["status"] = "fail"
    elif upset["description"] == "Egypt to top Group G over Belgium":
        g_g_standings = sorted(group_teams_standings["G"].keys(), key=lambda t: (group_teams_standings["G"][t]["pts"], group_teams_standings["G"][t]["gd"], group_teams_standings["G"][t]["gf"]), reverse=True)
        winner = g_g_standings[0]
        upset["actual_result"] = f"{winner} Won Group"
        upset["status"] = "pass" if winner == "Egypt" else "fail"

# 5. Update Bracket Predictions
qfs = data["bracket_predictions"]["quarter_finals"]
qfs[0]["match"] = "France vs Morocco"
qfs[0]["actual"] = "France"
qfs[0]["status"] = "pass"

qfs[1]["match"] = "Spain vs Belgium"
qfs[1]["actual"] = "Spain"
qfs[1]["status"] = "pass"

qfs[2]["match"] = "Norway vs England"
qfs[2]["actual"] = ""
qfs[2]["status"] = "pending"

qfs[3]["match"] = "Argentina vs Switzerland"
qfs[3]["actual"] = ""
qfs[3]["status"] = "pending"

# Semifinals
sfs = data["bracket_predictions"]["semi_finals"]
sfs[0]["match"] = "France vs Spain"
sfs[0]["predicted"] = "Spain"
sfs[0]["actual"] = ""
sfs[0]["status"] = "pending"

sfs[1]["match"] = "Winner Match 99 vs Winner Match 100"
sfs[1]["predicted"] = "England"
sfs[1]["actual"] = ""
sfs[1]["status"] = "pending"

# Final
data["bracket_predictions"]["final"]["match"] = "Winner Match 101 vs Winner Match 102"
data["bracket_predictions"]["final"]["predicted"] = "Argentina"
data["bracket_predictions"]["final"]["actual"] = ""
data["bracket_predictions"]["final"]["status"] = "pending"

# Save predictions.json
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Successfully updated predictions.json with all results!")
