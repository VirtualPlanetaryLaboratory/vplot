# -*- coding: utf-8 -*-
from . import logger
from . import custom_units
from .quantity import Quantity
import re
import os
from glob import glob
import astropy.units as u
import logging
import numpy as np
import warnings


def get_param_unit(param, file, line):
    """
    Grab the parameter unit from a line in the log file.

    Returns an `astropy.units` unit.
    """
    match = re.search(r"\[(.*?)\]", param)
    if match:
        unit_str = match.groups()[0]

        with warnings.catch_warnings(record=True) as w:
            try:
                unit = u.Unit(unit_str)
                assert len(w) == 0
            except ValueError:
                logger.error(
                    "Error processing line {} of {}: ".format(line, file)
                    + "Cannot interpret unit."
                )
                unit = u.Unit("")
            except AssertionError:
                logger.warn(
                    "Error processing line {} of {}: ".format(line, file)
                    + str(w[0].message)
                )
                unit = u.Unit("")

        return unit
    else:
        # Dimensionless
        return u.Unit("")


def get_param_name(param, file, line):
    """
    Grab the parameter name from a line in the log file.

    Returns a string.
    """
    # Replace bad characters
    repl = [("#", "")]
    for a, b in repl:
        param = param.replace(a, b)

    # Search for a match
    match = re.search(r"\((.*?)\)", param)
    if match:
        param = match.groups()[0]
        # If the param name starts with a number,
        # add an underscore so we can make it a
        # valid class property name
        if any(param.startswith(str(n)) for n in range(10)):
            param = "_" + param
        return param
    else:
        # There is no (ParameterName) here.
        # This is therefore not a variable, but a setting.
        # If there are spaces, get rid of them and force title case
        if " " in param:
            param = param.title().replace(" ", "")
        return param


def get_param_value(val, unit, file, line):
    """
    Grab the parameter value from a line in the log file.

    Returns an int, float (with units), bool, None (if no value
    was provided) or a string (if processing failed).
    """
    # Remove spaces
    val = val.lstrip().rstrip()

    # Is there a value?
    if val == "":
        return None

    # Check if int, float, or bool
    int_chars = "-0123456789"
    float_chars = int_chars + ".+e"
    if all([c in int_chars for c in val]):
        try:
            val = int(val)
        except ValueError:
            logger.error(
                "Error processing line {} of {}: ".format(line, file)
                + "Cannot interpret value as integer."
            )
            # Return unprocessed string
            return val
    elif all([c in float_chars for c in val]):
        try:
            val = Quantity(float(val) * unit)
        except ValueError:
            logger.error(
                "Error processing line {} of {}: ".format(line, file)
                + "Cannot interpret value as float."
            )
            # Return unprocessed string
            return val
    elif (val.lower() == "true") or (val.lower() == "yes"):
        val = True
    elif (val.lower() == "false") or (val.lower() == "no"):
        val = False
    elif val.lower() == "inf":
        val = np.inf
    elif val.lower() == "-inf":
        val = -np.inf
    elif val.lower() == "nan":
        val = np.nan
    return val


class Log(object):
    """

    """

    def __init__(self, sysname=""):
        self.sysname = sysname
        self.header = LogStage("Header")
        self.initial = LogStage("Initial")
        self.final = LogStage("Final")
        self._body_names = []
        self.path = ""

    def __repr__(self):
        return "<VPLOT Log File: %s>" % self.sysname


class LogStage(object):
    """

    """

    def __init__(self, name="Header"):
        self._name = name

    def __repr__(self):
        return "<VPLOT Log Object: %s>" % self._name


class LogBody(object):
    """

    """

    def __init__(self, name=""):
        self._name = name

    def __repr__(self):
        return "<VPLOT Log Object: %s>" % self._name


def get_log(sysname=None, path=".", ext="log"):
    """

    """
    # Just in case!
    if ext.startswith("."):
        ext = ext[1:]

    # Look for the log file
    if sysname is None:
        lf = glob(os.path.join(path, "*.%s" % (ext)))
        if len(lf) > 1:
            raise Exception("There are multiple log files in this directory.")
        elif len(lf) == 0:
            raise Exception(
                "There doesn't seem to be a log file in this directory."
            )
        else:
            lf = lf[0]
            sysname = os.path.basename(lf).split(".%s" % ext)[0]
    else:
        lf = glob(os.path.join(path, "%s.%s" % (sysname, ext)))
        if len(lf) == 0:
            raise Exception(
                "There doesn't seem to be a log file in this directory."
            )
        else:
            lf = lf[0]

    # Grab the contents
    with open(lf, "r") as f:
        lines = f.readlines()

    # Shorten the file name for logging
    lf = os.path.basename(lf)

    # Remove newlines and blank lines
    header = []
    initial = []
    final = []
    stage = 0
    for i, line in enumerate(lines):
        line = line.replace("\n", "")
        if "INITIAL SYSTEM PROPERTIES" in line:
            stage = 1
        elif "FINAL SYSTEM PROPERTIES" in line:
            stage = 2
        if len(line):
            if stage == 0:
                if ("Log file" not in line) and ("FORMATTING" not in line):
                    header.append((i + 1, line))
            elif stage == 1:
                if ("SYSTEM PROPERTIES" not in line) and (
                    "PARAMETERS" not in line
                ):
                    initial.append((i + 1, line))
            elif stage == 2:
                if ("SYSTEM PROPERTIES" not in line) and (
                    "PARAMETERS" not in line
                ):
                    final.append((i + 1, line))

    # Instantiate a `Log` object
    log = Log(sysname)
    log.path = os.path.abspath(path)

    # Process the header
    for i, line in header:
        try:
            name_and_unit, value = line.split(":")
            unit = get_param_unit(name_and_unit, lf, i)
            name = get_param_name(name_and_unit, lf, i)
            value = get_param_value(value, unit, lf, i)
            setattr(log.header, name, value)
        except Exception as e:
            raise ValueError(
                "Error processing line {} of {}: ".format(i, lf) + str(e)
            )

    # Process the initial conditions
    body = "system"
    setattr(log.initial, body, LogBody(body))
    for i, line in initial:
        if "BODY:" not in line:
            try:
                name_and_unit, value = line.split(":")
                unit = get_param_unit(name_and_unit, lf, i)
                name = get_param_name(name_and_unit, lf, i)
                value = get_param_value(value, unit, lf, i)
                setattr(getattr(log.initial, body), name, value)
            except Exception as e:
                raise ValueError(
                    "Error processing line {} of {}: ".format(i, lf) + str(e)
                )
        else:
            try:
                match = re.search(r"BODY:\s(.*?)\s-", line)
                body = match.groups()[0]
            except:
                raise ValueError(
                    "Error processing line {} of {}: ".format(i, lf)
                    + "Cannot understand body name."
                    + line
                )
            setattr(log.initial, body, LogBody(body))
            log._body_names.append(body)

    # Process the final conditions
    body = "system"
    setattr(log.final, body, LogBody(body))
    for i, line in final:
        if "BODY:" not in line:
            try:
                name_and_unit, value = line.split(":")
                unit = get_param_unit(name_and_unit, lf, i)
                name = get_param_name(name_and_unit, lf, i)
                value = get_param_value(value, unit, lf, i)
                setattr(getattr(log.final, body), name, value)
            except Exception as e:
                raise ValueError(
                    "Error processing line {} of {}: ".format(i, lf) + str(e)
                )
        else:
            try:
                match = re.search(r"BODY:\s(.*?)\s-", line)
                body = match.groups()[0]
            except:
                raise ValueError(
                    "Error processing line {} of {}: ".format(i, lf)
                    + "Cannot understand body name."
                    + line
                )
            setattr(log.final, body, LogBody(body))

    return log
