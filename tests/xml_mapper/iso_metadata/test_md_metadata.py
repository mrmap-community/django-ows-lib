import os

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
