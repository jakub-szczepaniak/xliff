from lxml import etree as ET
from xliffdict import XLIFFDict
import fnmatch
import os
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
