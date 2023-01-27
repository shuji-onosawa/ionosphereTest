import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors


def initialize_parameters():
    """ Initialize the parameters used in the script. """
    params = {}
    params['want_log'] = False
    params['upper_distance_acceleration_area'] = 500  # km
    params['lower_distance_acceleration_area'] = 700  # km
    params['dt'] = 0.1
    params['acceleration_time'] = 20
    params['observe_time'] = 40
    return params


params = initialize_parameters()

# Check that the upper distance is smaller than the lower distance
if params['upper_distance_acceleration_area'] > params['lower_distance_acceleration_area']:
    print('Error: upper distance must be smaller than lower distance')
    exit()

# Get parameters from C++
with open("./data/params.txt") as f:
    paramlist = [s.strip() for s in f.readlines()]

ion_name = paramlist[0]
init_v_para_eV = paramlist[1]
init_v_perp_eV = paramlist[2]
max_v_para_for_resonance_eV = paramlist[3]
electric_field = paramlist[4]
occur_duration = paramlist[5]
occur_period = paramlist[6]
accele_t_max = paramlist[7]

# Read data
df = pd.read_csv('./data/result_x.csv', header=0)

# Filter data by distance
x_min = params['upper_distance_acceleration_area']
x_max = params['lower_distance_acceleration_area']
df = df[(df["x"] >= x_min) & (df["x"] <= x_max)]

# Pitch angles
pitch_angles = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

# Minimum and maximum times
t_min = df["time"].min()
t_max = t_min + params['acceleration_time']

# Number of time steps
n = int(params['observe_time'] / params['dt']) + 1
nt_acc = int((t_max - t_min) / params['dt']) + 1

# Initialize lists to store relative density and energy density sums
relative_density_sums = [[0 for _ in range(2 * n)] for _ in range(len(pitch_angles) - 1)]
energy_density_sums = [[0 for _ in range(2 * n)] for _ in range(len(pitch_angles) - 1)]

# Iterate over pitch angles and time steps
for i in range(len(pitch_angles) - 1):
    for j in range(2 * n):
        # Determine time range for current iteration
        t_min_j = max(t_min + j * params['dt'] - nt_acc * params['dt'], 0)
        t_max_j = min(t_min + (j + 1) * params['dt'], t_min + params['observe_time'])
        
        # Filter data based on time range and pitch angle range
        filtered_df = df[(t_min_j <= df["time"]) & (df["time"] < t_max_j) & (pitch_angles[i] <= df["pitch_angle"]) &
                         (df["pitch_angle"] < pitch_angles[i + 1])]
        
        # Sum relative density and energy density for current iteration
        energy_density_sums[i][j] = filtered_df["energy_density"].sum()
        relative_density_sums[i][j] = filtered_df["relative_density"].sum()

# Create list of times for plot
t_plot = [t_min + i * params['dt'] for i in range(2 * n)]

# Remove last element from pitch angles list
pitch_angles.pop(len(pitch_angles) - 1)

fig, axs = plt.subplots(2, 2 if params['want_log'] else 1, figsize=(12, 8))
axs = axs.flatten()

# energy_density_sumsをカラープロットします
axs[0].set_title('Graph1:erg_density')
mappable1 = axs[0].pcolormesh(t_plot, pitch_angles, energy_density_sums)
axs[0].set_xlabel('t')
axs[0].set_ylabel('pitch_angle')
fig.colorbar(mappable1, ax=axs[0], orientation="vertical")
axs[0].set_label("erg_density")

# relative_density_sumsをカラープロットします
axs[1].set_title('Graph2:relative_density')
mappable2 = axs[1].pcolormesh(t_plot, pitch_angles, relative_density_sums)
axs[1].set_xlabel('time')
axs[1].set_ylabel('pitch_angle')
fig.colorbar(mappable2, ax=axs[1], orientation="vertical")
axs[1].set_label("density")

if params['want_log']:
    # energy_density_sumsをlogでカラープロットします
    axs[2].set_title('Graph3:erg_density(log)')
    energy_density_sums_nonzero = np.array(energy_density_sums) + 1e-10
    mappable3 = axs[2].pcolormesh(t_plot, pitch_angles, energy_density_sums_nonzero, norm=matplotlib.colors.LogNorm())
    axs[2].set_xlabel('t')
    axs[2].set_ylabel('pitch_angle')
    fig.colorbar(mappable3, ax=axs[2], orientation="vertical", norm=matplotlib.colors.LogNorm())
    axs[2].set_label("erg_density(log)")

    # relative_density_sumsをlogでカラープロットします
    axs[3].set_title('Graph4:relative_density(log)')
    relative_density_sums_nonzero = np.array(relative_density_sums) + 1e-10
    mappable4 = axs[3].pcolormesh(t_plot, pitch_angles, relative_density_sums_nonzero, norm=matplotlib.colors.LogNorm())
    axs[3].set_xlabel('time')
    axs[3].set_ylabel('pitch_angle')
    fig.colorbar(mappable4, ax=axs[3], orientation="vertical", norm=matplotlib.colors.LogNorm())
    axs[3].set_label("density(log)")

# plt.subplots_adjust(wspace=0.5, hspace=0.4)
title = f"{ion_name}, {electric_field}mV/m, init_v_para = {init_v_para_eV}eV, init_v_perp = {init_v_perp_eV}eV, \
max_v_para_for_resonance = {max_v_para_for_resonance_eV}eV,\nWave occurs for {occur_duration}sec during {occur_period}sec, \
accleration_time_max = {accele_t_max}sec, accle_area: {x_min}-{x_max}km, accle_time = {params['acceleration_time']}s"
plt.suptitle(title)

filename = f"./graphs/pitch_angle_{ion_name}_{electric_field}mVm_init_v_para_{init_v_para_eV}eV_init_v_perp_{init_v_perp_eV}eV_max_\
resonance_{max_v_para_for_resonance_eV}eV_{occur_duration}sec_per_{occur_period}t_max_{accele_t_max}sec_area_{x_min}-{x_max}km_t_\
max_{params['acceleration_time']}.png"
plt.savefig(filename)
plt.show()
