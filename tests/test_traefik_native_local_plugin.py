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
        self.assertIn('"rule_evaluation": "host_runtime_observed_not_promoted"', source)
        self.assertNotIn('"rule_evaluation": "not_wired"', source)
        self.assertIn('"capability_promotion": "not_permitted"', source)
        self.assertIn('"integration_mode": "native-traefik-middleware"', source)
        self.assertIn('rule: "PathPrefix(`/`)"', source)

    def test_native_host_runner_uses_a_short_private_uds_root(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "scripts" / "runtime_native_smoke.py"
        ).read_text(encoding="utf-8")
        self.assertIn("tempfile.mkdtemp", source)
        self.assertIn('dir="/var/tmp"', source)
        self.assertIn("ENGINE_SOCKET_PATH_MAX_BYTES", source)
        self.assertIn("engine_socket_dir = create_private_engine_socket_dir()", source)
        self.assertIn("remove_private_engine_socket_dir(engine_socket_dir)", source)

    def test_engine_service_runtime_test_uses_a_short_private_uds_root(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "build" / "test-engine-service-runtime.sh"
        ).read_text(encoding="utf-8")
        self.assertIn("mktemp -d /var/tmp/msconnector-traefik-engine-test.XXXXXX", source)
        self.assertIn('SOCKET_PATH="$SOCKET_DIR/engine.sock"', source)
        self.assertIn('[ "${#SOCKET_PATH}" -le 100 ]', source)
        self.assertIn('rmdir "$SOCKET_DIR"', source)


if __name__ == "__main__":
    unittest.main()
