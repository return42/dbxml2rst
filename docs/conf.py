# -*- coding: utf-8 -*-
#
# Sphinx documentation build configuration file

import re
import dbxml2rst
import sphinx_rtd_theme

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = ['_build']

project   = 'dbxml2rst'
copyright = dbxml2rst.__copyright__
version   = dbxml2rst.__version__
release   = dbxml2rst.__version__
show_authors = True

extensions = [
    'sphinx.ext.autodoc'
    , 'sphinx.ext.extlinks'
    #, 'sphinx.ext.autosummary'
    #, 'sphinx.ext.doctest'
    , 'sphinx.ext.todo'
    , 'sphinx.ext.coverage'
    #, 'sphinx.ext.pngmath'
    #, 'sphinx.ext.mathjax'
    , 'sphinx.ext.viewcode'
    , 'sphinx.ext.intersphinx'
]

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ["../utils/sphinx-static"]
html_context = {
    'css_files': [
        '_static/theme_overrides.css',
    ],
}

intersphinx_mapping = {}
