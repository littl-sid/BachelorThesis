from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from functions import sort_files


def main():
    # alle passenden CSV-Dateien suchen
    all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # Dateien nach Trial und Video sortieren
    sorted_files = sort_files(all_files)


if __name__ == "__main__":
    main()
