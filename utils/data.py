#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from typing import Callable, List, Optional

from .utilities import DirType, resolve_directory

__all__ = [ "get_dataframe" ]

def get_dataframe(filename: str,
                  subdir: Optional[Union[List[str], str]] = None,
                  drop_columns: Optional[List[str]] = None,
                  drop_rows: Optional[List] = None,
                  precache_function: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
                  **kwargs) -> pd.DataFrame:
    # TODO: Document
    cache_dir = resolve_directory(DirType.DATA_CACHE, subdir)
    cache_file_name = cache_dir / f'{filename}.parquet'
    csv_file_name = resolve_directory(DirType.DATA_CSV, subdir) / f'{filename}.csv'
    try:
        df = pd.read_parquet(cache_file_name)
    except:
        df = pd.read_csv(csv_file_name)
        if drop_columns:
            df = df.drop(drop_columns, axis=1)
        if drop_rows:
            df = df.drop(drop_rows, axis=0)

        if precache_function:
            df = precache_function(df)

        cache_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        df.to_parquet(cache_file_name, compression='gzip')

    return df

