import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")

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

    # kurzer Eunschub Daten berechnen
    median = np.median(chase_durations)
    mean = np.mean(chase_durations)
    std = np.std(chase_durations)
    print(f"Median: {median:.2f}, Mean: {mean:.2f}, Std: {std:.2f}")

    # ----- Plot -----
    fig, ax = plt.subplots(figsize=(3, 2.25))  # 6, 4.5
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
        -0.5,  # y-Position unter der x-Achse, ggf. anpassen
        f"n = {n}",
        ha="center",
        va="top",
        fontsize=8,
    )

    plt.tight_layout()
    plt.savefig("fig_duration_chase.pdf")
    plt.show()


if __name__ == "__main__":
    main()
