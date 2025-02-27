
#%% IMPORT PACKAGES
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sqlalchemy import create_engine,text
#%% SETTINGS FOR GRAPHS
mpl.rcParams['figure.figsize']  = (16,8)
mpl.rcParams['font.size'] = 18
mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18
mpl.rcParams['axes.labelsize'] = 18
mpl.rcParams['axes.titlesize'] = 18
mpl.rcParams['legend.fontsize'] = 18

#%% IMPORT DATAS
WindData = pd.read_csv("C:\COPENAGHEN PRIMO ANNO\WIND_TURBINE_MEASUREMENTS\exercises\exercise 3_big_dataset\dataset.csv",parse_dates=['date_time'],index_col='date_time',
                       sep=';')

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
ten_minute_means = WindData.resample('10min').mean()
ten_minute_means.reset_index().set_index('date_time')
ten_minute_std = WindData.resample('10min').std()
ten_minute_std.reset_index().set_index('date_time')
ten_minute_max= WindData.resample('10min').max()
ten_minute_max.reset_index().set_index('date_time')
ten_minute_min = WindData.resample('10min').min()
ten_minute_min.reset_index().set_index('date_time')


ten_minute_ti = ten_minute_std/ten_minute_means*100
ten_minute_ti = ten_minute_ti.filter(items = ['Wsp_18m','Wsp_44m','Wsp_70m','Hor_ws_44m'])
ten_minute_ti.rename(columns={'Wsp_18m':'Ti_18m','Wsp_44m':'Ti_44m','Wsp_70m':'Ti_70m',
                               'Hor_ws_44m':'Sonic_Ti_44m'},inplace = True)
ten_minute_ti.reset_index().set_index('date_time')
mean_ws_18 = WindData['Wsp_18m'].mean()
mean_ws_44 = WindData['Wsp_44m'].mean()
mean_ws_70 = WindData['Wsp_70m'].mean()
#%% PLOT DATA

def plotting_1data(xdata,ydata,column_name,num_plots,ylabel):
    colors = ['#003f5c','#bc5090','#ffa600']
    fig = plt.figure()
    plt.plot(xdata,ydata,linestyle='--',linewidth=2,label=column_name,color = colors[0],alpha = 0.6)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel(ylabel,fontweight='bold')
    plt.legend()
    plt.xlim([xdata[0],xdata[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=True,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
    return fig

def plotting_multipledata(xdata,ydata,column_name,num_plots,y_label):
    colors = ['#003f5c','#bc5090','#ffa600']
    fig = plt.figure()
    for ii in range(0,num_plots):
        plt.plot(xdata,ydata[ii],linestyle='--',linewidth=2,label=column_name[ii],color = colors[ii],alpha = 0.6)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel(y_label,fontweight='bold')
    plt.legend()
    plt.xlim([xdata[0],xdata[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=True,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
    return fig

# #fig1 = plotting_multipledata(WindData.index, [np.array(WindData['Wsp_18m']),np.array(WindData['Wsp_44m']),
#                                      np.array(WindData['Wsp_70m'])],['Wdir_41m','Wsp_44m',
#                                                             'Wsp_70m'], 
#                                                              3, 'Wind Speed')
# #fig1.savefig("wind_speeds"+".pdf", format="pdf")
fig2 = plotting_multipledata(WindData.index, [np.array(WindData['Wdir_41m']),np.array(WindData['Dir_sonic']),
                                                            np.array(WindData['yaw'])],
                                                            ['Wdir_41m','Dir_sonic','yaw'], 
                                                             3, 'Wind direction')
fig2.savefig("wind_direction"+".pdf", format="pdf")
# #fig3 = plotting_multipledata(WindData.index, [np.array(WindData['X_44m']),np.array(WindData['Y_44m']),
#                                       np.array(WindData['Z_44m'])],['X_44m','Y_44m',
#                                                             'Z_44m'], 
#                                                              3, 'Sonic Wind Speed')
# #fig3.savefig("anemometer_velocity_components"+".pdf", format="pdf")
# #fig4 = plotting_multipledata(WindData.index, [np.array(WindData['T_44m']),np.array(WindData['AirAbs_18m']),
#                                       np.array(WindData['AirAbs_70m'])],['T_44m','AirAbs_18m',
#                                                             'AirAbs_70m'], 3, 'Temperature')
# #fig4.savefig("temperature"+".pdf", format="pdf")                                                           
# #fig5 = plotting_multipledata(WindData.index, [np.array(WindData['MyTB']),np.array(WindData['MxTB'])],
#                                                             ['MyTB','MxTB'], 
#                                                              2, 'Temperature')
# #fig5.savefig("root_moments"+".pdf", format="pdf")
#%% QUESTIONS

# 1
mean_horizontal_speed = np.sqrt(ten_minute_means['X_44m']**2+ten_minute_means['Y_44m']**2)
absolute_diff_speed = np.abs(mean_horizontal_speed-ten_minute_means['Hor_ws_44m'])
fig = plt.figure(6)
plt.plot(ten_minute_means.index,ten_minute_means['Hor_ws_44m'],linestyle='--',linewidth=2,label = 'Hor_ws before the mean')
plt.plot(ten_minute_means.index,mean_horizontal_speed,linestyle='--',linewidth=2,label = 'Hor_ws after the mean')
plt.xlabel('Time',fontweight='bold')
plt.ylabel('Wind speed',fontweight='bold')
plt.legend()

#%% connecting to SQL 
# Change user and password from DTU Learn
# connection_string = "mysql+pymysql://GroupXX:xxxxxx@data02.windenergy.dtu.dk:3306/group6"
# engine = create_engine(connection_string, echo=True)

# #exporting data to SQL
# ten_minute_means.to_sql('10_minute_means',engine,index=True,chunksize=144,if_exists='append')
# ten_minute_std.to_sql('10_minute_std',engine,index=True,chunksize=144,if_exists='append')
# ten_minute_max.to_sql('10_minute_max',engine,index=True,chunksize=144,if_exists='append')
# ten_minute_min.to_sql('10_minute_min',engine,index=True,chunksize=144,if_exists='append')
# ten_minute_ti.to_sql('10_minute_ti',engine,index=True,chunksize=144,if_exists='append')

