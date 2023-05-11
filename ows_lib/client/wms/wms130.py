from ows_lib.client.wms.mixins import WebMapServiceMixin


class WebMapService(WebMapServiceMixin):
    """Concrete WebMapService client for version 1.3.0"""

    crs_qp = "CRS"
    get_map_operation_name = "GetMap"
    get_feature_info_operation_name = "GetFeatureInfo"
