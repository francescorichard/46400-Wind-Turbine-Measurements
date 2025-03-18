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
mpl.rcParams['scatter.marker'] = "d"
plt_marker = "d"

#Latex font
plt.rcParams['font.family'] = 'serif'  # Latex font
plt.rcParams['mathtext.fontset'] = 'cm'  # Uses Computer Modern for math

#Export
mpl.rcParams['savefig.bbox'] = "tight"

#Colors
colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3']
temp_colors = ['#377eb8','#e41a1c','#4daf4a','#252525']

#%% script setting and variables
R_0 = 287.05             # [J/kgK] gas constant of dry air
R_w = 461.5              # [J/kgK] gas constant of water vapour
cut_out_ws = 25          # [m/s] cut-out wind speed
A = 2124                 # [m^2] rotor area
question1 = True

#%% question1: valid free sectors

# preliminary free sectors
preliminary_free_sector_mast = [(0, 70.5), (172.3, 360)]
preliminary_free_sector_turb = [(0, 161.8), (228.2, 360)]

# combined free sector, together with mast and turbine's free sectors
sector_free = [(0, 2.8), (228.2, 360)]
sector_mast = [(0, 54.7), (188.8, 360)]
sector_turbine = [(0, 2.8), (112.0, 161.8), (228.2, 360)]

if question1:
    # Creation of polar graph for mast
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")  # Put 0° to the north
    ax.set_theta_direction(-1)  # Clockwise direction of the angles
    
    # function to fill the plots
    def fill_sector(ax, sectors, color, label):
        for i, (start, end) in enumerate(sectors):
            theta = np.linspace(np.radians(start), np.radians(end), 100)
            r = np.ones_like(theta)  
            ax.fill_between(theta, 0, r, color=color, alpha=0.3, label=label if i == 0 else "")
            if start!=0:
                ax.plot([np.radians(start), np.radians(start)], [0, 1], color=color, linewidth=3)  # Bordo sinistro
            if end !=360:
                ax.plot([np.radians(end), np.radians(end)], [0, 1], color=color, linewidth=3)  # Bordo destro


    fill_sector(ax, sector_mast, 'red', 'Mast Sector')
    fill_sector(ax, sector_turbine, 'blue', 'Turbine Sector')
    
    # Graph settings
    ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))  
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],fontsize= 25)  
    ax.set_yticklabels([])
    
    # Legend and saving the file
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    fig.savefig(r'.\results\question1\final_free_sectors.pdf')        
    
#%% IMPORT DATAS

# reading the data
WindData = pd.read_csv(r".\data\2023-Jan-July-Power-data_AS03.csv",\
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
WindData['rho'] = 1/temp*(pressure/R_0-rel_humidity*vapor_pressure*(1/R_0-1/R_w))


#%% data rejection

# pitch graph before filtering
fig, ax = plt.subplots(1,1)
ax.scatter(WindData['Wsp_44m'],WindData['Pitch'],color='k',s=50)
ax.set_xlabel(r'$V\:[m/s]$')
ax.set_ylabel(r'$\theta\:[^\circ]$')
ax.grid()
ax.minorticks_on()
ax.grid()
ax.tick_params(direction='in',right=True,top =True)
ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
fig.savefig(r'.\results\question2\pitch_before_filtering.pdf')

# condition on rotational speed. The range is 14-31.4 rpm
condition_1 = (WindData['ROT'] <= 31.4)
condition_2 = (WindData['ROT'] >= 14)
WindData = WindData[condition_1 & condition_2]

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

# pitch graph after filtering
fig, ax = plt.subplots(1,1)
ax.scatter(WindData['Wsp_44m'],WindData['Pitch'],color='k',s=50)
ax.set_xlabel(r'$V\:[m/s]$')
ax.set_ylabel(r'$\theta\:[^\circ]$')
ax.grid()
ax.minorticks_on()
ax.grid()
ax.tick_params(direction='in',right=True,top =True)
ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
fig.savefig(r'.\results\question2\pitch_after_filtering.pdf')

#%% normalization of wind speed
rho_0 = WindData['rho'].mean()
# normalized wind speed for active controlled wind turbine
WindData['Wsp_44m'] = WindData['Wsp_44m']*(WindData['rho']/rho_0)**(1/3)
# mean density after filtering
print(f"The mean density after filtering is {WindData['rho'].mean():.4} kg/m^3")

#%% power curve

# scatter plot power
fig, ax = plt.subplots(1,1)
ax.scatter(WindData['Wsp_44m'],WindData['ActPow'],color=temp_colors[3],s=100, label='Mean')
ax.scatter(WindData['Wsp_44m'],WindData['ActPow_min'],color=temp_colors[0],s=100, label='Minimum')
ax.scatter(WindData['Wsp_44m'],WindData['ActPow_max'],color=temp_colors[1],s=100, label='Maximum')
ax.scatter(WindData['Wsp_44m'],WindData['ActPow_stdev'],color=temp_colors[2],s=100, label='Stdev')
ax.set_xlabel(r'$V\:[m/s]$')
ax.set_ylabel(r'$P\:[kW]$')
ax.grid()
ax.minorticks_on()
ax.legend(loc='upper left',fontsize=25)
ax.tick_params(direction='in',right=True,top =True)
ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
fig.savefig(r'.\results\question2\scatter_plot_power.pdf')

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


#%% power curve uncertainty evaluation

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

# power curve
fig, ax = plt.subplots(1,1)
ax.plot(mean_wind,mean_power,color='k', label='Mean power')
ax.errorbar(mean_wind, mean_power, yerr=unc_combined, fmt='o', color='k', capsize=5, label='Std Dev')
ax.set_xlabel(r'$V\:[m/s]$')
ax.set_ylabel(r'$P\:[kW]$')
ax.grid()
ax.minorticks_on()
ax.tick_params(direction='in',right=True,top =True)
ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
fig.savefig(r'.\results\question2\power_curve.pdf')

# power coefficient
fig, ax = plt.subplots(1,1)
ax.plot(mean_wind,cp,color='k',marker='d',markersize=10)
ax.set_xlabel(r'$V\:[m/s]$')
ax.set_ylabel(r'$C_p\:[kW]$')
ax.set_ylim([-2.2,1])
ax.grid()
ax.minorticks_on()
ax.tick_params(direction='in',right=True,top =True)
ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
ax.tick_params(direction='in',which='minor',length=5,bottom=True,top=True,left=True,right=True)
ax.tick_params(direction='in',which='major',length=10,bottom=True,top=True,right=True,left=True)
fig.savefig(r'.\results\question2\power_coefficient.pdf')

#%% annual energy production and AEP uncertainties

# understanding which is the first good bin with at least 3 n° of points
for ii in range(len(all_data['Number of points'])): 
    if all_data['Number of points'][ii]>3:
        initial_bin = ii
        break

# initialization arrays
V_ave = np.arange(4,12,1) # Rayleigh average speed
AEP_measured = np.zeros(len(V_ave)) # measured AEP
AEP_extrapolated = np.zeros(len(V_ave)) # extrapolated AEP
validity = [] # validity of extrapolated AEP in respect to measured AEP
unc_aep_abs = np.zeros(len(V_ave)) # absolute value AEP uncertainties
unc_aep_rel = np.zeros(len(V_ave)) # relative value AEP uncertainties
f_v_bef = np.zeros(len(mean_power)) # cdf of velocity before the one considered
f_v_now = np.zeros(len(mean_power)) # cdf of velocity considered

# AEP for different average velocities
for jj in range(len(V_ave)):
    # calculating AEP with all the wind speed bins
    for ii in range(initial_bin,len(mean_power)):
        # if it's first bin, I have to set the wind speed in the previous bin to
        # 0.5 and power to 0
        if ii==initial_bin:
            f_v_bef[ii] = 1-np.exp(-np.pi/4*((mean_wind[ii]-0.5)/V_ave[jj])**2)
            p_i_bef = 0
        else:
            f_v_bef[ii] = 1-np.exp(-np.pi/4*(mean_wind[ii-1]/V_ave[jj])**2)
            p_i_bef = mean_power[ii-1]
        f_v_now[ii] = 1-np.exp(-np.pi/4*(mean_wind[ii]/V_ave[jj])**2)
        p_i = mean_power[ii]
        
        # if the power is NaN, then I start to update just the extrapolated AEP
        if np.isnan(mean_power[ii]):
            f_v_now[ii] = 1-np.exp(-np.pi/4*(central_ws[ii]/V_ave[jj])**2 )        
            if np.isnan(mean_power[ii-1]):
                f_v_bef[ii] = 1-np.exp(-np.pi/4*(central_ws[ii-1]/V_ave[jj])**2)
            else:
                highest_power = mean_power[ii-1]
            AEP_extrapolated[jj] += 8760*(f_v_now[ii]-f_v_bef[ii])*highest_power
        # otherwise I update both AEP, which are the same until power is NaN
        else:
            AEP_measured[jj] += 8760*(f_v_now[ii]-f_v_bef[ii])*(p_i+p_i_bef)/2
            AEP_extrapolated[jj] += 8760*(f_v_now[ii]-f_v_bef[ii])*(p_i+p_i_bef)/2
    
    # relative occurence for AEP uncertainty
    rel_occurence = f_v_now-f_v_bef
    # absolute AEP uncertainty
    unc_aep_abs[jj] = 8760 * np.sqrt(np.sum(rel_occurence**2 * np.nan_to_num(unc_cat_a)**2) + 
                                 (np.sum(rel_occurence * np.nan_to_num(unc_cat_b)))**2)
    # relative AEP uncertainty
    unc_aep_rel[jj] = unc_aep_abs[jj]/AEP_measured[jj]*100
    
    # check validity of extrapolated AEP 
    if AEP_measured[jj]>= AEP_extrapolated[jj]*0.95:
        validity.append('Complete')
    else:
        validity.append('Incomplete')

# saving the results in a table
table_AEP = pd.DataFrame({'Ave_wind_speed (m/s)':V_ave,'measured_AEP (MWh)':AEP_measured/1e3,\
                          'stdv_AEP (MWh)':unc_aep_abs/1e3,'stdv_AEP_rel':unc_aep_rel,\
                          'extrapolated_AEP (MWh)':AEP_extrapolated/1e3,\
                          'validity':validity})