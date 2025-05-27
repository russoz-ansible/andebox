# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import re
import subprocess
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
    rc: 1
    in_stdout: >
      ERROR: lib/ansible/modules/dnf5.py:0:0: parameter-invalid: Argument 'expire-cache' in argument_spec is not a valid python identifier
  flags:
    skip_py: ["3.9", "3.10"]
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_ansibletest(git_repo, testcase):
    skip_py = testcase.flags.get("skip_py", [])
    if f"{sys.version_info.major}.{sys.version_info.minor}" in skip_py:
        pytest.skip("Unsupported python version")

    repo = testcase.input["repo"]
    repo_dir = git_repo(repo)

    proc = subprocess.run(
        ["andebox", "test"] + testcase.input["argv"],
        cwd=repo_dir,
        check=False,
        encoding="utf-8",
        capture_output=True,
    )
    msg = (
        f"rc={proc.returncode}, stdout=\n"
        f"{proc.stdout}\n\nstderr=\n"
        f"{proc.stderr}"
    )
    rc = testcase.output.get("rc", 0)
    assert proc.returncode == rc, f"Unexpected return code! {msg}"
    patt_out = testcase.output.get("in_stdout")
    if patt_out:
        print(f"{patt_out=}")
        match = re.search(patt_out, proc.stdout, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_out}) not found in stdout! {msg}"
    patt_err = testcase.output.get("in_stderr")
    if patt_err:
        print(f"{patt_err=}")
        match = re.search(patt_err, proc.stderr, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_err}) not found in stderr! {msg}"
