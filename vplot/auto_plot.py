# -*- coding: utf-8 -*-
from . import logger
from .output import get_output
import matplotlib.pyplot as plt
import numpy as np


def auto_plot(path=".", sysname=None, group="param", show=True, **kwargs):
    """Automatically plot the results of a :py:obj:`vplanet` run.
    
    Args:
        sysname (str, optional): System name. This is determined automatically,
            unless there are multiple runs in the same :py:obj:`path`. Defaults 
            to None.
        path (str, optional): Path to the directory containing the results of 
            the :py:obj:`vplanet` run. Defaults to the current directory.
        group (str, optional): How to group plots. Options are "param" 
            (one plot per parameter), "type" (one plot per physical type, such
            as angle, length, etc.), or "none" (one plot per column in the output
            file). Defaults to "param".
        show (bool, optional): Show the plots? Defaults to True. If False,
            returns the figures instead.
        kwargs (optional): Extra keyword arguments passed to 
            :py:class:`vplot.figure.VPLOTFigure`.
    
    Returns:
        If :py:obj:`show` is False, returns a list of figures.
    """
    # Parse kwargs
    group_allowed = ["type", "param", "none"]
    group = str(group).lower()
    assert group in group_allowed, "Keyword `group` must be one of {}.".format(
        ", ".join(group_allowed)
    )

    # Grab the output
    output = get_output(sysname=sysname, path=path)

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
    figs = []
    if group == "type":

        physical_types = list(set([p.unit.physical_type for p in params]))
        for physical_type in physical_types:
            arrays = [
                param
                for param in params
                if param.unit.physical_type == physical_type
            ]
            fig, ax = plt.subplots(1, **kwargs)
            for array in arrays:
                ax.plot(time, array)
            figs.append(fig)

    # One plot per parameter name (multiple bodies)
    elif group == "param":

        parameter_names = list(set([p.tags.get("name", None) for p in params]))
        for parameter_name in parameter_names:
            arrays = [
                param
                for param in params
                if param.tags.get("name", None) == parameter_name
            ]
            fig, ax = plt.subplots(1, **kwargs)
            for array in arrays:
                ax.plot(time, array)
            figs.append(fig)

    # One plot per parameter
    else:

        for param in params:
            fig, ax = plt.subplots(1, **kwargs)
            ax.plot(time, param)
            figs.append(fig)

    if show:
        plt.show()
    else:
        plt.close("all")
        return figs
