import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import glob
import numpy as np
from scipy.stats import mannwhitneyu
from functions import get_interactions, get_trial_and_video


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")

    interaction_count = []
    for f in all_files:
        _, video_number = get_trial_and_video(f)

        file = pd.read_csv(f)
        interactions = get_interactions(file)
        interaction_count.append([len(interactions), video_number])

    # ----- Plot -----
    df = pd.DataFrame(interaction_count, columns=["count", "video"])

    label_map = {
        1: "Tag auf Nacht",
        2: "Nacht auf Tag",
        3: "Tag auf Nacht",
        4: "Nacht auf Tag",
    }
    color_map = {1: "orange", 2: "red", 3: "skyblue", 4: "seagreen"}

    fig, ax = plt.subplots(figsize=(6, 4.5))  # <--- Axes-Objekt

    boxprops = dict(linewidth=1)
    medianprops = dict(linewidth=1, color="black")

    bplot = ax.boxplot(
        [df[df["video"] == i]["count"] for i in range(1, 5)],
        patch_artist=True,
        labels=[f"Video {i}" for i in range(1, 5)],
        boxprops=boxprops,
        medianprops=medianprops,
    )

    for patch, i in zip(bplot["boxes"], range(1, 5)):
        patch.set_facecolor(color_map[i])

    # n unter Boxplots
    ns = [len(df[df["video"] == i]) for i in range(1, 5)]
    for i, n in enumerate(ns, start=1):
        ax.text(i, -2.6 * max(ns), f"n = {n}", ha="center", va="top", fontsize=8)
    ax.set_ylim(bottom=-1 * max(ns))

    # ylim etwas größer setzen, damit Sterne Platz haben
    y_max = df["count"].max()
    ax.set_ylim(bottom=-0.3 * max(ns), top=y_max * 1.2)

    # Mann-Whitney-U Tests für alle 4 Videos
    video_data = [df[df["video"] == i]["count"].values for i in range(1, 5)]
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]  # alle 6 Kombinationen
    n_tests = len(pairs)  # für Bonferroni Korrektur

    for i, j in pairs:
        stat, p = mannwhitneyu(video_data[i], video_data[j], alternative="two-sided")

        # Bonferroni-Korrektur
        p = min(p * n_tests, 1.0)

        if p < 0.05:  # nur Signifikanz anzeigen
            if p < 0.001:
                sig = "***"
            elif p < 0.01:
                sig = "**"
            else:
                sig = "*"

            # Striche innerhalb des Plot-Rahmens
            y_max_plot = ax.get_ylim()[1]  # aktuelles y-Limit
            max_y_pair = max(max(video_data[i]), max(video_data[j]))
            y = min(max_y_pair * 1.1, y_max_plot * 0.95)
            h = y_max_plot * 0.03

            ax.plot(
                [i + 1, i + 1, j + 1, j + 1],
                [y, y + h, y + h, y],
                lw=1,
                color="black",
            )
            ax.text((i + j) / 2 + 1, y + h, sig, ha="center", va="bottom", fontsize=12)

            # Legende
            handles = [Line2D([0], [0], color=color_map[i], lw=6) for i in range(1, 5)]
            ax.legend(handles, [label_map[i] for i in range(1, 5)], loc="upper right")

    plt.tight_layout()
    plt.savefig("fig_interactioncount_over_videos.pdf")
    plt.show()


if __name__ == "__main__":
    main()
