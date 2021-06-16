import numpy as np
import matplotlib.pyplot as plt
import common
import sys

def magnitudes(file: str) -> [float]:
    data = common.Data(file)
    mag = [np.linalg.norm(i) for i in data.mag]
    return mag

# Takes the path of the data file as a command line argument and
# saves the plot of the strength of the magnetic field
def main():
    file = sys.argv[1]
    mag = magnitudes(file)
    plt.plot(mag)
    plt.savefig("magnitude_plot.jpg")

if __name__ == "__main__":
    main()