import numpy as np

# fester Zufalls-Seed
rng = np.random.default_rng(42)

# -------------------------
# PARAMETER
# -------------------------
WEAK_ELO_THRESHOLD = 1500
DRAW_PROB = 0.25
N_SEASONS = 20000


# -------------------------
# TEAM-STÄRKEN (32 TEAMS)
# -------------------------
def generate_teams_32():
    teams = []

    # 8 Top
    for i in range(8):
        teams.append(("Team_Top_" + str(i+1), rng.integers(1850, 2051)))

    # 8 stark
    for i in range(8):
        teams.append(("Team_Strong_" + str(i+1), rng.integers(1750, 1850)))

    # 8 mittel
    for i in range(8):
        teams.append(("Team_Mid_" + str(i+1), rng.integers(1550, 1750)))

    # 8 schwach
    for i in range(8):
        teams.append(("Team_Weak_" + str(i+1), rng.integers(1350, 1550)))

    rng.shuffle(teams)
    return teams  # (name, elo)


# -------------------------
# SPIELMODELL
# -------------------------
def win_probability(elo_a, elo_b):
    return 1.0 / (1.0 + 10 ** (-(elo_a - elo_b) / 400.0))

def simulate_match(elo_a, elo_b):
    p_win_a = win_probability(elo_a, elo_b)
    p_draw = DRAW_PROB

    p_win_a_adj = (1 - p_draw) * p_win_a

    r = rng.random()
    if r < p_draw:
        return (1, 1)
    elif r < p_draw + p_win_a_adj:
        return (3, 0)
    else:
        return (0, 3)


# -------------------------
# GRUPPENPHASE SIMULIEREN
# -------------------------
def simulate_group_stage(teams):
    points = np.zeros(len(teams), dtype=int)

    # 8 Gruppen à 4 Teams
    indices = np.arange(32)
    rng.shuffle(indices)
    groups = [indices[i*4:(i+1)*4] for i in range(8)]

    # Jede Gruppe: Hin- & Rückrunde
    for group in groups:
        for i in range(4):
            for j in range(i + 1, 4):
                a = group[i]
                b = group[j]

                _, elo_a = teams[a]
                _, elo_b = teams[b]

                # Spiel 1
                pa, pb = simulate_match(elo_a, elo_b)
                points[a] += pa
                points[b] += pb

                # Spiel 2 (Rückspiel)
                pa, pb = simulate_match(elo_a, elo_b)
                points[a] += pa
                points[b] += pb

    return groups, points


# -------------------------
# EINE SAISON AUSWERTEN
# -------------------------
def simulate_one_baseline_season():
    teams = generate_teams_32()
    groups, points = simulate_group_stage(teams)

    weak_qualified = 0       # schwache Teams in Top 2
    weak_group_winner = 0    # schwache Gruppensieger

    for group in groups:
        # Ranking innerhalb der Gruppe
        ranked = sorted(group, key=lambda i: points[i], reverse=True)

        top2 = ranked[:2]
        winner = ranked[0]

        # Top 2 zählen
        for i in top2:
            if teams[i][1] < WEAK_ELO_THRESHOLD:
                weak_qualified += 1

        # Gruppensieger
        if teams[winner][1] < WEAK_ELO_THRESHOLD:
            weak_group_winner += 1

    return weak_qualified, weak_group_winner


# -------------------------
# MONTE CARLO
# -------------------------
def run_baseline_simulation(n_seasons=N_SEASONS):
    total_qualified = 0
    total_winners = 0

    for _ in range(n_seasons):
        q, w = simulate_one_baseline_season()
        total_qualified += q
        total_winners += w

    print("-----------------------------------------")
    print("BASELINE (alt): Gruppenphase")
    print("32 Teams, 8 Gruppen, Hin- & Rückrunde")
    print(f"Elo-Schwelle (schwach): < {WEAK_ELO_THRESHOLD}")
    print(f"Remis-Wahrscheinlichkeit: {DRAW_PROB:.2f}")
    print(f"Simulierte Saisons: {n_seasons}")
    print("-----------------------------------------")
    print(f"Ø schwache Teams im Achtelfinale (Top 2): {total_qualified / n_seasons:.2f}")
    print(f"Ø schwache Gruppensieger (8 Gruppen):     {total_winners / n_seasons:.2f}")
    print("Hinweis: keine Tiebreaker, vereinfachtes Modell.")
    print("-----------------------------------------")

    return total_qualified / n_seasons, total_winners / n_seasons


if __name__ == "__main__":
    run_baseline_simulation()
