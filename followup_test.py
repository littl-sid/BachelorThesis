from scipy.stats import mannwhitneyu
from IPython import embed
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import numpy as np
import itertools
from functions import get_interactions, sort_files, get_followup_interactions


def count_interactions(files):
    all_interactions = []

    for f in files:
        file = pd.read_csv(f)
        interactions = get_interactions(file)
        all_interactions.append(len(interactions))
    return all_interactions


def count_followup_interactions(files):
    all_interactions = []

    for f in files:
        file = pd.read_csv(f)
        interactions = get_followup_interactions(file)
        all_interactions.append(len(interactions))
    return all_interactions


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events_followup/Trial*_V*_events.csv")

    # sort files for trial and video number
    sorted_files = sort_files(all_files)

    interactions_old = []
    interactions_followup = []

    for trial in sorted_files:
        count = count_interactions(trial)
        interactions_old.append(count)

        count_followup = count_followup_interactions(trial)
        interactions_followup.append(count_followup)

    print(f"old:{interactions_old} followup: {interactions_followup}")


if __name__ == "__main__":
    main()
