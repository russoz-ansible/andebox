# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
import argparse
import re
from functools import partial
from pathlib import Path

import yaml

from ..context import CollectionContext
from ..context import ContextType
from ..exceptions import AndeboxException
from .base import AndeboxAction


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
        raise argparse.ArgumentTypeError("invalid value: {v}") from e


class RuntimeAction(AndeboxAction):
    name = "runtime"
    help = "returns information from runtime.yml"
    args = [
        dict(
            names=["--plugin-type", "-pt"],
            specs=dict(
                choices=PLUGIN_TYPES, help="specify the plugin type to be searched"
            ),
        ),
        dict(
            names=["--regex", "--regexp", "-r"],
            specs=dict(
                action="store_true", help="treat plugin names as regular expressions"
            ),
        ),
        dict(
            names=["--info-type", "-it"],
            specs=dict(
                type=partial(info_type_param, RUNTIME_TYPES),
                help=f"restrict type of response elements. Must be one of {RUNTIME_TYPES}, "
                "and it may be shortened down to one letter.",
            ),
        ),
        dict(names=["plugin_names"], specs=dict(nargs="+")),
    ]
    name_tests = []
    current_version = None
    info_type = None

    def print_runtime(self, name, node):
        def is_info_type(_type):
            return self.info_type is None or self.info_type.lower() == _type.lower()

        redir, tomb, depre = [node.get(x) for x in RUNTIME_TYPES]
        if redir and is_info_type("R"):
            print(f"R {name}: redirected to {redir}")
        elif tomb and is_info_type("T"):
            print(
                f"T {name}: terminated in {tomb['removal_version']}: {tomb['warning_text']}"
            )
        elif depre and is_info_type("D"):
            print(
                f"D {name}: deprecation in {depre['removal_version']} (current={self.current_version}): {depre['warning_text']}"
            )

    def runtime_process_plugin(self, plugin_routing, plugin_types):
        for plugin_type in plugin_types:
            matching = [
                name
                for name in plugin_routing[plugin_type]
                if any(test(name) for test in self.name_tests)
            ]
            for name in matching:
                self.print_runtime(
                    f"{plugin_type} {name}", plugin_routing[plugin_type][name]
                )

    def run(self, context: CollectionContext):
        if context.type != ContextType.COLLECTION:
            raise AndeboxException(
                "Action 'runtime' must be executed in a collection context!"
            )
        with open(Path("meta") / "runtime.yml") as runtime_yml:
            runtime = yaml.safe_load(runtime_yml)

        plugin_types = (
            [context.args.plugin_type] if context.args.plugin_type else PLUGIN_TYPES
        )
        _, _, self.current_version = context.read_coll_meta()
        self.info_type = context.args.info_type

        def name_test(name, other):
            if name.endswith(".py"):
                name = name.split("/")[-1]
                name = name.split(".")[0]
            return name == other

        test_func = re.search if context.args.regex else name_test
        self.name_tests = [partial(test_func, n) for n in context.args.plugin_names]

        self.runtime_process_plugin(runtime["plugin_routing"], plugin_types)
