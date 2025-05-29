# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import pytest

from .utils import AndeboxTestHelper
from .utils import load_test_cases
from .utils import verify_patterns

TEST_CASES = load_test_cases(
    yaml_content=r"""
- id: cg-context
  input:
    repo: https://github.com/ansible-collections/community.general.git
  expected:
    rc: 0
    in_stdout:
      - "^\\s+Type: ContextType\\.COLLECTION"
      - "^\\s+Collection: community\\.general \\d+\\.\\d+\\.\\d+"

- id: ac-context
  input:
    repo: https://github.com/ansible/ansible.git
  expected:
    rc: 0
    in_stdout:
      - "^\\s+Type: ContextType\\.ANSIBLE_CORE"
  flags:
    skip_py: ["3.9", "3.10"]
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_context(git_repo, testcase, run_andebox, save_fixtures):

    test = AndeboxTestHelper(
        testcase,
        save_fixtures(),
        lambda tc_input: {"basedir": git_repo(tc_input["repo"])},
        lambda data: {"andebox": run_andebox(["context"])},
        [verify_patterns],
    )
    test.execute()
