from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors" / "envoy" / "harness" / "run_envoy_composite_matrix.sh"


class EnvoyCompositeReceiptContractTest(unittest.TestCase):
    def test_real_cases_bind_receipts_to_started_runtime_inputs(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")

        self.assertIn('"started_binary_artifacts": {"envoy": envoy, "composite": composite}', source)
        self.assertIn('event_artifact = artifact(event_log, "event JSONL", private=True)', source)
        self.assertIn('structural_artifact = artifact(structural, "structural event artifact", private=True)', source)
        self.assertIn('"event_log_artifact": event_artifact', source)
        self.assertIn('"structural_event_artifact_binding": structural_artifact', source)
        self.assertIn('"rendered_config_artifact": config_artifact', source)
        self.assertIn('"client_observation_artifact": probe_artifact', source)
        self.assertIn('"upstream_observation": upstream_artifact', source)
        self.assertIn('"causal_binding": "started_binary_config_client_upstream_artifacts" if upstream_artifact else "started_binary_config_client_no_upstream_request_observed"', source)
        self.assertIn('"upstream_observation_state": upstream_state', source)
        self.assertIn('upstream_observation_state=not_reached', source)
        self.assertIn('upstream_observation_state=request_started', source)
        self.assertIn('upstream_observation_state=response_observed', source)
        self.assertIn('"client_protocol": "HTTP/1.1"', source)
        self.assertIn('MAX_BINARY_BYTES = 512 * 1024 * 1024', source)
        self.assertIn('MAX_PRIVATE_BYTES = 16 * 1024 * 1024', source)
        self.assertIn('chunk = stream.read(1024 * 1024)', source)
        self.assertNotIn('hashlib.sha256(path.read_bytes())', source)
        self.assertIn('stat.S_IMODE(info.st_mode) & 0o77', source)
        self.assertIn('runtime_root = pathlib.Path(runtime_root_text).resolve(strict=True)', source)
        self.assertIn('path.resolve(strict=True).relative_to(runtime_root)', source)
        self.assertIn('info.st_nlink != 1', source)
        self.assertIn('chmod 600 "$VERSION_OUTPUT" || fail "could not restrict Envoy version artifact"', source)
        self.assertIn('PROJECTION_WRITER="$SCRIPT_DIR/write_composite_verifier_projection.py"', source)
        self.assertIn('verifier_case_supported()', source)
        self.assertIn('envoy_response_metadata_omitted', source)
        self.assertIn('run_case p3_redirect P3 GET /vector/p3-redirect', source)
        self.assertIn('headers.append(("X-Msconnector-Vector", "msconnector-p3-redirect"))', source)
        self.assertIn('--require-response-header "Location: $P3_REDIRECT_TARGET"', source)
        self.assertIn('[ "$observed_status" = 302 ] || fail "P3 redirect status was not 302"', source)
        self.assertIn('"redirect_location_verified": False', source)
        self.assertIn('wait_for_event_phase "$case_event_log" terminal timeout', source)
        run_case_source = source[source.index('run_case() {'):source.index('run_follow_up_case() {')]
        self.assertLess(
            run_case_source.index('wait_for_event_phase "$case_event_log" terminal timeout'),
            run_case_source.index('cleanup || fail "bounded cleanup failed for case $case_id"'),
        )
        self.assertIn('maximum_bytes = 256 * 1024', source)
        self.assertIn('maximum_line_bytes = 16 * 1024', source)
        self.assertIn('os.O_RDONLY | no_follow', source)
        self.assertIn('MAX_EVENT_LOG_BYTES = 256 * 1024', source)
        self.assertIn('check_client_probe "$case_probe"', source)
        self.assertIn('upstream-request-observation.json', source)
        self.assertIn('upstream-response-observation.json', source)
        self.assertIn('--upstream-request-observation "$case_upstream_request_observation"', source)
        self.assertIn('--upstream-response-observation "$case_upstream_response_observation"', source)
        self.assertIn('case_verifier_status=LIFECYCLE_ONLY', source)
        self.assertIn('"shared_verifier_manifest_artifact": verifier_manifest_artifact', source)
        self.assertIn('"shared_verifier_summary_artifact": verifier_summary_artifact', source)
        self.assertIn('"shared_verifier_status": verifier_status', source)

    def test_structural_verifier_status_and_payload_free_contract_remain_conservative(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")

        self.assertIn('"host_execution_status": "structural_input_only"', source)
        self.assertIn('"payloads_persisted": False', source)
        self.assertIn('"host_execution_evidence": "real_envoy_http1_client_observation"', source)
        self.assertIn('"verdict": "lifecycle_only_for_supported_cases_not_catalog_acceptance"', source)
        self.assertIn('"catalog_acceptance": False', source)
        self.assertIn('"p4_strict": "not_run_requires_client_visible_reset_or_abort_proof"', source)
        self.assertIn('"same_service_process_verified": True', source)
        self.assertNotIn('"same_service_process_start_token"', source)
        for forbidden in ("request_body", "response_body", "opaque_handle"):
            self.assertNotIn(f'"{forbidden}"', source)


if __name__ == "__main__":
    unittest.main()
