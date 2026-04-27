# code: language=python tabSize=4
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
import subprocess
import webbrowser
from contextlib import chdir as set_dir
from pathlib import Path

import typer

from ..context import andebox_context

app = typer.Typer(name="docsite", help="builds collection docsite")


@app.callback(invoke_without_command=True)
def docsite_cmd(
    ctx: typer.Context,
    keep: bool = typer.Option(
        False,
        "--keep",
        "-k",
        help="keep temporary collection directory after execution",
    ),
    open_: bool = typer.Option(False, "--open", "-o", help="open browser pointing to main page after build"),
    dest_dir: Path = typer.Option(..., "--dest-dir", "-d", help="directory where docsite is generated"),
) -> None:
    with andebox_context(ctx, require_collection=True, make_temp_tree=True, keep=keep) as context:
        dest_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        if not (dest_dir / "build.sh").exists():
            subprocess.run(
                [
                    context.binary_path("antsibull-docs"),
                    "sphinx-init",
                    "--use-current",
                    "--lenient",
                    f"{context.namespace}.{context.name}",
                    "--dest-dir",
                    f"{dest_dir}",
                ],
                cwd=context.full_dir,
                check=True,
            )

        with set_dir(dest_dir):
            subprocess.run(
                [
                    context.binary_path("python"),
                    "-m",
                    "pip",
                    "install",
                    "-qr",
                    "requirements.txt",
                ],
                check=True,
            )
            subprocess.run(["./build.sh"], check=True)

        if open_:
            webbrowser.open(f"{dest_dir / 'build' / 'html' / 'index.html'}")
