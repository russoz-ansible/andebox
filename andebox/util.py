# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021-2023 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021-2023 Alexei Znamensky
# SPDX-License-Identifier: MIT
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from typing import Generator


@contextmanager
def set_dir(path: Path) -> Generator[Any, Any, Any]:
    previous = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(previous)
