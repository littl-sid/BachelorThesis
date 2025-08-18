import matplotlib.pyplot as plt
from IPython import embed
import numpy as np

# Fish Lists
all_fish = [  # Trial_1, ..., Trial_12 - Frequency, Size hideout at the end
    [  # T1
        [900, 19, "große Röhre"],
        [770, 16, "kleine Röhre"],
        [870, 18, "mittlere Röhre"],
        [835, 14, "zwischen Futter und Röhre"],
    ],
    [  # T3
        [725, 17, "Wandspalt"],
        [875, 14, "E-Reihe"],
        [675, 16, "mittlere Röhre"],
        [910, 18, "große Röhre"],
    ],
    [  # T4
        [630, 15, "E-Reihe"],
        [780, 14, "große Röhre"],
        [644, 18, "E-Reihe"],
        [805, 19, "halb in Rampe"],
    ],
    [  # T5
        [809, 15, "kleine Röhre"],
        [808, 19, "mittlere Röhre"],
        [720, 17, "Wandspalt"],
        [840, 19, "große Röhre"],
    ],
    [  # T6
        [684, 14, "Wandspalt"],
        [660, 15, "mittlere Röhre"],
        [861, 18, "große Röhre"],
        [826, 15, "E-Kabel"],
    ],
    [  # T7
        [876, 18.5, "kleine Röhre"],
        [824, 20, "große Röhre"],
        [793, 15, "frei im Wasser"],
        [797, 18, "mittlere Röhre"],
    ],
    [  # T8
        [806, 16, "große Röhre"],
        [840, 15, "unter Rampe"],
        [810, 16.5, "unter Rampe"],
        [825, 20, "unter Rampe"],
    ],
    [  # T10
        [720, 17, "Wandspalt"],
        [730, 15, "E-Kabel"],
        [840, 20.5, "große Röhre"],
        [870, 19, "mittlere Röhre"],
    ],
    [  # T11
        [780, 15.5, "Wandspalt"],
        [770, 17, "große Röhre"],
        [614, 14, "mittlere Röhre"],
        [790, 20, "mittlere Röhre"],
    ],
    [  # T12
        [724, 13, "mittlere Röhre"],
        [837, 18, "große Röhre"],
        [650, 14, "Wanspalt"],
        [712, 13, "Wandspalt"],
    ],
]


# Mapping-Tabelle
hide_map = {"große Röhre": 1, "mittlere Röhre": 2, "kleine Röhre": 3, "Wandspalt": 4}

# Farbpalette für Trials
colors = plt.cm.tab10.colors  # 10 Farben aus matplotlib Tab10


def plot_by_attribute(attribute_index, title):
    plt.figure(figsize=(8, 5))
    for trial_idx, trial in enumerate(all_fish, start=1):
        color = colors[(trial_idx - 1) % len(colors)]  # Farbe für Trial

        # Nach gewähltem Attribut sortieren (0=Frequenz, 1=Größe)
        sorted_fishes = sorted(trial, key=lambda x: x[attribute_index], reverse=True)

        ranks = []
        hide_nums = []
        for rank, fish in enumerate(sorted_fishes, start=1):
            hide_num = hide_map.get(fish[2], 5)
            ranks.append(rank)
            hide_nums.append(hide_num)

        # Scatterpunkte
        plt.scatter(ranks, hide_nums, s=50, edgecolor="black", color=color)

        # Trendlinie
        z = np.polyfit(ranks, hide_nums, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(ranks), max(ranks), 100)
        plt.plot(x_line, p(x_line), linestyle="-", alpha=0.8, color=color)

        # Legende mit Steigung
        slope = z[0]
        plt.scatter([], [], color=color, label=f"Trial {trial_idx}: m={slope:.2f}")

    # Achsen und Labels
    plt.xticks([1, 2, 3, 4], ["1", "2", "3", "4"])
    plt.yticks(
        [1, 2, 3, 4, 5],
        ["große Röhre", "mittlere Röhre", "kleine Röhre", "Wandspalt", "andere"],
    )
    plt.xlabel("Rang (1 = höchster Wert)")
    plt.ylabel("Versteck")
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()


def plot_frequency_vs_size():
    plt.figure(figsize=(8, 5))
    for trial_idx, trial in enumerate(all_fish, start=1):
        color = colors[(trial_idx - 1) % len(colors)]

        # Ränge für Frequenz
        freq_sorted = sorted(trial, key=lambda x: x[0], reverse=True)
        freq_ranks = {
            tuple(fish): rank for rank, fish in enumerate(freq_sorted, start=1)
        }

        # Ränge für Größe
        size_sorted = sorted(trial, key=lambda x: x[1], reverse=True)
        size_ranks = {
            tuple(fish): rank for rank, fish in enumerate(size_sorted, start=1)
        }

        # Daten zum Plotten: Frequenz-Rang gegen Größe-Rang
        x_vals = []
        y_vals = []
        for fish in trial:
            key = tuple(fish)
            x_vals.append(freq_ranks[key])
            y_vals.append(size_ranks[key])

        plt.scatter(x_vals, y_vals, s=50, edgecolor="black", color=color)
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(x_vals), max(x_vals), 100)
        plt.plot(x_line, p(x_line), linestyle="-", alpha=0.8, color=color)
        slope = z[0]
        plt.scatter([], [], color=color, label=f"Trial {trial_idx}: m={slope:.2f}")

    plt.xlabel("Rang nach Frequenz (1 = höchster Wert)")
    plt.ylabel("Rang nach Größe (1 = höchster Wert)")
    plt.title("Rang der Frequenz vs Rang der Größe")
    plt.xticks([1, 2, 3, 4])
    plt.yticks([1, 2, 3, 4])
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()


def main():
    plot_by_attribute(attribute_index=1, title="Fisch-Ränge nach Größe mit Trendlinien")
    plot_by_attribute(
        attribute_index=0, title="Fisch-Ränge nach Frequenz mit Trendlinien"
    )
    plot_frequency_vs_size()


if __name__ == "__main__":
    main()
