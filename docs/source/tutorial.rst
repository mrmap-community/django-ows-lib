.. _tutorial:


Tutorial
========

Client
------

To communicate with an ogc service, first thing you need is a client. To initialize the client you need a capabilities document.

.. code-block:: python
    
    from pathlib import Path
    
    from ows_lib.xml_mapper.utils import get_parsed_service
    from ows_lib.client.utils import get_client 

    capabilities = get_parsed_service(Path("path/to/capabiliries.xml"))

    client = get_client(capabilities)

.. note::
    
    The utility function will automaticly detect the kind of service and the correct version of the service.
    Now you can use the default API's of the differend kind of services.


WebMapService
^^^^^^^^^^^^^

.. code-block:: python

    get_map_request = client.prepare_get_map_request(
        layers=["root"] ,
        styles=["root"] ,
        crs="EPSG:4326" ,
        bbox=(180, 90, 90, 180) ,
        width=600 ,
        height=400,
        format="image/png")

    response = client.send_request(get_map_request)