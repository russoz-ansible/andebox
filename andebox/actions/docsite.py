# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
import os
import subprocess
import webbrowser
from pathlib import Path

from ..context import CollectionContext
from ..context import ContextType
from ..exceptions import AndeboxException
from ..util import set_dir
from .base import AndeboxAction


class DocsiteAction(AndeboxAction):
    name = "docsite"
    help = "builds collection docsite"
    args = [
        dict(
            names=("--keep", "-k"),
            specs=dict(
                help="keep temporary collection directory after execution",
                action="store_true",
            ),
        ),
        dict(
            names=("--open", "-o"),
            specs=dict(
                help="open browser pointing to main page after build",
                action="store_true",
            ),
        ),
        dict(
            names=("--dest-dir", "-d"),
            specs=dict(
                help="directory which should contain the docsite",
                default=".builtdocs",
                type=Path,
            ),
        ),
    ]

    def run(self, context: CollectionContext):
        if context.type != ContextType.COLLECTION:
            raise AndeboxException(
                "Action 'docsite' must be executed in a collection context!"
            )
        try:
            with context.temp_tree() as collection_dir:
                os.makedirs(context.args.dest_dir, mode=0o755, exist_ok=True)
                if not (context.args.dest_dir / "build.sh").exists():
                    subprocess.run(
                        [
                            context.binary_path("antsibull-docs"),
                            "sphinx-init",
                            "--use-current",
                            "--lenient",
                            f"{context.namespace}.{context.name}",
                            "--dest-dir",
                            f"{context.args.dest_dir}",
                        ],
                        cwd=collection_dir,
                        check=True,
                    )

                with set_dir(context.args.dest_dir):
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
        except Exception as e:
            raise AndeboxException(f"Error running when building docsite: {e}") from e

        if context.args.open:
            webbrowser.open(
                f"{context.args.dest_dir / 'build' / 'html' / 'index.html'}"
            )
