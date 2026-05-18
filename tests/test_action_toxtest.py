# code: language=python tabSize=4
#
# (C) 2026 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2026 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import pytest

from andebox.actions.toxtest import TOX_INI_FILENAME, _make_default_tox_ini

from .utils import GenericTestCase, load_test_cases, verify_return_code


def _make_collection(path):
    (path / "meta").mkdir(parents=True)
    (path / "meta" / "runtime.yml").write_text("requires_ansible: '>=2.18'\n")
    (path / "galaxy.yml").write_text("namespace: test\nname: coll\nversion: 1.0.0\n")


TEST_CASES = load_test_cases(
    f"""
- id: no-opts
  input:
    args: [tox-test]
  expected:
    rc: 0
    cmd: ["tox", "-c", "{TOX_INI_FILENAME}", "--"]

- id: list
  input:
    args: [tox-test, --list]
  expected:
    rc: 0
    cmd: ["tox", "-c", "{TOX_INI_FILENAME}", "-a", "--"]

- id: recreate
  input:
    args: [tox-test, --recreate]
  expected:
    rc: 0
    cmd: ["tox", "-c", "{TOX_INI_FILENAME}", "-r", "--"]

- id: env
  input:
    args: [tox-test, --env, ac218]
  expected:
    rc: 0
    cmd: ["tox", "-c", "{TOX_INI_FILENAME}", "-e", "ac218", "--"]

- id: params
  input:
    args: [tox-test, sanity]
  expected:
    rc: 0
    cmd: ["tox", "-c", "{TOX_INI_FILENAME}", "--", "sanity"]

- id: params-with-sep
  input:
    args: [tox-test, --, sanity]
  expected:
    rc: 0
    cmd: ["tox", "-c", "{TOX_INI_FILENAME}", "--", "sanity"]

- id: all-opts
  input:
    args: [tox-test, --list, --recreate, --env, ac219]
  expected:
    rc: 0
    cmd: ["tox", "-c", "{TOX_INI_FILENAME}", "-a", "-r", "-e", "ac219", "--"]

- id: nonzero-rc
  input:
    args: [tox-test]
    subprocess_rc: 1
  expected:
    rc: 1

- id: tox-ini-not-overwritten
  input:
    args: [tox-test]
    existing_tox_ini: |
      [tox]
      # custom
  expected:
    rc: 0
    tox_ini_content: |
      [tox]
      # custom
"""
)

TEST_CASES_IDS = [tc.id for tc in TEST_CASES]


def test_make_default_tox_ini_structure():
    content = _make_default_tox_ini()
    assert "[tox]" in content
    assert "envlist" in content
    assert "[testenv]" in content
    assert "andebox test" in content


def test_make_default_tox_ini_envs():
    content = _make_default_tox_ini()
    for env in ("ac218", "ac219", "ac220", "ac221", "dev"):
        assert env in content


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_toxtest_command(make_helper, testcase, run_andebox, tmp_path, mocker):
    def setup(tc):
        _make_collection(tmp_path)
        if existing := tc.input.get("existing_tox_ini"):
            (tmp_path / TOX_INI_FILENAME).write_text(existing)
        mock_call = mocker.patch(
            "andebox.actions.toxtest.subprocess.call",
            return_value=tc.input.get("subprocess_rc", 0),
        )
        return {"basedir": tmp_path, "mock_call": mock_call}

    def verify_cmd(tc):
        expected_cmd = tc.expected.get("cmd")
        if expected_cmd:
            assert tc.data["mock_call"].call_args[0][0] == expected_cmd

    def verify_tox_ini(tc):
        expected_content = tc.expected.get("tox_ini_content")
        if expected_content is not None:
            assert (tmp_path / TOX_INI_FILENAME).read_text() == expected_content

    test = make_helper(testcase, setup, run_andebox, [verify_return_code, verify_cmd, verify_tox_ini])
    test.run()


def test_tox_ini_created_when_missing(make_helper, run_andebox, tmp_path, mocker):
    testcase = GenericTestCase(id="creates-ini", input={"args": ["tox-test"]}, expected={})

    def setup(tc):
        _make_collection(tmp_path)
        mocker.patch("andebox.actions.toxtest.subprocess.call", return_value=0)
        return {"basedir": tmp_path}

    def verify_created(tc):
        assert (tmp_path / TOX_INI_FILENAME).exists()

    test = make_helper(testcase, setup, run_andebox, verify_created)
    test.run()
