from abc import ABC

from requests import Request, Response, Session

from ows_lib.client.exceptions import InitialError
from ows_lib.client.utils import update_queryparams
from ows_lib.models.ogc_request import OGCRequest
from ows_lib.xml_mapper.capabilities.mixins import OGCServiceMixin
from ows_lib.xml_mapper.utils import get_parsed_service


class OgcClient(ABC):
    """Abstract OgcClient class which implements some basic functionality for all ogc client applications

    :param capabilities: The capabilities document to initialize the client
    :type capabilities: OGCServiceMixin | str

    :param session: The session object that shall be used
    :type session: requests.Session, optional
    """
    capabilities: OGCServiceMixin

    def __init__(
            self,
            capabilities,
            session: Session = Session(),
            *args,
            **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session

        if isinstance(capabilities, OGCServiceMixin):
            self.capabilities = capabilities
        elif capabilities is str and "?" in capabilities:
            # client was initialized with an url
            response = self.send_request(
                request=Request(method="GET", url=capabilities))
            if response.status_code <= 202 and "xml" in response.headers["content-type"]:
                self.capabilities = get_parsed_service(response.content)
            else:
                raise InitialError(
                    f"client could not be initialized by the given url: {capabilities}. Response status code: {response.status_code}")

    def send_request(self, request: OGCRequest, timeout: int = 10) -> Response:
        """Sends a given request with internal session object.

        :param request: A request object that shall be sended
        :type request: requests.Request

        :param timeout: The time value for maximium waiting time of the response.
        :type int:

        :return: Returns the response of the given request
        :rtype: requests.Response

        """
        return self.session.send(request=request.prepare(), timeout=timeout)

    def get_capabilitites_request(self) -> OGCRequest:
        """Constructs a basic GetCapabilities request to use for requesting

        :return: A valid GetCapabilitites request
        :rtype: requests.Request
        """
        params = {
            "VERSION": self.capabilities.service_type.version,
            "REQUEST": "GetCapabilities",
            "SERVICE": self.capabilities.service_type.name
        }

        url = update_queryparams(
            url=self.capabilities.get_operation_url_by_name_and_method(
                "GetCapabilities", "Get").url,
            params=params)

        return OGCRequest(method="Get", url=url)
