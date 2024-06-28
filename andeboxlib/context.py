# -*- coding: utf-8 -*-
# (c) 2023, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import shutil
import sys
import tempfile
from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from pathlib import Path

import yaml

from .exceptions import AndeboxException

toplevel_exclusion = (".git", ".tox", ".venv", ".virtualvenv", "venv", "virtualenv")


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
    def ansible_test(self) -> str:
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
                    shutil.copytree(
                        entry.name,
                        os.path.join(full_dir, entry.name),
                        symlinks=True,
                        ignore_dangling_symlinks=True,
                    )
                else:
                    shutil.copy(
                        entry.name,
                        os.path.join(full_dir, entry.name),
                        follow_symlinks=False,
                    )

    @contextmanager
    def temp_tree(self):
        full_dir = self.top_dir / self.sub_dir
        full_dir.mkdir(parents=True, exist_ok=True)
        print(f"directory  = {full_dir}", file=sys.stderr)
        self.copy_tree(full_dir)

        self.post_sub_dir(self.top_dir)

        yield full_dir

        if self.args.keep:
            print(f"Keeping temporary directory: {full_dir}")
        else:
            print(f"Removing temporary directory: {full_dir}")
            shutil.rmtree(self.top_dir)

    def copy_exclude_lines(self, src, dest, exclusion_filenames):
        with open(src, "r") as src_file, open(dest, "w") as dest_file:
            for line in src_file.readlines():
                if not any(line.startswith(f) for f in exclusion_filenames):
                    dest_file.write(line)

    def binary_path(self, binary) -> Path:
        if self.args.venv:
            return str(Path(self.args.venv) / "bin" / binary)
        else:
            return str(Path(binary))


class AnsibleCoreContext(AbstractContext):
    @property
    def ansible_test(self):
        return str(self.top_dir / "bin" / "ansible-test")

    @property
    def sub_dir(self):
        return ""

    def post_sub_dir(self, top_dir):
        pass


class CollectionContext(AbstractContext):
    @property
    def ansible_test(self):
        return self.binary_path("ansible-test")

    @property
    def sub_dir(self):
        namespace, collection = self.determine_collection(self.args.collection)
        coll_dir = Path("ansible_collections") / namespace / collection
        print(f"collection = {namespace}.{collection}", file=sys.stderr)
        return coll_dir

    def post_sub_dir(self, top_dir):
        os.putenv(
            "ANSIBLE_COLLECTIONS_PATH",
            ":".join(
                [str(top_dir)]
                + os.environ.get("ANSIBLE_COLLECTIONS_PATH", "").split(":")
            ),
        )

    def read_coll_meta(self):
        with open("galaxy.yml") as galaxy_meta:
            meta = yaml.safe_load(galaxy_meta)
        self.namespace, self.name, self.version = (
            meta["namespace"],
            meta["name"],
            meta["version"],
        )
        return meta["namespace"], meta["name"], meta["version"]

    def determine_collection(self, coll_arg):
        if coll_arg:
            coll_split = coll_arg.split(".")
            return ".".join(coll_split[:-1]), coll_split[-1]
        return self.read_coll_meta()[:2]


def _base_dir_type(dir_):
    if (dir_ / "bin" / "ansible-playbook").exists():
        return AnsibleCoreContext
    if (dir_ / "meta" / "runtime.yml").exists():
        return CollectionContext
    raise ValueError()


def _determine_base_dir_rec(
    dir_: Path,
):
    try:
        return dir_, _base_dir_type(dir_)
    except ValueError:
        if dir_ == dir_.anchor:
            raise AndeboxUnknownContext()
        return _determine_base_dir_rec(dir_.parent)


def _determine_base_dir():
    cur_dir = Path.cwd()
    try:
        return _determine_base_dir_rec(cur_dir)
    except AndeboxUnknownContext as e:
        raise AndeboxUnknownContext(
            f"Cannot determine current directory context: f{cur_dir}"
        ) from e


class Context:
    @staticmethod
    def create(args) -> AbstractContext:
        base_dir, basedir_type = _determine_base_dir()
        return (basedir_type)(base_dir, args)
