# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import subprocess

import yaml

from andeboxlib.actions.base import AndeboxAction
from andeboxlib.exceptions import AndeboxException


class AnsibleTestError(AndeboxException):
    pass


class AnsibleTestAction(AndeboxAction):
    name = "test"
    help = "runs ansible-test in a temporary environment"
    args = [
        dict(names=("--keep", "-k"),
             specs=dict(action="store_true", help="Keep temporary directory after execution")),
        dict(names=("--exclude-from-ignore", "-efi", "-ei"),
             specs=dict(action="store_true", help="Matching lines in ignore files will be filtered out")),
        dict(names=("--requirements", "-R"),
             specs=dict(action="store_true",
                        help="Install integration_tests_dependencies from tests/requirements.yml prior")),
        dict(names=("--venv", "-V"),
             specs=dict(help="""path to the virtual environment where andebox and ansible are installed""")),
        dict(names=("ansible_test_params", ),
             specs=dict(nargs="+")),
    ]

    @classmethod
    def make_parser(cls, subparser):
        action_parser = super(AnsibleTestAction, cls).make_parser(subparser)
        action_parser.epilog = "Notice the use of '--' to delimit andebox's options from ansible-test's"
        action_parser.usage = "%(prog)s usage: andebox test [-h] [--keep] -- [ansible_test_params ...]"

    def run(self, args):
        namespace, collection = self.determine_collection(args.collection)
        with self.ansible_collection_tree(namespace, collection, args.keep) as collection_dir:
            if args.requirements:
                self.install_requirements(args.venv)
            if args.exclude_from_ignore:
                self.exclude_from_ignore(args.exclude_from_ignore, args.ansible_test_params, collection_dir)
            rc = subprocess.call([self.binary_path(args.venv, "ansible-test")] + args.ansible_test_params, cwd=collection_dir)

            if rc != 0:
                raise AnsibleTestError("Error running ansible-test (rc={0})".format(rc))

    def exclude_from_ignore(self, exclude_from_ignore, ansible_test_params, coll_dir):
        files = [f for f in ansible_test_params if os.path.isfile(f)]
        print("Excluding from ignore files: {files}".format(files=files))
        if exclude_from_ignore:
            src_dir = os.path.join(os.getcwd(), 'tests', 'sanity')
            dest_dir = os.path.join(coll_dir, 'tests', 'sanity')
            with os.scandir(src_dir) as ts_dir:
                for ts_entry in ts_dir:
                    if ts_entry.name.startswith('ignore-') and ts_entry.name.endswith('.txt'):
                        self.copy_exclude_lines(os.path.join(src_dir, ts_entry.name),
                                                os.path.join(dest_dir, ts_entry.name),
                                                files)

    @staticmethod
    def install_requirements(venv):
        rc = subprocess.call([AnsibleTestAction.binary_path(venv, "ansible-galaxy"),
                              "collection",
                              "install",
                              "-r",
                              os.path.join('.', 'tests', 'integration', 'requirements.yml')])

        if rc != 0:
            raise AnsibleTestError("Error installing dependencies (rc={0})".format(rc))
