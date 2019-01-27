import re
import bs4
import requests


def make_soup():
    """
    Initial parsing of HTML into bs4 soup
    """
    # It's a pretty complex, auto-generated HTML file. Turns out
    # BeautifulSoup's html.parser, lxml, and xml don't completely parse.
    # Initial workarounds chopped up the file and parsed individually, but the
    # most lenient html5lib parse seems to do the trick.
    response = requests.get(
        'https://genome.ucsc.edu/goldenPath/help/trackDb/trackDbHub.html')
    soup = bs4.BeautifulSoup(response.text, 'html5lib')
    return soup


def get_supported_types(soup):
    """
    Extract supported types

    There is a table that stores the supported filetypes. It contains links of
    the form <a href="#filetype">, so we search for the BAM one, the find the
    parent (a <li>) and then it's parent (the <ul>). That will be our list of
    supported filetypes::

        <ol>
            <ul>
                <li><a href="#bam"> <---- (FIND THIS)
                <li><a href="#bigBed">
                ...
            </ul>
            <li>
            <ul>
                <li><a href="#superTrack">...
            </ul>
            <li> (don't care about this one since not in a ul)
    """
    abam = soup.find('a', href=re.compile('#bam'))
    ol = abam.parent.parent.parent.parent
    supported_types = []
    for ul in ol.find_all('ul'):
        for a in ul.find_all('a'):
            ref = a['href'].replace('#', '')

            # some have text like "#bigMaf_-_Multiple_Alignments", so split on
            # the '_'
            ref = ref.split('_')[0]
            supported_types.append(ref)

    # multiWig is not included in this table, but it's considered a type in the
    # divs.
    supported_types.append('multiWig')

    # If a setting pertains to all types, they are not all listed, rather, the
    # "all" type is specified.
    supported_types.append('all')

    return supported_types


def support_level(soup):
    # Another set of tables stores the support level
    settings_tables = soup.find_all('table', class_='settingsTable')
    support_levels = {}
    for t in settings_tables:
        for td in t.find_all('td'):
            if not td.has_attr('class'):
                continue
            key = td['class']
            assert len(key) == 1
            key = key[0]
            code = td.find('code')
            if not code or not code.has_attr('class'):
                continue
            support = code['class']
            support_levels[key] = support
    return support_levels


def parse_divs(soup, supported_types):
    """
    Parameters
    ----------
    soup : parsed BeautifulSoup object

    supported_types : list
        list of supported types, as extracted from get_supported_types()

    Details
    -------

    ANATOMY OF A DIV...
    These divs are found under the <div class="library">, and you can read the
    comments in the original HTML for more details.

    ::

        <!--
        The div's class is effectively a unique name across the HTML, so this
        is what we'll use for a key in the dictionaries we're creating. It will
        be stored in the id_ variable.
        -->
        <div class="bamGrayMode">

          <!--
          The span class starts with "types" and includes the track types the
          setting is relevant to. This will be stored in the "types" variable.
          -->
          <span class="types bam"></span>

          <!--
          The format class contains <code> chunks. Sometimes, as shown here,
          there are multiple options or sub-options.
          -->
          <div class="format">
              <code>bamGrayMode &lt;aliQual/baseQual/unpaired&gt;</code><br/>
              <code>aliQualRange &lt;min:max&gt;</code><br/>
              <code>baseQualRange &lt;min:max&gt;</code>
          </div>

          DESCRIPTION GOES HERE...may have any tags within here.

          SOMETIMES AN EXAMPLE IN <pre> TAGS:
          <p>
              <b>
                  Example:
              </b>
          </p>
          <pre>
              showNames off
          </pre>
        </div>
    """

    def keep(tag):
        """
        Track settings have a <span class="types..."> indicating which type
        they're from. However some are examples that luckily are tagged as such
        (e.g., bed_example).
        """
        if tag.name != 'span':
            return
        if tag.parent.has_attr('class'):
            for c in tag.parent['class']:
                if 'example' in c:
                    return

        if tag.has_attr('class'):
            if 'types' in tag['class']:
                if 'customTracks' not in tag['class']:
                    return True

    d = soup.find_all(keep)

    specs = {}
    debug = {}

    for i in d:

        div = i.parent
        _id = div.attrs['class']
        assert len(_id) == 1
        _id = _id[0]

        # For easier debugging, all divs inspected will go to the debug dict.
        # Various filters may exclude it from being in the specs dictionary
        # though.
        debug[_id] = div

        types = set(i.attrs['class']).intersection(supported_types)

        if len(types.intersection(supported_types)) == 0:
            continue

        types = list(types)
        fmt = div.find_all(name='div', attrs='format')
        assert len(fmt) == 1
        fmt = fmt[0]

        required_p = div.find_all(name='p', attrs='isRequired')
        required = False
        if required_p:
            for i in required_p:
                if 'yes' in i.text.lower() or 'for hubs' in i.text.lower():
                    required = True

        # Some, like bamGrayMode, have several "sub names" like bamGrayMode,
        # aliQualRnage, baseQualRange. Handle those here.
        formats = fmt.find_all('code')
        if formats is None:
            continue
        else:
            formats = [n.text for n in formats]

        # Most non-hub-relevant settings are filtered out py the supported
        # types filter, but some sneak through (e.g. several only used by
        # ENCODE).
        no_hub = div.find_all('p', string=re.compile('NOT FOR HUBS'))
        if no_hub:
            continue

        example = div.find('pre')
        if example is not None:
            example = str(example.string)

        desc = div.find_all('p')
        if desc is not None:
            desc = ' '.join([' '.join(''.join(i.strings).split()) for i in
                             desc])
        if _id in specs:
            raise ValueError("duplicate value for {}".format(_id))

        # We are only concerned with settings, not types. Types (bigBed, bam,
        # etc) have "type" in their format.
        if any([i.split()[0] == 'type' for i in formats]):
            continue

        # Special cases
        #
        if _id in ['view', 'subGroupN', 'parent_view']:
            continue

        spec = {
            'format': formats,
            'types': sorted(types),
            'required': required,
            'example': example,
            'desc': desc,
        }
        specs[_id] = spec

        # In some cases there are more than one format. In those cases,
        # consider a new _id based on the first word of the sub-option. Note
        # that we should add the divs to the debug dict as well.
        if len(formats) > 1:
            for format_ in formats:
                new_id = format_.split()[0]
                specs[new_id] = spec
                debug[new_id] = spec

    return specs, debug


def print_parsed(specs):
    """
    Given the parsed specs, print them in a form that can be diffed with
    parsed_params.py

    Parameters
    ----------
    specs : dict
        Returned dictionary from parse_divs()
    """
    observed_types = set()
    for i in specs.values():
        observed_types.update(i['types'])
    observed_types = sorted(observed_types)

    s = ['# Observed types from the parsed document']
    s.append('TRACKTYPES = [')
    for i in observed_types:
        s.append("    '{}',".format(i))
    s.append(']')
    print('\n'.join(s) + '\n')

    data_types = specs['bigDataUrl']['types']

    s = ['# Tracks for which the definition specifies bigDataUrl']
    s.append('DATA_TRACKTYPES = [')
    for i in data_types:
        s.append("    '{}',".format(i))
    s.append(']')
    print('\n'.join(s) + '\n')
    print('param_defs = [')
    print()
    for k, v in sorted(specs.items()):
        print(
            (
    '''
    Param(
        name="{k}",
        fmt={v[format]},
        types={v[types]},
        required={v[required]},
        validator=str),'''.format(**locals())
            )
        )


if __name__ == "__main__":
    soup = make_soup()
    supported_types = get_supported_types(soup)
    specs, debug = parse_divs(soup, supported_types)
    print_parsed(specs)
