# Changelog


## Next version
### Added
### Changed
- [DRF] Updated `DynamicViewset` code to work with DRF 3.12+
### Fixed
- [Core] Fixed various typos
- [Django] `DateCreatedField` and `DateUpdatedField` were respectively renamed `CreatedAtField` and `UpdatedAtField`
- [DRF] Replaced custom model field validator `length_validator` with `LengthValidator` to work properly
- [DRF] The `url_path` of an extra action will now be defaulted to its name if not provided
- [DRF] `ActionTestCase` now instantiates an API client in its `setUpClass`. The client defaults to `APIClient` and
can be overridden through the `client_class` attribute.


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
