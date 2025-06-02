# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# Copyright (c) 2024, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import pytest

from .utils import load_test_cases
from .utils import verify_patterns

TEST_CASES = load_test_cases(
    yaml_content=r"""
- id: cg-context
  input:
    args: [context]
    repo: https://github.com/ansible-collections/community.general.git
  expected:
    rc: 0
    in_stdout:
      - "^\\s+Type: ContextType\\.COLLECTION"
      - "^\\s+Collection: community\\.general \\d+\\.\\d+\\.\\d+"

- id: ac-context
  input:
    args: [context]
    repo: https://github.com/ansible/ansible.git
  expected:
    rc: 0
    in_stdout:
      - "^\\s+Type: ContextType\\.ANSIBLE_CORE"
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_context(git_repo, testcase, run_andebox, make_helper):

    test = make_helper(
        testcase,
        git_repo,
        run_andebox,
        [verify_patterns],
    )
    test.execute()
