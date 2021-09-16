# Changelog
All notable changes (beginning at version 0.2.0) to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2021-09-10
### Added
- CHAT format input.
- Asynchronous parsing. 
- Updates to query definitions and related SASTADEV functions.
- Automatic corrections on input files to improve parses of irregular language (implemented in SASTADEV).
- Logos for participating organisations.
### Changed
- Updated look.
### Removed
- Users can no longer toggle 'Inform only', the option is forcibly set to true.
### Fixed
- Asynchronous parsing ensures the application does not lock all users for the duration.
### Security
- Fix vulnerabilities in both frontend and backend.