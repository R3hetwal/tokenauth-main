# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Test'
copyright = '2023, RB'
author = 'RB'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# import os
# import sys
# sys.path.insert(0, os.path.abspath('home/WINDOWS_10_RB/NAXA/tokenauth-main-master/test/'))
import os
import sys

sys.path.insert(0, os.path.abspath('..'))


extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
# Add 'members' to autodoc_default_flags
autodoc_default_flags = ['members']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
exclude_tree = {
    'api': 'api',
    'core': 'core',
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
