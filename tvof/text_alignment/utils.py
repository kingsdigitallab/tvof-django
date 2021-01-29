from text_viewer.kiln_requester import CachedRequesterKiln
import re


def read_alignment_html():
    '''returns the alignment html file as a single string'''
    kiln = CachedRequesterKiln()
    url = '/backend/preprocess/alists/TVOF_para_alignment.xml'
    ret = kiln.request(url)
    if not ret:
        raise Exception('Could not fetch alignment XML from Kiln')

    return ret


def read_alignment_ms_names(site_key=None):
    '''returns a list of MSS from the alignment html
    [
        [NORMALISED_NAME, SLUG, VISIBLE]
    ]
    '''

    visible_slugs = read_alignment_visible_ms_slugs(site_key)

    normalised_names = get_normalised_ms_names(
        re.findall(
            r'<seg type="ms_name">\s*([^<]+)\s*</seg>',
            read_alignment_html()
        )
    ).values()

    return [
        [
            name,
            get_key_from_name(name),
            get_key_from_name(name) in visible_slugs
        ]
        for name in sorted(normalised_names)
    ]


def read_alignment_visible_ms_slugs(site_key=None):
    '''Returns the list of MSS slugs that a user can see and select
    on the alignment visualisation settings screen.
    Empty list means ALL.

    site_key: see settings.DATA_RELEASE['sites']
    default is the current instance
    '''
    from tvof.data_release.utils import read_settings_file
    return read_settings_file('alignment_filters', [], site_key)


def write_alignment_visible_ms_slugs(ms_slugs, site_key=None):
    from tvof.data_release.utils import write_settings_file
    write_settings_file('alignment_filters', ms_slugs, site_key)


def get_normalised_ms_names(ms_names):
    '''
    Returns all unique MS names found in ms_names (can contain duplicates)
    Returns dictionary fo the form {UNIQUE_INPUT_NAME -> NORMALISED_NAME}
    e.g. {Dijon -> Dijon 262, Dijon262 -> Dijon 262, 'Fr20125': 'Fr 20125'}
    slug is produced from the NORMALISED NAME (see get_key_from_name())

    ms_names = a raw list of ms names as found in alignment file
    can contain duplicates
    '''

    # get all unique names
    from collections import Counter
    ms_names = Counter(ms_names)

    # now normalise the names
    # Fr15455 | Fr 15455, Marciana_fr_Z_II | Marciana Fr Z Ii
    for name in ms_names:
        normalised = name.replace(
            '-',
            ' ').replace(
            '_',
            ' ').lower().strip()
        normalised = re.sub(r'(?i)([a-z])(\d)', r'\1 \2', normalised)
        normalised = normalised.title()
        ms_names[name] = normalised

    # merge
    # e.g. Dijon -> Dijon 562
    for name, normalised in list(ms_names.items()):
        if ' ' not in normalised:
            candidates = [
                v
                for v
                in set(ms_names.values())
                if v.startswith(normalised + ' ')
            ]
            c = len(candidates)
            if c == 1:
                ms_names[name] = candidates[0]
            elif c > 2:
                print('WARNING: ambiguous MS name: %s (%s ?)' %
                      (name, ', '.join(candidates)))
            elif c == 0:
                print('INFO: MS name without number: %s' % name)

    # print '\n'.join(['%s | %s' % (k, v) for k, v in ms_names.items()])

    return ms_names


def get_key_from_name(name):
    import re
    return re.sub(r'[^\w_]+', r'-', name.lower()).strip()


def get_name_from_key(akey):
    import re
    return re.sub(r'[_]', r' ', akey.title()).strip()
