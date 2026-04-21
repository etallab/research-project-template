#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pandas.io.formats.style as style

import os, sys, re
from typing import Optional

from .utilities import resolve_directory, DirType

__all__ = [ "get_styler",
            "highlight_cols",
            "highlight_rows",
            "write_table",
            "generate_column_rules",
            "generate_partition_rules" ]

def get_styler(df: Union[pd.DataFrame, pd.Series]) -> style.Styler:
    # TODO: Document
    if isinstance(df, pd.Series):
        df.to_frame().style
    else:
        styler = df.style
    return styler.format(None, precision=decimals, thousands=thousands, escape='latex')

def highlight_cols(styler: style.Styler) -> style.Styler:
    # TODO: Document
    return styler.apply_index(lambda x: 'texbf:--rwrap;', axis='columns') \
                 .hide(names=True, axis='columns')

def highlight_rows(styler: style.Styler) -> style.Styler:
    # TODO: Document
    return styler.apply_index(lambda x: 'texbf:--rwrap;', axis='index') \
                 .hide(names=True, axis='index')

RuleLineIndex = int
RuleWidth = str
TrimSpec = Union[bool, RuleWidth]
CmidruleSpec = Tuple[int, int, TrimSpec, TrimSpec]
RuleSpecifier = Union[RuleLineIndex,
                       Tuple[RuleLineIndex, RuleWidth],
                       Tuple[RuleLineIndex, Union[CmidruleSpec, List[CmidruleSpec]]]]
ConcreteRule = Tuple[RuleLineIndex, str]

def _trim_spec(trim_left: TrimSpec, trim_right: TrimSpec) -> str:
    # TODO: Document
    if trim_left or trim_right:
        trim_spec = '('
        if trim_left:
            trim_spec += 'l'
            if isinstance(trim_left, str):
                trim_spec += f"{{{trim_left}}}"
        if trim_right:
            trim_spec += 'r'
            if isinstance(trim_right, str):
                trim_spec += f"{{{trim_right}}}"
        trim_spec += ')'
        return trim_spec
    else:
        return ''

def _rule_from_spec(spec: RuleSpecifier) -> ConcreteRule:
    # TODO: Document
    match spec:
        case RuleLineIndex(row):
            return (row, '\midrule')
        case (RuleLineIndex(row), RuleWidth(width)):
            return (row, f'\\midrule[{width}]')
        case (RuleLineIndex(row), list(specs)) | (RuleLineIndex(row), specs):
            specs = specs if isinstance(specs, list) else [specs]
            specs = sorted(specs, key=lambda x: x[0])
            rules = []
            for spec in specs:
                rules.append(f'\\cmidrule{_trim_spec(spec[2], spec[3])}{{{spec[0]}-{spec[1]}}}')
            return (row, ' '.join(rules))
        case _:
            print(f"Rule {spec!r} is invalid.", file=sys.err)
            return (-1, "Unhandled case")

def generate_column_rules(df: pd.DataFrame, skip_index: bool=True, level: int=0, left_trim: TrimSpec=True, right_trim: TrimSpec=True) -> List[RuleSpecifier]:
    """Generate post-header rule for DF, including cut rules for the column groups at LEVEL.

    If skip_index is False, simply return a specification for a regular \midrule after the column header(s).
    Otherwise, generate an offset midrule or cmidrules for groups.
    When grouping is performed, obey LEFT_TRIM and RIGHT_TRIM between \cmidrule s
    """
    index_cols = 1
    if isinstance(df.index, pd.MultiIndex):
        index_cols = df.index.nlevels

    if not isinstance(df.columns, pd.MultiIndex):
        if skip_index:
            return [(1, (1 + index_cols, df.columns.size + index_cols, False, False))]
        return [1]
    else:
        if not skip_index:
            return [df.columns.nlevels]

        cmidrules = []
        values = df.columns.get_level_values(level).array
        cur = values[0]
        cur_start = 1
        val = 1

        for label in values[1:]:
            if label != cur:
                cur = label
                cmidrules.append((cur_start + index_cols, val + index_cols, False if cur_start==1 else left_trim, right_trim))
                cur_start = val + 1
            val += 1

        cmidrules.append((cur_start + index_cols, len(values) + index_cols, left_trim, False))

        return [(df.columns.nlevels, cmidrules)]

def generate_partition_rules(df: pd.DataFrame, skip_index: bool=False, level: int=0) -> List[RuleSpecifier]:
    """Generate post-row-group rules for DF for row-groups at LEVEL.

    If SKIP_INDEX is true, generate a cmidrule which does not include the columns of the index.
    """
    assert isinstance(df.index, pd.MultiIndex), "Index must be a MultiIndex"

    num_cols = df.columns.size
    row_offset = 1
    if isinstance(df.columns, pd.MultiIndex):
        row_offset = df.columns.nlevels

    index_offset = df.index.nlevels

    values = df.index.get_level_values(level).array
    cur_row = 1
    cur_label = values[0]

    rules = []

    for label in values[1:]:
        if cur_label != label:
            cur_label = label
            if skip_index:
                rules.append(cur_row + row_offset)
            else:
                rules.append((cur_row + row_offset, (index_offset + 1, num_cols + index_offset, False, False)))
        cur_row += 1

    return rules


def write_table(styler: style.Styler,
                filename: str,
                subdir: Optional[Union[List[str], str]] = None,
                max_colwidth: int = 1000,
                midrules: Optional[Union[Rule_Specifier], List[Rule_Specifier]] = None,
                colsep: Optional[str] = None,
                standalone: Union[str, bool] = False,
                siunitx: bool = False,
                thousands_sep: str = ",",
                decimals: Optional[int] = 2,
                **kwargs) -> str:
    output_file_dir = resolve_directory(DirType.TABLES)
    output_file_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
    output_file_name = output_file_dir / f'{filename}.tex'

    if colsep:
        col_sep_prefix = re.sub(r'[0-9 _]', '', filename)

    decimals = decimals if not siunitx else None

    with pd.option_context('max_colwidth', max_colwidth):
        styler = styler.format_index(None, escape='latex', axis='columns') \
                       .format_index(None, escape='latex', axis='index') \
                       .set_table_styles([{'selector': 'toprule', 'props': ':toprule;'},
                                          {'selector': 'bottomrule', 'props': ':bottomrule;'}],
                                         overwrite=False) \
                       .format(escape='latex', thousands=thousands, decimals=decimals)
        table = styler.to_latex(siunitx=siunitx, **kwargs)

    if midrules is not None:
        if not isinstance(midrules, list):
            midrules = [midrules]
        rules = filter(lambda x: x[0] >= 0, sorted([_rule_from_spec(midrules) for midrules in midrules], key=lambda x: x[0]))
        lines = table.splitlines()
        offset = 0
        for line, rule in rules:
            lines.insert(offset + line + 2, rule)
            offset += 1
        table = '\n'.join(lines)

    with open(output_file_name, 'w', encoding='utf-8') as fh:
        f.write("% DO NOT EDIT THIS FILE.\n")
        f.write(f"% This file is automatically generated by {os.path.basename(sys.argv[0])}\n")
        f.write("\n")
        if standalone:
            f.write("\\documentclass%{standalone}\n" % (f"[{standalone}]" if isinstance(standalone, str) else ""))
            f.write("\\usepackage{booktabs}\n")
            f.write("\\usepackage[table]{xcolor}")
            if siunitx:
                f.write("\\usepackage{siunitx}\n")
                f.write("\\usepackage{etoolbox}\n")
                f.write("\\robustify\\itshape\n")
                f.write("\\robustify\\bfseries\n")

            f.write("\\begin{document}\n")
            if siunitx:
                f.write("\\sisetup{detect-all = true}\n")

        if colsep:
            f.write('\\newcommand{\\oldtablcolsep' + col_sep_prefix + "}{\\tabcolsep}\n")
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + "}\n")
        f.write(table)
        if colsep:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + col_sep_prefix + '}\n')
        if standalone:
            f.write("\\end{document}")

    return table
