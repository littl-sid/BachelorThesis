from IPython import embed
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import get_periods, get_interactions, get_color, get_legend


def get_interactions_on_platforms(dataset, name):
    all_interactions_A = []
    all_interactions_B = []
    all_interactions_not_clear = []
    all_error = []
    # go through files
    for f in dataset:
        file = pd.read_csv(f)

        # get periods of Plattform locations for #fish > 2
        plattform_A_period = get_periods(file, ["2 A", "3 A", "4 A"])
        plattform_B_period = get_periods(file, ["2 B", "3 B", "4 B"])

        # get all interaction events
        interactions = get_interactions(file)

        interactions_A = 0
        interactions_B = 0
        interactions_not_clear = 0
        error = 0
        # sort contacts for their location
        for _, row in interactions.iterrows():
            interaction_time = row["Time"]

            in_A = any(
                start <= interaction_time <= end for (start, end) in plattform_A_period
            )
            in_B = any(
                start <= interaction_time <= end for (start, end) in plattform_B_period
            )

            if in_A and in_B:
                interactions_not_clear += 1
            elif in_A:
                interactions_A += 1
            elif in_B:
                interactions_B += 1
            else:
                error += 1

        all_interactions_A.append(interactions_A)
        all_interactions_B.append(interactions_B)
        all_interactions_not_clear.append(interactions_not_clear)
        all_error.append(error)

    # ----- Plot -----
    # Farben bestimmen
    color_A, color_B = get_color(f)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Boxplot zeichnen
    bp = ax.boxplot(
        [all_interactions_A, all_interactions_B, all_interactions_not_clear],
        labels=["A", "B", "X"],
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
    ax.legend(handles=handles, loc="upper right")

    # Stichprobengröße unter jede Box schreiben
    ns = [
        len(all_interactions_A),
        len(all_interactions_B),
        len(all_interactions_not_clear),
    ]
    for i, n in enumerate(ns, start=1):
        ax.text(i, -0.05 * max(ns), f"n = {n}", ha="center", va="top", fontsize=10)

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
    ax.set_title("Interaktionen Plattformen")

    plt.tight_layout()
    plt.savefig(f"fig_plattform_interactions_{name}.png")
    plt.show()


def main():
    # get all CSV files
    dataset_1 = []
    for d in [
        "BORIS_events/Trial3_V*_events.csv",
        "BORIS_events/Trial4_V*_events.csv",
        "BORIS_events/Trial5_V*_events.csv",
        "BORIS_events/Trial6_V*_events.csv",
    ]:
        dataset_1.extend(glob.glob(d))

    dataset_2 = []
    for d in [
        "BORIS_events/Trial7_V*_events.csv",
        "BORIS_events/Trial8_V*_events.csv",
        "BORIS_events/Trial10_V*_events.csv",
        "BORIS_events/Trial11_V*_events.csv",
        "BORIS_events/Trial12_V*_events.csv",
    ]:
        dataset_2.extend(glob.glob(d))

    get_interactions_on_platforms(dataset_1, 1)
    get_interactions_on_platforms(dataset_2, 2)


if __name__ == "__main__":
    main()
