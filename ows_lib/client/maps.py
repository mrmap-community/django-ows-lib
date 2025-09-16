# Mapping (service, version) -> Client-Klasse
from ows_lib.client.csw.csw202 import CatalogueService as CSW202
from ows_lib.client.enums import OGCServiceEnum
from ows_lib.client.wfs.wfs200 import WebFeatureService as WFS200
from ows_lib.client.wms.wms111 import WebMapService as WMS111
from ows_lib.client.wms.wms130 import WebMapService as WMS130

CLIENT_MAP: dict[tuple[OGCServiceEnum, str], type] = {
    (OGCServiceEnum.WMS, "1.1.1"): WMS111,
    (OGCServiceEnum.WMS, "1.3.0"): WMS130,
    (OGCServiceEnum.WFS, "2.0.0"): WFS200,
    (OGCServiceEnum.CSW, "2.0.2"): CSW202,
}
