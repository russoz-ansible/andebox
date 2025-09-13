# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2025 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2025 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import yaml

from andebox.actions.changelog_fragment import ChangelogFragmentAction
from andebox.context import CollectionContext, ContextType
from andebox.exceptions import AndeboxException


class TestChangelogFragmentAction:
    """Test class for ChangelogFragmentAction"""

    def test_sanitize_branch_name(self):
        """Test branch name sanitization"""
        action = ChangelogFragmentAction()
        
        # Basic alphanumeric
        assert action.sanitize_branch_name("feature-123") == "feature-123"
        assert action.sanitize_branch_name("feature_branch") == "feature_branch"
        
        # Special characters
        assert action.sanitize_branch_name("feature/fix-bug") == "feature-fix-bug"
        assert action.sanitize_branch_name("feature@hotfix") == "feature-hotfix"
        assert action.sanitize_branch_name("feature#123") == "feature-123"
        
        # Multiple special characters and consecutive hyphens
        assert action.sanitize_branch_name("feature///fix@bug###") == "feature-fix-bug"
        assert action.sanitize_branch_name("--feature--") == "feature"
        
        # Edge cases
        assert action.sanitize_branch_name("123") == "123"
        assert action.sanitize_branch_name("f") == "f"

    def test_is_plugin_file(self):
        """Test plugin file detection"""
        action = ChangelogFragmentAction()
        
        # Plugin files
        assert action.is_plugin_file("plugins/modules/test_module.py") is True
        assert action.is_plugin_file("plugins/module_utils/helper.py") is True
        assert action.is_plugin_file("plugins/lookup/test_lookup.py") is True
        assert action.is_plugin_file("plugins/filter/test_filter.py") is True
        assert action.is_plugin_file("plugins/callback/test_callback.py") is True
        
        # Non-plugin files
        assert action.is_plugin_file("README.md") is False
        assert action.is_plugin_file("tests/test_something.py") is False
        assert action.is_plugin_file("docs/guide.rst") is False
        assert action.is_plugin_file("galaxy.yml") is False

    def test_get_plugin_changes(self):
        """Test filtering changed files to plugin files only"""
        action = ChangelogFragmentAction()
        
        changed_files = {
            "plugins/modules/test_module.py",
            "plugins/module_utils/helper.py",
            "README.md",
            "tests/test_something.py",
            "plugins/lookup/test_lookup.py",
            "docs/guide.rst"
        }
        
        plugin_changes = action.get_plugin_changes(changed_files)
        expected = [
            "plugins/modules/test_module.py",
            "plugins/module_utils/helper.py", 
            "plugins/lookup/test_lookup.py"
        ]
        
        assert len(plugin_changes) == 3
        assert all(change in expected for change in plugin_changes)

    def test_generate_fragment_content(self):
        """Test fragment content generation"""
        action = ChangelogFragmentAction()
        
        plugin_changes = [
            "plugins/modules/test_module.py",
            "plugins/module_utils/helper.py",
            "plugins/lookup/test_lookup.py"
        ]
        
        content = action.generate_fragment_content(plugin_changes, "feature-branch")
        
        assert "minor_changes" in content
        changes = content["minor_changes"]
        assert len(changes) == 3
        assert "Updated module ``test_module``" in changes
        assert "Updated module_util ``helper``" in changes
        assert "Updated lookup ``test_lookup``" in changes

    def test_generate_fragment_content_no_changes(self):
        """Test fragment content generation with no plugin changes"""
        action = ChangelogFragmentAction()
        
        content = action.generate_fragment_content([], "feature-branch")
        assert content == {}

    @patch("andebox.actions.changelog_fragment.subprocess.run")
    def test_get_current_branch(self, mock_run):
        """Test getting current git branch"""
        action = ChangelogFragmentAction()
        
        # Mock successful git command
        mock_run.return_value = Mock(stdout="feature-branch\n", returncode=0)
        
        branch = action.get_current_branch()
        assert branch == "feature-branch"
        
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("andebox.actions.changelog_fragment.subprocess.run")
    def test_get_current_branch_error(self, mock_run):
        """Test error handling when getting current git branch"""
        action = ChangelogFragmentAction()
        
        # Mock git command failure
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")
        
        with pytest.raises(AndeboxException, match="Failed to get current git branch"):
            action.get_current_branch()

    @patch("andebox.actions.changelog_fragment.subprocess.run")
    def test_get_changed_files(self, mock_run):
        """Test getting changed files"""
        action = ChangelogFragmentAction()
        
        # Mock git diff output
        mock_run.return_value = Mock(
            stdout="plugins/modules/test.py\nREADME.md\nplugins/lookup/test.py\n",
            returncode=0
        )
        
        changed_files = action.get_changed_files()
        expected = {"plugins/modules/test.py", "README.md", "plugins/lookup/test.py"}
        assert changed_files == expected

    @patch("andebox.actions.changelog_fragment.subprocess.run")
    def test_get_changed_files_error(self, mock_run):
        """Test error handling when getting changed files"""
        action = ChangelogFragmentAction()
        
        # Mock git command failure
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")
        
        with pytest.raises(AndeboxException, match="Failed to get changed files"):
            action.get_changed_files()

    def test_run_wrong_context_type(self):
        """Test running action with wrong context type"""
        action = ChangelogFragmentAction()
        
        # Mock non-collection context
        context = Mock()
        context.type = ContextType.ANSIBLE_CORE
        
        with pytest.raises(AndeboxException, match="can only be used in collection context"):
            action.run(context)

    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_current_branch")
    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_changed_files")
    def test_run_main_branch_skip(self, mock_get_changed_files, mock_get_current_branch, capsys):
        """Test skipping fragment creation on main branch"""
        action = ChangelogFragmentAction()
        
        mock_get_current_branch.return_value = "main"
        
        # Mock collection context
        context = Mock()
        context.type = ContextType.COLLECTION
        context.args = Mock()
        context.args.force = False
        
        action.run(context)
        
        captured = capsys.readouterr()
        assert "Skipping changelog fragment creation on main branch" in captured.out

    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_current_branch")
    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_changed_files")
    def test_run_no_plugin_changes(self, mock_get_changed_files, mock_get_current_branch, capsys):
        """Test skipping fragment creation when no plugin files changed"""
        action = ChangelogFragmentAction()
        
        mock_get_current_branch.return_value = "feature-branch"
        mock_get_changed_files.return_value = {"README.md", "tests/test.py"}
        
        # Mock collection context
        context = Mock()
        context.type = ContextType.COLLECTION
        context.args = Mock()
        context.args.force = False
        
        action.run(context)
        
        captured = capsys.readouterr()
        assert "No plugin files changed, skipping changelog fragment creation" in captured.out

    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_current_branch")
    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_changed_files")
    def test_run_create_fragment(self, mock_get_changed_files, mock_get_current_branch, capsys):
        """Test successful fragment creation"""
        action = ChangelogFragmentAction()
        
        mock_get_current_branch.return_value = "feature/fix-bug"
        mock_get_changed_files.return_value = {
            "plugins/modules/test_module.py",
            "README.md"
        }
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            fragment_dir = Path(temp_dir) / "changelogs" / "fragments"
            
            # Mock collection context
            context = Mock()
            context.type = ContextType.COLLECTION
            context.args = Mock()
            context.args.force = False
            context.args.fragment_dir = str(fragment_dir)
            
            action.run(context)
            
            # Check fragment was created
            fragment_file = fragment_dir / "feature-fix-bug.yml"
            assert fragment_file.exists()
            
            # Check fragment content
            with fragment_file.open() as f:
                content = yaml.safe_load(f)
            
            assert "minor_changes" in content
            assert "Updated module ``test_module``" in content["minor_changes"]
            
            captured = capsys.readouterr()
            assert f"Created changelog fragment: {fragment_file}" in captured.out

    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_current_branch")
    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_changed_files")
    def test_run_force_no_changes(self, mock_get_changed_files, mock_get_current_branch, capsys):
        """Test forced fragment creation with no plugin changes"""
        action = ChangelogFragmentAction()
        
        mock_get_current_branch.return_value = "feature-branch"
        mock_get_changed_files.return_value = {"README.md"}
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            fragment_dir = Path(temp_dir) / "changelogs" / "fragments"
            
            # Mock collection context with force=True
            context = Mock()
            context.type = ContextType.COLLECTION
            context.args = Mock()
            context.args.force = True
            context.args.fragment_dir = str(fragment_dir)
            
            action.run(context)
            
            # Check fragment was created
            fragment_file = fragment_dir / "feature-branch.yml"
            assert fragment_file.exists()
            
            # Check fragment content
            with fragment_file.open() as f:
                content = yaml.safe_load(f)
            
            assert "minor_changes" in content
            assert "Changes from branch feature-branch" in content["minor_changes"]

    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_current_branch")
    @patch("andebox.actions.changelog_fragment.ChangelogFragmentAction.get_changed_files")
    def test_run_existing_fragment(self, mock_get_changed_files, mock_get_current_branch, capsys):
        """Test skipping when fragment file already exists"""
        action = ChangelogFragmentAction()
        
        mock_get_current_branch.return_value = "feature-branch"
        mock_get_changed_files.return_value = {"plugins/modules/test.py"}
        
        # Create temporary directory with existing fragment
        with tempfile.TemporaryDirectory() as temp_dir:
            fragment_dir = Path(temp_dir) / "changelogs" / "fragments"
            fragment_dir.mkdir(parents=True)
            
            # Create existing fragment file
            fragment_file = fragment_dir / "feature-branch.yml"
            fragment_file.write_text("existing: content\n")
            
            # Mock collection context
            context = Mock()
            context.type = ContextType.COLLECTION
            context.args = Mock()
            context.args.force = False
            context.args.fragment_dir = str(fragment_dir)
            
            action.run(context)
            
            # Check original content is preserved
            assert fragment_file.read_text() == "existing: content\n"
            
            captured = capsys.readouterr()
            assert f"Fragment file {fragment_file} already exists, skipping" in captured.out

    def test_special_characters_in_branch_name(self):
        """Test handling of special characters in branch names"""
        action = ChangelogFragmentAction()
        
        test_cases = [
            ("feature/fix-bug#123", "feature-fix-bug-123"),
            ("hotfix@2024.01.15", "hotfix-2024-01-15"),
            ("user/feature!important", "user-feature-important"),
            ("fix$$$bug", "fix-bug"),
            ("feature___test", "feature___test"),  # underscores preserved
            ("my-feature-branch", "my-feature-branch"),  # hyphens preserved
        ]
        
        for input_branch, expected in test_cases:
            assert action.sanitize_branch_name(input_branch) == expected


# Integration test using a temporary git repository
class TestChangelogFragmentIntegration:
    """Integration tests using temporary git repositories"""
    
    def setup_git_repo(self, temp_dir: Path) -> None:
        """Set up a temporary git repository"""
        os.chdir(temp_dir)
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        
        # Create initial commit
        (temp_dir / "README.md").write_text("# Test Collection\n")
        subprocess.run(["git", "add", "README.md"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

    def test_integration_create_fragment_with_plugin_changes(self, capsys):
        """Integration test: create fragment with actual git repo and plugin changes"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            self.setup_git_repo(temp_path)
            
            # Create a feature branch
            subprocess.run(["git", "checkout", "-b", "feature/new-module"], check=True)
            
            # Create plugin file and make changes
            plugins_dir = temp_path / "plugins" / "modules"
            plugins_dir.mkdir(parents=True)
            
            module_file = plugins_dir / "test_module.py"
            module_file.write_text("# Test module\n")
            
            subprocess.run(["git", "add", str(module_file)], check=True)
            
            # Create collection context
            action = ChangelogFragmentAction()
            context = Mock()
            context.type = ContextType.COLLECTION
            context.args = Mock()
            context.args.force = False
            context.args.fragment_dir = "changelogs/fragments"
            
            action.run(context)
            
            # Check fragment was created
            fragment_file = temp_path / "changelogs" / "fragments" / "feature-new-module.yml"
            assert fragment_file.exists()
            
            with fragment_file.open() as f:
                content = yaml.safe_load(f)
            
            assert "minor_changes" in content
            assert "Updated module ``test_module``" in content["minor_changes"]

    def test_integration_no_plugin_changes(self, capsys):
        """Integration test: no fragment creation when no plugin files changed"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            self.setup_git_repo(temp_path)
            
            # Create a feature branch
            subprocess.run(["git", "checkout", "-b", "docs-update"], check=True)
            
            # Make non-plugin changes
            docs_file = temp_path / "docs" / "guide.rst"
            docs_file.parent.mkdir(parents=True)
            docs_file.write_text("Documentation update\n")
            
            subprocess.run(["git", "add", str(docs_file)], check=True)
            
            # Create collection context
            action = ChangelogFragmentAction()
            context = Mock()
            context.type = ContextType.COLLECTION
            context.args = Mock()
            context.args.force = False
            context.args.fragment_dir = "changelogs/fragments"
            
            action.run(context)
            
            # Check no fragment was created
            fragment_dir = temp_path / "changelogs" / "fragments"
            if fragment_dir.exists():
                assert not any(fragment_dir.glob("*.yml"))
            
            captured = capsys.readouterr()
            assert "No plugin files changed, skipping changelog fragment creation" in captured.out