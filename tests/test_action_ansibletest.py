# -*- coding: utf-8 -*-
# Copyright (c) 2024, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import pytest

from .utils import GIT_REPO_AC
from .utils import GIT_REPO_CG
from .utils import load_test_cases
from .utils import verify_patterns
from .utils import verify_return_code

TEST_CASES = load_test_cases(
    yaml_content=f"""
- id: cg-sanity
  input:
    repo: {GIT_REPO_CG}
    argv:
      - -R
      - --
      - sanity
      - --docker
      - default
      - plugins/module_utils/deps.py
  expected: {{}}

- id: cg-unit
  input:
    repo: {GIT_REPO_CG}
    argv:
      - "--"
      - "units"
      - "--docker"
      - "default"
      - "tests/unit/plugins/module_utils/test_cmd_runner.py"
  expected: {{}}

# - id: cg-unit-no-req
#   input:
#     repo: https://github.com/ansible-collections/community.general.git
#     argv:
#       - "-R"
#       - "--"
#       - "units"
#       - "--docker"
#       - "default"
#       - "tests/unit/plugins/module_utils/test_cmd_runner.py"
#   expected: {{}}

- id: ac-sanity-ei
  input:
    repo: {GIT_REPO_AC}
    argv:
      - "-ei"
      - "--"
      - "sanity"
      - "--docker"
      - "default"
      - "--skip-test"
      - "release-names"
      - "lib/ansible/modules/dnf5.py"
  expected:
    rc: 1
    in_stdout: >
      ERROR: lib/ansible/modules/dnf5.py:0:0: parameter-invalid: Argument 'expire-cache' in argument_spec is not a valid python identifier
  flags:
    skip_py: ["3.9", "3.10"]
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_test(make_helper, git_repo, testcase, run_andebox, save_fixtures):
    def executor(tc_input, data):
        return {"rc": run_andebox(["test"] + tc_input["argv"])}

    test = make_helper(
        testcase,
        git_repo,
        executor,
        [verify_patterns, verify_return_code],
    )
    test.execute()


# code: language=python tabSize=4
