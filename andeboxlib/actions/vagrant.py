# -*- coding: utf-8 -*-
# (c) 2021-2023, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os

from fabric.connection import Connection

from andeboxlib.actions.base import AndeboxAction
from andeboxlib.exceptions import AndeboxException


class VagrantError(AndeboxException):
    pass


class VagrantAction(AndeboxAction):
    name = "vagrant"
    help = "runs 'andebox test -- integration' within a VM managed with vagrant"
    args = [
        dict(names=("--name", "-n"),
             specs=dict(help="""name of the vagrant VM (default: "default")""")),
        dict(names=("--sudo", "-s"),
             specs=dict(action="store_true",
                        help="""use sudo to run andebox""")),
        dict(names=("--venv", "-V"),
             specs=dict(help="""path to the virtual environment where andebox and ansible are installed (default: "/venv")""")),
        dict(names=("--destroy", "-d"),
             specs=dict(action="store_true",
                        help="""destroy the VM after the test""")),
        dict(names=("andebox_params", ),
             specs=dict(nargs="+")),
    ]
    default_name = "default"
    default_venv = "/venv"

    @classmethod
    def make_parser(cls, subparser):
        action_parser = super(VagrantAction, cls).make_parser(subparser)
        action_parser.epilog = "Notice the use of '--' to delimit the vagrant command from the one running inside the VM"
        action_parser.usage = "%(prog)s usage: andebox vagrant [-h] [-n name] -- <andebox-cmd> [andebox-cmd-opts [-- test-params]]"

    def run(self, args):
        import vagrant

        if not os.path.exists("Vagrantfile"):
            raise VagrantError("Missing Vagrantfile in the current directory")

        # argparse does not seem to honour defaults in subparsers, so making do with these
        machine_name = args.name or self.default_name
        venv = args.venv or self.default_venv

        print(f"== SETUP vagrant VM: {machine_name} {'=' * 80}")
        v = vagrant.Vagrant()
        for line in v.up(vm_name=machine_name, stream_output=True):
            print(line, end="")

        try:
            print("\n")
            with Connection(user=v.user(vm_name=machine_name),
                            host=v.hostname(vm_name=machine_name),
                            port=v.port(vm_name=machine_name),
                            connect_kwargs={
                                "key_filename": v.keyfile(vm_name=machine_name),
                            },) as c:

                print(f"== BEGIN vagrant andebox: {machine_name} {'=' * 80}")
                with c.cd("/vagrant"):
                    andebox_path = self.binary_path(venv, "andebox")
                    cmd = f"{andebox_path} test --venv {venv} -R -- integration {' '.join(args.andebox_params)}"
                    if args.sudo:
                        cmd = "sudo -HE " + cmd

                    c.run(cmd)
        except Exception as e:
            raise VagrantError(str(e)) from e
        finally:
            if args.destroy:
                v.destroy()
            print(f"==== END vagrant andebox: {machine_name} {'=' * 80}")
