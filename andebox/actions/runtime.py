# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
import re
from functools import partial
from pathlib import Path
from typing import List
from typing import Optional

import typer
import yaml

from ..context import andebox_context
from ..context import ContextType
from ..exceptions import AndeboxException


PLUGIN_TYPES = (
    "connection",
    "lookup",
    "modules",
    "doc_fragments",
    "module_utils",
    "callback",
    "inventory",
)
RUNTIME_TYPES = ("redirect", "tombstone", "deprecation")


def info_type_param(types, v):
    try:
        r = [t for t in types if t.startswith(v.lower())]
        return r[0][0].upper()
    except IndexError as e:
        raise typer.BadParameter(f"invalid value: {v}") from e


def _print_runtime(name, node, info_type, current_version):
    def is_info_type(_type):
        return info_type is None or info_type.lower() == _type.lower()

    redir, tomb, depre = [node.get(x) for x in RUNTIME_TYPES]
    if redir and is_info_type("R"):
        print(f"R {name}: redirected to {redir}")
    elif tomb and is_info_type("T"):
        print(
            f"T {name}: terminated in {tomb['removal_version']}: {tomb['warning_text']}"
        )
    elif depre and is_info_type("D"):
        print(
            f"D {name}: deprecation in {depre['removal_version']} (current={current_version}): {depre['warning_text']}"
        )


def _runtime_process_plugin(
    plugin_routing, plugin_types, name_tests, info_type, current_version
):
    for plugin_type in plugin_types:
        matching = [
            name
            for name in plugin_routing[plugin_type]
            if any(test(name) for test in name_tests)
        ]
        for name in matching:
            _print_runtime(
                f"{plugin_type} {name}",
                plugin_routing[plugin_type][name],
                info_type,
                current_version,
            )


app = typer.Typer(name="runtime", help="returns information from runtime.yml")


@app.callback(invoke_without_command=True)
def runtime_cmd(
    ctx: typer.Context,
    plugin_type: Optional[str] = typer.Option(
        None, "--plugin-type", "-pt", help="specify the plugin type to be searched"
    ),
    regex: bool = typer.Option(
        False,
        "--regex",
        "--regexp",
        "-r",
        help="treat plugin names as regular expressions",
    ),
    info_type: Optional[str] = typer.Option(
        None,
        "--info-type",
        "-it",
        help=f"restrict type of response elements. Must be one of {RUNTIME_TYPES}, and it may be shortened down to one letter.",
    ),
    plugin_names: List[str] = typer.Argument(...),
) -> None:
    parsed_info_type = (
        partial(info_type_param, RUNTIME_TYPES)(info_type) if info_type else None
    )

    with andebox_context(ctx) as context:
        if context.type != ContextType.COLLECTION:
            raise AndeboxException(
                "Action 'runtime' must be executed in a collection context!"
            )
        with open(Path("meta") / "runtime.yml") as runtime_yml:
            runtime = yaml.safe_load(runtime_yml)

        plugin_types = [plugin_type] if plugin_type else PLUGIN_TYPES
        _, _, current_version = context.read_coll_meta()  # type: ignore

        def name_test(name, other):
            if name.endswith(".py"):
                name = name.split("/")[-1]
                name = name.split(".")[0]
            return name == other

        test_func = re.search if regex else name_test
        name_tests = [partial(test_func, n) for n in plugin_names]

        _runtime_process_plugin(
            runtime["plugin_routing"],
            plugin_types,
            name_tests,
            parsed_info_type,
            current_version,
        )
