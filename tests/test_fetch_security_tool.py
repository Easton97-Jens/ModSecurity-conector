from __future__ import annotations

import importlib.util
import io
import sys
import tarfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "tools" / "fetch_security_tool.py"


def load_module():
    spec = importlib.util.spec_from_file_location("fetch_security_tool", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


fetcher = load_module()


class FetchSecurityToolTest(unittest.TestCase):
    def test_loads_verified_binary_records(self):
        expected = {
            "actionlint": ("rhysd", "actionlint", "actionlint"),
            "zizmor": ("zizmorcore", "zizmor", "zizmor"),
            "gitleaks_cli": ("gitleaks", "gitleaks", "gitleaks"),
        }

        for name, (owner, repository, executable) in expected.items():
            with self.subTest(tool=name):
                record = fetcher.load_record(fetcher.DEFAULT_MANIFEST, name)
                self.assertEqual(record["integration"], "downloaded_binary")
                self.assertEqual(record["upstream"]["owner"], owner)
                self.assertEqual(record["upstream"]["repository"], repository)
                self.assertEqual(record["checksum"]["executable"], executable)
                self.assertEqual(len(record["checksum"]["sha256"]), 64)

    def test_rejects_unknown_or_non_binary_tools(self):
        with self.assertRaisesRegex(ValueError, "unknown security tool"):
            fetcher.load_record(fetcher.DEFAULT_MANIFEST, "not_a_tool")
        with self.assertRaisesRegex(ValueError, "not a downloaded binary"):
            fetcher.load_record(fetcher.DEFAULT_MANIFEST, "gitleaks_action")

    def test_validate_only_does_not_require_a_destination(self):
        output = io.StringIO()
        with patch.object(
            sys,
            "argv",
            ["fetch_security_tool.py", "--tool", "actionlint", "--validate-only"],
        ):
            with redirect_stdout(output):
                self.assertIsNone(fetcher.main())
        self.assertEqual(output.getvalue(), "actionlint: manifest metadata valid\n")

    def test_recognizes_only_simple_top_level_tool_headers(self):
        self.assertTrue(fetcher.is_tool_header("  gitleaks_cli:"))
        self.assertFalse(fetcher.is_tool_header("gitleaks_cli:"))
        self.assertFalse(fetcher.is_tool_header("  gitleaks-cli:"))
        self.assertFalse(fetcher.is_tool_header("  gitleaks_cli: value"))
        self.assertFalse(fetcher.is_tool_header("  :"))

    def test_safe_member_rejects_archive_traversal(self):
        safe = tarfile.TarInfo("release/actionlint")
        safe.type = tarfile.REGTYPE
        parent = tarfile.TarInfo("../actionlint")
        parent.type = tarfile.REGTYPE
        absolute = tarfile.TarInfo("/actionlint")
        absolute.type = tarfile.REGTYPE

        self.assertTrue(fetcher.safe_member(safe))
        self.assertFalse(fetcher.safe_member(parent))
        self.assertFalse(fetcher.safe_member(absolute))


if __name__ == "__main__":
    unittest.main()
