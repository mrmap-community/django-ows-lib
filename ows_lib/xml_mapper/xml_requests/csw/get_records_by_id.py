from eulxml.xmlmap import StringField, StringListField, XmlObject

from ows_lib.xml_mapper.namespaces import CSW_2_0_2_NAMESPACE


class GetRecordByIdRequest(XmlObject):
    ROOT_NS = CSW_2_0_2_NAMESPACE
    ROOT_NAME = "GetRecordById"
    ROOT_NAMESPACES = {
        "csw": CSW_2_0_2_NAMESPACE,
    }

    service_version = StringField(xpath="./@version")
    service_type = StringField(xpath="./@service")
    element_set_name = StringField(xpath="./csw:ElementSetName")

    ids = StringListField(xpath="./csw:Id")
