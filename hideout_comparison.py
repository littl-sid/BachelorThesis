import matplotlib.pyplot as plt
from IPython import embed
import numpy as np

# Fish Lists
all_fish = [  # Frequency, Size, hideout at the end, Trial number
    [  # T1
        [900, 19, "große Röhre", 1],
        [770, 16, "kleine Röhre", 1],
        [870, 18, "mittlere Röhre", 1],
        [835, 14, "zwischen Futter und Röhre", 1],
    ],
    [  # T3
        [725, 17, "Wandspalt", 3],
        [875, 14, "E-Reihe", 3],
        [675, 16, "mittlere Röhre", 3],
        [910, 18, "große Röhre", 3],
    ],
    [  # T4
        [630, 15, "E-Reihe", 4],
        [780, 14, "große Röhre", 4],
        [644, 18, "E-Reihe", 4],
        [805, 19, "halb in Rampe", 4],
    ],
    [  # T5
        [809, 15, "kleine Röhre", 5],
        [808, 19, "mittlere Röhre", 5],
        [720, 17, "Wandspalt", 5],
        [840, 19, "große Röhre", 5],
    ],
    [  # T6
        [684, 14, "Wandspalt", 6],
        [660, 15, "mittlere Röhre", 6],
        [861, 18, "große Röhre", 6],
        [826, 15, "E-Kabel", 6],
    ],
    [  # T7
        [876, 18.5, "kleine Röhre", 7],
        [824, 20, "große Röhre", 7],
        [793, 15, "frei im Wasser", 7],
        [797, 18, "mittlere Röhre", 7],
    ],
    [  # T8
        [806, 16, "große Röhre", 8],
        [840, 15, "unter Rampe", 8],
        [810, 16.5, "unter Rampe", 8],
        [825, 20, "unter Rampe", 8],
    ],
    [  # T10
        [720, 17, "Wandspalt", 10],
        [730, 15, "E-Kabel", 10],
        [840, 20.5, "große Röhre", 10],
        [870, 19, "mittlere Röhre", 10],
    ],
    [  # T11
        [780, 15.5, "Wandspalt", 11],
        [770, 17, "große Röhre", 11],
        [614, 14, "mittlere Röhre", 11],
        [790, 20, "mittlere Röhre", 11],
    ],
    [  # T12
        [724, 13, "mittlere Röhre", 12],
        [837, 18, "große Röhre", 12],
        [650, 14, "Wanspalt", 12],
        [712, 13, "Wandspalt", 12],
    ],
]

hide_map = {"große Röhre": 1, "mittlere Röhre": 2, "kleine Röhre": 3}

colors = [
    "#6b8e23",
    "#8fbfbd",
    "#556b2f",
    "#4682b4",
    "#7ca982",
    "#b0c4de",
    "#c2b280",
    "#5f9ea0",
    "#a2ad00",
    "#8b7765",
]
trial_numbers = sorted({trial[0][-1] for trial in all_fish})
color_map = {trial: colors[i % len(colors)] for i, trial in enumerate(trial_numbers)}


def plot_by_attribute(attribute_index, name, name_2):
    plt.figure(figsize=(6, 4.5))

    all_ranks = []
    all_hide_nums = []

    for trial in all_fish:
        trial_number = trial[0][-1]
        color = color_map[trial_number]

        sorted_fishes = sorted(trial, key=lambda x: x[attribute_index], reverse=True)
        ranks = []
        hide_nums = []

        for rank, fish in enumerate(sorted_fishes, start=1):
            hide_num = hide_map.get(fish[2], 4)
            ranks.append(rank)
            hide_nums.append(hide_num)
            all_ranks.append(rank)
            all_hide_nums.append(hide_num)

        plt.scatter(ranks, hide_nums, s=50, color=color)
        z = np.polyfit(ranks, hide_nums, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(ranks), max(ranks), 100)
        plt.plot(x_line, p(x_line), linestyle="-", alpha=0.5, color=color)

        slope = z[0]
        n = len(ranks)
        plt.scatter(
            [], [], color=color, label=f"Trial {trial_number}: m={slope:.2f} (n={n})"
        )

    z_all = np.polyfit(all_ranks, all_hide_nums, 1)
    p_all = np.poly1d(z_all)
    x_line_all = np.linspace(min(all_ranks), max(all_ranks), 100)
    plt.plot(x_line_all, p_all(x_line_all), linestyle="-", color="black", alpha=1)
    slope_all = z_all[0]
    n_all = len(all_ranks)
    plt.scatter([], [], color="black", label=f"Gesamt: m={slope_all:.2f} (n={n_all})")

    plt.xticks([1, 2, 3, 4], ["1", "2", "3", "4"])
    plt.yticks(
        [1, 2, 3, 4], ["große Röhre", "mittlere Röhre", "kleine Röhre", "andere"]
    )
    plt.xlabel(f"Rang nach {name_2}")
    plt.ylabel("Versteck Qualität")
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    plt.tight_layout()
    plt.savefig(f"hideout_end_comparison_{name}.pdf")
    plt.show()


def plot_frequency_vs_size():
    plt.figure(figsize=(6, 4.5))

    all_x_vals = []
    all_y_vals = []

    for trial in all_fish:
        trial_number = trial[0][-1]
        color = color_map[trial_number]

        freq_sorted = sorted(trial, key=lambda x: x[0], reverse=True)
        freq_ranks = {
            tuple(fish): rank for rank, fish in enumerate(freq_sorted, start=1)
        }
        size_sorted = sorted(trial, key=lambda x: x[1], reverse=True)
        size_ranks = {
            tuple(fish): rank for rank, fish in enumerate(size_sorted, start=1)
        }

        x_vals = []
        y_vals = []
        for fish in trial:
            key = tuple(fish)
            x_vals.append(freq_ranks[key])
            y_vals.append(size_ranks[key])
            all_x_vals.append(freq_ranks[key])
            all_y_vals.append(size_ranks[key])

        plt.scatter(x_vals, y_vals, s=50, color=color)
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(x_vals), max(x_vals), 100)
        plt.plot(x_line, p(x_line), linestyle="-", alpha=0.5, color=color)

        slope = z[0]
        n = len(x_vals)
        plt.scatter(
            [], [], color=color, label=f"Trial {trial_number}: m={slope:.2f} (n={n})"
        )

    z_all = np.polyfit(all_x_vals, all_y_vals, 1)
    p_all = np.poly1d(z_all)
    x_line_all = np.linspace(min(all_x_vals), max(all_x_vals), 100)
    plt.plot(x_line_all, p_all(x_line_all), linestyle="-", color="black", alpha=1)
    slope_all = z_all[0]
    n_all = len(all_x_vals)
    plt.scatter([], [], color="black", label=f"Gesamt: m={slope_all:.2f} (n={n_all})")

    plt.xticks([1, 2, 3, 4])
    plt.yticks([1, 2, 3, 4])
    plt.xlabel("Rang nach Frequenz")
    plt.ylabel("Rang nach Größe")
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    plt.tight_layout()
    plt.savefig("hideout_end_comparison_attributes.pdf")
    plt.show()


def main():
    plot_by_attribute(attribute_index=1, name="size", name_2="Größe")
    plot_by_attribute(attribute_index=0, name="frequency", name_2="Frequenz")
    plot_frequency_vs_size()


if __name__ == "__main__":
    main()
