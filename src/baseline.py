"""
baseline.py

Monte Carlo simulation of the *classic* UEFA Champions League group stage
format (baseline) as a comparison to the new Swiss model.

Setup:
- 32 teams split into 8 groups of 4 teams
- Double round-robin within each group (home/away ignored in this simplified model)
- Group winners and runners-up qualify (Top 2 per group)

We track how often "weak" teams (Elo < 1500) qualify from the groups
and how often they finish as group winners.

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
DRAW_PROB = 0.25
N_SEASONS = 20000


# -------------------------
# TEAM GENERATION (32 TEAMS)
# -------------------------
def generate_teams_32():
    """
    Generate 32 teams with synthetic Elo ratings.

    Teams are split into four tiers (8 teams each):
    - Top
    - Strong
    - Medium
    - Weak

    Returns
    -------
    list of tuples
        Each tuple contains (team_name, elo_rating).
    """
    teams = []

    # 8 top teams (1850–2050)
    for i in range(8):
        teams.append(("Team_Top_" + str(i + 1), rng.integers(1850, 2051)))

    # 8 strong teams (1750–1850)
    for i in range(8):
        teams.append(("Team_Strong_" + str(i + 1), rng.integers(1750, 1850)))

    # 8 medium teams (1550–1750)
    for i in range(8):
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
        return (1, 1)
    elif r < p_draw + p_win_a_adj:
        return (3, 0)
    else:
        return (0, 3)


# -------------------------
# GROUP STAGE SIMULATION
# -------------------------
def simulate_group_stage(teams):
    """
    Simulate an 8-group group stage with double round-robin matches.

    Parameters
    ----------
    teams : list of tuples
        List of 32 teams as (name, elo).

    Returns
    -------
    tuple
        (groups, points)
        - groups: list of arrays of team indices (8 groups, 4 teams each)
        - points: numpy array of total points per team over the group stage
    """
    points = np.zeros(len(teams), dtype=int)

    indices = np.arange(32)
    rng.shuffle(indices)
    groups = [indices[i * 4:(i + 1) * 4] for i in range(8)]

    # Double round-robin within each group (home/away ignored)
    for group in groups:
        for i in range(4):
            for j in range(i + 1, 4):
                a = group[i]
                b = group[j]

                _, elo_a = teams[a]
                _, elo_b = teams[b]

                # Match 1
                pa, pb = simulate_match(elo_a, elo_b)
                points[a] += pa
                points[b] += pb

                # Match 2 (return match)
                pa, pb = simulate_match(elo_a, elo_b)
                points[a] += pa
                points[b] += pb

    return groups, points


# -------------------------
# SINGLE SEASON EVALUATION
# -------------------------
def simulate_one_baseline_season():
    """
    Simulate one baseline season and count weak qualifiers and weak group winners.

    Returns
    -------
    tuple of int
        (weak_qualified, weak_group_winner)
        - weak_qualified: number of weak teams finishing Top 2 across all groups
        - weak_group_winner: number of weak group winners across all groups
    """
    teams = generate_teams_32()
    groups, points = simulate_group_stage(teams)

    weak_qualified = 0
    weak_group_winner = 0

    for group in groups:
        ranked = sorted(group, key=lambda idx: points[idx], reverse=True)

        top2 = ranked[:2]
        winner = ranked[0]

        for idx in top2:
            if teams[idx][1] < WEAK_ELO_THRESHOLD:
                weak_qualified += 1

        if teams[winner][1] < WEAK_ELO_THRESHOLD:
            weak_group_winner += 1

    return weak_qualified, weak_group_winner


# -------------------------
# MONTE CARLO SIMULATION
# -------------------------
def run_baseline_simulation(n_seasons=N_SEASONS):
    """
    Run a Monte Carlo simulation for the baseline group stage format.

    Parameters
    ----------
    n_seasons : int
        Number of seasons to simulate.

    Returns
    -------
    tuple of float
        (avg_weak_qualified, avg_weak_group_winners)
        - avg_weak_qualified: average number of weak teams qualifying (Top 2) per season
        - avg_weak_group_winners: average number of weak group winners per season
    """
    total_qualified = 0
    total_winners = 0

    for _ in range(n_seasons):
        q, w = simulate_one_baseline_season()
        total_qualified += q
        total_winners += w

    avg_qualified = total_qualified / n_seasons
    avg_winners = total_winners / n_seasons

    print("-----------------------------------------")
    print("BASELINE FORMAT SIMULATION (GROUP STAGE)")
    print("32 teams, 8 groups, double round-robin")
    print(f"Weak Elo threshold: < {WEAK_ELO_THRESHOLD}")
    print(f"Draw probability: {DRAW_PROB:.2f}")
    print(f"Simulated seasons: {n_seasons}")
    print("-----------------------------------------")
    print(f"Avg. weak teams qualifying (Top 2): {avg_qualified:.2f}")
    print(f"Avg. weak group winners:            {avg_winners:.2f}")
    print("Note: simplified model (no tie-breakers, no home/away).")
    print("-----------------------------------------")

    return avg_qualified, avg_winners


if __name__ == "__main__":
    run_baseline_simulation()
