import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.colors
from multiprocessing import Process, Manager


def initialize_parameters():
    """ Initialize the parameters used in the script. """
    params = {}
    params['upper_distance_acceleration_area'] = 0  # km
    params['lower_distance_acceleration_area'] = 6998  # km
    params['dt'] = 0.1
    params['acceleration_time'] = 300
    params['observe_time'] = 400
    params['eps'] = 1e0
    return params


params = initialize_parameters()

# Check that the upper distance is smaller than the lower distance
if params['upper_distance_acceleration_area'] > params['lower_distance_acceleration_area']:
    print('Error: upper distance must be smaller than lower distance')
    exit()

# Get parameter from json
json_open = open("./src/params.json", 'r')
paramlist = json.load(json_open)

ion_name = paramlist["ion_name"]
init_v_para_eV = paramlist["init_v_para_eV"]
init_v_perp_eV = paramlist["init_v_perp_eV"]
max_v_para_for_resonance_eV = paramlist["max_v_para_for_resonance_eV"]
electric_field = paramlist["electric_field_mV/m"]
occur_duration = paramlist["occur_duration"]
occur_period = paramlist["occur_period"]
accele_t_max = paramlist["accele_t_max"]
folder_ver = paramlist["folder_ver"]
display_fig = paramlist["display_fig"]

folder_name_format = "{}_{}mVm_init_v_para_{}eV_init_v_perp_{}eV_max_resonance_{}eV_{}sec_per_{}t_max_{}sec"
folder_name = './data/' + folder_ver + '/' + folder_name_format.format(ion_name, electric_field, init_v_para_eV, init_v_perp_eV,
                                                                       max_v_para_for_resonance_eV, occur_duration, occur_period, accele_t_max)
dlists = pd.read_csv('./data/' + folder_ver + '/folderlists.csv', header=0)

# Pitch angles
pitch_angles = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
v_perps = np.float_power(10.0, list(np.arange(0.4, 3.2, 0.2)))
v_paras = np.float_power(10.0, list(np.arange(0.4, 3.2, 0.2)))

n = int(params['observe_time'] / params['dt']) + 1
x_min = params['upper_distance_acceleration_area']
x_max = params['lower_distance_acceleration_area']
relative_density_sums_ang = [[0 for _ in range(2 * n)] for _ in range(len(pitch_angles) - 1)]
relative_density_sums_perp = [[0 for _ in range(2 * n)] for _ in range(len(v_perps) - 1)]
relative_density_sums_para = [[0 for _ in range(2 * n)] for _ in range(len(v_paras) - 1)]

manager = Manager()
return_dict = manager.dict()
processes = []
return_dict['ang'] = relative_density_sums_ang
return_dict['perp'] = relative_density_sums_perp
return_dict['para'] = relative_density_sums_para


def process_data(proc_num, return_dict):
    # Read data
    name = dlists.iat[proc_num, 1]
    df = pd.read_csv(name + '/result_x.csv', header=0)
    print(name + "Plot\n")

    s_ang = [[0 for _ in range(2 * n)] for _ in range(len(pitch_angles) - 1)]
    s_perp = [[0 for _ in range(2 * n)] for _ in range(len(v_perps) - 1)]
    s_para = [[0 for _ in range(2 * n)] for _ in range(len(v_paras) - 1)]

    # Filter data by distance
    df = df[(df["x"] >= x_min) & (df["x"] <= x_max)]

    # Minimum and maximum times
    t_min = df["time"].min()
    t_max = t_min + params['acceleration_time']

    # Number of time steps
    nt_acc = int((t_max - t_min) / params['dt']) + 1

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
            s_ang[i][j] += filtered_df["relative_density"].sum()

    for i in range(len(v_perps) - 1):
        for j in range(2 * n):
            # Determine time range for current iteration
            t_min_j = max(t_min + j * params['dt'] - nt_acc * params['dt'], 0)
            t_max_j = min(t_min + (j + 1) * params['dt'], t_min + params['observe_time'])
            
            # Filter data based on time range and pitch angle range
            filtered_df = df[(t_min_j <= df["time"]) & (df["time"] < t_max_j) & (v_perps[i] <= df["v_perp_eV"]) &
                             (df["v_perp_eV"] < v_perps[i + 1])]
            
            # Sum relative density and energy density for current
            s_perp[i][j] += filtered_df["relative_density"].sum()

    for i in range(len(v_paras) - 1):
        for j in range(2 * n):
            # Determine time range for current iteration
            t_min_j = max(t_min + j * params['dt'] - nt_acc * params['dt'], 0)
            t_max_j = min(t_min + (j + 1) * params['dt'], t_min + params['observe_time'])
            
            # Filter data based on time range and pitch angle range
            filtered_df = df[(t_min_j <= df["time"]) & (df["time"] < t_max_j) & (v_paras[i] <= df["v_para_eV"]) &
                             (df["v_para_eV"] < v_paras[i + 1])]
            
            # Sum relative density and energy density for current
            s_para[i][j] += filtered_df["relative_density"].sum()
    # Sum the results from all processes
    return_dict['ang'] += np.array(s_ang)
    return_dict['perp'] += np.array(s_perp)
    return_dict['para'] += np.array(s_para)


for proc_num in range(len(dlists["foldername"])):
    p = Process(target=process_data, args=(proc_num, return_dict))
    processes.append(p)
    p.start()

# Wait for all processes to finish
for p in processes:
    p.join()

relative_density_sums_ang = return_dict['ang'].tolist()
relative_density_sums_perp = return_dict['perp'].tolist()
relative_density_sums_para = return_dict['para'].tolist()

# Create list of times for plot
t_plot = [i * params['dt'] for i in range(2 * n)]
# t_plot = [t_min + i * params['dt'] for i in range(2 * n)]

# Remove last element from pitch angles list
pitch_angles.pop(len(pitch_angles) - 1)
v_perps = np.delete(v_perps, (len(v_perps) - 1))
v_paras = np.delete(v_paras, (len(v_paras) - 1))

fig, axs = plt.subplots(3, 2, figsize=(12, 8))
axs = axs.flatten()

# relative_density_sums_angをカラープロットします
# axs[0].set_title('Graph1:ang_density')
mappable0 = axs[0].pcolormesh(t_plot, pitch_angles, relative_density_sums_ang)
axs[0].set_xlabel('time')
axs[0].set_ylabel('pitch_angle')
fig.colorbar(mappable0, ax=axs[0], orientation="vertical")
axs[0].set_label("density")

relative_density_sums_ang = np.array(relative_density_sums_ang) + params['eps']
mappable1 = axs[1].pcolormesh(t_plot, pitch_angles, relative_density_sums_ang, norm=matplotlib.colors.LogNorm())
axs[1].set_xlabel('time')
axs[1].set_ylabel('pitch_angle')
fig.colorbar(mappable1, ax=axs[1], orientation="vertical")
axs[1].set_label("density")


# relative_density_sums_perpをカラープロットします
# axs[1].set_title('Graph2:perp_density')
mappable1 = axs[2].pcolormesh(t_plot, v_perps, relative_density_sums_perp)
axs[2].set_xlabel('time')
axs[2].set_ylabel('v_perp_eV')
axs[2].set_yscale('log')
fig.colorbar(mappable1, ax=axs[2], orientation="vertical")
axs[2].set_label("density")

relative_density_sums_perp = np.array(relative_density_sums_perp) + params['eps']
mappable3 = axs[3].pcolormesh(t_plot, v_perps, relative_density_sums_perp, norm=matplotlib.colors.LogNorm())
axs[3].set_xlabel('time')
axs[3].set_ylabel('v_perp_eV')
axs[3].set_yscale('log')
fig.colorbar(mappable3, ax=axs[3], orientation="vertical")
axs[3].set_label("density")


# relative_density_sums_paraをカラープロットします
# axs[2].set_title('Graph3:para_density')
mappable4 = axs[4].pcolormesh(t_plot, v_paras, relative_density_sums_para)
axs[4].set_xlabel('time')
axs[4].set_ylabel('v_para_eV')
axs[4].set_yscale('log')
fig.colorbar(mappable4, ax=axs[4], orientation="vertical")
axs[4].set_label("density")

relative_density_sums_para = np.array(relative_density_sums_para) + params['eps']
mappable5 = axs[5].pcolormesh(t_plot, v_paras, relative_density_sums_para, norm=matplotlib.colors.LogNorm())
axs[5].set_xlabel('time')
axs[5].set_ylabel('v_para_eV')
axs[5].set_yscale('log')
fig.colorbar(mappable5, ax=axs[5], orientation="vertical")
axs[5].set_label("density")


# plt.subplots_adjust(wspace=0.5, hspace=0.4)
title = f"{ion_name}, {electric_field}mV/m, init_v_para = {init_v_para_eV}eV, init_v_perp = {init_v_perp_eV}eV, \
max_v_para_for_resonance = {max_v_para_for_resonance_eV}eV,\nWave occurs for {occur_duration}sec during {occur_period}sec, \
accleration_time_max = {accele_t_max}sec, accle_area: {x_min}-{x_max}km, accle_time = {params['acceleration_time']}s"
plt.suptitle(title)

filename = f"./data/{folder_ver}/pitch_angle_{ion_name}_{electric_field}mVm_init_v_para_{init_v_para_eV}eV_init_v_perp_{init_v_perp_eV}eV_max_\
resonance_{max_v_para_for_resonance_eV}eV_{occur_duration}sec_per_{occur_period}t_max_{accele_t_max}sec_area_{x_min}-{x_max}km_t_\
max_{params['acceleration_time']}.png"
plt.savefig(filename)
plt.show()
