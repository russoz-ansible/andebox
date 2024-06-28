# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from collections import namedtuple

import pytest

# from andeboxlib.actions.ansibletest import AnsibleTestAction, AnsibleTestError


Args = namedtuple(
    "Args",
    ["keep", "exclude_from_ignore", "requirements", "venv", "ansible_test_params"],
    defaults=[False, False, False, None, []],
)
AndeboxTestCase = namedtuple("AndeboxTestCase", ["id", "args"])


@pytest.fixture
def patch_get_bin_path(mocker):
    """
    Function used for mocking AnsibleModule.get_bin_path
    """

    def mockie(self, path, *args, **kwargs):
        return f"/testbin/{path}"

    mocker.patch("ansible.module_utils.basic.AnsibleModule.get_bin_path", mockie)


TEST_CASES = [
    AndeboxTestCase(
        id="ansibletest-simple",
        args=Args(),
    )
]
TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.mark.parametrize(
    "testcase", [[x.args, x] for x in TEST_CASES], ids=TEST_CASES_IDS
)
def test_args(mocker, testcase):
    pass
