# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import pytest

from .utils import AndeboxTestHelper
from .utils import load_test_cases


TEST_CASES = load_test_cases(
    yaml_content=r"""
- id: cg-context
  input:
    repo: https://github.com/ansible-collections/community.general.git
  output:
    rc: 0
    in_stdout:
      - "^\\s+Type: ContextType\\.COLLECTION"
      - "^\\s+Collection: community\\.general \\d+\\.\\d+\\.\\d+"

- id: ac-context
  input:
    repo: https://github.com/ansible/ansible.git
  output:
    rc: 0
    in_stdout:
      - "^\\s+Type: ContextType\\.ANSIBLE_CORE"
  flags:
    skip_py: ["3.9", "3.10"]
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_context_action(git_repo, testcase, run_andebox, capfd, request):
    """Test the context action using the AndeboxTestHelper class."""

    # Check any flags like xfail or skip_py
    AndeboxTestHelper.check_flags(testcase, request)

    # Define the setup function specific to this test
    def setup_test(tc):
        repo = tc.input["repo"]
        return git_repo(repo)

    # Create the AndeboxTestHelper instance
    test = AndeboxTestHelper(testcase, capfd)

    # Run the setup phase
    repo_dir = test.setup(setup_test)

    # Execute the andebox context command
    captured = test.execute(run_andebox, repo_dir, ["context"])

    # Verify the patterns in the output
    test.verify_patterns(captured)

    # Verify the return code
    test.verify_return_code()
