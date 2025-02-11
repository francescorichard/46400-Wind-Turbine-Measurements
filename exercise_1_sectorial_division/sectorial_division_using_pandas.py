#%% PACKAGES
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#read the data
data = pd.read_csv("C:\COPENAGHEN PRIMO ANNO\WIND_TURBINE_MEASUREMENTS\exercises\exercise 1_sectorial_division\wind_stats.csv",parse_dates=['SCAN_NAME'],index_col='SCAN_NAME')

#overall statistics
mean_speed = data['ws62'].mean()
mean_stdv = data['stdev62'].mean()

#create ti
data['ti62'] = data['stdev62']/data['ws62']
mean_ti = data['ti62'].mean()

#let's count if there are any data missing
num_data = data.shape[0]/data.count()[0]

#let's plot the results
colors = ['#c3121e','#0348a1']
fig = plt.figure(figsize=(16,12))
ax1 = fig.add_subplot(411)
data['ws62'].plot(ax=ax1,ylabel='wind speed 62 m',color=colors[0])

ax2=fig.add_subplot(412)
data['stdev62'].plot(ax=ax2,ylabel="sigma wind speed 62 m",color=colors[1])

ax3=fig.add_subplot(413)
data['wd60'].plot(ax=ax3,ylabel="wind direction at 60 m",color = colors[0])

ax4=fig.add_subplot(414)
data['ti62'].plot(ax=ax4,ylabel="TI at 62 m",xlabel='time',color=colors[1])
plt.show()

#%% dividng in sector bins
num_sectors = 12
sector_width = 360/num_sectors
data.loc[(data['wd60'] >= 0) & (data['wd60']<15), 'wd60'] += 360
statistic_values = np.zeros((12,3))
for ii in range(0,num_sectors):
    if ii==0:
        sector_start = 360-sector_width/2
        sector_end = 360+sector_width/2
    else:
        sector_start = ii*sector_width-sector_width/2
        sector_end = ii*sector_width+sector_width/2
    string = 'bin '+str(ii*sector_width)
    data[string] = (data['wd60'] >= sector_start) & (data['wd60']<sector_end)
    statistic_values[ii,0] = data.loc[data[string],'ws62'].mean()
    statistic_values[ii,1] = (data.loc[data[string],'stdev62']/data.loc[data[string],'ws62']).mean()
    statistic_values[ii,2] = data[data[string]].shape[0]/data.shape[0]*100
statistic_values = pd.DataFrame(statistic_values,columns=['mean62m','stdev62m','frequency [%%]'],index=
             ['0','30','60','90','120','150','180','210','240','270','300','330'])