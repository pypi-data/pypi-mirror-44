Pydistance

> A library for visualizing the closest point to a set of points.

![Example Image](https://github.com/dang3r/pydistance/blob/master/example.png?raw=true)

## Getting started

Install the Python3 package

```shell
pip3 install pydistance
```

## Usage

```
$ pyd --help
Usage: pyd [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  distance  Dumb command to test the distance_matrix api
  enrich    Enrich the locations with lat, lng information
  plot      Plot all employee addresses and the best determined office...
```

First, location information must be augmented with the latitude and longitude of each. Create a file `addrs.txt` and enrich it usinfg
`pyd enrich`.

To plot the closest point, use `pyd plot`.

## License

MIT