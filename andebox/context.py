# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2023 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2023 Alexei Znamensky
# SPDX-License-Identifier: MIT
import os
import shutil
import subprocess
import sys
import tempfile
import time
from abc import ABC
from abc import abstractmethod
from argparse import Namespace
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Generator
from typing import Tuple
from typing import Type

import yaml

from .exceptions import AndeboxException

toplevel_exclusion = (".git", ".tox", ".venv", ".virtualvenv", "venv", "virtualenv")


class AndeboxUnknownContext(AndeboxException):
    pass


class ContextType(Enum):
    ANSIBLE_CORE = 1
    COLLECTION = 2


class AbstractContext(ABC):
    _context_type: ContextType = None  # type: ignore

    def __init__(self, base_dir: Path, args: Namespace) -> None:
        self.base_dir = base_dir
        self.args = args
        self.venv = args.venv
        self.top_dir = Path(tempfile.mkdtemp(prefix="andebox."))

    @property
    def type(self) -> ContextType:
        return self._context_type  # type: ignore

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
    def tests_subdir(self) -> Path:
        return Path("tests")

    @property
    def sanity_test_subdir(self) -> Path:
        return self.tests_subdir / "sanity"

    @property
    def unit_test_subdir(self) -> Path:
        return self.tests_subdir / "unit"

    @property
    def integration_test_subdir(self) -> Path:
        return self.tests_subdir / "integration"

    def install_requirements(self, reqs: Path, path: Path | None, retries: int) -> None:
        pass

    @abstractmethod
    def post_sub_dir(self, top_dir: Path) -> None:
        pass

    def copy_tree(self) -> None:
        # copy files to tmp ansible coll dir
        with os.scandir() as it:
            for entry in it:
                if any(entry.name.startswith(x) for x in toplevel_exclusion):
                    continue
                if entry.is_dir():
                    shutil.copytree(
                        entry.name,
                        self.full_dir / entry.name,
                        symlinks=True,
                        ignore_dangling_symlinks=True,
                    )
                else:
                    shutil.copy(
                        entry.name,
                        self.full_dir / entry.name,
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

    def copy_exclude_lines(
        self, src: Path, dest: Path, exclusion_filenames: list[str]
    ) -> None:
        with src.open("r") as src_file, dest.open("w") as dest_file:
            for line in src_file.readlines():
                if not any(line.startswith(f) for f in exclusion_filenames):
                    dest_file.write(line)

    def binary_path(self, binary: str) -> str:
        if self.args.venv:
            return str(Path(self.args.venv) / "bin" / binary)

        return str(Path(binary))

    def exclude_from_ignore(self) -> None:
        files = [f for f in self.args.ansible_test_params if Path(f).is_file()]
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
                            src_dir / ts_entry.name,
                            dest_dir / ts_entry.name,
                            files,
                        )


class AnsibleCoreContext(AbstractContext):
    _context_type = ContextType.ANSIBLE_CORE

    @property
    def ansible_test(self) -> str:
        return str(self.top_dir / "bin" / "ansible-test")

    @property
    def sub_dir(self) -> str:
        return ""

    def post_sub_dir(self, top_dir: Path) -> None:
        pass

    @property
    def tests_subdir(self) -> Path:
        return Path("test")

    @property
    def unit_test_subdir(self) -> Path:
        return self.tests_subdir / "units"


class CollectionContext(AbstractContext):
    _context_type = ContextType.COLLECTION

    def __init__(self, base_dir: Path, args: Namespace) -> None:
        super().__init__(base_dir, args)
        self.name = self.version = ""
        self.namespace, self.collection = self.determine_collection(
            self.args.collection
        )

    @property
    def ansible_test(self) -> str:
        return self.binary_path("ansible-test")

    @property
    def sub_dir(self) -> Path:
        coll_dir = Path("ansible_collections") / self.namespace / self.collection
        return coll_dir

    def post_sub_dir(self, top_dir: Path) -> None:
        print(f"collection = {self.namespace}.{self.collection}", file=sys.stderr)
        os.putenv(
            "ANSIBLE_COLLECTIONS_PATH",
            ":".join(
                [str(top_dir)]
                + os.environ.get("ANSIBLE_COLLECTIONS_PATH", "").split(":")
            ),
        )

    def read_coll_meta(self) -> tuple[str, str, str]:
        with open("galaxy.yml") as galaxy_meta:
            meta = yaml.safe_load(galaxy_meta)
        self.namespace, self.name, self.version = (
            meta["namespace"],
            meta["name"],
            meta["version"],
        )
        return meta["namespace"], meta["name"], meta["version"]

    def determine_collection(self, coll_arg: str) -> tuple[str, str]:
        if coll_arg:
            coll_split = coll_arg.split(".")
            return ".".join(coll_split[:-1]), coll_split[-1]
        return self.read_coll_meta()[:2]

    def install_requirements(self, reqs: Path, path: Path | None, retries: int) -> None:
        # reqs = self.integration_test_subdir / "requirements.yml"
        if not reqs.exists():
            print(f"Cannot find requirements file: {reqs}")
            return

        print(f"Installing requirements ({reqs})", end="")
        if path:
            print(f" at path: {path}")
        else:
            print("")
        path_arg = ["-p", f"{path}"] if path else []

        cmd = (
            [self.binary_path("ansible-galaxy"), "collection", "install"]
            + path_arg
            + ["-r", f"{reqs}", "-vvv", "--force"]
        )
        print(f"Running: {cmd}")
        delay = 10
        for attempt in range(1, retries + 1):
            try:
                subprocess.run(cmd, check=True)
                break
            except subprocess.CalledProcessError:
                if attempt == retries:
                    raise
                print(
                    f"Install requirements failed (attempt {attempt}/{retries}), retrying in {delay}s..."
                )
                time.sleep(delay)


ConcreteContextType = Type[AnsibleCoreContext] | Type[CollectionContext]
ConcreteContext = AnsibleCoreContext | CollectionContext


def _base_dir_type(
    dir_: Path,
) -> ConcreteContextType:
    if (dir_ / "bin" / "ansible-playbook").exists():
        return AnsibleCoreContext
    if (dir_ / "meta" / "runtime.yml").exists():
        return CollectionContext
    raise ValueError()


def _determine_base_dir_rec(
    dir_: Path,
) -> Tuple[Path, ConcreteContextType]:
    try:
        return dir_, _base_dir_type(dir_)
    except ValueError:
        if dir_ == Path(dir_.anchor):
            raise AndeboxUnknownContext()  # pylint: disable=raise-missing-from
        return _determine_base_dir_rec(dir_.parent)


def _determine_base_dir() -> Tuple[Path, ConcreteContextType]:
    cur_dir = Path.cwd()
    try:
        return _determine_base_dir_rec(cur_dir)
    except AndeboxUnknownContext as e:
        raise AndeboxUnknownContext(
            f"Cannot determine current directory context: f{cur_dir}"
        ) from e


def create_context(args: Namespace) -> ConcreteContext:
    base_dir, basedir_type = _determine_base_dir()
    return basedir_type(base_dir, args)
