# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import pytest
from unittest.mock import patch
import matplotlib
import matplotlib.pyplot as plt

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


def test_entry_point_function():
    """Test _entry_point function directly for code coverage."""
    from vplot.command_line import _entry_point

    # Test with --help flag (should exit)
    with patch('sys.argv', ['vplot', '--help']):
        with pytest.raises(SystemExit) as excinfo:
            _entry_point()
        assert excinfo.value.code == 0

    # Test with minimal arguments
    with patch('sys.argv', ['vplot', '-g', 'param']):
        # Change to example directory
        original_cwd = os.getcwd()
        try:
            os.chdir(path)
            # Mock show to prevent actual display
            with patch('matplotlib.pyplot.show'):
                _entry_point()
        finally:
            os.chdir(original_cwd)
            plt.close('all')


def test_entry_point_exists():
    """Test that vplot command is installed and accessible."""
    result = subprocess.run(
        ["vplot", "--help"],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0
    assert "vplot" in result.stdout.lower() or "usage" in result.stdout.lower()


def test_command_line_default():
    """Test vplot command with default arguments."""
    result = subprocess.run(
        ["vplot"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}  # Non-interactive backend
    )
    # Should execute without error
    assert result.returncode == 0


def test_command_line_group_type():
    """Test --group type argument."""
    result = subprocess.run(
        ["vplot", "-g", "type"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_group_param():
    """Test --group param argument."""
    result = subprocess.run(
        ["vplot", "-g", "param"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_group_none():
    """Test --group none argument."""
    result = subprocess.run(
        ["vplot", "-g", "none"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_bodies_filter():
    """Test --bodies argument for filtering."""
    result = subprocess.run(
        ["vplot", "-b", "cbp"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_params_filter():
    """Test --params argument for filtering."""
    result = subprocess.run(
        ["vplot", "-p", "Eccentricity"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_xlog():
    """Test --xlog argument."""
    result = subprocess.run(
        ["vplot", "--xlog"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_ylog():
    """Test --ylog argument."""
    result = subprocess.run(
        ["vplot", "--ylog"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_figsize():
    """Test --figsize argument."""
    result = subprocess.run(
        ["vplot", "--figsize", "10", "8"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    assert result.returncode == 0


def test_command_line_invalid_group():
    """Test that invalid group argument fails appropriately."""
    result = subprocess.run(
        ["vplot", "-g", "invalid"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "MPLBACKEND": "Agg"}
    )
    # Should fail with non-zero exit code
    assert result.returncode != 0
