# Pydistance

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

To use, create a text file and run the plot command.

```bash
cat <<EOF
Toronto, Ontario, Canada
Palo Alto, California, USA
Mt. Everest, Nepal
Berlin, Germany
EOF > addrs.txt
pyd plot --adrs-file=addrs.txt
```


## License

MIT