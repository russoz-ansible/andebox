# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os

from andeboxlib.cli import _make_parser
from andeboxlib.context import ContextType
from andeboxlib.context import create_context


GIT_REPO_CG = "https://github.com/ansible-collections/community.general.git"
GIT_REPO_AC = "https://github.com/ansible/ansible.git"


def test_ansible_cg(git_repo):
    repo_dir = git_repo(GIT_REPO_CG)

    try:
        os.chdir(next(repo_dir))
        parser = _make_parser()
        context = create_context(parser.parse_args(args=["context"]))
        assert context.type == ContextType.COLLECTION

    finally:
        next(repo_dir, None)


def test_ansible_core(git_repo):
    repo_dir = git_repo(GIT_REPO_AC)

    try:
        os.chdir(next(repo_dir))
        parser = _make_parser()
        context = create_context(parser.parse_args(args=["context"]))
        assert context.type == ContextType.ANSIBLE_CORE

    finally:
        next(repo_dir, None)
