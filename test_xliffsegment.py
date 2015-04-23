import unittest
from lxml import etree as ET
from cleanuntranslated import TransUnit


class TestTransUnit(unittest.TestCase):

    def setUp(self):
        self.not_empty_state = ET.fromstring('''<trans-unit id="tu-3" resname="p">
          <source>Source</source>
          <target state="signed-off">Sample target</target>
          </trans-unit>''')
        self.empty_state = ET.fromstring('''<trans-unit id="tu-3" resname="p">
          <source>Source</source>
          <target state="">Sample target</target>
          </trans-unit>''')
        self.no_state = ET.fromstring('''<trans-unit id="tu-3" resname="p">
          <source>Source</source>
          <target>Sample target</target>
          </trans-unit>''')
        self.unit_with_namespace = self._create_unit_with_namespace()

    def _create_unit_with_namespace(self):
        NAMESPACE = '{urn:oasis:names:tc:xliff:document:1.2}'
        unit = ET.Element(
            "{}trans_unit".format(NAMESPACE),
            id='1',
            resname='abc')

        ET.SubElement(unit, "{}source".format(NAMESPACE))
        ET.SubElement(unit, "{}target".format(NAMESPACE))

        return unit

    def tearDown(self):
        pass

    def test_trans_unit_created_from_string(self):

        trans_unit = TransUnit.create(self.not_empty_state)

        self.assertNotEqual(trans_unit, None)

    def test_trans_unit_created_has_id(self):

        trans_unit = TransUnit.create(self.not_empty_state)

        self.assertEqual(trans_unit.id, "tu-3")

    def test_trans_unit_with_state(self):

        trans_unit = TransUnit.create(self.not_empty_state)

        self.assertEqual(trans_unit.state, "signed-off")

    def test_trans_unit_with_empty_state(self):

        trans_unit = TransUnit.create(self.empty_state)

        self.assertEqual(trans_unit.state, "")

    def test_trans_unit_with_no_state(self):

        trans_unit = TransUnit.create(self.no_state)

        self.assertEqual(trans_unit.state, "")

    def test_trans_unit_with_namespace_works(self):

        trans_unit = TransUnit.create(self.unit_with_namespace)

        self.assertNotEqual(trans_unit, None)

    def test_has_any_state_true_if_exist(self):

        trans_unit = TransUnit.create(self.not_empty_state)

        self.assertEqual(
            trans_unit.has_any_state(["signed-off"]),
            True)

    def test_has_any_state_false_if_not_exist(self):

        trans_unit = TransUnit.create(self.not_empty_state)

        self.assertEqual(
            trans_unit.has_any_state(["not-translated"]),
            False)


if __name__ == '__main__':
    unittest.main()
