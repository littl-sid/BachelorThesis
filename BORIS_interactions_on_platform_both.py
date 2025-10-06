from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import pandas as pd
import glob
from functions import (
    get_followup_interactions,
    get_color,
    get_legend,
)


def get_interactions_on_platforms(dataset, ax):
    all_interactions_A = []
    all_interactions_B = []

    for f in dataset:
        file = pd.read_csv(f)
        interactions = get_followup_interactions(file)

        interactions_A = sum(
            row["Behavior"] in ["int A 1", "int A 2"]
            for _, row in interactions.iterrows()
        )
        interactions_B = sum(
            row["Behavior"] in ["int B 1", "int B 2"]
            for _, row in interactions.iterrows()
        )

        all_interactions_A.append(interactions_A)
        all_interactions_B.append(interactions_B)

    color_A, color_B = get_color(dataset[0])

    bp = ax.boxplot(
        [all_interactions_A, all_interactions_B],
        labels=["links", "rechts"],
        patch_artist=True,
        boxprops=dict(color="black"),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", color="red", alpha=0.5),
    )

    for patch, col in zip(bp["boxes"], [color_A, color_B]):
        patch.set_facecolor(col)

    ns = [len(all_interactions_A), len(all_interactions_B)]
    for i, n in enumerate(ns, start=1):
        ax.text(i, -0.2 * max(ns), f"n = {n}", ha="center", va="top", fontsize=8)

    stat, p = mannwhitneyu(
        all_interactions_A, all_interactions_B, alternative="two-sided"
    )

    if p < 0.001:
        sig = "***"
    elif p < 0.01:
        sig = "**"
    elif p < 0.05:
        sig = "*"
    else:
        sig = "ns"

    max_y = max(max(all_interactions_A), max(all_interactions_B))
    y, h = max_y * 1.1, max_y * 0.05
    ax.plot([1, 1, 2, 2], [y, y + h, y + h, y], lw=1.5, color="black")
    ax.text(1.5, y + h, sig, ha="center", va="bottom", fontsize=12)

    handles = get_legend(dataset[0])
    # ax.legend(handles=handles, loc="upper right", fontsize=8)

    return ax


def main():
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4.5), sharey=True)

    get_interactions_on_platforms(dataset_1, ax1)
    get_interactions_on_platforms(dataset_2, ax2)

    ax1.set_ylabel("# Interaktionen")

    # Eine gemeinsame Legende unten hinzufügen
    handles = get_legend(dataset_1[0])  # reicht, da Farben gleich
    fig.legend(handles=handles, loc="upper center", ncol=2, fontsize=8, frameon=False)

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Platz für Legende oben
    plt.savefig("fig_plattform_interactions_two_datasets.pdf")
    plt.show()


if __name__ == "__main__":
    main()
