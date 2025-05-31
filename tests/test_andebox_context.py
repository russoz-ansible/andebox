# -*- coding: utf-8 -*-
# Copyright (c) 2024, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import os

import pytest
from andebox.cli import _make_parser
from andebox.context import AndeboxUnknownContext
from andebox.context import ContextType
from andebox.context import create_context

from .utils import GIT_REPO_AC
from .utils import GIT_REPO_CG


def test_ansible_cg(git_repo):
    repo_dir = git_repo(GIT_REPO_CG)

    os.chdir(repo_dir)
    parser = _make_parser()
    context = create_context(parser.parse_args(args=["context"]))
    assert context.type == ContextType.COLLECTION


def test_ansible_core(git_repo):
    repo_dir = git_repo(GIT_REPO_AC)

    os.chdir(repo_dir)
    parser = _make_parser()
    context = create_context(parser.parse_args(args=["context"]))
    assert context.type == ContextType.ANSIBLE_CORE


def test_invalid_dir(tmp_path):
    repo_dir = tmp_path / "invalid_repo"
    repo_dir.mkdir(parents=True, exist_ok=True)

    os.chdir(str(repo_dir))
    parser = _make_parser()
    with pytest.raises(AndeboxUnknownContext):
        create_context(parser.parse_args(args=["context"]))


# code: language=python tabSize=4
