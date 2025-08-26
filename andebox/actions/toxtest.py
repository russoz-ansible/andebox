# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
import os
import subprocess

from ..exceptions import AndeboxException
from .base import AndeboxAction


def _make_default_tox_ini():
    return """\
;
; andebox tox-test's tox.ini -- this file is not overwritten by andebox
[tox]
isolated_build = true
envlist = ac213, ac214, ac215, ac216, ac217, ac218, ac219, dev
skipsdist = true

[testenv]
passenv = PWD, HOME
skip_install = true
allowlist_externals = andebox
commands = andebox test -- {posargs}

[testenv:ac213]
basepython = python3.10
deps =
  ansible-core~=2.13.0
  andebox>=0.36

[testenv:ac214]
basepython = python3.11
deps =
  ansible-core~=2.14.0
  andebox>=0.36

[testenv:ac215]
basepython = python3.11
deps =
  ansible-core~=2.15.0
  andebox>=0.66

[testenv:ac216]
basepython = python3.12
deps =
  ansible-core~=2.16.0
  andebox>=0.66

[testenv:ac217]
basepython = python3.12
deps =
  ansible-core~=2.17.0
  andebox>=0.66

[testenv:ac218]
basepython = python3.13
deps =
  ansible-core~=2.18.0
  andebox>=0.66

[testenv:ac219]
basepython = python3.13
deps =
  ansible-core~=2.19.0
  andebox>=0.66

[testenv:dev]
basepython = python3.13
deps =
  https://github.com/ansible/ansible/archive/devel.tar.gz
  andebox>=0.66
"""


class ToxTestError(AndeboxException):
    pass


class ToxTestAction(AndeboxAction):
    name = "tox-test"
    help = "runs ansible-test within tox, for testing in multiple ansible versions"
    args = [
        dict(
            names=("--env", "-e"),
            specs=dict(help="tox environments to run the test in"),
        ),
        dict(
            names=("--list", "-l"),
            specs=dict(action="store_true", help="list all tox environments (tox -a)"),
        ),
        dict(
            names=("--recreate", "-r"),
            specs=dict(
                action="store_true",
                help="force recreation of virtual environments (tox -r)",
            ),
        ),
        dict(names=("ansible_test_params",), specs=dict(nargs="*")),
    ]
    tox_ini_filename = ".andebox-tox-test.ini"

    @classmethod
    def make_parser(cls, subparser):
        action_parser = super(ToxTestAction, cls).make_parser(subparser)
        action_parser.epilog = (
            "Notice the use of '--' to delimit andebox's options from tox's"
        )
        action_parser.usage = "%(prog)s [-h] [--env ENV] -- [ansible_test_params ...]"

    def run(self, context):
        if not os.path.exists(self.tox_ini_filename):
            with open(self.tox_ini_filename, "w") as tox_ini:
                tox_ini.write(_make_default_tox_ini())

        cmd_args = ["tox", "-c", self.tox_ini_filename]
        if context.args.list:
            cmd_args.append("-a")
        if context.args.recreate:
            cmd_args.append("-r")
        if context.args.env:
            cmd_args.extend(["-e", context.args.env])
        cmd_args.append("--")
        cmd_args.extend(context.args.ansible_test_params)
        rc = subprocess.call(cmd_args)

        if rc != 0:
            raise ToxTestError(f"Error running tox (rc={rc})")
