from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import get_periods, get_interactions


def main():
    # get all CSV files
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")
    sorted_files = sort_files(all_files)

    for trial in sorted_files:
        


if __name__ == "__main__":
    main()
