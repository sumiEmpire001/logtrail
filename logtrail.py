"""Filter JSON Lines event logs without modifying source data."""
from __future__ import annotations
import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)

def scan(path: Path, level: str | None = None, contains: str | None = None,
         since: datetime | None = None, limit: int | None = None) -> dict:
    matches = []
    counts = Counter()
    invalid = []
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError("event must be an object")
                timestamp = event.get("timestamp")
                severity = event.get("level")
                message = event.get("message")
                if not all(isinstance(x, str) for x in (timestamp, severity, message)):
                    raise ValueError("timestamp, level and message must be strings")
                when = parse_time(timestamp)
            except (json.JSONDecodeError, ValueError, TypeError) as exc:
                invalid.append({"line": line_no, "error": str(exc)})
                continue
            counts[severity.upper()] += 1
            if level and severity.casefold() != level.casefold():
                continue
            if contains and contains.casefold() not in message.casefold():
                continue
            if since and when < since:
                continue
            if limit is None or len(matches) < limit:
                matches.append({"line": line_no, **event})
    return {"matched": len(matches), "events": matches,
            "levels": dict(sorted(counts.items())), "invalid_lines": invalid}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Inspect JSONL event logs")
    parser.add_argument("file", type=Path)
    parser.add_argument("--level", help="Filter severity (case insensitive)")
    parser.add_argument("--contains", help="Filter message substring")
    parser.add_argument("--since", help="ISO 8601 timezone-aware minimum timestamp")
    parser.add_argument("--limit", type=int, help="Maximum matching events to return")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args(argv)
    try:
        if args.limit is not None and args.limit < 0:
            raise ValueError("--limit must be non-negative")
        since = parse_time(args.since) if args.since else None
        report = scan(args.file, args.level, args.contains, since, args.limit)
    except (OSError, ValueError) as exc:
        print(f"logtrail: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for event in report["events"]:
            print(f"{event['timestamp']} [{event['level']}] {event['message']}")
        print(f"Matched: {report['matched']} | Invalid lines: {len(report['invalid_lines'])}")
    return 1 if report["invalid_lines"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
