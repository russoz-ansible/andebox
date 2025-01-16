#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 2021-2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

__version__ = "0.73"

import argparse
import signal
import sys
from pathlib import Path
import importlib
import pkgutil

import andeboxlib.actions
from .actions.base import AndeboxAction
from .context import create_context
from .exceptions import AndeboxException
from .util import set_dir


#
# Adapted from:
# https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/
#
def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def load_actions():
    results = []

    for finder, name, ispkg in iter_namespace(andeboxlib.actions):
        for attr in dir(module := importlib.import_module(name)):
            try:
                action = getattr(module, attr)
                if issubclass(action, AndeboxAction) and action != AndeboxAction:
                    results.append(action)
            except TypeError:
                pass

    return results


actions = load_actions()


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="andebox", description=f"Ansible Developer (Tool)Box v{__version__}"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--collection",
        "-c",
        help="fully qualified collection name (not necessary if a proper galaxy.yml file is available)",
    )
    parser.add_argument(
        "--venv",
        "-V",
        help="path to the virtual environment where andebox and ansible are installed",
        type=Path,
    )
    subparser = parser.add_subparsers(dest="action", required=True)

    for action in actions:
        action.make_parser(subparser)

    return parser


class AndeBox:
    def __init__(self) -> None:
        self.actions = {ac.name: ac() for ac in actions}
        self.parser = _make_parser()

    def run(self):
        args = self.parser.parse_args()
        context = create_context(args)
        with set_dir(context.base_dir):
            action = self.actions[args.action]
            action.run(context)


def run():
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        box = AndeBox()
        box.run()
        return 0
    except KeyboardInterrupt:
        print("Interrupted by user", file=sys.stderr)
        return 2
    except (AndeboxException, BrokenPipeError) as e:
        print(str(e), file=sys.stderr)
        return 1
