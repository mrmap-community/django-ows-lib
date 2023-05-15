import os
from pathlib import Path

from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file

from ows_lib.xml_mapper.capabilities.wfs.wfs200 import WebFeatureService
from ows_lib.xml_mapper.utils import get_import_path_for_xml_mapper
from tests.settings import DJANGO_TEST_ROOT_DIR


class UtilsTestCase(SimpleTestCase):

    def setUp(self) -> None:
        self.wms_111 = Path(os.path.join(DJANGO_TEST_ROOT_DIR,
                                         "test_data/capabilities/wms/1.1.1.xml"))
        self.wms_130 = Path(os.path.join(DJANGO_TEST_ROOT_DIR,
                                         "test_data/capabilities/wms/1.3.0.xml"))
        self.wfs_200 = Path(os.path.join(DJANGO_TEST_ROOT_DIR,
                                         "test_data/capabilities/wfs/2.0.0.xml"))

    def test_get_import_path_for_xml_mapper_for_wfs_200(self):
        expected_path = "ows_lib.xml_mapper.capabilities.wfs.wfs200"
        resolved_path = get_import_path_for_xml_mapper(self.wfs_200)
        self.assertEqual(expected_path, resolved_path)

    def test_get_import_path_for_xml_mapper_for_wms111(self):
        expected_path = "ows_lib.xml_mapper.capabilities.wms.wms111"
        resolved_path = get_import_path_for_xml_mapper(self.wms_111)
        self.assertEqual(expected_path, resolved_path)

    def test_get_import_path_for_xml_mapper_for_wms130(self):
        expected_path = "ows_lib.xml_mapper.capabilities.wms.wms130"
        resolved_path = get_import_path_for_xml_mapper(self.wms_130)
        self.assertEqual(expected_path, resolved_path)
