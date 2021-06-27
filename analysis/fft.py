import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys 
from scipy.fftpack import fft, fftfreq 

def main():
    file = sys.argv[1]
    df = pd.read_csv(file)
    df = df[['mag_x','mag_y','mag_z']]
    df['mag'] = np.linalg.norm(df[['mag_x','mag_y','mag_z']], axis=1)
    const = np.average(df['mag'])
    df['mag'] = df['mag'] - const

    n = df['mag'].size
    print(f"n = {n}")
    freq = fftfreq(n, d=3/n)
    fourier = fft(df['mag'].to_numpy())
    amplitudes = np.abs(fourier)

    dom = np.argmax(amplitudes)
    print(f"Dominant frequency {freq[dom]}, {amplitudes[dom]}")

    plt.yscale('log')
    plt.title('Fourier transform of magnetic intensity')
    plt.plot(freq, amplitudes)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Time from experiment start (min)")
    plt.ylabel("Magnetic field strength (μT)")

    plt.savefig("fft.png")

if __name__ == "__main__":
    main()
