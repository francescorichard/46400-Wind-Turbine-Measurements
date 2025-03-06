'''If you want to run successfully this code, you need to install the following
packages. Furthermore, you have to create in the same folder where this file is 
saved a folder named 'results'. This needs to have the following subfolders:
  - results
      - question1
      - question2
      - question4
      - question6
'''


#%% IMPORT PACKAGES

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
import math

#%% SETTINGS FOR GRAPHS
#size
mpl.rcParams['figure.figsize'] = (40,10)

#font size of label, title, and legend
mpl.rcParams['font.size'] = 25
mpl.rcParams['xtick.labelsize'] = 40
mpl.rcParams['ytick.labelsize'] = 40
mpl.rcParams['axes.labelsize'] = 45
mpl.rcParams['axes.titlesize'] = 55
mpl.rcParams['legend.fontsize'] = 40

#Lines and markers
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.markersize'] = 7
mpl.rcParams['scatter.marker'] = "+"
plt_marker = "d"

#Latex font
plt.rcParams['font.family'] = 'serif'  # Latex font
plt.rcParams['mathtext.fontset'] = 'cm'  # Uses Computer Modern for math

#Export
mpl.rcParams['savefig.bbox'] = "tight"

#Colors
colors = ['#e41a1c','#377eb8','#4daf4a']
#%% IMPORT DATAS
WindData = pd.read_csv("dataset_as03.csv",\
                       parse_dates=['name'],index_col='name')
    
# booleans to choose from which question I want the results
plots_question_1 = False # default to False to have a faster code
plots_question_1_cleaned = False # default to False to have a faster code
plots_question_2 = False # default to False to have a faster code
question_4 = False
question_5 = False
question_6 = False
question_7 = True
#%% question 1: plots
if plots_question_1:
    # #wind speed mean
    fig = plt.figure(1)
    plt.plot(WindData.index,WindData['Cup116m_Mean'],linestyle='--',label = '116 m')
    plt.plot(WindData.index,WindData['Cup114m_Mean'],linestyle='--',label = '114 m',)
    plt.plot(WindData.index,WindData['Cup100m_Mean'],linestyle='--',label = '100 m',alpha=0.6)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Cup anemometer mean wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_speed_cup.pdf')
    
    
    # # #wind speed max
    fig = plt.figure(2)
    plt.plot(WindData.index,WindData['Cup116m_Max'],linestyle='--',label = '116 m')
    plt.plot(WindData.index,WindData['Cup114m_Max'],linestyle='--',label = '114 m')
    plt.plot(WindData.index,WindData['Cup100m_Max'],linestyle='--',label = '100 m',alpha=0.6)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Cup anemometer max wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\max_speed_cup.pdf')
    
    # #wind speed min
    fig = plt.figure(3)
    plt.plot(WindData.index,WindData['Cup116m_Min'],linestyle='--',label = '116 m')
    plt.plot(WindData.index,WindData['Cup114m_Min'],linestyle='--',label = '114 m')
    plt.plot(WindData.index,WindData['Cup100m_Min'],linestyle='--',label = '100 m',alpha=0.6)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Cup anemometer min wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\min_speed_cup.pdf')

    #wind speed std
    fig = plt.figure(4)
    plt.plot(WindData.index,WindData['Cup116m_Stdv'],linestyle='--',label = '116 m')
    plt.plot(WindData.index,WindData['Cup114m_Stdv'],linestyle='--',label = '114 m')
    plt.plot(WindData.index,WindData['Cup100m_Stdv'],linestyle='--',label = '100 m',alpha=0.6)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Cup anemometer wind speed stdv',fontweight='bold')    
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\stdv_speed_cup.pdf')

    
    # wind direction mean
    fig = plt.figure(5)
    plt.plot(WindData.index,WindData['Vane100m_Mean'],linestyle='--',label = 'Vane',alpha=0.8)
    plt.plot(WindData.index,WindData['Sonic100m_Dir'],linestyle='--',label = 'Sonic',alpha=0.8)  
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind direction [°]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Wind vane mean wind direction',fontweight='bold') 
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_wind_direction.pdf')

    # wind direction max
    fig = plt.figure(6)
    plt.plot(WindData.index,WindData['Vane100m_Max'],linestyle='--',label = 'Vane')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind direction [°]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Wind vane max wind direction',fontweight='bold')     
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\max_wind_direction.pdf')

    # wind direction min
    fig = plt.figure(7)
    plt.plot(WindData.index,WindData['Vane100m_Min'],linestyle='--',label = 'Vane')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind direction [°]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Wind vane min wind direction',fontweight='bold')     
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\min_wind_direction.pdf')
    
    # wind direction stdv
    fig = plt.figure(8)
    plt.plot(WindData.index,WindData['Vane100m_Stdv'],linestyle='--',label = 'Vane')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind direction [°]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Wind vane wind direction stdv',fontweight='bold')     
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\stdv_wind_direction.pdf')
    
    # temperature mean
    fig = plt.figure(9)
    plt.plot(WindData.index,WindData['Temp100m_Mean'],linestyle='--',label = '100 m')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Temperature [°C]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Vane mean temperature',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_temperature.pdf')

    # temperature max
    # fig = plt.figure(10)
    plt.plot(WindData.index,WindData['Temp100m_Max'],linestyle='--',label = '100 m')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Temperature [°C]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Vane max temperature',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\max_temperature.pdf')
    
    # temperature min
    fig = plt.figure(11)
    plt.plot(WindData.index,WindData['Temp100m_Min'],linestyle='--',label = '100 m')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Temperature [°C]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Vane min temperature',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\min_temperature.pdf')
     
    # # temperature stdv
    fig = plt.figure(12)
    plt.plot(WindData.index,WindData['Temp100m_Stdv'],linestyle='--',label = '100 m')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Temperature [°C]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Vane temperature stdv',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\stdv_temperature.pdf')
    
    # #sonic anemometer mean, both scalar and vector
    fig = plt.figure(13)
    plt.plot(WindData.index,WindData['Sonic100m_Scalar_Mean'],linestyle='--',label = 'Scalar')
    plt.plot(WindData.index,WindData['Sonic100m_Vector_Mean'],linestyle='--',label = 'Vector',alpha=0.8)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Sonic anemometer mean wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_speed_sonic.pdf')

    # #sonic anemometer scalar max
    fig = plt.figure(14)
    plt.plot(WindData.index,WindData['Sonic100m_Scalar_Max'],linestyle='--',linewidth=2,label = 'Scalar Max')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Sonic anemometer max wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\max_speed_sonic.pdf')

    # #sonic anemometer scalar min
    fig = plt.figure(15)
    plt.plot(WindData.index,WindData['Sonic100m_Scalar_Min'],linestyle='--',linewidth=2,label = 'Scalar Min')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Sonic anemometer min wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\min_speed_sonic.pdf')
    
    # #sonic anemometer scalar stdv
    fig = plt.figure(16)
    plt.plot(WindData.index,WindData['Sonic100m_Scalar_Stdv'],linestyle='--',linewidth=2,label = 'Scalar Stdv')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Sonic anemometer wind speed stdv',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\stdv_speed_sonic.pdf')

#%% question 1: cleaning data

# cup anemometer and wind vane
columns_to_replace = ['Cup116m_Mean','Cup114m_Mean','Cup100m_Mean','Cup116m_Max',\
                      'Cup114m_Max','Cup100m_Max','Cup116m_Min','Cup114m_Min',\
                      'Cup100m_Min','Cup116m_Stdv','Cup114m_Stdv','Cup100m_Stdv',\
                      'Vane100m_Mean','Vane100m_Max','Vane100m_Min','Vane100m_Stdv']
WindData.loc[WindData['Cup116m_Mean']==0,columns_to_replace] = np.nan

# sonic anemometer
columns_to_replace = ['Sonic100m_Dir','Sonic100m_Scalar_Mean','Sonic100m_Scalar_Max',\
                      'Sonic100m_Scalar_Min','Sonic100m_Scalar_Stdv','Sonic100m_Vector_Mean']
WindData.loc[WindData['Sonic100m_Vector_Mean']==0,columns_to_replace] = np.nan

# temperature
WindData.loc[WindData['Temp100m_Mean']==0,'Temp100m_Mean'] = np.nan
dates_to_modify = ['2015-11-28 07:50:00', '2015-11-28 08:00:00'] # peaks to eliminate
columns_to_replace = ['Temp100m_Mean','Temp100m_Max','Temp100m_Min','Temp100m_Stdv']
WindData.loc[pd.to_datetime(dates_to_modify), columns_to_replace] = np.nan

# change the values of the lidar from type object to numbers
columns_to_replace = ['Spd','Spd_stdv','Spd_min','Spd_max','Dir','Dir_stdv',\
                      'W','W_stdv','Available','CNR','Broad']
for col in columns_to_replace:
    WindData[col] = pd.to_numeric(WindData[col], errors='coerce')

# let's do some examples of cleaned data. Choose one plot for cup and vane, one for
# sonic, and one for temperature
if plots_question_1_cleaned:
    #mean wind speed
    fig = plt.figure(1)
    plt.plot(WindData.index,WindData['Cup116m_Mean'],linestyle='--',label = '116 m')
    plt.plot(WindData.index,WindData['Cup114m_Mean'],linestyle='--',label = '114 m',)
    plt.plot(WindData.index,WindData['Cup100m_Mean'],linestyle='--',label = '100 m',alpha=0.6)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Cup anemometer mean wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_speed_cup_cleaned.pdf')
    
    # mean temperature
    fig = plt.figure(2)
    plt.plot(WindData.index,WindData['Temp100m_Mean'],linestyle='--',label = '100 m')
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Temperature [°C]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Vane mean temperature',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_temperature_cleaned.pdf')
    
    # #sonic anemometer mean, both scalar and vector
    fig = plt.figure(3)
    plt.plot(WindData.index,WindData['Sonic100m_Scalar_Mean'],linestyle='--',label = 'Scalar')
    plt.plot(WindData.index,WindData['Sonic100m_Vector_Mean'],linestyle='--',label = 'Vector',alpha=0.8)
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Sonic anemometer mean wind speed',fontweight='bold')
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_speed_sonic_cleaned.pdf')
    
    # wind direction mean
    fig = plt.figure(4)
    plt.plot(WindData.index,WindData['Vane100m_Mean'],linestyle='--',label = 'Vane',alpha=0.8)
    plt.plot(WindData.index,WindData['Sonic100m_Dir'],linestyle='--',label = 'Sonic',alpha=0.8)  
    plt.xlabel('Time',fontweight='bold')
    plt.ylabel('Wind direction [°]',fontweight='bold')
    plt.legend(loc='upper left')
    plt.title('Wind vane mean wind direction',fontweight='bold') 
    plt.xlim([WindData.index[0],WindData.index[-1]])
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question1\mean_wind_direction_cleaned.pdf')
#%% question 2: ratio of the cup anemometer and sonic wind speeds at 100m
# To clean the plot, let's just take the wind speeds higher than 4 m/s. This 
# is also needed because otherwhise the wind vane won't be very accurate.
condition_velocity = (WindData['Cup100m_Mean']>4)
filtered_data = WindData[condition_velocity]

if plots_question_2:
    fig,axs = plt.subplots(1,1,sharex=True)
    axs.scatter(filtered_data['Vane100m_Mean'],filtered_data['Cup100m_Mean']/filtered_data['Sonic100m_Scalar_Mean'],\
             color =colors[0])
    axs.set_ylabel(r'$V_{cup}/V_{Sonic}$',fontweight='bold')
    axs.set_xlabel(r'Wind direction [°]')
    axs.set_title(r'$V_{cup}/V_{sonic}\:as\:a\:function\:of\:wind\:direction$',fontweight='bold')
    axs.set_xlim([filtered_data['Vane100m_Mean'].min(),filtered_data['Vane100m_Mean'].max()])
    axs.minorticks_on()
    axs.tick_params(direction='in',right=False,top =True)
    axs.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    axs.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    axs.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question2\ratio_wind_speeds.pdf')
#%% question 3
# there are some turbines north of the mast (200 m), while there is another 
# mast at 300 m (307°). Hence, we can take as a free directional range, the range
# between 45° (N-E) and 270° (W). Later we will calculate the regression with
# a smaller directional range.

#%% question 4

# let's impose some conditions. The direction is taken between the chosen range,
# the velocity needs to be between 4 m/s and 16 m/s, in order to compare the
# results with the cup, and the temperature should be higher than 2°C to avoid
# ice formation on the cup. Furthermore, a condition on the lidar's availability is taken
# into account
condition_direction = (WindData['Vane100m_Mean']>45) & (WindData['Vane100m_Mean']<270)
condition_velocity = (WindData['Cup100m_Mean']>4) & (WindData['Cup100m_Mean']<16)
condition_temperature = WindData['Temp100m_Mean']>2
num=0
for ii in range(len(condition_temperature)):
    if condition_temperature[ii] == False and WindData['Temp100m_Mean'][ii] is not None \
        and not math.isnan(WindData['Temp100m_Mean'][ii]):
        num += 1
condition_availability1 = WindData['Available']== 100
condition_availability2 = (WindData['Available'] > 0) & (WindData['Available'] < 50) 
if question_4:
    graphs = [0,1,2]
    for graph in graphs:
        if graph == 0:
            # just using direction constraints
            filtered_data = WindData[condition_direction]
            title = 'Linear regression with direction constraint: 45°-270°'
            filename = r'.\results\question4\regression_direction_constraint.pdf'
        elif graph == 1:
            filtered_data = WindData[condition_direction & condition_availability1] 
            title = 'Linear regression with direction constraint: 45°-270° and maximum\n'\
                + 'lidar availabililty'
            filename = r'.\results\question4\regression_max_lidar_availability.pdf'
        else:
            filtered_data = WindData[condition_direction & condition_availability2] 
            title = 'Linear regression with direction constraint: 45°-270° and low\n '\
                + 'lidar availabililty'
            filename = r'.\results\question4\regression_low_lidar_availability.pdf'
        filtered_data = filtered_data[['Cup100m_Mean', 'Spd']].dropna() #eliminate Nan values
        windcube_speed = filtered_data['Spd'] # lidar wind speed
        cup_speed = filtered_data['Cup100m_Mean'] # cup wind speed
        X = cup_speed.values.reshape(-1, 1)  # Independent variable
        y = windcube_speed.values  # Dependent variable
        model = LinearRegression()
        model.fit(X, y)
        gain = model.coef_[0]  # slope
        offset = model.intercept_  # intercept
        r_squared = model.score(X, y)  # R²
        model_results = X*gain+offset
        
        fig = plt.figure(figsize=(20, 20))
        plt.scatter(X.flatten(), y, label='Data',alpha=0.6)
        plt.plot(X, model_results, color='red', label=f'Fit: y={gain:.3f}x+{offset:.3f}, $R^2$={r_squared:.4f}')
        plt.xlabel('Cup Anemometer Speed [m/s]',fontweight='bold')
        plt.ylabel('Windcube Speed [m/s]',fontweight='bold')
        plt.legend(loc='upper left',frameon=False)
        plt.title(title,fontweight='bold')
        plt.minorticks_on()
        plt.tick_params(direction='in',right=False,top =True)
        plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
        plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
        plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
        plt.savefig(filename)

#%% question 5
if question_5:
    # number of points with temperature below 2 degrees
    temp_below_2 = len(WindData['Temp100m_Mean'].dropna())-(WindData['Temp100m_Mean']>2).sum()

#%% question 6

if question_6:   
    #considering all filters
    filtered_data = WindData[condition_direction & condition_velocity & condition_temperature]
    filtered_data = filtered_data[['Cup100m_Mean', 'Spd']].dropna()
    windcube_speed = filtered_data['Spd']
    cup_speed = filtered_data['Cup100m_Mean']
    X = cup_speed.values.reshape(-1, 1)  # Independent variable
    y = windcube_speed.values  # Dependent variable
    model = LinearRegression()
    model.fit(X, y)
    gain = model.coef_[0]  # slope
    offset = model.intercept_  # intercept
    r_squared = model.score(X, y)  # R²
    model_results = X*gain+offset
    
    #regression without offset
    model_forced = LinearRegression(fit_intercept=False)
    model_forced.fit(X, y)
    gain_forced = model_forced.coef_[0]  # slope
    r_squared_forced= model_forced.score(X, y)  # R²
    model_forced_results = X*gain_forced
    
    fig = plt.figure(figsize=(20, 20))
    plt.scatter(X.flatten(), y, label='Data',alpha=0.6)
    plt.plot(X, model_results, color='red', label=f'Fit: y={gain:.3f}x+{offset:.3f}, $R^2$={r_squared:.4f}')
    plt.plot(X, model_forced_results, color='k', label=f'Fit: y={gain_forced:.3f}x, $R^2$={r_squared_forced:.4f}',alpha=0.7)
    plt.xlabel('Cup Anemometer Speed [m/s]',fontweight='bold')
    plt.ylabel('Windcube Speed [m/s]',fontweight='bold')
    plt.legend(loc='upper left',frameon=False)
    plt.title('Velocity, temperature and direction filters applied',fontweight='bold')
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question6\regression_all_filters.pdf')
    
    
    filtered_data_dir = WindData[condition_velocity & condition_temperature]
    filtered_data_dir = filtered_data_dir[['Dir', 'Vane100m_Mean']].dropna()
    windcube_direction = filtered_data_dir['Dir']
    cup_direction = filtered_data_dir['Vane100m_Mean']
    X_dir = cup_direction.values.reshape(-1, 1)  # Independent variable
    y_dir = windcube_direction.values  # Dependent variable
    # regression with offset
    model_dir = LinearRegression()
    model_dir.fit(X_dir, y_dir)
    gain_dir = model_dir.coef_[0]  # slope
    offset_dir = model_dir.intercept_  # intercept
    r_squared_dir = model_dir.score(X_dir, y_dir)  # R²
    model_results_dir = X_dir*gain_dir+offset_dir
    
     # regression without offset
    model_forced_dir = LinearRegression(fit_intercept=False)
    model_forced_dir.fit(X_dir, y_dir)
    gain_forced_dir = model_forced_dir.coef_[0]  # slope
    r_squared_forced_dir= model_forced_dir.score(X_dir, y_dir)  # R²
    model_forced_results_dir = X_dir*gain_forced_dir
    title = 'Direction regression'
    
    fig = plt.figure(figsize=(20, 20))
    plt.scatter(X_dir.flatten(), y_dir, label='Data',alpha=0.6)
    plt.plot(X_dir, model_results_dir, color='red', label=f'Fit: y={gain_dir:.3f}x{offset_dir:.3f}, $R^2$={r_squared_dir:.4f}')
    plt.plot(X_dir, model_forced_results_dir, color='k', label=f'Fit: y={gain_forced_dir:.3f}x, $R^2$={r_squared_forced_dir:.4f}',alpha=0.7)
    plt.xlabel('Wind vane Direction [°]',fontweight='bold')
    plt.ylabel('Windcube Direction [°]',fontweight='bold')
    plt.legend(loc='upper center',frameon=False)
    plt.title('Lidar wind direction versus wind vane wind direction',fontweight='bold')
    plt.minorticks_on()
    plt.tick_params(direction='in',right=False,top =True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    plt.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=False)
    plt.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=False,left=True)
    plt.savefig(r'.\results\question6\regression_direction.pdf')

#%% question  7
if question_7:
    wind_speeds = [4, 8, 12] #wind speeds
    rel_uncertainty = []
    abs_uncertainty = []
    u_cal1 = 0.06/2 # k=1 1^st calibration uncertainty
    k_c = 0.8 #class A
    for ii,V in enumerate(wind_speeds):
        u_mount = 0.01*V # boom-mounted cup uncertainty (slide 18 wind speed uncertainties cup)
        u_cal2 =  0.01/np.sqrt(3)*V # k=1 #2^nd calibration uncertainty
        u_ope = k_c/(100*np.sqrt(3))*(0.5*V+5) #operational uncertainty
        u_cal = np.sqrt(u_cal1**2+u_cal2**2)
        u_tot = np.sqrt(u_cal**2+u_ope**2+u_mount**2)
        abs_uncertainty.append(u_tot)
        rel_uncertainty.append(u_tot/V*100) #percentage