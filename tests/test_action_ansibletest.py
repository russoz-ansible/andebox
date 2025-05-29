# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import pytest

from .utils import AndeboxTestHelper
from .utils import load_test_cases
from .utils import verify_patterns


TEST_CASES = load_test_cases(
    yaml_content="""
- id: cg-sanity
  input:
    repo: https://github.com/ansible-collections/community.general.git
    argv:
      - -R
      - --
      - sanity
      - --docker
      - default
      - plugins/module_utils/deps.py
  expected: {}

- id: cg-unit
  input:
    repo: https://github.com/ansible-collections/community.general.git
    argv:
      - "--"
      - "units"
      - "--docker"
      - "default"
      - "tests/unit/plugins/module_utils/test_cmd_runner.py"
  expected: {}

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
#   expected: {}

- id: ac-sanity-ei
  input:
    repo: https://github.com/ansible/ansible.git
    argv:
      - "-ei"
      - "--"
      - "sanity"
      - "--docker"
      - "default"
      - "--skip-test"
      - "release-names"
      - "lib/ansible/modules/dnf5.py"
  exception:
    class: AndeboxException
  expected:
    in_stdout: >
      ERROR: lib/ansible/modules/dnf5.py:0:0: parameter-invalid: Argument 'expire-cache' in argument_spec is not a valid python identifier
  flags:
    skip_py: ["3.9", "3.10"]
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_test(git_repo, testcase, run_andebox, save_fixtures):
    def setup_test(tc_input):
        repo = tc_input["repo"]
        repo_dir = git_repo(repo)
        return {"basedir": repo_dir}

    def executor(data):
        return {"andebox": run_andebox(["test"] + testcase.input["argv"])}

    test = AndeboxTestHelper(
        testcase, save_fixtures(), setup_test, executor, verify_patterns
    )
    test.execute()
