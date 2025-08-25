from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import sort_files, get_interactions


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # sort files for trial and video number
    sorted_files = sort_files(all_files)

    # count in trial videos the interactions
    for trial in sorted_files:
        interaction_count = []
        for v in trial:
            file = pd.read_csv(v)
            interactions = get_interactions(file)
            interaction_count.append(len(interactions))


if __name__ == "__main__":
    main()
