import os

from django.test import SimpleTestCase
from eulxml.xmlmap import XmlObject, load_xmlobject_from_file
from isodate.isodatetime import parse_datetime
from lxml import etree
from lxml.etree import fromstring

from ows_lib.xml_mapper.xml_responses.csw.achnowledgment import Acknowledgement
from tests.settings import DJANGO_TEST_ROOT_DIR


class AcknowledgmentResponseTestCase(SimpleTestCase):

    excepted_xml = os.path.join(DJANGO_TEST_ROOT_DIR,
                                "test_data/xml_responses/acknowledgement_2.0.2.xml")

    def setUp(self) -> None:
        self.parsed_xml_response: Acknowledgement = load_xmlobject_from_file(
            self.excepted_xml, xmlclass=Acknowledgement)

    def test_acknowledgement_construction(self):

        first = self.parsed_xml_response.serializeDocument()
        second = Acknowledgement(
            time_stamp=parse_datetime("2023-11-02T08:24:47Z"),
        )
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

        echoed_request = """
        <csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" service="CSW" version="2.0.2">
            <csw:Query typeNames="csw:Record">
                <csw:ElementSetName>full</csw:ElementSetName>
                <csw:Constraint version="1.1.0">
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo matchCase="true">
                            <ogc:PropertyName>AnyText</ogc:PropertyName>
                            <ogc:Literal>Bâtiments</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                </csw:Constraint>
                <ogc:SortBy xmlns:ogc="http://www.opengis.net/ogc">
                    <ogc:SortProperty>
                        <ogc:PropertyName>Title</ogc:PropertyName>
                        <ogc:SortOrder>DESC</ogc:SortOrder>
                    </ogc:SortProperty>
                </ogc:SortBy>
            </csw:Query>
        </csw:GetRecords>
        """
        second.echoed_get_records_request = XmlObject(
            node=fromstring(echoed_request, parser=parser))

        second = second.serializeDocument()

        # We need to format both xml files the same way... otherwise the self.assertXMLEqual function, which is based on str compare will fail
        parser = etree.XMLParser(
            remove_blank_text=True, remove_comments=True, ns_clean=True, encoding="UTF-8", remove_pis=True)

        first_xml = etree.fromstring(text=first, parser=parser)
        second_xml = etree.fromstring(text=second, parser=parser)

        self.maxDiff = None
        self.assertXMLEqual(etree.tostring(first_xml).decode("UTF-8"),
                            etree.tostring(second_xml).decode("UTF-8"))
