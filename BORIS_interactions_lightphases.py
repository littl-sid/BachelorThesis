from IPython import embed
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import mannwhitneyu
import pandas as pd
import glob
import numpy as np
from functions import get_periods, get_interactions


def main():
    # alle passenden CSV-Dateien suchen
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    all_interactions_light = []
    all_interactions_dark = []
    # Durch Trials gehen
    for f in all_files:
        file = pd.read_csv(f)
        light_period = get_periods(file, "Licht")
        interactions = get_interactions(file)

        interactions_light = 0
        interactions_dark = 0
        # sort contacts if they are during light or not
        for _, row in interactions.iterrows():
            interaction_time = row["Time"]

            # check if contact is during light
            in_light = any(
                start <= interaction_time <= end for (start, end) in light_period
            )

            if in_light:
                interactions_light += 1
            else:
                interactions_dark += 1

        all_interactions_light.append(interactions_light)
        all_interactions_dark.append(interactions_dark)

    # ----- Boxplot -----
    data = [all_interactions_light, all_interactions_dark]
    labels = ["Tag", "Nacht"]
    colors = ["gold", "grey"]

    fig, ax = plt.subplots(figsize=(10, 6))
    box = ax.boxplot(
        data,
        labels=labels,
        patch_artist=True,
        boxprops=dict(facecolor="white", color="black"),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", color="red", alpha=0.5),
    )

    # Boxen einfärben
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # Stichprobengröße n in die Legende aufnehmen
    handles = []
    for label, counts, color in zip(labels, data, colors):
        n = len(counts)
        handles.append(Patch(facecolor=color, label=f"{label} (n={n})"))

    ax.legend(handles=handles, loc="upper right")

    #  --- Man-Whitney-U-Test ---
    stat, p = mannwhitneyu(
        all_interactions_light, all_interactions_dark, alternative="two-sided"
    )

    # Sigifcance over boxes
    max_val = max(max(all_interactions_light), max(all_interactions_dark))
    y_offset = 0
    if p < 0.001:
        sig = "***"
    elif p < 0.01:
        sig = "**"
    elif p < 0.05:
        sig = "*"
    else:
        sig = "ns"

    ax.text(1.5, max_val + y_offset, sig, ha="center", va="bottom", fontsize=14)

    ax.set_ylabel("# Interaktionen")
    # ax.set_title("Interaktionen Tag vs. Nacht")
    plt.tight_layout()
    plt.savefig("fig_interactions_lightphases.png")
    plt.show()


if __name__ == "__main__":
    main()
