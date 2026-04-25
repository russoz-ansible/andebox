# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
import os
import subprocess
from typing import List
from typing import Optional

import typer

from ..context import andebox_context
from ..exceptions import AndeboxException


def _make_default_tox_ini():
    return """\
;
; andebox tox-test's tox.ini -- this file is not overwritten by andebox
[tox]
isolated_build = true
envlist = ac217, ac218, ac219, ac220, ac221, dev
skipsdist = true

[testenv]
passenv = PWD, HOME
skip_install = true
allowlist_externals = andebox
commands = andebox test -- {posargs}

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

[testenv:ac220]
basepython = python3.13
deps =
  ansible-core~=2.20.0
  andebox>=0.66

[testenv:ac221]
basepython = python3.14
deps =
  ansible-core~=2.21.0
  andebox>=0.66

[testenv:dev]
basepython = python3.13
deps =
  https://github.com/ansible/ansible/archive/devel.tar.gz
  andebox>=0.66
"""


class ToxTestError(AndeboxException):
    pass


TOX_INI_FILENAME = ".andebox-tox-test.ini"

app = typer.Typer(
    name="tox-test",
    help="runs ansible-test within tox, for testing in multiple ansible versions",
)


@app.callback(invoke_without_command=True)
def tox_test_cmd(
    ctx: typer.Context,
    env: Optional[str] = typer.Option(
        None, "--env", "-e", help="tox environments to run the test in"
    ),
    list_: bool = typer.Option(
        False, "--list", "-l", help="list all tox environments (tox -a)"
    ),
    recreate: bool = typer.Option(
        False,
        "--recreate",
        "-r",
        help="force recreation of virtual environments (tox -r)",
    ),
    ansible_test_params: Optional[List[str]] = typer.Argument(None),
) -> None:
    with andebox_context(ctx):
        if not os.path.exists(TOX_INI_FILENAME):
            with open(TOX_INI_FILENAME, "w") as tox_ini:
                tox_ini.write(_make_default_tox_ini())

        cmd_args = ["tox", "-c", TOX_INI_FILENAME]
        if list_:
            cmd_args.append("-a")
        if recreate:
            cmd_args.append("-r")
        if env:
            cmd_args.extend(["-e", env])
        cmd_args.append("--")
        cmd_args.extend(ansible_test_params or [])
        rc = subprocess.call(cmd_args)

        if rc != 0:
            raise ToxTestError(f"Error running tox (rc={rc})")
