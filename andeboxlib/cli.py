#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2021-2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

__version__ = '0.39'

import argparse
import sys
import signal

from andeboxlib.exceptions import AndeboxException
from andeboxlib.actions.ansibletest import AnsibleTestAction
from andeboxlib.actions.ignorefile import IgnoreLinesAction
from andeboxlib.actions.runtime import RuntimeAction
from andeboxlib.actions.toxtest import ToxTestAction
from andeboxlib.actions.vagrant import VagrantAction


_actions = [AnsibleTestAction, IgnoreLinesAction, RuntimeAction, ToxTestAction, VagrantAction]


def _make_parser():
    parser = argparse.ArgumentParser(prog="andebox", description="Ansible Developer (Tool)Box v{}".format(__version__))
    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s {0}".format(__version__))
    parser.add_argument("--collection", "-c",
                        help="fully qualified collection name (not necessary if a proper galaxy.yml file is available)")
    subparser = parser.add_subparsers(dest="action", required=True)

    for action in _actions:
        action.make_parser(subparser)

    return parser


class AndeBox:
    actions = {}
    parser = None

    def __init__(self) -> None:
        self.add_actions(*_actions)

    def add_actions(self, *actions):
        self.actions.update({ac.name: ac() for ac in actions})

    def build_argparser(self):
        self.parser = _make_parser()

    def run(self):
        self.build_argparser()
        args = self.parser.parse_args()
        action = self.actions[args.action]
        action.run(args)


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
