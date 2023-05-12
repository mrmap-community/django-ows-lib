from typing import Dict, List

from django.contrib.gis.geos import GEOSGeometry
from eulxml.xmlmap import XmlObject, load_xmlobject_from_string
from requests import Request

from ows_lib.client.enums import OGCOperationEnum
from ows_lib.client.exceptions import MissingBboxParam, MissingServiceParam
from ows_lib.client.utils import (construct_polygon_from_bbox_query_param,
                                  get_requested_feature_types,
                                  get_requested_layers)
from ows_lib.xml_mapper.xml_requests.utils import PostRequest
from ows_lib.xml_mapper.xml_requests.wfs.get_feature import (GetFeatureRequest,
                                                             Query)


class OGCRequest(Request):
    """Extended Request class which provides some analyzing functionality for ogc requests."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._params_lower: dict = {}
        self._ogc_query_params: dict = {}
        self._bbox: GEOSGeometry = None
        self._requested_entities: List[str] = []
        self._xml_request: XmlObject = None

        if self.method == "GET":
            self.operation: str = self.params_lower.get("request", "")
            self.service_version: str = self.params_lower.get("version", "")
            self.service_type: str = self.params_lower.get("service", "")
        elif self.method == "POST":
            post_request: PostRequest = load_xmlobject_from_string(
                string=self.data, xmlclass=PostRequest)

            self.operation: str = post_request.operation
            self.service_version: str = post_request.version
            self.service_type: str = post_request.service_type

    @property
    def requested_entities(self) -> List[str]:
        """Returns the list of requested entities

        This function analyzes the request and find out which layers or featuretypes are requests.

        :return: list of requested layers | list of request featuretypes
        :rtype: List[str]
        """
        if not self._requested_entities:
            if self.is_wms:
                self._requested_entities.extend(
                    get_requested_layers(params=self.params_lower))
            else:
                if self.is_get_feature_request:
                    if self.is_get:
                        self._requested_entities.extend(
                            get_requested_feature_types(params=self.params_lower))
                    elif self.is_post:
                        self._requested_entities.extend(
                            self.xml_request.requested_feature_types)
        return self._requested_entities

    @property
    def is_wms(self) -> bool:
        """Check for wms request

        :return: true if this is a wms request
        :rtype: bool
        """
        return self.service_type.lower() == 'wms'

    @property
    def is_wfs(self) -> bool:
        """Check for wfs request

        :return: true if this is a wfs request
        :rtype: bool
        """
        return self.service_type.lower() == 'wfs'

    @property
    def is_post(self) -> bool:
        """Check for post method

        :return: true if this is a post request
        :rtype: bool
        """
        return self.method.lower() == "post"

    @property
    def is_get(self) -> bool:
        """Check for get method

        :return: true if this is a post request
        :rtype: bool
        """
        return self.method.lower() == "get"

    @property
    def is_get_capabilities_request(self) -> bool:
        """Check for ogc get capabilites request

        :return: true if this is a get capabilities request
        :rtype: bool
        """
        return self.operation.lower() == OGCOperationEnum.GET_CAPABILITIES.value.lower()

    @property
    def is_get_map_request(self) -> bool:
        """Check for wms get map request

        :return: true if this is a wms get map request
        :rtype: bool
        """
        return self.operation.lower() == OGCOperationEnum.GET_MAP.value.lower()

    @property
    def is_get_feature_info_request(self) -> bool:
        """Check for wms transaction request

        :return: true if this is a wfs tranasction request
        :rtype: bool
        """
        return self.operation.lower() == OGCOperationEnum.GET_FEATURE_INFO.value.lower()

    @property
    def is_get_feature_request(self) -> bool:
        """Check for wfs get feature request

        :return: true if this is a wfs get feature request
        :rtype: bool
        """
        return self.operation.lower() == OGCOperationEnum.GET_FEATURE.value.lower()

    @property
    def is_transaction_request(self) -> bool:
        """Check for wfs transaction request

        :return: true if this is a wfs tranasction request
        :rtype: bool
        """
        return self.operation.lower() == OGCOperationEnum.TRANSACTION.value.lower()

    @property
    def bbox(self) -> GEOSGeometry:
        """Analyzes the given request and tries to construct a Polygon from the query parameters.

        The axis order for different wms/wfs versions will be well transformed to the correct needed mathematical interpretation.

        :raises MissingBboxParam: if the bbox query param is missing
        :raises MissingServiceParam: if the service query param is missing. Without that the correct axis order can't be interpreted.

        :return: the given bbox as polygon object
        :rtype: GEOSGeometry
        """
        if not self._bbox:
            try:
                self._bbox = construct_polygon_from_bbox_query_param(
                    get_dict=self.params_lower)
            except (MissingBboxParam, MissingServiceParam):
                # only to avoid error while handling sql in service property
                self._bbox = GEOSGeometry("POLYGON EMPTY")
        return self._bbox

    @property
    def params_lower(self) -> Dict:
        """Lower case key mapper for paramas

        :return: all parameters of the request in lower case key
        :rtype: Dict
        """
        return {k.lower(): v for k, v in self.params.items()} if not self._params_lower else self._params_lower

    @property
    def ogc_query_params(self) -> Dict:
        """ Parses the GET parameters into all member variables, which can be found in a ogc request.
        :return: all ogc query parameters
        :rtype: Dict
        """
        if not self._ogc_query_params:
            query_keys = ["SERVICE", "REQUEST", "LAYERS", "BBOX", "VERSION", "FORMAT",
                          "OUTPUTFORMAT", "SRS", "CRS", "SRSNAME", "WIDTH", "HEIGHT",
                          "TRANSPARENT", "EXCEPTIONS", "BGCOLOR", "TIME", "ELEVATION",
                          "QUERY_LAYERS", "INFO_FORMAT", "FEATURE_COUNT", "I", "J"]
            self._ogc_query_params = {key: self.params_lower.get(
                key, self.params_lower.get(key.lower())) for key in query_keys}

        return self._ogc_query_params

    @property
    def xml_request(self) -> XmlObject:
        """Constructs a xml request object based on the given request.

        This function analyzes the given request by its method and operation. 
        If it is a get request, the get feature operation for example will be converted to an postable xml object.

        :return: The mapped xml object
        :rtype: XmlObject
        """
        if not self._xml_request:
            if self.is_get_feature_request:
                # FIXME: depending on version, different xml mapper are needed...
                if self.is_post:
                    self._xml_request: GetFeatureRequest = load_xmlobject_from_string(
                        string=self.data, xmlclass=GetFeatureRequest)
                elif self.is_get:
                    # we construct a xml get feature request to post it with a filter
                    queries: List[Query] = []
                    for feature_type in self.requested_entities:
                        query: Query = Query()
                        query.type_names = feature_type
                        queries.append(query)
                    self._xml_request: GetFeatureRequest = GetFeatureRequest()
                    self._xml_request.queries = queries
        return self._xml_request
