import csv

WEAK_ELO_THRESHOLD = 1500

def load_elo_map(path):
    elo = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = row["team"].strip()
            elo_val = float(row["elo"])
            elo[team] = elo_val
    return elo

def load_real_list(path):
    top8 = []
    top24 = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = row["team"].strip()
            grp = row["group"].strip()
            if grp == "top8":
                top8.append(team)
                top24.append(team)
            elif grp == "9-24":
                top24.append(team)
    return top8, top24

def count_weak(teams, elo_map):
    weak = 0
    for t in teams:
        if t in elo_map and elo_map[t] < WEAK_ELO_THRESHOLD:
            weak += 1
    return weak

def main():
    elo_map = load_elo_map("data/clubelo_snapshot.csv")
    top8, top24 = load_real_list("data/real_swiss_2024_25_top24.csv")

    weak8 = count_weak(top8, elo_map)
    weak24 = count_weak(top24, elo_map)

    print("REAL-LIFE CHECK (Swiss / League Phase 2024/25)")
    print(f"Weak threshold: Elo < {WEAK_ELO_THRESHOLD}")
    print(f"Weak teams in Top 8 : {weak8} / 8")
    print(f"Weak teams in Top 24: {weak24} / 24")

if __name__ == "__main__":
    main()
