'''
Created on 31. jan. 2018

@author: ELP
'''
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('q_mca048_Opo.csv',sep=';')
df = df[df.Q_m3_s >= 0]
df.Time = pd.to_datetime(df['Time'], format='%d.%m.%y %H:%M') 
df = df.sort_values('Time')

fig, (ax, ax2) = plt.subplots(2, 1, sharey=False,figsize = (10,6))

ax.plot(df.Time.values, df.Q_m3_s.values,'o',markersize = 1) 
ax2.plot(df.Time.values, df.h_m.values,'o',markersize = 1) 

ax2.set_xlabel('Time')
ax.set_ylabel('Q_m3_s')
ax2.set_ylabel('h_m')

plt.show()
