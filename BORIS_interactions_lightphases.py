from IPython import embed
import matplotlib.pyplot as plt
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

    plt.savefig("fig_interactions_lightphases.png")
    plt.show()


if __name__ == "__main__":
    main()
