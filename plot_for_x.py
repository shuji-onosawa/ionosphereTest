import pandas as pd
import matplotlib.pyplot as plt

dft = pd.read_csv('result_t.csv')
dfx = pd.read_csv('result_x.csv')

fig, ((ax1, ax5), (ax2, ax6)) = plt.subplots(2, 2, figsize=(12, 8))

ax1.plot(dft['time'], dft['v_perp_eV'], 'b-', label='v_perp_eV')
ax1.plot(dft['time'], dft['v_para_eV'], 'r-', label='v_para_eV')
ax1.set_xlabel('time(s)')
ax2.set_yscale("log")
ax1.set_ylabel('velocity')

# Add new y-axis for pitch_angle
ax3 = ax1.twinx()
ax3.set_frame_on(True)
ax3.patch.set_visible(False)
pitch_angle = dft['pitch_angle']
ax3.plot(dft['time'], pitch_angle,'g-',label='pitch_angle')
ax3.set_ylabel('pitch_angle', color='g')
ax3.yaxis.set_ticks_position('right')
ax3.yaxis.set_tick_params(labelright=True)

ax2.plot(dft['time'], dft['v_perp_eV'], 'b-', label='')
ax2.plot(dft['time'], dft['v_para_eV'], 'r-', label='')
ax2.set_xlabel('time(s)')
ax2.set_yscale("log")
ax2.set_xscale("log")
ax2.set_ylabel('velocity_eV')

ax4 = ax2.twinx()
ax4.set_frame_on(True)
ax4.patch.set_visible(False)
ax4.plot(dft['time'], pitch_angle,'g-',label='')
ax4.set_ylabel('pitch_angle', color='g')
ax4.yaxis.set_ticks_position('right')
ax4.yaxis.set_tick_params(labelright=True)



ax5.plot(dfx['x'], dfx['v_perp_eV'], 'b-', label='')
ax5.plot(dfx['x'], dfx['v_para_eV'], 'r-', label='')
ax5.set_xlabel('x(km)')
ax5.set_yscale("log")
ax5.set_ylabel('velocity')

#Add new y-axis for relative_density
ax7 = ax5.twinx()
ax7.spines["right"].set_position(("axes", 1.15))
ax7.set_frame_on(True)
ax7.patch.set_visible(False)
relative_density = dfx['relative_density']
ax7.plot(dfx['x'], relative_density,'m-',label='relative_density')
ax7.set_ylabel('relative_density', color='m')
ax7.yaxis.set_ticks_position('right')
ax7.yaxis.set_tick_params(labelright=True)

#Add new y-axis for pitch_angle
ax9 = ax5.twinx()
ax9.set_frame_on(True)
ax9.patch.set_visible(False)
pitch_angle = dfx['pitch_angle']
ax9.plot(dfx['x'], pitch_angle,'g-',label='')
ax9.set_ylabel('pitch_angle', color='g')
ax9.yaxis.set_ticks_position('right')
ax9.yaxis.set_tick_params(labelright=True)

ax6.plot(dfx['x'], dfx['v_perp_eV'], 'b-', label='')
ax6.plot(dfx['x'], dfx['v_para_eV'], 'r-', label='')
ax6.set_xlabel('x(km)')
ax6.set_yscale("log")
ax6.set_xscale("log")
ax6.set_ylabel('velocity_eV')

#Add new y-axis for relative_density
ax8 = ax6.twinx()
ax8.spines["right"].set_position(("axes", 1.15))
ax8.set_frame_on(True)
ax8.patch.set_visible(False)
relative_density = dfx['relative_density']
ax8.plot(dfx['x'], relative_density,'m-',label='')
ax8.set_ylabel('relative_density', color='m')
ax8.yaxis.set_ticks_position('right')
ax8.yaxis.set_tick_params(labelright=True)

#Add new y-axis for pitch_angle
ax10 = ax6.twinx()
ax10.set_frame_on(True)
ax10.patch.set_visible(False)
pitch_angle = dfx['pitch_angle']
ax10.plot(dfx['x'], pitch_angle,'g-',label='')
ax10.set_ylabel('pitch_angle', color='g')
ax10.yaxis.set_ticks_position('right')
ax10.yaxis.set_tick_params(labelright=True)

fig.legend(loc='upper left')
plt.subplots_adjust(wspace=0.4)
plt.show()
