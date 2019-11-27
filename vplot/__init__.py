# -*- coding: utf-8 -*-
__author__ = "Rodrigo Luger (rodluger@gmail.edu)"
__copyright__ = "Copyright 2018, 2019 Rodrigo Luger"


# Set up the logger
import logging

logger = logging.getLogger("vplot")
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter("%(levelname)s:%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


# Set up the custom figure **before** any other imports
from . import figure


# Set up the matplotlib stylesheet
import matplotlib.pyplot as plt

plt.style.use("seaborn-paper")


# Import user-facing stuff
from .output import GetOutput
from .autoplot import AutoPlot
