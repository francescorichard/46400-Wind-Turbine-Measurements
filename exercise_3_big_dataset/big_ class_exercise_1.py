
#%% IMPORT PACKAGES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

#%% SETTINGS FOR GRAPHS
mpl.rcParams['figure.figsize']  = (16,12)
mpl.rcParams['font.size'] = 14
mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.titlesize'] = 14
mpl.rcParams['legend.fontsize'] = 14

#%% IMPORT DATAS
WindData = pd.read_csv("C:\COPENAGHEN PRIMO ANNO\WIND_TURBINE_MEASUREMENTS\exercises\exercise 3_big_dataset\dataset.csv",parse_dates=['date_time'],index_col='date_time',
                       sep=';')

#%% PLOT DATA
# You can zoom in data and plot just one part to speed it up by using the function
# WindData['columnname'].loc['initialtime:finaltime']
colors = ['#003f5c','#bc5090','#ffa600']
fig, (ax1, ax2, ax3) = plt.subplots(3,1,figsize=(16,12))
ax1.plot(WindData.index,WindData['Wsp_18m'],linestyle='--',linewidth=1,label='$18\:m$',color = colors[0],alpha = 0.6)
ax1.plot(WindData.index,WindData['Wsp_44m'],linestyle='--',linewidth=1,label='$44\:m$',color = colors[1],alpha = 0.6)
ax1.plot(WindData.index,WindData['Wsp_70m'],linestyle='--',linewidth=1,label='$70\:m$',color = colors[2],alpha=0.6)
ax1.set_ylabel('Wind speed',fontweight='bold')
ax1.legend()
ax1.set_xlim([WindData.index[0],WindData.index[-1]])

ax2.plot(WindData.index,WindData['Wdir_41m'],linestyle='--',linewidth=1,label='$41\:m$',color = colors[0])
ax2.set_ylabel('Wind direction',fontweight='bold')
ax2.legend()
ax2.set_xlim([WindData.index[0],WindData.index[-1]])

ax3.plot(WindData.index,WindData['T_44m'],linestyle='--',linewidth=1,label='$44\:m$',color = colors[1])
ax3.set_ylabel('Temperature',fontweight='bold')
ax3.set_xlabel('Time',fontweight='bold')
ax3.legend()
ax3.set_xlim([WindData.index[0],WindData.index[-1]])

#%% Horizontal component wind speed 44m
WindData['Hor_ws_44m'] = np.sqrt(WindData['X_44m']**2+WindData['Y_44m']**2)

#%% Sonic wind direction
#The signs are related to the way the sonic anemometer determines the speeds
WindData['Dir_sonic'] = np.rad2deg(np.atan2(-WindData['Y_44m'],-WindData['X_44m']))
WindData.loc[WindData['Dir_sonic']<0,'Dir_sonic'] += 360
WindData['Diff_direction'] = np.abs(WindData['Dir_sonic']-WindData['Wdir_41m'])
# colors = ['#c3121e','#0348a1']
# fig, (ax1, ax2) = plt.subplots(2,1,sharex = True)
# WindData['Wdir_41m'].plot(ax = ax1,label='$41\:m$',color = colors[0])
# ax1.legend()
# WindData['Dir_sonic'].plot(ax = ax2,label='$44\:m$',color = colors[1])
# ax2.legend()

#%% Tower bottom moment conversion
# They are swapped so I need to reput them in the right order
WindData.rename(columns={"MxTB":"MzTB","MyTB":"MxTB"}, inplace=True)
WindData.rename(columns={"MzTB":"MyTB"},inplace=True) #inplace substitues the old dataset

gain_x, gain_y = 15953.4, 15953.4
offset_x, offset_y = 1230.8, -3349.4
WindData['MxTB'] = WindData['MxTB']*gain_x+offset_x
WindData['MyTB'] = WindData['MyTB']*gain_y+offset_y

#%% Let's calculate the statistics
ten_mean_speed = WindData.resample('10min').mean()
ten_std = WindData.resample('10min').std()
ten_max= WindData.resample('10min').max()
ten_min = WindData.resample('10min').min()

turb_intensity = ten_std/ten_mean_speed*100
turb_intensity = turb_intensity.filter(items = ['Wsp_18m','Wsp_44m','Wsp_70m','Hor_ws_44m'])
turb_intensity.rename(columns={'Wsp_18m':'Ti_18m','Wsp_44m':'Ti_44m','Wsp_70m':'Ti_70m',
                               'Hor_ws_44m':'Sonic_Ti_44m'},inplace = True)




