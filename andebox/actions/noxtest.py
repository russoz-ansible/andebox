# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2026 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2026 Alexei Znamensky
# SPDX-License-Identifier: MIT
from pathlib import Path
from typing import List, Optional
from unittest.mock import patch

import typer

from ..context import andebox_context
from ..exceptions import AndeboxException

# (ansible-core version, default python, all supported pythons)
VERSION_MATRIX = [
    ("2.17", "3.11", ["3.10", "3.11", "3.12"]),
    ("2.18", "3.12", ["3.11", "3.12", "3.13"]),
    ("2.19", "3.12", ["3.11", "3.12", "3.13"]),
    ("2.20", "3.13", ["3.12", "3.13", "3.14"]),
    ("2.21", "3.13", ["3.12", "3.13", "3.14"]),
    ("devel", "3.14", ["3.13", "3.14", "3.15"]),
]


class NoxTestError(AndeboxException):
    pass


app = typer.Typer(
    name="nox-test",
    help="runs ansible-test within nox, for testing in multiple ansible/python versions",
)


def session_name(ac_ver: str, py: str) -> str:
    return f"ac{ac_ver}-p{py}"


def register_sessions(nox_module) -> None:
    for ac_ver, default_py, all_pys in VERSION_MATRIX:
        for py in all_pys:

            def make(av: str, python: str, is_default: bool) -> None:
                name = session_name(av, python)

                def session_func(session) -> None:
                    if av == "devel":
                        pkg = "https://github.com/ansible/ansible/archive/devel.tar.gz"
                    else:
                        pkg = f"ansible-core~={av}.0"
                    session.install(pkg, "andebox")
                    session.chdir(session.invoked_from)
                    session.run("andebox", "test", *session.posargs, external=True)

                session_func.__name__ = name
                nox_module.session(python=python, name=name, default=is_default)(session_func)

            make(ac_ver, py, py == default_py)


def select_sessions(
    ansible_cores: Optional[List[str]],
    pythons: Optional[List[str]],
) -> Optional[List[str]]:
    if not ansible_cores and not pythons:
        return None
    result = []
    for ac_ver, _, all_pys in VERSION_MATRIX:
        if ansible_cores and ac_ver not in ansible_cores:
            continue
        for py in all_pys:
            if pythons and py not in pythons:
                continue
            result.append(session_name(ac_ver, py))
    return result or None


def run_nox(
    sessions: Optional[List[str]],
    list_sessions: bool,
    reuse_venv: bool,
    posargs: Optional[List[str]],
) -> None:
    import nox

    noxfile = Path(__file__).parent.parent / "_nox_sessions.py"

    argv = ["nox", "-f", str(noxfile)]
    if list_sessions:
        argv.append("--list")
    if reuse_venv:
        argv.append("--reuse-existing-virtualenvs")

    for s in sessions or []:
        argv.extend(["-s", s])

    if posargs:
        argv += ["--"] + list(posargs)

    with patch("sys.argv", argv):
        try:
            nox.main()
        except SystemExit as e:
            if e.code not in (None, 0):
                raise NoxTestError(f"nox exited with code {e.code}") from e


@app.callback(invoke_without_command=True)
def nox_test_cmd(
    ctx: typer.Context,
    session: Optional[List[str]] = typer.Option(None, "--session", "-s", help="nox session(s) to run directly"),
    list_: bool = typer.Option(False, "--list", "-l", help="list all nox sessions"),
    reuse_venv: bool = typer.Option(
        False,
        "--reuse-venv",
        "-r",
        help="reuse existing virtual environments (nox --reuse-existing-virtualenvs)",
    ),
    ansible_core: Optional[List[str]] = typer.Option(
        None,
        "--ansible-core",
        "-a",
        help="ansible-core version(s) to test against (e.g. 2.17)",
    ),
    python: Optional[List[str]] = typer.Option(
        None,
        "--python",
        "-p",
        help="python version(s) to test with (e.g. 3.12)",
    ),
    ansible_test_params: Optional[List[str]] = typer.Argument(None),
) -> None:
    with andebox_context(ctx):
        sessions = session or select_sessions(ansible_core, python)
        run_nox(
            sessions=sessions,
            list_sessions=list_,
            reuse_venv=reuse_venv,
            posargs=ansible_test_params,
        )
