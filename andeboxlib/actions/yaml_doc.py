# -*- coding: utf-8 -*-
# (c) 2024, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import re
from io import StringIO
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

try:
    from ruamel.yaml import YAML

    HAS_RUAMEL = True
except ImportError:
    HAS_RUAMEL = False

from .base import AndeboxAction


DESCRIPTION_ACCEPTED_END_CHARS = (".", "!", ":", ";", ",", "?")
OFFENDING_REGEXPS = [
    re.compile(exp)
    for exp in [
        r"`",
        r"\bi\.e\.?\b",  # i.e
        r"\be\.g\.?\b",  # e.g.
        r"[^/]etc\b",  # etc, but not /etc
        r"\bvia\b",  # via
        r"\bversus\b",
        r"\bvs\.?\b",
        r"\bversa\b",
        r"\b[Ww]ill\b" r"[a-zI]'(re|t|d|ll|ve)",
        r"(there|let|he)'s",
        r"\s([Aa]pis?|[Jj]son|[Ii]ps?|[Dd]ns)[\s\.,]",
    ]
]


class YAMLDocException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__()
        self.args = args


def fix_desc_value(line: str) -> str:
    line = line.strip()  # remove extraneous whitespace chars from heads and tails
    line = re.sub(r"\s\s+", " ", line)
    if not line[0].isupper():
        line = line[0].upper() + line[1:]
    if line.endswith(".)"):
        return f"{line[:-2]})."
    if line.endswith(DESCRIPTION_ACCEPTED_END_CHARS):
        return line
    return f"{line}."


def process_description(desc: Union[List[str], str]) -> Union[List[str], str]:
    try:
        if isinstance(desc, str):
            return fix_desc_value(desc)
        else:  # assume list
            return [fix_desc_value(x) for x in desc]
    except Exception as e:
        raise YAMLDocException(desc) from e


def process_options(opts: Dict[str, Any], suboptions_kw: str) -> Dict[str, Any]:
    try:
        for option in opts.values():
            if "description" in option:
                option["description"] = process_description(option["description"])
            if suboptions_kw in option:
                option[suboptions_kw] = process_options(
                    option[suboptions_kw], suboptions_kw
                )
        return opts
    except Exception as e:
        raise YAMLDocException(opts, suboptions_kw) from e


def process_documentation(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if data.get("short_description", " ").endswith("."):
            data["short_description"] = data["short_description"].rstrip(".")
        if desc := data.get("description"):
            data["description"] = process_description(desc)
        if notes := data.get("notes"):
            data["notes"] = process_description(notes)
        if seealso := data.get("seealso"):
            for sa in seealso:
                if sa_desc := sa.get("description"):
                    sa["description"] = process_description(sa_desc)
        if options := data.get("options"):
            data["options"] = process_options(options, "suboptions")

        return data
    except Exception as e:
        raise YAMLDocException(data) from e


def process_return(data: Dict[str, Dict]) -> Dict[str, Dict]:
    try:
        data = process_options(data, "contains")
        return data
    except Exception as e:
        raise YAMLDocException(data) from e


def get_processor(variable: str, in_doc_fragments: bool = False) -> Callable:
    processors_map = {
        "DOCUMENTATION": process_documentation,
        "RETURN": process_return,
    }
    return processors_map.get(
        variable, process_documentation if in_doc_fragments else lambda x: x
    )


def report_offenders(content: List[str], content_first_line: int) -> None:
    for num, line in enumerate(content):
        if any(offender.search(line) for offender in OFFENDING_REGEXPS):
            # both vars come from enumerate(), which starts at 0, so must add 2
            print(f"  {2 + content_first_line + num:4}: {line}")


class YAMLDocAction(AndeboxAction):
    name = "yaml-doc"
    help = "analyze and/or reformat YAML documentation in plugins"
    args = [
        dict(
            names=("--offenders", "-o"),
            specs=dict(
                action="store_true",
                help="Notifies of backtick characters inside the docs",
            ),
        ),
        dict(
            names=("--dry_run", "-n"),
            specs=dict(
                action="store_true",
                help="Do not modify files",
            ),
        ),
        dict(
            names=("files",),
            specs=dict(
                help="Files where to search for YAML content",
                type=Path,
                nargs="+",
            ),
        ),
    ]

    def make_yaml(self) -> YAML:
        if not HAS_RUAMEL:
            raise ValueError("This action requires ruamel.yaml to be installed")

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.explicit_start = False
        yaml.width = 120
        yaml.preserve_quotes = True
        yaml.top_level_colon_align = False
        yaml.compact_seq_seq = False
        return yaml

    def read_yaml(self, content: str) -> Optional[Union[Dict[str, Any], list]]:
        return self.yaml.load(content)

    def dump_yaml(self, data: Union[Dict[str, Any], list]) -> str:
        output = StringIO()
        self.yaml.dump(data, output)
        return output.getvalue()

    def process_yaml_block(
        self, quoted_content: List[str], processor: Callable, dry_run: bool
    ) -> List[str]:

        data = self.read_yaml("\n".join(quoted_content))
        if not data:
            # If no data (e.g. an empty or comment-only block), then keep original content
            return quoted_content

        data = processor(data)
        yaml_content = self.dump_yaml(data)
        yaml_content = yaml_content.splitlines()
        if isinstance(data, list):
            yaml_content = [
                (line[2:] if line.startswith("  ") else line) for line in yaml_content
            ]
        while yaml_content[0] == "":
            yaml_content = yaml_content[1:]

        # Do the YAML parsing in dry run, but return the original content
        if dry_run:
            return quoted_content
        return yaml_content

    def reformat_yaml_in_python_file(
        self, file_path: Path, offenders: bool, dry_run: bool
    ):
        QUOTE_RE_FRAG = r'(?:"|\'){3}'
        VAR_RE_FRAG = r"(?:[A-Z]+)"
        ONELINE_RE = re.compile(
            rf"^\s*{VAR_RE_FRAG}\s*=\s*r?{QUOTE_RE_FRAG}.*{QUOTE_RE_FRAG}$"
        )
        FIRST_LINE_RE = re.compile(rf"^(\s*{VAR_RE_FRAG})\s*=\s*r?{QUOTE_RE_FRAG}(.*)$")

        print(f"Opening file {file_path}")
        with open(file_path, "r") as file:
            lines = file.readlines()

        updated_lines = []

        is_doc_frag = "doc_fragments" in file_path.parts
        in_variable = ""
        first_line = ""
        quoted_content = []
        first_line_no = 0

        for line_no, line in enumerate(lines):
            line = line.rstrip()
            if in_variable:
                if not re.match(rf"^\s*{QUOTE_RE_FRAG}", line):
                    quoted_content.append(line)
                    continue

                updated_lines.append(first_line)
                outbound_content = self.process_yaml_block(
                    quoted_content,
                    get_processor("DOCUMENTATION" if is_doc_frag else in_variable),
                    dry_run,
                )
                if offenders and in_variable != "EXAMPLES":
                    report_offenders(outbound_content, first_line_no)
                updated_lines.extend(outbound_content)
                updated_lines.append('"""')

                in_variable = ""
                quoted_content = []
                first_line_no = 0

            else:
                if ONELINE_RE.search(line):
                    updated_lines.append(re.sub(QUOTE_RE_FRAG, '"""', line))
                elif match := FIRST_LINE_RE.search(line):
                    in_variable, yaml_first_line = match.groups()
                    first_line = f'{in_variable} = r"""{yaml_first_line}'
                    first_line_no = line_no
                else:
                    updated_lines.append(line)

        if not dry_run:
            # Write the updated lines back to the file
            with open(file_path, "w") as file:
                file.writelines([f"{x}\n" for x in updated_lines])

    def run(self, context):
        self.yaml = self.make_yaml()
        for file_path in context.args.files:
            self.reformat_yaml_in_python_file(
                file_path, context.args.offenders, context.args.dry_run
            )
