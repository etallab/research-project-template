#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from enum import StrEnum
import os

from typing import List, Optional, Union, Dict

__all__ = [
    'resolve_directory',
    'DirType'
]


def _get_default_root() -> Path:
    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError('Unable to find project root relative to "%s".' \
                            % (__file__))


class DirType(StrEnum):
    ROOT = 'ROOT'
    DATA = 'DATA'
    DATA_CACHE = 'cache'
    DATA_RAW = 'raw'
    DATA_CSV = 'csv'
    OUT = 'OUT'
    FIGURES = 'figs'
    TABLES = 'tables'


DIRS: Dict[DirType, Path] = {}

DIRS[DirType.ROOT] = Path(os.environ.get("ROOT_DIR", _get_default_root())) \
    .resolve()

DIRS[DirType.DATA] = Path(os.environ.get("DATA_DIR",
                                         DIRS[DirType.ROOT] / 'data')) \
    .resolve()
DIRS[DirType.DATA_CACHE] = Path(os.environ.get("CACHE_DIR",
                                               DIRS[DirType.DATA] / 'cache')) \
    .resolve()
DIRS[DirType.DATA_RAW] = Path(os.environ.get("RAW_DIR",
                                             DIRS[DirType.ROOT] / 'raw')) \
    .resolve()
DIRS[DirType.DATA_CSV] = Path(os.environ.get("CSV_DIR",
                                             DIRS[DirType.ROOT] / 'csv')) \
    .resolve()

DIRS[DirType.OUT] = Path(os.environ.get("OUT_DIR",
                                        DIRS[DirType.ROOT] / 'out')) \
    .resolve()
DIRS[DirType.FIGURES] = Path(os.environ.get("FIGURES_DIR",
                                            DIRS[DirType.OUT] / 'figures')) \
    .resolve()
DIRS[DirType.TABLES] = Path(os.environ.get("TABLES_DIR",
                                           DIRS[DirType.OUT] / 'tables')) \
    .resolve()


def resolve_directory(dir_type: DirType,
                      subdir: Optional[Union[List[str], str]] = None,
                      ensure_exists: bool = True) -> Path:
    # TODO: Document
    directory = DIRS[dir_type]

    if isinstance(subdir, str):
        directory = directory / subdir
    elif isinstance(subdir, list):
        for sub in subdir:
            directory = directory / sub

    if ensure_exists:
        directory.mkdir(0o755, parents=True, exist_ok=True)
    return directory
