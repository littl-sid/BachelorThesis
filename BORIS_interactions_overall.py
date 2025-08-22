from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import sort_files, count_interactions


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
        interactions_light, interactions_dark = count_interactions(file)
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
