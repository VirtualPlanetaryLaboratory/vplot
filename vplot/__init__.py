# -*- coding: utf-8 -*-
__author__ = "Rodrigo Luger (rodluger@gmail.edu)"
__copyright__ = "Copyright 2018, 2019 Rodrigo Luger"

# Import the version
from .vplot_version import __version__


# Set up the logger
import logging

logger = logging.getLogger("vplot")
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter("%(levelname)s:%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


# Override matplotlib.figure.Figure
from . import figure


# Set up the matplotlib stylesheet
from . import style


# Import user-facing stuff
from .figure import VPLOTFigure
from .log import Log, LogBody, LogStage
from .output import get_output, Output, Body
from .auto_plot import auto_plot
from .quantity import VPLOTQuantity as Quantity


# Backwards-compatibility hacks
GetOutput = get_output


class colors:
    red = "#c91111"
    orange = "#e09401"
    pale_blue = "#13aed5"
    dark_blue = "#1321d8"
    purple = "#642197"


# User-facing stuff
__all__ = [
    "get_output",
    "auto_plot",
    "Log",
    "LogBody",
    "LogStage",
    "Output",
    "Body",
    "VPLOTFigure",
    "colors",
    "GetOutput",
]
