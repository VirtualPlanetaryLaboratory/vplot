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
import shutil
import nbsphinx
import vplot

# -- Hacks -------------------------------------------------------------------

# PATH stuff
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))


# Hack `nbsphinx` to enable us to hide certain input cells in the
# jupyter notebooks. This works with nbsphinx==0.5.0
nbsphinx.RST_TEMPLATE = nbsphinx.RST_TEMPLATE.replace(
    "{% block input -%}",
    '{% block input -%}\n{%- if not "hide_input" in cell.metadata.tags %}',
)
nbsphinx.RST_TEMPLATE = nbsphinx.RST_TEMPLATE.replace(
    "{% endblock input %}", "{% endif %}\n{% endblock input %}"
)


# -- Project information -----------------------------------------------------

project = "vplot"
copyright = "2019, Rodrigo Luger"
author = "Rodrigo Luger"

# The full version, including alpha/beta/rc tags
release = vplot.__version__


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
    "notebooks/*_template.ipynb",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {"display_version": True}
html_last_updated_fmt = "%Y %b %d at %H:%M:%S UTC"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/hide_input.css"]


# -- Extension settings ------------------------------------------------------

# Get current git branch
branch = os.getenv("GHBRANCH", "master")

nbsphinx_prompt_width = 0
nbsphinx_timeout = 600
napoleon_use_ivar = True
todo_include_todos = True
autosummary_generate = True
autodoc_docstring_signature = True

# Copy the logo over
os.makedirs("_build/html", exist_ok=True)
shutil.copy("vplot.svg", "_build/html/vplot.svg")
