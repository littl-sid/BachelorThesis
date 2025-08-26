from IPython import embed
import matplotlib.pyplot as plt
import pandas as pd
import re


def sort_files(files):
    # alle passenden CSV-Dateien suchen
    # all_files = glob.glob("BORIS_events/Trial*_V*_events.csv")

    # Regex zum Herausziehen von Trial- und Video-Nummern
    pattern = re.compile(r"Trial(\d+)_")

    # Listen für die Trials
    T3 = []
    T4 = []
    T5 = []
    T6 = []
    T7 = []
    T8 = []
    T10 = []
    T11 = []
    T12 = []

    for f in files:
        match = pattern.search(f)
        if match:
            trial_num = int(match.group(1))
            if trial_num == 3:
                T3.append(f)
            elif trial_num == 4:
                T4.append(f)
            elif trial_num == 5:
                T5.append(f)
            elif trial_num == 6:
                T6.append(f)
            elif trial_num == 7:
                T7.append(f)
            elif trial_num == 8:
                T8.append(f)
            elif trial_num == 10:
                T10.append(f)
            elif trial_num == 11:
                T11.append(f)
            elif trial_num == 12:
                T12.append(f)

    # Jede Liste alphabetisch sortieren
    T3.sort()
    T4.sort()
    T5.sort()
    T6.sort()
    T7.sort()
    T8.sort()
    T10.sort()
    T11.sort()
    T12.sort()

    return T3, T4, T5, T6, T7, T8, T10, T11, T12


def get_all_interactions(file):
    # get the interaction events of the file
    interactions_def = [
        "contact",
        "Tail Whip",
        "Mouth Aggression",
        "shoving",
        "bluff charge",
        "chasing onset",
        "chasing offset",
    ]

    interactions = file[
        file["Behavior"].str.contains("|".join(interactions_def), case=False, na=False)
    ]
    return interactions


def get_interactions(file):
    interactions_def = [
        "contact",
        "Tail Whip",
        # "Mouth Aggression",
        # "shoving",
        "bluff charge",
        "chasing onset",
    ]

    interactions = []
    for _, row in file.iterrows():
        if row["Behavior"] in ["Mouth Aggression", "shoving"]:
            # nur Start-Zeilen
            if row["Behavior type"].upper() == "START":
                interactions.append(row)
        elif row["Behavior"] in interactions_def:
            interactions.append(row)

    # in DataFrame zurückwandeln
    return pd.DataFrame(interactions)


# def get_interactions(file):
#     # get the interaction events of the file
#     interactions_def = [
#         "contact",
#         "Tail Whip",
#         "Mouth Aggression",
#         "shoving",
#         "bluff charge",
#         "chasing onset",
#     ]

#     interactions = file[
#         file["Behavior"].str.contains("|".join(interactions_def), case=False, na=False)
#     ]
#     return interactions


def get_periods(file, behaviors):
    # get the perios in which behaviors occur
    periods = []
    start_time = None
    for _, row in file.iterrows():
        if row["Behavior"] in behaviors and row["Behavior type"].upper() == "START":
            start_time = row["Time"]
        elif (
            row["Behavior"] in behaviors
            and row["Behavior type"].upper() == "STOP"
            and start_time is not None
        ):
            periods.append((start_time, row["Time"]))
            start_time = None
    return periods


def get_trial_and_video(file):
    # --- get trial- & video number from filename with pattern such as: 'BORIS_events/Trial5_V3_events.csv'

    trial_match = re.search(r"Trial(\d+)", file)
    video_match = re.search(r"V(\d+)", file)

    trial_number = int(trial_match.group(1)) if trial_match else None
    video_number = int(video_match.group(1)) if video_match else None

    return trial_number, video_number


def get_legend(file):
    trial, _ = get_trial_and_video(file)
    color_A, _ = get_color(file)
    _, color_B = get_color(file)

    if 1 <= trial <= 6:
        legend = [
            plt.Line2D([0], [0], color=color_A, lw=4, label="A schlechte Platte"),
            plt.Line2D([0], [0], color=color_B, lw=4, label="B gute Platte"),
        ]
    elif 7 <= trial <= 12:
        legend = [
            plt.Line2D([0], [0], color=color_A, lw=4, label="A gute Platte"),
            plt.Line2D([0], [0], color=color_B, lw=4, label="B schlechte Platte"),
        ]
    else:
        legend = []

    return legend


def get_color(file):
    trial, _ = get_trial_and_video(file)

    if 1 <= trial <= 6:
        # A = schlechte Platte, B = gute Platte
        color_A = "skyblue"
        color_B = "seagreen"
    elif 7 <= trial <= 12:
        # Bedeutung umgekehrt
        color_A = "seagreen"
        color_B = "skyblue"
    return color_A, color_B
