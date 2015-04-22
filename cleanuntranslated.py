import xml.etree.ElementTree as ET
import codecs
from copy import deepcopy
import re

ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')

xliff = ET.parse('sample/MAR_doc_user_CZ.xlf')
xliff_root = xliff.getroot()

NAMESPACE = '{urn:oasis:names:tc:xliff:document:1.2}'


def remove_segment_tag(segment):
    segment = re.sub(r'<seg-source.+?>', '', segment)
    return re.sub(r'</seg-source>', '', segment)

print(xliff_root)
for segment in xliff_root.iter(tag='{}trans-unit'.format(NAMESPACE)):
    source = segment[0]
    target = segment[1]
    if target.attrib == {}:
        target.clear()
        segsource = deepcopy(source)
        segsource.tag = 'seg-source'
        segment.append(segsource)
        as_string = ET.tostring(segsource, encoding='unicode')
        just_segment = remove_segment_tag(as_string)
        subsegments = just_segment.split('.')
        print(len(subsegments))

print(xliff_root)

newtree = ET.ElementTree(xliff_root)
with codecs.open('test_cleaned.xlf', 'w', encoding='UTF-8') as result:
    newtree.write(result, encoding='unicode',  xml_declaration=True)

source_to_segment = '''<ph id="20">&lt;MadCap:variable name="MyVariables.AA"/&gt;</ph>
 for Outlook<bpt id="0">&lt;sup&gt;</bpt>®<ept id="0">
 &lt;/sup&gt;</ept> 2003.'''
subsegments = source_to_segment.split('.')
print(subsegments)

