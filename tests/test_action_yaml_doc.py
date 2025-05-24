# -*- coding: utf-8 -*-
# (c) 2025, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import difflib
import importlib.util

import pytest
from andeboxlib.actions.yaml_doc import YAMLDocAction

from .utils import load_test_cases
from .utils import MockContext


def load_module_vars(pyfile) -> dict[str, str | None]:
    spec = importlib.util.spec_from_file_location("test_module", str(pyfile))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {
        "DOCUMENTATION": getattr(mod, "DOCUMENTATION", None),
        "EXAMPLES": getattr(mod, "EXAMPLES", None),
        "RETURN": getattr(mod, "RETURN", None),
    }


TEST_CASES = load_test_cases(
    yaml_content="""
- id: doc-only
  input:
    DOCUMENTATION: |
      ---
      short_description: test plugin
      description:
          - this is a test
      options:
        foo:
          description: foo option
  output:
    DOCUMENTATION: |
      short_description: test plugin
      description:
        - This is a test.
      options:
        foo:
          description: Foo option.

- id: doc-and-examples
  input:
    DOCUMENTATION: |
      ---
      short_description: test plugin
      description:
        -      this is a test
    EXAMPLES: |
      # Example usage
      - name:    run test
        test_module:
  output:
    DOCUMENTATION: |
      short_description: test plugin
      description:
        - This is a test.
    EXAMPLES: |
      # Example usage
      - name: run test
        test_module:

- id: all-blocks
  input:
    DOCUMENTATION: |
      ---
      short_description: test plugin
      description:
        - This is a test.
    EXAMPLES: |
      # Example usage
      - name: Run test
        test_module:
    RETURN: |
      foo:
        description: foo return value
        returned: always
        type: str
  output:
    DOCUMENTATION: >-
      short_description: test plugin
    EXAMPLES: >-
      Example usage
    RETURN: >-
      Foo return value.

- id: return-with-json-sample
  input:
    RETURN: |
      ---
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
  output:
    RETURN: |
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

- id: json-sample-cg-apache2_mod_proxy
  input:
    DOCUMENTATION: null
    EXAMPLES: null
    RETURN: |
      ---
      member:
        description: Specific balancer member information dictionary, returned when the module is invoked with O(member_host) parameter.
        type: dict
        returned: success
        sample:
          {"attributes":
                {"Busy": "0",
                "Elected": "42",
                "Factor": "1",
                "From": "136K",
                "Load": "0",
                "Route": null,
                "RouteRedir": null,
                "Set": "0",
                "Status": "Init Ok ",
                "To": " 47K",
                "Worker URL": null
            },
            "balancer_url": "http://10.10.0.2/balancer-manager/",
            "host": "10.10.0.20",
            "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.20:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
            "path": "/ws",
            "port": 8080,
            "protocol": "http",
            "status": {
                "disabled": false,
                "drained": false,
                "hot_standby": false,
                "ignore_errors": false
            }
          }
      members:
        description: List of member (defined above) dictionaries, returned when the module is invoked with no O(member_host)
          and O(state) args.
        returned: success
        type: list
        sample:
          [{"attributes": {
                "Busy": "0",
                "Elected": "42",
                "Factor": "1",
                "From": "136K",
                "Load": "0",
                "Route": null,
                "RouteRedir": null,
                "Set": "0",
                "Status": "Init Ok ",
                "To": " 47K",
                "Worker URL": null
            },
            "balancer_url": "http://10.10.0.2/balancer-manager/",
            "host": "10.10.0.20",
            "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.20:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
            "path": "/ws",
            "port": 8080,
            "protocol": "http",
            "status": {
                "disabled": false,
                "drained": false,
                "hot_standby": false,
                "ignore_errors": false}
            },
            {"attributes": {
                "Busy": "0",
                "Elected": "42",
                "Factor": "1",
                "From": "136K",
                "Load": "0",
                "Route": null,
                "RouteRedir": null,
                "Set": "0",
                "Status": "Init Ok ",
                "To": " 47K",
                "Worker URL": null
            },
            "balancer_url": "http://10.10.0.2/balancer-manager/",
            "host": "10.10.0.21",
            "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.21:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
            "path": "/ws",
            "port": 8080,
            "protocol": "http",
            "status": {
                "disabled": false,
                "drained": false,
                "hot_standby": false,
                "ignore_errors": false}
            }
          ]
  output:
    RETURN: |
      member:
        description: Specific balancer member information dictionary, returned when the module is invoked with O(member_host) parameter.
        type: dict
        returned: success
        sample: |
          {
            "attributes": {
              "Busy": "0",
              "Elected": "42",
              "Factor": "1",
              "From": "136K",
              "Load": "0",
              "Route": null,
              "RouteRedir": null,
              "Set": "0",
              "Status": "Init Ok ",
              "To": " 47K",
              "Worker URL": null
            },
            "balancer_url": "http://10.10.0.2/balancer-manager/",
            "host": "10.10.0.20",
            "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.20:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
            "path": "/ws",
            "port": 8080,
            "protocol": "http",
            "status": {
              "disabled": false,
              "drained": false,
              "hot_standby": false,
              "ignore_errors": false
            }
          }
      members:
        description: List of member (defined above) dictionaries, returned when the module is invoked with no O(member_host) and
          O(state) args.
        returned: success
        type: list
        sample: |
          [
            {
              "attributes": {
                "Busy": "0",
                "Elected": "42",
                "Factor": "1",
                "From": "136K",
                "Load": "0",
                "Route": null,
                "RouteRedir": null,
                "Set": "0",
                "Status": "Init Ok ",
                "To": " 47K",
                "Worker URL": null
              },
              "balancer_url": "http://10.10.0.2/balancer-manager/",
              "host": "10.10.0.20",
              "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.20:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
              "path": "/ws",
              "port": 8080,
              "protocol": "http",
              "status": {
                "disabled": false,
                "drained": false,
                "hot_standby": false,
                "ignore_errors": false
              }
            },
            {
              "attributes": {
                "Busy": "0",
                "Elected": "42",
                "Factor": "1",
                "From": "136K",
                "Load": "0",
                "Route": null,
                "RouteRedir": null,
                "Set": "0",
                "Status": "Init Ok ",
                "To": " 47K",
                "Worker URL": null
              },
              "balancer_url": "http://10.10.0.2/balancer-manager/",
              "host": "10.10.0.21",
              "management_url": "http://10.10.0.2/lb/?b=mywsbalancer&w=http://10.10.0.21:8080/ws&nonce=8925436c-79c6-4841-8936-e7d13b79239b",
              "path": "/ws",
              "port": 8080,
              "protocol": "http",
              "status": {
                "disabled": false,
                "drained": false,
                "hot_standby": false,
                "ignore_errors": false
              }
            }
          ]
"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.fixture
def python_file_with_yaml_blocks_in_collection(tmp_path_factory):
    """
    Creates a valid Ansible collection structure in a temporary directory,
    writes a module with the given YAML blocks, and returns the file path.
    The directory is automatically cleaned up after the test session.
    """
    # Simulate the collection structure under a temporary path
    repo_dir = tmp_path_factory.mktemp("community_crypto")
    module_dir = repo_dir / "plugins" / "modules"
    module_dir.mkdir(parents=True, exist_ok=True)
    pyfile = module_dir / "test_module.py"
    print(f"Creating {pyfile}")

    def _create_file(documentation, examples=None, returns=None):
        blocks = []
        if documentation:
            blocks.append(f'DOCUMENTATION = r"""\n{documentation.strip()}\n"""')
        if examples:
            blocks.append(f'EXAMPLES = r"""\n{examples.strip()}\n"""')
        if returns:
            blocks.append(f'RETURN = r"""\n{returns.strip()}\n"""')
        file_content = "\n\n".join(blocks) + "\n"
        pyfile.write_text(file_content)
        return pyfile

    return _create_file


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_yaml_doc_action_blocks_in_collection(
    request, python_file_with_yaml_blocks_in_collection, testcase
):
    # Handle xfail flags if present
    if "xfail" in testcase.flags:
        request.node.add_marker(
            pytest.mark.xfail(
                reason=testcase.flags["xfail"],
                strict=False,
                run=True,
            )
        )

    input_ = testcase.input
    output = testcase.output

    pyfile = python_file_with_yaml_blocks_in_collection(
        input_.get("DOCUMENTATION"), input_.get("EXAMPLES"), input_.get("RETURN")
    )

    # Create action and context
    action = YAMLDocAction()
    context = MockContext(
        indent=2,
        width=120,
        offenders=False,
        fix_offenders=False,
        dry_run=False,
        files=[pyfile],
    )

    # Run the action
    action.run(context)

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
