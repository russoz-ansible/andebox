# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
import subprocess

from ..context import ContextType
from ..exceptions import AndeboxException
from .base import AndeboxAction


class AnsibleTestAction(AndeboxAction):
    name = "test"
    help = "runs ansible-test in a temporary environment"
    args = [
        dict(
            names=("--keep", "-k"),
            specs=dict(
                action="store_true", help="keep temporary directory after execution"
            ),
        ),
        dict(
            names=("--exclude-from-ignore", "-efi", "-ei"),
            specs=dict(
                action="store_true",
                help="matching lines in ignore files will be filtered out",
            ),
        ),
        dict(
            names=("--skip-requirements", "-R"),
            specs=dict(
                action="store_true",
                help="skip installation of test requirements.yml",
            ),
        ),
        dict(
            names=("--galaxy-retry",),
            specs=dict(
                type=int,
                default=3,
                help="Number of times to retry requirements installation on failure (default: 3)",
            ),
        ),
        dict(
            names=("test",),
            specs=dict(
                choices=["sanity", "units", "integration"],
                help="test type",
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
                if (
                    context.type == ContextType.COLLECTION
                    and not context.args.skip_requirements
                ):
                    if context.args.test in ["units", "integration"]:
                        req_path = dict(
                            units=context.unit_test_subdir / "requirements.yml",
                            integration=context.integration_test_subdir
                            / "requirements.yml",
                        )
                        context.install_requirements(
                            reqs=req_path[context.args.test],
                            path=context.top_dir,
                            retries=context.args.galaxy_retry,
                        )
                if context.args.exclude_from_ignore:
                    context.exclude_from_ignore()
                print(
                    f"Running: {[context.ansible_test, context.args.test] + context.args.ansible_test_params}"
                )
                subprocess.run(
                    [context.ansible_test, context.args.test]
                    + context.args.ansible_test_params,
                    cwd=temp_dir,
                    check=True,
                )
        except Exception as e:
            raise AndeboxException(f"Error running ansible-test: {e}") from e
