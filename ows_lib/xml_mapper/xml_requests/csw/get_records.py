from django.db.models.query_utils import Q
from eulxml.xmlmap import NodeField, StringField, XmlObject
from lxml.etree import XMLSyntaxError
from pygeofilter.backends.django.evaluate import to_filter
from pygeofilter.parsers.fes.util import NodeParsingError

from ows_lib.contrib.fes.parser import parse as parse_fes
from ows_lib.xml_mapper.exceptions import InvalidParameterValueException
from ows_lib.xml_mapper.namespaces import CSW_2_0_2_NAMESPACE, OGC_NAMESPACE


class GetRecordsRequest(XmlObject):
    ROOT_NS = CSW_2_0_2_NAMESPACE
    ROOT_NAME = "GetRecords"
    ROOT_NAMESPACES = {
        "csw": CSW_2_0_2_NAMESPACE,
        "ogc": OGC_NAMESPACE
    }

    service_version = StringField(xpath="./@version")
    service_type = StringField(xpath="./@service")
    result_type = StringField(xpath="./@resultType")
    max_records = StringField(xpath="./@maxRecords")
    element_set_name = StringField(xpath="./csw:Query/csw:ElementSetName")
    type_names = StringField(xpath="./csw:Query/@typeNames")

    _sort_by_property = StringField(
        xpath='./csw:Query/ogc:SortBy/ogc:SortProperty/ogc:PropertyName')
    _sort_by_order = StringField(
        xpath='./csw:Query/ogc:SortBy/ogc:SortProperty/ogc:SortOrder')

    constraint_filter = NodeField(
        xpath="./csw:Query/csw:Constraint/ogc:Filter", node_class=XmlObject)

    @property
    def sort_by(self):
        prop = self._sort_by_property

        if self._sort_by_order == "DESC":
            return f"-{prop}"
        else:
            return prop

    @sort_by.setter
    def sort_by(self, value):
        if value.startswith("-"):
            self._sort_by_order = "DESC"
            self._sort_by_property = value.split("-")[1]
        else:
            self._sort_by_order = "ASC"
            self._sort_by_property = value

    def get_django_filter(self, field_mapping=None, mapping_choices=None):
        if not self.constraint_filter:
            return Q()
        try:
            ast = parse_fes(
                self.constraint_filter.node)
            return to_filter(ast, field_mapping, mapping_choices)
        except (XMLSyntaxError, NodeParsingError) as e:
            return InvalidParameterValueException(
                ogc_request=self,
                message=e
            )
