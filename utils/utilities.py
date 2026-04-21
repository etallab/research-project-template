#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from enum import StrEnum
import os

from typing import List, Optional, Union

__all__ = [ 'resolve_directory', 'DirType' ]

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
            pass
        case DirType.DATA_RAW:
            pass
        case DirType.DATA_CSV:
            pass
        case DirType.FIGURES:
            pass
        case DirType.TABLES:
            pass

    if isinstance(subdir, str):
        directory = directory / subdir
    elif isinstance(subdir, list):
        for sub in subdir:
            directory = directory / sub

    return directory
