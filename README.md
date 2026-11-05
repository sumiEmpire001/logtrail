# Logtrail

A lightweight, dependency-free Python CLI for inspecting newline-delimited JSON (JSONL) event logs.

## Features

- Filter events by severity, message substring, and ISO 8601 timestamp
- Count severity levels across all valid records
- Detect malformed lines with source line numbers
- Export JSON reports for further analysis
- Use exit codes 0 (all valid), 1 (malformed records), and 2 (bad arguments/file errors)

## Install

```bash
python -m pip install .
```

Or run `python logtrail.py --help` directly.

## Usage

```bash
logtrail examples/events.jsonl
logtrail examples/events.jsonl --level ERROR
logtrail examples/events.jsonl --since 2026-11-01T10:01:00Z --json
logtrail examples/events.jsonl --contains connection --limit 10
```

Each nonblank input line must be a JSON object with string fields `timestamp`, `level`, and `message`. Timestamps must be timezone-aware ISO 8601 strings. Unknown fields are retained in JSON output. Input files are never modified.

## Development

```bash
python -m unittest discover -s tests -v
python -m pip install build
python -m build
```

CI runs the tests and builds distributions on Linux and Windows with Python 3.9, 3.11, and 3.13.

## License

MIT.
