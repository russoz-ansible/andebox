# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# Copyright (c) 2025, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
import difflib
import importlib.util

import pytest

from .utils import load_test_cases
from .utils import verify_patterns


TEST_CASES = load_test_cases(
    """
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
  expected:
    DOCUMENTATION: |
      short_description: Test plugin
      description:
        - This is a test.
      options:
        foo:
          description: Foo option.

- id: doc-and-examples
  input:
    DOCUMENTATION: |
      ---
      short_description: test plugin.
      description:
        -      this is a test
    EXAMPLES: |
      # Example usage
      - name:    run test
        test_module:
  expected:
    DOCUMENTATION: |
      short_description: Test plugin
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
      short_description:       test plugin ...
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
  expected:
    DOCUMENTATION: >-
      short_description: Test plugin
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
  expected:
    RETURN: |
      my_list:
        description: A list of items.
        returned: always
        type: list
        sample:
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
        sample:
          {
            "key1": "value1",
            "key2": {
              "nested": "value2"
            }
          }

- id: json-sample-cg-apache2_mod_proxy
  input:
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
  expected:
    RETURN: |
      member:
        description: Specific balancer member information dictionary, returned when the module is invoked with O(member_host) parameter.
        type: dict
        returned: success
        sample:
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
        sample:
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

- id: dict-description
  input:
    DOCUMENTATION: |
      ---
      short_description: test plugin
      description:
        this: is a test
        that: should fail
        because: description is not
        meant: to be a dict
      options:
        foo:
          description: foo option
          type: wrong_type
  expected: {}
  exception:
    class: YAMLDocException

- id: description-offender
  input:
    yaml_doc_args:
      - -o
    DOCUMENTATION: |
      ---
      short_description: test plugin
      description:
        - This will be fine.
      options:
        foo:
          description: foo option
          type: wrong_type
  expected:
    DOCUMENTATION: |
      short_description: Test plugin
      description:
        - This will be fine.
      options:
        foo:
          description: Foo option.
          type: wrong_type
    in_stdout: >-
        - This __FIXME__\\(will\\) be fine\\.

- id: description-fix-offender
  input:
    yaml_doc_args:
      - -O
    DOCUMENTATION: |
      ---
      short_description: test plugin
      description:
        - This will be fine.
      options:
        foo:
          description: foo option
          type: wrong_type
  expected:
    DOCUMENTATION: |
      short_description: Test plugin
      description:
        - This __FIXME__(will) be fine.
      options:
        foo:
          description: Foo option.
          type: wrong_type
    in_stdout: >-
        - This __FIXME__\\(will\\) be fine\\.

- id: word-wrapper
  input:
    yaml_doc_args:
      - -w
      - "40"
    DOCUMENTATION: |
      short_description: test plugin
      description:
        - Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus.
      options: {}
  expected:
    DOCUMENTATION: |
      short_description: Test plugin
      description:
        - Lorem ipsum dolor sit amet consectetur
          adipiscing elit quisque faucibus.
      options: {}

"""
)

TEST_CASES_IDS = [item.id for item in TEST_CASES]


@pytest.fixture
def mock_plugin(tmp_path_factory):
    repo_dir = tmp_path_factory.mktemp("community_crypto")
    module_dir = repo_dir / "plugins" / "modules"
    module_dir.mkdir(parents=True, exist_ok=True)
    pyfile = module_dir / "test_module.py"
    print(f"Creating {pyfile}")

    def _create_file(tc_input):
        blocks = []
        if documentation := tc_input.get("DOCUMENTATION"):
            blocks.append(f'DOCUMENTATION = r"""\n{documentation.strip()}\n"""')
        if examples := tc_input.get("EXAMPLES"):
            blocks.append(f'EXAMPLES = r"""\n{examples.strip()}\n"""')
        if returns := tc_input.get("RETURN"):
            blocks.append(f'RETURN = r"""\n{returns.strip()}\n"""')
        file_content = "\n\n".join(blocks) + "\n"
        pyfile.write_text(file_content)
        return {"pyfile": pyfile.name, "basedir": str(repo_dir)}

    return _create_file


@pytest.fixture
def yaml_doc_executor(run_andebox):

    def _executor(tc_input, data):
        tc = dict(tc_input)
        tc["args"] = (
            ["-c", "some.collection", "yaml-doc"]
            + tc.get("yaml_doc_args", [])
            + [f"plugins/modules/{data['pyfile']}"]
        )
        tc["andebox_context_type"] = "collection"

        return run_andebox(tc, data)

    return _executor


def load_module_vars(pyfile) -> dict[str, str | None]:
    spec = importlib.util.spec_from_file_location("test_module", str(pyfile))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {
        "DOCUMENTATION": getattr(mod, "DOCUMENTATION", None),
        "EXAMPLES": getattr(mod, "EXAMPLES", None),
        "RETURN": getattr(mod, "RETURN", None),
    }


@pytest.mark.parametrize("testcase", TEST_CASES, ids=TEST_CASES_IDS)
def test_action_yaml_doc(make_helper, yaml_doc_executor, mock_plugin, testcase):

    def validate_yaml_doc(expected, data):
        actual_docs = load_module_vars(f"plugins/modules/{data['pyfile']}")
        for var in ["DOCUMENTATION", "EXAMPLES", "RETURN"]:
            if (expected_var := expected.get(var)) is not None:
                assert var in actual_docs, f"{var} not found in file"
                actual_var = actual_docs[var].strip()
                print(f"ACTUAL\n{actual_var}")

                expected_var = expected_var.strip()
                print(f"EXPECTED\n{expected_var.strip()}")
                assert expected_var in actual_var, "\n".join(
                    difflib.unified_diff(
                        actual_var.splitlines(),
                        expected_var.splitlines(),
                    )
                )

    test = make_helper(
        testcase, mock_plugin, yaml_doc_executor, [validate_yaml_doc, verify_patterns]
    )
    test.execute()
