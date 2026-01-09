"""
compare.py

Compares the Champions League Swiss format with the classical
group stage baseline using Monte Carlo simulations.

This module runs both simulations, prints a summary to the console,
and stores the aggregated results in a CSV file for further analysis
and visualization.

Authors:
- Julian Eberl
- Samuel Bonk
- Yannic Leinweber
"""

import csv
import os

from src.swiss import run_swiss_simulation
from src.baseline import run_baseline_simulation


# Number of simulated seasons (increase for final runs)
N_SEASONS = 20000


def main():
    """
    Run and compare Swiss-format and baseline simulations.

    The function executes Monte Carlo simulations for both formats,
    prints a summary of the results, and writes the aggregated metrics
    to a CSV file.
    """
    print("\n=== COMPARE: SWISS vs BASELINE ===\n")

    # Run Swiss simulation
    swiss_top8, swiss_top24 = run_swiss_simulation(N_SEASONS)

    # Run baseline simulation
    baseline_top2, baseline_winners = run_baseline_simulation(N_SEASONS)

    # Print summary to console
    print("\n=== SUMMARY ===")
    print(f"Swiss:    avg. weak teams in Top 8   = {swiss_top8:.2f}")
    print(f"Swiss:    avg. weak teams in Top 24  = {swiss_top24:.2f}")
    print(f"Baseline: avg. weak teams in Top 2   = {baseline_top2:.2f}")
    print(f"Baseline: avg. weak group winners   = {baseline_winners:.2f}")
    print("================\n")

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Write results to CSV
    with open("data/summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["swiss_avg_weak_top8", swiss_top8])
        writer.writerow(["swiss_avg_weak_top24", swiss_top24])
        writer.writerow(["baseline_avg_weak_top2", baseline_top2])
        writer.writerow(["baseline_avg_weak_group_winners", baseline_winners])
        writer.writerow(["n_seasons", N_SEASONS])

    print("Saved results to data/summary.csv\n")


if __name__ == "__main__":
    main()
