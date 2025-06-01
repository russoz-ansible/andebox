# -*- coding: utf-8 -*-
# Copyright (c) 2025, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import pytest

from .utils import AndeboxTestHelper
from .utils import GIT_REPO_CG
from .utils import load_test_cases
from .utils import verify_patterns


TEST_CASES = load_test_cases(
    yaml_content=f"""
- id: basic-ignores
  input:
    repo: {GIT_REPO_CG}
    args: []
  expected:
    in_stdout: "tests/unit/plugins/modules/test_gio_mime.yaml no-smart-quotes"
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_ignorefile(git_repo, testcase, run_andebox, save_fixtures):
    def executor(data):
        return {"andebox": run_andebox(["ignores"] + testcase.input["args"])}

    test = AndeboxTestHelper(
        testcase, save_fixtures(), git_repo, executor, verify_patterns
    )
    test.execute()
