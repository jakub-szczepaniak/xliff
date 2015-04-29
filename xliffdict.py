from lxml import etree as ET
from transunit import TransUnit
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
        elif isinstance(document, ET._Element):
            new_xliff.document = document
        else:
            raise Exception("XLIFF file not correct!")

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
