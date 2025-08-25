from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np


def count_light_interactions(file):
    # ----- contacts in light perios -----
    # get the light phase of the file
    light_phase = []
    start_time = None

    for _, row in file.iterrows():
        if row["Behavior"] == "Licht" and row["Behavior type"] == "START":
            start_time = row["Time"]
        elif (
            row["Behavior"] == "Licht"
            and row["Behavior type"] == "STOP"
            and start_time is not None
        ):
            light_phase.append((start_time, row["Time"]))
            start_time = None

    # get the interaction events of the file
    interactions_def = [
        "contact",
        "Tail Whip",
        "Mouth Aggression",
        "shoving",
        "bluff charge",
        "chasing onset",
        "chasing offset",
    ]

    interactions = file[
        file["Behavior"].str.contains("|".join(interactions_def), case=False, na=False)
    ]

    # sort contacts if they are during light or not
    interactions_light = 0
    interactions_dark = 0

    for _, row in interactions.iterrows():
        interaction_time = row["Time"]

        # check if contact is during light
        in_light = any(start <= interaction_time <= end for (start, end) in light_phase)

        if in_light:
            interactions_light += 1
        else:
            interactions_dark += 1
    return interactions_light, interactions_dark


def main():
    # alle passenden CSV-Dateien suchen
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # Dateien nach Trial und Video sortieren
    # sorted_files = sort_files(all_files)

    all_interactions_light = []
    all_interactions_dark = []
    # Durch Trials gehen
    for f in all_files:
        file = pd.read_csv(f)
        interactions_light, interactions_dark = count_light_interactions(file)
        all_interactions_light.append(interactions_light)
        all_interactions_dark.append(interactions_dark)

    # ----- Plot ------
    # means and stds
    mean_light = np.mean(all_interactions_light)
    mean_dark = np.mean(all_interactions_dark)
    std_light = np.std(all_interactions_light, ddof=1)  # ddof=1 für Stichproben-Std
    std_dark = np.std(all_interactions_dark, ddof=1)

    # Plot
    plt.bar(
        ["Tag", "Nacht"],
        [mean_light, mean_dark],
        yerr=[std_light, std_dark],  # Fehlerbalken
        capsize=5,  # kleine "Kappen" auf den Fehlerbalken
    )
    plt.ylabel("# Interaktionen")
    plt.title("Interaktionen Tag vs. Nacht")
    plt.show()


if __name__ == "__main__":
    main()
