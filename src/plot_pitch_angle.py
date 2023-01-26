import pandas as pd
import matplotlib.pyplot as plt

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

# 読み込み
df = pd.read_csv('./data/result_x.csv', header=0)

focus_height = 8000  # Height from accleration area upper limit(km)
acclere_range = 7900  # Heigth accleration area(km)

# xがAからBまでのデータのみ抽出

x_min = focus_height - acclere_range
x_max = focus_height

df = df[(df["x"] >= x_min) & (df["x"] <= x_max)]

pitch_angles = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

# tの最小値と最大値
t_min, t_max = df["time"].min(), df["time"].max()

# dt
dt = 1

# t_minからt_min+dt, t_minからt_min+2*dt, t_minからt_min+3*dt.....t_minから
# t_min+n*dt, t_min+dtからt_min+n*dt, t_min+2*dtからt_min+n*dt, t_min+3*dtから
# t_min+n*dt......t_min*(n-1)+dtからt_min+n*dtまでのそれぞれについての、
# pitch_angleが0-10, 10-20, 20-30, 30-40, 40-50, 50-60, 60-70, 70-80, 80-90それぞれにおけるrelative_densityの和を求める
n = int((t_max - t_min) / dt) + 1  # nの定義

relative_density_sums = [[0 for _ in range(2 * n)] for _ in range(len(pitch_angles) - 1)]
energy_density_sums = [[0 for _ in range(2 * n)] for _ in range(len(pitch_angles) - 1)]


for i in range(len(pitch_angles) - 1):
    for j in range(2 * n):
        t_min_j = max(t_min + j * dt - n * dt, 0)
        t_max_j = min(t_min + j * (dt + 1), t_max)
        for index, row in df[(t_min_j <= df["time"]) &
                             (df["time"] < t_max_j) &
                             (pitch_angles[i] <= df["pitch_angle"]) &
                             (df["pitch_angle"] < pitch_angles[i + 1])].iterrows():
            energy_density_sums[i][j] += row["energy_density"]
            relative_density_sums[i][j] += row["relative_density"]


t_plot = [i * dt for i in range(2 * n)]
pitch_angles.pop(len(pitch_angles) - 1)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))


# energy_density_sumsをカラープロットします
ax1.set_title('Graph1:erg_density')
mappable1 = ax1.pcolormesh(t_plot, pitch_angles, energy_density_sums)
ax1.set_xlabel('t_min + n*dt')
ax1.set_ylabel('pitch_angle')
ax1bar = fig.colorbar(mappable1, ax=ax1, orientation="vertical")
# ax1bar.setclim(-1,1)
ax1.set_label("erg_density")

# relative_density_sumsをカラープロットします
ax1.set_title('Graph2:relative_density')
mappable2 = ax2.pcolormesh(t_plot, pitch_angles, relative_density_sums)
ax2.set_xlabel('t_min + n*dt')
ax2.set_ylabel('pitch_angle')
ax1bar = fig.colorbar(mappable2, ax=ax2, orientation="vertical")
# ax1bar.setclim(-1,1)
ax1.set_label("density")


plt.suptitle(ion_name + " " + electric_field + 'mV/m,' + ' init_v_para = ' + init_v_para_eV + 'eV, init_v_perp = ' + init_v_perp_eV +
             'eV, max_v_para_for_resonance = ' + max_v_para_for_resonance_eV + "eV,\nWave occurs for " + occur_duration + "sec during " +
             occur_period + "sec, " + "accleration_time_max" + accele_t_max + 'sec, ' + 'x_max = ' + x_max + 'km x_min = ' + x_min + 'km')
plt.subplots_adjust(wspace=0.5, hspace=0.4)
plt.savefig('./graphs/pitch_angle' + ion_name + electric_field + 'mVm_' + 'init_v_para_' + init_v_para_eV + 'eV_init_v_perp_' + init_v_perp_eV +
            'eV_max_resonance_' + max_v_para_for_resonance_eV + "eV" + occur_duration + "sec_per" + occur_period + "t_max" + accele_t_max +
            "sec" + 'x_max_' + x_max + 'x_min_' + x_min + '.png')
plt.show()
