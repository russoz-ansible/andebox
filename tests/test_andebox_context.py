# code: language=python tabSize=4
#
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import subprocess
from contextlib import chdir as set_dir

import pytest

from andebox.context import AndeboxUnknownContext, ContextType, create_context

from .utils import GIT_REPO_AC, GIT_REPO_CG, GenericTestCase


@pytest.fixture
def repo_dir(git_repo):
    def _repo_dir(repo: str) -> str:
        tc = GenericTestCase(id="repo_dir", input={"repo": repo}, expected={})
        result = git_repo(tc)
        return result["basedir"]

    return _repo_dir


def test_ansible_cg(repo_dir):
    with set_dir(repo_dir(GIT_REPO_CG)):
        context = create_context()
        assert context.type == ContextType.COLLECTION


def test_ansible_core(repo_dir):
    with set_dir(repo_dir(GIT_REPO_AC)):
        context = create_context()
        assert context.type == ContextType.ANSIBLE_CORE


def test_invalid_dir(tmp_path):
    repo_dir = tmp_path / "invalid_repo"
    repo_dir.mkdir(parents=True, exist_ok=True)

    with set_dir(repo_dir):
        with pytest.raises(AndeboxUnknownContext):
            create_context()


def test_copy_tree_skips_gitignored(tmp_path):
    repo_dir = tmp_path / "coll"
    (repo_dir / "meta").mkdir(parents=True)
    (repo_dir / "meta" / "runtime.yml").write_text("---\n")
    (repo_dir / "galaxy.yml").write_text("namespace: ns\nname: coll\nversion: 1.0.0\n")
    (repo_dir / ".gitignore").write_text("*.log\nbuild/\n/top_only.txt\n!keep.log\n")
    (repo_dir / "plugins" / "modules").mkdir(parents=True)
    (repo_dir / "plugins" / "modules" / "mod.py").write_text("")
    (repo_dir / "plugins" / "modules" / "debug.log").write_text("")
    (repo_dir / "plugins" / "modules" / "keep.log").write_text("")
    (repo_dir / "plugins" / "build").mkdir()
    (repo_dir / "plugins" / "build" / "artifact.txt").write_text("")
    (repo_dir / "plugins" / "top_only.txt").write_text("")
    (repo_dir / "build").mkdir()
    (repo_dir / "build" / "artifact.txt").write_text("")
    (repo_dir / "top_only.txt").write_text("")
    (repo_dir / "root.log").write_text("")
    subprocess.run(["git", "init", "-q"], cwd=repo_dir, check=True)

    with set_dir(repo_dir):
        context = create_context()
        with context.temp_tree() as full_dir:
            copied = {p.relative_to(full_dir).as_posix() for p in full_dir.rglob("*") if p.is_file()}

    assert copied == {
        "galaxy.yml",
        "meta/runtime.yml",
        "plugins/modules/mod.py",
        "plugins/modules/keep.log",
        "plugins/top_only.txt",
    }


def test_copy_tree_outside_git_repo(tmp_path):
    repo_dir = tmp_path / "coll"
    (repo_dir / "meta").mkdir(parents=True)
    (repo_dir / "meta" / "runtime.yml").write_text("---\n")
    (repo_dir / "galaxy.yml").write_text("namespace: ns\nname: coll\nversion: 1.0.0\n")
    (repo_dir / ".gitignore").write_text("*.log\n")
    (repo_dir / "root.log").write_text("")

    with set_dir(repo_dir):
        context = create_context()
        with context.temp_tree() as full_dir:
            copied = {p.relative_to(full_dir).as_posix() for p in full_dir.rglob("*") if p.is_file()}

    assert copied == {"galaxy.yml", "meta/runtime.yml", "root.log"}
