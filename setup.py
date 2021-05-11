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
        "numpy>=1.19.4",
        "matplotlib>=3.4.2",
        "astropy>=4.2.1",
        # "vplanet",  # TODO! Add this in production
    ],
    entry_points={
        "console_scripts": ["vplot=vplot.command_line:_entry_point"]
    },
    zip_safe=False,
)
