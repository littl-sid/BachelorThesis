from IPython import embed
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import sort_files


def get_change_times_stop(df, interactions, platform):
    change_times = []

    # Nach Zeit sortieren
    df = df.sort_values("Time").reset_index(drop=True)

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        # Nur wenn Interaktion gefolgt von Platform-Ereignis
        if row["Behavior"] in interactions and next_row["Behavior"] in platform:
            duration = next_row["Time"] - row["Time"]
            change_times.append(duration)

    return change_times


def get_change_times_start(df, interactions, platform):
    change_times = []

    # Nach Zeit sortieren
    df = df.sort_values("Time").reset_index(drop=True)

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        # Nur wenn Interaktion gefolgt von Platform-Ereignis
        if row["Behavior"] in platform and next_row["Behavior"] in interactions:
            duration = next_row["Time"] - row["Time"]
            change_times.append(duration)

    return change_times


def get_data(sorted_files):
    interactions_A = ["int A 1", "int A 2"]
    platform_A = ["0 A", "1 A", "2 A", "3 A", "4 A"]
    interactions_B = ["int B 1", "int B 2"]
    platform_B = ["0 B", "1 B", "2 B", "3 B", "4 B"]

    all_A_start = []
    all_B_start = []
    all_A_stop = []
    all_B_stop = []
    all_data_start = []
    all_data_stop = []

    for trial in sorted_files:
        for f in trial:
            file = pd.read_csv(f)

            # DataFrames direkt filtern
            A = file[file["Behavior"].isin(interactions_A + platform_A)].reset_index(
                drop=True
            )
            B = file[file["Behavior"].isin(interactions_B + platform_B)].reset_index(
                drop=True
            )

            # Dauer berechnen
            A_start = get_change_times_start(A, interactions_A, platform_A)
            B_start = get_change_times_start(B, interactions_B, platform_B)
            A_stop = get_change_times_stop(A, interactions_A, platform_A)
            B_stop = get_change_times_stop(B, interactions_B, platform_B)

            all_A_start.extend(A_start)
            all_B_start.extend(B_start)
            all_data_start.extend(A_start + B_start)

            all_A_stop.extend(A_stop)
            all_B_stop.extend(B_stop)
            all_data_stop.extend(A_stop + B_stop)
    return (
        all_data_start,
        all_data_stop,
        all_A_start,
        all_B_start,
        all_A_stop,
        all_B_stop,
    )


def main():
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")
    sorted_files = sort_files(all_files)
    unfiltered_all_start, unfiltered_all_stop, A_start, B_start, A_stop, B_stop = (
        get_data(sorted_files)
    )

    all_start = [x for x in unfiltered_all_start if x <= 30]
    all_stop = [x for x in unfiltered_all_stop if x <= 30]
    print(f"vor -> vorher: {len(unfiltered_all_start)}, gefiltert: {len(all_start)}")
    print(f"nach -> vorher: {len(unfiltered_all_stop)}, gefiltert: {len(all_stop)}")

    # Pearson r Test (gefiltert)
    min_len = min(len(all_start), len(all_stop))
    r, p_value = pearsonr(all_start[:min_len], all_stop[:min_len])
    print(f"Gefiltert:   Pearson r = {r:.3f}, p = {p_value:.4f}")

    # Pearson r Test (ungefiltert)
    min_len = min(len(unfiltered_all_start), len(unfiltered_all_stop))
    r, p_value = pearsonr(unfiltered_all_start[:min_len], unfiltered_all_stop[:min_len])
    print(f"Ungefiltert: Pearson r = {r:.3f}, p = {p_value:.4f}")

    for name, dataset in zip(["vor", "nach"], [all_start, all_stop]):
        median = np.median(dataset)
        mean = np.mean(dataset)
        std = np.std(dataset)
        print(f"{name} -> Median: {median:.2f}, Mean: {mean:.2f}, Std: {std:.2f}")

    # ----- Plot -----
    data_to_plot = [all_start, all_stop]
    labels = ["vor", "nach"]

    fig, ax = plt.subplots(figsize=(6, 4.5))

    bp = ax.boxplot(
        data_to_plot,
        labels=labels,
        patch_artist=True,
        medianprops=dict(color="black"),
    )

    colors = ["skyblue", "seagreen"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    # Stichprobengröße unter den Boxen annotieren
    for i, d in enumerate(data_to_plot, start=1):
        n = len(d)
        ax.text(
            i,
            -0.5,
            f"n={n}",
            ha="center",
            va="top",
            fontsize=8,
        )

    ax.set_ylabel("Duration [s]")
    plt.tight_layout()
    plt.savefig("fig_interactions_effect.pdf")
    plt.show()


if __name__ == "__main__":
    main()
