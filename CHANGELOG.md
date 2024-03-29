# Changelog

All notable changes to this project will be documented in this file.<br>
(**Note:** The format is mostly based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/))

**Format:** `[x.y.z] - mm/dd/yyyy`
<hr>

## [1.2.1] - 06/27/2023
### Added
- Added an OS filter. If the OS is not Windows, returns a warning
- Users now can clear the encrypted message and token results by right-clicking on it
### Changed
- The setting window and the theme editor can only be opened once
- Saving the theme without auto-restart will close the setting window
- Copying an empty message or token will result in a warning
### Fixed
- Fixed the looped set appending to prevent the code from being overloaded because it's too large

## [1.2.0] - 06/27/2023
### Added
- Added a setting window
### Changed
- Appearance mode, theme, etc are now stored and saved in files
- The "brand" attributes now display slightly faster

## [1.1.1] - 06/19/2023
### Fixed
- Fixed `AttributeError` and `_tkinter.TclError`. If those errors are raised again, the application won't be affected

## [1.1.0] - 06/18/2023
### Added
- Added 2 more "brand" attributes
- Added a switch mode button at the main hub to switch the appearance mode (e.g light, dark)
### Changed
- Slightly modified the redirect-to-the-main-hub message whenever the application is closed

## [1.0.0] - 06/18/2023
### Added
- Uploaded the whole application code

<hr>

# ToDo List
- Add base64 encryption and decryption
- Create a fully completed wiki
