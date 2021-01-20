import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 10, 0.1)
s = np.sin(x)
c = np.cos(x)
plt.rcParams["font.size"] = 14
plt.plot(x, s, "r", label="sin")
plt.plot(x, c, "k", label="cos")
plt.title("Title", fontsize=18)
plt.xlabel("xlabel", fontsize=18)
plt.ylabel("ylabel", fontsize=18)
plt.legend(fontsize=18)
plt.tick_params(labelsize=18)
plt.show()
