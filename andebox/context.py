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
from argparse import ArgumentParser
from argparse import Namespace
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Generator
from typing import List
from typing import Tuple
from typing import Type

import yaml
from git import Repo

from .exceptions import AndeboxException

toplevel_exclusion = (
    ".git",
    ".nox",
    ".tox",
    ".venv",
    ".virtualvenv",
    "venv",
    "virtualenv",
    "__pycache__",
    ".ansible",
    ".ruff_cache",
)


class AndeboxUnknownContext(AndeboxException):
    pass


class ContextType(Enum):
    ANSIBLE_CORE = 1
    COLLECTION = 2


class AbstractContext(ABC):
    _context_type: ContextType = None  # type: ignore

    def __init__(self, base_dir: Path, parser: ArgumentParser, args: Namespace) -> None:
        self.base_dir = base_dir
        self.parser = parser

        self.args = args
        self.venv = self.args.venv
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

    @abstractmethod
    def get_plugin_paths(self) -> List[str]:
        """Return list of plugin paths for this context type."""
        pass

    @abstractmethod
    def extract_plugin_type_from_path(self, file_path: str) -> str:
        """Extract plugin type from file path for this context type."""
        pass

    def get_default_branch(self) -> str:
        """Get the default branch for the current repository."""
        try:
            repo = Repo()
            # Check if we have remotes and can determine default branch
            if repo.remotes:
                try:
                    # Try to get the default branch from remote HEAD
                    for remote in repo.remotes:
                        try:
                            remote_head = remote.refs.HEAD
                            if remote_head.reference:
                                return remote_head.reference.name.split('/')[-1]
                        except Exception:
                            continue
                except Exception:
                    pass
            
            # Fallback: try to find the first available local branch
            try:
                if repo.refs:
                    # Return the first available branch
                    return repo.refs[0].name
            except Exception:
                pass
                
            # Final fallback - use HEAD if available
            try:
                return repo.head.reference.name
            except Exception:
                pass
                
        except Exception:
            pass
            
        # If all else fails, we can't determine the default branch
        raise AndeboxException("Unable to determine default branch for repository")


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

    def get_plugin_paths(self) -> List[str]:
        """Return plugin paths for ansible-core context by discovering them."""
        plugin_paths = []
        
        # Check for modules directory
        modules_path = Path("lib/ansible/modules")
        if modules_path.exists() and modules_path.is_dir():
            plugin_paths.append("lib/ansible/modules/")
        
        # Check for module_utils directory  
        module_utils_path = Path("lib/ansible/module_utils")
        if module_utils_path.exists() and module_utils_path.is_dir():
            plugin_paths.append("lib/ansible/module_utils/")
            
        # Check for plugins directory and discover plugin types
        plugins_base = Path("lib/ansible/plugins")
        if plugins_base.exists() and plugins_base.is_dir():
            for plugin_dir in plugins_base.iterdir():
                if plugin_dir.is_dir():
                    plugin_paths.append(f"lib/ansible/plugins/{plugin_dir.name}/")
        
        return plugin_paths

    def extract_plugin_type_from_path(self, file_path: str) -> str:
        """Extract plugin type from file path for ansible-core context."""
        plugin_paths = self.get_plugin_paths()
        for path in plugin_paths:
            if file_path.startswith(path):
                # For ansible-core: lib/ansible/modules/ -> modules
                # or lib/ansible/plugins/lookup/ -> lookup
                path_parts = path.split('/')
                if len(path_parts) >= 3:
                    if path_parts[2] == "modules":
                        return "modules"
                    elif len(path_parts) >= 4:
                        return path_parts[3]
                break
        return ""


class CollectionContext(AbstractContext):
    _context_type = ContextType.COLLECTION

    def __init__(self, base_dir: Path, parser: ArgumentParser, args: Namespace) -> None:
        super().__init__(base_dir, parser, args)
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

    def get_plugin_paths(self) -> List[str]:
        """Return plugin paths for collection context by discovering them."""
        plugin_paths = []
        
        # Check for plugins directory and discover plugin types
        plugins_base = Path("plugins")
        if plugins_base.exists() and plugins_base.is_dir():
            for plugin_dir in plugins_base.iterdir():
                if plugin_dir.is_dir():
                    plugin_paths.append(f"plugins/{plugin_dir.name}/")
        
        return plugin_paths

    def extract_plugin_type_from_path(self, file_path: str) -> str:
        """Extract plugin type from file path for collection context."""
        plugin_paths = self.get_plugin_paths()
        for path in plugin_paths:
            if file_path.startswith(path):
                # For collections: plugins/modules/ -> modules
                return path.split('/')[1]
        return ""


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
        raise AndeboxUnknownContext(f"Cannot determine context for: {cur_dir}") from e


def create_context(parser: ArgumentParser, args: Namespace) -> ConcreteContext:
    base_dir, basedir_type = _determine_base_dir()
    return basedir_type(base_dir, parser, args)
