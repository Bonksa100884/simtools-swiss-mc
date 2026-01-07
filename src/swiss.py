import numpy as np

# fester Zufalls-Seed, damit Ergebnisse reproduzierbar sind
rng = np.random.default_rng(42)

# -------------------------
# PARAMETER
# -------------------------
WEAK_ELO_THRESHOLD = 1500   # "schwach" = Elo < X
N_TEAMS = 36
DRAW_PROB = 0.25
N_SEASONS = 20000  # kannst du später hochdrehen


# -------------------------
# TEAM-STÄRKEN GENERIEREN
# -------------------------
# Plausible Verteilung: 8 top, 10 stark, 10 mittel, 8 schwach
def generate_teams():
    teams = []

    # 8 Top-Teams (1850–2050)
    for i in range(8):
        teams.append(("Team_Top_" + str(i + 1), rng.integers(1850, 2051)))

    # 10 starke (1750–1850)
    for i in range(10):
        teams.append(("Team_Strong_" + str(i + 1), rng.integers(1750, 1850)))

    # 10 mittlere (1550–1750)
    for i in range(10):
        teams.append(("Team_Mid_" + str(i + 1), rng.integers(1550, 1750)))

    # 8 schwache (1350–1550)
    for i in range(8):
        teams.append(("Team_Weak_" + str(i + 1), rng.integers(1350, 1550)))

    rng.shuffle(teams)
    return teams  # Liste von (name, elo)


# -------------------------
# SPIELMODELL (Elo + Remis)
# -------------------------
def win_probability(elo_a, elo_b):
    return 1.0 / (1.0 + 10 ** (-(elo_a - elo_b) / 400.0))


def simulate_match(elo_a, elo_b):
    p_win_a = win_probability(elo_a, elo_b)
    p_draw = DRAW_PROB

    # Rest (1 - p_draw) teilen wir proportional auf Sieg/Niederlage auf
    p_win_a_adj = (1 - p_draw) * p_win_a

    r = rng.random()
    if r < p_draw:
        return (1, 1)   # Remis
    elif r < p_draw + p_win_a_adj:
        return (3, 0)   # A gewinnt
    else:
        return (0, 3)   # B gewinnt


# -------------------------
# SWISS: 4 TÖPFE + 2 GEGNER JE TOPF
# -------------------------
def make_pots_by_elo(teams):
    # sortiere nach Elo absteigend
    teams_sorted = sorted(teams, key=lambda x: x[1], reverse=True)

    # 4 Töpfe à 9 Teams
    pot1 = teams_sorted[0:9]
    pot2 = teams_sorted[9:18]
    pot3 = teams_sorted[18:27]
    pot4 = teams_sorted[27:36]

    return [pot1, pot2, pot3, pot4]


def simulate_swiss_league_phase(teams):
    points = np.zeros(len(teams), dtype=int)

    pots = make_pots_by_elo(teams)

    # name -> index, damit wir Gegner schnell finden
    name_to_idx = {}
    for i in range(len(teams)):
        name_to_idx[teams[i][0]] = i

    # Für jedes Team: 2 Gegner aus jedem Topf ziehen (8 Spiele total)
    for i in range(len(teams)):
        name_i, elo_i = teams[i]
        opponents = set()

        for pot in pots:
            candidates = []

            for (name_j, elo_j) in pot:
                j = name_to_idx[name_j]
                if j != i and j not in opponents:
                    candidates.append(j)

            pick = rng.choice(candidates, size=2, replace=False)
            for j in pick:
                opponents.add(j)

        # Spiele simulieren
        for j in opponents:
            _, elo_j = teams[j]
            pi, pj = simulate_match(elo_i, elo_j)
            points[i] += pi

        # Hinweis: Wir addieren pj NICHT zu Team j,
        # da jedes Team seine eigenen 8 Spiele "zieht".
        # -> einfache, stabile Approximation.

    return points


# -------------------------
# EINE SAISON AUSWERTEN
# -------------------------
def simulate_one_swiss_season():
    teams = generate_teams()
    points = simulate_swiss_league_phase(teams)

    # Ranking nach Punkten (absteigend)
    order = np.argsort(-points)
    ranked = [(teams[k][0], teams[k][1], int(points[k])) for k in order]

    top8 = ranked[:8]
    top24 = ranked[:24]

    weak_in_top8 = 0
    weak_in_top24 = 0

    for (name, elo, pts) in top8:
        if elo < WEAK_ELO_THRESHOLD:
            weak_in_top8 += 1

    for (name, elo, pts) in top24:
        if elo < WEAK_ELO_THRESHOLD:
            weak_in_top24 += 1

    return weak_in_top8, weak_in_top24


# -------------------------
# MONTE CARLO
# -------------------------
def run_swiss_simulation(n_seasons=N_SEASONS):
    total_w8 = 0
    total_w24 = 0

    for _ in range(n_seasons):
        w8, w24 = simulate_one_swiss_season()
        total_w8 += w8
        total_w24 += w24

    print("-----------------------------------------")
    print("SWISS (simpel): 4 Pots, 2 Gegner je Pot")
    print(f"Elo-Schwelle (schwach): < {WEAK_ELO_THRESHOLD}")
    print(f"Spiele pro Team: 8")
    print(f"Remis-Wahrscheinlichkeit: {DRAW_PROB:.2f}")
    print(f"Simulierte Saisons: {n_seasons}")
    print("-----------------------------------------")
    print(f"Ø schwache Teams in TOP 8 :  {total_w8 / n_seasons:.2f} pro Saison")
    print(f"Ø schwache Teams in TOP 24:  {total_w24 / n_seasons:.2f} pro Saison")
    print("Hinweis: vereinfachtes Swiss (keine UEFA-Draw-Constraints, keine Tiebreaker).")
    print("-----------------------------------------")
    
    return total_w8 / n_seasons, total_w24 / n_seasons


if __name__ == "__main__":
    run_swiss_simulation()

