# -*- coding: utf-8 -*-
# (c) 2025, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import difflib
import importlib.util
import subprocess
import textwrap
from pathlib import Path

import pytest


def load_module_vars(pyfile):
    spec = importlib.util.spec_from_file_location("test_module", str(pyfile))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {
        "DOCUMENTATION": getattr(mod, "DOCUMENTATION", None),
        "EXAMPLES": getattr(mod, "EXAMPLES", None),
        "RETURN": getattr(mod, "RETURN", None),
    }


TEST_CASES = [
    dict(
        id="doc-only",
        input=dict(
            DOCUMENTATION=textwrap.dedent(
                """
                ---
                short_description: test plugin
                description:
                    - this is a test
                options:
                  foo:
                    description: foo option
            """
            ),
            EXAMPLES=None,
            RETURN=None,
        ),
        output=dict(
            DOCUMENTATION=textwrap.dedent(
                """\
                ---
                short_description: test plugin
                description:
                  - This is a test.
                options:
                  foo:
                    description: Foo option.
            """
            ),
        ),
    ),
    dict(
        id="doc-and-examples",
        input=dict(
            DOCUMENTATION=textwrap.dedent(
                """
                ---
                short_description: test plugin
                description:
                  -      this is a test
            """
            ),
            EXAMPLES=textwrap.dedent(
                """
                # Example usage
                - name:    run test
                  test_module:
            """
            ),
            RETURN=None,
        ),
        output=dict(
            DOCUMENTATION=textwrap.dedent(
                """\
                ---
                short_description: test plugin
                description:
                  - This is a test.
            """
            ),
            EXAMPLES=textwrap.dedent(
                """\
                # Example usage
                - name: run test
                  test_module:
            """
            ),
        ),
    ),
    dict(
        id="all-blocks",
        input=dict(
            DOCUMENTATION=textwrap.dedent(
                """
                ---
                short_description: test plugin
                description:
                  - This is a test.
            """
            ),
            EXAMPLES=textwrap.dedent(
                """
                # Example usage
                - name: Run test
                  test_module:
            """
            ),
            RETURN=textwrap.dedent(
                """
                foo:
                  description: foo return value
                  returned: always
                  type: str
            """
            ),
        ),
        output=dict(
            DOCUMENTATION="short_description: test plugin",
            EXAMPLES="Example usage",
            RETURN="foo return value",
        ),
    ),
    dict(
        id="return-with-json-sample",
        flags={
            "xfail": "JSON sample formatting and document markers not working properly yet"
        },
        input=dict(
            DOCUMENTATION=None,
            EXAMPLES=None,
            RETURN=textwrap.dedent(
                """
                my_list:
                    description: A list of items
                    returned: always
                    type: list
                    sample: [{"id": 1, "name": "item1"}, {"id": 2, "name": "item2"}]
                my_dict:
                    description: A dictionary of data
                    returned: always
                    type: dict
                    sample: {"key1": "value1", "key2": {"nested": "value2"}}
                """
            ),
        ),
        output=dict(
            RETURN=textwrap.dedent(
                """\
                ---
                my_list:
                    description: A list of items.
                    returned: always
                    type: list
                    sample: |
                        [
                            {
                                "id": 1,
                                "name": "item1"
                            },
                            {
                                "id": 2,
                                "name": "item2"
                            }
                        ]
                my_dict:
                    description: A dictionary of data.
                    returned: always
                    type: dict
                    sample: |
                        {
                            "key1": "value1",
                            "key2": {
                                "nested": "value2"
                            }
                        }
                """
            ),
        ),
    ),
]
TEST_CASES_IDS = [item["id"] for item in TEST_CASES]


@pytest.fixture
def python_file_with_yaml_blocks_in_collection(git_repo):
    """
    Creates a valid Ansible collection structure in a real collection repo clone,
    writes a module with the given YAML blocks, and returns the file path.
    Uses a small community collection for speed.
    """
    # Use a smaller collection, e.g. ansible-collections/community.crypto
    repo_dir = Path(
        next(git_repo("https://github.com/ansible-collections/community.crypto.git"))
    )
    # Place the module in plugins/modules/
    module_dir = repo_dir / "plugins" / "modules"
    module_dir.mkdir(parents=True, exist_ok=True)
    pyfile = module_dir / "test_module.py"

    def _create_file(documentation, examples=None, returns=None):
        blocks = []
        if documentation:
            blocks.append(f'DOCUMENTATION = r"""{documentation.strip()}\n"""')
        if examples:
            blocks.append(f'EXAMPLES = r"""{examples.strip()}\n"""')
        if returns:
            blocks.append(f'RETURN = r"""{returns.strip()}\n"""')
        file_content = "\n\n".join(blocks) + "\n"
        pyfile.write_text(file_content)
        return pyfile

    return _create_file


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_yaml_doc_action_blocks_in_collection(
    request, python_file_with_yaml_blocks_in_collection, testcase
):
    # Handle test flags (xfail, skip, etc.)
    if "flags" in testcase:
        flags = testcase["flags"]
        if "xfail" in flags:
            request.node.add_marker(
                pytest.mark.xfail(
                    reason=flags["xfail"],
                    strict=False,  # Don't fail if the test unexpectedly passes
                    run=True,  # Always run the test
                )
            )

    input_ = testcase["input"]
    output = testcase["output"]

    pyfile = python_file_with_yaml_blocks_in_collection(
        input_["DOCUMENTATION"], input_["EXAMPLES"], input_["RETURN"]
    )

    # Run andebox yaml-doc on the file (from the collection root)
    result = subprocess.run(
        ["andebox", "yaml-doc", str(pyfile)],
        cwd=pyfile.parent.parent.parent,  # collection root
        check=False,
        encoding="utf-8",
        capture_output=True,
    )
    assert result.returncode == 0, f"andebox yaml-doc failed: {result.stderr}"

    actual = load_module_vars(pyfile)

    for var in ["DOCUMENTATION", "EXAMPLES", "RETURN"]:
        expected = output.get(var)
        if expected is not None:
            print(f"ACTUAL\n{actual[var]}")
            print(f"EXPECTED\n{expected}")
            assert var in actual, f"{var} not found in file"
            assert expected in actual[var], "\n".join(
                difflib.unified_diff(actual[var].splitlines(), expected.splitlines())
            )
            # f"{var} does not contain expected text: {expected}"
