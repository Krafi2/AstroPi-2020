import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import os
import pandas as pd
import csv

data = r'C:\school\kgang\data01.csv'


df = pd.read_csv(data)  

vector_df = df[['acc_x','acc_y','acc_z']]
df[['date', 'ts']] = df['date/time'].str.split(' ', 1, expand=True)
# vector_df.apply(np.linalg.norm(), axis = 1, result_type='expand')
df['norm'] = np.linalg.norm(vector_df[['acc_x','acc_y','acc_z']].values,axis=1)
# magnetometer_df = df[['ts','vector']]
# magnetometer_df = df[['vector']]
df['ts'].to_string()
figure(num=None, dpi=200, facecolor='w', edgecolor='k')
fig = plt.figure()

fig.set_figheight(5)
fig.set_figwidth(20)

plt.title('Magnetometer')
result = df[['norm']]
# plt.xlabel('ts')
# plt.ylabel('')
x = df['ts']
y = df['norm']
_, ax = plt.subplots(figsize=(10,6))
plt.plot(x,y)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

ax.set_xticks(['23:47:09.387459','00:00:00.389181','00:15:00.942102','00:30:01.118891','00:45:01.228531',
               '00:59:59.037723', '01:15:00.400303', '01:30:00.886085', '01:45:01.032100', '02:00:00.882025',
               '02:15:00.847863','02:30:00.738659', '02:45:00.847540'])
ax.set_xticklabels(['23:45', '00:00', '00:15', '00:30','00:45','01:00','01:15','01:30','01:45','02:00',
                    '02:15', '02:30', '02:45' ])
# figure(num=None, dpi=200, facecolor='w', edgecolor='k')
# fig = plt.figure()
#
# fig.set_figheight(5)
# fig.set_figwidth(10)

plt.title('Magnetometer')
# result = df[['norm']]
#
# plt.xlim([450, 650])
plt.show()
# save_name = str('magnetometer')+'.png'
# plt.savefig(save_name, dpi=200)


