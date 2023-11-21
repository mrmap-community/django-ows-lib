import os

from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file
from isodate.isodatetime import parse_datetime
from lxml import etree

from ows_lib.xml_mapper.xml_responses.csw.get_records import GetRecordsResponse
from tests.settings import DJANGO_TEST_ROOT_DIR
from tests.utils import ExtendedSimpleTestCase


class GetRecordsResponseTestCase(ExtendedSimpleTestCase):

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

        self.maxDiff = None
        self.assertXMLIEqual(first,
                             second)
