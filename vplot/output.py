# -*- coding: utf-8 -*-
from . import logger
from . import custom_units
from .log import GetLog
from .quantity import Quantity
import logging
import numpy as np
import re
import os
import subprocess
import warnings
import astropy.units as u


class Output(object):
    """

    """

    def __init__(self):
        self.sysname = ""
        self.bodies = []

    def __getitem__(self, i):
        return self.bodies[i]

    def __len__(self):
        return len(self.bodies)

    def __repr__(self):
        return "<VPLOT Output: %s>" % self.sysname


class Body(object):
    """

    """

    def __init__(self):
        self.name = ""
        self._params = []

    def __getitem__(self, i):
        return self._params[i]

    def __len__(self):
        return len(self._params)

    def __repr__(self):
        return "<VPLOT Body: %s>" % self.name


def GetParamDescriptions():
    """

    """

    # Call vplanet help (it better be in the path!)
    try:
        help = subprocess.getoutput("vplanet -h")
    except OSError:
        logging.error("Unable to call VPLANET. Is it in your PATH?")
        return {}

    # Remove bold tags
    help = help.replace("\x1b[1m", "")
    help = help.replace("\x1b[0m", "")

    # Get only the output params
    stroutput = help.split("These options follow the argument saOutputOrder.")[1]
    stroutput = [x for x in stroutput.split("\n") if len(x)]
    description = {}
    for out in stroutput:
        if out.startswith("[-]"):
            n, d, _ = re.search(r"\[-\](.*) -- (.*). \[(.*)\]", out).groups()
            description.update({n: d})
        else:
            n, d = re.search("(.*) -- (.*).", out).groups()
            description.update({n: d})

    return description


def GetParams(outputorder, file):
    """

    """
    # Get parameter descriptions from the vplanet help
    description = GetParamDescriptions()

    # Remove spaces from units
    units = re.search(r"\[(.*?)\]", outputorder)
    if units is not None:
        for unit in units.group():
            outputorder = outputorder.replace(unit, unit.replace(" ", ""))

    # Populate the params
    outputorder = outputorder.split()
    params = []
    for j, param in enumerate(outputorder):

        # Get the name and units
        name, unit_str = re.search(r"(.*?)\[(.*?)\]", param).groups()

        # If the param name starts with a number,
        # add an underscore so we can make it a
        # valid class property name
        if any(name.startswith(str(n)) for n in range(10)):
            name = "_" + name

        # Process the unit
        with warnings.catch_warnings(record=True) as w:
            try:
                unit = u.Unit(unit_str)
                assert len(w) == 0
            except ValueError as e:
                logger.error("Error processing unit {}: ".format(unit_str) + (str(e)))
                unit = u.Unit("")
            except AssertionError:
                logger.warn(
                    "Error processing unit {}: ".format(unit_str) + str(w[0].message)
                )
                unit = u.Unit("")

        # Grab the array in the fwfile/bwfile
        array = []
        for line in file:
            array.append(float(line.split()[j]))

        # Give it units, a name, and a description
        array = Quantity(
            np.array(array) * unit, name=name, description=description.get(name, name)
        )

        # Add to the list
        params.append(array)

    return params


def GetArrays(log):
    """

    """
    # Initialize
    output = Output()

    # Get basic system info
    output.log = log
    output.sysname = log.sysname
    output.path = log.path

    # Grab body properties
    for i, body_name in enumerate(log._body_names):

        # Create a body
        body = Body()
        body.name = body_name

        # Grab the input file name
        body.infile = getattr(log.header, "BodyFile%d" % (i + 1))

        # Grab the output file names
        body.fwfile = "%s.%s.forward" % (output.sysname, body.name)
        body.bwfile = "%s.%s.backward" % (output.sysname, body.name)
        body.climfile = "%s.%s.Climate" % (output.sysname, body.name)
        if not os.path.exists(os.path.join(output.path, body.climfile)):
            body.climfile = ""

        # Grab the body color
        body.color = getattr(log.initial, body.name).Color

        # Grab the forward arrays. Note that they may not exist for this body
        try:
            with open(os.path.join(output.path, body.fwfile), "r") as f:
                fwfile = f.readlines()
        except IOError:
            fwfile = [""]

        # Grab the backward arrays. Note that they may not exist for this body
        try:
            with open(os.path.join(output.path, body.bwfile), "r") as f:
                bwfile = f.readlines()
        except IOError:
            bwfile = [""]

        # Now grab the output order and the params
        outputorder = getattr(log.initial, body.name).OutputOrder
        if fwfile != [""]:
            body._params = GetParams(outputorder, fwfile)
        elif bwfile != [""]:
            body._params = GetParams(outputorder, bwfile)

        # Climate file
        if body.climfile != "":
            # Grab the climate arrays...
            try:
                with open(os.path.join(output.path, body.climfile), "r") as f:
                    climfile = f.readlines()
            except IOError:
                raise Exception("Unable to open %s." % body.climfile)

            # ... and the grid order
            try:
                gridorder = getattr(log.initial, body.name).GridOutputOrder
                body._gridparams = GetParams(gridorder, climfile)
            except:
                logger.error(
                    "Unable to obtain grid output parameters from %s." % body.climfile
                )
        else:
            body._gridparams = []

        # Add the body
        output.bodies.append(body)

    return output


def GetOutput(sysname=None, path="."):
    """

    """
    # Get the log file and the arrays
    log = GetLog(sysname=sysname, path=path)
    output = GetArrays(log)

    for body in output.bodies:

        # Make the body accessible as an attribute
        setattr(output, body.name, body)

        # Make all the arrays accessible as attributes
        for array in getattr(output, body.name)._params:
            setattr(getattr(output, body.name), array.name, array)

        # Grid params
        if len(getattr(output, body.name)._gridparams):

            # Get the time array
            iTime = np.argmax(
                [
                    array.name == "Time"
                    for array in getattr(output, body.name)._gridparams
                ]
            )
            Time = getattr(output, body.name)._gridparams[iTime]

            # Get 2d array dimensions
            J = np.where(Time[1:] > Time[:-1])[0][0] + 1
            _, r = divmod(len(Time), J)
            if r != 0:
                raise Exception(
                    "Irregular time grid detected for {}. VPLOT is confused!".format(
                        body.name
                    )
                )

            for array in getattr(output, body.name)._gridparams:
                if array.name != "Time":
                    # We don't want to overwrite the time array!
                    setattr(getattr(output, body.name), array.name, array)

    return output