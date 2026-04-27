# code: language=python tabSize=4
#
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import typer

from ..context import ContextType, andebox_context


def printline(title, content):
    print(f"{title:>20}: {content}")


app = typer.Typer(name="context", help="returns information from running context")


@app.callback(invoke_without_command=True)
def context_cmd(ctx: typer.Context) -> None:
    with andebox_context(ctx) as context:
        printline("Base dir", context.base_dir)
        if context.venv:
            printline("Venv", context.venv)
        printline("Type", context.type)
        printline("Temp dir", context.top_dir)
        printline("ansible-test", context.ansible_test)
        printline("Sanity tests", context.sanity_test_subdir)
        printline("Integration tests", context.integration_test_subdir)

        if context.type == ContextType.COLLECTION:
            ns, name, version = context.read_coll_meta()  # type: ignore
            printline("Collection", f"{ns}.{name} {version}")
