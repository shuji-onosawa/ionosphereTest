import json
import math
import subprocess
import csv
import numpy as np

# Load params.json
with open("./src/params.json", "r") as f:
    params = json.load(f)

prev_display_fig = params["display_fig"]
params["display_fig"] = False
folderlists = []

# Increase electric_field_mV/m by 0.01 for 10 times
angles = 0.5 * np.pi
divnum = 12
for i in range(divnum):
    n = 3  # 切り捨てしたい桁
    val = math.floor(0.3 * (np.cos(np.pi / 180.0 * 90 / (divnum + 1) * (i + 1))) * 10 ** n) / (10 ** n)
    params["electric_field_mV/m"] = val
    with open("./src/params.json", "w") as f:
        json.dump(params, f, indent=4, separators=(',', ': '))
    
    # Compile Runge-Kutta.cpp
    subprocess.run(["g++", "-o", "./execute/Runge-Kutta.out", "./src/Runge-Kutta.cpp"])
    
    # Execute Runge-Kutta.out
    subprocess.run(["./execute/Runge-Kutta.out"])

    with open("./src/params.json", "r") as f:
        paramlist = json.load(f)
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
                                                                               max_v_para_for_resonance_eV, occur_duration, occur_period,
                                                                               accele_t_max)
        folderlists.append([i, folder_name])
        print("Calc" + folder_name + "\n")

params["display_fig"] = prev_display_fig
with open("./src/params.json", "w") as f:
    json.dump(params, f, indent=4, separators=(',', ': '))

with open('./data/' + folder_ver + '/folderlists.csv', "w", newline="") as f:
    dict_writer = csv.writer(f)
    header = ["number", "foldername"]
    dict_writer.writerow(header)
    dict_writer.writerows(folderlists)

subprocess.run(["python3", "./src/plot_pitch_angle.py"])
