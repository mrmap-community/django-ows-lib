import os

from django.db.models.expressions import Value
from django.db.models.query_utils import Q
from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.xml_mapper.xml_requests.csw.get_records import GetRecordsRequest
from tests.settings import DJANGO_TEST_ROOT_DIR


class GetRecordsRequestTestCase(SimpleTestCase):

    request_xml = os.path.join(DJANGO_TEST_ROOT_DIR,
                               "test_data/xml_requests/get_records_2.2.0.xml")

    def setUp(self) -> None:
        self.parsed_xml_request: GetRecordsRequest = load_xmlobject_from_file(
            self.request_xml, xmlclass=GetRecordsRequest)

    def test_success_parsing(self):

        self.assertEqual(self.parsed_xml_request.service_type, "CSW")
        self.assertEqual(self.parsed_xml_request.service_version, "2.0.2")
        self.assertEqual(self.parsed_xml_request.sort_by, "-Title")
        self.assertEqual(self.parsed_xml_request.element_set_name, "full")

        self.assertEqual(self.parsed_xml_request.type_names, "csw:Record")

        self.assertEqual(
            Q(search__exact=Value("Bâtiments")),
            self.parsed_xml_request.get_django_filter(
                field_mapping={"AnyText": "search"})
        )
