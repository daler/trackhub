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

workdir = HERE.parent

os.chdir(workdir)

target = workdir / 'example_hubs'
target.mkdir(exist_ok=True)


def extract_and_run(source, dest):
    rst = workdir / source
    doctree = publish_doctree(open(rst).read())
    for i in doctree.traverse():
        if i.tagname == "literal_block":
            break

    # Thanks https://stackoverflow.com/a/28482312 for empty globals dict
    _globals = {}
    s = i.astext()
    exec(s,  _globals)

    # Save a copy of the script too
    with open(dest / 'source.py', 'w') as fout:
        fout.write(s)


for line in open(HERE / "example_hubs.tsv"):
    source, dest = line.strip().split('\t')
    source = Path(source)
    dest = Path(dest)
    extract_and_run(source, dest)
