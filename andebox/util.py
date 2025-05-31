# -*- coding: utf-8 -*-
# Copyright (c) 2021-2023, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
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


# code: language=python tabSize=4
