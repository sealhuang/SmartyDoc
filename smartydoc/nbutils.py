# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import io
import sys

import nbformat

def merge_notebook(in_nbs, out_nb):
    """Usage:
    
    merge_notebook(['A.ipynb', 'B.ipynb', 'C.ipynb'], 'merged.ipynb')
    """
    merged = None

    for fname in in_nbs:
        with io.open(fname, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        if merged is None:
            merged = nb
        else:
            # TODO: add an optional marker between joined notebooks
            # like an horizontal rule, for example, or some other arbitrary
            # (user specified) markdown cell)
            merged.cells.extend(nb.cells)

    if not hasattr(merged.metadata, 'name'):
        merged.metadata.name = ''
    merged.metadata.name += '_merged'

    nbformat.write(merged, out_nb)


