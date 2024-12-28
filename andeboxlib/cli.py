#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2021-2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

__version__ = "0.68"

import argparse
import signal
import sys
from pathlib import Path

from .actions.ansibletest import AnsibleTestAction
from .actions.docsite import DocsiteAction
from .actions.ignorefile import IgnoreLinesAction
from .actions.yaml_doc import YAMLDocAction
from .actions.runtime import RuntimeAction
from .actions.toxtest import ToxTestAction
from .actions.vagrant import VagrantAction
from .context import Context
from .exceptions import AndeboxException
from .util import set_dir

_actions = [
    AnsibleTestAction,
    IgnoreLinesAction,
    YAMLDocAction,
    RuntimeAction,
    ToxTestAction,
    VagrantAction,
    DocsiteAction,
]


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

    for action in _actions:
        action.make_parser(subparser)

    return parser


class AndeBox:
    def __init__(self) -> None:
        self.actions = {ac.name: ac() for ac in _actions}
        self.parser = _make_parser()

    def run(self):
        args = self.parser.parse_args()
        context = Context.create(args)
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
