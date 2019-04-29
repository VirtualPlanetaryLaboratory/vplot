vplot
-----
A suite of plotting routines for ``vplanet``. It can be used to both generate a
plot of all ``vplanet`` output data, or combined with matplotlib to easily import data
for professional figures. If running from the command line, the output parameter
list(s) must include Time, i.e. you can only instantly plot the evolution of the
parameters as a function of time.

Installation
============

``vplot`` will work most effectively if installed as the super-user as follows:

.. code-block:: bash

    git clone https://github.com/VirtualPlanetaryLaboratory/vplot.git
    cd vplot
    python setup.py develop

If you prefer to install without root access, you can do so by replacing the last line with:

.. code-block:: bash

    python setup.py install --user

You can edit the ``vplot_config.py`` to specify custom
settings. This file is automatically created in the *cwd* when you run ``vplot``.
Type ``vplot -h`` for the complete list of options.

``vplot`` can be run from the command line to quickly generate a figure that shows
the evolution of every output parameter from a ``vplanet`` simulation. After a simulation
has completed, simply type

.. code-block:: bash

    vplot

and a figure will appear with all the output data plotted.


Quick-and-dirty docs
====================
.. code-block:: bash

    VPLOT
    -----
    usage: vplot  [-h [OPTION_NAME]] [-b [BODIES [BODIES ...]]]
                  [-x XAXIS] [-y [YAXIS [YAXIS ...]]] [-a ALPHA]

    optional arguments:
      -h [OPTION_NAME]          Show this help message or the docstring for OPTION_NAME
      -b BODIES [BODIES ...]    Bodies to plot; should match names of .in files in cwd
      -x XAXIS                  Parameter to plot on the x-axis
      -y YAXIS [YAXIS ...]      Parameter(s) to plot on the y-axis
      -a ALPHA                  Parameter to control line alpha

    version: 0.3.0

    vplot_config.py options:
      figheight, figname, figwidth, interactive, legend_all, legend_fontsize, legend_loc,
      line_styles, linewidth, maxplots, maxylabelsize, short_labels, skip_xzero_log,
      tight_layout, title, xlabel_fontsize, xlog, xticklabel_fontsize, ylabel_fontsize,
      ylog, ymargin, yticklabel_fontsize


    Type `vplot -h OPTION_NAME` for info on any option

After installation ``vplot`` can be imported and used with matplotlib to easily
import ``vplanet`` data and quickly generate figures. You can check the examples/ directory
in the ``vplanet`` repo for examples on how to use ``vplot`` in this case.

``vplot`` must be installed to perform unit tests with ``vplanet``.
