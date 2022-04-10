# @jetblack/tzdata

This contains timezone data from IANA in JSON format.

## Installation

The resulting package can be installed from npmjs.

```bash
npm install --save @jetblack/tzdata
```

Alternatively individual files can be streamed from [jsdelivr](https://www.jsdelivr.com/).

## Usage

See [@jetblack/date](https://github.com/rob-blackbourn/jetblack-js-date)
for usage instructions.

## Data Formats

The data is provided in both a verbose and minified format.

### Verbose format

The verbose format presents the data as is from the IANA utilities. Each
line describes an offset from UTC for a given timezone. A line has the
following format.

* utc (ISO formatted date string): The date in UTC from which the offset applies,
* local (ISO formatted date string): The equivalent local date at this point in time,
* offset (ISO formatted duration string): The offset from UTC,
* abbr (string): The common abbreviation for the time zone,
* isDst (boolean): True if the offset includes a daylight savings adjustment.

### Minified format

Each line of minified data has the following format.

* u (number): The time in milliseconds since 1 Jan 1970 in UTC from which the offset applies,
* o (number): The offset in minutes,
* a (string): The common abbreviation for the time zone,
* d (number): 1 if the offset includes a daylight savings adjustment.
