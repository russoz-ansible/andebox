# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import argparse
import os
import re
from functools import partial

import yaml

from .base import AndeboxAction


PLUGIN_TYPES = ('connection', 'lookup', 'modules', 'doc_fragments', 'module_utils', 'callback', 'inventory')


def info_type(types, v):
    try:
        r = [t for t in types if t.startswith(v.lower())]
        return r[0][0].upper()
    except IndexError as e:
        raise argparse.ArgumentTypeError("invalid value: {0}".format(v)) from e


class RuntimeAction(AndeboxAction):
    RUNTIME_TYPES = ('redirect', 'tombstone', 'deprecation')
    name = "runtime"
    help = "returns information from runtime.yml"
    args = [
        dict(names=["--plugin-type", "-pt"],
             specs=dict(choices=PLUGIN_TYPES,
                        help="Specify the plugin type to be searched")),
        dict(names=["--regex", "--regexp", "-r"],
             specs=dict(action="store_true",
                        help="Treat plugin names as regular expressions")),
        dict(names=["--info-type", "-it"],
             specs=dict(type=partial(info_type, RUNTIME_TYPES),
                        help="Restrict type of response elements. Must be in {0}, may be shortened "
                             "down to one letter.".format(RUNTIME_TYPES))),
        dict(names=["plugin_names"],
             specs=dict(nargs='+')),
    ]
    name_tests = []
    current_version = None
    info_type = None

    def print_runtime(self, name, node):
        def is_info_type(_type):
            return self.info_type is None or self.info_type.lower() == _type.lower()

        redir, tomb, depre = [node.get(x) for x in self.RUNTIME_TYPES]
        if redir and is_info_type('R'):
            print('R {0}: redirected to {1}'.format(name, redir))
        elif tomb and is_info_type('T'):
            print('T {0}: terminated in {1}: {2}'.format(name, tomb['removal_version'], tomb['warning_text']))
        elif depre and is_info_type('D'):
            print('D {0}: deprecation in {1} (current={2}): {3}'.format(
                  name, depre['removal_version'], self.current_version, depre['warning_text']))

    def runtime_process_plugin(self, plugin_routing, plugin_types):
        for plugin_type in plugin_types:
            matching = [
                name
                for name in plugin_routing[plugin_type]
                if any(test(name) for test in self.name_tests)
            ]
            for name in matching:
                self.print_runtime('{0} {1}'.format(plugin_type, name), plugin_routing[plugin_type][name])

    def run(self, context, args):
        with open(os.path.join("meta", "runtime.yml")) as runtime_yml:
            runtime = yaml.safe_load(runtime_yml)

        plugin_types = [args.plugin_type] if args.plugin_type else PLUGIN_TYPES
        _, _, self.current_version = context.read_coll_meta()
        self.info_type = args.info_type

        def name_test(name, other):
            if name.endswith('.py'):
                name = name.split('/')[-1]
                name = name.split('.')[0]
            return name == other

        test_func = re.search if args.regex else name_test
        self.name_tests = [partial(test_func, n) for n in args.plugin_names]

        self.runtime_process_plugin(runtime['plugin_routing'], plugin_types)
