# -*- coding: utf-8 -*-
# (c) 2023, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import shutil
import sys
import tempfile
from contextlib import contextmanager

import yaml

coll_copy_exclusion = ('.git', '.tox', '.venv', '.virtualvenv', 'venv', 'virtualenv')


def _copy_collection(coll_dir):
    # copy files to tmp ansible coll dir
    with os.scandir() as it:
        for entry in it:
            if any(entry.name.startswith(x) for x in coll_copy_exclusion):
                continue
            if entry.is_dir():
                shutil.copytree(entry.name, os.path.join(coll_dir, entry.name), symlinks=True, ignore_dangling_symlinks=True)
            else:
                shutil.copy(entry.name, os.path.join(coll_dir, entry.name), follow_symlinks=False)


@contextmanager
def ansible_collection_tree(namespace, collection, keep=False):
    top_dir = ""
    coll_dir = ""
    try:
        top_dir = tempfile.mkdtemp(prefix="andebox.")
        coll_dir = os.path.join(top_dir, "ansible_collections", namespace, collection)
        os.makedirs(coll_dir)
        print(f"collection = {namespace}.{collection}", file=sys.stderr)
        print(f"directory  = {coll_dir}", file=sys.stderr)

        _copy_collection(coll_dir)
        os.putenv('ANSIBLE_COLLECTIONS_PATH', ':'.join([top_dir] + os.environ.get('ANSIBLE_COLLECTIONS_PATH', '').split(':')))
        yield coll_dir

    finally:
        if keep:
            print('Keeping temporary directory: {0}'.format(coll_dir))
        else:
            print('Removing temporary directory: {0}'.format(coll_dir))
            shutil.rmtree(top_dir)


def read_coll_meta():
    with open("galaxy.yml") as galaxy_meta:
        meta = yaml.load(galaxy_meta, Loader=yaml.BaseLoader)
    return meta['namespace'], meta['name'], meta['version']


def determine_collection(coll_arg):
    if coll_arg:
        coll_split = coll_arg.split('.')
        return '.'.join(coll_split[:-1]), coll_split[-1]
    return read_coll_meta()[:2]


def binary_path(venv, binary):
    _list = ([venv, "bin"] if venv else []) + [binary]
    return os.path.join(*_list)


def copy_exclude_lines(src, dest, exclusion_filenames):
    with open(src, "r") as src_file, open(dest, "w") as dest_file:
        for line in src_file.readlines():
            if not any(line.startswith(f) for f in exclusion_filenames):
                dest_file.write(line)
