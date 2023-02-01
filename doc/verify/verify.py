import numpy as np

lamb = 74.9892 * 3.14159265 / 180.0
b1 = np.sqrt(1.0 + 3.0 * np.sin(lamb) * np.sin(lamb)) / np.power(np.cos(lamb), 6.0)
lamb = 70.9874 * 3.14159265 / 180.0
b2 = np.sqrt(1.0 + 3.0 * np.sin(lamb) * np.sin(lamb)) / np.power(np.cos(lamb), 6.0)

print(np.sqrt(b2 / b1))

####################################################

oxigen_mass = 1.672e-27 * 16.0
electric_field = 1.00e-3
oxigen_charge = 1.602e-19 * 8.0
vel = electric_field * oxigen_charge / oxigen_mass * 2.0
eV = 0.5 * oxigen_mass * vel * vel / (1.6021e-19)
print(eV)
