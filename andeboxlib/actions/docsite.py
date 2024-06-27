# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import subprocess
import webbrowser

from ..util import set_dir

from .base import AndeboxAction
from ..exceptions import AndeboxException


class DocsiteAction(AndeboxAction):
    name = "docsite"
    help = "builds collection docsite"
    args = [
        dict(names=("--keep", "-k"),
             specs=dict(action="store_true", help="Keep temporary collection directory after execution")),
        dict(names=("--venv", "-V"),
             specs=dict(help="""path to the virtual environment where andebox and ansible are installed""")),
        dict(names=("--open", "-o"),
             specs=dict(action="store_true", help="Open browser pointing to main page after build")),
        dict(names=("--dest-dir", "-d"),
             specs=dict(help="Directory which should contain the docsite", default=".builtdocs")),
    ]

    def run(self, context, args):
        try:
            with context.temp_tree() as collection_dir:
                os.makedirs(args.dest_dir, mode=0o755, exist_ok=True)
                if not os.path.exists(os.path.join(args.dest_dir, "build.sh")):
                    subprocess.run([
                            context.binary_path(args.venv, "antsibull-docs"),
                            "sphinx-init", "--use-current", "--lenient",
                            f"{context.driver.namespace}.{context.driver.name}",
                            "--dest-dir", args.dest_dir
                        ],
                        cwd=collection_dir,
                        check=True
                    )

                with set_dir(args.dest_dir):
                    subprocess.run([context.binary_path(args.venv, "python"), "-m", "pip", "install", "-qr", "requirements.txt"], check=True)
                    subprocess.run(["./build.sh"], check=True)
        except Exception as e:
            raise AndeboxException(f"Error running when building docsite: {e}") from e

        if args.open:
            webbrowser.open(f"{os.path.join(args.dest_dir, 'build', 'html', 'index.html')}")
