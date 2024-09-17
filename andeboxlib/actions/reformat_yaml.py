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


class ReformatYAMLAction(AndeboxAction):
    name = "reformat-yaml"
    help = "reformat YAML content in plugins"
    args = [
        dict(
            names=("files",),
            specs=dict(
                help="Python files where to search for YAML content",
                type=Path,
                nargs="+",
            ),
        ),
    ]

    @staticmethod
    def format_yaml(yaml_content: str) -> str:
        from ruamel.yaml import YAML

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(2)
        yaml.explicit_start = True
        yaml.width = 140
        yaml.preserve_quotes = True
        yaml.top_level_colon_align = False
        yaml.compact_seq_seq = False

        data = yaml.load(yaml_content)
        output = StringIO()
        yaml.dump(data, output)
        return output.getvalue(), data

    def reformat_yaml_in_python_file(self, file_path):
        QUOTE_RE_FRAG = r'(?:"|\'){3}'
        VAR_RE_FRAG = r"[A-Z][A-Z_0-9]*"
        ONELINE_RE = re.compile(
            rf"^\s*{VAR_RE_FRAG}\s*=\s*r?{QUOTE_RE_FRAG}.*{QUOTE_RE_FRAG}$"
        )
        FIRST_LINE_RE = re.compile(rf"^(\s*{VAR_RE_FRAG})\s*=\s*r?{QUOTE_RE_FRAG}(.*)$")

        print(f"Opening file {file_path}")
        with open(file_path, "r") as file:
            lines = file.readlines()

        updated_lines = []

        variable = ""
        first_line = ""
        quoted_content = []

        for line in lines:
            line = line.rstrip()
            if variable:
                if not re.match(rf"^\s*{QUOTE_RE_FRAG}", line):
                    quoted_content.append(line)
                    continue

                updated_lines.append(first_line)

                yaml_content, data = self.format_yaml("\n".join(quoted_content))
                if data:
                    yaml_content = yaml_content.splitlines()
                    while yaml_content[0] == "":
                        yaml_content = yaml_content[1:]
                    updated_lines.extend(yaml_content)
                else:
                    # If no data (e.g. an empty or comment-only block), then keep original content
                    updated_lines.extend(quoted_content)

                updated_lines.append('"""')

                variable = ""
                quoted_content = []

            else:
                if ONELINE_RE.search(line):
                    updated_lines.append(re.sub(QUOTE_RE_FRAG, '"""', line))
                elif match := FIRST_LINE_RE.search(line):
                    variable, yaml_first_line = match.groups()
                    first_line = f'{variable} = """{yaml_first_line}'
                else:
                    updated_lines.append(line)

        # Write the updated lines back to the file
        with open(file_path, "w") as file:
            file.writelines([f"{x}\n" for x in updated_lines])

    def run(self, context):
        for file_path in context.args.files:
            self.reformat_yaml_in_python_file(file_path)
