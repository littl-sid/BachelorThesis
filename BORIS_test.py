import matplotlib.pyplot as plt
from IPython import embed
import pandas as pd
import glob
from functions import sort_files


def main():
    # CSV laden und einlesen
    file = pd.read_csv("BORIS_events/Trial10_V3_events.csv")

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

    # Plot
    plt.bar(["Licht", "Dunkel"], [interactions_light, interactions_dark])
    plt.ylabel("Anzahl Interaktionen")
    plt.title("Interaktionen bei Licht vs. Dunkelheit")
    plt.show()


if __name__ == "__main__":
    main()
