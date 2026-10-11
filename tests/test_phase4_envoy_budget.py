"""Isolated Envoy budget tests using actual Go functions and stdlib only.

This is not a gRPC/CGo/libModSecurity or hosted Envoy integration test.
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

from tests.c_source_contract import matching_delimiter

ROOT = Path(__file__).resolve().parents[1]
PROCESSOR = ROOT / "connectors/envoy/ext_proc/internal/processor"

def go_definition(source: str, name: str) -> str:
    pattern = rf"(?m)^func (?:\([^)\n]*\) )?{re.escape(name)}\("
    match = re.search(pattern, source)
    if match is None:
        raise AssertionError(f"Go function {name} not found")
    opening = source.index("{", match.start())
    return source[match.start():matching_delimiter(source, opening, "{", "}") + 1]

FIXTURE = """package processor
import "math"
type Direction string
const (
    DirectionRequest Direction = "request"
    DirectionResponse Direction = "response"
)
type Action string
const (ActionAllow Action = "allow"; ActionDeny Action = "deny")
type Decision struct { Action Action; Status int }
func allowDecision() Decision { return Decision{Action: ActionAllow} }
func payloadTooLargeDecision() Decision { return Decision{Action: ActionDeny} }
type Config struct {
    MaxBodyChunkBytes int
    MaxRequestBodyBytes int64
}
type Summary struct { RequestBodyBytes int64; ResponseBodyBytes int64 }
type streamState struct { config Config; engine any; summary Summary }
type PassthroughEngine struct{}
type CommonRuntimeEngine struct { phase4Mode int }
const (
    commonRuntimePhase4ModeOff = 0
    commonRuntimePhase4ModeSafe = 1
    commonRuntimePhase4ModeStrict = 2
)
"""

class EnvoyPhase4BudgetTests(unittest.TestCase):
    def test_processor_disables_legacy_response_budget_without_removing_chunk_limit(self) -> None:
        source = (PROCESSOR / "processor.go").read_text(encoding="utf-8")
        function = go_definition(source, "bodyLimitDecision")
        self.assertNotIn("Phase4BodyBudgetDisabler", source)
        self.assertIn("direction == DirectionRequest && next > state.config.MaxRequestBodyBytes", function)
        self.assertNotIn("math.MaxInt64", function)
        self.assertIn("cumulativeBodyBytes(current, bodyLength)", function)
        self.assertNotIn("LateActionPolicy", function)

    def test_compiled_mode_prechecks_and_loaded_engine_readback(self) -> None:
        go = shutil.which("go")
        if go is None:
            self.skipTest("Go toolchain unavailable")
        with tempfile.TemporaryDirectory(prefix="envoy-phase4-budget-") as directory:
            root = Path(directory)
            source = (PROCESSOR / "processor.go").read_text(encoding="utf-8")
            functions = "\n\n".join([
                go_definition(source, "bodyLimitDecision"),
                go_definition(source, "cumulativeBodyBytes"),
            ])
            (root / "budget.go").write_text(FIXTURE + functions, encoding="utf-8")
            (root / "budget_test.go").write_text(
                (PROCESSOR / "phase4_budget_test.go").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update({
                "GO111MODULE": "off", "GOTOOLCHAIN": "local",
                "GOPROXY": "off", "GOSUMDB": "off", "GOENV": "off",
            })
            # Honor an existing external cache root; never cache in the checkout.
            environment.setdefault("GOCACHE", str(root / "go-cache"))
            result = subprocess.run(
                [go, "test", "-count=1", "-v", "."], cwd=root,
                env=environment, capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

if __name__ == "__main__":
    unittest.main()
