from eulxml.xmlmap import (DateTimeField, IntegerField, NodeListField,
                           StringField, XmlObject)

from ows_lib.xml_mapper.iso_metadata.iso_metadata import MdMetadata
from ows_lib.xml_mapper.namespaces import (CSW_2_0_2_NAMESPACE, GMD_NAMESPACE,
                                           XSI_NAMESPACE)


class CswRecord(XmlObject):
    ROOT_NAME = "Record"
    ROOT_NS = CSW_2_0_2_NAMESPACE
    ROOT_NAMESPACES = {
        "csw": CSW_2_0_2_NAMESPACE,
    }


class GetRecordsResponse(XmlObject):
    ROOT_NAME = "GetRecordsResponse"
    ROOT_NS = CSW_2_0_2_NAMESPACE
    ROOT_NAMESPACES = {
        "csw": CSW_2_0_2_NAMESPACE,
        "gmd": GMD_NAMESPACE,
        "xsi": XSI_NAMESPACE
    }

    XSD_SCHEMA = "http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"

    schema_location = StringField(
        xpath="./@xsi:schemaLocation"
    )

    # mandatory attributes
    total_records = IntegerField(
        xpath="./csw:SearchResults/@numberOfRecordsMatched")
    records_returned = IntegerField(
        xpath="./csw:SearchResults/@numberOfRecordsReturned")

    # optional attributes
    version = StringField(xpath="./@version")
    next_record = IntegerField(xpath="./csw:SearchResults/@nextRecord")
    record_schema = StringField(
        xpath="./csw:SearchResults/@recordSchema")
    element_set = StringField(
        xpath="./csw:SearchResults/@elementSet")
    result_set_id = StringField(
        xpath="./csw:SearchResults/@resultSetId")
    expires = DateTimeField(
        xpath="./csw:SearchResults/@expires")
    time_stamp = DateTimeField(
        xpath="./csw:SearchStatus/@timestamp")

    # record subelements
    csw_records = NodeListField(
        xpath="./csw:SearchResults/csw:Record", node_class=CswRecord)
    gmd_records = NodeListField(
        xpath="./csw:SearchResults/gmd:MD_Metadata", node_class=MdMetadata)

    def __init__(self, node=None, context=None, **kwargs):
        super().__init__(node, context, **kwargs)
        if not self.schema_location:
            self.schema_location = "http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"
