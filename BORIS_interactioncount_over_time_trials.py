from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import sort_files, get_interactions, get_trial_and_video


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # sort files for trial and video number
    sorted_files = sort_files(all_files)

    # color palette trials
    colors = plt.cm.tab10.colors  # 10 Farben aus matplotlib Tab10

    # count in trial videos the interactions
    for trial in sorted_files:
        interaction_count = []
        for v in trial:
            trial_number, _ = get_trial_and_video(v)
            color = colors[(trial_number - 1) % len(colors)]  # Farbe nach Trialnummer

            file = pd.read_csv(v)
            interactions = get_interactions(file)
            interaction_count.append(len(interactions))

        # --- Plot part 1 ---
        x_axis = range(1, len(interaction_count) + 1)
        plt.scatter(x_axis, interaction_count, color=color)
        # Trendlinie
        z = np.polyfit(x_axis, interaction_count, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(x_axis), max(x_axis), 100)
        plt.plot(x_line, p(x_line), linestyle="-", alpha=0.8, color=color)
        # Legend
        n = len(interaction_count)
        slope = z[0]
        plt.scatter(
            [], [], color=color, label=f"Trial {trial_number}: m={slope:.2f}, n={n}"
        )

        interaction_count = []

    # ----- Plot part 2 -----
    plt.xticks([1, 2, 3, 4], ["1", "2", "3", "4"])
    plt.ylabel("# Interaktionen")
    plt.xlabel("Zeit über Videonummer")
    # plt.title("Interaktionsanzahl über die Zeit")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    plt.savefig("fig_interactioncount_over_time_trials.png")
    plt.show()


if __name__ == "__main__":
    main()
