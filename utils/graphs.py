#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import seaborn as sns

from typing import Any, Dict, Optional, Union, List, Tuple

from .utilities import resolve_directory, DirType

__all__ = [
    'prep_plots',
    'save_plots'
]


def prep_plots(figure_width: float = 6.0,
               figure_height: float = 5.0,
               dpi: float = 600.0,
               fontsize: int = 24,
               rcParams: Optional[Dict[str, Any]] = None,
               constrained_layout: bool = True,
               **kwargs):
    # TODO: Document
    sns.set(style='whitegrid', palette='colorblind')
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    plt.rcParams['figure.figsize'] = [figure_width, figure_height]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['font.size'] = fontsize

    if rcParams:
        for key, value in rcParams.items():
            plt.rcParams[key] = value

    return plt.subplots(constrained_layout=constrained_layout, **kwargs)


def save_plots(fig: plt.Figure,
               name: str,
               subdir:  Optional[Union[List[str], str]] = None,
               formats: List[Union[str, Tuple[str, Dict[str, Any]]]] = ['pdf',
                                                                        'png'],
               **kwargs):
    # TODO: Document
    out_dir = resolve_directory(DirType.FIGURES, subdir)
    for out_format in formats:
        match out_format:
            case str(extension):
                out_file = out_dir / f'{name}.{extension}'
                fig.savefig(out_file, **kwargs)
            case (extension, subkwargs):
                out_file = out_dir / f'{name}.{extension}'
                args = {}
                for key, value in kwargs.items():
                    args[key] = value
                for key, value in subkwargs.items():
                    args[key] = value
                fig.savefig(out_file, **args)
