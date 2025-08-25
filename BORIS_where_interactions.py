from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import get_periods, get_interactions


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    all_interactions_A = []
    all_interactions_B = []
    all_interactions_not_clear = []
    # go through files
    for f in all_files:
        file = pd.read_csv(f)

        # get periods of Plattform locations for #fish > 2
        plattform_A_period = get_periods(file, ["2 A", "3 A", "4 A"])
        plattform_B_period = get_periods(file, ["2 B", "3 B", "4 B"])

        # get all interaction events
        interactions = get_interactions(file)

        interactions_A = 0
        interactions_B = 0
        interactions_not_clear = 0
        # sort contacts for their location
        for _, row in interactions.iterrows():
            interaction_time = row["Time"]

            in_A = any(
                start <= interaction_time <= end for (start, end) in plattform_A_period
            )
            in_B = any(
                start <= interaction_time <= end for (start, end) in plattform_B_period
            )

            if in_A and in_B:
                interactions_not_clear += 1
            elif in_A:
                interactions_A += 1
            elif in_B:
                interactions_B += 1
            else:
                interactions_not_clear += 1

        all_interactions_A.append(interactions_A)
        all_interactions_B.append(interactions_B)
        all_interactions_not_clear.append(interactions_not_clear)

    # ----- Plot ------
    # means and stds
    mean_A = np.mean(all_interactions_A)
    mean_B = np.mean(all_interactions_B)
    mean_X = np.mean(all_interactions_not_clear)
    std_A = np.std(all_interactions_A, ddof=1)  # ddof=1 für Stichproben-Std
    std_B = np.std(all_interactions_B, ddof=1)
    std_X = np.std(all_interactions_not_clear, ddof=1)

    # Plot
    plt.bar(
        ["A", "B", "X"],
        [mean_A, mean_B, mean_X],
        yerr=[std_A, std_B, std_X],  # Fehlerbalken
        capsize=5,  # kleine "Kappen" auf den Fehlerbalken
    )
    plt.ylabel("# Interaktionen")
    plt.title("Interaktionen Plattformen")
    plt.show()


if __name__ == "__main__":
    main()
