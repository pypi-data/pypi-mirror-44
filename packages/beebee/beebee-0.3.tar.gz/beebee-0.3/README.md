# beebee

Process BONSAI data sources for use in Brightway2 calculations.

Takes JSON-LD data following the [BONSAI ontology](https://github.com/BONSAMURAIS/ontology), and turns it into a Numpy [.npy](https://www.numpy.org/neps/nep-0001-npy-format.html) files that can be used directly by [Brightway2](https://brightwaylca.org/).

Can also take electricity data from the [bentso library](https://github.com/BONSAMURAIS/bentso) (which itself wraps [entsoe-py](https://github.com/EnergieID/entsoe-py) which wraps the [ENTSO-E API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html))

## Installation

`beebee` requires the following:

* arborist
* bentso
* docopt
* numpy

## Contributing

Please feel free to either file an issues or submit a pull request!
