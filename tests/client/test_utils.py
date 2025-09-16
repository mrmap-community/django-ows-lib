from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase
from requests import Session

from ows_lib.client.utils import get_client
from ows_lib.client.wms.wms111 import WebMapService as WMS111
from ows_lib.xml_mapper.capabilities.mixins import OGCServiceMixin


# Dummy-Service wie zuvor
class DummyService(OGCServiceMixin):
    def __init__(self, name: str, version: str):
        class StubType:
            def __init__(self, name, version):
                self.name = name
                self.version = version
        self.service_type = StubType(name, version)


class GetClientMockedTests(SimpleTestCase):

    @patch.object(WMS111, "send_request")
    def test_get_client_from_url_mocked(self, mock_send):
        # Mock-Response konfigurieren
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/xml"}
        mock_response.content = b"<xml>mocked capabilities</xml>"
        mock_send.return_value = mock_response

        url = "http://example.com?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities"

        client = get_client(url, session=Session())

        # Prüfen, dass send_request aufgerufen wurde
        mock_send.assert_called_once()
        self.assertIsInstance(client, WMS111)

    @patch.object(WMS111, "send_request")
    def test_get_client_from_url_mocked_fail(self, mock_send):
        # Mock-Response simuliert Fehler
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.headers = {"content-type": "text/html"}
        mock_response.content = b"error"
        mock_send.return_value = mock_response

        url = "http://example.com?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities"

        from ows_lib.client.exceptions import InitialError

        with self.assertRaises(InitialError) as cm:
            get_client(url, session=Session())

        mock_send.assert_called_once()
        self.assertIn(
            "client could not be initialized by the given url", str(cm.exception))
        mock_send.assert_called_once()
        self.assertIn(
            "client could not be initialized by the given url", str(cm.exception))
