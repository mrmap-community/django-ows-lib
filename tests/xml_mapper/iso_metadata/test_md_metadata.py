import os
from datetime import datetime

from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon as GeosPolygon
from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.xml_mapper.iso_metadata.iso_metadata import MdMetadata
from tests.settings import DJANGO_TEST_ROOT_DIR


class MDMetadataTestCase(SimpleTestCase):

    path = os.path.join(DJANGO_TEST_ROOT_DIR,
                        "test_data/iso_metadata/dataset.xml")

    def setUp(self) -> None:
        self.parsed_metadata: MdMetadata = load_xmlobject_from_file(
            self.path, xmlclass=MdMetadata)

    def test_base_mapper(self):
        self.assertEqual(
            self.parsed_metadata.file_identifier,
            "de.dwd.geoserver.fach.RBSN_FF"
        )

    def test_date_stamp(self):
        self.assertEqual(
            self.parsed_metadata.date_stamp,
            datetime.fromisoformat("2019-05-16T12:55:18")
        )

    def test_bounding_geometry_getter(self):
        min_x = 5.87
        max_x = 15.04
        min_y = 47.27
        max_y = 55.06

        self.assertEqual(
            self.parsed_metadata.bounding_geometry,

            MultiPolygon(GeosPolygon(((min_x, min_y),
                                      (min_x, max_y),
                                      (max_x, max_y),
                                      (max_x, min_y),
                                      (min_x, min_y))))
        )
