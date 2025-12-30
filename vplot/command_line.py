from . import flistAutoPlot
import argparse


def fnEntryPoint():
    parserArgs = argparse.ArgumentParser(prog="vplot", add_help=True)
    parserArgs.add_argument(
        "-g",
        "--sGroup",
        dest="sGroup",
        default="param",
        help="What to group plots by (param | type | none)",
    )
    parserArgs.add_argument(
        "-b", "--listBodies", dest="listBodies", nargs="*", default=[], help="Which bodies to plot",
    )
    parserArgs.add_argument(
        "-p",
        "--listParams",
        dest="listParams",
        nargs="*",
        default=[],
        help="Which parameters to plot",
    )
    parserArgs.add_argument(
        "--xlog", action="store_true", help="Logarithmic x axes?"
    )
    parserArgs.add_argument(
        "--ylog", action="store_true", help="Logarithmic y axes?"
    )
    parserArgs.add_argument(
        "--figsize",
        nargs=2,
        type=int,
        default=None,
        help="Figure size in inches",
    )
    args = parserArgs.parse_args()
    flistAutoPlot(**args.__dict__)
