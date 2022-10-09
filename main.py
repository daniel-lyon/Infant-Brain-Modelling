# Import required functions
import numpy as np
import matplotlib.pyplot as plt

from math import pi
from functions import *

# Variables
omega_min = 0       # minimum x-axis power spectra
omega_max = 650     # maximum x-axis power spectra
gamma_e = 100       # Base = 100 (s^-1)
alpha = 50          # Base = 50 (s^-1)
beta = 4*alpha      # Base = 4*alpha (s^-1)
t_0 = 0.08          # Base = 0.08 (s)
G_ese = 11.3        # Base = 11.3
G_ee = 3.2          # Base = 3.2
G_ei = -7.7         # Base = -7.7 
G_esre = -5.7       # Base = -5.7 
G_srs = -0.32       # Base = -0.32 
min_age = 0         # minimum age to plot
max_age = 10        # maximum age to plot
stab_range = 2.5    # x and y axis range for stability plots

# X-axis data points
omega = [i for i in range(omega_min, omega_max+1)]
freq = [omega[i]/(2*pi) for i in omega]

# Data for the mean 18-28 age range
phi_e_final, stability_x, stability_y = equation8(alpha, gamma_e, t_0, G_ee, G_ei, G_ese, G_esre, G_srs)

# Signal Spectrum Plot
plt.plot(freq, phi_e_final)
plt.scatter(freq, phi_e_final, 5)
plt.title('Mean 18-28 Signal Spectrum')
plt.yscale('log')
plt.xscale('log')
plt.xlim(0, 10**2.1)
plt.ylabel('Power')
plt.xlabel('Frequency')
plt.savefig('Plots/Mean 18-28 Signal Spectrum', dpi = 200)
plt.show()

# Stability Plot
plt.plot([0,0], [-stab_range, stab_range], linewidth = 0.5, color = 'black')
plt.plot([-stab_range, stab_range], [0,0], linewidth = 0.5, color = 'black')
plt.plot(stability_x, stability_y, linewidth = 2)
plt.title('Stability of Mean 18-28 Signal Spectrum')
plt.ylabel('Imaginary')
plt.xlabel('Real')
plt.xlim(-stab_range, stab_range)
plt.ylim(-stab_range, stab_range)
plt.savefig('Plots/Mean 18-28 Stability Plot', dpi = 200)
plt.show() 

# List of all ages
ages = [i for i in range(min_age, max_age+1)]
ages.insert(0, -0.25)

# Colour mapping of the data
colours = plt.cm.viridis(np.linspace(min_age, 1, max_age+3))

# Lists to hold the signal and stability values for all ages
sign_outputs = []
stab_outputs = []

# Data for the given age range
for age in ages:
    
    # Variables as a function of age
    alpha = -12*age+180                 # -12*age+180 
    gamma_e = 1.4*age+43                # 1.4*age+43
    t_0 = (-4*age+104)/1000             # (-4*age+104)/1000 
    G_ee = -0.14*age+5.4                # 0.14*age+5.4 
    G_ei = 0.17*age-10.1                # 0.17*age-10.1
    G_ese = 0.01*age+10.9               # 0.01*age+10.9 
    G_esre = 0.2*age-9                  # 0.2*age-9      
    G_srs = -0.005*age-0.21             # -0.22*age+1.5
        
    sig_y, stab_x, stab_y = equation8(alpha, gamma_e, t_0, G_ee, G_ei, G_ese, G_esre, G_srs)
    sign_outputs.append(sig_y)
    stab_outputs.append([stab_x, stab_y])

# Signal Spectrum Plots for given ages and mean 18-28
for index, fig in enumerate(sign_outputs):
    plt.plot(freq, fig, color = colours[index])   
plt.plot(freq, phi_e_final, color = 'black', linewidth = 3)
plt.title(f'Signal Spectrums From Ages -0.25 to {max(ages)}')
ages.append('Mean 18-28')
plt.legend(ages)
plt.yscale('log')           # Comment out this line
plt.xscale('log')           # and this one too
# plt.xlim(3, 12)           # with these uncommented
# plt.ylim(0, 0.007)        # too to zoom in to an area of interest
plt.ylabel('Power')
plt.xlabel('Frequency')
plt.savefig('Plots/Ages Signal Spectrum', dpi = 200)
plt.show()

# Stability Plots for given age ranges and mean 18-28
plt.plot([0,0], [-stab_range, stab_range], linewidth = 0.5, color = 'black', label = '_nolegend_')
plt.plot([-stab_range, stab_range], [0,0], linewidth = 0.5, color = 'black', label = '_nolegend_')
for index, points in enumerate(stab_outputs):
    x = points[0]
    y = points[1]
    plt.plot(x, y, color = colours[index])
plt.plot(stability_x, stability_y, color = 'black', linewidth = 3)
plt.title('Stability of Signal Spectrums')
plt.legend(ages)
plt.ylabel('Imaginary')
plt.xlabel('Real')
plt.xlim(-stab_range, stab_range)
plt.ylim(-stab_range, stab_range)
plt.savefig('Plots/Ages Stability Plot', dpi = 200)
plt.show()

ages.pop(-1)        # Remove "mean 18-28" because its not a number (-1 = END)
ages.remove(-0.25)  # Remove -0.25 because its not significantly different enough from 0

# Limits to find areas betweens. Empty list to store areas
all_limits = [[3,4], [4,5], [5,6], [6,7], [7,8], [8,9], [9,10], [10,11], [11,12]]
all_areas = []

# For every age, find the area for all limits
for age in ages:

    # List of areas for the given age
    age_area = []

    # Calculate the variables for each age
    alpha = -12*age+180
    gamma_e = 1.4*age+43
    t_0 = (-4*age+104)/1000
    G_ee = -0.14*age+5.4
    G_ei = 0.17*age-10.1
    G_ese = 0.01*age+10.9
    G_esre = 0.2*age-9
    G_srs = -0.005*age-0.21

    sig_y, stab_x, stab_y = equation8(alpha, gamma_e, t_0, G_ee, G_ei, G_ese, G_esre, G_srs)

    for limit in all_limits:

        area = calc_area(y=sig_y, x=freq, xlims=limit, dx=1/(2*pi))
        age_area.append(area)

    all_areas.append(age_area)

# X-axis values to plot the bar graph on
x_values = [3, 4, 5, 6, 7, 8, 9, 10, 11]

# Create figure with a subplot for each age
fig, axs = plt.subplots(1, 11, sharey=True, tight_layout=True)
fig.suptitle("Percentage of Total Power Spectra Between Key Frequencies (3-12 Hz) For Ages 0-10")
fig.supxlabel('Frequency (Hz)')
fig.supylabel("Power Percentage (%)", x = 0.01)

# Calculate area as a percentage for each limit in each age
for index, age_area in enumerate(all_areas):
    area_sum = sum(age_area) # Calculate total area for given age
    percent_area = [] # List to store the percentage of total area in each limit

    # Calculate the area percentage for each limit
    for area in age_area:
        percent = (area/area_sum)*100
        percent_area.append(percent)
    
    # Allocate subplot to the figure with corresponding colour and age identified
    axs[index].bar(x_values, percent_area, color = colours[index])
    axs[index].set_title(f"Age {index}")

# Plot the figure and save
plt.setp(axs, xticks = [3,6,9,12])
plt.show()
fig.savefig('Plots/Percentage Plot', dpi = 200)