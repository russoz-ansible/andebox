# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pytest
from andeboxlib.cli import _make_parser
from andeboxlib.cli import AndeBox
from andeboxlib.context import AnsibleCoreContext
from andeboxlib.context import CollectionContext
from andeboxlib.context import ContextType
from git import Repo


@pytest.fixture(scope="session")
def git_repo(tmp_path_factory):
    cloned_repos = {}

    def _clone(url: str) -> Path:
        if url in cloned_repos:
            return cloned_repos[url]

        repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
        dest = tmp_path_factory.mktemp(repo_name)
        print(f"Cloning {url} into {dest}")
        Repo.clone_from(url, dest, depth=1)
        cloned_repos[url] = dest
        return dest

    return _clone


# See https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
#
@pytest.fixture(scope="session", autouse=True)
def install_andebox():
    proj_dir = os.getcwd()

    print(f"{proj_dir=}")

    print("Uninstalling andebox")
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", "andebox"],
        check=True,
        encoding="utf-8",
        capture_output=True,
    )
    print("Installing andebox")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", proj_dir],
        check=True,
        encoding="utf-8",
        capture_output=True,
    )

    yield

    print("Uninstalling andebox (cleanup)")
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", "andebox"],
        check=False,
        encoding="utf-8",
        capture_output=True,
    )


@pytest.fixture
def run_andebox(mocker):

    def _run_andebox(
        args: List[str],
        context_type: ContextType | None = None,
    ) -> AndeBox:
        parser = _make_parser()
        parsed_args = parser.parse_args(args)

        if context_type is not None:
            mock_base_dir_type = mocker.patch("andeboxlib.context._base_dir_type")
            mock_base_dir_type.return_value = (
                AnsibleCoreContext
                if context_type == ContextType.ANSIBLE_CORE
                else CollectionContext
            )

        box = AndeBox(parsed_args)
        box.run()
        return box

    return _run_andebox


@pytest.fixture
def save_fixtures(request, mocker, capfd):

    def _save_fixtures(**extras) -> Dict[str, Any]:
        d = dict(
            request=request,
            mocker=mocker,
            capfd=capfd,
        )
        d.update(extras)
        return d

    return _save_fixtures
