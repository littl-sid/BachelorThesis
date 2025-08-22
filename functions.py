from IPython import embed
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
