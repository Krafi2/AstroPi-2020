import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
import sys 

def main():
    file = sys.argv[1]
    df = pd.read_csv(file)
    mag = df[['mag_x','mag_y','mag_z']]
    df['norm'] = np.linalg.norm(mag.values, axis=1)
    n = df['norm'].size
    plt.title('Magnetometer')
    x = np.arange(n) / n * 180 
    y = df['norm']
    plt.plot(x,y)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Time from experiment start (min)")
    plt.ylabel("Magnetic field strength (μT)")

    plt.savefig("magnetometer.jpg")

if __name__ == "__main__":
    main()
