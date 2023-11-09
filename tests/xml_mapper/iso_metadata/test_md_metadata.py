import os
from datetime import datetime

from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon as GeosPolygon
from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.xml_mapper.iso_metadata.iso_metadata import (MdMetadata,
                                                          ReferenceSystem,
                                                          WrappedIsoMetadata)
from tests.settings import DJANGO_TEST_ROOT_DIR


class MDMetadataTestCase(SimpleTestCase):

    path = os.path.join(DJANGO_TEST_ROOT_DIR,
                        "test_data/iso_metadata/dataset.xml")

    def setUp(self) -> None:
        self.parsed_metadata: MdMetadata = load_xmlobject_from_file(
            self.path, xmlclass=MdMetadata)

    def test_file_identifier(self):
        self.assertEqual(
            self.parsed_metadata.file_identifier,
            "de.dwd.geoserver.fach.RBSN_FF"
        )

    def test_dataset_id(self):
        self.assertEqual(
            self.parsed_metadata.dataset_id,
            "de.dwd.geoserver.fach.RBSN_FF"
        )

    def test_dataset_id_code_space(self):
        self.assertEqual(
            self.parsed_metadata.dataset_id_code_space,
            "https://registry.gdi-de.org/id/de.bund.dwd/"
        )

    def test_date_stamp(self):
        self.assertEqual(
            self.parsed_metadata.date_stamp,
            datetime.fromisoformat("2019-05-16T12:55:18")
        )

    def test_keywords(self):
        self.assertEqual(
            [kw.keyword for kw in self.parsed_metadata.keywords],
            ["meteorological", "inspireidentifiziert", "Wind", "meteorology",
                "Meteorologisch-geografische Kennwerte", "Deutschland", None]
        )

    def test_ref_system(self):
        self.assertEqual(
            [ref_system
             for ref_system in self.parsed_metadata.reference_systems],
            [ReferenceSystem(code="EPSG:4258"),
             ReferenceSystem(code="EPSG:4326")]
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


class WrappedMDMetadataTestCase(SimpleTestCase):

    path = os.path.join(DJANGO_TEST_ROOT_DIR,
                        "test_data/iso_metadata/wrapped_dataset.xml")

    def setUp(self) -> None:
        self.parsed_metadata: MdMetadata = load_xmlobject_from_file(
            self.path, xmlclass=WrappedIsoMetadata).iso_metadata[0]

    def test_field_dict(self):
        self.assertEqual(
            self.parsed_metadata.date_stamp,
            datetime.fromisoformat("2023-09-12T06:49:23")
        )

        field_dict = self.parsed_metadata.transform_to_model()
        expected = {
            'file_identifier': '80b250a6-4dda-481d-8568-162e20c1cb7a',
            'date_stamp': datetime(2023, 9, 12, 6, 49, 23),
            'dataset_id': 'LK2022',
            'bounding_geometry': GeosPolygon.from_ewkt("MULTIPOLYGON (((9.87 50.2, 9.87 51.64, 12.65 51.64, 12.65 50.2, 9.87 50.2)))")
        }
        self.assertEqual(field_dict, expected)
