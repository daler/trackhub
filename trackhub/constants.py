from __future__ import absolute_import

from .parsed_params import param_defs, TRACKTYPES

# http://genome-source.cse.ucsc.edu/gitweb/
#       ?p=kent.git;a=blob;f=src/hg/makeDb/trackDb/README;hb=HEAD

param_dict = {i.name: i for i in param_defs}

# These should at least be first...
initial_params = ['track', 'bigDataUrl', 'shortLabel', 'longLabel', 'type']

track_fields = {i: initial_params[:] for i in TRACKTYPES}

observed_types = set()
for param in param_defs:
    observed_types.update(param.types)

for tracktype in observed_types:
    lst = track_fields[tracktype]
    for param in param_defs:
        if tracktype in param.types:
            lst.append(param.name)
