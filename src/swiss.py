"""
swiss.py

Monte Carlo simulation of a simplified Champions League Swiss-format league phase.

Core idea:
- 36 teams with synthetic Elo ratings (tiered distribution)
- Match outcomes based on Elo win probabilities + fixed draw probability
- Swiss scheduling is approximated using 4 Elo-based pots:
  each team draws 2 opponents from each pot (8 matches total)

Important simplification:
Points are accumulated per team independently. Opponent points are NOT
added in the same loop (each team "draws its own schedule"), which is a
simple and stable approximation for this project.

Outputs:
- Average number of weak teams (Elo < threshold) reaching Top 8 and Top 24.

Authors:
- Julian Eberl
- Samuel Bonk
- Yannic Leinweber
"""

import numpy as np

# Fixed random seed for reproducibility
rng = np.random.default_rng(42)

# -------------------------
# PARAMETERS
# -------------------------
WEAK_ELO_THRESHOLD = 1500  # weak = Elo < threshold
N_TEAMS = 36
DRAW_PROB = 0.25
N_SEASONS = 20000


# -------------------------
# TEAM GENERATION
# -------------------------
def generate_teams():
    """
    Generate 36 teams with synthetic Elo ratings (tiered distribution).

    Distribution (example):
    - 8 top teams
    - 10 strong teams
    - 10 medium teams
    - 8 weak teams

    Returns
    -------
    list of tuples
        Each tuple contains (team_name, elo_rating).
    """
    teams = []

    # 8 top teams (1850–2050)
    for i in range(8):
        teams.append(("Team_Top_" + str(i + 1), rng.integers(1850, 2051)))

    # 10 strong teams (1750–1850)
    for i in range(10):
        teams.append(("Team_Strong_" + str(i + 1), rng.integers(1750, 1850)))

    # 10 medium teams (1550–1750)
    for i in range(10):
        teams.append(("Team_Mid_" + str(i + 1), rng.integers(1550, 1750)))

    # 8 weak teams (1350–1550)
    for i in range(8):
        teams.append(("Team_Weak_" + str(i + 1), rng.integers(1350, 1550)))

    rng.shuffle(teams)
    return teams


# -------------------------
# MATCH MODEL (ELO + DRAW)
# -------------------------
def win_probability(elo_a, elo_b):
    """
    Compute the win probability of team A against team B using the Elo formula.

    Parameters
    ----------
    elo_a : int
        Elo rating of team A.
    elo_b : int
        Elo rating of team B.

    Returns
    -------
    float
        Probability that team A wins (ignoring draws).
    """
    return 1.0 / (1.0 + 10 ** (-(elo_a - elo_b) / 400.0))


def simulate_match(elo_a, elo_b):
    """
    Simulate a single match between two teams with a fixed draw probability.

    Parameters
    ----------
    elo_a : int
        Elo rating of team A.
    elo_b : int
        Elo rating of team B.

    Returns
    -------
    tuple of int
        Points awarded to (team A, team B):
        - (3, 0) if A wins
        - (1, 1) if draw
        - (0, 3) if B wins
    """
    p_win_a = win_probability(elo_a, elo_b)
    p_draw = DRAW_PROB

    # Allocate non-draw probability according to Elo win chance
    p_win_a_adj = (1 - p_draw) * p_win_a

    r = rng.random()
    if r < p_draw:
        return (1, 1)  # draw
    elif r < p_draw + p_win_a_adj:
        return (3, 0)  # A wins
    else:
        return (0, 3)  # B wins


# -------------------------
# SWISS APPROXIMATION: 4 POTS + 2 OPPONENTS PER POT
# -------------------------
def make_pots_by_elo(teams):
    """
    Split teams into four pots based on Elo ranking (descending).

    Parameters
    ----------
    teams : list of tuples
        List of (team_name, elo_rating).

    Returns
    -------
    list
        List of four pots, each containing 9 teams.
    """
    teams_sorted = sorted(teams, key=lambda x: x[1], reverse=True)

    pot1 = teams_sorted[0:9]
    pot2 = teams_sorted[9:18]
    pot3 = teams_sorted[18:27]
    pot4 = teams_sorted[27:36]

    return [pot1, pot2, pot3, pot4]


def simulate_swiss_league_phase(teams):
    """
    Simulate the Swiss-format league phase (simplified scheduling).

    Each team draws:
    - 2 opponents from each of the 4 pots (8 matches total)

    Points are accumulated for each team independently (approximation).

    Parameters
    ----------
    teams : list of tuples
        List of teams with Elo ratings.

    Returns
    -------
    numpy.ndarray
        Array of total points per team.
    """
    points = np.zeros(len(teams), dtype=int)
    pots = make_pots_by_elo(teams)

    # Map team name -> index for fast lookups
    name_to_idx = {teams[i][0]: i for i in range(len(teams))}

    for i in range(len(teams)):
        _, elo_i = teams[i]
        opponents = set()

        for pot in pots:
            candidates = []
            for (name_j, _) in pot:
                j = name_to_idx[name_j]
                if j != i and j not in opponents:
                    candidates.append(j)

            pick = rng.choice(candidates, size=2, replace=False)
            for j in pick:
                opponents.add(j)

        # Simulate the 8 matches
        for j in opponents:
            _, elo_j = teams[j]
            pi, _ = simulate_match(elo_i, elo_j)
            points[i] += pi

        # Note: we do NOT add the opponent points here.
        # Each team draws its own 8 matches -> simple approximation.

    return points


# -------------------------
# SINGLE SEASON EVALUATION
# -------------------------
def simulate_one_swiss_season():
    """
    Simulate one Swiss-format season and count weak teams in Top 8 / Top 24.

    Returns
    -------
    tuple of int
        (weak_in_top8, weak_in_top24)
    """
    teams = generate_teams()
    points = simulate_swiss_league_phase(teams)

    order = np.argsort(-points)
    ranked = [(teams[k][0], teams[k][1], int(points[k])) for k in order]

    top8 = ranked[:8]
    top24 = ranked[:24]

    weak_in_top8 = sum(1 for (_, elo, _) in top8 if elo < WEAK_ELO_THRESHOLD)
    weak_in_top24 = sum(1 for (_, elo, _) in top24 if elo < WEAK_ELO_THRESHOLD)

    return weak_in_top8, weak_in_top24


# -------------------------
# MONTE CARLO SIMULATION
# -------------------------
def run_swiss_simulation(n_seasons=N_SEASONS):
    """
    Run a Monte Carlo simulation over many Swiss-format seasons.

    Parameters
    ----------
    n_seasons : int
        Number of seasons to simulate.

    Returns
    -------
    tuple of float
        (avg_weak_top8, avg_weak_top24)
    """
    total_w8 = 0
    total_w24 = 0

    for _ in range(n_seasons):
        w8, w24 = simulate_one_swiss_season()
        total_w8 += w8
        total_w24 += w24

    avg_top8 = total_w8 / n_seasons
    avg_top24 = total_w24 / n_seasons

    print("-----------------------------------------")
    print("SWISS FORMAT SIMULATION (simplified)")
    print("4 pots, 2 opponents per pot (8 matches)")
    print(f"Weak Elo threshold: < {WEAK_ELO_THRESHOLD}")
    print(f"Draw probability: {DRAW_PROB:.2f}")
    print(f"Simulated seasons: {n_seasons}")
    print("-----------------------------------------")
    print(f"Avg. weak teams in TOP 8 :  {avg_top8:.2f} per season")
    print(f"Avg. weak teams in TOP 24:  {avg_top24:.2f} per season")
    print("Note: simplified Swiss (no UEFA constraints, no tie-breakers).")
    print("-----------------------------------------")

    return avg_top8, avg_top24


if __name__ == "__main__":
    run_swiss_simulation()

