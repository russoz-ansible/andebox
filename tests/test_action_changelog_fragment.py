# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2025 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2025 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import pytest
from unittest.mock import Mock

from andebox.actions.changelog_fragment import ChangelogFragmentAction
from andebox.context import ContextType

from .utils import load_test_cases
from .utils import verify_patterns
from .utils import verify_return_code


# Unit tests for static utility methods
class TestChangelogFragmentUtilities:
    """Unit tests for utility methods that don't require git setup"""

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
        
        # Mock collection context
        collection_context = Mock()
        collection_context.type = ContextType.COLLECTION
        
        # Plugin files
        assert action.is_plugin_file("plugins/modules/test_module.py", collection_context) is True
        assert action.is_plugin_file("plugins/module_utils/helper.py", collection_context) is True
        assert action.is_plugin_file("plugins/lookup/test_lookup.py", collection_context) is True
        assert action.is_plugin_file("plugins/filter/test_filter.py", collection_context) is True
        assert action.is_plugin_file("plugins/callback/test_callback.py", collection_context) is True
        
        # Non-plugin files
        assert action.is_plugin_file("README.md", collection_context) is False
        assert action.is_plugin_file("tests/test_something.py", collection_context) is False
        assert action.is_plugin_file("docs/guide.rst", collection_context) is False
        assert action.is_plugin_file("galaxy.yml", collection_context) is False
        
        # Test ansible-core context
        ansible_core_context = Mock()
        ansible_core_context.type = ContextType.ANSIBLE_CORE
        
        assert action.is_plugin_file("lib/ansible/modules/test_module.py", ansible_core_context) is True
        assert action.is_plugin_file("lib/ansible/module_utils/helper.py", ansible_core_context) is True
        assert action.is_plugin_file("plugins/modules/test_module.py", ansible_core_context) is False

    def test_get_plugin_changes(self):
        """Test filtering changed files to plugin files only"""
        action = ChangelogFragmentAction()
        
        # Mock collection context
        collection_context = Mock()
        collection_context.type = ContextType.COLLECTION
        
        changed_files = {
            "plugins/modules/test_module.py",
            "plugins/module_utils/helper.py",
            "README.md",
            "tests/test_something.py",
            "plugins/lookup/test_lookup.py",
            "docs/guide.rst"
        }
        
        plugin_changes = action.get_plugin_changes(changed_files, collection_context)
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
        
        # Mock collection context
        collection_context = Mock()
        collection_context.type = ContextType.COLLECTION
        
        plugin_changes = [
            "plugins/modules/test_module.py",
            "plugins/module_utils/helper.py",
            "plugins/lookup/test_lookup.py"
        ]
        
        content = action.generate_fragment_content(plugin_changes, collection_context)
        
        assert "minor_changes" in content
        changes = content["minor_changes"]
        assert len(changes) == 3
        assert "Updated module ``test_module``" in changes
        assert "Updated module_util ``helper``" in changes
        assert "Updated lookup ``test_lookup``" in changes

    def test_generate_fragment_content_no_changes(self):
        """Test fragment content generation with no plugin changes"""
        action = ChangelogFragmentAction()
        
        # Mock collection context
        collection_context = Mock()
        collection_context.type = ContextType.COLLECTION
        
        content = action.generate_fragment_content([], collection_context)
        assert content == {}

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


# Integration tests using the project's test framework
TEST_CASES = load_test_cases(
    """
- id: main-branch-skip
  input:
    repo: https://github.com/ansible-collections/community.general.git
    args:
      - changelog-fragment
  expected:
    rc: 0
    in_stdout: >
      Skipping changelog fragment creation on main branch

- id: help-message
  input:
    repo: https://github.com/ansible-collections/community.general.git
    args:
      - changelog-fragment
      - --help
  expected:
    rc: 0
    in_stdout:
      - "generates changelog fragment from git branch name and changed plugin files"
      - "--fragment-dir"
      - "--force"
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_changelog_fragment(make_helper, git_repo, testcase, run_andebox):
    test = make_helper(
        testcase,
        git_repo,
        run_andebox,
        [verify_patterns, verify_return_code],
    )
    test.run()