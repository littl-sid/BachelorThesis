import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from matplotlib.lines import Line2D
from functions import sort_files, get_interactions, get_trial_and_video


def count_interactions(files):
    all_interactions = []
    for f in files:
        file = pd.read_csv(f)
        interactions = get_interactions(file)
        all_interactions.append(len(interactions))
    return all_interactions


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")
    sorted_files = sort_files(all_files)

    colors = plt.cm.tab10.colors  # Farbpalette

    # Figure mit zwei Subplots nebeneinander (gemeinsame x- und y-Achse)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 5.625), sharex=True, sharey=True)

    # ---------- Plot 1: pro Trial ----------
    for trial in sorted_files:
        interaction_count = []
        for v in trial:
            trial_number, _ = get_trial_and_video(v)
            color = colors[(trial_number - 1) % len(colors)]
            file = pd.read_csv(v)
            interactions = get_interactions(file)
            interaction_count.append(len(interactions))

        x_axis = range(1, len(interaction_count) + 1)
        ax1.scatter(x_axis, interaction_count, color=color)
        z = np.polyfit(x_axis, interaction_count, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(x_axis), max(x_axis), 100)
        ax1.plot(x_line, p(x_line), linestyle="-", alpha=0.8, color=color)

        slope = z[0]
        n = len(interaction_count)
        ax1.scatter(
            [], [], color=color, label=f"Trial {trial_number}: m={slope:.2f}, n={n}"
        )

    ax1.set_xticks([1, 2, 3, 4])
    ax1.set_xticklabels(["1", "2", "3", "4"])
    ax1.legend(loc="upper right", fontsize=8)

    # ---------- Plot 2: alle zusammen ----------
    interaction_count = []
    for trial in sorted_files:
        for v in trial:
            trial_number, video_number = get_trial_and_video(v)
            file = pd.read_csv(v)
            interactions = get_interactions(file)
            interaction_count.append([len(interactions), video_number])

    x = np.array([i[1] for i in interaction_count])
    y = np.array([i[0] for i in interaction_count])

    ax2.scatter(x, y, color="seagreen")

    coeffs = np.polyfit(x, y, 1)
    slope = coeffs[0]
    y_fit = np.poly1d(coeffs)(x)
    ax2.plot(x, y_fit, color="black", linestyle="-")

    n = len(interaction_count)
    line_handle = Line2D(
        [0], [0], color="black", linestyle="-", label=f"m = {slope:.2f}, n={n}"
    )
    ax2.legend(handles=[line_handle], loc="upper right", fontsize=8)

    ax2.set_xticks([1, 2, 3, 4])
    ax2.set_xticklabels(["1", "2", "3", "4"])

    # ---------- Gemeinsame Labels ----------
    fig.supxlabel("Video-Nr.", y=0.05)
    fig.supylabel("# Interaktionen")

    # ---------- Layout & Save ----------
    plt.tight_layout()
    plt.savefig("fig_interactioncount_two_plots.pdf")
    plt.show()


if __name__ == "__main__":
    main()
