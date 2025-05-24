# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import re
import subprocess
import sys

import pytest

GIT_REPO_CG = "https://github.com/ansible-collections/community.general.git"
GIT_REPO_AC = "https://github.com/ansible/ansible.git"


TEST_CASES = [
    dict(
        id="cg-context",
        input=dict(
            repo=GIT_REPO_CG,
        ),
        output=dict(
            rc=0,
            in_stdout=[
                r"^\s+Type: ContextType.COLLECTION",
                r"^\s+Collection: community.general \d+\.\d+\.\d+",
            ],
        ),
    ),
    dict(
        id="ac-context",
        skip_py={"3.9", "3.10"},
        input=dict(
            repo=GIT_REPO_AC,
        ),
        output=dict(
            rc=0,
            in_stdout=[
                r"^\s+Type: ContextType.ANSIBLE_CORE",
            ],
        ),
    ),
]
TEST_CASES_IDS = [item["id"] for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_ansibletest(git_repo, testcase):
    repo = testcase["input"]["repo"]
    repo_dir = git_repo(repo)

    skip_py = testcase.get("skip_py")
    if skip_py and f"{sys.version_info.major}.{sys.version_info.minor}" in skip_py:
        pytest.skip("Unsupported python version")

    proc = subprocess.run(
        ["andebox", "context"],
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
    rc = testcase["output"].get("rc", 0)
    assert proc.returncode == rc, f"Unexpected return code! {msg}"
    patt_outs = testcase["output"].get("in_stdout", [])
    for patt_out in patt_outs:
        print(f"{patt_out=}")
        match = re.search(patt_out, proc.stdout, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_out}) not found in stdout! {msg}"
    patt_errs = testcase["output"].get("in_stderr", [])
    for patt_err in patt_errs:
        print(f"{patt_err=}")
        match = re.search(patt_err, proc.stderr, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_err}) not found in stderr! {msg}"
