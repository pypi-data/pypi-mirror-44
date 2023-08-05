# Arborist

Generate the URIs needed for the BONSAI knowledge graph

The RDF output directory has the following structure:

    activitytype
        lcia
    flowobject
        lcia
        us_epa
        exiobase3_3_17
    unit
    location
    foaf

The convention now is that each subdirectory has a `.ttl` file *and* and `.jsonld` file with the **same name** as the directory.

## Installation

Nothing special, use `pip` or `conda`.

## Contributing

All contributions should be via pull request, do not edit this package directly! We actually use it for stuff.
