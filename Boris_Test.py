import matplotlib.pyplot as plt
from IPython import embed
import numpy as np
import glob
from functions import sort_files


def main():
    # alle passenden CSV-Dateien suchen
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # Dateien nach Trial und Video sortieren
    sorted_files = sort_files(all_files)


if __name__ == "__main__":
    main()
