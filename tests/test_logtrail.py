import json
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from logtrail import scan, parse_time, main

class LogtrailTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "events.jsonl"
        self.path.write_text("\n".join([
            json.dumps({"timestamp": "2026-01-01T10:00:00Z", "level": "INFO", "message": "Boot"}),
            json.dumps({"timestamp": "2026-01-02T10:00:00+00:00", "level": "ERROR", "message": "Disk full"}),
            "not-json",
        ]) + "\n")
    def tearDown(self):
        self.temp.cleanup()
    def test_filters(self):
        r = scan(self.path, level="error", contains="disk")
        self.assertEqual(r["matched"], 1)
        self.assertEqual(r["levels"], {"ERROR": 1, "INFO": 1})
    def test_since(self):
        r = scan(self.path, since=parse_time("2026-01-02T00:00:00Z"))
        self.assertEqual(r["matched"], 1)
    def test_limit(self):
        self.assertEqual(scan(self.path, limit=0)["matched"], 0)
    def test_bad_line(self):
        self.assertEqual(scan(self.path)["invalid_lines"][0]["line"], 3)
    def test_cli_json(self):
        output = StringIO()
        with redirect_stdout(output):
            code = main([str(self.path), "--json"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["matched"], 2)
    def test_naive_time(self):
        with self.assertRaises(ValueError):
            parse_time("2026-01-01T00:00:00")
if __name__ == "__main__":
    unittest.main()
