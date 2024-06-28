# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os

from andeboxlib.cli import run


def test_sanity(monkeypatch, git_repo):
    repo = "https://github.com/ansible-collections/community.general.git"
    repo_dir = git_repo(repo)

    try:
        os.chdir(next(repo_dir))
        monkeypatch.setattr(
            "sys.argv",
            [
                "andebox",
                "test",
                "--",
                "sanity",
                "--docker",
                "default",
                "plugins/module_utils/deps.py",
            ],
        )
        run()
    finally:
        next(repo_dir, None)


def test_unit(monkeypatch, git_repo):
    repo = "https://github.com/ansible-collections/community.general.git"
    repo_dir = git_repo(repo)

    try:
        os.chdir(next(repo_dir))
        monkeypatch.setattr(
            "sys.argv",
            [
                "andebox",
                "test",
                "--",
                "units",
                "--docker",
                "default",
                "--python",
                "3.11",
                "tests/unit/plugins/module_utils/test_cmd_runner.py",
            ],
        )
        run()
    finally:
        next(repo_dir, None)
