merge_ics
=========

A simple Python script to merge [RFC5545](https://tools.ietf.org/html/rfc5545) calendar files. It accepts several input calendars (referred to as *sources*) and processes them into one or more output calendar (*sinks*).

## Installation

```
pip install merge_ics
```

## Usage

```
merge_ics <config_file>
```

## Config file format

`merge_ics` reads configuration from YAML files passed through the command line as above. These YAML files should contain two nodes:
- `sources` specifies the input calendars, and
- `sinks` describes the calendars that should be outputted by the script.

#### `sources`

The `sources` node should contain a mapping whose keys are arbitrary identifiers for the input calendars. The values should again be mappings, with the possible keys being `filename` and `url`. The value for `filename` should describe a local ics file, while that for `url` should point to a remote one. The presence of both keys will result in `merge_ics` trying to read and parse the local copy, downloading the remote copy only in case of error.

#### `sinks`

The `sinks` node should contain a collection, each of which is a descriptor for an output calendar. These sink descriptors should contain three keys:

- `filename`: the filename where to write the calendar.
- `sources`: a mapping with keys being the arbitrary identifiers of the sources that you want to merge. The events from each of these source calendars will be given the corresponding values in a `CATEGORIES` prop.
- `options`: a mapping of calendar-level props. Make sure to always include `version` and `prodid` (otherwise the resulting ics file will be non-conformant).

### Example

```
sources:
  1:
    filename: https://example.com/cal_local.ics
  online_cal:
    url: https://example.com/cal_online.ics
  2:
    filename: cal2.ics
    url: https://example.com/cal2.ics
sinks:
  -
    filename: output_cal1.ics
    sources:
      1: Local Events
    options:
      prodid: -//Owner//LocalEvents//EN
      x-wr-calname: Local Events
      x-wr-caldesc: Events from my local calendar
      calscale: GREGORIAN
      method: PUBLISH
      x-published-ttl: PT15M
  -
    filename: output_cal123.ics
    sources:
      1: Local Events
      online_cal: Online Events
      2: Another Category
    options:
      prodid: -//Owner//Merged//EN
      x-wr-calname: Merged Calendar
      x-wr-caldesc: All my events
      calscale: GREGORIAN
      method: PUBLISH
      x-published-ttl: PT15M
```

## License

MIT
