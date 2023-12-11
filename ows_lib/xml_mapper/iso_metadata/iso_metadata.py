import urllib
from typing import Dict, List

from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon as GeosPolygon
from eulxml import xmlmap

from ows_lib.xml_mapper.gml.gml import Gml
from ows_lib.xml_mapper.mixins import CustomXmlObject
from ows_lib.xml_mapper.namespaces import (GCO_NAMESPACE, GMD_NAMESPACE,
                                           GML_3_1_1_NAMESPACE, SRV_NAMESPACE)


class Keyword(CustomXmlObject, xmlmap.XmlObject):
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAME = "keyword"
    ROOT_NAMESPACES = dict([("gmd", GMD_NAMESPACE),
                            ("gco", GCO_NAMESPACE)])

    keyword = xmlmap.StringField(xpath="gco:CharacterString")


class Category(CustomXmlObject, xmlmap.XmlObject):
    # TODO: Add xml specific information like root_ns, root_name, and namespaces list

    category = xmlmap.StringField(xpath=".")


class Dimension(CustomXmlObject, xmlmap.XmlObject):
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAME = "extent"
    ROOT_NAMESPACES = dict([("gmd", GMD_NAMESPACE),
                            ("gml", GML_3_1_1_NAMESPACE)])

    temporal_extent_start = xmlmap.DateTimeField(
        xpath="gml:TimePeriod/gml:beginPosition")
    temporal_extent_start_indeterminate_position = xmlmap.StringField(
        xpath="gml:TimePeriod/gml:beginPosition/@indeterminatePosition")
    temporal_extent_end = xmlmap.DateTimeField(
        xpath="gml:TimePeriod/gml:endPosition")
    temporal_extent_end_indeterminate_position = xmlmap.StringField(
        xpath="gml:TimePeriod/gml:endPosition/@indeterminatePosition")


class EXGeographicBoundingBox(xmlmap.XmlObject):
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAME = "EX_GeographicBoundingBox"
    ROOT_NAMESPACES = dict([("gmd", GMD_NAMESPACE),
                            ("gco", GCO_NAMESPACE)])

    _min_x = xmlmap.FloatField(xpath="gmd:westBoundLongitude/gco:Decimal")
    _max_x = xmlmap.FloatField(xpath="gmd:eastBoundLongitude/gco:Decimal")
    _min_y = xmlmap.FloatField(xpath="gmd:southBoundLatitude/gco:Decimal")
    _max_y = xmlmap.FloatField(xpath="gmd:northBoundLatitude/gco:Decimal")

    @property
    def geometry(self) -> GeosPolygon:
        if self._min_x is not None and self._max_x is not None and self._min_y is not None and self._max_y is not None:
            return GeosPolygon(((self._min_x, self._min_y),
                               (self._min_x, self._max_y),
                               (self._max_x, self._max_y),
                               (self._max_x, self._min_y),
                               (self._min_x, self._min_y)))

    @geometry.setter
    def geometry(self, value: GeosPolygon):
        self._min_x = value.extent[0]
        self._min_y = value.extent[1]
        self._max_x = value.extent[2]
        self._max_y = value.extent[3]


class EXBoundingPolygon(xmlmap.XmlObject):
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAME = "EX_BoundingPolygon"
    ROOT_NAMESPACES = dict([("gmd", GMD_NAMESPACE)])

    _geometry_list = xmlmap.NodeListField(xpath="gmd:polygon",
                                          node_class=Gml)

    @property
    def geometries(self) -> MultiPolygon:
        """Return all founded gml geometries as a list of geos geometries.
        :return: 
        :rtype: MultiPolygon
        """
        geometries = []
        for geometry in self._geometry_list:
            geometries.append(geometry.to_geometry())
        return MultiPolygon(geometries)

    @geometries.setter
    def geometries(self, value):
        # TODO
        raise NotImplementedError()


class ReferenceSystem(CustomXmlObject, xmlmap.XmlObject):
    ROOT_NAME = "RS_Identifier"
    ROOT_NS = "gmd"
    ROOT_NAMESPACES = dict([("gmd", GMD_NAMESPACE),
                            ("gco", GCO_NAMESPACE)])

    _ref_system = xmlmap.StringField(xpath="gmd:code/gco:CharacterString")
    _gmx_ref_system = xmlmap.StringField(xpath="gmd:code/gmx:Anchor")

    def __eq__(self, other):
        return self.code == other.code and self.prefix == other.prefix

    def transform_to_model(self) -> Dict:
        attr = super().transform_to_model()
        attr.update({"code": self.code, "prefix": self.prefix})
        return attr

    def _parse_ref_system(self):
        ref_child = self._ref_system if self._ref_system else self._gmx_ref_system
        if ref_child:
            if "http://www.opengis.net/def/crs/EPSG" in ref_child:
                code = ref_child.split("/")[-1]
                prefix = "EPSG"
            else:
                code = ref_child.split(":")[-1]
                prefix = "EPSG"

            return code, prefix
        else:
            return None

    @property
    def code(self):
        code, _ = self._parse_ref_system()
        return code

    @code.setter
    def code(self, value):
        if "EPSG:" not in value:
            raise NotImplementedError(
                "we only can handle epsg codes like 'EPSG:4236' for now")
        self._ref_system = value

    @property
    def prefix(self):
        _, prefix = self._parse_ref_system()
        return prefix

    @prefix.setter
    def prefix(self, value):
        if "EPSG:" not in value:
            raise NotImplementedError(
                "we only can handle epsg codes like 'EPSG:4236' for now")
        self._ref_system = value


class CiResponsibleParty(CustomXmlObject, xmlmap.XmlObject):
    ROOT_NAME = "CI_ResponsibleParty"
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAMESPACES = dict([("gmd", "http://www.isotc211.org/2005/gmd"),
                           ("gco", "http://www.isotc211.org/2005/gco")])

    name = xmlmap.StringField(xpath="gmd:organisationName/gco:CharacterString")
    person_name = xmlmap.StringField(
        xpath="gmd:individualName/gco:CharacterString")
    phone = xmlmap.StringField(
        xpath="gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString")
    email = xmlmap.StringField(
        xpath="gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString")


class BaseIsoMetadata(CustomXmlObject, xmlmap.XmlObject):
    """Base ISO Metadata class with namespace declaration common to all ISO Metadata
    XmlObjects.

    .. Note::
       This class is intended mostly for internal use, but could be
       useful when extending or adding additional ISO Metadata
       :class:`~eulxml.xmlmap.XmlObject` classes.  The
       :attr:`GMD_NAMESPACE` is mapped to the prefix **gmd**.
       :attr:`GCO_NAMESPACE` is mapped to the prefix **gco**.
    """
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAMESPACES = {
        "gmd": GMD_NAMESPACE,
        "gco": GCO_NAMESPACE,
    }


class BasicInformation(BaseIsoMetadata):
    title = xmlmap.StringField(
        xpath="gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString")
    abstract = xmlmap.StringField(xpath="gmd:abstract/gco:CharacterString")
    access_constraints = xmlmap.StringField(
        xpath="gmd:resourceConstraints/gmd:MD_LegalConstraints[gmd:accessConstraints/gmd:MD_RestrictionCode/@codeListValue=\"otherRestrictions\"]/gmd:otherConstraints/gco:CharacterString")

    # character_set_code = xmlmap.StringField(xpath=f"{NS_WC}characterSet']/{NS_WC}MD_CharacterSetCode']/@codeListValue")

    dataset_contact = xmlmap.NodeField(xpath="gmd:pointOfContact/gmd:CI_ResponsibleParty",
                                       node_class=CiResponsibleParty)
    keywords = xmlmap.NodeListField(xpath="gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword",
                                    node_class=Keyword)

    _code_md = xmlmap.StringField(
        xpath="gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString")

    is_broken = False  # flag to signal that this metadata object has integrity error

    def _parse_identifier(self):
        _code = ""
        _code_space = ""
        if self._code_md:
            # new implementation:
            # http://inspire.ec.europa.eu/file/1705/download?token=iSTwpRWd&usg=AOvVaw18y1aTdkoMCBxpIz7tOOgu
            # from 2017-03-02 - the MD_Identifier - see C.2.5 Unique resource identifier - it is separated with a slash
            # - the codes pace should be everything after the last slash
            # now try to check if a single slash is available and if the md_identifier is a url
            parsed_url = urllib.parse.urlsplit(self._code_md)
            if parsed_url.scheme == "http" or parsed_url.scheme == "https" and "/" in parsed_url.path:
                tmp = self._code_md.split("/")
                _code = tmp[len(tmp) - 1]
                _code_space = self._code_md.replace(_code, "")
            elif parsed_url.scheme == "http" or parsed_url.scheme == "https" and "#" in self._code_md:
                tmp = self._code_md.split("#")
                _code = tmp[1]
                _code_space = tmp[0]
            else:
                _code = self._code_md
                _code_space = ""

        return _code.replace('\n', '').strip(), _code_space.replace('\n', '').strip()

    @property
    def code(self) -> str:
        return self._parse_identifier()[0]

    @property
    def code_space(self) -> str:
        return self._parse_identifier()[1]


class MdDataIdentification(BasicInformation):
    ROOT_NAME = "MD_DataIdentification"
    equivalent_scale = xmlmap.FloatField(
        xpath="gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer")
    ground_res = xmlmap.FloatField(
        xpath="gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gmd:Distance")
    categories = xmlmap.NodeListField(xpath="gmd:topicCategory/gmd:MD_TopicCategoryCode",
                                      node_class=Category)
    bbox_lat_lon_list = xmlmap.NodeListField(xpath="gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox",
                                             node_class=EXGeographicBoundingBox)
    bounding_polygon_list = xmlmap.NodeListField(xpath="gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_BoundingPolygon",
                                                 node_class=EXBoundingPolygon)
    dimensions = xmlmap.NodeListField(xpath="gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent",
                                      node_class=Dimension)


class SvOperationMetadata(BaseIsoMetadata):
    ROOT_NS = SRV_NAMESPACE
    ROOT_NAME = "SV_OperationMetadata"
    ROOT_NAMESPACES = {
        "gmd": GMD_NAMESPACE,
        "gco": GCO_NAMESPACE,
        "srv": SRV_NAMESPACE
    }

    # mandatory fields
    operation = xmlmap.StringField(
        xpath="svr:operationName/gco:characterString")
    dcp = xmlmap.StringListField(
        xpath="srv:DCP/srv:DCPList[codeList='http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#DCPList']/@codeListValue")
    url = xmlmap.StringListField(
        xpath="srv:connectPoint/gmd:CI_OnlineResource/gmd:linkage/gmd:URL")


class SvServiceIdentification(BasicInformation):
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAME = "SV_ServiceIdentification"
    ROOT_NAMESPACES = {
        "gmd": GMD_NAMESPACE,
        "gco": GCO_NAMESPACE,
        "srv": SRV_NAMESPACE
    }

    # mandatory fields
    service_type = xmlmap.StringField(xpath="srv:serviceType/gco:LocalName")
    coupling_type = xmlmap.StringField(
        xpath="srv:couplingType/srv:SV_CouplingType[@codeList='SV_CouplingType']/@codeListValue")
    contains_operations = xmlmap.NodeListField(xpath="srv:containsOperations/svr:SV_OperationMetadata",
                                               node_class=SvOperationMetadata)
    # optional fields
    service_type_version = xmlmap.StringListField(
        xpath="srv:serviceTypeVersion/gco:characterString")
    bbox_lat_lon_list = xmlmap.NodeListField(xpath="srv:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox",
                                             node_class=EXGeographicBoundingBox)
    bounding_polygon_list = xmlmap.NodeListField(xpath="srv:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_BoundingPolygon",
                                                 node_class=EXBoundingPolygon)
    dimensions = xmlmap.NodeListField(xpath="srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent",
                                      node_class=Dimension)

    equivalent_scale = xmlmap.FloatField(
        xpath="srv:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer")
    ground_res = xmlmap.FloatField(
        xpath="srv:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance")


class MdMetadata(BaseIsoMetadata):
    """XML mapper class to deserialize/serialize metadata information defined in the ISO 19115 specs.

    """
    XSD_SCHEMA = "http://www.isotc211.org/2005/gmd"  # NOSONAR: the xml schema url will still be with insecure http protocol. To match all xml files, we need to let it as it is.

    ROOT_NAME = "MD_Metadata"
    ROOT_NS = GMD_NAMESPACE
    ROOT_NAMESPACES = {
        "gmd": GMD_NAMESPACE,
        "gco": GCO_NAMESPACE,
        "srv": SRV_NAMESPACE,
    }

    file_identifier = xmlmap.StringField(
        xpath="gmd:fileIdentifier/gco:CharacterString")
    # language = xmlmap.StringField(xpath=f"{NS_WC}identificationInfo']//{NS_WC}language']/{NS_WC}LanguageCode']")

    # TODO: add a default value such as http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_ScopeCode for example?
    _hierarchy_level_code_list = xmlmap.StringField(
        xpath="gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeList"

    )
    _hierarchy_level = xmlmap.StringField(
        xpath="gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue")

    _date_stamp_date = xmlmap.DateField(xpath="gmd:dateStamp/gco:Date")
    _date_stamp_date_time = xmlmap.DateTimeField(
        xpath="gmd:dateStamp/gco:DateTime")
    metadata_contact = xmlmap.NodeField(
        xpath="gmd:contact/gmd:CI_ResponsibleParty", node_class=CiResponsibleParty)
    reference_systems = xmlmap.NodeListField(
        xpath="gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier", node_class=ReferenceSystem)

    _md_data_identification = xmlmap.NodeField(xpath="gmd:identificationInfo/gmd:MD_DataIdentification",
                                               node_class=MdDataIdentification)
    _sv_service_identification = xmlmap.NodeField(xpath="gmd:identificationInfo/srv:SV_ServiceIdentification",
                                                  node_class=SvServiceIdentification)

    def _get_child_identification(self):
        if self._md_data_identification:
            return self._md_data_identification
        elif self._sv_service_identification:
            return self._sv_service_identification

    @property
    def is_dataset(self):
        return self._hierarchy_level == "dataset"

    @property
    def is_service(self):
        return self._hierarchy_level == "service"

    @property
    def date_stamp(self):
        return self._date_stamp_date if self._date_stamp_date else self._date_stamp_date_time

    @date_stamp.setter
    def date_stamp(self, value):
        self._date_stamp_date_time = value

    @property
    def bounding_geometry(self):
        child = self._get_child_identification()
        if child:
            polygon_list = []
            for bbox in child.bbox_lat_lon_list:
                if bbox.geometry:
                    polygon_list.append(bbox.geometry)
            for polygon in child.bounding_polygon_list:
                if polygon.geometries:
                    polygon_list.extend(polygon.geometries)
            return MultiPolygon(polygon_list)

    @bounding_geometry.setter
    def bounding_geometry(self, value: MultiPolygon):
        bbox = value.convex_hull
        bounding_polygons = value
        # TODO
        raise NotImplementedError()

    def get_spatial_res(self):
        child = self._get_child_identification()
        if child:
            if child.equivalent_scale is not None and child.equivalent_scale > 0:
                return child.equivalent_scale, "scaleDenominator"
            elif child.ground_res is not None and child.ground_res > 0:
                return child.ground_res, "groundDistance"

    @property
    def spatial_res_type(self):
        res = self.get_spatial_res()
        return res[1] if res else None

    @spatial_res_type.setter
    def spatial_res_type(self, value):
        # TODO
        raise NotImplementedError()

    @property
    def spatial_res_value(self):
        res = self.get_spatial_res()
        return res[0] if res else None

    @spatial_res_value.setter
    def spatial_res_value(self, value):
        # TODO
        raise NotImplementedError()

    @property
    def code(self) -> str:
        child = self._get_child_identification()
        if child and hasattr(child, "code"):
            return child.code

    @property
    def code_space(self) -> str:
        child = self._get_child_identification()
        if child and hasattr(child, "code_space"):
            return child.code_space

    @property
    def keywords(self) -> List[str]:
        child = self._get_child_identification()
        if child:
            return child.keywords
        return []

    @keywords.setter
    def keywords(self, value):
        child = self._get_child_identification()
        if child:
            child.keywords = value

    @property
    def title(self):
        child = self._get_child_identification()
        if child:
            return child.title

    @title.setter
    def title(self, value):
        child = self._get_child_identification()
        if child:
            child.title = value

    @property
    def abstract(self):
        child = self._get_child_identification()
        if child:
            return child.abstract

    @abstract.setter
    def abstract(self, value):
        child = self._get_child_identification()
        if child:
            child.abstract = value

    def transform_to_model(self) -> Dict:
        attr = super().transform_to_model()
        if self.date_stamp:
            attr.update({"date_stamp": self.date_stamp})
        if self.code:
            attr.update({"code": self.code})
        if self.code_space:
            attr.update({"code_space": self.code_space})
        if self.spatial_res_value:
            attr.update({"spatial_res_value": self.spatial_res_value})
        if self.bounding_geometry:
            attr.update({"bounding_geometry": self.bounding_geometry})
        if self.title:
            attr.update({"title": self.title})
        if self.abstract:
            attr.update({"abstract": self.abstract})
        return attr


class WrappedIsoMetadata(xmlmap.XmlObject):
    """Helper class to parse wrapped IsoMetadata objects.

    This class is needed if you want to parse GetRecordsResponse xml for example. There are 0..n ``gmd:MD_Metadata``
    nodes wrapped by a ``csw:GetRecordsResponse`` node.
    """
    ROOT_NAMESPACES = {"gmd": GMD_NAMESPACE}

    iso_metadata = xmlmap.NodeListField(
        xpath="//gmd:MD_Metadata", node_class=MdMetadata)
