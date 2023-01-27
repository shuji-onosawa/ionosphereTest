import matplotlib.pyplot as plt
import pandas as pd

# Read in the data from the csv files
t_data = pd.read_csv('./data/result_t.csv')
x_data = pd.read_csv('./data/result_x.csv')

# Create figure and axes
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(12, 12))

# Plot data on ax1
ax1.plot(t_data['time'], t_data['v_perp_eV'], label='v_perp_eV')
ax1.plot(t_data['time'], t_data['v_para_eV'], label='v_para_eV')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Energy (eV)')
ax1_2 = ax1.twinx()
ax1_2.plot(t_data['time'], t_data['pitch_angle'], 'r', label='pitch_angle')
ax1_2.set_ylabel('Pitch Angle')

# Plot data on ax2 (log scale)
ax2.semilogx(t_data['time'], t_data['v_perp_eV'], label='')
ax2.semilogx(t_data['time'], t_data['v_para_eV'], label='')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Energy (eV)')
ax2_2 = ax2.twinx()
ax2_2.semilogx(t_data['time'], t_data['pitch_angle'], 'r', label='')
ax2_2.set_ylabel('Pitch Angle')

# Plot data on ax3
ax3.plot(x_data['x'], x_data['v_perp_eV'], label='')
ax3.plot(x_data['x'], x_data['v_para_eV'], label='')
ax3.set_xlabel('X (km)')
ax3.set_ylabel('Energy (eV)')
ax3_2 = ax3.twinx()
ax3_2.spines["right"].set_position(("axes", 1.15))
ax3_2.plot(x_data['x'], x_data['pitch_angle'], 'r', label='')
ax3_2.set_ylabel('Pitch Angle')
ax3_3 = ax3.twinx()
ax3_3.plot(x_data['x'], x_data['relative_density'], 'g', label='')
ax3_3.set_ylabel('relative_density')

# Plot data on ax4 (log scale)
ax4.semilogx(x_data['x'], x_data['v_perp_eV'], label='')
ax4.semilogx(x_data['x'], x_data['v_para_eV'], label='')
ax4.set_xlabel('X (km)')
ax4.set_ylabel('Energy (eV)')
ax4_2 = ax4.twinx()
ax4_2.spines["right"].set_position(("axes", 1.15))
ax4_2.semilogx(x_data['x'], x_data['pitch_angle'], 'r', label='')
ax4_2.set_ylabel('Pitch Angle')
ax4_3 = ax4.twinx()
ax4_3.semilogx(x_data['x'], x_data['relative_density'], 'g', label='relative_density')
ax4_3.set_ylabel('relative_density')

# Plot data on ax5
ax5.plot(x_data['x'], x_data['energy'], 'c', label='energy')
ax5.set_xlabel('X (km)')
ax5.set_ylabel('Energy (eV)')
ax5_2 = ax5.twinx()
ax5_2.plot(x_data['x'], x_data['energy_density'], 'm', label='energy_density')
ax5_2.set_ylabel('Energy density')

# Plot data on ax6 (log scale)
ax6.semilogx(x_data['x'], x_data['energy'], 'c', label='')
ax6.set_xlabel('X (km)')
ax6.set_ylabel('Energy (eV)')
ax6_2 = ax6.twinx()
ax6_2.semilogx(x_data['x'], x_data['energy_density'], 'm', label='')
ax6_2.set_ylabel('Energy density')

# Get parameter from c++
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
title_format = "{}, {} mV/m, init_v_para = {} eV, init_v_perp = {} eV, \nmax_v_para_for_resonance = {} eV,Wave occurs for {}\
    sec during {} sec, \naccleration_time_max {} sec"
plt.suptitle(title_format.format(ion_name, electric_field, init_v_para_eV, init_v_perp_eV, max_v_para_for_resonance_eV,
             occur_duration, occur_period, accele_t_max))
plt.subplots_adjust(wspace=0.5, hspace=0.4)

file_name_format = "./graphs/{}_{}mVm_init_v_para_{}eV_init_v_perp_{}eV_max_resonance_{}eV_{}sec_per_{}t_max_{}sec.png"
plt.savefig(file_name_format.format(ion_name, electric_field, init_v_para_eV, init_v_perp_eV, max_v_para_for_resonance_eV,
            occur_duration, occur_period, accele_t_max))

fig.legend(loc='upper left')
plt.subplots_adjust(wspace=0.5, hspace=0.4)
plt.show()
