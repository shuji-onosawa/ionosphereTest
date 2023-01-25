import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('result.csv')

fig, ax = plt.subplots()

ax.plot(df['time'], df['v_perp'], 'b-', label='v_perp')
ax.plot(df['time'], df['v_para'], 'r-', label='v_para')
ax.set_yscale("log")
ax.set_xlabel('time')
ax.set_ylabel('velocity')

# Add new y-axis for pitch_angle
ax3 = ax.twinx()
ax3.set_frame_on(True)
ax3.patch.set_visible(False)

pitch_angle = df['pitch_angle']
ax3.plot(df['time'], pitch_angle,'g-',label='pitch_angle')
ax3.set_ylabel('pitch_angle', color='g')
ax3.yaxis.set_ticks_position('right')
ax3.yaxis.set_tick_params(labelright=True)

fig.legend(loc='upper left')
plt.show()
