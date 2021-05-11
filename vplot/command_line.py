from . import auto_plot
import argparse


def _entry_point():
    parser = argparse.ArgumentParser(prog="vplot", add_help=True)
    parser.add_argument(
        "-g",
        "--group",
        default="param",
        help="What to group plots by (param | type | none)",
    )
    parser.add_argument(
        "-b", "--bodies", nargs="*", default=[], help="Which bodies to plot",
    )
    parser.add_argument(
        "-p",
        "--params",
        nargs="*",
        default=[],
        help="Which parameters to plot",
    )
    parser.add_argument(
        "--xlog", action="store_true", help="Logarithmic x axes?"
    )
    parser.add_argument(
        "--ylog", action="store_true", help="Logarithmic y axes?"
    )
    parser.add_argument(
        "--figsize",
        nargs=2,
        type=int,
        default=None,
        help="Figure size in inches",
    )
    args = parser.parse_args()
    auto_plot(**args.__dict__)
