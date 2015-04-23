from lxml import etree as ET
from transunit import TransUnit
import fnmatch
import os
NAMESPACE = '{urn:oasis:names:tc:xliff:document:1.2}'


class XLIFFDict:

    "Container for xliff document"

    def __init__(self):
        self.segments = dict()
        self.header = dict()
        self.document = None

    @staticmethod
    def create(document):

        new_xliff = XLIFFDict()
        new_xliff.document = document

        if isinstance(document, str):
            new_xliff.document = ET.parse(document)
        elif isinstance(document, ET._ElementTree):
            new_xliff.document = document.getroot()
        else:
            new_xliff.document = document

        header = new_xliff.document.find('{}file'.format(NAMESPACE))

        if header is None:
            raise Exception("XLIFF file not correct!")
        else:
            new_xliff.header = header.attrib

        for unit in new_xliff.document.iter('{}trans-unit'.format(NAMESPACE)):
            tunit = TransUnit.create(unit)
            new_xliff.segments[tunit.id] = tunit

        return new_xliff

    def serialize(self, new_filename):

        new_document = ET.ElementTree(self.document)
        new_document.write(
            new_filename,
            encoding='UTF-16',
            xml_declaration=True)


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


def clean_empty_state_from_xliff(filename, targetFolder):

    source_document = read_xliff_file(filename)

    for target_segment in source_document.iter(
            tag='{}target'.format(NAMESPACE)):
        if segmenthas_any_states(target_segment, [None, ""]):
            target_segment.clear()

    newtree = ET.ElementTree(source_document)
    newtree.write(os.path.join(targetFolder, filename),
                  encoding='UTF-16',
                  xml_declaration=True)


def main():
    targetFolder = 'targetSegmentsRemoved'
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)
    for filename in os.listdir():
        if fnmatch.fnmatch(filename, "*.xlf"):
            clean_empty_state_from_xliff(filename, targetFolder)
            print("Processed :" + filename)
    input("Press Enter to continue")

if __name__ == "__main__":
    main()
