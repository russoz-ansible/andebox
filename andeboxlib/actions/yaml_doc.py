# -*- coding: utf-8 -*-
# (c) 2024-2025, Alexei Znamensky <russoz@gmail.com>
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


FIXME_TAG = "__FIXME__"


def fixme(s):
    return f"{FIXME_TAG}({s})"


DESCRIPTION_ACCEPTED_END_CHARS = (".", "!", ":", ";", ",", "?")
OFFENDING_SPEC = [
    # processed in order, apply only the first hit
    # if using parenthesis in regexp, they MUST be non-capturing, as in (?:pattern1|pattern2|...)
    dict(regexp=r"`", apply=fixme),
    dict(regexp=r"\bi\.e\.?\b", apply=fixme),  # i.e
    dict(regexp=r"\be\.g\.?\b", apply=fixme),  # e.g.
    dict(regexp=r"[^/]etc\b", apply=fixme),  # etc, but not /etc
    dict(regexp=r"\bvia\b", apply=fixme),  # via
    dict(regexp=r"\bversus\b", apply=fixme),
    dict(regexp=r"\bvs\.?\b", apply=fixme),
    dict(regexp=r"\bversa\b", apply=fixme),
    dict(regexp=r"won't", replace="will not"),
    # dict(regexp=r"\b(?:[Ww]i|')ll\b", apply=fixme),
    dict(regexp=r"[a-zI]'ve", apply=lambda s: s.replace("'ve", " have")),
    dict(regexp=r"can't", replace="cannot"),
    dict(regexp=r"Can't", replace="Cannot"),
    dict(regexp=r"[a-zI]n't", apply=lambda s: s.replace("n't", " not")),
    dict(regexp=r"[a-zI]'re", apply=lambda s: s.replace("'re", " are")),
    dict(regexp=r"[a-zI]'d", apply=lambda s: s.replace("'d", " would")),
    dict(regexp=r"let's", replace="let us"),
    dict(
        regexp=r"(?:there|s?he|it)'s (?:been|[dg]one)",
        apply=lambda s: s.replace("'s", " has"),
    ),
    dict(regexp=r"(?:there|s?he|it)'s", apply=lambda s: s.replace("'s", " is")),
    dict(
        regexp=r"\s(?:[Aa]pi|[Ii]p|[Ii]d|[Uu]r[il])",
        plural=r"s?[\s\.,]",
        apply=str.upper,
    ),
    dict(regexp=r"\s(?:[Jj]son|[Dd]ns|[Hh]tml|[Vv]m)[\s\.,]", apply=str.upper),
]
OFFENDING_SPEC = [
    (re.compile(f"(.*[^(])({x['regexp']})({x.get('plural', '')})([^)]?.*)"), x)
    for x in OFFENDING_SPEC
]


class YAMLDocException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__()
        self.args = args


class YAMLDocAction(AndeboxAction):
    name = "yaml-doc"
    help = "analyze and/or reformat YAML documentation in plugins"
    args = [
        dict(
            names=("--offenders", "-o"),
            specs=dict(
                action="store_true",
                help="report potential style-related offending constructs",
            ),
        ),
        dict(
            names=("--fix-offenders", "-O"),
            specs=dict(
                action="store_true",
                help="fix potential style-related offending constructs, implies (--offenders)",
            ),
        ),
        dict(
            names=("--dry_run", "-n"),
            specs=dict(
                action="store_true",
                help="do not modify files",
            ),
        ),
        dict(
            names=("--width", "-w"),
            specs=dict(
                type=int,
                default=120,
                help="width for the YAML output (default: 120)",
            ),
        ),
        dict(
            names=("--indent", "-i"),
            specs=dict(
                type=int,
                default=2,
                help="indentation for the YAML output (default: 2)",
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

    def apply_offender_rule(self, line_num: int, line: str) -> str:
        for regexp, spec in OFFENDING_SPEC:
            if match := regexp.match(line):
                if self.offenders and not self.fix_offenders:
                    print(f"  {line_num:4}: {line}")
                prefix, term, plural, suffix = match.groups()

                if func := spec.get("apply"):
                    mod_line = f"{prefix}{func(term)}{plural}{suffix}"
                    return mod_line
                elif repl := spec.get("replace"):
                    mod_line = f"{prefix}{repl}{plural}{suffix}"
                    return mod_line

        # Nothing found, return line as-is
        return line

    def process_offenders(self, content: List[str]) -> List[str]:
        result = []
        for num, line in enumerate(content):

            line_num = 2 + self.first_line_no + num

            def apply(line):
                # pylint: disable=cell-var-from-loop
                return self.apply_offender_rule(line_num, line)

            prev_line = fixed_line = line
            while (fixed_line := apply(fixed_line)) != prev_line:
                prev_line = fixed_line

            if fixed_line != line:
                print(f"  {line_num:4}: {fixed_line}")
            result.append(fixed_line)

        return result

    def make_yaml_instance(self) -> YAML:
        if not HAS_RUAMEL:
            raise ValueError("This action requires ruamel.yaml to be installed")

        yaml = YAML()
        yaml.indent(**self.indent)
        yaml.width = self.width
        yaml.preserve_quotes = True
        yaml.explicit_start = False
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

    def fix_desc_str(self, line: str) -> str:
        line = line.strip()  # remove extraneous whitespace chars from heads and tails
        line = re.sub(r"\s\s+", " ", line)
        if not line[0].isupper():
            line = line[0].upper() + line[1:]
        if line.endswith(".)"):
            return f"{line[:-2]})."
        if line.endswith(DESCRIPTION_ACCEPTED_END_CHARS):
            return line
        return f"{line}."

    def process_description(self, desc: Union[List[str], str]) -> Union[List[str], str]:
        try:
            if isinstance(desc, str):
                return self.fix_desc_str(desc)
            else:  # assume list
                return [self.fix_desc_str(x) for x in desc]
        except Exception as e:
            raise YAMLDocException(desc) from e

    def process_options(
        self, opts: Dict[str, Any], suboptions_kw: str
    ) -> Dict[str, Any]:
        try:
            for option in opts.values():
                if "description" in option:
                    option["description"] = self.process_description(
                        option["description"]
                    )
                if suboptions_kw in option:
                    option[suboptions_kw] = self.process_options(
                        option[suboptions_kw], suboptions_kw
                    )
            return opts
        except Exception as e:
            raise YAMLDocException(opts, suboptions_kw) from e

    def process_documentation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if data.get("short_description", " ").endswith("."):
                data["short_description"] = data["short_description"].rstrip(".")
            if desc := data.get("description"):
                data["description"] = self.process_description(desc)
            if notes := data.get("notes"):
                data["notes"] = self.process_description(notes)
            if seealso := data.get("seealso"):
                for sa in seealso:
                    if sa_desc := sa.get("description"):
                        sa["description"] = self.process_description(sa_desc)
            if options := data.get("options"):
                data["options"] = self.process_options(options, "suboptions")

            return data
        except Exception as e:
            raise YAMLDocException(data) from e

    def process_return(self, data: Dict[str, Dict]) -> Dict[str, Dict]:
        try:
            data = self.process_options(data, "contains")
            return data
        except Exception as e:
            raise YAMLDocException(data) from e

    def get_processor(self, variable: str, in_doc_fragments: bool = False) -> Callable:
        processors_map = {
            "DOCUMENTATION": self.process_documentation,
            "RETURN": self.process_return,
        }
        return processors_map.get(
            variable, self.process_documentation if in_doc_fragments else lambda x: x
        )

    def process_yaml(self, quoted_content: List[str], processor: Callable) -> List[str]:

        data = self.read_yaml("\n".join(quoted_content))
        if not data:
            # If no data (e.g. an empty or comment-only block), then keep original content
            return quoted_content

        data = processor(data)
        # trying to determine whether the content is in JSON format of YAML
        # if isinstance(data, dict):
        #     for k, v in data.items():
        #         if isinstance(v, dict):
        #             print("=" * 15)
        #             print(f"{k}.sample = {v.get('sample')}")
        #             print(f"{k}.sample = {type(v.get('sample'))}")
        #             print(f"{v}")
        yaml_content = self.dump_yaml(data)
        yaml_content = yaml_content.splitlines()
        if isinstance(data, list):
            yaml_content = [
                (line[2:] if line.startswith("  ") else line) for line in yaml_content
            ]
        while yaml_content[0] == "":
            yaml_content = yaml_content[1:]

        # Do the YAML parsing in dry run, but return the original content
        if self.dry_run:
            return quoted_content
        return yaml_content

    def postprocess_content(self, in_variable: str, content: List[str]) -> List[str]:
        if self.offenders and in_variable != "EXAMPLES":
            fixed_content = self.process_offenders(content)
            if self.fix_offenders:
                content = fixed_content
        if in_variable != "EXAMPLES":
            fixed_content = self.postprocess_line_length(content)
            if self.fix_offenders:
                content = fixed_content
        return content

    def postprocess_line_length(self, content: List[str]) -> List[str]:
        hard_limit = 160

        LINE_RE = re.compile(r"^(\s*[-\s]\s)\S.*")
        results = []
        for line in content:
            if len(line) <= hard_limit:
                results.append(line)
                continue

            if match := LINE_RE.match(line):
                lead_spaces = len(match.group(1)) * " "
                line_split = line.split(" ")
                first_part = f'{" ".join(line_split[:-1])}'
                last_part = f"{lead_spaces}{line_split[-1]}"

                if len(first_part) > hard_limit:
                    first_part = f"{first_part} {FIXME_TAG}"
                if len(last_part) > hard_limit:
                    last_part = f"{last_part} {FIXME_TAG}"
                results.append(first_part)
                results.append(last_part)
            else:
                results.append(f"{line} {FIXME_TAG}")
        return results

    # pylint: disable=attribute-defined-outside-init
    def process_file(self, file_path: Path):
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
        self.first_line_no = 0

        for line_no, line in enumerate(lines):
            line = line.rstrip()
            if in_variable:
                if not re.match(rf"^\s*{QUOTE_RE_FRAG}", line):
                    quoted_content.append(line)
                    continue

                updated_lines.append(first_line)
                outbound_content = self.process_yaml(
                    quoted_content,
                    self.get_processor("DOCUMENTATION" if is_doc_frag else in_variable),
                )
                updated_lines.extend(
                    self.postprocess_content(in_variable, outbound_content)
                )
                updated_lines.append('"""')

                in_variable = ""
                quoted_content = []
                self.first_line_no = 0

            else:
                if ONELINE_RE.search(line):
                    updated_lines.append(re.sub(QUOTE_RE_FRAG, '"""', line))
                elif match := FIRST_LINE_RE.search(line):
                    in_variable, yaml_first_line = match.groups()
                    first_line = f'{in_variable} = r"""{yaml_first_line}'
                    self.first_line_no = line_no
                else:
                    updated_lines.append(line)

        if not self.dry_run:
            # Write the updated lines back to the file
            with open(file_path, "w") as file:
                file.writelines([f"{x}\n" for x in updated_lines])

    @staticmethod
    def calculate_indent(num: int):
        return dict(mapping=num, sequence=num + 2, offset=2)

    # pylint: disable=attribute-defined-outside-init
    def run(self, context):
        self.offenders = context.args.offenders or context.args.fix_offenders
        self.fix_offenders = context.args.fix_offenders
        self.dry_run = context.args.dry_run
        self.width = context.args.width
        self.indent = self.calculate_indent(context.args.indent)
        self.yaml = self.make_yaml_instance()

        for file_path in context.args.files:
            self.process_file(file_path)
