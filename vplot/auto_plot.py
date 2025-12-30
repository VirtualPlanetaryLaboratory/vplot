# -*- coding: utf-8 -*-
from vplanet import get_output
import matplotlib.pyplot as plt
import numpy as np


def flistAutoPlot(
    sPath=".",
    sSysname=None,
    sGroup="param",
    listBodies=[],
    listParams=[],
    bShow=True,
    **kwargs
):
    """Automatically plot the results of a :py:obj:`vplanet` run.

    Args:
        sSysname (str, optional): System name. This is determined automatically,
            unless there are multiple runs in the same :py:obj:`sPath`. Defaults
            to None.
        sPath (str, optional): Path to the directory containing the results of
            the :py:obj:`vplanet` run. Defaults to the current directory.
        sGroup (str, optional): How to group plots. Options are "param"
            (one plot per parameter), "type" (one plot per physical type, such
            as angle, length, etc.), or "none" (one plot per column in the output
            file). Defaults to "param".
        listBodies (list, optional): Which bodies to generate plots for. These
            should be specified as a list of strings (case-insensitive). Defaults
            to ``[]``, in which case all available bodies are plotted.
        listParams (list, optional): Which parameters to generate plots for. These
            should be specified as a list of strings (case-insensitive). Defaults
            to ``[]``, in which case all available parameters are plotted.
        bShow (bool, optional): Show the plots? Defaults to True. If False,
            returns the figures instead.
        kwargs (optional): Extra keyword arguments passed directly to
            :py:class:`vplot.VPLOTFigure`.

    Returns:
        If :py:obj:`bShow` is False, returns a list of figures.
    """
    # Parse kwargs
    listGroupAllowed = ["type", "param", "none"]
    sGroup = str(sGroup).lower()
    assert sGroup in listGroupAllowed, "Keyword `sGroup` must be one of {}.".format(
        ", ".join(listGroupAllowed)
    )

    if type(listBodies) is str:
        listBodies = [listBodies]
    assert type(listBodies) is list, "Keyword `listBodies` must be a list."
    for iI, sBody in enumerate(listBodies):
        assert type(sBody) is str, "Items in `listBodies` must be strings."
        listBodies[iI] = sBody.lower()
    listBodyNames = listBodies

    if type(listParams) is str:
        listParams = [listParams]
    assert type(listParams) is list, "Keyword `listParams` must be a list."
    for iI, sParam in enumerate(listParams):
        assert type(sParam) is str, "Items in `listParams` must be strings."
        listParams[iI] = sParam.lower()
    listParamNames = [sParam for sParam in listParams if sParam.lower() != "time"]

    # Grab the output
    output = get_output(sysname=sSysname, path=sPath)

    # Grab all params
    listParams = []
    time = None
    for body in output.bodies:
        if len(listBodyNames) == 0 or body._name.lower() in listBodyNames:
            for param in body._params:
                if param.tags.get("name", "").lower() == "time":
                    if time is None:
                        time = param
                    else:
                        assert np.array_equal(
                            time.to("yr"), param.to("yr")
                        ), "Mismatch in the time arrays for two of the bodies."
                elif (
                    len(listParamNames) == 0
                    or param.tags.get("name", "").lower() in listParamNames
                ):
                    listParams.append(param)

    if len(listParams) == 0:
        raise RuntimeError("No parameters found for plotting.")
    elif time is None:
        raise RuntimeError("No `Time` array found for any of the bodies.")

    # One plot per physical type
    listFigs = []
    if sGroup == "type":

        listPhysicalTypes = list(set([p.unit.physical_type for p in listParams]))
        for sPhysicalType in listPhysicalTypes:
            listArrays = [
                param
                for param in listParams
                if param.unit.physical_type == sPhysicalType
            ]
            fig, axCurrent = plt.subplots(1, **kwargs)
            for array in listArrays:
                axCurrent.plot(time, array)
            listFigs.append(fig)

    # One plot per parameter name (multiple bodies)
    elif sGroup == "param":

        listParameterNames = list(set([p.tags.get("name", None) for p in listParams]))
        for sParameterName in listParameterNames:
            listArrays = [
                param
                for param in listParams
                if param.tags.get("name", None) == sParameterName
            ]
            fig, axCurrent = plt.subplots(1, **kwargs)
            for array in listArrays:
                axCurrent.plot(time, array)
            listFigs.append(fig)

    # One plot per parameter
    else:

        for param in listParams:
            fig, axCurrent = plt.subplots(1, **kwargs)
            axCurrent.plot(time, param)
            listFigs.append(fig)

    if bShow:
        plt.show()
    else:
        plt.close("all")
        return listFigs
