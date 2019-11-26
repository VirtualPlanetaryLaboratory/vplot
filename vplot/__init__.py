# -*- coding: utf-8 -*-
__author__ = "Rodrigo Luger (rodluger@uw.edu)"
__copyright__ = "Copyright 2018, 2019 Rodrigo Luger"

import matplotlib.pyplot as plt
import logging

# Set up the matplotlib stylesheet
plt.style.use("seaborn-paper")

# Set up the logger
logger = logging.getLogger("vplot")
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter("%(levelname)s:%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

# Import user-facing stuff
from .output import GetOutput
