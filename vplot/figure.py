import matplotlib
from matplotlib.figure import Figure
import astropy.units as u


class VPLOTFigure(Figure):
    """
    
    """

    def __init__(self, *args, long_labels=True, mpl_units=True, **kwargs):

        # Axes labels: name or description?
        self.long_labels = long_labels

        # Enable astropy/matplotlib quantity support?
        if mpl_units:
            from .quantity_support import quantity_support

            quantity_support()

        super().__init__(*args, **kwargs)

    def _add_labels(self):

        # Axes labels: name or description?
        if self.long_labels:
            label_type = "description"
        else:
            label_type = "name"

        # Get the labels for each axis
        for ax in self.axes:

            xlabels = []
            ylabels = []
            ytypes = []

            for line in ax.lines:

                # Get the Quantity instances for the x and y data
                x, y = line.get_data()

                # If x is a Quantity, update its label
                if hasattr(x, "unit") and hasattr(x, label_type):
                    if x.unit != u.Unit(""):
                        xlabels.append("{} [{}]".format(getattr(x, label_type), x.unit))
                    else:
                        xlabels.append("{}".format(getattr(x, label_type)))
                else:
                    xlabels.append("")

                # If y is a Quantity, update its label
                if hasattr(x, "unit") and hasattr(x, label_type):
                    if y.unit != u.Unit(""):
                        ylabels.append("{} [{}]".format(getattr(y, label_type), y.unit))
                    else:
                        ylabels.append("{}".format(getattr(y, label_type)))
                    ytypes.append(
                        "{} [{}]".format(y.unit.physical_type.title(), y.unit)
                    )
                else:
                    ylabels.append("")
                    ytypes.append("")

                # Update the label of the actual line (for the legend)
                if (
                    line.get_label() is None
                    or line.get_label() == ""
                    or line.get_label().startswith("_line")
                ):
                    line.set_label(ylabels[-1])

            # Label the x axis if no label is present
            if len(set(xlabels)) == 1 and ax.get_xlabel() == "":
                ax.set_xlabel(xlabels[0])
            elif len(set(xlabels)) > 1:
                # TODO: What should we do in this case?
                pass

            # Label the y axis if no label is present
            if len(set(ylabels)) == 1 and ax.get_ylabel() == "":
                ax.set_ylabel(ylabels[0])
            elif len(set(ylabels)) > 1:

                # See if there are any legends
                legends = [
                    c
                    for c in ax.get_children()
                    if isinstance(c, matplotlib.legend.Legend)
                ]

                # If not, add a legend
                if len(legends) == 0:
                    ax.legend(loc="best")

                # If there's no axis label, let's attempt to add one
                if ax.get_ylabel() == "":
                    if len(set(ytypes)) == 1:
                        ax.set_ylabel(ytypes[0])

    def show(self, *args, **kwargs):
        self._add_labels()
        super().show(*args, **kwargs)

    def savefig(self, *args, **kwargs):
        self._add_labels()
        super().savefig(*args, **kwargs)


# HACK
matplotlib.figure.Figure = VPLOTFigure
