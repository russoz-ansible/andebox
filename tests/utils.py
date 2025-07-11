# -*- coding: utf-8 -*-
# code: language=python tabSize=4
#
# (C) 2024 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2024 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
import re
import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from types import MappingProxyType
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Sequence

import pytest
import yaml
from andebox.util import set_dir


GIT_REPO_CG = "https://github.com/ansible-collections/community.general.git"
GIT_REPO_AC = "https://github.com/ansible/ansible.git"


@dataclass
class GenericTestCase:
    id: str
    input: Mapping[str, Any]
    expected: Mapping[str, Any]
    flags: Dict[str, Any] = field(default_factory=dict)
    exception: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.input, MappingProxyType):
            self.input = MappingProxyType(dict(self.input))
        if not isinstance(self.expected, MappingProxyType):
            self.expected = MappingProxyType(dict(self.expected))


def load_test_cases(source: str | Path) -> List[GenericTestCase]:
    """
    Loads test cases from a YAML string or from a file path.
    Tries to parse as YAML content first (if str); if that fails with a yaml.YAMLError, or if not a str, tries to open as a file.
    """
    if isinstance(source, str):
        try:
            data = yaml.safe_load(source)
        except yaml.YAMLError:
            yaml_path = Path(source)
            with yaml_path.open() as f:
                data = yaml.safe_load(f)
    else:
        yaml_path = Path(source)
        with yaml_path.open() as f:
            data = yaml.safe_load(f)

    return [
        GenericTestCase(
            id=case["id"],
            input=case["input"],
            expected=case["expected"],
            flags=case.get("flags", {}),
            exception=case.get("exception", {}),
        )
        for case in data
    ]


def _enforce_list(arg: Any) -> list[Any]:
    if isinstance(arg, Sequence) and not isinstance(arg, str):
        return list(arg)
    return [arg]


FuncOrFuncList = Callable | List[Callable]


class AndeboxTestHelper:

    def __init__(
        self,
        testcase: GenericTestCase,
        fixtures: Dict[str, Any],
        setups: FuncOrFuncList,
        executor: Callable,
        validators: FuncOrFuncList,
    ) -> None:
        self.testcase: GenericTestCase = testcase
        self.fixtures = fixtures

        self.setups = _enforce_list(setups)
        self.executor = executor
        self.validators = _enforce_list(validators)

        self.testcase.data["basedir"] = Path.cwd()

    def check_flags(self) -> None:
        request = self.fixtures["request"]
        flags = dict(self.testcase.flags)

        if skip_py := flags.get("skip_py", []):
            if f"{sys.version_info.major}.{sys.version_info.minor}" in skip_py:
                pytest.skip("Unsupported python version")
                return
            del flags["skip_py"]

        for marker_name, marker_params in flags.items():
            marker = pytest.mark.__getattr__(marker_name)
            if isinstance(marker_params, str):
                request.node.add_marker(marker(marker_params))
            elif isinstance(marker_params, list):
                request.node.add_marker(marker(*marker_params))
            elif isinstance(marker_params, dict):
                request.node.add_marker(marker(**marker_params))
            elif marker_params is None:
                request.node.add_marker(marker())
            else:
                raise TypeError(
                    f"Unsupported marker parameters type: {type(marker_params)}"
                )

    @staticmethod
    def _execute(executor_callable: Callable, testcase: GenericTestCase) -> None:
        executor_name = getattr(executor_callable, "__name__", repr(executor_callable))
        executor_result = executor_callable(testcase)
        if executor_result is not None:
            assert isinstance(
                executor_result, Mapping
            ), f"Data returned from executor function {executor_name} must be a Mapping or None, but got {type(executor_result)}"
            testcase.data.update(executor_result)

    def run(self) -> None:
        self.check_flags()
        for setup in self.setups:
            update_data = setup(self.testcase)
            if update_data:
                assert isinstance(
                    update_data, Mapping
                ), f"Data returned from setup function {getattr(setup, '__name__', repr(setup))} must be a Mapping but got {type(update_data)}"
                self.testcase.data.update(update_data)
        self.fixtures["capfd"].readouterr()

        with set_dir(self.testcase.data["basedir"]):
            expected_exception = self.testcase.exception
            if expected_exception:
                expected_classname = expected_exception["class"]
                with pytest.raises(Exception) as exc_info:
                    AndeboxTestHelper._execute(self.executor, self.testcase)

                actual_classname = exc_info.value.__class__.__name__
                assert (
                    actual_classname == expected_classname
                ), f"Expected exception class {expected_classname}, but got {actual_classname}"

                expected_value = expected_exception.get("value")
                if expected_value:
                    assert expected_value in str(
                        exc_info.value
                    ), f"Expected exception message to contain '{expected_value}', but got: {exc_info.value}"
            else:
                AndeboxTestHelper._execute(self.executor, self.testcase)

            capfd_capture = self.fixtures["capfd"].readouterr()
            self.testcase.data["stdout"] = capfd_capture.out
            self.testcase.data["stderr"] = capfd_capture.err

            for validator in self.validators:
                validator(self.testcase)  # Pass the entire testcase object


def verify_patterns(testcase: GenericTestCase) -> None:
    expected = testcase.expected
    data = testcase.data
    stdout = data["stdout"]
    stderr = data["stderr"]
    msg = f"stdout=\n{stdout}\n\nstderr=\n{stderr}"

    patt_outs = expected.get("in_stdout", [])
    if isinstance(patt_outs, str):
        patt_outs = [patt_outs]

    for patt_out in patt_outs:
        print(f"{patt_out=}")
        match = re.search(patt_out, stdout, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_out}) not found in stdout! {msg}"

    patt_errs = expected.get("in_stderr", [])
    if isinstance(patt_errs, str):
        patt_errs = [patt_errs]

    for patt_err in patt_errs:
        print(f"{patt_err=}")
        match = re.search(patt_err, stderr, re.M)
        print(f"{match=}")
        assert bool(match), f"Pattern ({patt_err}) not found in stderr! {msg}"


def verify_return_code(testcase: GenericTestCase) -> None:
    expected = testcase.expected
    data = testcase.data
    expected_rc = expected.get("rc")

    if expected_rc is not None:
        assert (
            expected_rc == data["rc"]
        ), f"Expected return code {expected_rc}, but got {data['rc']}"


def validate_stdout(testcase: GenericTestCase) -> None:
    expected = testcase.expected
    data = testcase.data
    if expected.get("stdout_line_count"):
        assert len(data["stdout"].splitlines()) == expected["stdout_line_count"]
