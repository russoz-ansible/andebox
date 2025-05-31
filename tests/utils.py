# -*- coding: utf-8 -*-
# Copyright (c) 2024, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import re
import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Sequence

import pytest
import yaml
from andebox.util import set_dir


GIT_REPO_CG = "https://github.com/ansible-collections/community.general.git"
GIT_REPO_AC = "https://github.com/ansible/ansible.git"


@dataclass
class GenericTestCase:
    id: str
    input: Dict[str, Any]
    expected: Dict[str, Any]
    flags: Dict[str, str] = field(default_factory=dict)
    exception: Dict[str, Any] = field(default_factory=dict)


def load_test_cases(
    yaml_path: str | Path | None = None, yaml_content: str | None = None
) -> List[GenericTestCase]:
    if (yaml_path is None and yaml_content is None) or (
        yaml_path is not None and yaml_content is not None
    ):
        raise ValueError("Exactly one of yaml_path or yaml_content must be provided")

    if yaml_path is not None:
        yaml_path = Path(yaml_path)
        with yaml_path.open() as f:
            data = yaml.safe_load(f)
    else:
        assert yaml_content is not None
        data = yaml.safe_load(yaml_content)

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
        setup: FuncOrFuncList,
        executor: Callable,
        validator: FuncOrFuncList,
    ) -> None:
        self.testcase: GenericTestCase = testcase
        self.fixtures = fixtures

        self.setup = _enforce_list(setup)
        self.executor = executor
        self.validator = _enforce_list(validator)

        self.data: Dict[str, Any] = {"basedir": Path.cwd()}

    def check_flags(self) -> None:
        request = self.fixtures["request"]
        flags = self.testcase.flags
        if "xfail" in flags:
            request.node.add_marker(
                pytest.mark.xfail(
                    reason=flags["xfail"],
                    strict=False,
                    run=True,
                )
            )

        skip_py = flags.get("skip_py", [])
        if f"{sys.version_info.major}.{sys.version_info.minor}" in skip_py:
            pytest.skip("Unsupported python version")

    def execute(self) -> None:
        self.check_flags()
        for setup in self.setup:
            self.data.update(setup(self.testcase.input))
        self.fixtures["capfd"].readouterr()

        with set_dir(self.data["basedir"]):
            expected_exception = self.testcase.exception
            if expected_exception:
                expected_class = expected_exception["class"]
                with pytest.raises(Exception) as exc_info:
                    (self.executor)(self.data)
                actual_class = exc_info.value.__class__.__name__
                assert (
                    actual_class == expected_class
                ), f"Expected exception class {expected_class}, but got {actual_class}"

                expected_value = expected_exception.get("value")
                if expected_value:
                    assert expected_value in str(
                        exc_info.value
                    ), f"Expected exception message to contain '{expected_value}', but got: {exc_info.value}"
            else:
                (self.executor)(self.data)

            self.data["captured"] = self.fixtures["capfd"].readouterr()

            for validator in self.validator:
                validator(self.testcase.expected, self.data)


def verify_patterns(expected: Dict[str, Any], data: Dict[str, Any]) -> None:
    stdout = data["captured"].out
    stderr = data["captured"].err
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


def verify_return_code(expected: Dict[str, Any], data: Dict[str, Any]) -> None:
    expected_rc = expected.get("rc")

    if expected_rc is not None:
        assert (
            expected_rc == data["rc"]
        ), f"Expected return code {data['rc']}, but got {expected_rc}"


# code: language=python tabSize=4
