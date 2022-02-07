# Changelog
All notable changes (beginning at version 0.2.0) to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2022-02-07
### Added
- Implement latest method defintions.
- Upgrade to Python 3.7.x
- Concurrent parsing: up to 8 transcripts can be parsed in parallel.
### Changed
- All marked utterances are given utterance IDs, no longer use utterance numbers. Analysis now numbers utterance 1-N, where N is number of marked utterances.
- Phase out `python-ucto`, and by proxy `ucto` (through changes in `corpus2alpino`). Severly reduces dependency complexity.
### Removed
- Dropped Python 3.6.x support.
### Security
- Fixed multipe vulnerabilities in backend and frontend.

## [0.2.6] - 2021-12-17
### Changed
- Differentiate CHAT postcode markers by method. For STAP `[+ VU]` is marked, for all methods `[+ G]`

## [0.2.5] - 2021-11-12
### Added
- Process CHAT postcodes `[+ VU]` and `[+ G]` as utterance analysis markers
### Changed
- Updated VKL logo

## [0.2.4] - 2021-09-23
### Fixed
- Trailing whitespace in SIF headers is ignored

## [0.2.3] - 2021-09-23
### Changed
- Run pre-queries before core-queries

## [0.2.0] - 2021-09-10
### Added
- CHAT format input.
- Asynchronous parsing; the parse process continues in the background.
- Updates to query definitions and related SASTADEV functions.
- Automatic corrections on input files to improve parses of irregular language (implemented in SASTADEV).
- Logos for participating organisations.
### Changed
- Give corpora a method category, can only query and annotate using methods within this category.
- Updated look.
### Removed
- Remove 'Inform only' choice, the option is forcibly set to true.
### Fixed
- Asynchronous parsing ensures the application does not lock all users for the duration.
### Security
- Fix multiple vulnerabilities in both frontend and backend.
