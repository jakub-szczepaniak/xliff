from lxml import etree as ET
from copy import deepcopy
NAMESPACE = '{urn:oasis:names:tc:xliff:document:1.2}'


def read_xliff_file(filename):

    xliff = ET.parse(filename)
    xliff_root = xliff.getroot()
    return xliff_root


def new_filename(filename, suffix):
    broken = filename.split('.')
    broken.insert(-1, suffix)
    return ".".join(broken)


def segmenthas_any_states(element, states):
    
    return any(state in element.attrib.values() for state in states) or 'state' not in element.attrib.keys()


def split_xliff(filename):

    source_document = read_xliff_file(filename)

    for trans_unit in source_document.iter(tag='{}trans-unit'.format(NAMESPACE)):
        print(trans_unit)


def clean_empty_state(filename):

    source_document = read_xliff_file(filename)
    review_document = deepcopy(source_document)
    for target_segment in source_document.iter(tag='{}target'.format(NAMESPACE)):
        if segmenthas_any_states(target_segment, [None, ""]):
            target_segment.clear()

    for target_segment in review_document.iter(tag='{}target'.format(NAMESPACE)):
        if not segmenthas_any_states(target_segment, ['needs-review-l10n']):
            target_segment.getparent().clear()

    for_review_tree = ET.ElementTree(review_document)
    for_review_tree.write(
        new_filename(filename, 'for_review'),
        encoding='UTF-16',
        xml_declaration=True)
    newtree = ET.ElementTree(source_document)
    newtree.write(new_filename(filename, 'clean'),
                  encoding='UTF-16',
                  xml_declaration=True)


def main():
    clean_empty_state('./sample/fmserver_es_GUI.ttk.xlf')

if __name__ == "__main__":
    main()
