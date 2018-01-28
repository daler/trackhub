import requests
import ruamel.yaml as yaml
from ruamel.yaml.scalarstring import PreservedScalarString, preserve_literal
import bs4
from collections import OrderedDict, defaultdict
from pprint import pprint
from textwrap import dedent

q = requests.get('https://genome.ucsc.edu/goldenPath/help/trackDb/trackDbHub.html')
soup = bs4.BeautifulSoup(q.text, 'lxml')

# This is where it appears the params and formats are defined
lib = soup.find('div', id='library')

# Identify which types are valid for hubs. We will filter out those params that
# can't be used on these types.
hub_div = soup.find('div', attrs={'class': 'type_for_hubs'})
hub_types = []
for i in hub_div.find_all('a'):
    # One of the types listed here is "bam/cram", but later divs specify type
    # as "bam". So here we include them as separate entries.
    hub_types.extend(i.text.split('/'))

# There is also an "all" class, so we need to add it here.
hub_types.append('all')

divs = lib.find_all('div')
ds = []
for div in divs:

    # Ordered dict so the YAML is more readable
    d = OrderedDict()

    # If the div had a span, then it's probably one of the top-level divs
    # representing a parameter and therefore its class name is the name of
    # the param.
    if div.span:
        assert len(div['class']) == 1
        d['name'] = div['class'][0]

        # Only consider the param if it applies to hub track types
        types = [i for i in
                 sorted(set(div.span['class']).difference(['types'])) if i ]
        if len(set(types).intersection(hub_types)) == 0:
            continue
        d['types'] = types

        # A handful of the fields are required or are required for hubs only.
        req = div.find('p', attrs={'class': 'isRequired'})
        if req:
            d['required'] = req.text.replace('Required: ', '')
        else:
            d['required'] = False

        # kind of a tricky part here
        txt = []
        for tag in div.find_all(['p', 'pre']):
            if not tag.has_attr('class'):
                for line in tag.text.splitlines():
                    txt.append(line.rstrip())
        d['text'] = '\n'.join(txt)
        d['text'] = preserve_literal(d['text'].replace('\r\n', '\n').replace('\r', '\n').strip())

        if 'NOT FOR HUBS' in d['text']:
            continue

        if 'Internal only' in d['text']:
            continue

        d['format'] = None

        others = div.find_all('div', attrs={'class': 'format'})
        if others:
            assert len(others) == 1
            d['format'] = others[0].text

        print(d)
        ds.append(d)


with open('params.yaml', 'w') as fout:
    yaml.round_trip_dump(ds, fout, Dumper=yaml.RoundTripDumper)
with open('params.json', 'w') as fout:
    import json
    json.dump(ds, fout)

# This should get us started on something to edit for a proper params.py
with open('params_autogen.py', 'w') as fout:
    type_params = defaultdict(list)
    params = {}
    for d in ds:
        for t in d['types']:
            type_params[t].append(d['name'])
        params[d['name']] = d
    for k, v in type_params.items():
        fout.write(dedent(
            """
            track_types["{k}"] = [
            """.format(k=k)))
        for name in v:
            d = params[name]
            fout.write(dedent(
                """
                Parameter(
                    "{d[name]}",
                    "{d[format]}",
                ),
                """.format(d=d)))
        fout.write(']\n\n')
