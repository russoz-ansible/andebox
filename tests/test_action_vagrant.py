# code: language=python tabSize=4
#
# (C) 2026 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2026 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
from unittest.mock import MagicMock

import pytest

from .utils import GenericTestCase, load_test_cases, verify_return_code


def _make_collection(path):
    (path / "meta").mkdir(parents=True)
    (path / "meta" / "runtime.yml").write_text("requires_ansible: '>=2.18'\n")
    (path / "galaxy.yml").write_text("namespace: test\nname: coll\nversion: 1.0.0\n")


def _make_vagrant_mocks(mocker):
    mock_vagrant_cls = mocker.patch("vagrant.Vagrant")
    mock_v = mock_vagrant_cls.return_value
    mock_v.up.return_value = iter([])
    mock_v.user.return_value = "vagrant"
    mock_v.hostname.return_value = "127.0.0.1"
    mock_v.port.return_value = 2222
    mock_v.keyfile.return_value = "/tmp/key"

    mock_conn_cls = mocker.patch("andebox.actions.vagrant.Connection")
    mock_c = mock_conn_cls.return_value.__enter__.return_value
    mock_c.cd.return_value = MagicMock()
    mock_c.cd.return_value.__enter__ = MagicMock(return_value=None)
    mock_c.cd.return_value.__exit__ = MagicMock(return_value=False)

    return mock_v, mock_c


TEST_CASES = load_test_cases(
    """
- id: basic-run
  input:
    args: [vagrant]
  expected:
    rc: 0
    up_vm_name: default
    destroy_called: false

- id: custom-vm-name
  input:
    args: [vagrant, --name, myvm]
  expected:
    rc: 0
    up_vm_name: myvm

- id: sudo
  input:
    args: [vagrant, --sudo]
  expected:
    rc: 0
    cmd_starts_with: "sudo -HE "

- id: destroy
  input:
    args: [vagrant, --destroy]
  expected:
    rc: 0
    destroy_called: true

- id: missing-vagrantfile
  input:
    args: [vagrant]
    has_vagrantfile: false
  expected:
    rc: 1

- id: import-error
  input:
    args: [vagrant]
    import_error: "No module named vagrant"
  expected:
    rc: 1

- id: connection-error
  input:
    args: [vagrant]
    connection_error: "SSH connection failed"
  expected:
    rc: 1
"""
)

TEST_CASES_IDS = [tc.id for tc in TEST_CASES]


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_vagrant_command(make_helper, testcase, run_andebox, tmp_path, mocker):
    def setup(tc):
        _make_collection(tmp_path)

        if import_error_msg := tc.input.get("import_error"):
            mocker.patch("andebox.actions.vagrant.IMPORT_ERROR", ImportError(import_error_msg))
            return {"basedir": tmp_path}

        mock_v, mock_c = _make_vagrant_mocks(mocker)

        if connection_error_msg := tc.input.get("connection_error"):
            mock_conn_cls = mocker.patch("andebox.actions.vagrant.Connection")
            mock_conn_cls.return_value.__enter__.side_effect = RuntimeError(connection_error_msg)

        if tc.input.get("has_vagrantfile", True):
            (tmp_path / "Vagrantfile").write_text("# Vagrantfile\n")

        return {"basedir": tmp_path, "mock_v": mock_v, "mock_c": mock_c}

    def verify_up_vm_name(tc):
        up_vm_name = tc.expected.get("up_vm_name")
        if up_vm_name and "mock_v" in tc.data:
            tc.data["mock_v"].up.assert_called_once_with(vm_name=up_vm_name, stream_output=True)

    def verify_cmd(tc):
        cmd_starts_with = tc.expected.get("cmd_starts_with")
        if cmd_starts_with and "mock_c" in tc.data:
            cmd = tc.data["mock_c"].run.call_args[0][0]
            assert cmd.startswith(cmd_starts_with)

    def verify_destroy(tc):
        destroy_called = tc.expected.get("destroy_called")
        if destroy_called is not None and "mock_v" in tc.data:
            if destroy_called:
                tc.data["mock_v"].destroy.assert_called_once()
            else:
                tc.data["mock_v"].destroy.assert_not_called()

    test = make_helper(
        testcase,
        setup,
        run_andebox,
        [verify_return_code, verify_up_vm_name, verify_cmd, verify_destroy],
    )
    test.run()


def test_vagrant_run_contains_integration(make_helper, run_andebox, tmp_path, mocker):
    testcase = GenericTestCase(id="run-integration", input={"args": ["vagrant"]}, expected={})

    def setup(tc):
        _make_collection(tmp_path)
        mock_v, mock_c = _make_vagrant_mocks(mocker)
        (tmp_path / "Vagrantfile").write_text("# Vagrantfile\n")
        return {"basedir": tmp_path, "mock_c": mock_c}

    def verify_integration(tc):
        cmd = tc.data["mock_c"].run.call_args[0][0]
        assert "andebox" in cmd
        assert "integration" in cmd

    test = make_helper(testcase, setup, run_andebox, verify_integration)
    test.run()
