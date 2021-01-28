# Changelog

## Next version
#### New
#### Improvements
- [DRF] Updated `DynamicViewset` code to work with DRF 3.12+
#### Fixes
- [Core] Fixed various typos
- [DRF] Replaced custom model field validator `length_validator` with `LengthValidator` to work properly


## v3.0.0
#### New
- Django commands and operations handler
- DRF new tools:
    - Custom viewset with action configs
    - Action handlers
    - Improved permission classes
    - Improved serializers
- TestCase classes for Django and DRF
- Added Github action for auto-publish on release
#### Improvements
- Better docstrings with reStructedText
- Changed the project tree arborescence
#### Fixes
- Various fixes
