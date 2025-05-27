# -*- coding: utf-8 -*-
# code: language=python tabSize=4
import os
import sys

sys.path.insert(0, os.path.abspath("../andebox"))
from andebox import __version__  # noqa: E402

project = "andebox"
copyright = "2025, Alexei Znamensky"
author = "Alexei Znamensky"
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_theme_options = {
    "navigation_with_keys": True,
    "sidebar_hide_name": False,
}
