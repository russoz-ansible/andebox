# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import pytest
from tests.utils import validate_stdout

from .utils import GIT_REPO_CG
from .utils import load_test_cases
from .utils import verify_patterns


TEST_CASES = load_test_cases(
    f"""
- id: basic
  input:
    repo: {GIT_REPO_CG}
    args:
      - ignores
  expected:
    in_stdout: "tests/unit/plugins/modules/test_gio_mime.yaml no-smart-quotes"
- id: specific-version
  input:
    repo: {GIT_REPO_CG}
    args:
      - ignores
      - -s
      - "2.19"
      - -H-5
  expected:
    in_stdout: "1  tests/unit/plugins/modules/test_gio_mime.yaml no-smart-quotes"
    stdout_line_count: 5
- id: specific-version-and-file
  input:
    repo: {GIT_REPO_CG}
    args:
      - ignores
      - -s
      - "2.19"
      - -H-5
      - -ff
      - test_gio_mime
  expected:
    in_stdout: "1  tests/unit/plugins/modules/test_gio_mime.yaml no-smart-quotes"
    stdout_line_count: 1
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_ignores(make_helper, git_repo, testcase, run_andebox):
    test = make_helper(
        testcase, git_repo, run_andebox, [verify_patterns, validate_stdout]
    )
    test.run()
