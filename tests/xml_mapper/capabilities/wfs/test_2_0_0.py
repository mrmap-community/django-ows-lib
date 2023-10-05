import os

from django.contrib.gis.geos import Polygon
from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.xml_mapper.capabilities.mixins import OperationUrl
from ows_lib.xml_mapper.capabilities.wfs.wfs200 import WebFeatureService
from ows_lib.xml_mapper.namespaces import (OWS_1_1_NAMESPACE,
                                           WFS_2_0_0_NAMESPACE,
                                           XLINK_NAMESPACE)
from tests.settings import DJANGO_TEST_ROOT_DIR


class WebFeatureServiceTestCase(SimpleTestCase):

    path = os.path.join(DJANGO_TEST_ROOT_DIR,
                        "test_data/capabilities/wfs/2.0.0.xml")

    xml_class = WebFeatureService

    version = "2.0.0"

    def setUp(self) -> None:
        self.parsed_capabilities: self.xml_class = load_xmlobject_from_file(
            self.path, xmlclass=self.xml_class)

    def _test_service_metadata_mapper(self):
        self.assertEqual(
            self.parsed_capabilities.title,
            "DWD GeoServer WFS")
        self.assertEqual(
            self.parsed_capabilities.abstract,
            "This is the Web Feature Server of DWD.")
        self.assertEqual(
            self.parsed_capabilities.fees,
            "none"
        )
        self.assertEqual(
            self.parsed_capabilities.access_constraints,
            "http://www.dwd.de/DE/service/copyright/copyright_node.html"
        )

    def _test_service_contact_mapper(self):
        self.assertEqual(
            self.parsed_capabilities.service_contact.name,
            "Deutscher Wetterdienst"
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.person_name,
            ""
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.phone,
            ""
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.facsimile,
            ""
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.email,
            "info@dwd.de"
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.country,
            "Germany"
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.postal_code,
            "63067"
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.city,
            "Offenbach"
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.state_or_province,
            "Hessen"
        )
        self.assertEqual(
            self.parsed_capabilities.service_contact.address,
            ""
        )

    def _test_service_keywords(self):
        self.assertEqual(
            self.parsed_capabilities.keywords[0],
            "meteorology"
        )
        self.assertEqual(
            self.parsed_capabilities.keywords[1],
            "climatology"
        )

    def _test_get_capabilities_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].operation,
            "GetCapabilities"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].mime_types[0],
            "text/xml"
        )

        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].operation,
            "GetCapabilities"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].mime_types[0],
            "text/xml"
        )

    def _test_describe_feature_type_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].operation,
            "DescribeFeatureType"
        )

        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].mime_types[0],
            "application/gml+xml; version=3.2"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].operation,
            "DescribeFeatureType"
        )

        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].mime_types[0],
            "application/gml+xml; version=3.2"
        )

    def _test_get_feature_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[4].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[4].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[4].operation,
            "GetFeature"
        )
        self.assertEqual(
            len(self.parsed_capabilities.operation_urls[4].mime_types),
            16
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[4].mime_types[0],
            "application/gml+xml; version=3.2"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[4].mime_types[1],
            "GML2"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[4].mime_types[2],
            "KML"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[5].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[5].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[5].operation,
            "GetFeature"
        )
        self.assertEqual(
            len(self.parsed_capabilities.operation_urls[5].mime_types),
            16
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[5].mime_types[0],
            "application/gml+xml; version=3.2"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[5].mime_types[1],
            "GML2"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[5].mime_types[2],
            "KML"
        )

    def _test_get_property_value_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[6].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[6].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[6].operation,
            "GetPropertyValue"
        )

        self.assertEqual(
            self.parsed_capabilities.operation_urls[6].mime_types[0],
            "application/gml+xml; version=3.2"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[7].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[7].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[7].operation,
            "GetPropertyValue"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[7].mime_types[0],
            "application/gml+xml; version=3.2"
        )

    def _test_list_stored_queries_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[8].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[8].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[8].operation,
            "ListStoredQueries"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[9].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[9].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[9].operation,
            "ListStoredQueries"
        )

    def _test_describe_stored_queries_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[10].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[10].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[10].operation,
            "DescribeStoredQueries"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[11].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[11].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[11].operation,
            "DescribeStoredQueries"
        )

    def _test_create_stored_query_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[12].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[12].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[12].operation,
            "CreateStoredQuery"
        )

    def _test_drop_stored_query_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[13].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[13].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[13].operation,
            "DropStoredQuery"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[14].url,
            "https://maps.dwd.de/geoserver/wfs"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[14].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[14].operation,
            "DropStoredQuery"
        )

    def _test_service_type_mapper(self):
        self.assertEqual(
            self.parsed_capabilities.service_type.version, self.version)
        self.assertEqual(self.parsed_capabilities.service_type.name, "wfs")

    def _test_feature_type_mapper(self):
        ft = self.parsed_capabilities.get_feature_type_by_identifier(
            "dwd:RBSN_T2m")
        self.assertEqual(
            ft.identifier,
            "dwd:RBSN_T2m"
        )
        self.assertEqual(
            ft.title,
            "2m Temperatur an RBSN Stationen"
        )
        self.assertEqual(
            ft.abstract,
            "Messwerte der 2m Temperatur an den DWD Stationen im Regional Basic Synoptic Network (RBSN) der WMO. Erweitert um weitere Stationen der Grundversorgung."
        )

        self.assertEqual(
            ft.bbox_lat_lon,
            Polygon(
                (
                    (6.02439799999999, 47.398578),
                    (6.02439799999999, 55.010987),
                    (14.950565, 55.010987),
                    (14.950565, 47.398578),
                    (6.02439799999999, 47.398578)
                )
            )
        )
        self.assertEqual(
            ft.keywords[0],
            "Beobachtungssystem"
        )

        self.assertEqual(
            ft.reference_systems[0].code,
            "4258"
        )
        self.assertEqual(
            ft.reference_systems[0].prefix,
            "EPSG"
        )

        self.assertDictEqual(
            ft.reference_systems[0].transform_to_model(
            ),
            {"code": "4258", "prefix": "EPSG"}
        )

        self.assertEqual(
            ft.remote_metadata[0].link,
            "https://registry.gdi-de.org/id/de.bund.dwd/de.dwd.geoserver.fach.RBSN_T2m"
        )

    def test_wms_xml_mapper(self):
        self._test_service_metadata_mapper()
        self._test_service_contact_mapper()
        self._test_service_keywords()
        self._test_get_capabilities_operation_urls()
        self._test_describe_feature_type_operation_urls()
        self._test_get_feature_operation_urls()
        self._test_get_property_value_operation_urls()
        self._test_list_stored_queries_operation_urls()
        self._test_describe_stored_queries_operation_urls()
        self._test_create_stored_query_operation_urls()
        self._test_drop_stored_query_operation_urls()
        self._test_service_type_mapper()
        self._test_feature_type_mapper()

    def _get_added_get_feature_operation_url(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/ows:OperationsMetadata/ows:Operation[@name='GetFeature']/ows:DCP/ows:HTTP/ows:Get/@xlink:href",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

    def _get_operation_xml_nodes(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/ows:OperationsMetadata",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })

    def _get_all_operation_urls(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/ows:OperationsMetadata/ows:Operation//ows:DCP/ows:HTTP//@xlink:href",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })

    def _get_added_operation_url(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/ows:OperationsMetadata/ows:Operation[@name='GetCapabilities']/ows:DCP/ows:HTTP/ows:Get/@xlink:href",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

    def test_wfs_operation_urls_append(self):
        o_url = OperationUrl(
            method="Get",
            operation="GetFeature",
            mime_types=["image/png"],
            url="http://example.com")

        self.parsed_capabilities.operation_urls.append(
            o_url
        )

        added_operation_url = self._get_added_get_feature_operation_url()

        self.assertEqual(
            added_operation_url,
            "http://example.com"
        )

    def test_wfs_operation_urls_insert(self):
        o_url = OperationUrl(
            method="Get",
            operation="GetFeature",
            mime_types=["image/png"],
            url="http://example.com")

        self.parsed_capabilities.operation_urls.insert(
            0,
            o_url
        )

        added_operation_url = self._get_added_get_feature_operation_url()

        self.assertEqual(
            added_operation_url,
            "http://example.com"
        )

    def test_wfs_operation_urls_clear(self):
        self.parsed_capabilities.operation_urls.clear()

        operation_urls = self._get_all_operation_urls()

        self.assertEqual(
            len(self.parsed_capabilities.operation_urls),
            0
        )

        self.assertEqual(
            len(operation_urls),
            6
        )

    def test_wfs_operation_urls_pop(self):
        self.parsed_capabilities.operation_urls.pop(1)

        operation_urls = self._get_all_operation_urls()

        self.assertEqual(
            len(self.parsed_capabilities.operation_urls),
            14
        )

        self.assertEqual(
            len(operation_urls),
            20
        )

    def test_wfs_operation_urls_remove(self):

        o_url = self.parsed_capabilities.operation_urls[2]

        self.parsed_capabilities.operation_urls.remove(o_url)

        operation_urls = self._get_all_operation_urls()

        self.assertEqual(
            len(self.parsed_capabilities.operation_urls),
            14
        )

        self.assertEqual(
            len(operation_urls),
            20
        )

    def test_wfs_operation_urls_update_single_object(self):

        o_url = self.parsed_capabilities.operation_urls[0]
        o_url.url = "http://example.com"

        new_o_url_url = self._get_added_operation_url()

        self.assertEqual(
            new_o_url_url,
            "http://example.com"
        )

    def test_camouflage_urls(self):

        self.parsed_capabilities.camouflage_urls(new_domain="example.com")

        new_o_url_url = self._get_added_operation_url()

        self.assertEqual(
            new_o_url_url,
            "https://example.com/geoserver/wfs"
        )

    def _get_first_feature_type_min_x(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/wfs:FeatureTypeList/wfs:FeatureType[1]/ows:WGS84BoundingBox/ows:LowerCorner",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0].text.split(" ")[0]

    def _get_first_feature_type_min_y(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/wfs:FeatureTypeList/wfs:FeatureType[1]/ows:WGS84BoundingBox/ows:LowerCorner",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0].text.split(" ")[1]

    def _get_first_feature_type_max_x(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/wfs:FeatureTypeList/wfs:FeatureType[1]/ows:WGS84BoundingBox/ows:UpperCorner",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0].text.split(" ")[0]

    def _get_first_feature_type_max_y(self):
        return self.parsed_capabilities.node.xpath(
            "//wfs:WFS_Capabilities/wfs:FeatureTypeList/wfs:FeatureType[1]/ows:WGS84BoundingBox/ows:UpperCorner",
            namespaces={
                "wfs": WFS_2_0_0_NAMESPACE,
                "ows": OWS_1_1_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0].text.split(" ")[1]

    def test_feature_type_bbox_setter(self):
        new_poly = Polygon(
            (
                (-10, -20),
                (-10, 20),
                (10, 20),
                (10, -20),
                (-10, -20)
            )
        )

        self.parsed_capabilities.feature_types[0].bbox_lat_lon = new_poly

        first_feature_type_min_x = self._get_first_feature_type_min_x()
        first_feature_type_max_x = self._get_first_feature_type_max_x()
        first_feature_type_min_y = self._get_first_feature_type_min_y()
        first_feature_type_max_y = self._get_first_feature_type_max_y()

        self.assertEqual(
            float(first_feature_type_min_x),
            -10.0
        )
        self.assertEqual(
            float(first_feature_type_max_x),
            10.0
        )
        self.assertEqual(
            float(first_feature_type_min_y),
            -20.0
        )
        self.assertEqual(
            float(first_feature_type_max_y),
            20.0
        )

    def test_feature_types_property(self):
        self.assertEqual(
            len(self.parsed_capabilities.feature_types),
            55
        )
