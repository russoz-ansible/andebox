# -*- coding: utf-8 -*-
# Copyright (c) 2024, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import List

import pytest
from andebox.cli import _make_parser
from andebox.cli import AndeBox
from andebox.context import AnsibleCoreContext
from andebox.context import CollectionContext
from andebox.context import ContextType
from git import Repo


@pytest.fixture(scope="session")
def git_repo(tmp_path_factory) -> Callable[[str], Path]:
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
def install_andebox() -> Generator[None, None, None]:
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
            mock_base_dir_type = mocker.patch("andebox.context._base_dir_type")
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


# code: language=python tabSize=4
