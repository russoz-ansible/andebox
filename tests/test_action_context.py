# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import re
import sys

import pytest

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
def test_ansibletest(git_repo, testcase, run_andebox, capfd, request):
    if "xfail" in testcase.flags:
        request.node.add_marker(
            pytest.mark.xfail(
                reason=testcase.flags["xfail"],
                strict=False,
                run=True,
            )
        )

    skip_py = testcase.flags.get("skip_py", [])
    if f"{sys.version_info.major}.{sys.version_info.minor}" in skip_py:
        pytest.skip("Unsupported python version")

    repo = testcase.input["repo"]
    repo_dir = git_repo(repo)

    print(f"\nRunning andebox context for {testcase.id}...")
    captured = capfd.readouterr()  # Clear any output from setup

    run_andebox(repo_dir, ["context"])

    captured = capfd.readouterr()

    msg = f"stdout=\n" f"{captured.out}\n\nstderr=\n" f"{captured.err}"
    patt_outs = testcase.output.get("in_stdout", [])
    for patt_out in patt_outs:
        print(f"{patt_out=}")
        match = re.search(patt_out, captured.out, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_out}) not found in stdout! {msg}"
    patt_errs = testcase.output.get("in_stderr", [])
    for patt_err in patt_errs:
        print(f"{patt_err=}")
        match = re.search(patt_err, captured.err, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_err}) not found in stderr! {msg}"
