# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from git import Repo


@pytest.fixture(scope="session")
def git_repo():
    clones = {}

    temp_dir = Path(tempfile.mkdtemp(prefix="andebox-test-tmp-repo."))

    def _shallow_clone_git_repo(repo_url):
        if repo_url not in clones:
            # Setup: Create a temporary directory
            stem = Path(repo_url).stem
            dest = str(temp_dir / stem)

            # Perform shallow clone
            print(f"Cloning repo {repo_url} => {dest}")
            Repo.clone_from(repo_url, dest, depth=1)

            # Store the path for later cleanup
            clones[repo_url] = dest

        while repo_url in clones:
            print(f"Yielding {repo_url} => {clones[repo_url]}")
            yield clones[repo_url]

    # Teardown: Remove all temporary directories at the end of the session
    yield _shallow_clone_git_repo

    shutil.rmtree(temp_dir)


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
