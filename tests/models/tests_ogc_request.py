import os

from django.db.models.expressions import Value
from django.db.models.query_utils import Q
from django.test import RequestFactory, SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.models.ogc_request import OGCRequest
from ows_lib.xml_mapper.exceptions import (
    InvalidParameterValueException,
    MissingConstraintLanguageParameterException)
from ows_lib.xml_mapper.xml_requests.wfs.get_feature import GetFeatureRequest
from tests.settings import DJANGO_TEST_ROOT_DIR


class OGCRequestTest(SimpleTestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_ogc_request_from_django_request(self):

        django_request = self.factory.get(
            "http://mrmap-proxy/wms/cd16cc1f-3abb-4625-bb96-fbe80dbe23e3/",
            {
                "REQUEST": ["GetMap"],
                "SERVICE": "WMS",
                "VERSION": "1.3.0",
                "LAYERS": "somelayer,anotherlayer"
            }
        )
        ogc_request = OGCRequest.from_django_request(django_request)

        self.assertEqual(django_request, ogc_request._djano_request)
        self.assertTrue(ogc_request.is_get)
        self.assertTrue(ogc_request.is_get_map_request)
        self.assertEqual(["somelayer", "anotherlayer"],
                         ogc_request.requested_entities)
        ogc_request.prepare()

    def test_ogc_request_with_get_map_request(self):
        """Test that OGCRequest helper class works correctly for a given GetMap get request"""

        ogc_request: OGCRequest = OGCRequest(
            method="GET",
            url="http://mrmap-proxy/wms/cd16cc1f-3abb-4625-bb96-fbe80dbe23e3/",
            params={"REQUEST": ["GetMap"], "SERVICE": "WMS", "VERSION": "1.3.0", "LAYERS": "somelayer,anotherlayer"})

        self.assertTrue(ogc_request.is_get)
        self.assertTrue(ogc_request.is_get_map_request)
        self.assertEqual(["somelayer", "anotherlayer"],
                         ogc_request.requested_entities)
        ogc_request.prepare()

    def test_ogc_request_with_post_get_feature_request(self):
        """Test that create manager function works correctly for a given GetFeature post request"""

        path = os.path.join(DJANGO_TEST_ROOT_DIR,
                            "./test_data/xml_requests/get_feature_2.0.0.xml")

        get_feature_request: GetFeatureRequest = load_xmlobject_from_file(
            filename=path, xmlclass=GetFeatureRequest)

        ogc_request: OGCRequest = OGCRequest(
            url="http://mrmap-proxy/wfs/73cf78c9-6605-47fd-ac4f-1be59265df65/",
            data=get_feature_request.serializeDocument(),
            headers={"content_type": "application/gml+xml; version=3.2"},
            method="POST")

        self.assertTrue(ogc_request.is_post)
        self.assertTrue(ogc_request.is_get_feature_request)
        self.assertEqual(["ms:Countries"], ogc_request.requested_entities)
        self.assertTrue(isinstance(ogc_request.xml_request, GetFeatureRequest))
        ogc_request.prepare()

    def test_ogc_request_with_get_records_request_without_constraint_langugage(self):
        """Test that OGCRequest helper class works correctly for a given GetMap get request"""

        # Missing constraint language
        ogc_request: OGCRequest = OGCRequest(
            method="GET",
            url="http://mrmap-proxy/csw/cd16cc1f-3abb-4625-bb96-fbe80dbe23e3/",
            params={"REQUEST": ["GetRecords"], "SERVICE": "CSW", "VERSION": "2.0.2", "Constraint": "title LIKE '%ips%'"})

        self.assertTrue(ogc_request.is_csw)
        self.assertTrue(ogc_request.is_get_records_request)

        self.assertEqual(
            MissingConstraintLanguageParameterException,
            type(ogc_request.filter_constraint()))

    def test_ogc_request_with_get_records_request_with_cql_filter(self):
        """Test that OGCRequest helper class works correctly for a given GetMap get request"""

        # cql filter
        ogc_request: OGCRequest = OGCRequest(
            method="GET",
            url="http://mrmap-proxy/csw/cd16cc1f-3abb-4625-bb96-fbe80dbe23e3/",
            params={"REQUEST": ["GetRecords"], "SERVICE": "CSW", "VERSION": "2.0.2", "Constraint": "title LIKE '%ips%' ", "CONSTRAINTLANGUAGE": "CQL_TEXT"})

        expected_query = Q(title__contains='ips')

        self.assertTrue(ogc_request.is_csw)
        self.assertTrue(ogc_request.is_get_records_request)
        f = ogc_request.filter_constraint()
        self.assertEqual(expected_query, f)

    def test_ogc_request_with_get_records_request_with_wrong_cql_filter(self):
        """Test that OGCRequest helper class works correctly for a given GetMap get request"""

        # cql filter
        ogc_request: OGCRequest = OGCRequest(
            method="GET",
            url="http://mrmap-proxy/csw/cd16cc1f-3abb-4625-bb96-fbe80dbe23e3/",
            params={"REQUEST": ["GetRecords"], "SERVICE": "CSW", "VERSION": "2.0.2", "Constraint": "title like '%ips%' ", "CONSTRAINTLANGUAGE": "CQL_TEXT"})

        self.assertTrue(ogc_request.is_csw)
        self.assertTrue(ogc_request.is_get_records_request)
        self.assertEqual(
            InvalidParameterValueException,
            type(ogc_request.filter_constraint()))

    def test_ogc_request_with_get_records_request_with_wrong_fes_filter(self):
        """Test that OGCRequest helper class works correctly for a given GetMap get request"""

        # cql filter
        ogc_request: OGCRequest = OGCRequest(
            method="GET",
            url="http://mrmap-proxy/csw/cd16cc1f-3abb-4625-bb96-fbe80dbe23e3/",
            params={"REQUEST": ["GetRecords"], "SERVICE": "CSW", "VERSION": "2.0.2", "Constraint": '<ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:a><ogc:ValueReference>type</ogc:ValueReference><ogc:Literal>dataset</ogc:Literal></ogc:a></ogc:Filter>', "CONSTRAINTLANGUAGE": "FILTER"})

        self.assertTrue(ogc_request.is_csw)
        self.assertTrue(ogc_request.is_get_records_request)

        self.assertEqual(
            InvalidParameterValueException,
            type(ogc_request.filter_constraint()))

    def test_ogc_request_with_get_records_request_with_fes_filter(self):
        """Test that OGCRequest helper class works correctly for a given GetMap get request"""

        # cql filter
        ogc_request: OGCRequest = OGCRequest(
            method="GET",
            url="http://mrmap-proxy/csw/cd16cc1f-3abb-4625-bb96-fbe80dbe23e3/",
            params={"REQUEST": ["GetRecords"], "SERVICE": "CSW", "VERSION": "2.0.2", "Constraint": '<ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:PropertyIsEqualTo><ogc:ValueReference>type</ogc:ValueReference><ogc:Literal>dataset</ogc:Literal></ogc:PropertyIsEqualTo></ogc:Filter>', "CONSTRAINTLANGUAGE": "FILTER"})

        expected_query = Q(type__exact=Value('dataset'))

        self.assertTrue(ogc_request.is_csw)
        self.assertTrue(ogc_request.is_get_records_request)
        f = ogc_request.filter_constraint()
        self.assertEqual(expected_query, f)
