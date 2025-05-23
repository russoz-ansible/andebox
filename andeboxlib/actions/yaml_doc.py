# -*- coding: utf-8 -*-
# (c) 2024-2025, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import hashlib
import json
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
JSON_SAMPLE_PREFIX = "JSONSAMPLE"


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
    dict(regexp=r"\b(?:[Ww]i|')ll\b", apply=fixme),
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


class AnsibleDocProcessor:
    """Process YAML documentation blocks in Ansible module and plugin files.

    This class handles the specialized formatting and validation of YAML blocks
    commonly found in Ansible module and plugin files, such as:
    - DOCUMENTATION blocks containing module/plugin details
    - EXAMPLES blocks showing usage examples
    - RETURN blocks defining returned values
    - Doc fragments providing reusable documentation
    """

    def __init__(
        self,
        indent: int = 2,
        width: int = 120,
        offenders: bool = False,
        fix_offenders: bool = False,
        dry_run: bool = False,
    ):
        """Initialize the processor."""
        self.indent = indent
        self.width = width
        self.offenders = offenders
        self.fix_offenders = fix_offenders
        self.dry_run = dry_run
        self.yaml_indents = self._calculate_indent(indent)
        self.yaml = self.make_yaml_instance()
        self.first_line_no = 0
        self.json_samples = {}

    @staticmethod
    def _calculate_indent(num: int) -> Dict[str, int]:
        """Calculate indentation settings."""
        return dict(mapping=num, sequence=num + 2, offset=2)

    def make_yaml_instance(self) -> YAML:
        """Create a configured YAML instance."""
        yaml = YAML()
        yaml.indent(**self.yaml_indents)
        yaml.width = self.width
        yaml.preserve_quotes = True
        yaml.explicit_start = False
        yaml.preserve_quotes = True
        yaml.top_level_colon_align = False
        yaml.compact_seq_seq = False
        return yaml

    def read_yaml(self, content: str) -> Optional[Union[Dict[str, Any], list]]:
        """Read YAML content."""
        return self.yaml.load(content)

    def dump_yaml(self, data: Union[Dict[str, Any], list]) -> str:
        """Dump YAML content."""
        output = StringIO()
        self.yaml.dump(data, output)
        return output.getvalue()

    def fix_desc_str(self, line: str) -> str:
        """Fix description string formatting."""
        line = line.strip()
        line = re.sub(r"\s\s+", " ", line)
        if not line[0].isupper():
            line = line[0].upper() + line[1:]
        if line.endswith(".)"):
            return f"{line[:-2]})."
        if line.endswith(DESCRIPTION_ACCEPTED_END_CHARS):
            return line
        return f"{line}."

    def process_description(self, desc: Union[List[str], str]) -> Union[List[str], str]:
        """Process description strings."""
        try:
            if isinstance(desc, str):
                return self.fix_desc_str(desc)
            else:
                return [self.fix_desc_str(x) for x in desc]
        except Exception as e:
            raise YAMLDocException(desc) from e

    def _store_json_sample(self, sample: Any) -> str:
        """Store a JSON sample and return its unique ID."""
        # Create JSON string for hashing (without indentation to be more space efficient)
        json_str = json.dumps(sample)
        # Create a unique hash for the JSON content
        sample_hash = hashlib.md5(json_str.encode()).hexdigest()[:8]
        sample_id = f"{JSON_SAMPLE_PREFIX}-{sample_hash}"
        # Store the prettified JSON
        self.json_samples[sample_id] = json.dumps(sample, indent=self.indent)
        return sample_id

    def process_sample(self, sample: Any, type_: str) -> Any:
        """Process sample values."""
        output_sample = self.dump_yaml(sample)
        is_json = (type_ == "list" and output_sample.strip().startswith("[")) or (
            type_ == "dict" and output_sample.strip().startswith("{")
        )
        if not is_json:
            return sample
        # Store the JSON and return a placeholder ID
        return self._store_json_sample(sample)

    def process_options(
        self, opts: Dict[str, Any], suboptions_kw: str
    ) -> Dict[str, Any]:
        """Process options block."""
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
                if "sample" in option and option["type"] in ("list", "dict"):
                    option["sample"] = self.process_sample(
                        option["sample"], option["type"]
                    )
            return opts
        except Exception as e:
            raise YAMLDocException(opts, suboptions_kw) from e

    def process_documentation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process DOCUMENTATION block."""
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
        """Process RETURN block."""
        try:
            data = self.process_options(data, "contains")
            return data
        except Exception as e:
            raise YAMLDocException(data) from e

    def get_processor(self, variable: str, in_doc_fragments: bool = False) -> Callable:
        """Get the appropriate processor for the block type."""
        processors_map = {
            "DOCUMENTATION": self.process_documentation,
            "RETURN": self.process_return,
        }
        return processors_map.get(
            variable, self.process_documentation if in_doc_fragments else lambda x: x
        )

    def process_yaml(self, quoted_content: List[str], processor: Callable) -> List[str]:
        """Process YAML content."""
        data = self.read_yaml("\n".join(quoted_content))
        # If no data (e.g. an empty or comment-only block), then keep original content
        if not data:
            return quoted_content

        # Clear stored JSON samples before processing new content
        self.json_samples.clear()

        data = processor(data)
        yaml_content = self.dump_yaml(data).splitlines()

        if isinstance(data, list):
            yaml_content = [
                (line[2:] if line.startswith("  ") else line) for line in yaml_content
            ]
        while yaml_content and yaml_content[0] == "":
            yaml_content.pop(0)

        return quoted_content if self.dry_run else yaml_content

    def postprocess_content(self, in_variable: str, content: List[str]) -> List[str]:
        """Post-process content."""
        # First restore any JSON samples with proper indentation
        content = self.postprocess_json_samples(content)

        # Then apply other post-processing steps
        if self.offenders and in_variable != "EXAMPLES":
            fixed_content = self.process_offenders(content)
            if self.fix_offenders:
                content = fixed_content
        if in_variable != "EXAMPLES":
            fixed_content = self.postprocess_line_length(content)
            if self.fix_offenders:
                content = fixed_content
        return content

    def apply_offender_rule(self, line_num: int, line: str) -> str:
        """Apply offender rules to a line."""
        for regexp, spec in OFFENDING_SPEC:
            if match := regexp.match(line):
                if self.offenders and not self.fix_offenders:
                    print(f"  {line_num:4}: {line}")
                prefix, term, plural, suffix = match.groups()

                if func := spec.get("apply"):
                    return f"{prefix}{func(term)}{plural}{suffix}"
                elif repl := spec.get("replace"):
                    return f"{prefix}{repl}{plural}{suffix}"

        return line

    def process_offenders(self, content: List[str]) -> List[str]:
        """Process offending content."""
        result = []
        for num, line in enumerate(content):
            line_num = 2 + self.first_line_no + num

            def apply(line):
                return self.apply_offender_rule(line_num, line)

            prev_line = fixed_line = line
            while (fixed_line := apply(fixed_line)) != prev_line:
                prev_line = fixed_line

            if fixed_line != line:
                print(f"  {line_num:4}: {fixed_line}")
            result.append(fixed_line)

        return result

    def postprocess_json_samples(self, content: List[str]) -> List[str]:
        """Post-process JSON samples by restoring them with proper indentation.

        After processing, each sample is removed from the json_samples map.
        """
        result = []
        sample_pattern = re.compile(
            rf"^(\s+sample:)\s+({JSON_SAMPLE_PREFIX}-[0-9a-f]{{8}})$"
        )

        for line in content:
            match = sample_pattern.match(line)
            if (not match) or match.group(2) not in self.json_samples:
                result.append(line)
                continue

            indentend_sample_key = match.group(1)
            sample_id = match.group(2)

            json_lines = self.json_samples[sample_id].splitlines()
            base_indent = " " * (
                len(indentend_sample_key) - len("sample:") + self.indent
            )
            # Add first line with | marker
            result.append(f"{indentend_sample_key} |")
            # Add JSON lines with proper indentation
            result.extend(f"{base_indent}{line}" for line in json_lines)

            del self.json_samples[sample_id]

        return result

    def postprocess_line_length(self, content: List[str]) -> List[str]:
        """Post-process line lengths."""
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

    def process_file(self, file_path: Path) -> None:
        """Process a single file."""
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
                processor = self.get_processor(
                    "DOCUMENTATION" if is_doc_frag else in_variable
                )
                outbound_content = self.process_yaml(quoted_content, processor)
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
                    if yaml_first_line.endswith("---"):
                        yaml_first_line = yaml_first_line[:-3]
                    first_line = f'{in_variable} = r"""{yaml_first_line}'
                    self.first_line_no = line_no
                else:
                    updated_lines.append(line)

        if not self.dry_run:
            with open(file_path, "w") as file:
                file.writelines([f"{x}\n" for x in updated_lines])

        # Verify that all JSON samples were properly processed
        assert (
            len(self.json_samples) == 0
        ), f"Found unprocessed JSON samples: {list(self.json_samples.keys())}"


class YAMLDocAction(AndeboxAction):
    """Action to analyze and/or reformat YAML documentation in plugins."""

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

    def run(self, context):
        """Process YAML documentation in files."""
        processor = AnsibleDocProcessor(
            indent=context.args.indent,
            width=context.args.width,
            offenders=context.args.offenders or context.args.fix_offenders,
            fix_offenders=context.args.fix_offenders,
            dry_run=context.args.dry_run,
        )

        for file_path in context.args.files:
            processor.process_file(file_path)
