# -*- coding: utf-8 -*-

from setuptools import setup
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vplot"))
from vplot_version import __version__  # NOQA


def readme():
    """Get the long description from the README."""
    with open("README.rst") as f:
        return f.read()


# Setup!
setup(
    name="vplot",
    version=__version__,
    description="VPLANET Plotting Tools",
    long_description=readme(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    url="https://github.com/VirtualPlanetaryLaboratory/vplot/",
    author="Rodrigo Luger",
    author_email="rodluger@gmail.edu",
    license="MIT",
    packages=["vplot"],
    install_requires=["numpy", "matplotlib >= 3.1.1"],
    include_package_data=True,
    package_data={},
    cmdclass={},
    scripts=["bin/vplot"],
    zip_safe=False,
)
