from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import get_followup_interactions, get_color, get_legend


def get_interactions_on_platforms(dataset, name):
    all_interactions_A = []
    all_interactions_B = []
    # all_interactions_not_clear = []
    # all_error = []
    # go through files
    for f in dataset:
        file = pd.read_csv(f)

        # get all interaction events
        interactions = get_followup_interactions(file)

        interactions_A = 0
        interactions_B = 0

        # sort interations for their location
        for _, row in interactions.iterrows():
            in_A = row["Behavior"] in ["int A 1", "int A 2"]
            in_B = row["Behavior"] in ["int B 1", "int B 2"]

            if in_A:
                interactions_A += 1
            elif in_B:
                interactions_B += 1

        all_interactions_A.append(interactions_A)
        all_interactions_B.append(interactions_B)

    # ----- Plot -----
    # Farben bestimmen
    color_A, color_B = get_color(f)

    fig, ax = plt.subplots(figsize=(6, 4.5))

    # kurzer Einschub für Berechnungen
    median_A = np.median(all_interactions_A)
    mean_A = np.mean(all_interactions_A)
    std_A = np.std(all_interactions_A)
    median_B = np.median(all_interactions_B)
    mean_B = np.mean(all_interactions_B)
    std_B = np.std(all_interactions_B)
    print(f"{name}:")
    print(f"  A: Median = {median_A:.2f}, Mean = {mean_A:.2f}, Std = {std_A:.2f}")
    print(f"  B: Median = {median_B:.2f}, Mean = {mean_B:.2f}, Std = {std_B:.2f}")

    # Boxplot zeichnen
    bp = ax.boxplot(
        [all_interactions_A, all_interactions_B],
        labels=["A", "B"],
        patch_artist=True,
        boxprops=dict(color="black"),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", color="red", alpha=0.5),
    )

    # Farben einsetzen
    colors = [color_A, color_B, "gray"]
    for patch, col in zip(bp["boxes"], colors):
        patch.set_facecolor(col)

    # Legende
    handles = get_legend(f)
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1, 1))

    # Stichprobengröße unter jede Box schreiben
    ns = [
        len(all_interactions_A),
        len(all_interactions_B),
    ]
    for i, n in enumerate(ns, start=1):
        ax.text(i, -0.1 * max(ns), f"n = {n}", ha="center", va="top", fontsize=8)

    # ----- Statistischer Test A vs. B -----
    # Mann-Whitney-U-Test
    stat, p = mannwhitneyu(
        all_interactions_A, all_interactions_B, alternative="two-sided"
    )

    # oder alternativ: t-Test
    # stat, p = ttest_ind(all_interactions_A, all_interactions_B, equal_var=False)

    # Signifikanz-Level bestimmen
    if p < 0.001:
        sig = "***"
    elif p < 0.01:
        sig = "**"
    elif p < 0.05:
        sig = "*"
    else:
        sig = "ns"

    # Linie und Sternchen über A und B zeichnen
    max_y = max(max(all_interactions_A), max(all_interactions_B))
    y, h = max_y * 1.1, max_y * 0.05
    ax.plot([1, 1, 2, 2], [y, y + h, y + h, y], lw=1.5, color="black")
    ax.text(1.5, y + h, sig, ha="center", va="bottom", fontsize=12)

    ax.set_ylabel("# Interaktionen")
    # ax.set_title("Interaktionen Plattformen")

    plt.tight_layout()
    plt.savefig(f"fig_plattform_interactions_{name}.pdf")
    plt.show()


def main():
    # get all CSV files
    dataset_1 = []
    for d in [
        "BORIS_events_followup/Trial3_V*_events.csv",
        "BORIS_events_followup/Trial4_V*_events.csv",
        "BORIS_events_followup/Trial5_V*_events.csv",
        "BORIS_events_followup/Trial6_V*_events.csv",
    ]:
        dataset_1.extend(glob.glob(d))

    dataset_2 = []
    for d in [
        "BORIS_events_followup/Trial7_V*_events.csv",
        "BORIS_events_followup/Trial8_V*_events.csv",
        "BORIS_events_followup/Trial10_V*_events.csv",
        "BORIS_events_followup/Trial11_V*_events.csv",
        "BORIS_events_followup/Trial12_V*_events.csv",
    ]:
        dataset_2.extend(glob.glob(d))

    get_interactions_on_platforms(dataset_1, 1)
    get_interactions_on_platforms(dataset_2, 2)


if __name__ == "__main__":
    main()
