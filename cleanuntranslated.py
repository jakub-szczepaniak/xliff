from lxml import etree as ET


def read_xliff_file(filename):

    xliff = ET.parse(filename)
    xliff_root = xliff.getroot()
    return xliff_root


def segmenthas_states(element, states):
    return any(state in element.attrib.values() for state in states) or 'state' not in element.attrib.keys()


def clean_empty_state(filename):
    NAMESPACE = '{urn:oasis:names:tc:xliff:document:1.2}'
    source_document = read_xliff_file(filename)
    for target_segment in source_document.iter(tag='{}target'.format(NAMESPACE)):
        if segmenthas_states(target_segment, [None, ""]):
            target_segment.clear()

    newtree = ET.ElementTree(source_document)
    newtree.write("{}.clean".format(filename),
                  encoding='UTF-16',
                  xml_declaration=True)


def main():
    clean_empty_state('./sample/fmserver_es_2003.ttk.xlf')
    
if __name__ == "__main__":
    main()
