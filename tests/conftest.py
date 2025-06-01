# -*- coding: utf-8 -*-
# Copyright (c) 2024, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import os
import subprocess
import sys
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import List

import pytest
from andebox.cli import run as cli_run
from andebox.context import AnsibleCoreContext
from andebox.context import CollectionContext
from andebox.context import ContextType
from git import Repo

from .utils import AndeboxTestHelper


@pytest.fixture(scope="session")
def git_repo(tmp_path_factory) -> Callable[[dict], dict]:
    cloned_repos = {}

    def _clone(tc_input: dict) -> dict:
        url = tc_input["repo"]
        if url in cloned_repos:
            dest = cloned_repos[url]
        else:
            repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
            dest = tmp_path_factory.mktemp(repo_name)
            print(f"Cloning {url} into {dest}")
            Repo.clone_from(url, dest, depth=1)
            cloned_repos[url] = dest
        return {"basedir": dest}

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
    ) -> int:
        mocker.patch("sys.argv", ["andebox"] + args)
        if context_type is not None:
            mock_base_dir_type = mocker.patch("andebox.context._base_dir_type")
            mock_base_dir_type.return_value = (
                AnsibleCoreContext
                if context_type == ContextType.ANSIBLE_CORE
                else CollectionContext
            )
        return cli_run()

    def _make_run_andebox(tc_input: dict, data: dict) -> dict:
        args = tc_input["args"]
        context_type = tc_input.get("andebox_context_type")
        match context_type:
            case "ansible-core":
                context_type = ContextType.ANSIBLE_CORE
            case "collection":
                context_type = ContextType.COLLECTION
            case None:
                context_type = None
            case _:
                raise ValueError(f"Unknown context type: {context_type}")
        return {"rc": _run_andebox(args, context_type)}

    return _make_run_andebox


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


@pytest.fixture
def make_helper(save_fixtures):

    def _make_helper(
        testcase,
        setup,
        executor,
        validator,
    ) -> AndeboxTestHelper:
        return AndeboxTestHelper(
            testcase,
            save_fixtures(),
            setup,
            executor,
            validator,
        )

    return _make_helper


# code: language=python tabSize=4
