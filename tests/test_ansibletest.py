# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os

import pytest
from andeboxlib.cli import run

GIT_CG = "https://github.com/ansible-collections/community.general.git"
GIT_AC = "https://github.com/ansible/ansible.git"


TEST_CASES = [
    dict(
        id="sanity",
        input=dict(
            repo=GIT_CG,
            argv=[
                "--",
                "sanity",
                "--docker",
                "default",
                "--python",
                "3.11",
                "plugins/module_utils/deps.py",
            ],
        ),
        output=dict(
            rc=0,
            in_stdout="ERROR: lib/ansible/modules/dnf5.py:0:0: parameter-invalid: Argument 'expire-cache' in argument_spec is not a valid python identifier",
        ),
    ),
    dict(
        id="unit",
        input=dict(
            repo=GIT_CG,
            argv=[
                "--",
                "units",
                "--docker",
                "default",
                "--python",
                "3.11",
                "tests/unit/plugins/module_utils/test_cmd_runner.py",
            ],
        ),
        output=dict(
            rc=0,
        ),
    ),
    dict(
        id="ei",
        input=dict(
            repo=GIT_CG,
            argv=[
                "-ei",
                "--",
                "sanity",
                "--docker",
                "default",
                "--skip-test",
                "release-names",
                "lib/ansible/modules/dnf5.py",
            ],
        ),
        output=dict(
            rc=1,
        ),
    ),
]
TEST_CASES_IDS = [item["id"] for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_andebox_test(monkeypatch, git_repo, capfd, testcase):
    repo = testcase["input"]["repo"]
    repo_dir = git_repo(repo)

    try:
        os.chdir(next(repo_dir))
        monkeypatch.setattr(
            "sys.argv",
            ["andebox", "test"] + testcase["input"]["argv"],
        )
        rc = run()

        assert rc == testcase["output"]["rc"]
    finally:
        next(repo_dir, None)
