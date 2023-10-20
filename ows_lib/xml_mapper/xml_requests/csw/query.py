import copy
from typing import List

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon as GeosPolygon
from eulxml.xmlmap import (NodeField, NodeListField, StringField,
                           StringListField, XmlObject)

from ows_lib.xml_mapper.consts import FES_AND, FES_OR, FES_WITHIN
from ows_lib.xml_mapper.namespaces import CSW_2_0_2_NAMESPACE, OGC_NAMESPACE


class Query(XmlObject):
    ROOT_NS = CSW_2_0_2_NAMESPACE
    ROOT_NAME = "Query"
    ROOT_NAMESPACES = {
        "ogc": OGC_NAMESPACE
    }
