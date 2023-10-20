import copy
from typing import List

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon as GeosPolygon
from django.db.models.query_utils import Q
from eulxml.xmlmap import (NodeField, NodeListField, StringField,
                           StringListField, XmlObject)

from ows_lib.xml_mapper.consts import FES_AND, FES_OR, FES_WITHIN
from ows_lib.xml_mapper.gml.gml import Gml
from ows_lib.xml_mapper.namespaces import (CSW_2_0_2_NAMESPACE,
                                           GML_3_2_2_NAMESPACE, OGC_NAMESPACE)


class Comparision(XmlObject):

    """
    TODO: property_name can be validated by:
    [4] NCName ::= (Letter | '_') (NCNameChar)*
    /* An XML Name, minus the ":" */
    [5] NCNameChar ::= Letter | Digit | '.' | '-' | '_' | CombiningChar | Extender
    [6] QName ::= (Prefix ':')? LocalPart
    [7] Prefix ::= NCName
    [8] LocalPart ::= NCName
    """
    # TODO: handle xpath values
    property_name = StringField(xpath="./PropertyName")
    literal = StringField(xpath="./Literal")

    # simple lookup map for mapping property names to django model names
    property_name_lookup = {}

    django_lookup: str = ""

    def get_lookup_value(self):
        return self.literal

    def get_property_name(self):
        return self.property_name_lookup.get(self.property_name, self.property_name)

    def get_django_query(self) -> Q:
        if not self.django_lookup:
            raise NotImplementedError()
        return Q(f"{self.get_property_name()}__{self.django_lookup}={self.get_lookup_value()}")


class PropertyIsEqualTo(Comparision):
    ROOT_NAME = "PropertyIsEqualTo"
    django_lookup = "exact"


class PropertyIsNotEqualTo(Comparision):
    ROOT_NAME = "PropertyIsNotEqualTo"
    django_lookup = "exact"

    def get_django_query(self) -> Q:
        return ~super().get_django_query()


class PropertyIsLessThan(Comparision):
    ROOT_NAME = "PropertyIsLessThan"
    django_lookup = "lt"


class PropertyIsLessThanOrEqualTo(Comparision):
    ROOT_NAME = "PropertyIsLessThanOrEqualTo"
    django_lookup = "lte"


class PropertyIsGreaterThan(Comparision):
    ROOT_NAME = "PropertyIsGreaterThan"
    django_lookup = "gt"


class PropertyIsGreaterThanOrEqualTo(Comparision):
    ROOT_NAME = "PropertyIsGreaterThanOrEqualTo"
    django_lookup = "gte"


class PropertyIsLike(Comparision):
    # FES 2.0 only
    ROOT_NAME = "PropertyIsLike"
    django_lookup = "icontains"

    wild_card = StringField(xpath="./@wildCard")
    singleChar = StringField(xpath="./@singleChar")
    escapeChar = StringField(xpath="./@escapeChar")

    # TODO: wildCard=*, singleChar="#" escapeChar="!"

    # contains : *JOHN*
    # startswith: JOHN*
    # endswith: *JOHN


class PropertyIsNull(Comparision):
    ROOT_NAME = "PropertyIsNull"
    django_lookup = "isnull"

    literal = True


class SpatialComparision(Comparision):
    ROOT_NAMESPACES = {
        "gml": GML_3_2_2_NAMESPACE
    }

    gml = NodeField(xpath="gml:*", node_class=Gml)

    def get_lookup_value(self):
        return self.gml.to_geometry


class Intersects(SpatialComparision):
    ROOT_NAME = "Intersects"
    django_lookup = "intersects"


class Disjoint(SpatialComparision):
    ROOT_NAME = "Disjoint"
    django_lookup = "disjoint"


class Contains(SpatialComparision):
    ROOT_NAME = "Contains"
    django_lookup = "contains"


class Within(SpatialComparision):
    ROOT_NAME = "Within"
    django_lookup = "within"


class Touches(SpatialComparision):
    ROOT_NAME = "Touches"
    django_lookup = "touches"


class Crosses(SpatialComparision):
    ROOT_NAME = "Crosses"
    django_lookup = "crosses"


class Overlaps(SpatialComparision):
    ROOT_NAME = "Overlaps"
    django_lookup = "overlaps"


class Equals(SpatialComparision):
    ROOT_NAME = "Equals"
    django_lookup = "equals"


class Filter(XmlObject):
    # TODO:
    # ROOT_NS = CSW_2_0_2_NAMESPACE
    ROOT_NAME = "Filter"
    # ROOT_NAMESPACES = {
    #    "ogc": OGC_NAMESPACE
    # }
