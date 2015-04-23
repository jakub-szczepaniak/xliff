#from lxml import etree as ET


class TransUnit(object):

    "Container for XLIFF trans-unit element"

    def __init__(self, argument):
        self.origin_unit = argument
        self.attributes = argument.attrib
        self.id = ''
        self.ns = ''
        self.state = ''

    @staticmethod
    def create(xml_tu):

        tunit = TransUnit(xml_tu)

        tunit.id = tunit.attributes['id']
        tunit.ns = tunit.__read_ns()
        tunit.state = tunit.__get_state_from_target()
        return tunit

    def __get_state_from_target(self):

        target = self.origin_unit.find('{}target'.format(self.ns))
        if "state" in target.attrib.keys():
            return target.attrib['state']
        else:
            return ''

    def __has_ns(self):
        return '{' in self.origin_unit.tag

    def __read_ns(self):
        if self.__has_ns():
            ns, tag = self.origin_unit.tag.split('}')
            ns = ns + '}'
            return ns
        else:
            return ''

    def has_any_state(self, list_of_states):

        return self.state in list_of_states
