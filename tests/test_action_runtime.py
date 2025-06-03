# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import pytest

from .utils import GIT_REPO_CG
from .utils import load_test_cases
from .utils import validate_stdout
from .utils import verify_patterns


TEST_CASES = load_test_cases(
    f"""
- id: basic
  input:
    repo: {GIT_REPO_CG}
    args:
      - runtime
      - --regex
      - -it
      - tombstone
      - .*
  expected:
    in_stdout: >
      T modules rax_clb_nodes: terminated in 9.0.0: This module relied on the deprecated package pyrax.
- id: redirects-endswith-y
  input:
    repo: {GIT_REPO_CG}
    args:
      - runtime
      - --regex
      - -it
      - redirect
      - y$
  expected:
    in_stdout: >
      R modules postgresql_query: redirected to community.postgresql.postgresql_query
    stdout_line_count: 4
- id: redirects-callbacks-endswith-y
  input:
    repo: {GIT_REPO_CG}
    args:
      - runtime
      - --regex
      - -it
      - redirect
      - -pt
      - callback
      - y$
  expected:
    in_stdout: >
      R callback osx_say: redirected to community.general.say
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
