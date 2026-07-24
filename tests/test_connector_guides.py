"""Regression tests for the controlled connector-guide renderer."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "generate_connector_guides.py"
EXPECTED_RENDER_SHA256 = "b98dae8bd83ebb0ee3f6694269b29d0ee1f97a26ec7aba8aaa054eac749d4728"


def load_generator() -> object:
    spec = importlib.util.spec_from_file_location("connector_guides_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load generator: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATOR = load_generator()


def render_digest() -> tuple[int, str]:
    digest = hashlib.sha256()
    count = 0
    for connector, data in GENERATOR.CONNECTORS.items():
        for kind in GENERATOR.DOCUMENT_KINDS:
            for german in (False, True):
                digest.update(f"{connector}\0{kind}\0{german}\0".encode("utf-8"))
                digest.update(GENERATOR.content(kind, connector, data, german).encode("utf-8"))
                count += 1
    return count, digest.hexdigest()


class ConnectorGuidesTests(unittest.TestCase):
    def test_all_rendered_guides_match_the_current_output_contract(self) -> None:
        count, digest = render_digest()

        self.assertEqual(count, 96)
        self.assertEqual(digest, EXPECTED_RENDER_SHA256)

    def test_main_writes_each_paired_guide_to_a_temporary_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            with mock.patch.object(GENERATOR, "ROOT", temporary_root):
                GENERATOR.main()

            guide_root = temporary_root / "docs" / "connectors"
            expected_paths = set()
            for connector, data in GENERATOR.CONNECTORS.items():
                for kind in GENERATOR.DOCUMENT_KINDS:
                    for german, suffix in ((False, ".md"), (True, ".de.md")):
                        path = guide_root / connector / f"{kind}{suffix}"
                        expected_paths.add(path)
                        self.assertEqual(
                            path.read_text(encoding="utf-8"),
                            GENERATOR.content(kind, connector, data, german),
                        )

            actual_paths = set(guide_root.rglob("*.md"))
            self.assertEqual(actual_paths, expected_paths)
            self.assertEqual(len(actual_paths), 96)


if __name__ == "__main__":
    unittest.main()
