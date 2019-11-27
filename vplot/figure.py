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

        # Set the labels if they haven't been set by the user
        for ax in self.axes:
            if len(ax.lines):
                x, y = ax.lines[0].get_data()
                if ax.get_xlabel() == "":
                    if x.unit != u.Unit(""):
                        ax.set_xlabel("{} [{}]".format(getattr(x, label_type), x.unit))
                    else:
                        ax.set_xlabel("{}".format(getattr(x, label_type)))
                if ax.get_ylabel() == "":
                    if y.unit != u.Unit(""):
                        ax.set_ylabel("{} [{}]".format(getattr(y, label_type), y.unit))
                    else:
                        ax.set_ylabel("{}".format(getattr(y, label_type)))

    def show(self, *args, **kwargs):
        self._add_labels()
        super().show(*args, **kwargs)

    def savefig(self, *args, **kwargs):
        self._add_labels()
        super().savefig(*args, **kwargs)


# HACK
matplotlib.figure.Figure = VPLOTFigure
