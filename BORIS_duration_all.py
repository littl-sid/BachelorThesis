import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np


def get_duration(files, behavior):
    behavior_periods = []
    # go through files
    for f in files:
        file = pd.read_csv(f)

        # get periods of chasing
        start_time = None

        if behavior == "chasing onset":
            for _, row in file.iterrows():
                if row["Behavior"] == "chasing onset":
                    start_time = row["Time"]
                elif row["Behavior"] == "chasing offset":
                    behavior_periods.append([start_time, row["Time"]])
                    start_time = None
        else:
            for _, row in file.iterrows():
                if (
                    row["Behavior"] == behavior
                    and row["Behavior type"].upper() == "START"
                ):
                    start_time = row["Time"]
                elif (
                    row["Behavior"] == behavior
                    and row["Behavior type"].upper() == "STOP"
                ):
                    behavior_periods.append([start_time, row["Time"]])
                    start_time = None

    # sort data
    durations = []
    for t in behavior_periods:
        if t[0] is None or t[1] is None:
            continue
        duration = float(t[1]) - float(t[0])
        durations.append(duration)
    return durations


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")

    chase = get_duration(all_files, "chasing onset")
    mouth = get_duration(all_files, "Mouth Aggression")
    shove = get_duration(all_files, "shoving")

    data_to_plot = [chase, mouth, shove]
    labels = ["Chasing", "Mouth Aggression", "Shoving"]
    colors = ["seagreen", "skyblue", "orange"]

    # Kurze Stat-Ausgabe pro Kategorie
    for name, dataset in zip(labels, data_to_plot):
        median = np.median(dataset)
        mean = np.mean(dataset)
        std = np.std(dataset)
        print(f"{name} -> Median: {median:.2f}, Mean: {mean:.2f}, Std: {std:.2f}")

    # ----- Plot -----
    fig, ax = plt.subplots(figsize=(6, 4.5))

    bp = ax.boxplot(
        data_to_plot,
        patch_artist=True,
        labels=labels,
        medianprops=dict(color="black"),
    )

    # Farben setzen – jede Box bekommt ihre definierte Farbe
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    # Stichprobengrößen annotieren
    for i, d in enumerate(data_to_plot, start=1):
        n = len(d)
        ax.text(
            i,
            -1.6,
            f"n={n}",
            ha="center",
            va="top",
            fontsize=9,
        )

    ax.set_ylabel("Dauer [s]")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig("fig_duration_all_behaviors.pdf")
    plt.show()


if __name__ == "__main__":
    main()
