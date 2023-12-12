Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[v0.12.4] - 2023-12-12
---------------------

Fixed
~~~~~

* TypeError: cannot unpack non-iterable NoneType object in `_parse_ref_system` method.


[v0.12.3] - 2023-12-12
---------------------

Fixed
~~~~~

* added missing gmx namespace to `ReferenceSystem` mapper



[v0.12.2] - 2023-12-11
---------------------

Fixed
~~~~~

* None value check for floating values in bbox parser



[v0.12.1] - 2023-12-04
---------------------

Changed
~~~~~~~

* removed maximum version dependency requirements in setup.py


[v0.12.0] - 2023-11-30
---------------------

Changed
~~~~~~~

* renamed `dataset_id` and `dataset_id_code_space` to `code` and `code_space` and use it for service metadata mapper too


[v0.11.3] - 2023-11-22
---------------------

Fixed
~~~~~

* removes `dataset_id` and `dataset_id_code_space` from service metadata mapper



[v0.11.2] - 2023-11-22
---------------------

Fixed
~~~~~

* reference system parsing for `gmx:Anchor` elements


[v0.11.1] - 2023-11-22
---------------------

Fixed
~~~~~

* missing `title` and `abstract` property on iso metadata mapper.
* iso service metadata mapper


[v0.11.0] - 2023-11-21
---------------------

Added
~~~~~

* implement Acknowledgment mapper.
* add implementation to convert `GetRecords` and `GetRecordById` requests by http get method to postable xml object provided by the `xml_request` property of the ogc_request model.


[v0.10.0] - 2023-11-14
---------------------

Added
~~~~~

* Add support post request handling for csw 2.0.2, containing filter handling.


[v0.9.2] - 2023-11-9
---------------------

Fixed
~~~~~

* fixes `transform_to_model` for `ReferenceSystem` mapper for iso metadata records


[v0.9.1] - 2023-11-9
---------------------

Fixed
~~~~~

* fixes `ReferenceSystem` mapper for iso metadata records


[v0.9.0] - 2023-11-8
---------------------

Added
~~~~~

* keyword property on iso metadata mapper

[v0.8.1] - 2023-11-7
---------------------

Fixed
~~~~~

* fixes csw mapper and test cases which are not running


[v0.8.0] - 2023-11-2
---------------------

Added
~~~~~

* attributes to `GetRecordsResponse` mapper



[v0.7.1] - 2023-10-26
---------------------

Fixed
~~~~~

* wrong usage of `len` function inside `get_constraint`


[v0.7.0] - 2023-10-26
---------------------

Changed
~~~~~~~

* `get_constraint` function of csw client now supports multiple `record_types`. Now it is possible to filter by multiple type_names.


[v0.6.0] - 2023-10-24
---------------------

Added
~~~~~
* on `ogc_request` model:
    #. `filter_constraint` function to get a django filter from `csw constraint`
    #. `is_csw` property
    #. `is_get_records_request` property
    #. `is_describe_record_request` property
    #. `is_get_record_by_id_request` property


[v0.5.4] - 2023-10-05
---------------------

Fixed
~~~~~

* Inheritance order of `mixins` which calls `transform_to_model`. Customized `transform_to_model` function of mixins was not called cause of the inheritance order.



[v0.5.3] - 2023-09-15
---------------------

Fixed
~~~~~

* remove `super().transform_to_model()` call from `TimeExtent` helper object


[v0.5.2] - 2023-09-15
---------------------

Fixed
~~~~~

* return type `spatial_res_type` and `spatial_res_value` was switched


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