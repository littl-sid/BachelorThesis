import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def main():
    print("Hello from thesis!")
    print("Electric fish are amazing!")
    print("Testing git")
    x = np.arange(20)
    y = np.random.normal(size=len(x))
    plt.plot(x, y)
    plt.show()
    # some change


if __name__ == "__main__":
    main()
