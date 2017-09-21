#!/usr/bin/env python

import os
import subprocess as sp
from docutils.core import publish_doctree

# Extract the example from the README
HERE = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(HERE, '..', 'README.rst')
doctree = publish_doctree(open(readme).read())
for i in doctree.traverse():
    if i.tagname == 'literal_block':
        break

# Run it
exec(i.astext())

# send useful info to the driver script
print('\n\n# TO_RUN: export REMOTE_FN="{0}"; export HUB_URL="{1}"\n\n'.format(os.path.dirname(hub.remote_fn), hub.url))
