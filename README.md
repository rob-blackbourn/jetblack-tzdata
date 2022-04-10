# jetblack-tzdata

A builder for timezone data.

This is work in progress.

## Overview

This is a re-implementation in Python of the JavaScript build scripts from
[moment-timezone](https://github.com/moment/moment-timezone)
for exporting IANA timezone data to JSON format.

## Installation

The resulting package can be installed from npmjs.

```bash
npm install --save @jetblack/tzdata
```

## Usage

See [@jetblack/date](https://github.com/rob-blackbourn/jetblack-js-date)
for usage instructions.

## Development

To build the package, first install it to a virtual environment with poetry. Then run `build-tzdata`.
This will create the packages in the `package` folder. The package can then
be published to npmjs.

Note: The version in `package/package.json` must be updated manually.

```bash
python3 -m venv .venv
. .venv/bin/activate
poetry install
build-tzdata --iana-version latest --iana-version 2022a --overwrite
cd package && npm publish --access public.
```
