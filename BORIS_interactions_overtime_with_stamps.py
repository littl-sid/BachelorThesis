import matplotlib.pyplot as plt
import pandas as pd
from IPython import embed
import glob
import numpy as np
from matplotlib.lines import Line2D
from functions import sort_files, get_interactions, sort_for_videos


def get_stamps_plot(files, video_number):
    for f in files:
        file = pd.read_csv(f)

        all_interactions = get_interactions(file)
        interactions = []
        timestamp = []

        for _, row in all_interactions.iterrows():
            interaction = row["Behavior"]
            time = row["Time"]

            interactions.append(interaction)
            timestamp.append(time)

            plt.scatter(timestamp, interactions)
    plt.title(f"Video{video_number}")
    plt.show()


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")

    V1, V2, V3, V4 = sort_for_videos(all_files)
    get_stamps_plot(V1, 1)
    get_stamps_plot(V2, 2)
    get_stamps_plot(V3, 3)
    get_stamps_plot(V4, 4)


if __name__ == "__main__":
    main()
