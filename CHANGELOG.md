# Changelog


## [v3.1.0] - XXXX-XX-XX
### Added
- [Django] Added `assert_logs` decorator to apply the `self.assertLogs` context to an entire test case
- [DRF] New `ImprovedRouter` which provides the new model route `bulk_destroy`

### Changed
- [Django] `DateCreatedField` and `DateUpdatedField` were respectively renamed `CreatedAtField` and `UpdatedAtField`
- [DRF] **ViewSets**:
    - Added `BulkDestroyMixin` to provide the `bulk_destroy` action to your viewset
    - `DynamicViewSet` and `DynamicModelViewSet` have been replace with `ImprovedViewSet` and `ImprovedModelViewSet`
    - They allow you to have 1 serializer/action, and have 3 level of permissions: app-wide, viewset-wide, and per action
- [DRF] **Serializers**:
    - New shortcuts for serializer fields attributes: `required_list, optional, optional_list`
    - New mixins to prevent actions in ModelSerializers: `NoCreateMixin`, `NoUpdateMixin`
    - Added methods `required_fields` and `check_is_not_empty` to `ImprovedSerializer`
- [DRF] **TestCases**:
    - `ImprovedTestCase`
        - Uses `get_user_model` rather than the default `User` model
        - `assert_email_was_sent` now takes more arguments for more flexibility
    - `ActionTestCase`
        - More properties: `api_client_class`, `url_template`, `http_method_name`, `success_code`, `payload`
        - Removed old properties: `client_class`, `service_base_url`, `service_extra_url`
        - `client` has become `api_client`
        - Removed method `assert_field_has_error`
        - Replaced `detail_url`, `detail_url_with_params`, `service_url_with_params` methods with a single `url` method
        - New method `assert_admin_permissions`
    - `ModelTestCase`
        - Removed method `assert_fields_are_required`
- [DRF] **Permissions**:
    - `IsVerified` and `IsNotVerified` permissions have been removed
    
### Fixed
- [Core] Fixed various typos
- [DRF] Replaced custom model field validator `length_validator` with `LengthValidator` to work properly
- [DRF] The `url_path` of an extra action will now be defaulted to its name if not provided
- [DRF] Custom `action` without the `detail` property will have their permissions fail automatically
- [DRF] Fixed `IdListSerializer` serializer to make its only field required



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
