from eulxml.xmlmap import DateTimeField, NodeField, StringField, XmlObject

from ows_lib.xml_mapper.namespaces import CSW_2_0_2_NAMESPACE


class Acknowledgement(XmlObject):
    ROOT_NAME = "Acknowledgement"
    ROOT_NS = CSW_2_0_2_NAMESPACE
    ROOT_NAMESPACES = {
        "csw": CSW_2_0_2_NAMESPACE,

    }

    # mandatory attributes
    time_stamp = DateTimeField(
        xpath="./@timestamp")

    echoed_get_records_request = NodeField(
        xpath="./csw:EchoedRequest/csw:GetRecords", node_class=XmlObject
    )

    request_id = StringField(
        xpath="./csw:RequestId"
    )
