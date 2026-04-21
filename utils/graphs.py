#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import seaborn as sns

from typing import Any, Dict, Optional

__all__ = [
    'prep_plots'
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

    if rcParam:
        for key, value in rcParams.items():
            plt.rcParams[key] = value

    if 'constrained_layout' not in kwargs:
        kwargs['constrained_layout'] = True

    return plt.subplots(constrained_layout=constrained_layout, **kwargs)
