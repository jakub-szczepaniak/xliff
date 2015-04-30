import unittest
from unittest.mock import patch
from unittest.mock import Mock
from lxml import etree as ET
from xliffdict import XLIFFDict


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

        self.xliff = ET.XML(self.from_string)

        self.wrong_xml = ET.XML(r'''<abc></abc>''')

    def tearDown(self):
        pass

    def test_created_from_root_works(self):
        xlf_element = ET.XML(self.from_string)

        xlif_dict = XLIFFDict.create(xlf_element)

        self.assertNotEqual(xlif_dict, None)

    @patch('xliffdict.ET')
    def test_it_loads_xliff_from_file(self, mock_ET):

        mock_ET.parse.return_value = self.xliff

        XLIFFDict.create("filename")
        self.assertTrue(mock_ET.parse.called, True)

    def test_internal_dict_is_not_empty(self):

        new_xlf = XLIFFDict.create(self.xliff)

        self.assertEqual(len(new_xlf.segments.values()), 3)

    def test_header_is_not_empty(self):

        new_xlf = XLIFFDict.create(self.xliff)

        self.assertEqual(len(new_xlf.header.values()), 8)

    def test_raises_exception_for_wrong_xml(self):

        with self.assertRaises(Exception) as exc:
            XLIFFDict.create(self.wrong_xml)
        self.assertEqual(exc.exception.args[0], 'XLIFF file not correct!')

    def test_raises_exception_for_wrong_object(self):
        with self.assertRaises(Exception) as exc:
            XLIFFDict.create(dict())
        self.assertEqual(exc.exception.args[0], 'XLIFF file not correct!')

    @unittest.skip("to be finished")
    def test_saves_file_to_disk(self):
        mock_ET = Mock(spec='xliffdict.ET.ElementTree')
        mock_ET.parse.return_value = self.xliff

        new_xlf = XLIFFDict.create(self.from_string)
        new_xlf.serialize('filename')

        mock_ET.assert_called_with('filename')



if __name__ == '__main__':
    unittest.main()
