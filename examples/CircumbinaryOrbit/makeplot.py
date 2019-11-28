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
output = vpl.get_output()
cbp = output.cbp
earth = output.earth

# Plot several things
plt.figure()
plt.title("Single body, single quantity")
plt.plot(cbp.Time, cbp.Eccentricity)

plt.figure()
plt.title("Single body, two quantities")
plt.plot(cbp.Time, cbp.LongA, ".")
plt.plot(cbp.Time, cbp.LongP, ".")

plt.figure()
plt.title("Two bodies, single quantity")
plt.plot(cbp.Time, cbp.Eccentricity)
plt.plot(earth.Time, earth.Eccentricity)

plt.figure()
plt.title("Two bodies, two quantities")
plt.plot(cbp.Time, cbp.LongA)
plt.plot(earth.Time, earth.LongP)

plt.figure()
plt.title("One angle in degrees, one in radians")
plt.plot(cbp.Time, cbp.LongA, ".")
plt.plot(cbp.Time, cbp.LongP.to("rad"), ".")

plt.figure()
plt.title("A vplot quantity and a quantity with no y units")
plt.plot(cbp.Time, cbp.LongA)
plt.plot(cbp.Time, 180 + np.random.randn(len(cbp.Time)))

plt.figure()
plt.title("A vplot quantity and a quantity with no x or y units")
plt.plot(cbp.Time, cbp.LongA)
plt.plot(
    np.linspace(0, 100, len(cbp.Time)), 180 + np.random.randn(len(cbp.Time))
)

plt.figure()
plt.title("Same as first plot, but with custom labels")
plt.plot(cbp.Time, cbp.Eccentricity)
plt.xlabel("Years elapsed")
plt.ylabel("Eccentricity of the circumbinary planet")

plt.figure()
plt.title("An unrelated, unitless quantity")
plt.plot(np.linspace(0, 1, 100), np.random.randn(100))

# Show all plotss
plt.show()
