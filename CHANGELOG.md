# Changelog

## [v5.0.0] - 2024-02-18

- [dev] Updated linters and pre-commits
- [dj] Replaced `NoBulkManager` with `ImprovedManager` which provides more flexibility
  - Can use `ImprovedManager(allow_bulk=False)` to disable bulk operations
- [dj] Added `generate_json_streaming_content` to `ImprovedViewSet` to stream JSON response
  - Added `parse_streaming_response` in test utils to handle streaming responses in unittests
  - Updated `APITestCase.build_url` to use the endpoint's name like `reverse` and also handle query params

### Breaking changes
- [dj] Removed `LifeCycleAbstractModel`

---

## [v4.0.0] - 2023-03-07
- Update local development configuration (pre-commits, requirements, etc.)
- Removal of most packages, and kept only **std** and **django_utils**
- Renamed **django_utils** package as **dj**
- Added new functions in both **dj** and **std** packages

---

## [v3.2.2] - 2022-11-08
### Added
N/A

### Changed
- [Django] Emails now have a default subject which can be overriden when calling `Email.send`

### Fixed
- [Django] Fixed emails not being sent when using the `cc` and `to` parameters

### Removed
- [Django] Removed the `commands` and the `operations` utilities

---

## [v3.2.1] - 2022-10-14
### Added
- [Core] For local development, added multiple libraries in the `requirements.txt` file

### Changed
N/A

### Fixed
- [Django] Fixed multiple incorrect imports

### Removed
- [Django] Removed the `assertImageToBase64` from the `ImprovedTestCase`

---

## [v3.2.0] - 2022-10-07
### Added
- [Django] Added `FileNameWithUUID` to generate unique names for `FileField` and `ImageField` fields
- [Django] Added `maybe_resize_image`, `image_to_base64`, and `resized_image_to_base64` image utils
- [Django] Added `update_model` and `update_m2m` utils to easily update models and relations
- [Django] Added `test_runner` module which provides custom test runners
- [DRF] Added `ReadOnlyModelSerializer` which removes create and update methods
- [DRF] Added `storage` module which provides utility for interacting with local storage and downloading files

### Changed
- [Django] Remove emails utils and added a `Email` class with similar utils
- [Django] Updated `NoBulkManager` to also exclude `bulk_update`
- [Django] `ImprovedTestCase` now has many more available assertions
- [DRF] `ActionTestCase` now has many more available assertions and utilities, including multipart api calls
- [DRF] No longer raises an error when no serializer is found by `ImprovedViewSet.get_serializer_class`

### Fixed
- [Core] Fixed various docstrings and typing issues.

### Removed
- [Django] Database function fields have been removed
- [Django] Removed `get_image_dimensions` and `image_as_html` image utils
- [Django] Removed `IntChoiceEnum` as it was redundant with django `IntChoices`
- [Django] Removed `filter_on_text` and `single_sort_by` query utils
- [Django] Remove the `ModelTestCase` class as it brought little to the table
- [DRF] Removed `UserPermissionMixin`, `IsAdminOrOwner`, `IsObjectOwner`, and `IsSuperUser` custom permissions
- [DRF] Removed all existing serializers utilities
- [DRF] `BulkDestroyMixin` has been removed

---

## [v3.1.0] - 2022-04-11
### Added
- [Core] Added typing for all functions and remove unnecessary docstrings
- [Django] Added `assert_logs` decorator to apply the `self.assertLogs` context to an entire test case
- [DRF] New `ImprovedRouter` which provides the new model route `bulk_destroy`

### Changed
- [Django] The django package has been renamed `django_utils` to avoid name conflict with the actual django lib
- [Django] `DateCreatedField` and `DateUpdatedField` were respectively renamed `CreatedAtField` and `UpdatedAtField`
- [Django] Added the `IntChoiceEnum` class to make integer choice fields easier to create (for models)
- [DRF] **ViewSets**:
    - Added `BulkDestroyMixin` to provide the `bulk_destroy` action to your viewset
    - `DynamicViewSet` and `DynamicModelViewSet` have been removed from the lib
    - As a result, also removed the `ActionHandler` custom class and `SerializerMode` Enum, as they are not longer useful  
    - Added two new viewsets: `ImprovedViewSet` and `ImprovedModelViewSet`
        - They allow you to have 1 serializer/permission per action (or fallback to a default) 
- [DRF] **Serializers**:
    - New shortcuts for serializer fields attributes: `required_list, optional, optional_list`
    - New mixins to prevent actions in ModelSerializers: `NoCreateMixin`, `NoUpdateMixin`
    - Added methods `required_fields` and `check_is_not_empty` to `ImprovedSerializer`
- [DRF] **TestCases**:
    - `ImprovedTestCase`
        - `assert_email_was_sent` now takes more arguments for more flexibility
        - No longer provide tools to create user or random data. Use your own Factories instead.
        - Added `upload_file` function to easily upload files from an existing files
    - `ActionTestCase`
        - No longer provide tools to create user or random data. Use your own Factories instead.
        - Added properties: `api_client_class`, `url_template`, `http_method_name`, `success_code`, `payload`
        - Removed old properties: `client_class`, `service_base_url`, `service_extra_url`
        - `client` has become `api_client`
        - Removed method `assert_field_has_error`
        - Replaced `detail_url`, `detail_url_with_params`, `service_url_with_params` methods with a single `url` method
    - `ModelTestCase`
        - Removed methods `assert_fields_are_required` and `common_errors`

    
### Fixed
- [Core] Fixed various typos
- [Django] Fixed `emails.extract_email_addresses` that did not take into account the `sep` arg
- [Django] Fixed `emails.send_html_email` that did not take into account the `sep` arg
- [DRF] Replaced custom model field validator `length_validator` with `LengthValidator` to work properly
- [DRF] The `url_path` of an extra action will now be defaulted to its name if not provided
- [DRF] Custom `action` without the `detail` property will have their permissions fail automatically
- [DRF] Fixed `IdListSerializer` serializer to make its only field required

### Removed
- [Django] Removed the `ModelWithImage` custom class 
- [DRF] IsVerified` and `IsNotVerified` permissions have been removed
- [Web] Removed the `selenium.py` utils

---

## [v3.0.0] - 2020-12-21
### Added
- [Core] Implemented Github action for auto-publish on release
- [Django] New `ImprovedCommand` class to create custom commands and use our new `Operation` class
- [Django] New `Operation` and `OperationTask` classes to better handle your `manage.py` commands
- [Django] New `ModelTestCase` class that provides utility when testing models
- [DRF] Added **major feature** with our custom viewsets, where you can register actions through dicts
- [DRF] New `ActionHandler` in charge of handling your service/endpoint logic (rather than having it in the viewset)
- [DRF] New `ActionTestCase` class that provides utility for testing your action handlers
- [DRF] Added several ready-to-go action handlers
- [DRF] Added various improved permission classes
- [DRF] Added various improved serializer classes

### Changed
- [Core] Better docstrings with reStructedText
- [Core] Changed the project tree arborescence

### Fixed
- [Core] Various fixes that I forgot to keep track of

### Removed
N/A
