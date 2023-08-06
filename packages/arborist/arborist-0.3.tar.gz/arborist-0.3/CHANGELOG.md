# Changelog

## [0.3] - 2019-04-04

### Changed

* Changed the data structure returned by `extract_metadata.get_metadata` to be a nested dictionary
* Changed the modelling of electricity in `electricity_grid`.

## [0.2] - 2019-04-04

### Added

* Common functions to write generic graphs, and graph `Dataset` sections (in `graph_common.py`)
* Several new metadata sections, such as climate change and elementary flow lists

### Changed

Rewrote all metadata processing to improve consistency and use common functions

### Fixed

* Lack of `Dataset` sections
* Typos and inconsistent approaches

## [0.1] - 2019-03-29

Initial release
