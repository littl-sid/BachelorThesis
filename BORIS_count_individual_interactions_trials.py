from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import get_interactions, get_trial_and_video


def count_individual_interactions(csv_file):
    trial_number, _ = get_trial_and_video(csv_file)
    file = pd.read_csv(csv_file)

    interactions = get_interactions(file)

    # count each interaction behavior
    contact_count = 0
    chase_count = 0
    mouth_aggression_count = 0
    shoving_count = 0
    bluff_count = 0
    tail_whip_count = 0
    for _, row in interactions.iterrows():
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

    return (
        trial_number,
        contact_count,
        chase_count,
        mouth_aggression_count,
        shoving_count,
        bluff_count,
        tail_whip_count,
    )


def main():
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")
    all_data = []

    # Daten sammeln
    for f in all_files:
        trial_data = count_individual_interactions(f)
        all_data.append(trial_data)

    # In DataFrame
    df = pd.DataFrame(
        all_data,
        columns=[
            "trial",
            "contact",
            "chasing",
            "mouth aggression",
            "shoving",
            "bluff charge",
            "tail whip",
        ],
    )

    # Nach Trial sortieren
    df.sort_values("trial", inplace=True)

    # Mean und std pro Trial und Verhalten berechnen
    behaviors = [
        "contact",
        "chasing",
        "mouth aggression",
        "shoving",
        "bluff charge",
        "tail whip",
    ]
    trial_groups = df.groupby("trial")[behaviors]
    mean_df = trial_groups.mean()
    std_df = trial_groups.std()

    x = np.arange(len(mean_df))
    width = 0.13

    colors = ["skyblue", "orange", "seagreen", "red", "purple", "yellow"]

    fig, ax = plt.subplots(figsize=(6, 4.5))

    # Bars für jede Behavior
    for i, (behavior, color) in enumerate(zip(behaviors, colors)):
        ax.bar(
            x + i * width - (len(behaviors) - 1) * width / 2,
            mean_df[behavior],
            width,
            yerr=std_df[behavior],
            capsize=3,
            label=behavior,
            color=color,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(mean_df.index)
    ax.set_xlabel("Trial")
    ax.set_ylabel("Durchschnittliche Anzahl Interaktionen")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("fig_count_individual_interactions_trials.pdf")
    plt.show()


if __name__ == "__main__":
    main()
