# -*- coding: utf-8 -*-
# code: language=python tabSize=4
import subprocess
import sys
import textwrap
from pathlib import Path

p = Path().parent / "andebox"

sys.path.insert(0, p.absolute().as_posix())
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


src = Path()
gen_dir = src / "_generated"
gen_dir.mkdir(parents=True, exist_ok=True)
out_file = gen_dir / "andebox_help.rst"
proc = subprocess.run(["andebox", "--help"], capture_output=True, text=True, check=False)
indented = textwrap.indent(proc.stdout.rstrip("\n"), "   ")
content = ".. code-block:: text\n\n" + indented + "\n"
with open(out_file, "w", encoding="utf-8") as fh:
    fh.write(content)

from andebox.actions.noxtest import VERSION_MATRIX  # noqa: E402

all_pythons = sorted(
    set(py for _, _, pys in VERSION_MATRIX for py in pys),
    key=lambda v: tuple(int(x) for x in v.split(".")),
)

rows = [
    ".. list-table::",
    "   :header-rows: 1",
    "   :stub-columns: 1",
    "   :widths: auto",
    "",
]
rows.append("   * - ac \\\\ py")
for py in all_pythons:
    rows.append(f"     - {py}")
for ac_ver, default_py, supported_pys in VERSION_MATRIX:
    rows.append(f"   * - {ac_ver}")
    for py in all_pythons:
        if py == default_py:
            rows.append("     - default")
        elif py in supported_pys:
            rows.append("     - ✓")
        else:
            rows.append("     -")

matrix_content = "\n".join(rows) + "\n"
with open(gen_dir / "noxtest_matrix.rst", "w", encoding="utf-8") as fh:
    fh.write(matrix_content)
