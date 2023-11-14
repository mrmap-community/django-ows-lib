
from eulxml.xmlmap import NodeListField, StringField, XmlObject

from ows_lib.xml_mapper.iso_metadata.iso_metadata import MdMetadata
from ows_lib.xml_mapper.namespaces import (CSW_2_0_2_NAMESPACE, GMD_NAMESPACE,
                                           XSI_NAMESPACE)


class GetRecordsResponse(XmlObject):
    ROOT_NAME = "GetRecordByIdResponse"
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

    gmd_records = NodeListField(
        xpath="./gmd:MD_Metadata", node_class=MdMetadata)

    def __init__(self, node=None, context=None, **kwargs):
        super().__init__(node, context, **kwargs)
        if not self.schema_location:
            self.schema_location = "http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"
