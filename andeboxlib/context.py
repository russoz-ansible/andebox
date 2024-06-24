# -*- coding: utf-8 -*-
# (c) 2023, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import shutil
import sys
import tempfile
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Tuple, Literal
from abc import ABC, abstractmethod

import yaml

from .exceptions import AndeboxException

coll_copy_exclusion = ('.git', '.tox', '.venv', '.virtualvenv', 'venv', 'virtualenv')


class AndeboxUnknownContext(AndeboxException):
    pass


class BaseContextDriver(ABC):

    def __init__(self, venv) -> None:
        self.venv = venv

    @property
    @abstractmethod
    def ansible_test(self) -> Path:
        pass

    def _copy_collection(self, coll_dir):
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
    def ansible_collection_tree(self, namespace, collection, keep=False):
        top_dir = ""
        coll_dir = ""
        try:
            top_dir = tempfile.mkdtemp(prefix="andebox.")
            coll_dir = os.path.join(top_dir, "ansible_collections", namespace, collection)
            os.makedirs(coll_dir)
            print(f"collection = {namespace}.{collection}", file=sys.stderr)
            print(f"directory  = {coll_dir}", file=sys.stderr)

            self._copy_collection(coll_dir)
            os.putenv('ANSIBLE_COLLECTIONS_PATH', ':'.join([top_dir] + os.environ.get('ANSIBLE_COLLECTIONS_PATH', '').split(':')))
            yield coll_dir

        finally:
            if keep:
                print('Keeping temporary directory: {0}'.format(coll_dir))
            else:
                print('Removing temporary directory: {0}'.format(coll_dir))
                shutil.rmtree(top_dir)


class AnsibleCoreContextDriver(BaseContextDriver):
    @property
    def ansible_test(self) -> Path:
        return Path.cwd() / Path("bin") / Path("ansible-test")


class CollectionContextDriver(BaseContextDriver):
    @property
    def ansible_test(self) -> Path:
        return self.venv / Path("bin") / Path("ansible-test")


class RoleContextDriver(BaseContextDriver):
    pass


class Context:
    class Type(Enum):
        ANSIBLE_CORE = AnsibleCoreContextDriver
        COLLECTION = CollectionContextDriver
        ROLE = RoleContextDriver

    def __init__(self, args) -> None:
        self.base_dir, self.basedir_type = self.determine_base_dir()
        self.driver = (self.basedir_type.value)(venv=args.venv)

    @staticmethod
    def base_dir_type(dir_):
        if (dir_ / Path("bin") / Path("ansible-playbook")).exists():
            return Context.Type.ANSIBLE_CORE
        if (dir_ / Path("meta") / Path("runtime.yml")).exists():
            return Context.Type.COLLECTION
        # if (dir_ / Path("meta") / Path("main.yml")).exists():
        #     return Context.Type.ROLE
        return None

    def _determine_base_dir(self, dir_: Path) -> Tuple[Path, Literal[Type.ANSIBLE_CORE, Type.COLLECTION]]:
        dir_type = self.base_dir_type(dir_)
        if dir_type is None:
            if dir_ == dir_.anchor:
                raise AndeboxUnknownContext()
            return self._determine_base_dir(dir_.parent)
        return dir_, dir_type

    def determine_base_dir(self):
        cur_dir = Path.cwd()
        try:
            return self._determine_base_dir(cur_dir)
        except AndeboxUnknownContext as e:
            raise AndeboxUnknownContext(f"Cannot determine current directory context: f{cur_dir}") from e

    def ansible_collection_tree(self, *args, **kwargs):
        return self.driver.ansible_collection_tree(*args, **kwargs)

    def read_coll_meta(self):
        with open("galaxy.yml") as galaxy_meta:
            meta = yaml.safe_load(galaxy_meta)
        return meta['namespace'], meta['name'], meta['version']

    def determine_collection(self, coll_arg):
        if coll_arg:
            coll_split = coll_arg.split('.')
            return '.'.join(coll_split[:-1]), coll_split[-1]
        return self.read_coll_meta()[:2]

    def copy_exclude_lines(self, src, dest, exclusion_filenames):
        with open(src, "r") as src_file, open(dest, "w") as dest_file:
            for line in src_file.readlines():
                if not any(line.startswith(f) for f in exclusion_filenames):
                    dest_file.write(line)

    def binary_path(self, venv, binary):
        _list = ([venv, "bin"] if venv else []) + [binary]
        return os.path.join(*_list)
