import numpy as np

lamb = 74.9892 * 3.14159265 / 180.0
b1 = np.sqrt(1.0 + 3.0 * np.sin(lamb) * np.sin(lamb)) / np.power(np.cos(lamb), 6.0)
lamb = 70.9874 * 3.14159265 / 180.0
b2 = np.sqrt(1.0 + 3.0 * np.sin(lamb) * np.sin(lamb)) / np.power(np.cos(lamb), 6.0)

print(np.sqrt(b2 / b1))

####################################################

oxigen_mass = 1.672e-27 * 16.0
electric_field = 1.00e-4
oxigen_charge = 1.602e-19 * 1.0
print(electric_field * oxigen_charge / oxigen_mass)

vel = np.sqrt(150.0 / oxigen_mass * 2.0 * (1.6021e-19))
dvmirror = 0.5 * 7.0e-7 * vel * vel
print(dvmirror)

print(oxigen_charge / oxigen_mass * 1e-9)

##################################
calc_vel = 6.0e3 / 3.5
eV = 0.5 * oxigen_mass * calc_vel * calc_vel / 1.6021e-19
print(eV)

##################################
R_e = 6.3e6
init_Inval_lat_deg = 75
inval_lat = init_Inval_lat_deg / 180.0 * 3.141592
L_shell = 10.0
gradBperB = 3.0 * np.sin(inval_lat) * (5.0 * np.sin(inval_lat) * np.sin(inval_lat) + 3.0) / (
    np.power((1.0 + 3.0 * np.sin(inval_lat) * np.sin(inval_lat)), 1.5) * np.cos(inval_lat) * np.cos(inval_lat)) * (1.0 / (R_e * L_shell))
print(gradBperB)
