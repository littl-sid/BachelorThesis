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

        interactions = get_interactions(file)

        # sort contacts if they are during light or not
        for _, row in interactions.iterrows():
            interaction_time = row["Time"]

            # check if contact is during light

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

    # means_light = [np.mean(x) for x in all_light]
    # means_dark = [np.mean(x) for x in all_dark]
    # stds_light = [np.std(x) for x in all_light]
    # stds_dark = [np.std(x) for x in all_dark]

    # ----- Boxplot -----
    # Dataframe für Boxplot
    records = []
    for label, light_vals, dark_vals in zip(labels, all_light, all_dark):
        for v in light_vals:
            records.append({"behavior": label, "phase": "Tag", "value": v})
        for v in dark_vals:
            records.append({"behavior": label, "phase": "Nacht", "value": v})

    dataframe = pd.DataFrame(records)

    plt.figure(figsize=(12, 6))
    sns.boxplot(
        x="behavior",
        y="value",
        hue="phase",
        data=dataframe,
        palette={"Tag": "#FFD700", "Nacht": "#A9A9A9"},
        width=0.6,
    )

    # Stichprobengrößen pro Box
    behaviors = dataframe["behavior"].unique()
    phases = ["Tag", "Nacht"]

    for i, behavior in enumerate(behaviors):
        for j, phase in enumerate(phases):
            vals = dataframe[
                (dataframe["behavior"] == behavior) & (dataframe["phase"] == phase)
            ]["value"]
            n = len(vals)
            # x-Position: i ± kleine Verschiebung je nach Hue
            x_pos = i - 0.2 if phase == "Tag" else i + 0.2
            plt.text(
                x_pos,
                -3,  # y-Position unterhalb der Box, ggf. anpassen
                f"n={n}",
                ha="center",
                va="top",
                fontsize=10,
            )

    # Mann-Whitney-U-Test und Signifikanz
    for i, (light_vals, dark_vals) in enumerate(zip(all_light, all_dark)):
        stat, p = mannwhitneyu(light_vals, dark_vals, alternative="two-sided")
        max_val = max(max(light_vals), max(dark_vals))
        y_offset = 0
        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = "ns"
        plt.text(i, max_val + y_offset, sig, ha="center", va="bottom", fontsize=12)

    plt.ylabel("# Interaktionen")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="", bbox_to_anchor=(1, 1), loc="upper right")
    plt.tight_layout()
    plt.savefig("fig_individual_interactions_lightphases.pdf")
    plt.show()


if __name__ == "__main__":
    main()
