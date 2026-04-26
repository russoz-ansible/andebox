#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021-2022 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021-2022 Alexei Znamensky
# SPDX-License-Identifier: MIT
import importlib
import pkgutil
import signal
import sys
from pathlib import Path
from typing import Optional

import andebox.actions
import click
import typer

from . import __version__
from .exceptions import AndeboxException


app = typer.Typer(
    name="andebox",
    help=f"Ansible Developer (Tool)Box v{__version__}",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"andebox {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
    collection: Optional[str] = typer.Option(
        None,
        "--collection",
        "-c",
        help="fully qualified collection name (not necessary if a proper galaxy.yml file is available)",
    ),
    venv: Optional[Path] = typer.Option(
        None,
        "--venv",
        "-V",
        help="path to the virtual environment where andebox and ansible are installed",
    ),
) -> None:
    ctx.ensure_object(dict)
    ctx.obj["collection"] = collection
    ctx.obj["venv"] = venv


#
# Adapted from:
# https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/
#
def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def load_actions():
    for finder, name, ispkg in iter_namespace(andebox.actions):
        module = importlib.import_module(name)
        if hasattr(module, "app") and isinstance(module.app, typer.Typer):
            app.add_typer(module.app)


load_actions()


def run():
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        result = app(standalone_mode=False)
        return result or 0
    except click.exceptions.NoArgsIsHelpError:
        return 0
    except KeyboardInterrupt:
        print("Interrupted by user", file=sys.stderr)
        return 100
    except (AndeboxException, BrokenPipeError) as e:
        print(str(e), file=sys.stderr)
        return 1
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return e.code
