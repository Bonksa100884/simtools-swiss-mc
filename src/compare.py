import csv

from src.swiss import run_swiss_simulation
from src.baseline import run_baseline_simulation

N_SEASONS = 20000  # final: z.B. 20000, zum Testen kleiner

def main():
    print("\n=== COMPARE: SWISS vs BASELINE ===\n")

    # Swiss
    swiss_top8, swiss_top24 = run_swiss_simulation(N_SEASONS)

    # Baseline
    baseline_top2, baseline_winners = run_baseline_simulation(N_SEASONS)

    # Summary in Konsole
    print("\n=== SUMMARY ===")
    print(f"Swiss:    Ø weak in Top 8   = {swiss_top8:.2f}")
    print(f"Swiss:    Ø weak in Top 24  = {swiss_top24:.2f}")
    print(f"Baseline: Ø weak in Top 2   = {baseline_top2:.2f}")
    print(f"Baseline: Ø weak winners    = {baseline_winners:.2f}")
    print("================\n")

    # CSV speichern
    with open("summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["swiss_avg_weak_top8", swiss_top8])
        writer.writerow(["swiss_avg_weak_top24", swiss_top24])
        writer.writerow(["baseline_avg_weak_top2", baseline_top2])
        writer.writerow(["baseline_avg_weak_group_winners", baseline_winners])
        writer.writerow(["n_seasons", N_SEASONS])

    print("Saved results to summary.csv\n")

if __name__ == "__main__":
    main()
