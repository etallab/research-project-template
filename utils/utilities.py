#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from enum import StrEnum
import os

from typing import List, Optional, Union

__all__ = [ 'resolve_directory',
            'DirType',
            'ROOT_DIR',
            'DATA_DIR',
            'CACHE_DIR',
            'RAW_DIR',
            'CSV_DIR',
            'OUT_DIR',
            'FIGURES_DIR',
            'TABLES_DIR' ]

def _get_default_root():
    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError(f"Unable to find project root relative to {__file__}.")

ROOT_DIR = Path(os.environ.get("ROOT_DIR", _get_default_root())).resolve()

DATA_DIR = Path(os.environ.get("CACHE_DIR", ROOT_DIR / 'data' )).resolve()
CACHE_DIR = Path(os.environ.get("CACHE_DIR", ROOT_DIR / 'data' / 'cache')).resolve()
RAW_DIR = Path(os.environ.get("RAW_DIR", ROOT_DIR / 'data' / 'raw')).resolve()
CSV_DIR = Path(os.environ.get("CSV_DIR", ROOT_DIR / 'data' / 'csv')).resolve()

OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT_DIR / 'out')).resolve()
FIGURES_DIR = Path(os.environ.get("FIGURES_DIR", OUT_DIR / 'figures')).resolve()
TABLES_DIR = Path(os.environ.get("TABLES_DIR", OUT_DIR / 'tables')).resolve()


class DirType(StrEnum):
    DATA_CACHE = 'cache'
    DATA_RAW = 'raw'
    DATA_CSV = 'csv'
    FIGURES = 'figs'
    TABLES = 'tables'

def resolve_directory(dir_type: DirType, subdir: Optional[Union[List[str], str]] = None) -> Path:
    directory = None
    match dir_type:
        case DirType.DATA_CACHE:
            directory = CACHE_DIR
        case DirType.DATA_RAW:
            directory = RAW_DIR
        case DirType.DATA_CSV:
            directory = CSV_DIR
        case DirType.FIGURES:
            directory = FIGURES_DIR
        case DirType.TABLES:
            directory = TABLES_DIR

    if isinstance(subdir, str):
        directory = directory / subdir
    elif isinstance(subdir, list):
        for sub in subdir:
            directory = directory / sub

    return directory
