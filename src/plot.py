import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('result.csv')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(df['time'], df['v_perp'], 'b-', label='v_perp')
ax1.plot(df['time'], df['v_para'], 'r-', label='v_para')
ax1.set_xlabel('time(s)')
ax1.set_yscale("log")
ax1.set_ylabel('velocity')

# Add new y-axis for pitch_angle
ax3 = ax1.twinx()
ax3.set_frame_on(True)
ax3.patch.set_visible(False)
pitch_angle = df['pitch_angle']
ax3.plot(df['time'], pitch_angle,'g-',label='pitch_angle')
ax3.set_ylabel('pitch_angle', color='g')
ax3.yaxis.set_ticks_position('right')
ax3.yaxis.set_tick_params(labelright=True)

ax2.plot(df['time'], df['v_perp_eV'], 'b-', label='v_perp_eV')
ax2.plot(df['time'], df['v_para_eV'], 'r-', label='v_para_eV')
ax2.set_xlabel('time(s)')
ax2.set_yscale("log")
ax2.set_ylabel('velocity_eV')

ax4 = ax2.twinx()
ax4.set_frame_on(True)
ax4.patch.set_visible(False)
ax4.plot(df['time'], pitch_angle,'g-',label='pitch_angle')
ax4.set_ylabel('pitch_angle', color='g')
ax4.yaxis.set_ticks_position('right')
ax4.yaxis.set_tick_params(labelright=True)

fig.legend(loc='upper left')
plt.subplots_adjust(wspace=0.4)
plt.show()
