class TransUnit(object):

    "Container for XLIFF trans-unit element"

    def __init__(self, argument):
        self.origin_unit = argument
        self.attributes = argument.attrib
        self.id = ''
        self.ns = ''
        self.state = ''
        self._source = ''

    @staticmethod
    def create(xml_tu):

        tunit = TransUnit(xml_tu)

        tunit.id = tunit.attributes['id']
        tunit.ns = tunit._read_ns()
        tunit.state = tunit._get_state_from_target()

        return tunit

    def _read_ns(self):
        if self._has_ns():
            ns, tag = self.origin_unit.tag.split('}')
            ns = ns + '}'
            return ns
        else:
            return ''

    def _has_ns(self):
        return '{' in self.origin_unit.tag

    def _get_state_from_target(self):

        target = self.origin_unit.find('{}target'.format(self.ns))
        if "state" in target.attrib.keys():
            return target.attrib['state']
        else:
            return ''

    def has_any_state(self, list_of_states):

        return self.state in list_of_states

    @property
    def source(self):

        self._source = self.origin_unit.find('{}source'.format(self.ns))
        return self._source.text

    @source.setter
    def source(self, valsource):
        self._source = valsource
