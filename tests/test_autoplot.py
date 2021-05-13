# -*- coding: utf-8 -*-
import vplot
import matplotlib
import os


# Non-interactive
matplotlib.use("Agg")


# Get the path to the example
path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "docs",
    "notebooks",
    "examples",
    "CircumbinaryOrbit",
)


def test_autplot():
    figs = vplot.auto_plot(path, show=False)

    # TODO: run tests here
