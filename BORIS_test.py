from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
import pandas as pd
import glob
import numpy as np
from functions import get_interactions, get_periods


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # Listen für Light-Perioden
    all_contact_light = []
    all_chase_light = []
    all_mouth_aggression_light = []
    all_shoving_light = []
    all_bluff_light = []
    all_tail_whip_light = []

    # Listen für Dark-Perioden
    all_contact_dark = []
    all_chase_dark = []
    all_mouth_aggression_dark = []
    all_shoving_dark = []
    all_bluff_dark = []
    all_tail_whip_dark = []

    # go through files
    for f in all_files:
        file = pd.read_csv(f)

        # get light period and interactions
        light_period = get_periods(file, "Licht")
        interactions = get_interactions(file)

        # sort contacts if they are during light or not
        for _, row in interactions.iterrows():
            interaction_time = row["Time"]

            # check if contact is during light

            # Counter light
            counter_contact_light = 0
            counter_chase_light = 0
            counter_mouth_aggression_light = 0
            counter_shoving_light = 0
            counter_bluff_light = 0
            counter_tail_whip_light = 0

            # Counter dark
            counter_contact_dark = 0
            counter_chase_dark = 0
            counter_mouth_aggression_dark = 0
            counter_shoving_dark = 0
            counter_bluff_dark = 0
            counter_tail_whip_dark = 0

            in_light = any(
                start <= interaction_time <= end for (start, end) in light_period
            )

            if in_light:
                if row["Behavior"] == "contact":
                    counter_contact_light += 1
                elif row["Behavior"] == "chasing onset":
                    counter_chase_light += 1
                elif row["Behavior"] == "Mouth Aggression":
                    counter_mouth_aggression_light += 1
                elif row["Behavior"] == "shoving":
                    counter_shoving_light += 1
                elif row["Behavior"] == "bluff charge":
                    counter_bluff_light += 1
                elif row["Behavior"] == "Tail Whip":
                    counter_tail_whip_light += 1
            else:
                if row["Behavior"] == "contact":
                    counter_contact_dark += 1
                elif row["Behavior"] == "chasing onset":
                    counter_chase_dark += 1
                elif row["Behavior"] == "Mouth Aggression":
                    counter_mouth_aggression_dark += 1
                elif row["Behavior"] == "shoving":
                    counter_shoving_dark += 1
                elif row["Behavior"] == "bluff charge":
                    counter_bluff_dark += 1
                elif row["Behavior"] == "Tail Whip":
                    counter_tail_whip_dark += 1

        # Light
        all_contact_light.append(counter_contact_light)
        all_chase_light.append(counter_chase_light)
        all_mouth_aggression_light.append(counter_mouth_aggression_light)
        all_shoving_light.append(counter_shoving_light)
        all_bluff_light.append(counter_bluff_light)
        all_tail_whip_light.append(counter_tail_whip_light)

        # Dark
        all_contact_dark.append(counter_contact_dark)
        all_chase_dark.append(counter_chase_dark)
        all_mouth_aggression_dark.append(counter_mouth_aggression_dark)
        all_shoving_dark.append(counter_shoving_dark)
        all_bluff_dark.append(counter_bluff_dark)
        all_tail_whip_dark.append(counter_tail_whip_dark)

    # ----- Plot -----
    # labels
    labels = [
        "contact",
        "chasing",
        "mouth aggression",
        "shoving",
        "bluff charge",
        "tail whip",
    ]

    # Data
    all_light = [
        all_contact_light,
        all_chase_light,
        all_mouth_aggression_light,
        all_shoving_light,
        all_bluff_light,
        all_tail_whip_light,
    ]

    all_dark = [
        all_contact_dark,
        all_chase_dark,
        all_mouth_aggression_dark,
        all_shoving_dark,
        all_bluff_dark,
        all_tail_whip_dark,
    ]

    # ----- Plot -----
    # labels
    labels = [
        "contact",
        "chasing",
        "mouth aggression",
        "shoving",
        "bluff charge",
        "tail whip",
    ]

    # Data
    all_light = [
        all_contact_light,
        all_chase_light,
        all_mouth_aggression_light,
        all_shoving_light,
        all_bluff_light,
        all_tail_whip_light,
    ]

    all_dark = [
        all_contact_dark,
        all_chase_dark,
        all_mouth_aggression_dark,
        all_shoving_dark,
        all_bluff_dark,
        all_tail_whip_dark,
    ]

    # --- Box Plot ---
    fig, ax = plt.subplots(figsize=(10, 6))

    positions_light = np.arange(len(labels)) - 0.2
    positions_dark = np.arange(len(labels)) + 0.2

    bpl = ax.boxplot(
        all_light,
        positions=positions_light,
        widths=0.35,
        patch_artist=True,
        boxprops=dict(facecolor="#FFD700"),
        medianprops=dict(color="black"),
    )

    bpd = ax.boxplot(
        all_dark,
        positions=positions_dark,
        widths=0.35,
        patch_artist=True,
        boxprops=dict(facecolor="#A9A9A9"),
        medianprops=dict(color="black"),
    )

    # axis, title, legend
    ax.set_ylabel("# Interaktionen")
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylim(bottom=0)

    # Mann-Whitney-U-Test and Significance
    y_max = max(max(map(max, all_light)), max(map(max, all_dark)))
    y_offset = y_max * 0.05

    for i, (light_vals, dark_vals) in enumerate(zip(all_light, all_dark)):
        stat, p = mannwhitneyu(light_vals, dark_vals, alternative="two-sided")

        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = "ns"

        ax.text(
            i,
            y_max + y_offset,
            sig,
            ha="center",
            va="bottom",
            fontsize=12,
        )

    # Legend with MW, SD, n
    means_light = [np.mean(x) for x in all_light]
    stds_light = [np.std(x, ddof=1) for x in all_light]
    means_dark = [np.mean(x) for x in all_dark]
    stds_dark = [np.std(x, ddof=1) for x in all_dark]

    legend_labels = [
        f"Tag: {label} (MW={mean:.2f} ± SD={std:.2f}, n={len(vals)})"
        for label, mean, std, vals in zip(labels, means_light, stds_light, all_light)
    ] + [
        f"Nacht: {label} (MW={mean:.2f} ± SD={std:.2f}, n={len(vals)})"
        for label, mean, std, vals in zip(labels, means_dark, stds_dark, all_dark)
    ]

    legend_colors = ["#FFD700"] * len(labels) + ["#A9A9A9"] * len(labels)
    handles = [
        Patch(facecolor=color, alpha=0.7, label=lab)
        for color, lab in zip(legend_colors, legend_labels)
    ]
    ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc="upper left", title="")

    # --- Show Plot ---
    plt.tight_layout()
    plt.savefig("fig_boxplot_light_dark.png")
    plt.show()


if __name__ == "__main__":
    main()
