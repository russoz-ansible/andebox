# code: language=python tabSize=4
# (C) 2021-2023 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021-2023 Alexei Znamensky
# SPDX-License-Identifier: MIT
import logging
from pathlib import Path
from typing import List, Optional

import typer

try:
    vagrant_logger = logging.getLogger("vagrant")
    prev_level = vagrant_logger.level
    vagrant_logger.setLevel(logging.ERROR)
    import vagrant
    from fabric.connection import Connection

    vagrant_logger.setLevel(prev_level)

    IMPORT_ERROR = None
except ImportError as e:
    IMPORT_ERROR = e

from ..context import andebox_context
from ..exceptions import AndeboxException


class VagrantError(AndeboxException):
    pass


app = typer.Typer(
    name="vagrant",
    help="runs 'andebox test -- integration' within a VM managed with vagrant",
)


@app.callback(invoke_without_command=True)
def vagrant_cmd(
    ctx: typer.Context,
    name: str = typer.Option(
        "default",
        "--name",
        "-n",
        help="""name of the vagrant VM (default: "default")""",
    ),
    destroy: bool = typer.Option(False, "--destroy", "-d", help="destroy the VM after the test"),
    sudo: bool = typer.Option(False, "--sudo", "-s", help="use sudo to run andebox inside the VM"),
    integration_test_params: Optional[List[str]] = typer.Argument(None),
) -> None:
    if IMPORT_ERROR:
        raise AndeboxException(f"Missing dependency for action 'vagrant': {IMPORT_ERROR}") from IMPORT_ERROR

    opts = ctx.obj or {}
    venv = opts.get("venv") or Path("/venv")

    with andebox_context(ctx) as context:
        if not Path("Vagrantfile").exists():
            raise VagrantError("Missing Vagrantfile in the current directory")

        print(f"== SETUP vagrant VM: {name} ".ljust(80, "="))
        v = vagrant.Vagrant()
        for line in v.up(vm_name=name, stream_output=True):
            print(line, end="")

        try:
            print("\n")
            with Connection(
                user=v.user(vm_name=name),
                host=v.hostname(vm_name=name),
                port=v.port(vm_name=name),
                connect_kwargs={
                    "key_filename": v.keyfile(vm_name=name),
                },
            ) as c:
                print(f"== BEGIN vagrant andebox: {name} ".ljust(80, "="))
                with c.cd("/vagrant"):
                    andebox_path = context.binary_path("andebox") if context.venv else str(venv / "bin" / "andebox")
                    vparams = list(integration_test_params or [])
                    if vparams[:1] == ["--"]:
                        vparams = vparams[1:]
                    cmd = f"{andebox_path} --venv {venv} test -- integration {' '.join(vparams)}"
                    if sudo:
                        cmd = "sudo -HE " + cmd

                    c.run(cmd)
        except Exception as e:
            raise VagrantError(str(e)) from e
        finally:
            if destroy:
                v.destroy()
            print(f"== END   vagrant andebox: {name} ".ljust(80, "="))
