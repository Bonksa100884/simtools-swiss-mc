"""
plot_results.py

Creates plots from aggregated Monte Carlo results stored in a CSV file.

Expected input:
- data/summary.csv (written by compare.py)

Output:
- figures/compare_plot.png

The plot compares how often weak teams (Elo < threshold) reach the
knockout stage proxy:
- Swiss: Top 24
- Baseline: Top 2 (group qualifiers)

Authors:
- Julian Eberl
- Samuel Bonk
- Yannic Leinweber
"""

import csv
import os
import matplotlib.pyplot as plt


def load_summary_csv(path="data/summary.csv"):
    """
    Load the summary CSV into a dictionary.

    Parameters
    ----------
    path : str
        Path to the summary CSV file.

    Returns
    -------
    dict
        Mapping from metric name to float value.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If a value cannot be converted to float.
    """
    data = {}
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) != 2:
                continue
            metric, value = row
            # n_seasons might be stored as an integer, but float conversion is fine
            data[metric] = float(value)
    return data


def make_compare_plot(data, out_path="figures/compare_plot.png"):
    """
    Create and save a bar chart comparing Swiss vs Baseline results.

    Parameters
    ----------
    data : dict
        Dictionary containing at least:
        - swiss_avg_weak_top24
        - baseline_avg_weak_top2
    out_path : str
        File path where the figure will be saved.

    Raises
    ------
    KeyError
        If required metrics are missing in the data dict.
    """
    swiss_val = data["swiss_avg_weak_top24"]
    baseline_val = data["baseline_avg_weak_top2"]

    labels = ["Swiss (Top 24)", "Baseline (Top 2)"]
    values = [swiss_val, baseline_val]

    plt.figure()
    plt.bar(labels, values)
    plt.ylabel("Average number of weak teams per season")
    plt.title("Weak teams reaching knockout stage: Swiss vs Baseline")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main():
    """
    Entry point: load summary data and generate the comparison plot.
    """
    os.makedirs("figures", exist_ok=True)

    data = load_summary_csv("data/summary.csv")
    make_compare_plot(data, "figures/compare_plot.png")

    print("Saved figures/compare_plot.png")


if __name__ == "__main__":
    main()

