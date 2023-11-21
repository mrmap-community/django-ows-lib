import os

from django.contrib.gis.geos import Polygon
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.xml_mapper.xml_requests.wfs.get_feature import GetFeatureRequest
from tests.settings import DJANGO_TEST_ROOT_DIR
from tests.utils import ExtendedSimpleTestCase


class GetFeatureRequestTestCase(ExtendedSimpleTestCase):

    insecure_xml = os.path.join(DJANGO_TEST_ROOT_DIR,
                                "test_data/xml_requests/get_feature_2.0.0.xml")
    secured_xml = os.path.join(DJANGO_TEST_ROOT_DIR,
                               "test_data/xml_requests/get_feature_secured_2.0.0.xml")

    def setUp(self) -> None:
        self.parsed_xml_request: GetFeatureRequest = load_xmlobject_from_file(
            self.insecure_xml, xmlclass=GetFeatureRequest)

    def test_secure_spatial(self):

        self.parsed_xml_request.secure_spatial(feature_types=[
            {
                "type_name": "ms:Countries",
                "geometry_property_name": "THE_GEOM",
                "allowed_area_union": Polygon(((-180, -90), (-180, 90), (180, 90), (180, -90), (-180, -90)), srid=4326),

            }
        ]
        )

        first = self.parsed_xml_request.serializeDocument()
        second = load_xmlobject_from_file(
            filename=self.secured_xml, xmlclass=GetFeatureRequest)
        second = second.serializeDocument()

        self.assertXMLIEqual(first, second)
