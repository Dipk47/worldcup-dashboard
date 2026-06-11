import json
import os

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(DIRECTORY, 'predictions.json')

# Team ratings based on H2H, recent form, and player analysis (out of 10)
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
    "United States": 7.7,
    "Colombia": 7.6,
    "Egypt": 7.5,
    "Ecuador": 7.4,
    "South Korea": 7.3,
    "Netherlands": 7.2,
    "Croatia": 7.1,
    "Ivory Coast": 7.0,
    "Senegal": 6.9,
    "Switzerland": 6.8,
    "Canada": 6.6,
    "Czechia": 6.5,
    "Türkiye": 6.4,
    "Austria": 6.3,
    "Paraguay": 6.2,
    "Australia": 6.1,
    "Sweden": 6.0,
    "Bosnia & Herzegovina": 5.8,
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
    "Bosnia": 5.8, # Alias
    "Bosnia & Herzegovina": 5.8,
    "Cabo Verde": 5.1, # Alias
    "DR Congo": 5.0
}

# Group structure
groups = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Switzerland", "Qatar", "Bosnia"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Türkiye"],
    "E": ["Germany", "Curaçao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Tunisia", "Sweden"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cabo Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Norway", "Iraq"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "Colombia", "Uzbekistan", "DR Congo"],
    "L": ["England", "Croatia", "Ghana", "Panama"]
}

# Generate 6 matches per group
# Pairing indices for round-robin (6 matches total):
# Match 1: 0 vs 1
# Match 2: 2 vs 3
# Match 3: 0 vs 2
# Match 4: 1 vs 3
# Match 5: 0 vs 3
# Match 6: 1 vs 2
round_pairings = [
    (0, 1, 0), # (team_a_idx, team_b_idx, matchday_offset)
    (2, 3, 1),
    (0, 2, 4),
    (1, 3, 5),
    (0, 3, 12),
    (1, 2, 13)
]

# Base date: June 11, 2026
dates_mapping = {
    0: "June 11, 2026",
    1: "June 12, 2026",
    4: "June 15, 2026",
    5: "June 16, 2026",
    12: "June 23, 2026",
    13: "June 24, 2026"
}

# Custom group offset to stagger matches
group_offsets = {
    "A": 0, "B": 1, "C": 2, "D": 0, "E": 3, "F": 4,
    "G": 1, "H": 2, "I": 4, "J": 2, "K": 5, "L": 0
}

# Override ratings for home nations in Mexico/USA/Canada
ratings["Mexico"] = 7.5 # Home boost (from 6.5)
ratings["United States"] = 8.2 # Home boost (from 7.7)
ratings["Canada"] = 7.2 # Home boost (from 6.6)
ratings["Scotland"] = 6.2 # Decent side
ratings["Belgium"] = 7.2 # Aging generation

matches = []
match_id = 1

for g_name, g_teams in groups.items():
    g_offset = group_offsets[g_name]
    for p in round_pairings:
        t_a = g_teams[p[0]]
        t_b = g_teams[p[1]]
        
        # Calculate match day index
        m_day = p[2] + g_offset
        if m_day > 14:
            m_day = 14
        
        date_str = dates_mapping.get(p[2], "June 25, 2026")
        # Adjust date string based on offset to make it realistic
        # E.g. stagger by 1 or 2 days
        day_val = int(date_str.split(" ")[1].replace(",", ""))
        actual_day = day_val + (g_offset % 3)
        actual_date = f"June {actual_day}, 2026"
        
        # Predict winner based on ratings
        r_a = ratings.get(t_a, 5.0)
        r_b = ratings.get(t_b, 5.0)
        
        # Adjustments for known upsets from our prior analysis
        # - Japan beats Netherlands
        # - Norway draws or beats France
        # - Morocco draws or beats Brazil
        if t_a == "Netherlands" and t_b == "Japan":
            pred = "Japan"
        elif t_a == "Japan" and t_b == "Netherlands":
            pred = "Japan"
        elif t_a == "France" and t_b == "Norway":
            pred = "Norway or Draw"
        elif t_a == "Norway" and t_b == "France":
            pred = "Norway or Draw"
        elif t_a == "Brazil" and t_b == "Morocco":
            pred = "Morocco or Draw"
        elif t_a == "Morocco" and t_b == "Brazil":
            pred = "Morocco or Draw"
        else:
            diff = r_a - r_b
            if abs(diff) < 0.5:
                pred = "Draw"
            elif diff > 0:
                pred = t_a
            else:
                pred = t_b
        
        matches.append({
            "id": f"m{match_id}",
            "group": g_name,
            "match": f"{t_a} vs {t_b}",
            "date": actual_date,
            "predicted_winner": pred,
            "score": "",
            "status": "pending"
        })
        match_id += 1

# Sort matches by date to make it look like a real timeline
def parse_date(m):
    day = int(m["date"].split(" ")[1].replace(",", ""))
    return day

matches.sort(key=parse_date)

# Re-assign IDs in sorted order
for idx, m in enumerate(matches):
    m["id"] = f"m{idx+1}"

# Load existing predictions.json
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update the matches array
data["key_matches"] = matches

# Save back to file
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Generated {len(matches)} group stage matches successfully in predictions.json!")
