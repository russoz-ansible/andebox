# -*- coding: utf-8 -*-
# (c) 2025, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import shutil
import subprocess
import sys
from pathlib import Path


def test_tox_docs_runs():
    # Always run from project root
    project_root = Path(__file__).resolve().parent.parent
    build_dir = project_root / "docs" / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    # Run sphinx-build from project root
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"],
        capture_output=True,
        text=True,
        cwd=str(project_root),
    )
    assert (
        result.returncode == 0
    ), f"sphinx-build failed: {result.stderr}\n{result.stdout}"
    assert (
        "build succeeded" in result.stdout.lower()
    ), f"Sphinx did not report successful build: {result.stdout}"
    index_html = build_dir / "html" / "index.html"
    assert index_html.exists(), "index.html was not generated in docs/_build/html/"
