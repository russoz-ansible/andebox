# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
import subprocess
from typing import List
from typing import Optional

import typer

from ..context import andebox_context
from ..context import ContextType


app = typer.Typer(
    name="test",
    help="runs ansible-test in a temporary environment",
)


@app.callback(invoke_without_command=True)
def ansible_test_cmd(
    ctx: typer.Context,
    keep: bool = typer.Option(
        False, "--keep", "-k", help="keep temporary directory after execution"
    ),
    exclude_from_ignore: bool = typer.Option(
        False,
        "--exclude-from-ignore",
        "-efi",
        "-ei",
        help="matching lines in ignore files will be filtered out (sanity tests)",
    ),
    skip_requirements: bool = typer.Option(
        False,
        "--skip-requirements",
        "-R",
        help="skip installation of test requirements.yml (unit/integration tests)",
    ),
    galaxy_retry: int = typer.Option(
        3,
        "--galaxy-retry",
        help="Number of times to retry requirements installation on failure (default: 3)",
    ),
    test: str = typer.Argument(
        ..., help="test type", metavar="[sanity|units|integration]"
    ),
    ansible_test_params: Optional[List[str]] = typer.Argument(None),
) -> None:
    if skip_requirements and test == "sanity":
        typer.echo(
            "andebox: error: --skip-requirements/-R cannot be used with 'sanity' test",
            err=True,
        )
        raise typer.Exit(2)
    if exclude_from_ignore and test != "sanity":
        typer.echo(
            "andebox: error: --exclude-from-ignore/-ei can only be used with 'sanity' test",
            err=True,
        )
        raise typer.Exit(2)

    params = ansible_test_params or []

    with andebox_context(ctx, make_temp_tree=True, keep=keep) as context:
        if context.type == ContextType.COLLECTION and not skip_requirements:
            if test in ["units", "integration"]:
                req_path = dict(
                    units=context.unit_test_subdir / "requirements.yml",
                    integration=context.integration_test_subdir / "requirements.yml",
                )
                context.install_requirements(
                    reqs=req_path[test],
                    path=context.top_dir,
                    retries=galaxy_retry,
                )
        if exclude_from_ignore:
            context.exclude_from_ignore(params)
        print(f"Running: {[context.ansible_test, test] + params}")
        subprocess.run(
            [context.ansible_test, test] + params,
            cwd=context.full_dir,
            check=True,
        )
