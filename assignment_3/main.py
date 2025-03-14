#%% IMPORT PACKAGES

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

#%% SETTINGS FOR GRAPHS
#size
mpl.rcParams['figure.figsize'] = (16,8)

#font size of label, title, and legend
mpl.rcParams['font.size'] = 25
mpl.rcParams['xtick.labelsize'] = 40
mpl.rcParams['ytick.labelsize'] = 40
mpl.rcParams['axes.labelsize'] = 45
mpl.rcParams['axes.titlesize'] = 45
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

#%% script setting and variables
R_0 = 287.05             # [J/kgK] gas constant of dry air
R_w = 461.5              # [J/kgK] gas constant of water vapour
rho_0 = 1.225            # [kg/m^3] air density at sea level
cut_out_ws = 25          # [m/s] cut-out wind speed
A = 2124                 # [m^2] rotor area
question1 = False

#%% question1: valid free sectors
sector_free = [(0, 2.8), (228.2, 360)]

if question1:
    # Creation of polar graph for mast
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")  # Imposta il Nord (0°) in alto
    ax.set_theta_direction(-1)  # Angoli in senso orario
    for start, end in sector_free:
        theta = np.linspace(np.radians(start), np.radians(end), 100)  # Converti in radianti
        r = np.ones_like(theta)  # Imposta il raggio massimo per il riempimento
        ax.fill_between(theta, 0, r, color='red', alpha=0.5)  # Colora i settori
        if start!=0:
            ax.text(np.radians(start), 0.9, f"{start}°", fontsize=40, ha='center', va='bottom', color='black')
        if end != 360:
            ax.text(np.radians(end), 0.9, f"{end}°", fontsize=40, ha='center', va='bottom', color='black')
    ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))  
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])  
    ax.set_yticklabels([])
    
#%% IMPORT DATAS
# reading the data
WindData = pd.read_csv("2023-Jan-July-Power-data_AS03.csv",\
                       parse_dates=['date_time'],index_col='date_time')

# transforming invalid data into Nan and into numeric
WindData = WindData.replace(['\\N', ' ', ''], np.nan)
WindData = WindData.apply(pd.to_numeric, errors='coerce')

# saving important data
temp = WindData['AirAbs_70m']+273.15
pressure = WindData['Press_enc_2m']*100
rel_humidity = 0.01*WindData['RH_2m']
vapor_pressure = 0.0000205*np.exp(0.0631846*temp)

# 10-minute density
rho = 1/temp*(pressure/R_0-rel_humidity*vapor_pressure*(1/R_0-1/R_w))

fig, ax = plt.subplots(1,1)
ax.scatter(WindData['Wdir_41m'],WindData['TI_44m'],color='k',s=20)
ax.set_xlabel(r'$direction\:[^\circ]$')
ax.set_ylabel(r'$TI\:[-]$')
ax.set_ylim([0,80])
ax.grid()
ax.minorticks_on()
ax.grid()
ax.tick_params(direction='in',right=True,top =True)
ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
#%% measured power curve

# condition on pitch. Look at image of V52. I have to take these pitches into
# consideration because for higher pitches the turbine is braking, hence the 
# results are not to be considered.
condition_1 = (WindData['Pitch'] < 4) & (WindData['Wsp_44m'] >= 0) & (WindData['Wsp_44m'] <= 5)
condition_2 = (WindData['Pitch'] < 0) & (WindData['Wsp_44m'] > 5) & (WindData['Wsp_44m'] <= 10.5)
condition_3 = (WindData['Pitch'] < 6) & (WindData['Wsp_44m'] > 10.5) & (WindData['Wsp_44m'] <= 13)
condition_4 = (WindData['Pitch'] > 1) & (WindData['Pitch'] < 10) & (WindData['Wsp_44m'] > 13) & (WindData['Wsp_44m'] <= 15)
condition_5 = (WindData['Pitch'] > 1) & (WindData['Pitch'] < 22) & (WindData['Wsp_44m'] > 15) & (WindData['Wsp_44m'] <= 25)
WindData = WindData[condition_1 | condition_2 | condition_3 | condition_4 |\
                    condition_5]

# condition for direction
condition_1 = (WindData['Wdir_41m']>= 0) & (WindData['Wdir_41m']<= 2.8)
condition_2 = (WindData['Wdir_41m']>= 228.2) & (WindData['Wdir_41m']<= 360)
WindData = WindData[condition_1 | condition_2]

# normalized wind speed for active controlled wind turbine
WindData['Wsp_44m'] = WindData['Wsp_44m']*(rho/rho_0)**(1/3)

# creating bins
width = 0.5 # width of velocity bins
bins = int(cut_out_ws/0.5+1)
number_ws = np.empty(bins)
mean_wind = np.empty(bins)
mean_power = np.empty(bins)
std_power = np.empty(bins)
cp = np.empty(bins)
central_ws = np.empty(bins)
for ii in range(bins):
    central_ws[ii] = ii*width # central wind speed of bin
    if ii==0:
        start_ws = 0
    else:
        start_ws = central_ws[ii]-width/2
    if ii==bins:
        end_ws = 25
    else:
        end_ws = central_ws[ii]+width/2
        
    filtered_wind =WindData['Wsp_44m'][(WindData['Wsp_44m'] >= start_ws) & (WindData['Wsp_44m'] <= end_ws)]
    filtered_power =WindData['ActPow'][(WindData['Wsp_44m'] >= start_ws) & (WindData['Wsp_44m'] <= end_ws)]
    filtered_std_power =WindData['ActPow_stdev'][(WindData['Wsp_44m'] >= start_ws) & (WindData['Wsp_44m'] <= end_ws)]
    number_ws[ii] = len(filtered_wind)
    mean_wind[ii] = filtered_wind.mean()
    mean_power[ii] = filtered_power.mean()
    std_power[ii] = filtered_power.std()
    cp[ii] = mean_power[ii]*1e3/(0.5*rho_0*A*mean_wind[ii]**3)
    
all_data = pd.DataFrame({'Central_ws': central_ws, 'Number of points': number_ws, 'mean wind': mean_wind,\
                         'mean power': mean_power,'power stdv': std_power,'cp':cp})

# power curve
fig, ax = plt.subplots(1,1)
ax.scatter(mean_wind,mean_power,color='k',s=300, label='Mean power')
ax.errorbar(mean_wind, mean_power, yerr=std_power, fmt='o', color='k', capsize=5, label='Std Dev')
ax.set_xlabel(r'$V\:[m/s]$')
ax.set_ylabel(r'$P\:[kW]$')
ax.grid()
ax.minorticks_on()
ax.legend(loc='upper left')
ax.tick_params(direction='in',right=True,top =True)
ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)

# pitch graph after filtering
# fig, ax = plt.subplots(1,1)
# ax.scatter(WindData['Wsp_44m'],WindData['Pitch'],color='k',s=300)
# ax.set_xlabel(r'$V\:[m/s]$')
# ax.set_ylabel(r'$\theta\:[^\circ]$')
# ax.grid()
# ax.minorticks_on()
# ax.grid()
# ax.tick_params(direction='in',right=True,top =True)
# ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
# ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
# ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)

#%% uncertainty evaluation

# category A
unc_cat_a = std_power/np.sqrt(number_ws)

# category B
# I need to consider: 
#       - power measurement uncertainty
#       - wind speed uncertainty
#       - temperature measurement uncertainty
#       - pressure measurement uncertainty
#       - relative humidity uncertainty

# power uncertainty
u_p = np.sqrt((0.002*mean_power)**2+3.7**2+0.3**2)

# wind speed uncertainty
u_v = np.sqrt(0.025**2+(0.038+0.0038*mean_wind)**2+(0.01*mean_wind)**2+\
              (0.02*mean_wind)**2+(0.001*mean_wind)**2)
sens_factor_v = np.zeros(len(mean_power))
for ii in range(1,len(mean_power)):
    if ii==1:
        sens_factor_v[ii] = mean_power[ii]/(mean_wind[ii]-0.5)
    else:
        sens_factor_v[ii] =(mean_power[ii]-mean_power[ii-1])/(mean_wind[ii]-mean_wind[ii-1])

# temperature uncertainty
u_t = 0.6
sens_factor_t = sens_factor_v*mean_wind/(3*288.15)

# pressure uncertainty
u_b = 2
sens_factor_b = sens_factor_v*mean_wind/(3*1013)

# relative humidity uncertainty
u_rh = 0.63e-2
sens_factor_rh = sens_factor_v*mean_wind*0.0018

# total category B 
unc_cat_b = np.sqrt(u_p**2+u_v**2*sens_factor_v**2+u_t**2*sens_factor_t**2+\
                    u_b**2*sens_factor_b**2+u_rh**2*sens_factor_rh**2)

unc_combined = np.sqrt(unc_cat_a**2+unc_cat_b**2)

all_data['catA uncertainty'] = unc_cat_a
all_data['catB uncertainty'] = unc_cat_b
all_data['combined uncertainty'] = unc_combined

#%% annual energy production
V_ave = np.arange(4,12,1)
AEP_measured = np.zeros(len(V_ave))
AEP_extrapolated = np.zeros(len(V_ave))
validity = []
unc_aep_abs = np.zeros(len(V_ave))
unc_aep_rel = np.zeros(len(V_ave))
f_v_bef = np.zeros(len(mean_power))
f_v_now = np.zeros(len(mean_power))
for jj in range(len(V_ave)):
    for ii in range(1,len(mean_power)):
        if ii==1:
            f_v_bef[ii] = 1-np.exp(-np.pi/4*((mean_wind[ii]-0.5)/V_ave[jj])**2)
            p_i_bef = 0
        else:
            f_v_bef[ii] = 1-np.exp(-np.pi/4*(mean_wind[ii-1]/V_ave[jj])**2)
            p_i_bef = mean_power[ii-1]
        f_v_now[ii] = 1-np.exp(-np.pi/4*(mean_wind[ii]/V_ave[jj])**2)
        p_i = mean_power[ii]
        
        if np.isnan(mean_power[ii]):
            f_v_now[ii] = 1-np.exp(-np.pi/4*(central_ws[ii]/V_ave[jj])**2 )        
            if np.isnan(mean_power[ii-1]):
                f_v_bef[ii] = 1-np.exp(-np.pi/4*(central_ws[ii-1]/V_ave[jj])**2)
            else:
                highest_power = mean_power[ii-1]
            AEP_extrapolated[jj] += 8760*(f_v_now[ii]-f_v_bef[ii])*highest_power
    
        else:
            AEP_measured[jj] += 8760*(f_v_now[ii]-f_v_bef[ii])*(p_i+p_i_bef)/2
            AEP_extrapolated[jj] += 8760*(f_v_now[ii]-f_v_bef[ii])*(p_i+p_i_bef)/2
    rel_occurence = f_v_now-f_v_bef
    unc_aep_abs[jj] = 8760 * np.sqrt(np.sum(rel_occurence**2 * np.nan_to_num(unc_cat_a)**2) + 
                                 (np.sum(rel_occurence * np.nan_to_num(unc_cat_a)))**2)
    unc_aep_rel[jj] = unc_aep_abs[jj]/AEP_measured[jj]*100
    if AEP_measured[jj]>= AEP_extrapolated[jj]*0.95:
        validity.append('Complete')
    else:
        validity.append('Incomplete')
table_AEP = pd.DataFrame({'Ave_wind_speed (m/s)':V_ave,'measured_AEP (MWh)':AEP_measured/1e3,\
                          'stdv_AEP (MWh)':unc_aep_abs/1e3,'stdv_AEP_rel':unc_aep_rel,\
                          'extrapolated_AEP (MWh)':AEP_extrapolated/1e3,\
                          'validity':validity})