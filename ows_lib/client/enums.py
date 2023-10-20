from enum import Enum


class OGCServiceEnum(Enum):
    """ Defines all supported service types

    """
    ALL = "all"
    WMS = "wms"
    WFS = "wfs"
    WMC = "wmc"
    DATASET = "dataset"
    CSW = "csw"


class OGCOperationEnum(Enum):
    """ Defines all known operation names

    """
    # ALL
    GET_CAPABILITIES = "GetCapabilities"

    # WMS
    GET_MAP = "GetMap"
    GET_FEATURE_INFO = "GetFeatureInfo"
    DESCRIBE_LAYER = "DescribeLayer"
    GET_LEGEND_GRAPHIC = "GetLegendGraphic"
    GET_STYLES = "GetStyles"
    PUT_STYLES = "PutStyles"

    # WFS
    GET_FEATURE = "GetFeature"
    TRANSACTION = "Transaction"
    LOCK_FEATURE = "LockFeature"
    DESCRIBE_FEATURE_TYPE = "DescribeFeatureType"
    GET_FEATURE_WITH_LOCK = "GetFeatureWithLock"
    GET_GML_OBJECT = "GetGmlObject"
    LIST_STORED_QUERIES = "ListStoredQueries"
    GET_PROPERTY_VALUE = "GetPropertyValue"
    DESCRIBE_STORED_QUERIES = "DescribeStoredQueries"

    # CSW
    GET_RECORDS = "GetRecords"
    DESCRIBE_RECORD = "DescribeRecord"
    GET_DOMAIN = "GetDomain"
    GET_RECORD_BY_ID = "GetRecordById"
    HARVEST_RECORDS = "harvestRecords"
