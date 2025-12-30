# -*- coding: utf-8 -*-
import vplanet
import vplot
import matplotlib
import matplotlib.pyplot as plt
import os
import pytest
import numpy as np


# Non-interactive
matplotlib.use("Agg")


# Path to example directory
path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "docs",
    "notebooks",
    "examples",
    "CircumbinaryOrbit",
)

# Run vplanet (or load existing output if already run)
output = vplanet.run(os.path.join(path, "vpl.in"))


class FigureTester(object):
    def __init__(
        self, xlabel="Simulation Time [yr]", ylabel="", legend_texts=[]
    ):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.legend_texts = sorted(legend_texts)
        self.fig, self.ax = plt.subplots(1)

    def __enter__(self):
        return self.fig

    def __exit__(self, type, value, traceback):
        self.fig._add_labels()

        # Check labels and legend
        assert self.ax.get_xlabel() == self.xlabel
        assert self.ax.get_ylabel() == self.ylabel
        legend = self.ax.get_legend()
        if self.legend_texts == []:
            assert legend is None
        else:
            assert self.legend_texts == sorted(
                [t.get_text() for t in legend.get_texts()]
            )

        plt.close(self.fig)


def test_basic():
    with FigureTester(ylabel="cbp: Orbital Eccentricity",):
        plt.plot(output.cbp.Time, output.cbp.Eccentricity)


def test_unit_change():
    with FigureTester(
        xlabel="Simulation Time [Myr]", ylabel="cbp: Orbital Eccentricity",
    ):
        plt.plot(output.cbp.Time.to("Myr"), output.cbp.Eccentricity)


def test_two_quantities():
    with FigureTester(
        ylabel="cbp: angle [deg]",
        legend_texts=[
            "Longitude of ascending node",
            "Longitude of pericenter",
        ],
    ):
        plt.plot(output.cbp.Time, output.cbp.LongA)
        plt.plot(output.cbp.Time, output.cbp.LongP)


def test_two_bodies():
    with FigureTester(
        ylabel="Orbital Eccentricity", legend_texts=["cbp", "earth"],
    ):
        plt.plot(output.cbp.Time, output.cbp.Eccentricity)
        plt.plot(output.earth.Time, output.earth.Eccentricity)


def test_two_quantities_two_bodies():
    with FigureTester(
        ylabel="angle [deg]",
        legend_texts=[
            "cbp: Longitude of ascending node",
            "earth: Longitude of pericenter",
        ],
    ):
        plt.plot(output.cbp.Time, output.cbp.LongA)
        plt.plot(output.earth.Time, output.earth.LongP)


def test_degrees_radians():
    with FigureTester(
        ylabel="cbp: angle [deg]",
        legend_texts=[
            "Longitude of ascending node",
            "Longitude of pericenter",
        ],
    ):
        plt.plot(output.cbp.Time, output.cbp.LongA)
        plt.plot(output.cbp.Time, output.cbp.LongP.to("rad"))


def test_mixed_y_units():
    with FigureTester(
        ylabel="angle [deg]",
        legend_texts=["cbp: Longitude of ascending node", "angle"],
    ):
        plt.plot(output.cbp.Time, output.cbp.LongA)
        plt.plot(output.cbp.Time, np.ones(len(output.cbp.LongA)))


def test_mixed_xy_units():
    with FigureTester(
        xlabel="time [yr]",
        ylabel="angle [deg]",
        legend_texts=["cbp: Longitude of ascending node", "angle"],
    ):
        plt.plot(output.cbp.Time, output.cbp.LongA)
        plt.plot(
            np.arange(len(output.cbp.Time)), np.ones(len(output.cbp.LongA))
        )


def test_custom_labels():
    with FigureTester(
        xlabel="xlabel", ylabel="ylabel",
    ):
        plt.plot(output.cbp.Time, output.cbp.Eccentricity)
        plt.xlabel("xlabel")
        plt.ylabel("ylabel")


def test_unitless():
    with FigureTester(
        xlabel="", ylabel="",
    ):
        plt.plot(np.linspace(0, 1, 100), np.ones(100))


def test_scatter():
    """Test that scatter plots preserve metadata and generate correct labels."""
    with FigureTester(ylabel="cbp: Orbital Eccentricity"):
        plt.scatter(output.cbp.Time, output.cbp.Eccentricity)


def test_scatter_two_bodies():
    """Test scatter plots with multiple bodies."""
    with FigureTester(
        ylabel="Orbital Eccentricity", legend_texts=["cbp", "earth"]
    ):
        plt.scatter(output.cbp.Time, output.cbp.Eccentricity)
        plt.scatter(output.earth.Time, output.earth.Eccentricity)


def test_mixed_plot_scatter():
    """Test combination of plot and scatter on same axes."""
    with FigureTester(
        ylabel="Orbital Eccentricity", legend_texts=["cbp", "earth"]
    ):
        plt.plot(output.cbp.Time, output.cbp.Eccentricity)
        plt.scatter(output.earth.Time, output.earth.Eccentricity)


def test_xlog():
    """Test logarithmic x-axis."""
    fig = plt.figure(xlog=True)
    ax = fig.add_subplot(111)
    ax.plot(output.cbp.Time, output.cbp.Eccentricity)
    fig._add_labels()
    fig._format_axes()  # Need to call _format_axes to apply log scale
    assert ax.get_xscale() == "log"
    assert ax.get_ylabel() == "cbp: Orbital Eccentricity"
    plt.close(fig)


def test_ylog():
    """Test logarithmic y-axis."""
    fig = plt.figure(ylog=True)
    ax = fig.add_subplot(111)
    ax.plot(output.cbp.Time, output.cbp.Eccentricity)
    fig._add_labels()
    fig._format_axes()  # Need to call _format_axes to apply log scale
    assert ax.get_yscale() == "log"
    assert ax.get_ylabel() == "cbp: Orbital Eccentricity"
    plt.close(fig)


def test_multiple_subplots():
    """Test figure with multiple subplots."""
    fig, axes = plt.subplots(2, 1)
    axes[0].plot(output.cbp.Time, output.cbp.Eccentricity)
    axes[1].plot(output.cbp.Time, output.cbp.LongA)
    fig._add_labels()

    # Both subplots get xlabels (vplot adds labels to all axes)
    assert axes[0].get_xlabel() == "Simulation Time [yr]"
    assert axes[0].get_ylabel() == "cbp: Orbital Eccentricity"
    assert axes[1].get_xlabel() == "Simulation Time [yr]"
    # When there's only one line, uses specific parameter name
    assert axes[1].get_ylabel() == "cbp: Longitude of ascending node [deg]"
    plt.close(fig)


def test_auto_legend_disabled():
    """Test that auto_legend=False prevents legend creation."""
    fig = plt.figure(auto_legend=False)
    ax = fig.add_subplot(111)
    ax.plot(output.cbp.Time, output.cbp.Eccentricity)
    ax.plot(output.earth.Time, output.earth.Eccentricity)
    fig._add_labels()

    assert ax.get_legend() is None
    plt.close(fig)


def test_max_label_length():
    """Test that max_label_length truncates long descriptions."""
    fig = plt.figure(max_label_length=10)
    ax = fig.add_subplot(111)
    ax.plot(output.cbp.Time, output.cbp.Eccentricity)
    fig._add_labels()

    # With short max_label_length, should use parameter name instead of description
    ylabel = ax.get_ylabel()
    assert "cbp" in ylabel
    assert len(ylabel) < 50  # Should be shorter than full description
    plt.close(fig)
