# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import sys
import subprocess

from andeboxlib.actions.base import AndeboxAction
from andeboxlib.exceptions import AndeboxException


def _make_default_tox_ini():
    return f"""; andebox tox-test's tox.ini -- this file is not overwritten by andebox
[tox]
isolated_build = true
envlist = 211, 212, 213, a4, a5, a6, dev
skipsdist = true

[testenv]
passenv = PWD HOME
skip_install = true
allowlist_externals = andebox
basepython = {sys.executable}
deps =
  andebox
  211: ansible-core>=2.11,<2.12
  212: ansible-core>=2.12,<2.13
  213: ansible-core>=2.13,<2.14
  214: ansible-core>=2.14,<2.15
  a4: ansible>=4.0.0,<5.0.0
  a5: ansible>=5.0.0,<6.0.0
  a6: ansible>=6.0.0,<7.0.0
  dev: https://github.com/ansible/ansible/archive/devel.tar.gz
commands = andebox test -- {{posargs}}
"""


class ToxTestError(AndeboxException):
    pass


class ToxTestAction(AndeboxAction):
    name = "tox-test"
    help = "runs ansible-test within tox, for testing in multiple ansible versions"
    args = [
        dict(names=("--env", "-e"),
             specs=dict(help="tox environments to run the test in")),
        dict(names=("--list", "-l"),
             specs=dict(action="store_true", help="list all tox environments (tox -a)")),
        dict(names=("--recreate", "-r"),
             specs=dict(action="store_true", help="force recreation of virtual environments (tox -r)")),
        dict(names=("ansible_test_params", ),
             specs=dict(nargs="*")),
    ]
    tox_ini_filename = ".andebox-tox-test.ini"

    def make_parser(self, subparser):
        action_parser = super().make_parser(subparser)
        action_parser.epilog = "Notice the use of '--' to delimit andebox's options from tox's"
        action_parser.usage = "%(prog)s usage: andebox tox-test [-h] [--env ENV] -- [ansible_test_params ...]"

    def run(self, args):
        if not os.path.exists(self.tox_ini_filename):
            with open(self.tox_ini_filename, "w") as tox_ini:
                tox_ini.write(_make_default_tox_ini())

        cmd_args = ["tox", "-c", self.tox_ini_filename]
        if args.list:
            cmd_args.append("-a")
        if args.recreate:
            cmd_args.append("-r")
        if args.env:
            cmd_args.extend(["-e", args.env])
        cmd_args.append("--")
        cmd_args.extend(args.ansible_test_params)
        rc = subprocess.call(cmd_args)

        if rc != 0:
            raise ToxTestError("Error running tox (rc={0})".format(rc))
