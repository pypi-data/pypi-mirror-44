# Polt

Live data visualisation via Matplotlib

[![pipeline status](https://gitlab.com/nobodyinperson/python3-polt/badges/master/pipeline.svg)](https://gitlab.com/nobodyinperson/python3-polt/commits/master)
[![coverage report](https://gitlab.com/nobodyinperson/python3-polt/badges/master/coverage.svg)](https://nobodyinperson.gitlab.io/python3-polt/coverage-report/)
[![documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)](https://nobodyinperson.gitlab.io/python3-polt/)
[![PyPI](https://badge.fury.io/py/polt.svg)](https://badge.fury.io/py/polt)

`polt` is a Python package for live data visualisation via
[Matplotlib](https://matplotlib.org/).

## What can `polt` do?

### Reading Numbers from STDIN

```bash
polt generate -c walk --max-rate 20 | polt live
```

![polt-random-walk-stdin](https://gitlab.com/nobodyinperson/python3-polt/uploads/5b869729f3abc5a630c1fc2861c9a012/polt-live-random-walk.png)

### Reading CSV from STDIN

```bash
polt generate \
     -c "sensor1_temperature_celsius=uniform(20,25)" \
     -c "sensor1_pressure_hPa=uniform(990,1020)" \
     -c "sensor2_pressure_hPa=uniform(990,1020)" \
     -c "sensor3_humidity_percent=uniform(10,90)" \
     -c "sensor3_temperature_kelvin=uniform(0,300)" \
     --max-rate 5 \
     | polt \
         add-source -p csv -o name=Data -o header-regex=key-quantity-unit \
         live -o extrapolate=yes -o subplots-for=unit
```

![polt-csv-stdin](https://gitlab.com/nobodyinperson/python3-polt/uploads/2e6c1c25d6a828bff4c075dec980e6a2/polt-live-5-random-sensors-by-unit.png)

### Reading Live Data from Logfiles

Imagine you have a file `data.txt` where another process constantly writes
lines of numbers into. `polt` can then use the common `tail` program to watch
that data:

```bash
polt add-source -c "tail -fn0 data.txt" live
```

### Configuration Files

`polt` can use configuration files (by default `~/.config/polt/polt.conf` and
`.polt.conf` in the current directory) to simplify invocation. It is also
possible to read and save the current configuration with the `polt config`
command.

### Easy to Customize

It is easy to extend `polt` with your own data parsers, filters or animation
routines.  Check [the
documentation](https://nobodyinperson.gitlab.io/python3-polt/) for further
information.

## Why on Earth is it called `polt` and not `plot`!?

I am a big fan of swapping syllables or characters around resulting in
ridiculously-sounding words. `polt` is one of those words which I am generating
quite frequently when typing quickly.

## Installation

The `polt` package is best installed via `pip`. Run from anywhere:

```bash
python3 -m pip install --user polt
```

This downloads and installs the package from the [Python Package
Index](https://pypi.org).

You may also install `polt` from the repository root:

```bash
python3 -m pip install --user .
```

## Translations

Currently, the following languages are available:

- English
- German

If you are interested in adding another language, just [open a New Issue
](https://gitlab.com/nobodyinperson/python3-polt/issues/new) and we will get
you going.

## Documentation

Documentation of the `polt` package can be found [here on
GitLab](https://nobodyinperson.gitlab.io/python3-polt/).

Also, the command-line help page `polt -h` is your friend.
