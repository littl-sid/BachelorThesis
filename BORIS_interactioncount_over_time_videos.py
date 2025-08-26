from IPython import embed
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from itertools import combinations
from scipy.stats import mannwhitneyu
import matplotlib.patches as mpatches
import pandas as pd
import glob
import numpy as np
from functions import get_interactions, get_trial_and_video


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # count in trial videos the interactions
    interaction_count = []
    for v in all_files:
        _, video_number = get_trial_and_video(v)

        file = pd.read_csv(v)
        interactions = get_interactions(file)
        interaction_count.append([len(interactions), video_number])

    # Data sorting
    video_numbers = sorted(set(i[1] for i in interaction_count))
    data = []
    video = []
    for vn in video_numbers:
        counts = [i[0] for i in interaction_count if i[1] == vn]
        data.append(counts)
        video.append(vn)

    # ----- Boxplot -----
    plt.figure(figsize=(10, 6))

    bp = plt.boxplot(
        data,
        labels=[f"Video {vn}" for vn in video],
        patch_artist=True,
        boxprops=dict(facecolor="white", color="black"),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", color="red", alpha=0.5),
    )

    # Boxcolors
    box_colors = ["gold", "orangered", "skyblue", "seagreen"]
    for patch, color in zip(bp["boxes"], box_colors):
        patch.set_facecolor(color)

    handles = []

    for vn, counts, color in zip(video, data, box_colors):
        n = len(counts)
        if vn in [1, 3]:
            label_text = f"Tag auf Nacht (n={n})"
        else:
            label_text = f"Nacht auf Tag (n={n})"
        handles.append(
            mpatches.Patch(facecolor=color, label=f"Video {vn}: {label_text}")
        )

    # --- pairwise whitney-u-test ---
    alpha = 0.05
    positions = range(1, len(data) + 1)  # positions of boxes on x-axis

    # function to convert p-value to stars
    def significance_stars(p):
        if p < 0.001:
            return "***"
        elif p < 0.01:
            return "**"
        elif p < 0.05:
            return "*"
        else:
            return ""

    # line offset to stagger multiple stars
    base_offset = 5
    step = 1
    line_count = 0

    # pairwise comparisons
    for i, j in combinations(range(len(data)), 2):
        stat, p = mannwhitneyu(data[i], data[j], alternative="two-sided")
        stars = significance_stars(p)
        if stars:
            y = max(max(data[i]), max(data[j])) + base_offset + line_count * step
            plt.plot([positions[i], positions[j]], [y, y], color="black", linewidth=1)
            plt.text((positions[i] + positions[j]) / 2, y + 0.1, stars, ha="center")
            line_count += 1

    # ----- draw single legend -----
    plt.legend(handles=handles, bbox_to_anchor=(1, 1), loc="upper right")

    plt.ylabel("# Interaktionen")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("fig_interactioncount_over_time_videos.pdf")
    plt.show()


if __name__ == "__main__":
    main()
