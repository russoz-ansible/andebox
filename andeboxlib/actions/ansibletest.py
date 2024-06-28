# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import subprocess
from pathlib import Path

from ..exceptions import AndeboxException
from .base import AndeboxAction


class AnsibleTestAction(AndeboxAction):
    name = "test"
    help = "runs ansible-test in a temporary environment"
    args = [
        dict(
            names=("--keep", "-k"),
            specs=dict(
                action="store_true", help="Keep temporary directory after execution"
            ),
        ),
        dict(
            names=("--exclude-from-ignore", "-efi", "-ei"),
            specs=dict(
                action="store_true",
                help="Matching lines in ignore files will be filtered out",
            ),
        ),
        dict(
            names=("--requirements", "-R"),
            specs=dict(
                action="store_true",
                help="Install integration_tests_dependencies from tests/requirements.yml prior",
            ),
        ),
        dict(
            names=("--venv", "-V"),
            specs=dict(
                help="path to the virtual environment where andebox and ansible are installed",
                type=Path,
            ),
        ),
        dict(names=("ansible_test_params",), specs=dict(nargs="+")),
    ]

    @classmethod
    def make_parser(cls, subparser):
        action_parser = super(AnsibleTestAction, cls).make_parser(subparser)
        action_parser.epilog = (
            "Notice the use of '--' to delimit andebox's options from ansible-test's"
        )
        action_parser.usage = "%(prog)s [-h] [--keep] -- [ansible_test_params ...]"

    def run(self, context, args):
        try:
            with context.temp_tree() as collection_dir:
                if args.requirements:
                    self.install_requirements(context, args.venv)
                if args.exclude_from_ignore:
                    self.exclude_from_ignore(
                        context,
                        args.exclude_from_ignore,
                        args.ansible_test_params,
                        collection_dir,
                    )
                subprocess.run(
                    [context.ansible_test] + args.ansible_test_params,
                    cwd=collection_dir,
                    check=True,
                )
        except Exception as e:
            raise AndeboxException(f"Error running ansible-test: {e}") from e

    def exclude_from_ignore(
        self, context, exclude_from_ignore, ansible_test_params, coll_dir
    ):
        files = [f for f in ansible_test_params if os.path.isfile(f)]
        print(f"Excluding from ignore files: {files}")
        if exclude_from_ignore:
            src_dir = os.path.join(os.getcwd(), "tests", "sanity")
            dest_dir = os.path.join(coll_dir, "tests", "sanity")
            with os.scandir(src_dir) as ts_dir:
                for ts_entry in ts_dir:
                    if ts_entry.name.startswith("ignore-") and ts_entry.name.endswith(
                        ".txt"
                    ):
                        context.copy_exclude_lines(
                            os.path.join(src_dir, ts_entry.name),
                            os.path.join(dest_dir, ts_entry.name),
                            files,
                        )

    @staticmethod
    def install_requirements(context, venv):
        subprocess.run(
            [
                context.binary_path("ansible-galaxy"),
                "collection",
                "install",
                "-r",
                f"{Path('tests') / 'integration' / 'requirements.yml'}",
            ],
            check=True,
        )
