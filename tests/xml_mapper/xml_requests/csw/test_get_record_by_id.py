import os

from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.xml_mapper.xml_requests.csw.get_records_by_id import \
    GetRecordByIdRequest
from tests.settings import DJANGO_TEST_ROOT_DIR


class GetRecordByIdRequestTestCase(SimpleTestCase):

    request_xml = os.path.join(DJANGO_TEST_ROOT_DIR,
                               "test_data/xml_requests/get_record_by_id_2.2.0.xml")

    def setUp(self) -> None:
        self.parsed_xml_request: GetRecordByIdRequest = load_xmlobject_from_file(
            self.request_xml, xmlclass=GetRecordByIdRequest)

    def test_success_parsing(self):

        self.assertEqual(self.parsed_xml_request.service_type, "CSW")
        self.assertEqual(self.parsed_xml_request.service_version, "2.0.2")
        self.assertEqual(self.parsed_xml_request.element_set_name, "full")

        self.assertEqual(
            self.parsed_xml_request.ids,
            [
                "5df54bf0-3a7d-44bf-9abf-84d772da8df1",
                "d256703f-f2d8-43e6-9c3a-c006299eba76",
                "d4b2a76c-4ff2-4585-bde1-445c5c738a3b6"
            ]
        )
