class TransUnit(object):

    "Container for XLIFF trans-unit element"

    def __init__(self, argument):
        self.origin_unit = argument
        self.attributes = argument.attrib
        self.id = ''
        self.ns = ''
        self.state = ''
        self._source = ''
        self._target = ''

    @staticmethod
    def create(xml_tu):

        tunit = TransUnit(xml_tu)

        tunit.id = tunit.attributes['id']
        tunit.ns = tunit._read_ns()
        tunit.state = tunit._get_state_from_target()
        tunit._source = tunit.origin_unit.find('{}source'.format(tunit.ns))
        tunit._target = tunit.origin_unit.find('{}target'.format(tunit.ns))
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
        return self._source.text

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def target(self):
        return self._target.text

    @target.setter
    def target(self, value):
        self._target = value
