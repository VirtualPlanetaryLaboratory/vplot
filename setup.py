# -*- coding: utf-8 -*-
from setuptools import setup
import os


# Setup!
setup(
    name="vplot",
    description="plotting tools for vplanet",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VirtualPlanetaryLaboratory/vplot/",
    author="Rodrigo Luger",
    author_email="rodluger@gmail.edu",
    license="MIT",
    packages=["vplot"],
    include_package_data=True,
    use_scm_version={
        "write_to": os.path.join("vplot", "vplot_version.py"),
        "write_to_template": '__version__ = "{version}"\n',
    },
    install_requires=[
        "setuptools_scm>=8.0",
        "numpy>=2.0.0",
        "matplotlib>=3.9.0",
        "astropy>=6.1.0",
        "vplanet>=2.4.24",
    ],
    entry_points={
        "console_scripts": ["vplot=vplot.command_line:fnEntryPoint"]
    },
    setup_requires=["setuptools_scm"],
    zip_safe=False,
)
