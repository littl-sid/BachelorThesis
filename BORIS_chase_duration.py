import matplotlib.pyplot as plt
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

    chase_durations = []
    for t in chase_periods:
        if t[0] is None or t[1] is None:
            continue
        duration = float(t[1]) - float(t[0])
        chase_durations.append(duration)

    # ----- Plot -----
    plt.figure(figsize=(6, 6))
    plt.boxplot(
        chase_durations, patch_artist=True, boxprops=dict(facecolor="saddlebrown")
    )
    plt.ylabel("Chase Dauer [s]")
    plt.xticks([])
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Statistics
    median_chase = np.median(chase_durations)
    mean_chase = np.mean(chase_durations)
    std_chase = np.std(chase_durations, ddof=1)
    n = len(chase_durations)

    # Legend
    stats_text = (
        f"Median = {median_chase:.2f}\n"
        f"Mittelwert = {mean_chase:.2f}\n"
        f"SD = {std_chase:.2f}\n"
        f"n = {n}"
    )
    plt.legend(
        [stats_text],
        handlelength=0,
        frameon=True,
        loc="upper right",
    )

    plt.savefig("fig_chase_duration.png")
    plt.show()


if __name__ == "__main__":
    main()
