# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import pytest
from andebox.cli import _make_parser
from andebox.context import AndeboxUnknownContext
from andebox.context import ContextType
from andebox.context import create_context
from andebox.util import set_dir

from .utils import GIT_REPO_AC
from .utils import GIT_REPO_CG


@pytest.fixture
def repo_dir(git_repo):
    return lambda repo: git_repo(dict(repo=repo))["basedir"]


def test_ansible_cg(repo_dir):
    with set_dir(repo_dir(GIT_REPO_CG)):
        parser = _make_parser()
        context = create_context(parser.parse_args(args=["context"]))
        assert context.type == ContextType.COLLECTION


def test_ansible_core(repo_dir):
    with set_dir(repo_dir(GIT_REPO_AC)):
        parser = _make_parser()
        context = create_context(parser.parse_args(args=["context"]))
        assert context.type == ContextType.ANSIBLE_CORE


def test_invalid_dir(tmp_path):
    repo_dir = tmp_path / "invalid_repo"
    repo_dir.mkdir(parents=True, exist_ok=True)

    with set_dir(repo_dir):
        parser = _make_parser()
        with pytest.raises(AndeboxUnknownContext):
            create_context(parser.parse_args(args=["context"]))
