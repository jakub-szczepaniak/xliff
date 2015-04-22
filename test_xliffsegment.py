import unittest
from XLIFFSegment import XLIFFSegment


class TestXLIFFSegment(unittest.TestCase):

    def setUp(self):
        self.xml_string = '''<trans-unit id="tu-3" resname="p">
          <source>Source</source>
          <target /><seg-source>The <ph id="31">&lt;MadCap:variable
           name="MyVariables.AA"/&gt;</ph> installs an additional
            toolbar in Microsoft Outlook<bpt id="0">&lt;sup&gt;</bpt>®
            <ept id="0">&lt;/sup&gt;</ept> 2003.</seg-source>
          </trans-unit>'''
        self.empty_segment = '''<trans-unit id="tu-3" resname="p">
        <source></source><target /></trans-unit>'''

    def tearDown(self):
        pass

    def test_source_text_without_tags(self):
        trans_unit = XLIFFSegment(self.xml_string)
        self.assertEqual(trans_unit.source, 'Source')

    def test_text_is_empty(self):
        trans_unit = XLIFFSegment(self.empty_segment)

        self.assertEqual(trans_unit.target, '')
        self.assertEqual(trans_unit.source, '')

    def test_trans_unit_attribs(self):
        trans_unit = XLIFFSegment(self.empty_segment)

        self.assertEqual(trans_unit.attr['id'], "tu-3")

if __name__ == '__main__':
    unittest.main()
