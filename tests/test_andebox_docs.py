# -*- coding: utf-8 -*-
# Copyright (c) 2025, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
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


# code: language=python tabSize=4
