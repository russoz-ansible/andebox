# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# Copyright (c) 2025, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import pytest
from tests.utils import validate_stdout

from .utils import GIT_REPO_CG
from .utils import load_test_cases
from .utils import verify_patterns


TEST_CASES = load_test_cases(
    yaml_content=f"""
- id: basic
  input:
    repo: {GIT_REPO_CG}
    args:
      - ignores
  expected:
    in_stdout: "tests/unit/plugins/modules/test_gio_mime.yaml no-smart-quotes"
- id: specific-version
  flags:
    xfail: "Not finding ignore-2.19.txt"
  input:
    repo: {GIT_REPO_CG}
    args:
      - ignores
      - -ifs
      - "2.19"
      - -H5
  expected:
    in_stdout: "1  tests/unit/plugins/modules/test_gio_mime.yaml no-smart-quotes"
    stdout_line_count: 5
- id: specific-version-and-file
  flags:
    xfail: "Not finding ignore-2.19.txt"
  input:
    repo: {GIT_REPO_CG}
    args:
      - ignores
      - -ifs
      - "2.19"
      - -H5
      - -ff
      - test_gio_mime
  expected:
    in_stdout: "1  tests/unit/plugins/modules/test_gio_mime.yaml no-smart-quotes"
    stdout_line_count: 1
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_ignorefile(make_helper, git_repo, testcase, run_andebox):
    test = make_helper(
        testcase, git_repo, run_andebox, [verify_patterns, validate_stdout]
    )
    test.execute()
