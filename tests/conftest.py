# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


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
            subprocess.run(["git", "clone", "--depth", "1", repo_url, dest], check=True)

            # Store the path for later cleanup
            clones[repo_url] = dest

        while repo_url in clones:
            yield clones[repo_url]

    # Teardown: Remove all temporary directories at the end of the session
    yield _shallow_clone_git_repo

    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def install_andebox():
    proj_dir = os.getcwd()

    print(f"{proj_dir=}")

    print("Uninstalling andebox")
    subprocess.run(
        ["pip", "uninstall", "-y", "andebox"],
        check=True,
        encoding="utf-8",
        capture_output=True,
    )
    print("Installing andebox")
    subprocess.run(
        ["pip", "install", "-e", proj_dir],
        check=True,
        encoding="utf-8",
        capture_output=True,
    )

    yield

    print("Uninstalling andebox (cleanup)")
    subprocess.run(
        ["pip", "uninstall", "-y", "andebox"],
        check=False,
        encoding="utf-8",
        capture_output=True,
    )
