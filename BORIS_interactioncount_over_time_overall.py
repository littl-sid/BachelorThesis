from IPython import embed
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import glob
import numpy as np
from functions import sort_files, get_interactions, get_trial_and_video


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # sort files for trial and video number
    sorted_files = sort_files(all_files)

    # count in trial videos the interactions
    interaction_count = []
    for trial in sorted_files:
        for v in trial:
            trial_number, video_number = get_trial_and_video(v)

            file = pd.read_csv(v)
            interactions = get_interactions(file)
            interaction_count.append([len(interactions), video_number])

    # ----- Plot -----
    plt.figure(figsize=(6, 4.5))

    x = np.array([i[1] for i in interaction_count])
    y = np.array([i[0] for i in interaction_count])

    plt.scatter(x, y, color="seagreen")

    # Trendlinie
    coeffs = np.polyfit(x, y, 1)  # linear fit
    slope = coeffs[0]
    y_fit = np.poly1d(coeffs)(x)
    plt.plot(x, y_fit, color="black", linestyle="-")

    n = len(interaction_count)
    line_handle = Line2D(
        [0], [0], color="black", linestyle="-", label=f"m = {slope:.2f}, n={n}"
    )
    plt.legend(handles=[line_handle], loc="upper right")

    # Plot
    plt.ylabel("# Interaktionen")
    plt.xlabel("Video-Nr.")
    plt.xticks([1, 2, 3, 4], ["1", "2", "3", "4"])
    # plt.title("Interaktionsanzahl über die Zeit")
    # plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    plt.savefig("fig_interactioncount_over_time_overall.pdf")
    plt.show()


if __name__ == "__main__":
    main()
