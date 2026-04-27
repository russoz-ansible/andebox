# code: language=python tabSize=4
#
# (C) 2026 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2026 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
from unittest.mock import MagicMock

import pytest

from andebox.actions.noxtest import VERSION_MATRIX, register_sessions, select_sessions, session_name

from .utils import load_test_cases


@pytest.mark.parametrize(
    "ac_ver,py,expected",
    [
        ("2.17", "3.12", "ac2.17-p3.12"),
        ("devel", "3.13", "acdevel-p3.13"),
    ],
)
def test_session_name(ac_ver, py, expected):
    assert session_name(ac_ver, py) == expected


TEST_CASES_SELECT = load_test_cases(
    """
- id: no-filters
  input:
    ansible_cores: null
    pythons: null
  expected:
    sessions: null

- id: empty-filters
  input:
    ansible_cores: []
    pythons: []
  expected:
    sessions: null

- id: ansible-core-only
  input:
    ansible_cores: ["2.18"]
    pythons: null
  expected:
    sessions: ["ac2.18-p3.11", "ac2.18-p3.12", "ac2.18-p3.13"]

- id: python-only
  input:
    ansible_cores: null
    pythons: ["3.12"]
  expected:
    sessions:
      - ac2.18-p3.12
      - ac2.19-p3.12
      - ac2.20-p3.12
      - ac2.21-p3.12

- id: valid-combination
  input:
    ansible_cores: ["2.18"]
    pythons: ["3.12"]
  expected:
    sessions: ["ac2.18-p3.12"]

- id: invalid-combination
  input:
    ansible_cores: ["2.18"]
    pythons: ["3.14"]
  expected:
    sessions: null

- id: unknown-ansible-core
  input:
    ansible_cores: ["2.99"]
    pythons: null
  expected:
    sessions: null

- id: unknown-python
  input:
    ansible_cores: null
    pythons: ["3.99"]
  expected:
    sessions: null

- id: devel-valid-python
  input:
    ansible_cores: ["devel"]
    pythons: ["3.13"]
  expected:
    sessions: ["acdevel-p3.13"]

- id: devel-invalid-python
  input:
    ansible_cores: ["devel"]
    pythons: ["3.9"]
  expected:
    sessions: null

- id: multiple-cores-single-python
  input:
    ansible_cores: ["2.18", "2.19"]
    pythons: ["3.12"]
  expected:
    sessions: ["ac2.18-p3.12", "ac2.19-p3.12"]

- id: single-core-filters-out-unsupported-pythons
  input:
    ansible_cores: ["2.18"]
    pythons: ["3.11", "3.12", "3.13"]
  expected:
    sessions: ["ac2.18-p3.11", "ac2.18-p3.12", "ac2.18-p3.13"]
"""
)
TEST_CASES_SELECT_IDS = [tc.id for tc in TEST_CASES_SELECT]


@pytest.mark.parametrize("testcase", TEST_CASES_SELECT, ids=TEST_CASES_SELECT_IDS)
def test_select_sessions(testcase):
    result = select_sessions(
        testcase.input["ansible_cores"],
        testcase.input["pythons"],
    )
    assert result == testcase.expected.get("sessions")


@pytest.fixture
def nox_mocks():
    nox_mock = MagicMock()
    register_sessions(nox_mock)
    return nox_mock


def test_register_sessions_called_once_per_matrix_entry(nox_mocks):
    nox_mock = nox_mocks
    total = sum(len(pys) for _, _, pys in VERSION_MATRIX)
    assert nox_mock.session.call_count == total


def test_register_sessions_names_match_matrix(nox_mocks):
    nox_mock = nox_mocks
    registered = {c.kwargs["name"] for c in nox_mock.session.call_args_list}
    assert registered == {session_name(ver, py) for ver, _, all_pys in VERSION_MATRIX for py in all_pys}


def test_register_sessions_python_matches_matrix(nox_mocks):
    nox_mock = nox_mocks
    registered = {c.kwargs["name"]: c.kwargs["python"] for c in nox_mock.session.call_args_list}
    for ac_ver, _, all_pys in VERSION_MATRIX:
        for py in all_pys:
            assert registered[session_name(ac_ver, py)] == py


def test_register_sessions_default_matches_matrix(nox_mocks):
    nox_mock = nox_mocks
    registered = {c.kwargs["name"]: c.kwargs["default"] for c in nox_mock.session.call_args_list}
    for ac_ver, default_py, all_pys in VERSION_MATRIX:
        for py in all_pys:
            assert registered[session_name(ac_ver, py)] == (py == default_py)


def test_register_sessions_decorator_applied_to_callable(nox_mocks):
    nox_mock = nox_mocks
    decorator = nox_mock.session.return_value
    for call in decorator.call_args_list:
        assert callable(call.args[0])


def test_register_sessions_func_passes_posargs_to_andebox_test(nox_mocks):
    """Session func runs `andebox test *posargs` — the `--` separator in the
    nox invocation is the only mechanism that controls what posargs contain."""
    nox_mock = nox_mocks
    decorator = nox_mock.session.return_value
    posargs = ["sanity", "--docker", "default"]
    for call in decorator.call_args_list:
        func = call.args[0]
        session = MagicMock()
        session.posargs = posargs
        func(session)
        session.run.assert_called_once_with("andebox", "test", *posargs, external=True)


def test_register_sessions_func_name_matches_session_name(nox_mocks):
    nox_mock = nox_mocks
    decorator = nox_mock.session.return_value
    for i, c in enumerate(nox_mock.session.call_args_list):
        func = decorator.call_args_list[i].args[0]
        assert func.__name__ == c.kwargs["name"]
