#!/usr/bin/env python

"""
This script expects a single `.. code-block:: python` directive which appears
as a "literal_block" to the docutils parser. This block is then executed just
like a doctest.

It's much easier to write and debug from ReST when syntax highlighting is
working. Currently it's working with `.. code-block:: python` but not with `..
testcode::`. Furthermore, I'd like to have the README tested, but the GitHub
ReST renderer doesn't support `.. testcode::` directive and so we're stuck with
``..  code-block:: python``.
"""

from pathlib import Path
import subprocess as sp
import os
from docutils.core import publish_doctree

HERE = Path(__file__).resolve().parent

repo_top = HERE.parent

orig_dir = os.getcwd()


for line in open(HERE / "example_hubs.tsv"):
    line = line.strip()
    if line.startswith('#') or not line:
        continue
    source, dest = line.split('\t')
    source = Path(source)
    dest = Path(dest)
    dest_dir = dest.parent
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Use docutils to convert rst to doctree and pull out the first literal
    # block encountered.
    rst = repo_top / source
    doctree = publish_doctree(open(rst).read())
    block = None
    for i in doctree.traverse():
        if i.tagname == "literal_block":
            block = i
            break

    # Thanks https://stackoverflow.com/a/28482312 for empty globals dict
    _globals = {}
    s = block.astext()
    try:
        os.chdir(repo_top)
        exec(s,  _globals)
    finally:
        os.chdir(orig_dir)


    # Save a copy of the script too
    with open(dest_dir / 'source.py', 'w') as fout:
        fout.write(s)
