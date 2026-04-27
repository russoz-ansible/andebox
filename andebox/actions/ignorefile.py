# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
import re
import sys
from dataclasses import dataclass
from functools import reduce, total_ordering
from pathlib import Path
from typing import Optional

import typer

from ..context import andebox_context


class IgnoreFileEntry:
    pattern = re.compile(r"^(?P<filename>\S+)\s(?P<ignore>\S+)(?:\s+#\s*(?P<comment>\S.*\S))?\s*$")
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
        return f"{self.ignore}:{self.error_code}" if self.error_code else self.ignore

    @property
    def rebuilt_comment(self):
        return f" # {self.comment}" if self.comment else ""

    @property
    def file_parts(self):
        if self.file_parts_depth is None:
            return str(Path(*self._file_parts))

        return str(Path(*self._file_parts[: self.file_parts_depth]))

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
            ffilter = ffilter if isinstance(ffilter, re.Pattern) else re.compile(ffilter)
            if not ffilter.search(match.group("filename")):
                return None

        ifilter = IgnoreFileEntry.filter_checks
        if ifilter is not None:
            ifilter = ifilter if isinstance(ifilter, re.Pattern) else re.compile(ifilter)
            if not ifilter.search(match.group("ignore")):
                return None

        return IgnoreFileEntry(match.group("filename"), match.group("ignore"), match.group("comment"))


# pragma: no cover
@total_ordering
@dataclass
class ResultLine:
    file_part: str
    ignore_check: str
    count: int = 1

    def increase(self) -> "ResultLine":
        self.count = self.count + 1
        return self

    def __lt__(self, other) -> bool:
        return self.count < other.count

    def __str__(self) -> str:
        r = [f"{self.count:6} "]
        if self.file_part:
            r.append(" ")
            r.append(self.file_part)
        if self.ignore_check:
            r.append(" ")
            r.append(self.ignore_check)
        return "".join(r)

    def __repr__(self) -> str:
        r = ["<ResultLine: ", str(self.count), ","]
        if self.file_part:
            r.append(" ")
            r.append(self.file_part)
        if self.ignore_check:
            r.append(" ")
            r.append(self.ignore_check)
        r.append(">")
        return "".join(r)


# pylint: disable=consider-using-with
def _make_fh_list_for_version(sanity_test_path, ignore_file_spec):
    if ignore_file_spec == "-":
        return [sys.stdin]
    if ignore_file_spec:
        return [open(sanity_test_path / f"ignore-{ignore_file_spec}.txt")]

    return [p.open() for p in sanity_test_path.iterdir() if p.name.startswith("ignore-") and p.name.endswith(".txt")]


def _read_ignore_file(fh):
    result = []
    with fh:
        for line in fh.readlines():
            entry = IgnoreFileEntry.parse(line)
            if entry:
                result.append(entry)
    return result


def _retrieve_ignore_entries(sanity_test_path, ignore_file_spec):
    return reduce(
        lambda a, b: a + b,
        [_read_ignore_file(fh) for fh in _make_fh_list_for_version(sanity_test_path, ignore_file_spec)],
    )


def _filter_lines(lines, num):
    if num == 0:
        return lines
    return lines[num:] if num < 0 else lines[:num]


app = typer.Typer(name="ignores", help="gathers stats on ignore*.txt file(s)")


@app.callback(invoke_without_command=True)
def ignores_cmd(
    ctx: typer.Context,
    spec: Optional[str] = typer.Option(None, "--spec", "-s", help="use ignore-SPEC.txt, or pass '-' to read from stdin"),
    depth: Optional[int] = typer.Option(None, "--depth", "-d", help="path depth for grouping files"),
    filter_files: Optional[str] = typer.Option(
        None,
        "--filter-files",
        "-ff",
        help="regular expression matching file names to be included",
    ),
    filter_checks: Optional[str] = typer.Option(
        None,
        "--filter-checks",
        "-fc",
        help="regular expression matching checks in ignore files to be included",
    ),
    suppress_files: bool = typer.Option(
        False,
        "--suppress-files",
        "-sf",
        help="supress file names from the output, consolidating the results",
    ),
    suppress_checks: bool = typer.Option(
        False,
        "--suppress-checks",
        "-sc",
        help="suppress the checks from the output, consolidating the results",
    ),
    head: int = typer.Option(
        10,
        "--head",
        "-H",
        help="number of lines to display in the output: leading lines if positive, trailing lines if negative, all lines if zero.",
    ),
) -> None:
    if filter_files:
        IgnoreFileEntry.filter_files = re.compile(filter_files)
    if filter_checks:
        IgnoreFileEntry.filter_checks = re.compile(filter_checks)
    if depth:
        IgnoreFileEntry.file_parts_depth = depth

    with andebox_context(ctx) as context:
        try:
            ignore_entries = _retrieve_ignore_entries(context.sanity_test_subdir, spec)
        except Exception as e:
            print(
                f"Error reading ignore file {spec}: {e}",
                file=sys.stderr,
            )
            raise e

        count_map = {}
        for entry in ignore_entries:
            fp = entry.file_parts if not suppress_files else ""
            ic = entry.ignore_check if not suppress_checks else ""
            key = fp + "|" + ic
            count_map[key] = count_map.get(key, ResultLine(fp, ic, 0)).increase()

        lines = [str(s) for s in sorted(count_map.values(), reverse=True)]
        print("\n".join(_filter_lines(lines, head)))
