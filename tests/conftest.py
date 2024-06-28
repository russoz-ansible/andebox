# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import shutil
import subprocess
import tempfile

import pytest


@pytest.fixture(scope="session")
def git_repo():
    clones = {}

    def _shallow_clone_git_repo(repo_url):
        if repo_url not in clones:
            # Setup: Create a temporary directory
            temp_dir = tempfile.mkdtemp()

            # Perform shallow clone
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, temp_dir], check=True
            )

            # Store the path for later cleanup
            clones[repo_url] = temp_dir

        yield clones[repo_url]

    # Teardown: Remove all temporary directories at the end of the session
    yield _shallow_clone_git_repo

    for temp_dir in clones.values():
        shutil.rmtree(temp_dir)
