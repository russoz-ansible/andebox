# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2025 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2025 Alexei Znamensky
# SPDX-License-Identifier: MIT
import re
from pathlib import Path
from typing import List, Set

import yaml
from git import Repo

from ..context import ConcreteContext, ContextType
from ..exceptions import AndeboxException
from .base import AndeboxAction


class ChangelogFragmentAction(AndeboxAction):
    name = "changelog-fragment"
    help = (
        "generates changelog fragment from git branch name and changed "
        "plugin files"
    )
    args = [
        dict(
            names=["--fragment-dir", "-d"],
            specs=dict(
                default="changelogs/fragments",
                help=(
                    "directory to store changelog fragments "
                    "(default: changelogs/fragments)"
                ),
            ),
        ),
        dict(
            names=["--force", "-f"],
            specs=dict(
                action="store_true",
                help=(
                    "force creation of fragment even if no plugin files "
                    "changed"
                ),
            ),
        ),
    ]

    @staticmethod
    def sanitize_branch_name(branch_name: str) -> str:
        # Replace non-alphanumeric chars except _ and - with -
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '-', branch_name)
        # Collapse multiple consecutive hyphens
        sanitized = re.sub(r'-+', '-', sanitized)
        # Remove leading/trailing hyphens
        sanitized = sanitized.strip('-')
        return sanitized

    @staticmethod
    def get_current_branch() -> str:
        try:
            repo = Repo(search_parent_directories=True)
            return repo.active_branch.name
        except Exception as e:
            raise AndeboxException(f"Failed to get current git branch: {e}")

    @staticmethod
    def get_changed_files(base_branch: str = None) -> Set[str]:
        try:
            repo = Repo(search_parent_directories=True)

            # If no base branch specified, try to determine it
            if base_branch is None:
                base_branch = ChangelogFragmentAction._get_base_branch(repo)

            # Get changes from base branch to current
            changed_files = set()
            try:
                base_commit = repo.commit(base_branch)
                head_commit = repo.head.commit

                # Get files changed between base and HEAD
                for item in base_commit.diff(head_commit):
                    if item.a_path:
                        changed_files.add(item.a_path)
                    if item.b_path:
                        changed_files.add(item.b_path)

            except Exception:
                # If comparison fails, only use staged/unstaged changes
                pass

            # Always include staged and unstaged changes
            changed_files.update(
                ChangelogFragmentAction._get_staged_unstaged_files(repo)
            )

            return changed_files

        except Exception as e:
            raise AndeboxException(f"Failed to get changed files: {e}")

    @staticmethod
    def _get_base_branch(repo) -> str:
        # Try common default branch names
        for branch in ["main", "master"]:
            try:
                repo.commit(branch)
                return branch
            except Exception:
                continue
        return "HEAD~1"

    @staticmethod
    def _get_staged_unstaged_files(repo) -> Set[str]:
        changed_files = set()

        # Get unstaged changes
        for item in repo.index.diff(None):
            if item.a_path:
                changed_files.add(item.a_path)
            if item.b_path:
                changed_files.add(item.b_path)

        # Get staged changes
        for item in repo.index.diff("HEAD"):
            if item.a_path:
                changed_files.add(item.a_path)
            if item.b_path:
                changed_files.add(item.b_path)

        return changed_files

    @staticmethod
    def get_plugin_paths(context: ConcreteContext) -> List[str]:
        if context.type == ContextType.COLLECTION:
            return [
                "plugins/modules/",
                "plugins/module_utils/",
                "plugins/lookup/",
                "plugins/filter/",
                "plugins/test/",
                "plugins/callback/",
                "plugins/connection/",
                "plugins/inventory/",
                "plugins/action/",
                "plugins/cache/",
                "plugins/become/",
                "plugins/cliconf/",
                "plugins/doc_fragments/",
                "plugins/httpapi/",
                "plugins/netconf/",
                "plugins/shell/",
                "plugins/strategy/",
                "plugins/terminal/",
                "plugins/vars/",
            ]
        elif context.type == ContextType.ANSIBLE_CORE:
            return [
                "lib/ansible/modules/",
                "lib/ansible/module_utils/",
                "lib/ansible/plugins/lookup/",
                "lib/ansible/plugins/filter/",
                "lib/ansible/plugins/test/",
                "lib/ansible/plugins/callback/",
                "lib/ansible/plugins/connection/",
                "lib/ansible/plugins/inventory/",
                "lib/ansible/plugins/action/",
                "lib/ansible/plugins/cache/",
                "lib/ansible/plugins/become/",
                "lib/ansible/plugins/cliconf/",
                "lib/ansible/plugins/doc_fragments/",
                "lib/ansible/plugins/httpapi/",
                "lib/ansible/plugins/netconf/",
                "lib/ansible/plugins/shell/",
                "lib/ansible/plugins/strategy/",
                "lib/ansible/plugins/terminal/",
                "lib/ansible/plugins/vars/",
            ]
        else:
            return []

    def is_plugin_file(self, file_path: str, context: ConcreteContext) -> bool:
        plugin_paths = self.get_plugin_paths(context)
        return any(file_path.startswith(plugin_path) for plugin_path in plugin_paths)

    def get_plugin_changes(
        self, changed_files: Set[str], context: ConcreteContext
    ) -> List[str]:
        return [f for f in changed_files if self.is_plugin_file(f, context)]

    def generate_fragment_content(
        self, plugin_changes: List[str], context: ConcreteContext
    ) -> dict:
        if not plugin_changes:
            return {}

        # Group changes by plugin type
        changes_by_type = {}
        plugin_paths = self.get_plugin_paths(context)

        for file_path in plugin_changes:
            plugin_type = self._extract_plugin_type(
                file_path, plugin_paths, context
            )

            if plugin_type:
                if plugin_type not in changes_by_type:
                    changes_by_type[plugin_type] = []

                # Extract plugin name (filename without extension)
                plugin_name = Path(file_path).stem
                changes_by_type[plugin_type].append(plugin_name)

        # Create fragment content
        fragment = {}
        for plugin_type, plugins in changes_by_type.items():
            section = "minor_changes"  # Use minor_changes for all plugin types

            if section not in fragment:
                fragment[section] = []

            for plugin in plugins:
                entry = f"Updated {plugin_type.rstrip('s')} ``{plugin}``"
                fragment[section].append(entry)

        return fragment

    def _extract_plugin_type(
        self,
        file_path: str,
        plugin_paths: List[str],
        context: ConcreteContext
    ) -> str:
        # Find which plugin path this file matches
        for path in plugin_paths:
            if file_path.startswith(path):
                # Extract plugin type from path
                if context.type == ContextType.COLLECTION:
                    # For collections: plugins/modules/ -> modules
                    return path.split('/')[1]
                elif context.type == ContextType.ANSIBLE_CORE:
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

    @staticmethod
    def get_default_branch() -> str:
        try:
            repo = Repo(search_parent_directories=True)
            # Try common default branch names
            for branch in ["main", "master"]:
                try:
                    repo.commit(branch)
                    return branch
                except Exception:
                    continue
            # If neither exists, return the first remote tracking branch
            if repo.remotes:
                for ref in repo.remotes.origin.refs:
                    if ref.name in ['origin/main', 'origin/master']:
                        return ref.name.split('/')[-1]
            return "main"  # fallback
        except Exception:
            return "main"  # fallback

    def run(self, context: ConcreteContext) -> None:
        # Get current branch name
        branch_name = self.get_current_branch()

        # Skip if on default branch unless forced
        default_branch = self.get_default_branch()
        if branch_name == default_branch and not context.args.force:
            print(
                f"Skipping changelog fragment creation on {branch_name} branch"
            )
            return

        # Sanitize branch name for filename
        sanitized_branch = self.sanitize_branch_name(branch_name)
        if not sanitized_branch:
            raise AndeboxException(
                f"Branch name '{branch_name}' cannot be sanitized to a "
                "valid filename"
            )

        # Get changed files
        changed_files = self.get_changed_files()

        # Filter to plugin files only
        plugin_changes = self.get_plugin_changes(changed_files, context)

        if not plugin_changes and not context.args.force:
            print("No plugin files changed, skipping changelog fragment creation")
            return

        # Generate fragment content
        fragment_content = self.generate_fragment_content(plugin_changes, context)

        if not fragment_content and not context.args.force:
            print("No changes to generate fragment content for")
            return

        # Ensure fragment directory exists
        fragment_dir = Path(context.args.fragment_dir)
        fragment_dir.mkdir(parents=True, exist_ok=True)

        # Create fragment file
        fragment_file = fragment_dir / f"{sanitized_branch}.yml"

        if fragment_file.exists():
            print(f"Fragment file {fragment_file} already exists, skipping")
            return

        # Write fragment content
        with fragment_file.open('w') as f:
            if fragment_content:
                yaml.dump(
                    fragment_content, f, default_flow_style=False, sort_keys=True
                )
            else:
                # Create minimal fragment for forced creation
                yaml.dump(
                    {"minor_changes": ["Changes from current branch"]},
                    f,
                    default_flow_style=False
                )

        print(f"Created changelog fragment: {fragment_file}")
