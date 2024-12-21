# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import argparse
import re
from io import StringIO
from pathlib import Path

from .base import AndeboxAction


def info_type(types, v):
    try:
        r = [t for t in types if t.startswith(v.lower())]
        return r[0][0].upper()
    except IndexError as e:
        raise argparse.ArgumentTypeError("invalid value: {v}") from e


def fix_period(line: str) -> str:
    if line.endswith(".)"):
        return f"{line[:-2]})."
    if line.endswith("."):
        return line
    return f"{line}."


def process_description(desc):
    if isinstance(desc, str):
        return fix_period(desc)
    else:  # assume list
        return [fix_period(x) for x in desc]


def process_options(opts):
    for option in opts.values():
        if "description" in option:
            option["description"] = process_description(option["description"])
        if "suboptions" in option:
            option["suboptions"] = process_options(option["suboptions"])
    return opts


def process_documentation(data):
    if data["short_description"].endswith("."):
        data["short_description"] = data["short_description"].rstrip(".")
    data["description"] = process_description(data["description"])
    if "options" in data:
        data["options"] = process_options(data["options"])

    return data


class ReformatYAMLAction(AndeboxAction):
    name = "reformat-yaml"
    help = "reformat YAML content in plugins"
    args = [
        dict(
            names=("files",),
            specs=dict(
                help="Files where to search for YAML content",
                type=Path,
                nargs="+",
            ),
        ),
    ]

    def make_yaml(self):
        from ruamel.yaml import YAML

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.explicit_start = False
        yaml.width = 140
        yaml.preserve_quotes = True
        yaml.top_level_colon_align = False
        yaml.compact_seq_seq = False
        return yaml

    def read_yaml(self, content: str):
        return self.yaml.load(content)

    def dump_yaml(self, data) -> str:
        output = StringIO()
        self.yaml.dump(data, output)
        return output.getvalue()

    def reformat_yaml_in_python_file(self, file_path):
        QUOTE_RE_FRAG = r'(?:"|\'){3}'
        VAR_RE_FRAG = r"(?:DOCUMENTATION|EXAMPLES|RETURN)"
        ONELINE_RE = re.compile(
            rf"^\s*{VAR_RE_FRAG}\s*=\s*r?{QUOTE_RE_FRAG}.*{QUOTE_RE_FRAG}$"
        )
        FIRST_LINE_RE = re.compile(rf"^(\s*{VAR_RE_FRAG})\s*=\s*r?{QUOTE_RE_FRAG}(.*)$")

        print(f"Opening file {file_path}")
        with open(file_path, "r") as file:
            lines = file.readlines()

        updated_lines = []

        in_variable = ""
        first_line = ""
        quoted_content = []

        for line in lines:
            line = line.rstrip()
            if in_variable:
                if not re.match(rf"^\s*{QUOTE_RE_FRAG}", line):
                    quoted_content.append(line)
                    continue

                updated_lines.append(first_line)

                data = self.read_yaml("\n".join(quoted_content))
                if data:
                    if in_variable == "DOCUMENTATION":
                        data = process_documentation(data)
                    yaml_content = self.dump_yaml(data)
                    yaml_content = yaml_content.splitlines()
                    if isinstance(data, list):
                        yaml_content = [
                            (line[2:] if line.startswith("  ") else line)
                            for line in yaml_content
                        ]
                    while yaml_content[0] == "":
                        yaml_content = yaml_content[1:]
                    updated_lines.extend(yaml_content)
                else:
                    # If no data (e.g. an empty or comment-only block), then keep original content
                    updated_lines.extend(quoted_content)

                updated_lines.append('"""')

                in_variable = ""
                quoted_content = []

            else:
                if ONELINE_RE.search(line):
                    updated_lines.append(re.sub(QUOTE_RE_FRAG, '"""', line))
                elif match := FIRST_LINE_RE.search(line):
                    in_variable, yaml_first_line = match.groups()
                    first_line = f'{in_variable} = r"""{yaml_first_line}'
                else:
                    updated_lines.append(line)

        # Write the updated lines back to the file
        with open(file_path, "w") as file:
            file.writelines([f"{x}\n" for x in updated_lines])

    def run(self, context):
        self.yaml = self.make_yaml()
        for file_path in context.args.files:
            self.reformat_yaml_in_python_file(file_path)
