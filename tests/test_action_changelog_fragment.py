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

    def test_generate_fragment_content(self):
        """Test fragment content generation"""
        action = ChangelogFragmentAction()
        
        # Mock collection context
        collection_context = Mock()
        collection_context.type = ContextType.COLLECTION
        collection_context.extract_plugin_type_from_path.side_effect = lambda path: {
            "plugins/modules/test_module.py": "modules",
            "plugins/module_utils/helper.py": "module_utils",
            "plugins/lookup/test_lookup.py": "lookup"
        }.get(path, "")
        
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
      - "generates changelog fragment based on changed plugin files"
      - "--fragment-dir"
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