from django.http import HttpResponse


class SemanticError(Exception):
    """Basic exception for errors raised by wrong semantic parsed content"""


class OGCServiceException(HttpResponse):
    status_code = 200
    message = None
    locator = None

    def __init__(self, ogc_request, message: str = None, locator: str = None, *args, **kwargs):
        if message:
            self.message = message
        if locator:
            self.locator = locator
        self.ogc_request = ogc_request
        super().__init__(content_type="application/xml",
                         content=self.get_exception_string(), *args, **kwargs)

    def __eq__(self, __value: object) -> bool:
        return self.status_code == __value.status_code and self.message == __value.message and self.locator == __value.locator

    def get_locator(self):
        return self.locator

    def get_locator_string(self):
        return f'locator="{self.get_locator()}"'

    def get_message(self):
        return self.message

    def get_exception_string(self):
        return \
            '<?xml version="1.0" encoding="UTF-8"?>'\
            f'<ServiceExceptionReport version="{self.ogc_request.service_version}" xmlns="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/ogc">'\
            f'<ServiceException code="{self.code}" {self.get_locator_string() if self.get_locator() else ""}>'\
            f'{self.get_message()}'\
            '</ServiceException>'\
            '</ServiceExceptionReport>'


class MissingParameterException(OGCServiceException):
    code = "MissingParameter"


class MissingRequestParameterException(MissingParameterException):
    locator = "request"
    message = "Could not determine request method from http request."


class MissingVersionParameterException(MissingParameterException):
    locator = "version"
    message = "Could not determine version for the requested service."


class MissingServiceParameterException(MissingParameterException):
    locator = "service"
    message = "Could not determine service for the requested service."


class MissingConstraintLanguageParameterException(MissingParameterException):
    locator = "CONSTRAINTLANGUAGE"
    message = "CONSTRAINTLANGUAGE parameter is missing."


class InvalidParameterValueException(OGCServiceException):
    code = "IvalidParameterValue"


class OperationNotSupportedException(OGCServiceException):
    code = "OperationNotSupported"
    message = "No such operation"

    def get_locator(self):
        query_parameters = {
            k.lower(): v for k, v in self.request.GET.items()}
        return query_parameters.get('request', None)

    def get_message(self):
        return f"No such operation: {self.get_locator()}"


class LayerNotDefined(OGCServiceException):
    code = "LayerNotDefined"
    message = "unknown layer"
    locator = "LAYERS"
