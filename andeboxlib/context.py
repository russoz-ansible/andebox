# -*- coding: utf-8 -*-
# (c) 2023, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import shutil
import subprocess
import sys
import tempfile
from abc import ABC
from abc import abstractmethod
from argparse import Namespace
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from typing import Generator
from typing import Type
from typing import Union

import yaml

from .exceptions import AndeboxException

toplevel_exclusion = (".git", ".tox", ".venv", ".virtualvenv", "venv", "virtualenv")


class AndeboxUnknownContext(AndeboxException):
    pass


class AbstractContext(ABC):
    UNSET = 0
    ANSIBLE_CORE = 1
    COLLECTION = 2
    _context_type = UNSET

    @property
    def type(self):
        return self._context_type

    def __init__(self, base_dir: Path, args: Namespace) -> None:
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
    def sub_dir(self) -> str:
        pass

    @property
    def full_dir(self) -> Path:
        return self.top_dir / self.sub_dir

    @property
    @abstractmethod
    def tests_subdir(self) -> Path:
        pass

    @property
    def sanity_test_subdir(self) -> Path:
        return self.tests_subdir / "sanity"

    @property
    def integration_test_subdir(self) -> Path:
        return self.tests_subdir / "integration"

    def install_requirements(self):
        reqs = self.integration_test_subdir / "requirements.yml"
        if reqs.exists():
            subprocess.run(
                [
                    self.binary_path("ansible-galaxy"),
                    "collection",
                    "install",
                    "-r",
                    f"{reqs}",
                ],
                check=True,
            )
        else:
            print(f"Cannot find requirements file: {reqs}")

    @abstractmethod
    def post_sub_dir(self, top_dir: Path):
        pass

    def copy_tree(self):
        # copy files to tmp ansible coll dir
        with os.scandir() as it:
            for entry in it:
                if any(entry.name.startswith(x) for x in toplevel_exclusion):
                    continue
                if entry.is_dir():
                    shutil.copytree(
                        entry.name,
                        os.path.join(self.full_dir, entry.name),
                        symlinks=True,
                        ignore_dangling_symlinks=True,
                    )
                else:
                    shutil.copy(
                        entry.name,
                        os.path.join(self.full_dir, entry.name),
                        follow_symlinks=False,
                    )

    @contextmanager
    def temp_tree(self) -> Generator[Path, Any, Any]:
        self.full_dir.mkdir(parents=True, exist_ok=True)
        print(f"directory  = {self.full_dir}", file=sys.stderr)
        self.copy_tree()

        self.post_sub_dir(self.top_dir)

        yield self.full_dir

        if self.args.keep:
            print(f"Keeping temporary directory: {self.full_dir}")
        else:
            print(f"Removing temporary directory: {self.full_dir}")
            shutil.rmtree(self.top_dir)

    def copy_exclude_lines(self, src, dest, exclusion_filenames):
        with open(src, "r") as src_file, open(dest, "w") as dest_file:
            for line in src_file.readlines():
                if not any(line.startswith(f) for f in exclusion_filenames):
                    dest_file.write(line)

    def binary_path(self, binary) -> str:
        if self.args.venv:
            return str(Path(self.args.venv) / "bin" / binary)

        return str(Path(binary))

    def exclude_from_ignore(self):
        files = [f for f in self.args.ansible_test_params if os.path.isfile(f)]
        print(f"Excluding from ignore files: {files}")
        if self.args.exclude_from_ignore:
            src_dir = Path.cwd() / self.sanity_test_subdir
            dest_dir = self.full_dir / self.sanity_test_subdir
            with os.scandir(src_dir) as ts_dir:
                for ts_entry in ts_dir:
                    if ts_entry.name.startswith("ignore") and ts_entry.name.endswith(
                        ".txt"
                    ):
                        self.copy_exclude_lines(
                            os.path.join(src_dir, ts_entry.name),
                            os.path.join(dest_dir, ts_entry.name),
                            files,
                        )


class AnsibleCoreContext(AbstractContext):
    context_type = AbstractContext.ANSIBLE_CORE

    @property
    def ansible_test(self):
        return str(self.top_dir / "bin" / "ansible-test")

    @property
    def sub_dir(self):
        return ""

    def post_sub_dir(self, top_dir):
        pass

    @property
    def tests_subdir(self):
        return Path("test")

    def install_requirements(self):
        pass


class CollectionContext(AbstractContext):
    context_type = AbstractContext.COLLECTION

    def __init__(self, base_dir, args) -> None:
        super().__init__(base_dir, args)
        self.name = self.version = ""
        self.namespace, self.collection = self.determine_collection(
            self.args.collection
        )

    @property
    def ansible_test(self):
        return self.binary_path("ansible-test")

    @property
    def sub_dir(self):
        coll_dir = Path("ansible_collections") / self.namespace / self.collection
        return coll_dir

    def post_sub_dir(self, top_dir):
        print(f"collection = {self.namespace}.{self.collection}", file=sys.stderr)
        os.putenv(
            "ANSIBLE_COLLECTIONS_PATH",
            ":".join(
                [str(top_dir)]
                + os.environ.get("ANSIBLE_COLLECTIONS_PATH", "").split(":")
            ),
        )

    @property
    def tests_subdir(self):
        return Path("tests")

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


ConcreteContexts = Union[AnsibleCoreContext, CollectionContext]


def _base_dir_type(
    dir_: Path,
) -> Union[Type[AnsibleCoreContext], Type[CollectionContext]]:
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
            raise AndeboxUnknownContext()  # pylint: disable=raise-missing-from
        return _determine_base_dir_rec(dir_.parent)


def _determine_base_dir():
    cur_dir = Path.cwd()
    try:
        return _determine_base_dir_rec(cur_dir)
    except AndeboxUnknownContext as e:
        raise AndeboxUnknownContext(
            f"Cannot determine current directory context: f{cur_dir}"
        ) from e


def create_context(args: Namespace) -> ConcreteContexts:
    base_dir, basedir_type = _determine_base_dir()
    return (basedir_type)(base_dir, args)
