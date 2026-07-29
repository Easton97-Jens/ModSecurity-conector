"""Regression contract for Apache smoke MIME configuration artifacts."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors" / "apache" / "harness" / "run_apache_smoke.sh"


class ApacheSmokeMimeTypesTests(unittest.TestCase):
    def test_harness_materializes_both_standard_mime_locations(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")
        setup = source.split(
            'if [ -f "$HTTPD_PREFIX/conf/mime.types" ]; then', 1
        )[1].split('if ! "$PYTHON_BIN" "$CASE_CLI" materialize', 1)[0]

        self.assertIn('MIME_TYPES_FILE="$RUNTIME_ROOT/conf/mime.types"', source)
        self.assertIn('MIME_TYPES_ROOT_FILE="$RUNTIME_ROOT/mime.types"', source)
        self.assertIn(
            'cp -a "$HTTPD_PREFIX/conf/mime.types" "$MIME_TYPES_FILE"', setup
        )
        self.assertIn(
            'cp -a "$HTTPD_PREFIX/conf/mime.types" "$MIME_TYPES_ROOT_FILE"', setup
        )
        self.assertIn(': > "$MIME_TYPES_FILE"', setup)
        self.assertIn(': > "$MIME_TYPES_ROOT_FILE"', setup)


if __name__ == "__main__":
    unittest.main()
