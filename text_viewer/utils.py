

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
        print(parent, leaf, elements)
        for i, element in enumerate(parent):
            if element in elements:
                yield {'parent': parent, 'el': element, 'index': i}


if 0:
    xml_str = '''<r>
    <gp>
      <p>
        <e>e1.1</e>
        <e class="c1">e1.2</e>
      </p>
      <p>
        <e>e2.1</e>
        <e>e2.2</e>
      </p>
    </gp>
    </r>
    '''

    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_str)
    for e in findall_from_xml(root, './/e[@class="c1"]'):
        print(e['el'].text)
