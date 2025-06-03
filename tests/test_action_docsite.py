# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2025 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2025 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import pytest

from .utils import GenericTestCase
from .utils import GIT_REPO_CG
from .utils import validate_stdout
from .utils import verify_patterns


@pytest.mark.slow
def test_docsite(make_helper, git_repo, run_andebox, tmp_path):

    doc_dir = tmp_path / "docsite"
    doc_dir.mkdir(parents=True, exist_ok=True)

    testcase = GenericTestCase(
        id="basic",
        input=dict(
            repo=GIT_REPO_CG,
            args=["docsite", "-d", str(doc_dir)],
        ),
        expected=dict(
            rc=0,
            in_stdout="build succeeded",
        ),
    )

    def validate_index_html(expected, data):
        index_html = doc_dir / "build" / "html" / "index.html"
        assert (
            index_html.exists()
        ), f"index.html was not generated in {doc_dir}/_build/html/"

    test = make_helper(
        testcase,
        git_repo,
        run_andebox,
        [validate_stdout, verify_patterns, validate_index_html],
    )
    test.execute()
