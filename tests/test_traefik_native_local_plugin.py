from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "connectors" / "traefik" / "native_middleware"


class TraefikNativeLocalPluginTest(unittest.TestCase):
    def test_local_plugin_package_matches_module_suffix(self) -> None:
        module = re.search(
            r"(?m)^module\s+([^\s]+)\s*$",
            (PLUGIN / "go.mod").read_text(encoding="utf-8"),
        )
        package = re.search(
            r"(?m)^package\s+([A-Za-z_][A-Za-z0-9_]*)\s*$",
            (PLUGIN / "middleware.go").read_text(encoding="utf-8"),
        )
        self.assertIsNotNone(module)
        self.assertIsNotNone(package)
        assert module is not None
        assert package is not None
        self.assertEqual(module.group(1).rsplit("/", 1)[-1], package.group(1))

    def test_native_host_runner_stages_plugin_and_refuses_promotion(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "scripts" / "runtime_native_smoke.py"
        ).read_text(encoding="utf-8")
        self.assertIn('"plugins-local/src"', source)
        self.assertIn('"rule_evaluation": "not_wired"', source)
        self.assertIn('"capability_promotion": "not_permitted"', source)
        self.assertIn('"integration_mode": "native-traefik-middleware"', source)
        self.assertIn('rule: "PathPrefix(`/`)"', source)


if __name__ == "__main__":
    unittest.main()
