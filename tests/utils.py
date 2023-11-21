from django.test import SimpleTestCase
from lxml import etree


class ExtendedSimpleTestCase(SimpleTestCase):
    def assertXMLIEqual(self, xml1, xml2):
        # We need to format both xml files the same way...
        # otherwise the self.assertXMLEqual function, which is based on str compare will fail
        parser = etree.XMLParser(
            remove_blank_text=True,
            remove_comments=True,
            ns_clean=True,
            encoding="UTF-8",
            remove_pis=True
        )

        first_xml = etree.fromstring(text=xml1, parser=parser)
        second_xml = etree.fromstring(text=xml2, parser=parser)

        self.assertXMLEqual(
            etree.tostring(first_xml).decode("UTF-8"),
            etree.tostring(second_xml).decode("UTF-8")
        )
