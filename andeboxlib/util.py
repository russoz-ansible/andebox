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
