# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import subprocess

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
        dict(names=("ansible_test_params",), specs=dict(nargs="+")),
    ]

    @classmethod
    def make_parser(cls, subparser):
        action_parser = super(AnsibleTestAction, cls).make_parser(subparser)
        action_parser.epilog = (
            "Notice the use of '--' to delimit andebox's options from ansible-test's"
        )
        action_parser.usage = "%(prog)s [-h] [--keep] -- [ansible_test_params ...]"

    def run(self, context):
        try:
            with context.temp_tree() as temp_dir:
                if context.args.requirements:
                    context.install_requirements()
                if context.args.exclude_from_ignore:
                    context.exclude_from_ignore()
                subprocess.run(
                    [context.ansible_test] + context.args.ansible_test_params,
                    cwd=temp_dir,
                    check=True,
                )
        except Exception as e:
            raise AndeboxException(f"Error running ansible-test: {e}") from e
