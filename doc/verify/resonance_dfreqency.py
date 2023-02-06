import numpy as np
import matplotlib.pyplot as plt

k = 10
x = np.linspace(0, 1, 1000)
y = np.sin(k * 2.0 * np.pi * x) / (k * 2.0 * np.pi * (1.0 - x))

plt.plot(x, -y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("sin(2*pi*x)/(2*pi*(1-x))")
plt.show()
