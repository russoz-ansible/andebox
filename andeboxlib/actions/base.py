# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import shutil
import sys
import tempfile
from contextlib import contextmanager

import yaml


class AndeboxAction:
    name = None
    help = None
    args = []  # of dict(names=[]: specs={})
    coll_copy_exclusion = ('.git', '.tox', '.venv', '.virtualvenv', 'venv', 'virtualenv')

    @staticmethod
    def copy_collection(coll_dir):
        # copy files to tmp ansible coll dir
        with os.scandir() as it:
            for entry in it:
                if any(entry.name.startswith(x) for x in AndeboxAction.coll_copy_exclusion):
                    continue
                if entry.is_dir():
                    shutil.copytree(entry.name, os.path.join(coll_dir, entry.name))
                else:
                    shutil.copy(entry.name, os.path.join(coll_dir, entry.name))

    @contextmanager
    def ansible_collection_tree(self, namespace, collection, keep=False):
        top_dir = ""
        coll_dir = ""
        try:
            top_dir = tempfile.mkdtemp(prefix="andebox.")
            coll_dir = os.path.join(top_dir, "ansible_collections", namespace, collection)
            os.makedirs(coll_dir)
            print("{0:10} = {1}.{2}".format("collection", namespace, collection), file=sys.stderr)
            print("{0:10} = {1}".format("directory", coll_dir), file=sys.stderr)

            self.copy_collection(coll_dir)
            os.putenv('ANSIBLE_COLLECTIONS_PATH', ':'.join([top_dir] + os.environ.get('ANSIBLE_COLLECTIONS_PATH', '').split(':')))
            yield coll_dir

        finally:
            if not keep:
                print('Removing temporary directory: {0}'.format(coll_dir))
                shutil.rmtree(top_dir)
            else:
                print('Keeping temporary directory: {0}'.format(coll_dir))

    def make_parser(self, subparser):
        action_parser = subparser.add_parser(self.name, help=self.help)
        for arg in self.args:
            action_parser.add_argument(*arg['names'], **arg['specs'])
        return action_parser

    def run(self, args):
        raise NotImplementedError()

    @staticmethod
    def read_coll_meta():
        with open("galaxy.yml") as galaxy_meta:
            meta = yaml.load(galaxy_meta, Loader=yaml.BaseLoader)
        return meta['namespace'], meta['name'], meta['version']

    def determine_collection(self, coll_arg):
        if coll_arg:
            coll_split = coll_arg.split('.')
            return '.'.join(coll_split[:-1]), coll_split[-1]
        return self.read_coll_meta()[:2]

    @staticmethod
    def copy_exclude_lines(src, dest, exclusion_filenames):
        with open(src, "r") as src_file, open(dest, "w") as dest_file:
            for line in src_file.readlines():
                if not any(line.startswith(f) for f in exclusion_filenames):
                    dest_file.write(line)

    def __str__(self):
        return "<AndeboxAction: {name}>".format(name=self.name)
