import csv
import matplotlib.pyplot as plt

# CSV lesen
data = {}
with open("data/summary.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for metric, value in reader:
        data[metric] = float(value)

labels = ["Swiss Top24", "Baseline Top2"]
values = [data["swiss_avg_weak_top24"], data["baseline_avg_weak_top2"]]

plt.bar(labels, values)
plt.ylabel("Avg # weak teams per season")
plt.title("Weak teams reaching knockout stage: Swiss vs Baseline")
plt.tight_layout()
plt.savefig("figures/compare_plot.png")
print("Saved compare_plot.png")
