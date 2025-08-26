from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    all_contact = []
    all_chase = []
    all_mouth_aggression = []
    all_shoving = []
    all_bluff = []
    all_tail_whip = []

    # go through files
    for f in all_files:
        file = pd.read_csv(f)

        # count each interaction behavior
        contact_count = 0
        chase_count = 0
        mouth_aggression_count = 0
        shoving_count = 0
        bluff_count = 0
        tail_whip_count = 0
        for _, row in file.iterrows():
            if row["Behavior"] == "contact":
                contact_count += 1
            elif row["Behavior"] == "chasing onset":
                chase_count += 1
            elif row["Behavior"] == "Mouth Aggression":
                mouth_aggression_count += 1
            elif row["Behavior"] == "shoving":
                shoving_count += 1
            elif row["Behavior"] == "bluff charge":
                bluff_count += 1
            elif row["Behavior"] == "Tail Whip":
                tail_whip_count += 1
        all_contact.append(contact_count)
        all_chase.append(chase_count)
        all_mouth_aggression.append(mouth_aggression_count)
        all_shoving.append(shoving_count)
        all_bluff.append(bluff_count)
        all_tail_whip.append(tail_whip_count)

    # ----- Plot -----
    # data summary
    data = [
        all_contact,
        all_chase,
        all_mouth_aggression,
        all_shoving,
        all_bluff,
        all_tail_whip,
    ]
    labels = [
        "contact",
        "chasing",
        "mouth aggression",
        "shoving",
        "bluff charge",
        "tail whip",
    ]

    means = [np.mean(d) for d in data]
    stds = [np.std(d, ddof=1) for d in data]  # ddof=1 → Stichproben-Standardabweichung

    # Plot
    plt.bar(labels, means, yerr=stds, capsize=5)
    plt.ylabel("# Interaktionen (MW ± SD)")
    plt.title("Verschiedene Interaktionen")
    plt.xticks(rotation=30, ha="right")  # bessere Lesbarkeit
    plt.tight_layout()

    plt.savefig("fig_count_indivdual_interactions_overall.png")
    plt.show()


if __name__ == "__main__":
    main()
