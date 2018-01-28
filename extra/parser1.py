"""
Parse the definition document:

    http://genome.ucsc.edu/goldenPath/help/trackDb/trackDbLibrary.shtml

into various useful forms.  The end goal is to automatically construct
validation (in trackhub.constants), but this is a long-term goal. For now, we
just want to make sure all parameters are represented.


In addition, this script converts the html and various div tag info into ReST
format, for eventual inclusion in the trackhub docs.


The definition document contains "settings blurbs" in <div> tags with
a specific format.  Here's a cheat-sheet:


    <div class="longLabel">
    -----------------------
    - class name usually reflects the param name
    - "*_example" will be ignored for now

    <span class="types all"</span>
    ------------------------------
    - span.attrs['class'][1:] are the track types the setting is valid for

    <div class="format">
    --------------------
        - settings DIVs must contain a sub-div with class "format"

        <code>longLabel</code></div>
        ----------------------------
            - the actual name of the setting is here, as the only content of
              the "format" div -- and is wrapped in code tags

    multiple <p> tags
    -----------------
        - content and description (converted to ReST)

"""
import subprocess
from bs4 import BeautifulSoup
import re
from trackhub import constants


def format_handler(s):
    """
    Convert a format string into a set() to [eventually] be used for validation

    TODO: still needs lots of work
    """
    int_range = re.compile('\d+-\d+')

    s = s.replace('>', '').replace('<', '')

    defined_options = s.split('/')

    option_set = set()

    remainder = []

    # detect int ranges
    for op in defined_options:
        m = int_range.search(op)
        if m:
            substr = op[m.start():m.end()]
            start, stop = substr.split('-')
            option_set.update(range(int(start), int(stop) + 1))
            remaining = s.replace(substr, '').replace('<', '').replace('>', '')
        else:
            remainder.append(op)
    option_set.update(remainder)

    return option_set


def html2rst(html):
    """
    Requires pandoc (sudo apt-get install pandoc); converts HTML string to ReST
    string
    """
    # thanks to
    # http://johnpaulett.com/2009/10/15/ \
    #        html-to-restructured-text-in-python-using-pandoc/
    p = subprocess.Popen(
        [
            'pandoc',
            '--from=html',
            '--to=rst',
            '--strict',
        ],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate(html)[0]


soup = BeautifulSoup(open('trackDbLibrary.shtml').read())

# Only consider settings for these track types
hub_types = set(['bam', 'bigBed', 'bigWig', 'vcfTabix', 'all'])
supported_params = {}
for div in soup.find_all('div'):

    # If we don't have this span class, it's not a settings blurb
    if not div.find_all('span', class_='types'):
        continue

    tag = div['class'][0]

    # example divs aren't useful for now
    if '_example' in tag:
        continue

    # As per the comments in the definition document, settings blurb divs are
    # required to have a sub-div of class "format"
    assert div.div['class'][0] == 'format'

    # Only hub-supported settings for now
    if 'NOT FOR HUBS' in div.text:
        if 'Not yet supported by bigBeds' not in div.text:
            continue

    types = div.span.attrs['class'][1:]

    # Skip if the setting doesn't apply to track hub types
    if len(set(types).intersection(hub_types)) == 0:
        continue

    # TODO: how to handle "sub-settings"?  E.g., url; bed; scoreFilter, etc
    definition = div.div.text.strip().replace('\n', '    ')

    content = html2rst(str(div))

    block = []
    block.append(tag)
    block.append('=' * len(tag))
    block.append(':definition: ``%s``' % definition)
    block.append('')
    block.append(':used for: ``%s``' % types)
    block.append('')

    items = definition.split()
    key = items[0]
    if len(items) == 1:
        format_string = ""
    else:
        format_string = items[1]

    block.append(":options: ``%s``" % format_handler(format_string))
    block.append('')
    block.append(content)

    supported_params[key] = '\n'.join(block)


existing_params = set(
    constants.track_fields.keys()
    + constants.track_typespecific_fields.keys()
    + constants.view_track_fields.keys()
    + constants.composite_track_fields.keys()
    + constants.aggregate_track_fields.keys()
)

print("Add these params to trackhub.constants:")
print("---------------------------------------")
for k, v in supported_params.items():
    if k not in existing_params:
        print(v)
