# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-10-2

### Fixed

- Removed leftover test code from v0.1.2.

## [0.1.2] - 2026-10-1

### Removed

- **Range**: Removed 7 logically redundant magic methods, including `__radd__`.
- **Interval**: Removed 7 logically redundant magic methods, including `__radd__`.

### Fixed

- **Range**:
  - Fixed a documentation error in `range_add`.
  - Fixed comparison and display errors in `range_sub`.
  - Fixed an operator error in `__add__`.
  - Fixed a logic error in `__neg__`.
- **Interval**:
  - Fixed comparison and display errors in `interval_sub`.
  - Fixed a logic error in `__neg__`.

### Changed

- **Interval**:
  - Improved `__repr__`.
  - Optimized the conditional logic in arithmetic magic methods such as `__add__`, and simplified related code.
- **StrictFloat**:
  - Made the class hashable.
- **Miscellaneous**:
  - Improved the `private` decorator in `_PackageTools`.

## [0.1.1] - 2026-9-20

### Added

- Added project URLs to `pyproject.toml`.

### Changed

- Optimized code.

## [0.1.0] - 2026-9-18

### Added

- Initial release.