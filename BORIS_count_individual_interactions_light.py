from IPython import embed
import matplotlib.pyplot as plt
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

    # MW and STD Light
    means_light = [
        np.mean(all_contact_light),
        np.mean(all_chase_light),
        np.mean(all_mouth_aggression_light),
        np.mean(all_shoving_light),
        np.mean(all_bluff_light),
        np.mean(all_tail_whip_light),
    ]

    stds_light = [
        np.std(all_contact_light, ddof=1),
        np.std(all_chase_light, ddof=1),
        np.std(all_mouth_aggression_light, ddof=1),
        np.std(all_shoving_light, ddof=1),
        np.std(all_bluff_light, ddof=1),
        np.std(all_tail_whip_light, ddof=1),
    ]

    # MW and STD Dark
    means_dark = [
        np.mean(all_contact_dark),
        np.mean(all_chase_dark),
        np.mean(all_mouth_aggression_dark),
        np.mean(all_shoving_dark),
        np.mean(all_bluff_dark),
        np.mean(all_tail_whip_dark),
    ]

    stds_dark = [
        np.std(all_contact_dark, ddof=1),
        np.std(all_chase_dark, ddof=1),
        np.std(all_mouth_aggression_dark, ddof=1),
        np.std(all_shoving_dark, ddof=1),
        np.std(all_bluff_dark, ddof=1),
        np.std(all_tail_whip_dark, ddof=1),
    ]

    # bars
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(
        x - width / 2,
        means_light,
        width,
        yerr=stds_light,
        capsize=5,
        color="#FFD700",
        label="Tag",
    )
    rects2 = ax.bar(
        x + width / 2,
        means_dark,
        width,
        yerr=stds_dark,
        capsize=5,
        color="#A9A9A9",
        label="Nacht",
    )

    # axis, title, legend
    ax.set_ylabel("# Interaktionen (MW ± SD)")
    ax.set_ylim(bottom=0)
    ax.set_title("einzelne Interaktionen Tag vs Nacht")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.legend()

    plt.tight_layout()

    plt.savefig("fig_count_indivudal_interactions_lightphases.png")
    plt.show()


if __name__ == "__main__":
    main()
