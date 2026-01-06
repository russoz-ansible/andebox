# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import pytest

from .utils import GIT_REPO_AC
from .utils import GIT_REPO_CG
from .utils import load_test_cases
from .utils import verify_patterns
from .utils import verify_return_code

TEST_CASES = load_test_cases(
    f"""
- id: cg-sanity
  input:
    repo: {GIT_REPO_CG}
    args:
      - test
      - --
      - sanity
      - --docker
      - default
      - plugins/module_utils/deps.py
  expected: {{}}

- id: cg-sanity-with-requirements-arg
  input:
    repo: {GIT_REPO_CG}
    args:
      - test
      - -R
      - --
      - sanity
      - --docker
      - default
      - plugins/module_utils/deps.py
  expected:
    rc: 2
    in_stderr: >-
      andebox: error: --skip-requirements/-R cannot be used with 'sanity' test

- id: cg-unit
  input:
    repo: {GIT_REPO_CG}
    args:
      - test
      - --
      - units
      - --docker
      - default
      - --python
      - "3.11"
      - tests/unit/plugins/module_utils/test_cmd_runner.py
  expected: {{}}

- id: cg-unit-with-ei-arg
  input:
    repo: {GIT_REPO_CG}
    args:
      - test
      - -ei
      - --
      - units
      - --docker
      - default
      - --python
      - "3.11"
      - tests/unit/plugins/module_utils/test_cmd_runner.py
  expected:
    rc: 2
    in_stderr: >-
      andebox: error: --exclude-from-ignore/-ei can only be used with 'sanity' test

- id: cg-unit-no-req
  input:
    repo: https://github.com/ansible-collections/community.general.git
    args:
      - test
      - -R
      - --
      - units
      - --docker
      - default
      - --python
      - "3.11"
      - tests/unit/plugins/modules/test_xfconf.py
  expected:
    rc: 1
    in_stdout: >
      ModuleNotFoundError: No module named 'ansible_collections.community.internal_test_tools'

- id: ac-sanity-ei
  flags:
    skip_py:
      - "3.11"
  input:
    repo: {GIT_REPO_AC}
    args:
      - test
      - -ei
      - --
      - sanity
      - --docker
      - default
      - --skip-test
      - release-names
      - lib/ansible/modules/dnf5.py
  expected:
    rc: 1
    in_stdout: >
      ERROR: lib/ansible/modules/dnf5.py:0:0: parameter-invalid: Argument 'expire-cache' in argument_spec is not a valid python identifier

- id: cg-sanity-exclude-ignore
  input:
    repo: https://github.com/ansible-collections/community.general.git
    args:
      - test
      - --exclude-from-ignore
      - --
      - sanity
      - --docker
      - default
      - plugins/modules/iptables_state.py
  expected:
    rc: 1
    in_stdout: >-
      ERROR: plugins/modules/iptables_state.py:0:0: undocumented-parameter:
      Argument '_back' is listed in the argument_spec, but not documented in the module documentation
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_test(make_helper, git_repo, testcase, run_andebox):
    test = make_helper(
        testcase,
        git_repo,
        run_andebox,
        [verify_patterns, verify_return_code],
    )
    test.run()
