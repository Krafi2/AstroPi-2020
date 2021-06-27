import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import os
import pandas as pd
import csv
from scipy.fft import fft, fftfreq
import matplotlib.pyplot  as pyplot



data = r'C:\school\kgang\output.csv'
df = pd.read_csv(data)
res = df.to_numpy()
# vector_df = df[['acc_x','acc_y','acc_z']]/
# df[['date', 'ts']] = df['date/time'].str.split(' ', 1, expand=True)
# vector_df.apply(np.linalg.norm(), axis = 1, result_type='expand')
# df['norm'] = np.linalg.norm(vector_df[['acc_x','acc_y','acc_z']].values,axis=1)
# magnetometer_df = df[['ts','vector']]

# yf = fft(df['norm'].to_numpy())
# yf = np.abs(yf)
# plt.plot(yf)
# plt.show()
# n = df['norm'].size
# xf = fftfreq(n, d=3/n)
# res = [np.linalg.norm(i) for i in yf]
fig = plt.figure()
#
ax = fig.add_subplot()
ax.set_yscale('log')
# max_y = max(res)  # Find the maximum y value
# max_x = xf[res.index(max_y)]  # Find the x value corresponding to the maximum y value
# print(max_x, max_y)
# plt.plot(xf, res)

plt.plot(res)
plt.show()
