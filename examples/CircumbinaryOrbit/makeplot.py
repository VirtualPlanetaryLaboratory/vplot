"""
This script produces a reproduction of Figure 4 of Leung and Lee (2013), 
the orbital dynamics of Kepler-16b, using VPLANET's binary module.

David P. Fleming, University of Washington, 2018
Rodrigo Luger, Flatiron Institute, 2019
"""
import vplot as vpl
import matplotlib.pyplot as plt
import numpy as np

# Load data
output = vpl.GetOutput()
cbp = output.cbp

# Plot
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 10))

fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, hspace=0.3, wspace=0.3)
for ax in axes.flatten():
    ax.margins(0, None)


axes[0, 0].set_title("Single body, single quantity")
axes[0, 0].plot(cbp.Time, cbp.Eccentricity)

axes[0, 1].set_title("Single body, two quantities")
axes[0, 1].plot(cbp.Time, cbp.LongA, ".")
axes[0, 1].plot(cbp.Time, cbp.LongP, ".")


# An unrelated, non-Quantity plot
axes[1, 2].plot(np.linspace(0, 1, 100), np.random.randn(100))

# Show
plt.show()
