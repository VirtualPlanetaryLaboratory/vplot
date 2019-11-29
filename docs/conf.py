# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "vplot"
copyright = "2019, Rodrigo Luger"
author = "Rodrigo Luger"

# The full version, including alpha/beta/rc tags
release = "0.4.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "matplotlib.sphinxext.plot_directive",
    "nbsphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "notebooks/examples/*",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension settings ------------------------------------------------------

# Get current git branch
branch = os.getenv("GHBRANCH", "master")

# Add a heading to notebooks
nbsphinx_prolog = """
{%s set docname = env.doc2path(env.docname, base=None) %s}
.. note:: This tutorial was generated from a Jupyter notebook that can be
          downloaded `here <https://github.com/VirtualPlanetaryLaboratory/vplot/blob/%s/{{ docname }}>`_.
""" % (
    "%",
    "%",
    branch,
)
nbsphinx_prompt_width = 0
nbsphinx_timeout = 600
napoleon_use_ivar = True
todo_include_todos = True
autosummary_generate = True
autodoc_docstring_signature = True

# Copy the logo over
import shutil

shutil.copy("vplot.svg", "_build/html/vplot.svg")
