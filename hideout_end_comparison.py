import matplotlib.pyplot as plt

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
    [  # T9
        [685, 13, "mittlere Röhre"],
        [647, 15, "Wandspalt"],
        [722, 14, "mittlere Röhre"],
        [833, 18, "große Röhre"],
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


def main():
    # Durch jeden Trial durchgehen
    for trial in all_fish:
        # Durch jeden Fisch durchgehen und den größten herausfinden
        fishes_in_trial = []
        for fish in trial:
            fish.append(fishes_in_trial)


if __name__ == "__main__":
    main()
