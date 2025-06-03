# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021-2023 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021-2023 Alexei Znamensky
# SPDX-License-Identifier: MIT
from pathlib import Path

try:
    from fabric.connection import Connection
    import vagrant

    IMPORT_ERROR = None
except ImportError as e:
    IMPORT_ERROR = e

from ..exceptions import AndeboxException
from .base import AndeboxAction


class VagrantError(AndeboxException):
    pass


class VagrantAction(AndeboxAction):
    name = "vagrant"
    help = "runs 'andebox test -- integration' within a VM managed with vagrant"
    args = [
        dict(
            names=("--name", "-n"),
            specs=dict(
                help="""name of the vagrant VM (default: "default")""",
                default="default",
            ),
        ),
        dict(
            names=("--sudo", "-s"),
            specs=dict(action="store_true", help="""use sudo to run andebox"""),
        ),
        dict(
            names=("--destroy", "-d"),
            specs=dict(action="store_true", help="""destroy the VM after the test"""),
        ),
        dict(names=("andebox_params",), specs=dict(nargs="+")),
    ]

    @classmethod
    def make_parser(cls, subparser):
        action_parser = super(VagrantAction, cls).make_parser(subparser)
        action_parser.epilog = (
            "Notice the use of '--' to delimit the vagrant command from the one running inside the VM\n"
            "If VENV is not provided, it is assumed to be `/venv`."
        )
        action_parser.usage = "%(prog)s [-hsd] [-n name] [-V VENV] -- <andebox-cmd> [andebox-cmd-opts [-- test-params]]"

    def run(self, context):
        if IMPORT_ERROR:
            raise AndeboxException(
                "Missing dependency for action 'vagrant': "
            ) from IMPORT_ERROR

        if not Path("Vagrantfile").exists():
            raise VagrantError("Missing Vagrantfile in the current directory")

        # argparse does not seem to honour defaults in subparsers, so making do with these
        machine_name = context.args.name
        if not context.args.venv:
            context.args.venv = "/venv"

        print(f"== SETUP vagrant VM: {machine_name} ".ljust(80, "="))
        v = vagrant.Vagrant()
        for line in v.up(vm_name=machine_name, stream_output=True):
            print(line, end="")

        try:
            print("\n")
            with Connection(
                user=v.user(vm_name=machine_name),
                host=v.hostname(vm_name=machine_name),
                port=v.port(vm_name=machine_name),
                connect_kwargs={
                    "key_filename": v.keyfile(vm_name=machine_name),
                },
            ) as c:

                print(f"== BEGIN vagrant andebox: {machine_name} ".ljust(80, "="))
                with c.cd("/vagrant"):
                    andebox_path = context.binary_path("andebox")
                    cmd = f"{andebox_path} --venv {context.args.venv} test -- integration {' '.join(context.args.andebox_params)}"
                    if context.args.sudo:
                        cmd = "sudo -HE " + cmd

                    c.run(cmd)
        except Exception as e:
            raise VagrantError(str(e)) from e
        finally:
            if context.args.destroy:
                v.destroy()
            print(f"== END   vagrant andebox: {machine_name} ".ljust(80, "="))
