Quickstart Guide
================

Installation
------------

**Requirements:**

- Python 3.9 or higher
- NumPy 2.0+
- Matplotlib 3.9+
- Astropy 6.1+
- VPLanet 2.4.24+

**From pip:**

.. code-block:: bash

    python -m pip install vplot

**From source:**

.. code-block:: bash

    git clone https://github.com/VirtualPlanetaryLaboratory/vplot
    cd vplot
    python -m pip install -e .

Basic Usage
-----------

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

The quickest way to visualize VPLanet output is via the command line:

.. code-block:: bash

    # Navigate to a directory containing vplanet output
    cd path/to/vplanet/simulation

    # Generate plots grouped by parameter
    vplot -g param

    # Generate plots grouped by physical type
    vplot -g type

    # Generate individual plots for each parameter
    vplot -g none

**Command line options:**

- ``-g, --group``: Grouping mode (``param``, ``type``, or ``none``)
- ``-b, --bodies``: Comma-separated list of bodies to plot (default: all)
- ``-p, --params``: Comma-separated list of parameters to plot (default: all)
- ``--xlog``: Use logarithmic x-axis
- ``--ylog``: Use logarithmic y-axis
- ``--show``: Display plots interactively (default: save to files)

**Example:**

.. code-block:: bash

    # Plot only eccentricity and semi-major axis for Earth
    vplot -g type -b Earth -p Eccentricity,SemiMajorAxis

Python API
~~~~~~~~~~

For more control, use vplot as a Python module:

**Automatic plotting:**

.. code-block:: python

    import vplot

    # Generate all plots for a simulation
    figs = vplot.auto_plot(
        path="path/to/simulation",
        group="param",     # Group by parameter
        show=False         # Save to files instead of showing
    )

    # Filter by bodies and parameters
    figs = vplot.auto_plot(
        path="path/to/simulation",
        group="type",                           # Group by physical type
        bodies=["Earth", "Moon"],               # Only plot these bodies
        params=["Eccentricity", "Inclination"]  # Only plot these params
    )

**Manual plotting with automatic labels:**

.. code-block:: python

    import matplotlib.pyplot as plt
    import vplanet
    import vplot

    # Load VPLanet output
    output = vplanet.run("vpl.in")

    # Create a figure - vplot automatically labels axes!
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot with automatic labeling
    ax.plot(output.Earth.Time, output.Earth.Eccentricity)

    # Show the plot
    plt.show()

**Scatter plots:**

.. code-block:: python

    import matplotlib.pyplot as plt
    import vplanet
    import vplot

    # Load output
    output = vplanet.run("vpl.in")

    # Scatter plot with automatic labels
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(output.Earth.Eccentricity, output.Earth.SemiMajorAxis)
    plt.show()

**Logarithmic axes:**

.. code-block:: python

    import matplotlib.pyplot as plt
    import vplanet
    import vplot

    output = vplanet.run("vpl.in")

    # Create figure with logarithmic x-axis
    fig = plt.figure(xlog=True)
    ax = fig.add_subplot(111)
    ax.plot(output.Earth.Time, output.Earth.SurfTemp)
    plt.show()

    # Or both axes logarithmic
    fig = plt.figure(xlog=True, ylog=True)
    ax = fig.add_subplot(111)
    ax.plot(output.Earth.Time, output.Earth.RotPer)
    plt.show()

**Multiple subplots:**

.. code-block:: python

    import matplotlib.pyplot as plt
    import vplanet
    import vplot

    output = vplanet.run("vpl.in")

    # Create figure with multiple subplots
    fig = plt.figure(figsize=(10, 8))

    ax1 = fig.add_subplot(221)
    ax1.plot(output.Earth.Time, output.Earth.Eccentricity)

    ax2 = fig.add_subplot(222)
    ax2.plot(output.Earth.Time, output.Earth.SemiMajorAxis)

    ax3 = fig.add_subplot(223)
    ax3.plot(output.Earth.Time, output.Earth.Obliquity)

    ax4 = fig.add_subplot(224)
    ax4.plot(output.Earth.Time, output.Earth.SurfTemp)

    plt.tight_layout()
    plt.show()

Features
--------

**Automatic axis labeling**

vplot automatically generates axis labels from VPLanet metadata:

- Parameter names are converted to readable labels
- Physical units are extracted and formatted
- Body names are included when plotting multiple bodies
- Physical types are detected and used for grouping

**Accessible color palette**

vplot provides a colorblind-friendly color palette:

.. code-block:: python

    import matplotlib.pyplot as plt
    import vplot

    # Use vplot colors
    plt.plot(x, y1, color=vplot.colors.red)
    plt.plot(x, y2, color=vplot.colors.orange)
    plt.plot(x, y3, color=vplot.colors.pale_blue)
    plt.plot(x, y4, color=vplot.colors.dark_blue)
    plt.plot(x, y5, color=vplot.colors.purple)

**Automatic legends**

When plotting multiple datasets, vplot can automatically create legends:

.. code-block:: python

    import matplotlib.pyplot as plt
    import vplanet
    import vplot

    output = vplanet.run("vpl.in")

    # auto_legend=True enables automatic legend generation
    fig = plt.figure(auto_legend=True)
    ax = fig.add_subplot(111)

    ax.plot(output.Earth.Time, output.Earth.Eccentricity)
    ax.plot(output.Mars.Time, output.Mars.Eccentricity)

    plt.show()

Troubleshooting
---------------

**Import errors**

If you encounter import errors, ensure all dependencies are installed:

.. code-block:: bash

    python -m pip install numpy>=2.0.0 matplotlib>=3.9.0 astropy>=6.1.0 vplanet>=2.4.24

**VPLanet not found**

vplot requires VPLanet to be installed and accessible. Install it via:

.. code-block:: bash

    python -m pip install vplanet

**No plots generated**

If ``auto_plot()`` returns an empty list, check that:

1. The path contains valid VPLanet output files
2. The system name matches your .in files
3. The bodies/params filters match available data

**Unit compatibility errors**

If you see "Incompatible units" errors, ensure you're not plotting parameters with incompatible physical types on the same axis.

Migration from v1.x
-------------------

**vplot v2.0 includes breaking changes:**

1. **Python version**: Minimum Python version increased to 3.9 (was 3.6)
2. **Dependencies**: All dependencies updated to modern versions (NumPy 2.0+, Matplotlib 3.9+, etc.)
3. **No backward compatibility**: v2.0 is a clean break from v1.x

**Code changes required:**

None! The Python API remains unchanged. All existing scripts using vplot should work as-is.

**If you need Python 3.6-3.8 support:**

Use vplot v1.x:

.. code-block:: bash

    python -m pip install "vplot<2.0"

Next Steps
----------

- See :doc:`examples` for detailed tutorials and notebooks
- See :doc:`api` for complete API documentation
- Report issues at https://github.com/VirtualPlanetaryLaboratory/vplot/issues
