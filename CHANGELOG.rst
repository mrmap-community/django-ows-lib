Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[v0.5.1] - 2023-09-14
---------------------

Fixed
~~~~~

* remove `super().transform_to_model()` at `OperationUrl` object


[v0.5.0] - 2023-09-14
---------------------

Changed
~~~~~~~

* call `super().transform_to_model()` in all child objects to get the default `field_dict`

Added
~~~~~

* custom `transform_to_model` function on `MdMetadata` mapper to push in the collected values


[v0.4.2] - 2023-09-14
---------------------

Fixed
~~~~~

* removes specific xpath of `_hierachy_level` which depends on `codeList` attribute to collect the codeListValue anyway


[v0.4.1] - 2023-05-26
---------------------

Fixed
~~~~~

* Undefined namespace prefix on `md_metadata.file_identifer` attribute


[v0.4.0] - 2023-05-26
---------------------

Added
~~~~~

* implemented `from_django_request` classmethod for creating `OGCRequest` objects from django request objects.


[v0.3.0] - 2023-05-25
---------------------

Changed
~~~~~~~

* improves development documentation section
* `ogc_query_params` now can handle multi value queryparams and only returns ogc queryparams that are present with a value.

Removed 
~~~~~~~

* `params_lower` property from `OGCRequest` model.


[v0.2.0] - 2023-05-17
---------------------

Added
~~~~~

* test cases for testing iso metadada mapper

Changed
~~~~~~~

* refactors xml mapper for iso metadata to implement a better abstraction view on it 


[v0.1.2] - 2023-05-16
---------------------

Added
~~~~~

* test cases for `get_import_path_for_xml_mapper` function

Fixed
~~~~~

* fixes wrong version missmatching in `get_import_path_for_xml_mapper` function

[v0.1.1] - 2023-05-15
---------------------

Fixed
~~~~~

* pip install requirements by adding the requirements from .requirements/base.txt

[v0.1.0] - 2023-05-15
---------------------

Added
~~~~~

* client for wms v1.1.1, wfs v2.0.0, csw v2.0.2
* xml mapper classes for wms v1.1.1, wfs v2.0.0, csw v2.0.2 capabilities
* xml mapper classes for wfs v2.0.0 get feature request

[unreleased]: https://github.com/mrmap-community/django-ows-lib/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/mrmap-community/django-ows-lib/releases/tag/v0.1.2
[0.1.1]: https://github.com/mrmap-community/django-ows-lib/releases/tag/v0.1.1
[0.1.0]: https://github.com/mrmap-community/django-ows-lib/releases/tag/v0.1.0