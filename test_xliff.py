import unittest
from unittest.mock import patch
from lxml import etree as ET
from cleanuntranslated import XLIFFDict


class TestXliffDict(unittest.TestCase):

    def setUp(self):
        self.from_string = r'''<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2"
 xmlns:gs4tr="http://www.gs4tr.org/schema/xliff-ext">
  <file datatype="x-CatalystTTK"
  original="C:\Users\Something_de.ttk"
  source-language="en-US"
  target-language="de"
  date="2015-03-04T12:56:08Z"
  product-name="Alchemy Catalyst"
  product-version="Alchemy Catalyst 11.0"
  build-num="11.1.132.0" >
    <body>
      <group id="1-1032"
      resname="\resource.resx" restype="x-Form">
        <trans-unit id="tu-1" resname="$this"  maxwidth="0">
          <source></source>
          <target></target>
        </trans-unit>
        <trans-unit id="tu-2" resname="xrLabel37.Text"  maxwidth="0">
          <source>Sent</source>
          <target state="needs-review-l10n"
          state-qualifier="exact-match">Gesendet</target>
        </trans-unit>
        <trans-unit id="tu-3" resname="xrLabel38.Text"  maxwidth="0">
          <source>Received</source>
          <target state="needs-review-l10n"
          state-qualifier="exact-match">Empfangen</target>
        </trans-unit>
        </group>
        </body>
        </file>
        </xliff>'''

    def tearDown(self):
        pass

    def test_created_from_root_works(self):
        xlf_element = ET.XML(self.from_string)

        xlif_dict = XLIFFDict.create(xlf_element)

        self.assertNotEqual(xlif_dict, None)

    @patch('cleanuntranslated.ET')
    def test_loaded_from_file_works(self, mock_ET):

        mock_ET.parse.return_value = self.from_string

        xlif_dict = XLIFFDict.create("filename")
        self.assertNotEqual(xlif_dict, None)


if __name__ == '__main__':
    unittest.main()
