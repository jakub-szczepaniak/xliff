from lxml import etree as ET
from copy import deepcopy
NAMESPACE = '{urn:oasis:names:tc:xliff:document:1.2}'


class TransUnit:

    "Container for XLIFF trans-unit element"

    def __init__(self, argument):
        self.origin_unit = argument
        self.attributes = argument.attrib
        self.id = ''
        self.state = ''

    @staticmethod
    def create(xml_tu):

        tunit = TransUnit(xml_tu)
        tunit.id = tunit.attributes['id']

        tunit.state = tunit.__get_state_from_target()
        return tunit

    def __get_state_from_target(self):

        target = self.origin_unit.find('{}target'.format(NAMESPACE))
        if "state" in target.attrib.keys():
            return target.attrib['state']
        else:
            return ''

    def has_any_state(self, list_of_states):

        return self.state in list_of_states


class XLIFFDict:

    def __init__(self, argument):
        self.dict = dict()

    @staticmethod
    def create_from_file(filename):
        new_dict = dict()
        xliff = ET.parse(filename)
        xliff_root = xliff.getroot()

        for unit in xliff_root.iter('{}trans-unit'.format(NAMESPACE)):
            tunit = TransUnit.create(unit)
            new_dict[tunit.id] = tunit
        return new_dict


def read_xliff_file(filename):

    xliff = ET.parse(filename)
    xliff_root = xliff.getroot()
    return xliff_root


def new_filename(filename, suffix):
    broken = filename.split('.')
    broken.insert(-1, suffix)
    return ".".join(broken)


def segmenthas_any_states(element, states):

    return any(
        state in element.attrib.values()
        for state in states) or 'state' not in element.attrib.keys()


def split_xliff(filename):
    pass


def read_dict_of_units(xliff_root):
    dict_of_units = dict()
    for unit in xliff_root.iter(tag='{}trans-unit'.format(NAMESPACE)):
        new_tu = TransUnit.create(unit)
        if new_tu.has_any_state(['needs-review-l10n']):
            dict_of_units[new_tu.id] = new_tu
    return dict_of_units


def clean_empty_state_from_xliff(filename):

    source_document = read_xliff_file(filename)
    review_document = deepcopy(source_document)

    review_dict = read_dict_of_units(review_document)
    print(review_dict)

    for target_segment in source_document.iter(
            tag='{}target'.format(NAMESPACE)):
        if segmenthas_any_states(target_segment, [None, ""]):
            target_segment.clear()

    for target_segment in review_document.iter(
            tag='{}target'.format(NAMESPACE)):
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
    clean_empty_state_from_xliff('./sample/fmserver_es_GUI.ttk.xlf')

if __name__ == "__main__":
    main()
