from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import numpy as np
import itertools
from functions import get_interactions, sort_files


def count_interactions(files):
    all_interactions = []

    for f in files:
        file = pd.read_csv(f)
        interactions = get_interactions(file)
        all_interactions.append(len(interactions))
    return all_interactions


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")

    # sort files for trial and video number
    sorted_files = sort_files(all_files)

    interactions_trials = []

    for trial in sorted_files:
        count = count_interactions(trial)
        interactions_trials.append(count)

    # ----- Plot -----
    # labels
    labels = ["3", "4", "5", "6", "7", "8", "10", "11", "12"]

    # kurzer Einschub für Berechnungen
    medians = [np.median(d) for d in interactions_trials]
    means = [np.mean(d) for d in interactions_trials]
    stds = [np.std(d, ddof=1) for d in interactions_trials]
    statistics_table = pd.DataFrame(
        {"behavior": labels, "median": medians, "mean": means, "std": stds}
    )
    print(statistics_table)

    # --- Boxplot ---
    records = []
    for label, counts in zip(labels, interactions_trials):
        for v in counts:
            records.append({"trial": label, "interactions": v})

    dataframe = pd.DataFrame(records)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    sns.boxplot(
        x="trial", y="interactions", data=dataframe, color="seagreen", width=0.6, ax=ax
    )

    # n unter die Boxplots setzen
    for i, label in enumerate(labels):
        n = len(dataframe[dataframe["trial"] == label])
        ax.text(i, -1.5, f"n = {n}", ha="center", va="top", fontsize=8)

    # --- Mann-Whitney-U-Test twosided, pairwise ---
    pairs = list(itertools.combinations(range(len(labels)), 2))
    y_max = dataframe["interactions"].max()

    for i, j in pairs:
        group_i = dataframe[dataframe["trial"] == labels[i]]["interactions"]
        group_j = dataframe[dataframe["trial"] == labels[j]]["interactions"]
        stat, p = mannwhitneyu(group_i, group_j, alternative="two-sided")

        # Signifikanzsymbole
        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = "ns"

        # Position oberhalb der Boxplots (leicht versetzt)
        y = y_max + 2 + (i + j) * 0.5  # Abstand zwischen Linien
        x = (i + j) / 2
        ax.text(x, y, sig, ha="center", va="top", fontsize=10)

    ax.set_ylabel("# Interaktionen")
    ax.set_xlabel("Trial")
    plt.tight_layout()
    plt.savefig("fig_count_interactions_trials.pdf")
    plt.show()


if __name__ == "__main__":
    main()
