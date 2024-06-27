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

toplevel_exclusion = ('.git', '.tox', '.venv', '.virtualvenv', 'venv', 'virtualenv')


class AndeboxUnknownContext(AndeboxException):
    pass


class AbstractContext(ABC):

    def __init__(self, base_dir, args) -> None:
        self.base_dir = base_dir
        self.args = args
        self.venv = args.venv
        self.top_dir = Path(tempfile.mkdtemp(prefix="andebox."))


    @property
    @abstractmethod
    def ansible_test(self) -> Path:
        pass

    @property
    @abstractmethod
    def sub_dir(self, args) -> Path:
        pass

    @abstractmethod
    def post_sub_dir(self, top_dir):
        pass

    def copy_tree(self, full_dir):
        # copy files to tmp ansible coll dir
        with os.scandir() as it:
            for entry in it:
                if any(entry.name.startswith(x) for x in toplevel_exclusion):
                    continue
                if entry.is_dir():
                    shutil.copytree(entry.name, os.path.join(full_dir, entry.name), symlinks=True, ignore_dangling_symlinks=True)
                else:
                    shutil.copy(entry.name, os.path.join(full_dir, entry.name), follow_symlinks=False)

    @contextmanager
    def temp_tree(self):
        full_dir = self.top_dir / self.sub_dir
        os.makedirs(full_dir)
        print(f"directory  = {full_dir}", file=sys.stderr)
        self.copy_tree(full_dir)

        self.post_sub_dir(self.top_dir)
        yield full_dir

        if self.args.keep:
            print(f'Keeping temporary directory: {full_dir}')
        else:
            print(f'Removing temporary directory: {full_dir}')
            shutil.rmtree(self.top_dir)

    def copy_exclude_lines(self, src, dest, exclusion_filenames):
        with open(src, "r") as src_file, open(dest, "w") as dest_file:
            for line in src_file.readlines():
                if not any(line.startswith(f) for f in exclusion_filenames):
                    dest_file.write(line)

    def binary_path(self, venv, binary):
        _list = ([venv, "bin"] if venv else []) + [binary]
        return os.path.join(*_list)


class AnsibleCoreContext(AbstractContext):
    @property
    def ansible_test(self) -> Path:
        return Path.cwd() / Path("bin") / Path("ansible-test")


class CollectionContext(AbstractContext):
    @property
    def ansible_test(self) -> Path:
        return self.venv / Path("bin") / Path("ansible-test")

    @property
    def sub_dir(self):
        namespace, collection = self.determine_collection(self.args.collection)
        coll_dir = Path("ansible_collections") / namespace / collection
        print(f"collection = {namespace}.{collection}", file=sys.stderr)
        return coll_dir

    def post_sub_dir(self, top_dir):
        os.putenv('ANSIBLE_COLLECTIONS_PATH',
                  ':'.join(
                      [str(top_dir)] +
                      os.environ.get('ANSIBLE_COLLECTIONS_PATH', '').split(':'))
        )

    def read_coll_meta(self):
        with open("galaxy.yml") as galaxy_meta:
            meta = yaml.safe_load(galaxy_meta)
        self.namespace, self.name, self.version = meta['namespace'], meta['name'], meta['version']
        return meta['namespace'], meta['name'], meta['version']

    def determine_collection(self, coll_arg):
        if coll_arg:
            coll_split = coll_arg.split('.')
            return '.'.join(coll_split[:-1]), coll_split[-1]
        return self.read_coll_meta()[:2]


class Context:
    class Type(Enum):
        ANSIBLE_CORE = AnsibleCoreContext
        COLLECTION = CollectionContext

    @staticmethod
    def create(args) -> AbstractContext:
        base_dir, basedir_type = Context.determine_base_dir()
        return (basedir_type.value)(base_dir, args)

    @staticmethod
    def base_dir_type(dir_) -> Literal[Type.ANSIBLE_CORE, Type.COLLECTION, None]:
        if (dir_ / Path("bin") / Path("ansible-playbook")).exists():
            return Context.Type.ANSIBLE_CORE
        if (dir_ / Path("meta") / Path("runtime.yml")).exists():
            return Context.Type.COLLECTION
        return None

    @staticmethod
    def _determine_base_dir(dir_: Path) -> Tuple[Path, Literal[Type.ANSIBLE_CORE, Type.COLLECTION]]:
        dir_type = Context.base_dir_type(dir_)
        if dir_type is None:
            if dir_ == dir_.anchor:
                raise AndeboxUnknownContext()
            return Context._determine_base_dir(dir_.parent)
        return dir_, dir_type

    @staticmethod
    def determine_base_dir():
        cur_dir = Path.cwd()
        try:
            return Context._determine_base_dir(cur_dir)
        except AndeboxUnknownContext as e:
            raise AndeboxUnknownContext(f"Cannot determine current directory context: f{cur_dir}") from e
