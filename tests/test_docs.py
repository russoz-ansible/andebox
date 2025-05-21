# -*- coding: utf-8 -*-
# (c) 2025, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import shutil
import subprocess
import sys


def test_tox_docs_runs():
    """Test that the Sphinx docs build succeeds and output is as expected."""
    # Always run from project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_dir = os.path.join(project_root, "docs", "_build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    # Run sphinx-build from project root
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    assert (
        result.returncode == 0
    ), f"sphinx-build failed: {result.stderr}\n{result.stdout}"
    assert (
        "build succeeded" in result.stdout.lower()
    ), f"Sphinx did not report successful build: {result.stdout}"
    index_html = os.path.join(build_dir, "html", "index.html")
    assert os.path.exists(
        index_html
    ), "index.html was not generated in docs/_build/html/"
