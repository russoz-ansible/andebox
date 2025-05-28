# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import pytest

from .utils import AndeboxTestHelper
from .utils import load_test_cases

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
  output: {}

- id: cg-unit
  input:
    repo: https://github.com/ansible-collections/community.general.git
    argv:
      - "--"
      - "units"
      - "--docker"
      - "default"
      - "tests/unit/plugins/module_utils/test_cmd_runner.py"
  output: {}

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
#   output: {}

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
  output:
    in_stdout: >
      ERROR: lib/ansible/modules/dnf5.py:0:0: parameter-invalid: Argument 'expire-cache' in argument_spec is not a valid python identifier
  flags:
    skip_py: ["3.9", "3.10"]
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_ansibletest_with_testcase(git_repo, testcase, run_andebox, capfd, request):
    AndeboxTestHelper.check_flags(testcase, request)

    def setup_test(tc):
        repo = tc.input["repo"]
        repo_dir = git_repo(repo)
        return repo_dir

    test = AndeboxTestHelper(testcase, capfd)
    repo_dir = test.setup(setup_test)
    captured = test.execute(run_andebox, repo_dir, ["test"] + testcase.input["argv"])
    test.verify_patterns(captured)
    test.verify_return_code()
