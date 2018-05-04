vplot
-----
A suite of plotting routines for ``vplanet``.

Installation
============

.. code-block:: bash

    git clone https://github.com/UWVPL/vplot.git
    cd vplot
    python setup.py develop

You can edit the ``vplot_config.py`` to specify custom
settings. This file is automatically created in the *cwd* when you run ``vplot``.
Type ``vplot -h`` for the complete list of options.


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
