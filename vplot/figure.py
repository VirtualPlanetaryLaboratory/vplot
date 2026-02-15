# -*- coding: utf-8 -*-
from vplanet import Quantity
import matplotlib
import matplotlib.pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import astropy.units as u


def ftupleGetArrayInfo(array, max_label_length=40):
    if hasattr(array, "unit") and hasattr(array, "tags"):
        if array.unit.physical_type != array.tags.get(
            "physical_type", array.unit.physical_type
        ):
            # The physical type of this array changed, so this is
            # no longer the original VPLANET quantity!
            sUnit = str(array.unit)
            if sUnit == "":
                sUnit = None
            sBody = None
            sLabel = None
            sPhysicalType = str(array.unit.physical_type)
            if sPhysicalType == "dimensionless":
                sPhysicalType = None
        else:
            sUnit = str(array.unit)
            if sUnit == "":
                sUnit = None
            sBody = array.tags.get("body", None)
            sLabel = array.tags.get("description", None)
            if sLabel is not None and len(sLabel) > max_label_length:
                sLabel = array.tags.get("name", None)
            sPhysicalType = str(array.unit.physical_type)
            if sPhysicalType == "dimensionless":
                sPhysicalType = None
    else:
        sUnit = None
        sBody = None
        sLabel = None
        sPhysicalType = None
    return sUnit, sBody, sLabel, sPhysicalType


class VPLOTFigure(Figure):
    """A ``vplot`` figure object, a subclass of :py:class:`matplotlib.figure.Figure`.
    
    This class adds certain functionality to the default ``matplotlib`` figure
    object, in particular the ability to recognize when ``vplanet`` quantities
    are plotted. When showing / drawing / saving the figure, this class will
    automatically label the axes and/or add a legend with the appropriate 
    parameter names, types, units, and corresponding ``vplanet`` body. All of
    these can be overridden by setting the axes or legend labels explcitly.

    This class accepts all args and kwargs as :py:class:`matplotlib.figure.Figure`,
    with support for the following additional keywords:

    Args:
        max_label_length (int, optional): If the parameter description is longer
            than this value, the axis will be labeled with the shorter parameter
            name instead. Default 40.
        mpl_units (bool, optional): Enable matplotlib units functionality? Default
            is True. This allows quantities of the same physical type but different
            units (such as ``yr`` and ``Gyr``) to be plotted on the same axis; 
            this class will handle unit conversions as needed. An error will be 
            raised if the unit conversion fails.
        xlog (bool, optional): Set the x axis scale to be logarithmic? Default False.
        ylog (bool, optional): Set the y axis scale to be logarithmic? Default False.

    """

    def __init__(
        self,
        *args,
        max_label_length=40,
        mpl_units=True,
        xlog=False,
        ylog=False,
        auto_legend=True,
        **kwargs
    ):

        # Parameters
        self.max_label_length = max_label_length
        self.xlog = xlog
        self.ylog = ylog
        self.auto_legend = auto_legend

        # Enable astropy/matplotlib quantity support? (Recommended)
        if mpl_units:
            from vplanet.quantity_support import quantity_support

            quantity_support()

        super().__init__(*args, **kwargs)

        # Watch the axes
        self._update_on_draw = True
        self.add_axobserver(self.fnAxObserver)

    def fnAxObserver(self, *args):

        # Force an update next time we draw
        self._update_on_draw = True

        # Override ax.scatter to preserve metadata in Quantity arrays.
        # Scatter converts Quantity arrays to numpy masked arrays, losing metadata.

        for axCurrent in self.axes:

            # Mark it so we don't do it repeatedly
            if hasattr(axCurrent, "__vplot__"):
                continue
            else:
                axCurrent.__vplot__ = True

            fnOldScatter = axCurrent.scatter

            def fnNewScatter(x, y, *args, **kwargs):
                collection = fnOldScatter(x, y, *args, **kwargs)

                def ftupleGetData():
                    return Quantity(x), Quantity(y)

                ftupleGetData.__vplot__ = True

                collection.get_data = ftupleGetData

                return collection

            axCurrent.scatter = fnNewScatter

        # TODO: Override ax.imshow as well so we can
        # automatically add units to colorbars.

    def fnAddLabels(self):

        # Get the labels for each axis
        for iK, axCurrent in enumerate(self.axes):

            # Skip if there's no data to parse
            if len(axCurrent.lines) == 0 and len(axCurrent.collections) == 0:
                continue

            # Check if there are labels already
            bXlabelExists = not (
                axCurrent.get_xlabel() is None or axCurrent.get_xlabel() == ""
            )
            bYlabelExists = not (
                axCurrent.get_ylabel() is None or axCurrent.get_ylabel() == ""
            )
            bLegendExists = axCurrent.get_legend() is not None

            # Skip if the user already set these
            if bXlabelExists and bYlabelExists and bLegendExists:
                continue

            # Get info on all lines in the axis
            listXunits = []
            listXlabels = []
            listXtypes = []
            listYunits = []
            listYlabels = []
            listYtypes = []
            listBodies = []
            listLines = [
                line
                for line in axCurrent.lines + axCurrent.collections
                if hasattr(line, "get_data")
            ]
            for line in listLines:

                # Get the data
                x, y = line.get_data()

                # Grab the x metadata
                sUnit, _, sLabel, sPhysicalType = ftupleGetArrayInfo(
                    x, self.max_label_length
                )
                listXunits.append(sUnit)
                listXlabels.append(sLabel)
                listXtypes.append(sPhysicalType)

                # Grab the y metadata
                sUnit, sBody, sLabel, sPhysicalType = ftupleGetArrayInfo(
                    y, self.max_label_length
                )
                listYunits.append(sUnit)
                listYlabels.append(sLabel)
                listYtypes.append(sPhysicalType)
                listBodies.append(sBody)

            # Figure out the x physical type
            if len(set(listXtypes)) == 0:
                sXtype = None
            elif len(set(listXtypes)) == 1:
                sXtype = listXtypes[0]
            elif len(set(listXtypes)) == 2 and None in listXtypes:
                # Allow unitless quantities to be shown on the same
                # axis as unitful quantities, since matplotlib.units allows it
                sXtype = [sXtype for sXtype in listXtypes if sXtype is not None][0]
            else:
                raise ValueError(
                    "Axis #{} contains quantities with different physical types: {}".format(
                        iK + 1, ", ".join(listXtypes)
                    )
                )

            # Figure out the y physical type
            if len(set(listYtypes)) == 0:
                sYtype = None
            elif len(set(listYtypes)) == 1:
                sYtype = listYtypes[0]
            elif len(set(listYtypes)) == 2 and None in listYtypes:
                # Allow unitless quantities to be shown on the same
                # axis as unitful quantities, since matplotlib.units allows it
                sYtype = [sYtype for sYtype in listYtypes if sYtype is not None][0]
            else:
                raise ValueError(
                    "Axis #{} contains quantities with different physical types: {}".format(
                        iK + 1, ", ".join(listYtypes)
                    )
                )

            # Figure out the x unit
            if len(set(listXunits)) == 0:
                sXunit = None
            elif len(set(listXunits)) == 1:
                if listXunits[0] is None:
                    sXunit = None
                else:
                    sXunit = str(listXunits[0])
            elif len(set(listXunits)) > 1:
                sXunit = None
                for sXunit in set(listXunits):
                    if sXunit is not None:
                        # A hacky way to figure out the actual unit
                        if axCurrent.convert_xunits(1 * u.Unit(sXunit)) == 1:
                            break

            # Figure out the y unit
            if len(set(listYunits)) == 0:
                sYunit = None
            elif len(set(listYunits)) == 1:
                if listYunits[0] is None:
                    sYunit = None
                else:
                    sYunit = str(listYunits[0])
            elif len(set(listYunits)) > 1:
                sYunit = None
                for sYunit in set(listYunits):
                    if sYunit is not None:
                        # A hacky way to figure out the actual unit
                        if axCurrent.convert_yunits(1 * u.Unit(sYunit)) == 1:
                            break

            # Are we dealing with single bodies/quantity types?
            bSingleBody = len(set(listBodies)) == 1 and listBodies[0] is not None
            bSingleXparam = len(set(listXlabels)) == 1 and listXlabels[0] is not None
            bSingleYparam = len(set(listYlabels)) == 1 and listYlabels[0] is not None

            # Skip auto-labeling on inner axes of shared-axis layouts
            bInnerXaxis = False
            bInnerYaxis = False
            try:
                subplotSpec = axCurrent.get_subplotspec()
                xSiblings = axCurrent.get_shared_x_axes().get_siblings(
                    axCurrent
                )
                if not subplotSpec.is_last_row() and len(xSiblings) > 1:
                    bInnerXaxis = True
                ySiblings = axCurrent.get_shared_y_axes().get_siblings(
                    axCurrent
                )
                if not subplotSpec.is_first_col() and len(ySiblings) > 1:
                    bInnerYaxis = True
            except AttributeError:
                pass  # Not a subplot (e.g., inset axes)

            # Add the x axis label
            if not bXlabelExists and not bInnerXaxis:

                sXlabel = ""

                if bSingleXparam:
                    sXlabel += "{}".format(listXlabels[0])
                elif sXtype is not None:
                    sXlabel += "{}".format(sXtype)

                if sXunit is not None:
                    sXlabel += " [{}]".format(sXunit)

                if sXlabel.endswith(": "):
                    sXlabel = sXlabel[:-2]

                axCurrent.set_xlabel(sXlabel)

            # Add the y axis label
            if not bYlabelExists and not bInnerYaxis:

                sYlabel = ""

                if bSingleBody:
                    sYlabel += "{}: ".format(listBodies[0])

                if bSingleYparam:
                    sYlabel += "{}".format(listYlabels[0])
                elif sYtype is not None:
                    sYlabel += "{}".format(sYtype)

                if sYunit is not None:
                    sYlabel += " [{}]".format(sYunit)

                if sYlabel.endswith(": "):
                    sYlabel = sYlabel[:-2]

                axCurrent.set_ylabel(sYlabel)

            # Add the legend
            if self.auto_legend and not bLegendExists:

                bMakeLegend = False

                for iJ, line in enumerate(listLines):
                    if (
                        line.get_label() is None
                        or line.get_label() == ""
                        or line.get_label().startswith("_line")
                        or line.get_label().startswith("_collection")
                        or line.get_label().startswith("_child")
                    ):

                        sLabel = ""

                        if not bSingleBody and listBodies[iJ] is not None:
                            sLabel += "{}: ".format(listBodies[iJ])

                        if not bSingleYparam:
                            if listYlabels[iJ] is not None:
                                sLabel += "{}".format(listYlabels[iJ])

                        if sLabel.endswith(": "):
                            sLabel = sLabel[:-2]

                        if sLabel != "":
                            line.set_label(sLabel)
                            bMakeLegend = True

                if bMakeLegend:
                    axCurrent.legend(loc="best")

    def fnFormatAxes(self):
        for axCurrent in self.axes:

            # Force time axis margins to be zero
            if "Time" in axCurrent.get_xlabel():
                axCurrent.margins(0, axCurrent.margins()[1])

            # Make axes logarithmic?
            if self.xlog:
                axCurrent.set_xscale("log")
            if self.ylog:
                axCurrent.set_yscale("log")

    def draw(self, *args, **kwargs):
        if self._update_on_draw:
            self.fnAddLabels()
            self.fnFormatAxes()
            self.tight_layout()
            self._update_on_draw = False
        super().draw(*args, **kwargs)


# Override Figure globally to enable automatic labeling.
matplotlib.figure.Figure = VPLOTFigure

# Override plt.figure since its default kwarg for FigureClass is
# matplotlib.figure.Figure. This default value is parsed on import,
# so if the user imported pyplot before vplot, the default figure
# class will still be the old one.
fnMplFigure = matplotlib.pyplot.figure


def fnFigureWrapper(*args, FigureClass=VPLOTFigure, **kwargs):
    return fnMplFigure(*args, FigureClass=VPLOTFigure, **kwargs)


matplotlib.pyplot.figure = fnFigureWrapper
