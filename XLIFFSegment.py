import xml.etree.ElementTree as ET

class XLIFFSegment(object):
	"""container for XLIFF segment"""
	def __init__(self, arg):
		self.origin = ET.fromstring(arg)
		self.attr = self.origin.attrib

		if self.origin.find('source').text:
			self.source = self.origin.find('source').text
		else:
			self.source = ''
		if self.origin.find('target').text:
			self.target = self.origin.find('target').text
		else:
			self.target = ''
	def source(self)
		return self.source
	