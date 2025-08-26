import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import glob
import numpy as np


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    chase_periods = []
    # go through files
    for f in all_files:
        file = pd.read_csv(f)

        # get periods of chasing
        start_time = None
        for _, row in file.iterrows():
            if row["Behavior"] == "chasing onset":
                start_time = row["Time"]
            elif row["Behavior"] == "chasing offset":
                chase_periods.append([start_time, row["Time"]])
                start_time = None

    # sort data
    chase_durations = []
    for t in chase_periods:
        if t[0] is None or t[1] is None:
            continue
        duration = float(t[1]) - float(t[0])
        chase_durations.append(duration)

    # ----- Plot -----
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(
        chase_durations,
        patch_artist=True,
        boxprops=dict(facecolor="seagreen"),
        medianprops=dict(color="black"),
    )
    ax.set_ylabel("Chase Dauer [s]")
    ax.set_ylim(bottom=0)
    ax.set_xticks([])
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    n = len(chase_durations)
    plt.text(
        1,  # x position
        -0.1,  # y-Position unter der x-Achse, ggf. anpassen
        f"n = {n}",
        ha="center",
        va="top",
        fontsize=10,
    )

    plt.tight_layout()
    plt.savefig("fig_duration_chase.pdf")
    plt.show()


if __name__ == "__main__":
    main()
