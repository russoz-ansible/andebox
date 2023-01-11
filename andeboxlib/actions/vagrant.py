# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os

import vagrant
from fabric.connection import Connection

from andeboxlib.actions.base import AndeboxAction
from andeboxlib.exceptions import AndeboxException


class VagrantError(AndeboxException):
    pass


class VagrantAction(AndeboxAction):
    name = "vagrant"
    help = "runs andebox within a VM managed with vagrant"
    args = [
        dict(names=("--name", "-n"),
             specs=dict(help="""name of the vagrant VM (default: "default")"""),
             default="default"),
        dict(names=("--sudo", "-s"),
             specs=dict(action="store_true",
                        help="""use sudo to run andebox""")),
        dict(names=("andebox_params", ),
             specs=dict(nargs="+")),
    ]

    def make_parser(self, subparser):
        action_parser = super().make_parser(subparser)
        action_parser.epilog = "Notice the use of '--' to delimit the vagrant command from the one running inside the VM"
        action_parser.usage = "%(prog)s usage: andebox vagrant [-h] [-n name] -- <andebox-cmd> [andebox-cmd-opts [-- test-params]]"

    def run(self, args):
        if not os.path.exists("Vagrantfile"):
            raise VagrantError("Missing Vagrantfile in the current directory")

        machine_name = args.name

        v = vagrant.Vagrant()
        for line in v.up(vm_name=machine_name, stream_output=True):
            print(line, end="")

        print("\n")
        with Connection(user=v.user(vm_name=machine_name),
                        host=v.hostname(vm_name=machine_name),
                        port=v.port(vm_name=machine_name),
                        connect_kwargs={
                            "key_filename": v.keyfile(vm_name=machine_name),
                        },) as c:

            print(f"== BEGIN vagrant VM: {machine_name} {'=' * 80}")
            with c.cd("/vagrant"):
                if args.sudo:
                    c.run(f"sudo andebox {' '.join(args.andebox_params)}")
                else:
                    c.run(f"andebox {' '.join(args.andebox_params)}")
            print(f"==== END vagrant VM: {machine_name} {'=' * 80}")
