import matplotlib.pyplot as plt
from IPython.display import HTML
import io
import base64


class FigureGrid(object):
    """A class / object to display plots in a horizontal / flow layout below a cell.
    
    Based on https://stackoverflow.com/a/49566213
    """

    def __init__(self, figs, **kwargs):
        # string buffer for the HTML: initially some CSS; images to be appended
        self.sHtml = """
        <style>
        .floating-box {
            display: inline-block;
            margin: 3px;
            overflow: visible;
            padding: 1em;
        }
        </style>
        """

        for fig in figs:
            self.add_figure(fig, **kwargs)

    def add_figure(self, fig, width=280):
        """ Saves a PNG representation of a Matplotlib Axes object """
        Bio = io.BytesIO()  # bytes buffer for the plot
        kwargs = dict(
            left=fig.subplotpars.left,
            right=fig.subplotpars.right,
            bottom=fig.subplotpars.bottom,
            top=fig.subplotpars.top,
        )
        # Give the figure some padding
        fig.subplots_adjust(left=0.2, right=0.9, bottom=0.2, top=0.9)
        fig.canvas.print_png(Bio)  # make a png of the plot in the buffer
        # Undo the changes
        fig.subplots_adjust(**kwargs)
        # encode the bytes as string using base 64
        sB64Img = base64.b64encode(Bio.getvalue()).decode()
        self.sHtml += (
            '<div class="floating-box">'
            + '<img src="data:image/png;base64,{}\n" width="{}px">'.format(
                sB64Img, width
            )
            + "</div>"
        )

    def display(self):
        """ Final step - display the accumulated HTML """
        display(HTML(self.sHtml))
