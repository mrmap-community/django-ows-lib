import os

from django.contrib.gis.geos import Polygon
from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file
from lxml import etree
from ows_lib.xml_mapper.xml_requests.wfs.get_feature import GetFeatureRequest
from tests.settings import DJANGO_TEST_ROOT_DIR


class GetFeatureRequestTestCase(SimpleTestCase):

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

        # We need to format both xml files the same way... otherwise the self.assertXMLEqual function, which is based on str compare will fail
        parser = etree.XMLParser(
            remove_blank_text=True, remove_comments=True, ns_clean=True, encoding="UTF-8", remove_pis=True)

        first_xml = etree.fromstring(text=first, parser=parser)
        second_xml = etree.fromstring(text=second, parser=parser)

        self.maxDiff = None
        self.assertXMLEqual(etree.tostring(first_xml).decode("UTF-8"),
                            etree.tostring(second_xml).decode("UTF-8"))
