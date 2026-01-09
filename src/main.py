"""
main.py

Monte Carlo simulation of the Champions League Swiss-format league phase.

This module generates teams with synthetic Elo ratings, simulates match
outcomes using an Elo-based probability model with draws, and evaluates
how often weak teams (Elo < 1500) reach the Top 8 or Top 24.

The simulation is intentionally simplified and does not include
UEFA draw constraints or tie-breaker rules.

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
WEAK_ELO_THRESHOLD = 1500
N_TEAMS = 36
DRAW_PROB = 0.25
N_SEASONS = 2000


# -------------------------
# TEAM GENERATION
# -------------------------
def generate_teams():
    """
    Generate a list of teams with synthetic Elo ratings.

    Teams are divided into four strength tiers:
    - Top teams
    - Strong teams
    - Medium teams
    - Weak teams

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
        Probability that team A wins.
    """
    return 1.0 / (1.0 + 10 ** (-(elo_a - elo_b) / 400.0))


def simulate_match(elo_a, elo_b):
    """
    Simulate a single match between two teams.

    The match outcome can be:
    - Win for team A
    - Draw
    - Win for team B

    Parameters
    ----------
    elo_a : int
        Elo rating of team A.
    elo_b : int
        Elo rating of team B.

    Returns
    -------
    tuple of int
        Points awarded to (team A, team B).
    """
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
# SWISS FORMAT: POTS + MATCHUPS
# -------------------------
def make_pots_by_elo(teams):
    """
    Divide teams into four pots based on Elo ranking.

    Parameters
    ----------
    teams : list of tuples
        List of (team_name, elo_rating).

    Returns
    -------
    list, ndarray
        List of four pots and the original ranking order.
    """
    order = np.argsort([-elo for (_, elo) in teams])
    sorted_teams = [teams[i] for i in order]

    pots = [
        sorted_teams[0:9],
        sorted_teams[9:18],
        sorted_teams[18:27],
        sorted_teams[27:36]
    ]

    return pots, order


def simulate_swiss_league_phase(teams):
    """
    Simulate the Swiss-format league phase.

    Each team plays 2 opponents from each pot (8 matches total).
    Points are accumulated independently per team.

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
    pots, _ = make_pots_by_elo(teams)

    name_to_idx = {teams[i][0]: i for i in range(len(teams))}

    for i in range(len(teams)):
        name_i, elo_i = teams[i]
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

        for j in opponents:
            _, elo_j = teams[j]
            pi, _ = simulate_match(elo_i, elo_j)
            points[i] += pi

    return points


# -------------------------
# SINGLE SEASON EVALUATION
# -------------------------
def simulate_one_swiss_season():
    """
    Simulate a single Swiss-format season and evaluate weak teams.

    Returns
    -------
    tuple of int
        Number of weak teams in Top 8 and Top 24.
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
    Run a Monte Carlo simulation over multiple seasons.

    Parameters
    ----------
    n_seasons : int
        Number of seasons to simulate.
    """
    total_w8 = 0
    total_w24 = 0

    for _ in range(n_seasons):
        w8, w24 = simulate_one_swiss_season()
        total_w8 += w8
        total_w24 += w24

    print("-----------------------------------------")
    print("SWISS FORMAT SIMULATION")
    print(f"Weak Elo threshold: < {WEAK_ELO_THRESHOLD}")
    print(f"Draw probability: {DRAW_PROB:.2f}")
    print(f"Simulated seasons: {n_seasons}")
    print("-----------------------------------------")
    print(f"Avg. weak teams in Top 8 :  {total_w8 / n_seasons:.2f}")
    print(f"Avg. weak teams in Top 24:  {total_w24 / n_seasons:.2f}")
    print("Note: simplified Swiss model (no UEFA constraints, no tie-breakers).")
    print("-----------------------------------------")


if __name__ == "__main__":
    run_swiss_simulation()