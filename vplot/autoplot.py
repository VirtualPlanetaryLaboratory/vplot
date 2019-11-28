# -*- coding: utf-8 -*-
from . import logger
from .output import GetOutput
import matplotlib.pyplot as plt
import numpy as np


def AutoPlot(sysname=None, path=".", group="param"):
    """

    """
    # Parse kwargs
    group_allowed = ["type", "param", "none"]
    group = str(group).lower()
    assert group in group_allowed, "Keyword `group` must be one of {}.".format(
        ", ".join(group_allowed)
    )

    # Grab the output
    output = GetOutput(sysname=sysname, path=path)

    # Grab all params
    params = []
    for body in output.bodies:
        params += body._params

    # Get the time array in years
    time = [
        param for param in params if param.tags.get("name", None) == "Time"
    ]
    if len(time) == 0:
        time = time[0]
    else:
        for k in range(1, len(time)):
            assert np.array_equal(
                time[0].to("yr"), time[k].to("yr")
            ), "Mismatch in the time arrays for two of the bodies."
        time = time[0]

    # Remove it from the params
    params = [
        param for param in params if param.tags.get("name", None) != "Time"
    ]

    # One plot per physical type
    if group == "type":

        physical_types = list(set([p.unit.physical_type for p in params]))
        for physical_type in physical_types:
            arrays = [
                param
                for param in params
                if param.unit.physical_type == physical_type
            ]
            fig, ax = plt.subplots(1)
            for array in arrays:
                ax.plot(time, array)

    # One plot per parameter name (multiple bodies)
    elif group == "param":

        parameter_names = list(set([p.tags.get("name", None) for p in params]))
        for parameter_name in parameter_names:
            arrays = [
                param
                for param in params
                if param.tags.get("name", None) == parameter_name
            ]
            fig, ax = plt.subplots(1)
            for array in arrays:
                ax.plot(time, array)

    # One plot per parameter
    else:

        for param in params:
            fig, ax = plt.subplots(1)
            ax.plot(time, param)

    plt.show()
