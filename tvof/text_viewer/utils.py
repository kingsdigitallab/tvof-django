import xml.etree.ElementTree as ET
import re


# def get_text_viewer_filters(client='textviewer'):
#     ret = None
#
#     from ..data_release.utils import get_abs_data_path
#     path = get_abs_data_path('text_viewer_filters')
#
#     if os.path.exists(path):
#         with open(path, 'rt') as fh:
#             content = fh.read()
#         filters = json.loads(content)
#         if filters:
#             ret = filters[client]
#
#     return ret


def findall_in_etree(tree, xpath):
    '''
    Similar to ElementTree.findall(xpath) but returns parents as well.

    Yields {
        'el': <element>,
        'parent': <parent element>,
        'index': index of <element> under <parent>
    }

    xpath: a simple xpath e.g. './/span[@class="c1"]'
    '''
    leaf = xpath.split('/')[-1]
    for parent in tree.findall('{}/..'.format(xpath)):
        elements = parent.findall(leaf)
        # print(parent, leaf, elements)
        for i, element in enumerate(parent):
            if element in elements:
                yield {'parent': parent, 'el': element, 'index': i}


def remove_xml_elements(xml, xpath):
    '''Remove all the elements matching xpath (and all their content)'''
    ret = 0
    xpath_from_parent = re.sub(r'.*/', '', xpath)

    for parent in xml.findall(xpath + '/..'):
        for item in parent.findall(xpath_from_parent)[::-1]:
            ret += 1
            if item.tail:
                last = None
                found = 0
                for kid in list(parent):
                    if item == kid:
                        if last is None:
                            parent.text = (parent.text or '') + item.tail
                        else:
                            last.tail = (last.tail or '') + item.tail
                        found = 1
                        break
                    last = kid
                assert found
            parent.remove(item)
    return ret


def get_unicode_from_xml(xmltree, encoding='utf-8', text_only=False,
                         remove_root=False):
    '''
    Returns the xmltree (EL subtree) as a unicode string.
    If text_only == True => element text only, no tags
    '''
    # if text_only = True => strip all XML tags
    # EXCLUDE the TAIL
    if text_only:
        return get_xml_element_text(xmltree)
    else:
        if hasattr(xmltree, 'getroot'):
            xmltree = xmltree.getroot()
        ret = ET.tostring(xmltree, encoding=encoding).decode()
        if xmltree.tail is not None and ret[0] == '<':
            # remove the tail
            import re
            ret = re.sub(r'[^>]+$', '', ret)

        if remove_root:
            ret = ret.replace('<root>', '').replace('</root>', '')

        return ret


def get_xml_element_text(element):
    # returns all the text within element and its descendants
    # WITHOUT the TAIL.
    #
    # element is etree Element object
    #
    # '<r>t0<e1>t1<e2>t2</e2>t3</e1>t4</r>'
    # e = (xml.findall(el))[0]
    # e.text => t1
    # e.tail => t4 (! part of e1)
    # get_xml_element_text(element) => 't1t2t3'

    return ''.join(element.itertext())


def get_xml_from_unicode(s):
    return ET.fromstring(s)
