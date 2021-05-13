# -*- coding: utf-8 -*-
__author__ = "Rodrigo Luger (rodluger@gmail.edu)"
__copyright__ = "Copyright 2018, 2019, 2020, 2021 Rodrigo Luger"

# Import the version
from .vplot_version import __version__


# Override matplotlib.figure.Figure
from . import figure


# Set up the matplotlib stylesheet
from . import style
from . import colors


# Import user-facing stuff
from .figure import VPLOTFigure
from .auto_plot import auto_plot
