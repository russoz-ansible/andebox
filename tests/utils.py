from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import yaml


@dataclass
class MockContext:
    """Mock context for testing actions."""

    class Args:
        def __init__(self, **kwargs):
            self.indent = kwargs.get("indent", 2)
            self.width = kwargs.get("width", 120)
            self.offenders = kwargs.get("offenders", False)
            self.fix_offenders = kwargs.get("fix_offenders", False)
            self.dry_run = kwargs.get("dry_run", False)
            self.files = kwargs.get("files", [])

    def __init__(self, **kwargs):
        self.args = self.Args(**kwargs)


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
    """
    Load test cases from either a YAML file or a YAML string content into GenericTestCase objects.

    Args:
        yaml_path: Path to YAML file containing test cases
        yaml_content: String containing YAML formatted test cases

    Returns:
        List of GenericTestCase objects

    Raises:
        ValueError: If neither or both yaml_path and yaml_content are provided

    Example YAML structure:
        - id: doc-only
          input:
            DOCUMENTATION: |
              ---
              short_description: test plugin
            EXAMPLES: null
            RETURN: null
          output:
            DOCUMENTATION: |
              ---
              short_description: test plugin
          flags:
            xfail: "reason for failure"
    """
    if (yaml_path is None and yaml_content is None) or (
        yaml_path is not None and yaml_content is not None
    ):
        raise ValueError("Exactly one of yaml_path or yaml_content must be provided")

    if yaml_path is not None:
        yaml_path = Path(yaml_path)
        with yaml_path.open() as f:
            data = yaml.safe_load(f)
    else:
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
