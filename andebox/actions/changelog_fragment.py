# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2025 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2025 Alexei Znamensky
# SPDX-License-Identifier: MIT
import re
import subprocess
from pathlib import Path
from typing import List, Set

import yaml

from ..context import CollectionContext, ContextType
from ..exceptions import AndeboxException
from .base import AndeboxAction


class ChangelogFragmentAction(AndeboxAction):
    name = "changelog-fragment"
    help = "generates changelog fragment from git branch name and changed plugin files"
    args = [
        dict(
            names=["--fragment-dir", "-d"],
            specs=dict(
                default="changelogs/fragments",
                help="directory to store changelog fragments (default: changelogs/fragments)",
            ),
        ),
        dict(
            names=["--force", "-f"],
            specs=dict(
                action="store_true",
                help="force creation of fragment even if no plugin files changed",
            ),
        ),
    ]

    @staticmethod
    def sanitize_branch_name(branch_name: str) -> str:
        """Sanitize branch name for use as filename.
        
        Replace non-alphanumeric characters (except underscore and hyphen) with hyphens.
        Remove leading/trailing hyphens and collapse multiple consecutive hyphens.
        """
        # Replace non-alphanumeric chars except _ and - with -
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '-', branch_name)
        # Collapse multiple consecutive hyphens
        sanitized = re.sub(r'-+', '-', sanitized)
        # Remove leading/trailing hyphens
        sanitized = sanitized.strip('-')
        return sanitized

    @staticmethod
    def get_current_branch() -> str:
        """Get the current git branch name."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise AndeboxException(f"Failed to get current git branch: {e}")

    @staticmethod
    def get_changed_files(base_branch: str = None) -> Set[str]:
        """Get list of files changed compared to base branch."""
        try:
            # If no base branch specified, try to determine it
            if base_branch is None:
                # Try common default branch names
                for branch in ["main", "master"]:
                    try:
                        subprocess.run(
                            ["git", "rev-parse", "--verify", branch],
                            capture_output=True,
                            check=True,
                        )
                        base_branch = branch
                        break
                    except subprocess.CalledProcessError:
                        continue
                
                # If still no base branch found, use HEAD~1 or fall back to staged/unstaged
                if base_branch is None:
                    base_branch = "HEAD~1"
            
            # Try to get changes against the base branch
            try:
                result = subprocess.run(
                    ["git", "diff", "--name-only", f"{base_branch}..HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                branch_changes = set(result.stdout.strip().split('\n')) - {''}
                
                # Also get staged and unstaged changes
                result = subprocess.run(
                    ["git", "diff", "--name-only", "--cached"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                staged_files = set(result.stdout.strip().split('\n')) - {''}
                
                result = subprocess.run(
                    ["git", "diff", "--name-only"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                unstaged_files = set(result.stdout.strip().split('\n')) - {''}
                
                # Combine all changes
                changed_files = branch_changes | staged_files | unstaged_files
                
            except subprocess.CalledProcessError:
                # If comparison fails, fall back to staged and unstaged changes only
                result = subprocess.run(
                    ["git", "diff", "--name-only", "--cached"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                staged_files = set(result.stdout.strip().split('\n')) - {''}
                
                result = subprocess.run(
                    ["git", "diff", "--name-only"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                unstaged_files = set(result.stdout.strip().split('\n')) - {''}
                
                changed_files = staged_files | unstaged_files
            
            return changed_files
        except subprocess.CalledProcessError as e:
            raise AndeboxException(f"Failed to get changed files: {e}")

    @staticmethod
    def is_plugin_file(file_path: str) -> bool:
        """Check if a file is a plugin file based on its path."""
        plugin_paths = [
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
        return any(file_path.startswith(plugin_path) for plugin_path in plugin_paths)

    def get_plugin_changes(self, changed_files: Set[str]) -> List[str]:
        """Filter changed files to only include plugin files."""
        return [f for f in changed_files if self.is_plugin_file(f)]

    def generate_fragment_content(self, plugin_changes: List[str], branch_name: str) -> dict:
        """Generate changelog fragment content based on changed plugin files."""
        if not plugin_changes:
            return {}

        # Group changes by plugin type
        changes_by_type = {}
        for file_path in plugin_changes:
            parts = file_path.split('/')
            if len(parts) >= 3 and parts[0] == "plugins":
                plugin_type = parts[1]
                if plugin_type not in changes_by_type:
                    changes_by_type[plugin_type] = []
                
                # Extract plugin name (filename without extension)
                plugin_name = Path(parts[-1]).stem
                changes_by_type[plugin_type].append(plugin_name)

        # Create fragment content
        fragment = {}
        for plugin_type, plugins in changes_by_type.items():
            # Use appropriate changelog section based on plugin type
            if plugin_type == "modules":
                section = "minor_changes"
            elif plugin_type == "module_utils":
                section = "minor_changes"
            else:
                section = "minor_changes"
            
            if section not in fragment:
                fragment[section] = []
            
            for plugin in plugins:
                fragment[section].append(f"Updated {plugin_type.rstrip('s')} ``{plugin}``")

        return fragment

    def run(self, context: CollectionContext) -> None:
        if context.type != ContextType.COLLECTION:
            raise AndeboxException("changelog-fragment action can only be used in collection context")

        # Get current branch name
        branch_name = self.get_current_branch()
        
        # Skip if on main/master branch unless forced
        if branch_name in ['main', 'master'] and not context.args.force:
            print(f"Skipping changelog fragment creation on {branch_name} branch")
            return

        # Sanitize branch name for filename
        sanitized_branch = self.sanitize_branch_name(branch_name)
        if not sanitized_branch:
            raise AndeboxException(f"Branch name '{branch_name}' cannot be sanitized to a valid filename")

        # Get changed files
        changed_files = self.get_changed_files()
        
        # Filter to plugin files only
        plugin_changes = self.get_plugin_changes(changed_files)
        
        if not plugin_changes and not context.args.force:
            print("No plugin files changed, skipping changelog fragment creation")
            return

        # Generate fragment content
        fragment_content = self.generate_fragment_content(plugin_changes, branch_name)
        
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
                yaml.dump(fragment_content, f, default_flow_style=False, sort_keys=True)
            else:
                # Create minimal fragment for forced creation
                yaml.dump({"minor_changes": [f"Changes from branch {branch_name}"]}, f, default_flow_style=False)

        print(f"Created changelog fragment: {fragment_file}")