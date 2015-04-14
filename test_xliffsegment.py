import unittest
from XLIFFSegment import XLIFFSegment
import codecs


class TestXLIFFSegment(unittest.TestCase):
	def setUp(self):
		self.xml_string = '''<trans-unit id="tu-1" resname="0" >
          <source>Source</source>
          <target>Target</target>
        </trans-unit>'''

	def tearDown(self):
		pass
	def test_source_text(self):
		trans_unit = XLIFFSegment(self.xml_string)
		self.assertEqual(trans_unit.source, 'Source')

    
if __name__ == '__main__':
	unittest.main()