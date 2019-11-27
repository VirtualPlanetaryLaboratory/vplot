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
earth = output.earth

# Plot
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 12))

fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, hspace=0.3, wspace=0.3)
for ax in axes.flatten():
    ax.margins(0, None)


axes[0, 0].set_title("Single body, single quantity")
axes[0, 0].plot(cbp.Time, cbp.Eccentricity)

axes[0, 1].set_title("Single body, two quantities")
axes[0, 1].plot(cbp.Time, cbp.LongA, ".")
axes[0, 1].plot(cbp.Time, cbp.LongP, ".")

axes[0, 2].set_title("Two bodies, single quantity")
axes[0, 2].plot(cbp.Time, cbp.Eccentricity)
axes[0, 2].plot(earth.Time, earth.Eccentricity)

axes[1, 0].set_title("Two bodies, two quantities")
axes[1, 0].plot(cbp.Time, cbp.LongA)
axes[1, 0].plot(earth.Time, earth.LongP)

axes[1, 1].set_title("One angle in degrees, one in radians")
axes[1, 1].plot(cbp.Time, cbp.LongA, ".")
axes[1, 1].plot(cbp.Time, cbp.LongP.to("rad"), ".")

axes[1, 2].set_title("A vplot quantity and a quantity with no y units")
axes[1, 2].plot(cbp.Time, cbp.LongA)
axes[1, 2].plot(cbp.Time, 180 + np.random.randn(len(cbp.Time)))

axes[2, 0].set_title("A vplot quantity and a quantity with no x or y units")
axes[2, 0].plot(cbp.Time, cbp.LongA)
axes[2, 0].plot(
    np.linspace(0, 100, len(cbp.Time)), 180 + np.random.randn(len(cbp.Time))
)

axes[2, 1].set_title("Same as first axis, but with custom labels")
axes[2, 1].plot(cbp.Time, cbp.Eccentricity)
axes[2, 1].set_xlabel("Years elapsed")
axes[2, 1].set_ylabel("Eccentricity of the circumbinary planet")

axes[2, 2].set_title("An unrelated, unitless quantity")
axes[2, 2].plot(np.linspace(0, 1, 100), np.random.randn(100))

# Show
plt.show()
