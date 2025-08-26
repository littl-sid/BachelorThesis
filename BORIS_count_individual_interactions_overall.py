from IPython import embed
from matplotlib.patches import Patch
import seaborn as sns
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
    plt.figure(figsize=(10, 6))
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

    # --- Bar Plot ---
    # means = np.array([np.mean(d) for d in data])  # calculate means
    # q1 = np.array([np.percentile(d, 25) for d in data])  # 25th percentile
    # q3 = np.array([np.percentile(d, 75) for d in data])  # 75th percentile
    # lower_err = np.clip(means - q1, 0, None)  # not below 0
    # upper_err = np.clip(q3 - means, 0, None)
    # yerr = [lower_err, upper_err]

    # plt.bar(labels, means, yerr=yerr, capsize=5)

    # --- Boxplot ---
    plt.boxplot(
        data,
        labels=labels,
        patch_artist=True,  # fill boxes with color
        boxprops=dict(facecolor="seagreen", color="black"),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", color="red", alpha=0.5),
    )

    for i, d in enumerate(data):
        n = len(d)
        plt.text(
            i + 1,  # Boxplot-Position (1-basiert)
            -3,  # y-Position unter der x-Achse, ggf. anpassen
            f"n = {n}",
            ha="center",
            va="top",
            fontsize=10,
        )

    # Plot
    # medians = [np.median(d) for d in data]
    # n = [len(d) for d in data]
    # handles = [
    #     Patch(facecolor="saddlebrown", label=f"{label}: median={median:.1f}, n={n}")
    #     for label, median, n in zip(labels, medians, n)
    # ]

    # plt.legend(
    #     handles=handles,
    #     # title="Medians & Sample Size",
    #     bbox_to_anchor=(1, 1),
    #     loc="upper right",
    # )

    plt.ylabel("# Interaktionen")
    # plt.title("Verhalten: Boxplot der Interaktionen")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("fig_count_individual_interactions.pdf")
    plt.show()


if __name__ == "__main__":
    main()
