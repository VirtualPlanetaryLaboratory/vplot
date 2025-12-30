# -*- coding: utf-8 -*-
import vplot
import matplotlib
import matplotlib.figure
import os
import pytest


# Non-interactive
matplotlib.use("Agg")


# Get the path to the example
path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "docs",
    "notebooks",
    "examples",
    "CircumbinaryOrbit",
)


def test_autplot():
    """Test basic auto_plot execution."""
    figs = vplot.flistAutoPlot(path, bShow=False)
    assert isinstance(figs, list)
    assert len(figs) > 0
    for fig in figs:
        matplotlib.pyplot.close(fig)


def test_autoplot_return_values():
    """Test that auto_plot returns correct number and type of figures."""
    figs = vplot.flistAutoPlot(path, bShow=False)

    # Should return multiple figures
    assert isinstance(figs, list)
    assert len(figs) > 0

    # Each should be a matplotlib figure
    for fig in figs:
        assert isinstance(fig, matplotlib.figure.Figure)
        matplotlib.pyplot.close(fig)


def test_autoplot_group_type():
    """Test grouping plots by physical type."""
    figs = vplot.flistAutoPlot(path, sGroup="type", bShow=False)
    assert len(figs) > 0
    for fig in figs:
        assert isinstance(fig, matplotlib.figure.Figure)
        matplotlib.pyplot.close(fig)


def test_autoplot_group_param():
    """Test grouping plots by parameter name."""
    figs = vplot.flistAutoPlot(path, sGroup="param", bShow=False)
    assert len(figs) > 0
    for fig in figs:
        assert isinstance(fig, matplotlib.figure.Figure)
        matplotlib.pyplot.close(fig)


def test_autoplot_group_none():
    """Test individual plots for each parameter."""
    figs = vplot.flistAutoPlot(path, sGroup="none", bShow=False)
    assert len(figs) > 0
    for fig in figs:
        assert isinstance(fig, matplotlib.figure.Figure)
        matplotlib.pyplot.close(fig)


def test_autoplot_filter_bodies():
    """Test filtering by body names."""
    figs = vplot.flistAutoPlot(path, listBodies=["cbp"], bShow=False)
    assert len(figs) > 0

    # Check that only cbp data is plotted (legends should only contain cbp)
    for fig in figs:
        for ax in fig.axes:
            legend = ax.get_legend()
            if legend is not None:
                legend_texts = [t.get_text() for t in legend.get_texts()]
                # If there are body names in legend, should only be cbp
                for text in legend_texts:
                    if "earth" in text.lower():
                        pytest.fail(f"Found 'earth' in legend when filtering for cbp only: {text}")
        matplotlib.pyplot.close(fig)


def test_autoplot_filter_params():
    """Test filtering by parameter names."""
    figs = vplot.flistAutoPlot(path, listParams=["Eccentricity"], bShow=False)
    assert len(figs) > 0

    # All figures should be for Eccentricity
    for fig in figs:
        for ax in fig.axes:
            ylabel = ax.get_ylabel()
            # Y-label should contain "Eccentricity"
            assert "Eccentricity" in ylabel or ylabel == ""
        matplotlib.pyplot.close(fig)


def test_autoplot_invalid_group():
    """Test that invalid group raises assertion error."""
    with pytest.raises(AssertionError, match="must be one of"):
        vplot.flistAutoPlot(path, sGroup="invalid", bShow=False)


def test_autoplot_xlog():
    """Test xlog parameter."""
    figs = vplot.flistAutoPlot(path, xlog=True, bShow=False)
    assert len(figs) > 0

    # Trigger formatting by calling draw (which calls _format_axes)
    fig = figs[0]
    fig.canvas.draw()

    # Check first figure has log x-axis
    assert fig.axes[0].get_xscale() == "log"

    for fig in figs:
        matplotlib.pyplot.close(fig)


def test_autoplot_ylog():
    """Test ylog parameter."""
    figs = vplot.flistAutoPlot(path, ylog=True, bShow=False)
    assert len(figs) > 0

    # Trigger formatting by calling draw (which calls _format_axes)
    fig = figs[0]
    fig.canvas.draw()

    # Check first figure has log y-axis
    assert fig.axes[0].get_yscale() == "log"

    for fig in figs:
        matplotlib.pyplot.close(fig)


def test_autoplot_figsize():
    """Test custom figure size."""
    figs = vplot.flistAutoPlot(path, figsize=(10, 8), bShow=False)
    assert len(figs) > 0

    # Check first figure has correct size
    fig = figs[0]
    size = fig.get_size_inches()
    assert size[0] == 10
    assert size[1] == 8

    for fig in figs:
        matplotlib.pyplot.close(fig)


def test_autoplot_bodies_string_converted():
    """Test that bodies parameter accepts a string and converts to list."""
    # auto_plot automatically converts strings to lists, so this should work
    figs = vplot.flistAutoPlot(path, listBodies="cbp", bShow=False)
    assert len(figs) > 0
    for fig in figs:
        matplotlib.pyplot.close(fig)


def test_autoplot_params_string_converted():
    """Test that params parameter accepts a string and converts to list."""
    # auto_plot automatically converts strings to lists, so this should work
    figs = vplot.flistAutoPlot(path, listParams="Eccentricity", bShow=False)
    assert len(figs) > 0
    for fig in figs:
        matplotlib.pyplot.close(fig)


def test_autoplot_no_params_found():
    """Test error when no parameters match the filter."""
    with pytest.raises(RuntimeError, match="No parameters found for plotting"):
        vplot.flistAutoPlot(path, listParams=["NonExistentParameter"], bShow=False)


def test_autoplot_show_true():
    """Test auto_plot with bShow=True (mock plt.show)."""
    from unittest.mock import patch
    with patch('matplotlib.pyplot.show'):
        # This should not return anything when bShow=True
        result = vplot.flistAutoPlot(path, sGroup="param", bShow=True)
        assert result is None


def test_main_module():
    """Test that __main__.py works."""
    import subprocess
    import sys
    result = subprocess.run(
        [sys.executable, "-m", "vplot", "--help"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=os.path.join(os.path.dirname(os.path.dirname(__file__)))
    )
    # Should work now that __main__.py exists
    assert result.returncode == 0
