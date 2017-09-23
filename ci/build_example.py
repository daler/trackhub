#!/usr/bin/env python

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
