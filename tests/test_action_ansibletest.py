# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import re
import sys

import pytest

from .utils import load_test_cases


TEST_CASES = load_test_cases(
    yaml_content="""
- id: cg-sanity
  input:
    repo: https://github.com/ansible-collections/community.general.git
    argv:
      - "--"
      - "sanity"
      - "--docker"
      - "default"
      - "plugins/module_utils/deps.py"
  output:
    rc: 0

- id: cg-unit
  input:
    repo: https://github.com/ansible-collections/community.general.git
    argv:
      - "-R"
      - "--"
      - "units"
      - "--docker"
      - "default"
      - "tests/unit/plugins/module_utils/test_cmd_runner.py"
  output:
    rc: 0

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
  output:
    exception:
      class: AndeboxException
    in_stdout: >
      ERROR: lib/ansible/modules/dnf5.py:0:0: parameter-invalid: Argument 'expire-cache' in argument_spec is not a valid python identifier
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

    print(f"\nRunning andebox test for {testcase.id}...")
    captured = capfd.readouterr()  # Clear any output from setup

    expected_exception = testcase.output.get("exception")
    if expected_exception:
        expected_class = expected_exception.get("class")
        with pytest.raises(Exception) as exc_info:
            run_andebox(repo_dir, ["test"] + testcase.input["argv"])

        actual_class = exc_info.value.__class__.__name__
        assert (
            actual_class == expected_class
        ), f"Expected exception class {expected_class}, but got {actual_class}"

        expected_value = expected_exception.get("value")
        if expected_value:
            assert expected_value in str(
                exc_info.value
            ), f"Expected exception message to contain '{expected_value}', but got: {exc_info.value}"

    else:
        run_andebox(repo_dir, ["test"] + testcase.input["argv"])

    captured = capfd.readouterr()

    msg = f"stdout=\n" f"{captured.out}\n\nstderr=\n" f"{captured.err}"
    patt_out = testcase.output.get("in_stdout")
    if patt_out:
        print(f"{patt_out=}")
        match = re.search(patt_out, captured.out, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_out}) not found in stdout! {msg}"
    patt_err = testcase.output.get("in_stderr")
    if patt_err:
        print(f"{patt_err=}")
        match = re.search(patt_err, captured.err, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_err}) not found in stderr! {msg}"
