#!/usr/bin/env python

"""
It's much easier to write and debug from ReST when syntax highlighting is
working. Currently it's working with `.. code-block:: python` but not with `..
testcode::`. Furthermore, I'd like to have the README tested, but the GitHub
ReST renderer doesn't support `.. testcode::` directive and so we're stuck with
``..  code-block:: python``.

This script expects a single `.. code-block:: python` directive which appears
as a "literal_block" to the docutils parser. This block is then executed just
like a doctest.

"""

import os
import subprocess as sp
from docutils.core import publish_doctree

# Extract the example from the README
HERE = os.path.abspath(os.path.dirname(__file__))

def extract_and_run(relpath):
    rst = os.path.join(HERE, relpath)
    doctree = publish_doctree(open(rst).read())
    for i in doctree.traverse():
        if i.tagname == 'literal_block':
            break
    exec(i.astext())


extract_and_run('../README.rst')
extract_and_run('../doc/source/assembly_example.rst')
extract_and_run('../doc/source/grouping.rst')
extract_and_run('../doc/source/html_doc.rst')
