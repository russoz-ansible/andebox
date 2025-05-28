import re
import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pytest
import yaml


@dataclass
class GenericTestCase:
    """Test case data structure for generic test cases."""

    id: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    flags: Dict[str, str] = field(default_factory=dict)


def load_test_cases(
    yaml_path: Optional[Union[str, Path]] = None, yaml_content: Optional[str] = None
) -> List[GenericTestCase]:
    """Load test cases from either a YAML file or a YAML string content into GenericTestCase objects."""
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
            output=case["output"],
            flags=case.get("flags", {}),
        )
        for case in data
    ]


class AndeboxTestHelper:
    """A reusable helper for structured testing of Andebox functionality.

    This class encapsulates common test execution patterns:
    1. Setup phase (handling flags, test environment, etc.)
    2. Execution phase (running commands with proper arguments)
    3. Verification phase (checking output against expected results)
    """

    def __init__(self, testcase: GenericTestCase, capfd: Any):
        """Initialize with minimal required components.

        Args:
            testcase: The test case data
            capfd: The pytest capfd fixture for capturing output
        """
        self.testcase = testcase
        self.capfd = capfd
        self.setup_result = None
        self.exception_info = None
        self.captured_output = None

    @staticmethod
    def check_flags(testcase: GenericTestCase, request: Any):
        """Check and apply test flags like xfail or skip_py."""
        if "xfail" in testcase.flags:
            request.node.add_marker(
                pytest.mark.xfail(
                    reason=testcase.flags["xfail"],
                    strict=False,
                    run=True,
                )
            )

        skip_py = testcase.flags.get("skip_py", [])
        if f"{sys.version_info.major}.{sys.version_info.minor}" in skip_py:
            pytest.skip("Unsupported python version")

    def setup(self, setup_func: Callable):
        """Run the setup phase of the test.

        Args:
            setup_func: Function to set up the test environment,
                        will be called with the testcase as argument
        """
        print(f"\nRunning test setup for {self.testcase.id}...")
        self.setup_result = setup_func(self.testcase)
        self.capfd.readouterr()  # Clear any output from setup
        return self.setup_result

    def execute(self, run_andebox: Callable, *args, context_type=None):
        """Execute the andebox command with the provided arguments.

        Args:
            run_andebox: The function to run andebox
            *args: Additional arguments to pass to run_andebox
            context_type: Optional context type for the andebox command
        """
        expected_exception = self.testcase.output.get("exception")
        if expected_exception:
            expected_class = expected_exception.get("class")
            with pytest.raises(Exception) as exc_info:
                run_andebox(*args, context_type=context_type)
            self.exception_info = exc_info
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
            run_andebox(*args, context_type=context_type)

        return self.capfd.readouterr()

    def verify_patterns(self, captured_output, prefix=None):
        """Verify output patterns against captured output.

        Args:
            captured_output: The captured stdout/stderr output
            prefix: Optional prefix for the pattern keys in the output dict
        """
        stdout = captured_output.out
        stderr = captured_output.err
        msg = f"stdout=\n{stdout}\n\nstderr=\n{stderr}"

        # Handle both single pattern and list of patterns
        key_stdout = f"{prefix}_stdout" if prefix else "in_stdout"
        key_stderr = f"{prefix}_stderr" if prefix else "in_stderr"

        patt_outs = self.testcase.output.get(key_stdout, [])
        if isinstance(patt_outs, str):
            patt_outs = [patt_outs]

        for patt_out in patt_outs:
            print(f"{patt_out=}")
            match = re.search(patt_out, stdout, re.M)
            print(f"{match=}")
            assert bool(match), f"Pattern ({patt_out}) not found in stdout! {msg}"

        patt_errs = self.testcase.output.get(key_stderr, [])
        if isinstance(patt_errs, str):
            patt_errs = [patt_errs]

        for patt_err in patt_errs:
            print(f"{patt_err=}")
            match = re.search(patt_err, stderr, re.M)
            print(f"{match=}")
            assert bool(match), f"Pattern ({patt_err}) not found in stderr! {msg}"

    def verify_exact_output(self, captured_output, key_prefix=None):
        """Verify exact output against expected output.

        Args:
            captured_output: The captured stdout/stderr output
            key_prefix: Optional prefix for the output keys
        """
        stdout = captured_output.out
        stderr = captured_output.err

        key_stdout = f"{key_prefix}_stdout" if key_prefix else "stdout"
        key_stderr = f"{key_prefix}_stderr" if key_prefix else "stderr"

        expected_stdout = self.testcase.output.get(key_stdout)
        if expected_stdout is not None:
            assert (
                stdout == expected_stdout
            ), f"Expected stdout to be '{expected_stdout}', but got '{stdout}'"

        expected_stderr = self.testcase.output.get(key_stderr)
        if expected_stderr is not None:
            assert (
                stderr == expected_stderr
            ), f"Expected stderr to be '{expected_stderr}', but got '{stderr}'"

    def verify_return_code(self, expected_rc=None):
        """Verify the expected return code.

        Args:
            expected_rc: Optional expected return code, defaults to testcase.output.get("rc")
        """
        if expected_rc is None:
            expected_rc = self.testcase.output.get("rc")

        if expected_rc is not None:
            # If we caught an exception, the return code should be non-zero
            if self.exception_info is not None:
                assert (
                    expected_rc != 0
                ), f"Expected non-zero return code, but got {expected_rc}"
            # For normal execution, we assume success (rc=0) unless specified otherwise
            else:
                assert (
                    expected_rc == 0
                ), f"Expected return code 0, but got {expected_rc}"

    def verify_custom(self, verification_func: Callable, *args, **kwargs):
        """Run custom verification logic.

        Args:
            verification_func: Custom function for verification
            *args, **kwargs: Additional arguments to pass to the verification function
        """
        verification_func(self.testcase, *args, **kwargs)
