# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import re
import sys
from functools import reduce

from looseversion import LooseVersion

from .base import AndeboxAction


class IgnoreFileEntry:
    pattern = re.compile(
        r"^(?P<filename>\S+)\s(?P<ignore>\S+)(?:\s+#\s*(?P<comment>\S.*\S))?\s*$"
    )
    filter_files = None
    filter_checks = None
    file_parts_depth = None

    def __init__(self, filename, ignore, comment):
        self.filename = filename
        self._file_parts = self.filename.split("/")

        if ":" in ignore:
            self.ignore, self.error_code = ignore.split(":")
        else:
            self.ignore, self.error_code = ignore, None
        self.comment = comment

    @property
    def ignore_check(self):
        return "{self.ignore}:{self.error_code}" if self.error_code else self.ignore

    @property
    def rebuilt_comment(self):
        return " # {self.comment}" if self.comment else ""

    @property
    def file_parts(self):
        if self.file_parts_depth is None:
            return os.path.join(*self._file_parts)

        return os.path.join(*self._file_parts[: self.file_parts_depth])

    def __str__(self):
        return f"<IgnoreFileEntry: {self.filename} {self.ignore_check}{self.rebuilt_comment}>"

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse(line):
        match = IgnoreFileEntry.pattern.match(line)
        if not match:
            raise ValueError(f"Line cannot be parsed as an ignore-file entry: {line}")

        ffilter = IgnoreFileEntry.filter_files
        if ffilter is not None:
            ffilter = (
                ffilter if isinstance(ffilter, re.Pattern) else re.compile(ffilter)
            )
            if not ffilter.search(match.group("filename")):
                return None

        ifilter = IgnoreFileEntry.filter_checks
        if ifilter is not None:
            ifilter = (
                ifilter if isinstance(ifilter, re.Pattern) else re.compile(ifilter)
            )
            if not ifilter.search(match.group("ignore")):
                return None

        return IgnoreFileEntry(
            match.group("filename"), match.group("ignore"), match.group("comment")
        )


class ResultLine:
    def __init__(self, file_part, ignore_check, count=1):
        self.file_part = file_part
        self.ignore_check = ignore_check
        self.count = count

    def increase(self):
        self.count = self.count + 1
        return self

    def __lt__(self, other):
        return self.count < other.count

    def __le__(self, other):
        return self.count <= other.count

    def __gt__(self, other):
        return self.count > other.count

    def __ge__(self, other):
        return self.count >= other.count

    def __eq__(self, other):
        return self.count == other.count

    def __ne__(self, other):
        return self.count != other.count

    def __str__(self):
        r = [f"{self.count:6} "]
        if self.file_part:
            r.append(" ")
            r.append(self.file_part)
        if self.ignore_check:
            r.append(" ")
            r.append(self.ignore_check)
        return "".join(r)

    def __repr__(self):
        r = ["<ResultLine: ", str(self.count), ","]
        if self.file_part:
            r.append(" ")
            r.append(self.file_part)
        if self.ignore_check:
            r.append(" ")
            r.append(self.ignore_check)
        r.append(">")
        return "".join(r)


_ignore_path = os.path.join(".", "tests", "sanity")
try:
    with os.scandir(os.path.join(_ignore_path)) as sanity_dir:
        _ignore_versions = sorted(
            [
                str(LooseVersion(entry.name[7:-4]))
                for entry in sanity_dir
                if entry.name.startswith("ignore-") and entry.name.endswith(".txt")
            ]
        )
except FileNotFoundError:
    _ignore_versions = []


class IgnoreLinesAction(AndeboxAction):
    name = "ignores"
    help = "gathers stats on ignore*.txt file(s)"
    args = [
        dict(
            names=["--ignore-file-spec", "-ifs"],
            specs=dict(
                choices=_ignore_versions + ["-"],
                help=(
                    "Use the ignore file matching this Ansible version. "
                    "The special value '-' may be specified to read "
                    "from stdin instead. If not specified, will use all available files. "
                    "If no choices are presented, the collection structure was not recognized."
                ),
            ),
        ),
        dict(
            names=["--depth", "-d"],
            specs=dict(type=int, help="Path depth for grouping files"),
        ),
        dict(
            names=["--filter-files", "-ff"],
            specs=dict(
                type=re.compile, help="Regexp matching file names to be included"
            ),
        ),
        dict(
            names=["--filter-checks", "-fc"],
            specs=dict(
                type=re.compile,
                help="Regexp matching checks in ignore files to be included",
            ),
        ),
        dict(
            names=["--suppress-files", "-sf"],
            specs=dict(
                action="store_true",
                help="Supress file names from the output, consolidating the results",
            ),
        ),
        dict(
            names=["--suppress-checks", "-sc"],
            specs=dict(
                action="store_true",
                help="Suppress the checks from the output, consolidating the results",
            ),
        ),
        dict(
            names=["--head", "-H"],
            specs=dict(
                type=int,
                default=10,
                help=(
                    "Number of lines to display in the output: leading lines if "
                    "positive, trailing lines if negative, all lines if zero."
                ),
            ),
        ),
    ]

    # pylint: disable=consider-using-with
    def make_fh_list_for_version(self, version):
        if version == "-":
            return [sys.stdin]
        if version:
            return [open(os.path.join(_ignore_path, f"ignore-{version}.txt"))]

        with os.scandir(os.path.join(_ignore_path)) as it:
            return [
                open(os.path.join(_ignore_path, entry.name))
                for entry in it
                if entry.name.startswith("ignore-") and entry.name.endswith(".txt")
            ]

    @staticmethod
    def read_ignore_file(fh):
        result = []
        with fh:
            for line in fh.readlines():
                entry = IgnoreFileEntry.parse(line)
                if entry:
                    result.append(entry)
        return result

    def retrieve_ignore_entries(self, version):
        return reduce(
            lambda a, b: a + b,
            [
                self.read_ignore_file(fh)
                for fh in self.make_fh_list_for_version(version)
            ],
        )

    @staticmethod
    def filter_lines(lines, num):
        if num == 0:
            return lines
        return lines[num:] if num < 0 else lines[:num]

    def run(self, context):
        if context.args.filter_files:
            IgnoreFileEntry.filter_files = context.args.filter_files
        if context.args.filter_checks:
            IgnoreFileEntry.filter_checks = context.args.filter_checks
        if context.args.depth:
            IgnoreFileEntry.file_parts_depth = context.args.depth

        try:
            ignore_entries = self.retrieve_ignore_entries(context.args.ignore_file_spec)
        except Exception as e:
            print(
                "Error reading ignore file {context.args.ignore_file_spec}: {e}",
                file=sys.stderr,
            )
            raise e

        count_map = {}
        for entry in ignore_entries:
            fp = entry.file_parts if not context.args.suppress_files else ""
            ic = entry.ignore_check if not context.args.suppress_checks else ""
            key = fp + "|" + ic
            count_map[key] = count_map.get(key, ResultLine(fp, ic, 0)).increase()

        lines = [str(s) for s in sorted(count_map.values(), reverse=True)]
        print("\n".join(self.filter_lines(lines, context.args.head)))
