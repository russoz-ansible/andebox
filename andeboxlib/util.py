import os
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def set_dir(path):
    previous = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(previous)
