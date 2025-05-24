# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import subprocess
import sys
from pathlib import Path

import pytest
from git import Repo


@pytest.fixture(scope="session")
def git_repo(tmp_path_factory):
    """
    Clones a git repository into a temporary directory.
    Caches clones by URL so they are reused during the session.
    Returns a function that accepts a URL and returns the repo path.
    """
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
