import os

from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file
from isodate.isodatetime import parse_datetime
from lxml import etree

from ows_lib.xml_mapper.xml_responses.csw.get_records import GetRecordsResponse
from tests.settings import DJANGO_TEST_ROOT_DIR


class GetRecordsResponseTestCase(SimpleTestCase):

    excepted_xml = os.path.join(DJANGO_TEST_ROOT_DIR,
                                "test_data/xml_responses/get_records_2.0.2.xml")

    def setUp(self) -> None:
        self.parsed_xml_response: GetRecordsResponse = load_xmlobject_from_file(
            self.excepted_xml, xmlclass=GetRecordsResponse)

    def test_get_records_response_construction(self):

        first = self.parsed_xml_response.serializeDocument()
        second = GetRecordsResponse(
            total_records=15075,
            records_returned=1000,
            next_record=1001,
            record_schema="http://www.opengis.net/cat/csw/2.0.2",
            element_set="full",
            time_stamp=parse_datetime("2023-11-02T08:24:47Z"),
            version="2.0.2"

        )
        second = second.serializeDocument()

        # We need to format both xml files the same way... otherwise the self.assertXMLEqual function, which is based on str compare will fail
        parser = etree.XMLParser(
            remove_blank_text=True, remove_comments=True, ns_clean=True, encoding="UTF-8", remove_pis=True)

        first_xml = etree.fromstring(text=first, parser=parser)
        second_xml = etree.fromstring(text=second, parser=parser)

        self.maxDiff = None
        self.assertXMLEqual(etree.tostring(first_xml).decode("UTF-8"),
                            etree.tostring(second_xml).decode("UTF-8"))
