# I12 current host evidence

**Language:** English | [Deutsch](pr-382-i12-host-evidence-20261014.de.md)

Status: **I12_PARTIAL**. Final reconciliation.

1,484 immutable IDs: 1,406 required and 78 diagnostic. Actual host starts and bounded probes do not replace complete selected-case receipts.

PASS / FAIL (required): **36 / 0**. Status counts: {"NOT_EXECUTED_UNQUALIFIED": 1447, "PASS": 37}

Actual selected execution with complete or incomplete qualification: 122 / 1406 required; 8 / 78 diagnostic; 130 / 1484 total. Separately, only the sibling request parser executed; selected companion parser unproven: 3. Execution dispositions: {"ACTUAL_CANONICAL_YAML_HOST_CLIENT_EXECUTED_INCOMPLETE_LIFECYCLE_PACKET": 27, "ACTUAL_NATIVE_OPERATION_EXECUTED_INCOMPLETE_LIFECYCLE_PACKET": 40, "CATALOG_NATIVE_OVERRIDE_ORACLE_CONFLICT": 2, "CATALOG_PARSER_SCOPE_CONFLICT_ACCEPTS_CONFIG_SINK_OPENS_AT_RUNTIME": 1, "LITERAL_CATALOG_EXIT_MISMATCH_NO_NORMALIZATION": 22, "QUALIFIED_CONFIG_PARSER_ONLY": 37, "SHARED_REQUEST_RUNTIME_REJECTION_DOES_NOT_BIND_COMPANION_PARSER": 3, "SOURCE_HOST_HEADER_COALESCING_ORACLE_CONFLICT": 1}

## Identity

```json
{
  "current_code_ci": "Historical93b4023234b8b3340464f5424b6e4d44e5d5dfdf terminal26SUCCESS/2SKIP and authenticated Sonar strict-zero/A are separately retained. The new two-file Apache working delta requires fresh ordinary final delivery CI/Sonar, attested externally and in both PR bodies; no self-referential documentation SHA.",
  "current_uncommitted_delta": {
    "current_delivery_ci": "Previous93b4023234b8b3340464f5424b6e4d44e5d5dfdf checkpoint remains historical; the new harness/test delta requires fresh delivery CI after ordinary commit.",
    "executed_harness_sha256": "30fd539bc319b8583cb9cfb23db7bedaf58c894afd5fc88c50076a8250d0d437",
    "new_commit_sha": null,
    "owner": "Parent Apache test harness only",
    "path": "connectors/apache/harness/run_apache_smoke.sh",
    "product_source_changed": false,
    "selected_production_inputs_equal_to_parent_a9": 194
  },
  "documentation_delivery_head": "Recorded by external final attestation and PR body after normal commit; no self-referential SHA.",
  "evidence_source_head": "6b472cab6c18dfb5d6034461e1df5609e4ec3606",
  "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
  "hosted_source_base_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "mrts_executed": false,
  "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
  "product_parent_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808"
}
```

Build producer, hosted source and final evidence head remain separate identities. Scoped source equivalence never relabels binaries or historical runs.

| Leg | IDs | Readiness | Attempts |
| --- | ---: | --- | --- |
| apache-native | 155 | BOUNDED_HOST_OBSERVED | 1791962156241815212, 1791974271929607351, 1791974703385184818, 1791974869509186563, 1791975496308340489 |
| nginx-native | 140 | BOUNDED_HOST_OBSERVED | 1791958559271098737, 1791960903387896662, 1791960907140903764, 1791962405402364792, 1791967087014954093, 1791968113416310259, 1791962256146614715 |
| haproxy-native-htx | 112 | BOUNDED_HOST_OBSERVED | 1791962159961898700 |
| haproxy-spop-request | 94 | BOUNDED_HOST_OBSERVED | 1791962159961898700 |
| haproxy-spop-htx-response-companion | 72 | BOUNDED_HOST_OBSERVED | 1791962159961898700 |
| envoy-ext-proc | 117 | BOUNDED_HOST_OBSERVED | 1791961917474604194 |
| envoy-ext-authz-request | 94 | BOUNDED_HOST_OBSERVED | 1791961920408788276 |
| envoy-ext-authz-response-companion | 73 | BOUNDED_HOST_OBSERVED | 1791961923941705273 |
| traefik-native-uds | 118 | BOUNDED_HOST_OBSERVED | 1791957943997129475, 1791969629249293459, 1791969989698580089, 1791970798770219279, 1791971306363843767, 1791972087966404513 |
| traefik-forwardauth-request | 93 | BOUNDED_HOST_OBSERVED | 1791957947370099330 |
| traefik-forwardauth-response-companion | 69 | BOUNDED_HOST_OBSERVED | 1791957950693069209 |
| lighttpd-stock-sidecar | 153 | BOUNDED_HOST_OBSERVED | 1791959532449402163 |
| lighttpd-patched-native | 116 | BOUNDED_HOST_OBSERVED | 1791958816572382205, 1791962363858300796, 1791962875711476473 |
| lighttpd-stock-native-control | 78 | CONFIGURATION_LAYER_ONLY | 1791965490885259819 |

Root qualified only the original configuration-parser contracts: 36 required + 1 diagnostic. HTTP and lifecycle evidence is not inferred.

Root approval: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/root-config-qualification-approval.json` — SHA256 `7493e547f9169926517a39466ef0834f3e53e01cb20e184a3d234df294dbb737`.

## Sonar and CI source checkpoint

```json
{
  "Sonar_check_id": 115796444509,
  "Sonar_gate": "OK",
  "accepted_issues": 0,
  "authenticated_sonar_evidence": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-query-receipts.json",
  "duplicated_blocks": 0,
  "duplicated_lines": 0,
  "duplication_density": 0.0,
  "new_issues": 0,
  "observed_check_counts": {
    "in_progress": 2,
    "skipped": 2,
    "success": 24
  },
  "provider_evidence": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/github-pr410-6b-source-checkpoint.json",
  "remaining_provider_checks": "Historical93b checkpoint passed all required checks and authenticated strict-zero/A. New Apache two-file working delta awaits fresh ordinary delivery and CI/Sonar; no final-head reuse.",
  "scaffold_check_id": 115804226929,
  "scaffold_result": "success",
  "security_hotspots": 0,
  "security_rating": "A",
  "source_head": "93b4023234b8b3340464f5424b6e4d44e5d5dfdf",
  "terminal_check_counts": {
    "skipped": 2,
    "success": 26
  },
  "terminal_provider_evidence": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-ci-monitor/terminal-checks.json"
}
```

These observed values apply to the stated code source revision. The later documentation/delivery head requires its own final provider confirmation, retained externally and in the PR body.

## Limits and remaining evidence

596 catalog entries retain originally unresolved expected values. Resolution requires separately reviewed source-bound oracle evidence.

Unmeasured client/backend/API/EOS/MIME/finish/free/cleanup values remain null with reasons. Configuration tests qualify only their parser layer; HTTP fields are not applicable under their original contract.

- `apache-native`: Initial27 bounded controls remain retained. Newly attempted canonical14: v1 fails before HTTP at owned-executable guard; v2 reaches all14 actualHTTP with12 fixturePASS/two fixtureFAIL; currentv3 reaches all14 actualHTTP with13 fixturePASS/one posttraffic duplicate-header oracle conflict. The system Apache core coalesces duplicate headers before the connector mapper; original oracle is preserved and no product bug/full-case FAIL is inferred. Root approved exact14 partial receipts (474 unique raw file hashes); lifetime/API/EOS/MIME/finish/free remain incomplete.
- `nginx-native`: True root-master/nobody-worker operation succeeds. Each historic60 batch has57 PASS,2 config failures before traffic and1 obsolete log-oracle mismatch after actual HTTP200 with response_committed=true.42 exact selected native operations ran after collector repair; full independent lifecycle fields and two catalog/native-override oracle resolutions remain missing. Additionally,14 exactly selected canonical YAML host/client cases actually executed; two phase3 fixture aliases bind the unchanged exact selected YAML. Derived31 rows add no requests; complete independent lifecycle qualification remains missing.
- `haproxy-native-htx`: Actual bounded host controls are retained; exact complete selected-case client/backend/API/EOS/MIME/finish/free qualification is missing.
- `haproxy-spop-request`: Actual bounded host controls are retained; exact complete selected-case client/backend/API/EOS/MIME/finish/free qualification is missing.
- `haproxy-spop-htx-response-companion`: Actual bounded host controls are retained; exact complete selected-case client/backend/API/EOS/MIME/finish/free qualification is missing.
- `envoy-ext-proc`: Actual bounded host controls are retained; exact complete selected-case client/backend/API/EOS/MIME/finish/free qualification is missing.
- `envoy-ext-authz-request`: Actual bounded host controls are retained; exact complete selected-case client/backend/API/EOS/MIME/finish/free qualification is missing.
- `envoy-ext-authz-response-companion`: Actual bounded host controls are retained; exact complete selected-case client/backend/API/EOS/MIME/finish/free qualification is missing.
- `traefik-native-uds`: Current independent nativeUDS v5 smoke: six profiles PASS; allow200/54B, P1deny403/alt429, P2deny403, P3deny403, safeP4 200/55B. No native client_cancel/protocol_error records. Original successful allow client_cancel1/EOSfalse and failed pretraffic executable-mode variant remain retained. Only Parent smoke TCP/Content-Length/response-FD and precise exception/test handling changed;185 product inputs equal. Successful nativeEOS remains null; no transport-EOF, barrier, finish/free or MIME projection.
- `traefik-forwardauth-request`: Actual independent local/offline forwardAuth host smoke succeeds for this profile; its own raw client/access/native observations remain retained. No native-UDS client_cancel/EOS finding is transferred. Complete selected-case mapping, independent API/finish/free/EOS/MIME/backend measurements remain unavailable.
- `traefik-forwardauth-response-companion`: Actual independent local/offline forwardAuth host smoke succeeds for this profile; its own raw client/access/native observations remain retained. No native-UDS client_cancel/EOS finding is transferred. Complete selected-case mapping, independent API/finish/free/EOS/MIME/backend measurements remain unavailable.
- `lighttpd-stock-sidecar`: Actual bounded host controls are retained; exact complete selected-case client/backend/API/EOS/MIME/finish/free qualification is missing.
- `lighttpd-patched-native`: Six actual P2 gate controls succeed after bounded harness repairs; previous EPERM/config failures remain retained. P3/P4/full selected native lifecycle is not established.
- `lighttpd-stock-native-control`: Eight independent diagnostic parser probes ran; one exact original parser-acceptance contract is Root-qualified PASS. The other77 diagnostic IDs remain unqualified.

## Artifact binding

### apache-native

```json
{
  "actual_client_exchanges": 81,
  "actual_host_loaded_sdk_sha256": null,
  "actual_main_native_cleanup_enter_return_pairs": 27,
  "actual_module_build_parent_sha": "8c574cdf86f10af976297c31d31485b042eba73b",
  "additional_full_case_PASS": 0,
  "additional_selected_partial_execution": 14,
  "canonical14_current_attempt": "1791975496308340489",
  "canonical14_executed_harness_sha256": "30fd539bc319b8583cb9cfb23db7bedaf58c894afd5fc88c50076a8250d0d437",
  "canonical14_fixture_verdicts": {
    "pass": 13,
    "posttraffic_original_oracle_conflict": 1
  },
  "canonical14_product_inputs_equal": 194,
  "canonical14_root_partial_approval": "approved_partial_execution_only",
  "canonical194_product_input_scope_distinct": true,
  "compiler_input_equality_scope": 140,
  "duplicate_header_disposition": "SOURCE_HOST_HEADER_COALESCING_ORACLE_CONFLICT",
  "fixture_cases": 27,
  "host_binary_sha256": "32226a96ed9257837341b7909edae8da368922565f4662b1f76624e7c74e4a3d",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "module_sha256": "908c9e7a7062ada3e36499a69e2c41e17791a36021d5872d0981bfc5864bb5d0",
  "owned_executable_identity": "Task-owned regular copy verified against original system Apache SHA; no guard weakening.",
  "per_case_effective_configs": "Retained in native42-apache27-raw-audit.json; exact hashes verified.",
  "scoped_equal_production_input_count": 140,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962156241815212/controller-result.json` — SHA256 `ce5bb2da87c49d80a8f8337886fcbfd6786994f13cff5a2689ee9ac0298e947c`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/apache-v1/preparation.json` — SHA256 `b344a33227c39e09f3af26b0ab7c798ee9736e748d39387f6f48009b2d6216fd`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/native42-apache27-raw-audit.json` — SHA256 `b1f90709b224be0a926f6bb14a7725359ce8593ea013dd5cc3bdd3f7f1902768`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/apache-duplicate-header-core-proof/ap_read_request.stdout` — SHA256 `79937edbef5dad3ac167b4d0667dd70eb0ee3e957df8161faed1d2185f0cbf7e`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/apache-duplicate-header-core-proof/ap_read_request.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/apache-duplicate-header-core-proof/ap_get_mime_headers_core.stdout` — SHA256 `f2284c6b63ca706a03857538727f436fa512bb50572898e471a14e45c3eca199`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/apache-duplicate-header-core-proof/ap_get_mime_headers_core.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/apache-duplicate-header-core-proof/receipt.json` — SHA256 `15299e98c87691ef60a490b26e8bda774390459928aed8eb80975ec5d66e0918`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/apache-duplicate-header-core-proof/conclusion.json` — SHA256 `97c4622d37fc25c00b833d0fb92f5f7edccec39dd83e7b04c9026ca2606ba38e`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/apache-canonical14-final-preparation/audit-1791975496308340489/candidate-rows.json` — SHA256 `645be5c9bed204a119a025d54808a2ba7810162d45fe79c5aeaba714fd894266`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/root-apache-canonical14-partial-approval.json` — SHA256 `cdc682111aaf517612cf249973de1d2934eccb3404f7207c5548a69e4d6cb5d3`.
### nginx-native

```json
{
  "actual_current_selected_native_operation_count": 42,
  "actual_host_loaded_sdk_sha256": null,
  "actual_module_build_parent_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
  "canonical_explicit_phase3_fixture_aliases": 2,
  "canonical_selected_yaml_host_client_executions": 14,
  "canonical_yaml_attempt": "1791962256146614715",
  "config_parser_mapped_sdk_scope": "All10 actual parser cases have complete per-parser map bound to selected private SDK SHA32257230... and independent official API version3.0.14; this does not supply missing native-operation lifecycle observations.",
  "current_native24_attempt": "1791968113416310259",
  "derived31_are_additional_requests": false,
  "distinct_selected_operation_and_canonical_yaml_executions": 56,
  "historical_batch_sizes": [
    60,
    60
  ],
  "historical_batch_verdicts": [
    {
      "pass": 57,
      "posttraffic_obsolete_log_oracle_mismatch": 1,
      "pretraffic_config_fail": 2
    },
    {
      "pass": 57,
      "posttraffic_obsolete_log_oracle_mismatch": 1,
      "pretraffic_config_fail": 2
    }
  ],
  "historical_fixture_names_have_no_direct_selected_id_match": true,
  "host_binary_sha256": "0d2287b344a1af4c6cc986dd915c09c60f3c942ec8ae76f8bdc5456506939746",
  "host_version": "1.31.6",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "module_sha256": "fa2709956a28725294006c0f24a404f0564c8d36f101b4555dfeac0457241bef",
  "native_v1_driver_counts": {
    "0": 18,
    "1": 24
  },
  "native_v2_driver_counts": {
    "0": 24
  },
  "native_v3_driver_counts": {
    "0": 24
  },
  "root_capability_mask": "0xe3",
  "root_master_uid": 0,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "smoke_control_count": 4,
  "source_harness_deltas": "Owned self-map/FD cleanup/parser-invocation receipt repairs are explicitly bound by retained execution manifests; original source/build identities remain unchanged.",
  "worker_capabilities": "0",
  "worker_uid": 65534
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791958559271098737/controller-result.json` — SHA256 `d6fa651b8e8214120160ebdd6f31bb60083a8a9e9840ac744e103f10976b48f6`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791960903387896662/controller-result.json` — SHA256 `e7d058a7712a8788f750a6ea2ffda24fa229e78b7ab764a19fde476ce74c6ba9`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791960907140903764/controller-result.json` — SHA256 `baeb08ed1ae6a7966f1628a9ad45a0e4ea8eaa62042f7ef12963c79e2751c6cb`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962405402364792/controller-result.json` — SHA256 `eaed1751522d6c8409c8714c826b68dbe543cbddce3cd1c256c68ecde6bc3f43`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791967087014954093/controller-result.json` — SHA256 `ed23303230c388a48b45b04f9bd0a449e9893f795ef05480ed3e9e665718e3d2`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/build-receipt.json` — SHA256 `180615a415ef54b4b3296987de21d59e204bf5be62f5efbd224b45cbd340be24`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/partial-observation-candidates.json` — SHA256 `9d3b40a9a86f3b84bcf580101bd94b740707920f1f611e7547dc7eae571c1be1`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/nginx-canonical14-partial-candidates.json` — SHA256 `eef981f8084d7d0f3fda77df5a09871024696116def1b0fc442758b2756bbac5`.
### haproxy-native-htx

```json
{
  "actual_artifact_build_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "actual_host_loaded_sdk_sha256": null,
  "combined_shared_fixture_count": 6,
  "direct_htx_fixture_count": 8,
  "host_version": "3.2.25",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "htx_binary_sha256": "99390449d3931c4efc72888766464ff749f488014a36ab3256a4dacc165b5f24",
  "numeric_client_exit_codes": null,
  "scoped_equal_production_input_count": 150,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "shared_probe_group": "haproxy-spop-htx-six",
  "spop_binary_sha256": "d1f4e5f7f53a81ffcc6489d90903c6d90f3e8e816f5e067e4ac27299b293cdbe"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962159961898700/controller-result.json` — SHA256 `086e27ca1cbcf5aa87bd25e19d07e9a2099af8de4406f59f7140866f3900ae5d`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/haproxy-v1/preparation.json` — SHA256 `6cca4b53d6b4b4c46e44057ebe05b8b61d9be9e2b72920b5058de49bf6543693`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/config-raw-audit.json` — SHA256 `677154baca5471d4918b694ea70618e920416d2e7483316b35ad0d0803af7131`.
### haproxy-spop-request

```json
{
  "actual_artifact_build_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "actual_host_loaded_sdk_sha256": null,
  "combined_shared_fixture_count": 6,
  "direct_htx_fixture_count": null,
  "host_version": "3.2.25",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "htx_binary_sha256": "99390449d3931c4efc72888766464ff749f488014a36ab3256a4dacc165b5f24",
  "numeric_client_exit_codes": null,
  "scoped_equal_production_input_count": 150,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "shared_probe_group": "haproxy-spop-htx-six",
  "spop_binary_sha256": "d1f4e5f7f53a81ffcc6489d90903c6d90f3e8e816f5e067e4ac27299b293cdbe"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962159961898700/controller-result.json` — SHA256 `086e27ca1cbcf5aa87bd25e19d07e9a2099af8de4406f59f7140866f3900ae5d`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/haproxy-v1/preparation.json` — SHA256 `6cca4b53d6b4b4c46e44057ebe05b8b61d9be9e2b72920b5058de49bf6543693`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/config-raw-audit.json` — SHA256 `677154baca5471d4918b694ea70618e920416d2e7483316b35ad0d0803af7131`.
### haproxy-spop-htx-response-companion

```json
{
  "actual_artifact_build_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "actual_host_loaded_sdk_sha256": null,
  "combined_shared_fixture_count": 6,
  "direct_htx_fixture_count": null,
  "host_version": "3.2.25",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "htx_binary_sha256": "99390449d3931c4efc72888766464ff749f488014a36ab3256a4dacc165b5f24",
  "numeric_client_exit_codes": null,
  "scoped_equal_production_input_count": 150,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "shared_probe_group": "haproxy-spop-htx-six",
  "spop_binary_sha256": "d1f4e5f7f53a81ffcc6489d90903c6d90f3e8e816f5e067e4ac27299b293cdbe"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962159961898700/controller-result.json` — SHA256 `086e27ca1cbcf5aa87bd25e19d07e9a2099af8de4406f59f7140866f3900ae5d`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/haproxy-v1/preparation.json` — SHA256 `6cca4b53d6b4b4c46e44057ebe05b8b61d9be9e2b72920b5058de49bf6543693`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/config-raw-audit.json` — SHA256 `677154baca5471d4918b694ea70618e920416d2e7483316b35ad0d0803af7131`.
### envoy-ext-proc

```json
{
  "actual_host_loaded_sdk_sha256": null,
  "actual_native_binary_build_parent_sha": "6175a30d94de66f349c11eb8164b28942e040457",
  "component_binaries": "Exact sealed artifact ledger and per-profile runtime configs retained in admission spec/controller references.",
  "host_version": "1.39.1",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "scoped_equal_production_input_count": 172,
  "selected_qualification_count": null,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791961917474604194/controller-result.json` — SHA256 `c1c737844c08a4aafa9b613bc81efdd08837e0f54915e2f289d40a630c312f41`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791961917474604194/data/runtime/runtime-summary.txt` — SHA256 `eeff5b50b74f055e056343835760f91475c834768f60d96f735d25aa869b2bcd`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/envoy-v1/preparation.json` — SHA256 `61db16d2ae7a182187030ca48c5e3e3128b0e2150ccd8a5fe7c04d29ebc0aedf`.
### envoy-ext-authz-request

```json
{
  "actual_host_loaded_sdk_sha256": null,
  "actual_native_binary_build_parent_sha": "6175a30d94de66f349c11eb8164b28942e040457",
  "component_binaries": "Exact sealed artifact ledger and per-profile runtime configs retained in admission spec/controller references.",
  "host_version": "1.39.1",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "scoped_equal_production_input_count": 172,
  "selected_qualification_count": null,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791961920408788276/controller-result.json` — SHA256 `91bd6b3f16892eaa08a1a66ea63a6e81ea474937c4fc268e5b1fa0efc63b3275`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791961920408788276/data/runtime/runtime-summary.txt` — SHA256 `566a0c5c7a1b16185cb7e8f20c3ceaa02d94997217558d8a8da5e3a1be660caa`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/envoy-v1/preparation.json` — SHA256 `61db16d2ae7a182187030ca48c5e3e3128b0e2150ccd8a5fe7c04d29ebc0aedf`.
### envoy-ext-authz-response-companion

```json
{
  "actual_host_loaded_sdk_sha256": null,
  "actual_native_binary_build_parent_sha": "6175a30d94de66f349c11eb8164b28942e040457",
  "component_binaries": "Exact sealed artifact ledger and per-profile runtime configs retained in admission spec/controller references.",
  "host_version": "1.39.1",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "scoped_equal_production_input_count": 172,
  "selected_qualification_count": null,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791961923941705273/controller-result.json` — SHA256 `fd584f99a0d39d4f93ad1f8df62840ab1d0d54971066f7d4a751e200e04fa169`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791961923941705273/data/runtime/runtime-summary.txt` — SHA256 `37832170b9d73336198ff4b6f15df7fbdee1b9d19bed2bc2f4048ebb91a46b29`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/envoy-v1/preparation.json` — SHA256 `61db16d2ae7a182187030ca48c5e3e3128b0e2150ccd8a5fe7c04d29ebc0aedf`.
### traefik-native-uds

```json
{
  "actual_effective_config_hashes": null,
  "actual_loaded_modsecurity_sha256": null,
  "actual_native_engine_binary_sha256": null,
  "cap_eff": "0000000000000000",
  "copied_executables": [
    {
      "copy": "/task/cache/traefik",
      "sha256": "327314f5a64a9b25aba05bf83b0942ab3bfde65573cee8cc1a9e5b49d268cd63",
      "source": "/mnt/artifacts/traefik/host"
    }
  ],
  "current_allow_body_bytes": 54,
  "current_allow_client_cancel_records": 0,
  "current_allow_native_eos": null,
  "current_allow_status": 200,
  "current_attempt": "1791972087966404513",
  "current_code_source_head": "6b472cab6c18dfb5d6034461e1df5609e4ec3606",
  "current_native_eos_missing_reason": "No successful allow-side physical EOS record; TCP EOF is a transport-only measurement.",
  "current_native_finish_free_call_counts": null,
  "current_native_functional_profiles": 6,
  "current_native_protocol_error_records": 0,
  "current_native_result": {
    "p1_allow_response_bytes": 54,
    "p1_allow_status": 200,
    "p1_alternative_status": 429,
    "p1_deny_status": 403,
    "p2_deny_status": 403,
    "p3_precommit_deny_status": 403,
    "p4_safe_log_only_response_bytes": 55,
    "p4_safe_log_only_status": 200
  },
  "current_p4safe_body_bytes": 55,
  "current_p4safe_status": 200,
  "current_retained_physical_summary": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/traefik-native-final-v5-physical-summary.json",
  "current_source_harness_delta": "Source-v5 ledger/delta preserves precise OSError and Future exception trace plus exact wrong-module test; product engine/plugin185 inputs remain unchanged.",
  "functional_profile_count": 6,
  "gid": 65534,
  "go_toolchain": "local/offline",
  "go_version": "1.27.2",
  "historical_allow_client_cancel_records": 1,
  "historical_allow_eos_record": false,
  "initial_v1_exec_mode_attempt": "1791969629249293459",
  "initial_v1_exec_mode_result": "Collector pretraffic exit77 from lost copied executable mode; preserved, no product failure.",
  "missing_hash_reason": "native engine/config workspace removed by successful owned cleanup; runtime did not persist engine binary or loaded-library map/digest",
  "native_engine_build_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "no_new_privs": "1",
  "prepared_artifact_build_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
  "production_input_equivalence_count": 185,
  "production_inputs_all_equal": true,
  "retake_history": [
    {
      "actual_allow_native_eos": false,
      "all_equal": true,
      "attempt": "1791957943997129475",
      "client_body_bytes": 54,
      "client_status": 200,
      "controller_exit": 0,
      "native_client_cancel_records": 1,
      "native_eos_missing_reason": "No successful allow-side physical EOS record emitted; transport EOF does not establish native EOS.",
      "native_finish_free_call_counts": null,
      "native_protocol_error_records": 0,
      "outside_mount_leaks": [],
      "owned_pids_remaining": [],
      "p4safe_body_bytes": 55,
      "p4safe_status": 200,
      "production_input_equivalence_count": 185,
      "supervisor_reaped": true
    },
    {
      "actual_allow_native_eos": null,
      "all_equal": true,
      "attempt": "1791969989698580089",
      "client_body_bytes": 54,
      "client_status": 200,
      "controller_exit": 0,
      "native_client_cancel_records": 0,
      "native_eos_missing_reason": "No successful allow-side physical EOS record emitted; transport EOF does not establish native EOS.",
      "native_finish_free_call_counts": null,
      "native_protocol_error_records": 0,
      "outside_mount_leaks": [],
      "owned_pids_remaining": [],
      "p4safe_body_bytes": 55,
      "p4safe_status": 200,
      "production_input_equivalence_count": 185,
      "supervisor_reaped": true
    },
    {
      "actual_allow_native_eos": null,
      "all_equal": true,
      "attempt": "1791970798770219279",
      "client_body_bytes": 54,
      "client_status": 200,
      "controller_exit": 0,
      "native_client_cancel_records": 0,
      "native_finish_free_call_counts": null,
      "native_protocol_error_records": 0,
      "outside_mount_leaks": [],
      "owned_pids_remaining": [],
      "p4safe_body_bytes": 55,
      "p4safe_status": 200,
      "production_input_equivalence_count": 185,
      "supervisor_reaped": true
    },
    {
      "actual_allow_native_eos": null,
      "all_equal": true,
      "attempt": "1791971306363843767",
      "client_body_bytes": 54,
      "client_status": 200,
      "controller_exit": 0,
      "native_client_cancel_records": 0,
      "native_finish_free_call_counts": null,
      "native_protocol_error_records": 0,
      "outside_mount_leaks": [],
      "owned_pids_remaining": [],
      "p4safe_body_bytes": 55,
      "p4safe_status": 200,
      "production_input_equivalence_count": 185,
      "supervisor_reaped": true
    },
    {
      "actual_allow_native_eos": null,
      "actual_controller_exit_code": 0,
      "actual_driver_exit_code": 0,
      "all_equal": true,
      "attempt": "1791972087966404513",
      "code_source_head": "6b472cab6c18dfb5d6034461e1df5609e4ec3606",
      "functional_profile_count": 6,
      "functional_profile_result": {
        "p1_allow_response_bytes": 54,
        "p1_allow_status": 200,
        "p1_alternative_status": 429,
        "p1_deny_status": 403,
        "p2_deny_status": 403,
        "p3_precommit_deny_status": 403,
        "p4_safe_log_only_response_bytes": 55,
        "p4_safe_log_only_status": 200
      },
      "hosted_source_base": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
      "native_client_cancel_records": 0,
      "native_eos_missing_reason": "No independent successful allow-side native EOS record. TCP EOF and synthetic barrier/host-forward metadata do not establish native EOS.",
      "native_finish_free_call_counts": null,
      "native_protocol_error_records": 0,
      "outside_mount_leaks": [],
      "owned_pids_remaining": [],
      "production_input_equivalence_count": 185,
      "raw_references": [
        {
          "bytes": 4474,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/controller-result.json",
          "sha256": "db220d1d2dd632d7fea3a513c502c501f3a8c9dbe72a45f9a2fa3af454b77194"
        },
        {
          "bytes": 8142,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/isolation-admission.json",
          "sha256": "7acdf0acae33122f9e6c857528a2ccfed7fe706f240bd3bb0b758d4e5f1aab96"
        },
        {
          "bytes": 1740,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/command.json",
          "sha256": "63e9c87b4deb4410c4f084b60182d5a5c583abad6540533e62bf8a18b939ae26"
        },
        {
          "bytes": 1624,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/runtime/result.json",
          "sha256": "9a412e84d9221c035e6fcf1279915f7ba3e048950e9fff3e8afeccd96010b6e7"
        },
        {
          "bytes": 13698,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/runtime/logs/events.jsonl",
          "sha256": "548265aeb1032e7da44ad62414eb3840763999141dfdecf2fda235c77577b198"
        },
        {
          "bytes": 48132,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/prepared-source-equality.json",
          "sha256": "a8ba6904cfa7d0db135bbc984a8bc24fd51f437c6c0a7cee64c8943c819f4e3e"
        },
        {
          "bytes": 932,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/source-delta-v5.json",
          "sha256": "12370ea9dd3c242c3d134643f9a30474e60fcf2d75c56a6bdbdc1a47661ca9df"
        },
        {
          "bytes": 3299,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/admission-native-v5.json",
          "sha256": "ae6061ef100348d6c2659e6be9d35131a80a5c1e2d07de339150f26a59404f84"
        },
        {
          "bytes": 240622,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/source-v5-ledger.json",
          "sha256": "e27ef82eacfb98b96d1e9409b1d474eddcf25d2273a0aa78fd498de1f38053bf"
        }
      ],
      "scope": "Actual final nativeUDS v5 fixture; six functional profiles, no selected lifecycle promotion."
    }
  ],
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "source_harness_delta": "runtime_native_smoke.py only: consume complete TCP EOF, reject truncated Content-Length, and retain/close original response descriptor independently of response replacement.",
  "source_input_equality_all": true,
  "source_input_equality_count": 185,
  "source_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "uid": 65534
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957943997129475/controller-result.json` — SHA256 `b034a64f54bb2944d72bad6d6827761803d908eea7537c070864a01fc57932df`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-current-observations/summary.json` — SHA256 `58b4ce4a0fcd99d83d10f80bd481b558e2799b67b1db581e41fc8985dfd51edf`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-preparation/manifest.json` — SHA256 `8fef707b6e1578075f579a945caf15504428166159be1ddbceb3ecd520de7dc7`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/before-after-final-physical-observations.json` — SHA256 `1e2bc36f467690d9d73f391ee358ba61f445d001827af3d32b7e6e19dfccd006`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/source-delta-v4.json` — SHA256 `091916cf0fc7ecde7f7d5bafbbb81878d377b61a836a9bec4958bba367d51af6`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/admission-native-v4.json` — SHA256 `54e31f9777667fe0202e6d81250840d9231e692b055424b8e8168805002b6648`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791971306363843767/controller-result.json` — SHA256 `65021883de2f4f6145b35ae324bb8224099baecf98552c5d5cb95a2f7131bd20`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/traefik-native-final-v5-physical-summary.json` — SHA256 `e6ac40c23c0c8b5370c3177fe628501cc3a918fb1ccd395ca84f763fce4f5d13`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/controller-result.json` — SHA256 `db220d1d2dd632d7fea3a513c502c501f3a8c9dbe72a45f9a2fa3af454b77194`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/isolation-admission.json` — SHA256 `7acdf0acae33122f9e6c857528a2ccfed7fe706f240bd3bb0b758d4e5f1aab96`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/command.json` — SHA256 `63e9c87b4deb4410c4f084b60182d5a5c583abad6540533e62bf8a18b939ae26`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/runtime/result.json` — SHA256 `9a412e84d9221c035e6fcf1279915f7ba3e048950e9fff3e8afeccd96010b6e7`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/runtime/logs/events.jsonl` — SHA256 `548265aeb1032e7da44ad62414eb3840763999141dfdecf2fda235c77577b198`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791972087966404513/data/prepared-source-equality.json` — SHA256 `a8ba6904cfa7d0db135bbc984a8bc24fd51f437c6c0a7cee64c8943c819f4e3e`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/source-delta-v5.json` — SHA256 `12370ea9dd3c242c3d134643f9a30474e60fcf2d75c56a6bdbdc1a47661ca9df`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/admission-native-v5.json` — SHA256 `ae6061ef100348d6c2659e6be9d35131a80a5c1e2d07de339150f26a59404f84`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-client-completion-retake/source-v5-ledger.json` — SHA256 `e27ef82eacfb98b96d1e9409b1d474eddcf25d2273a0aa78fd498de1f38053bf`.
### traefik-forwardauth-request

```json
{
  "actual_effective_config_hashes": {
    "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957947370099330/data/build/traefik-connector/runtime/config/traefik-command.txt": "91e969e9aaebc59058321702beba43488567084d23b826f0b9169d83e198b2ed",
    "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957947370099330/data/build/traefik-connector/runtime/config/traefik-dynamic.yml": "ac46809ac8abe44a17724a435b687993e6037512708b779483c5fd560af25caf",
    "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957947370099330/data/build/traefik-connector/runtime/config/traefik-forwardauth.conf": "882236309c354291587f553f4db0339103ad6e2a8d661dc94aea61fe1252d081"
  },
  "actual_loaded_modsecurity_sha256": null,
  "actual_native_engine_binary_sha256": null,
  "cap_eff": "0000000000000000",
  "copied_executables": [
    {
      "copy": "/task/cache/traefik",
      "sha256": "327314f5a64a9b25aba05bf83b0942ab3bfde65573cee8cc1a9e5b49d268cd63",
      "source": "/mnt/artifacts/traefik/host"
    },
    {
      "copy": "/task/build/traefik-connector/traefik-forwardauth",
      "sha256": "c24f25cd6bc133e4a68c222b9b4f8927f1ea854c5c6d046d84b34fffc9d2d485",
      "source": "/mnt/artifacts/traefik/forwardauth"
    }
  ],
  "functional_profile_count": 2,
  "gid": 65534,
  "go_toolchain": "local/offline",
  "go_version": "1.27.2",
  "missing_hash_reason": "loaded-library map/digest not persisted",
  "native_engine_build_sha": null,
  "no_new_privs": "1",
  "prepared_artifact_build_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "source_input_equality_all": true,
  "source_input_equality_count": 185,
  "source_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "uid": 65534
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957947370099330/controller-result.json` — SHA256 `6f57a799a781af551b9e40051e0c736e1b23849c48b799ee3d97630aa6b04901`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-current-observations/summary.json` — SHA256 `58b4ce4a0fcd99d83d10f80bd481b558e2799b67b1db581e41fc8985dfd51edf`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-preparation/manifest.json` — SHA256 `8fef707b6e1578075f579a945caf15504428166159be1ddbceb3ecd520de7dc7`.
### traefik-forwardauth-response-companion

```json
{
  "actual_effective_config_hashes": {
    "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957950693069209/data/build/traefik-connector/runtime/config/traefik-command.txt": "c488d5c15bde9f3c01eea2893ea09181bc0b2dfa8d104b462192a403366314d8",
    "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957950693069209/data/build/traefik-connector/runtime/config/traefik-dynamic.yml": "1a30fdb543b353573be0a9b5027856e0322967b66d6c68512d86aa3582466b8e",
    "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957950693069209/data/build/traefik-connector/runtime/config/traefik-forwardauth.conf": "d7691c8032ca02856dd3e885311a05b6f8e4f988b34728f607756fc3213ec386"
  },
  "actual_loaded_modsecurity_sha256": null,
  "actual_native_engine_binary_sha256": null,
  "cap_eff": "0000000000000000",
  "copied_executables": [
    {
      "copy": "/task/cache/traefik",
      "sha256": "327314f5a64a9b25aba05bf83b0942ab3bfde65573cee8cc1a9e5b49d268cd63",
      "source": "/mnt/artifacts/traefik/host"
    },
    {
      "copy": "/task/build/traefik-connector/traefik-forwardauth",
      "sha256": "c24f25cd6bc133e4a68c222b9b4f8927f1ea854c5c6d046d84b34fffc9d2d485",
      "source": "/mnt/artifacts/traefik/forwardauth"
    }
  ],
  "functional_profile_count": 4,
  "gid": 65534,
  "go_toolchain": "local/offline",
  "go_version": "1.27.2",
  "missing_hash_reason": "loaded-library map/digest not persisted",
  "native_engine_build_sha": null,
  "no_new_privs": "1",
  "prepared_artifact_build_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "source_input_equality_all": true,
  "source_input_equality_count": 185,
  "source_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "uid": 65534
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791957950693069209/controller-result.json` — SHA256 `c64cf7f723fb33293aa136aefbe922778325f42970ee7f56baeba3f8805e82b9`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-current-observations/summary.json` — SHA256 `58b4ce4a0fcd99d83d10f80bd481b558e2799b67b1db581e41fc8985dfd51edf`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-preparation/manifest.json` — SHA256 `8fef707b6e1578075f579a945caf15504428166159be1ddbceb3ecd520de7dc7`.
### lighttpd-stock-sidecar

```json
{
  "actual_host_loaded_sdk_sha256": null,
  "actual_sidecar_build_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "fresh_host_binary_sha256": "5746e51d8d3e6a825886b334741c0998940587c2ffc536181da894bc4045ee56",
  "functional_fixture_count": 7,
  "genuine_offline_host_provenance": "Fresh pinned native build plus original Parent provenance/static-linkage validators passed; original host missing-provenance record retained.",
  "host_version": "1.4.85",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "trusted_host_archive_sha256": "18de51b393bac4a6827879e1a7ff377c169e414bae92cd245091d80fc2601d13"
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791959532449402163/controller-result.json` — SHA256 `30f8985e192ad3ed45c339f49ddd19dfc11d36bdd69d1085fe3cdbdc21aa55cd`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/stock-current-provenance/stock-v2/preparation.json` — SHA256 `b4768099262d6ef5e9228fa76301b113196833cf6448406d03855bb45ab8434e`.
### lighttpd-patched-native

```json
{
  "actual_host_loaded_sdk_sha256": null,
  "actual_native_module_build_parent_sha": "8c574cdf86f10af976297c31d31485b042eba73b",
  "full_lifecycle_launcher": "Nested unshare remains unavailable under original nonroot admission; no forged active-namespace flag.",
  "hosted_parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
  "phase2_pre_upstream_fixture_count": 6,
  "scoped_equal_production_input_count": 149,
  "selected_sdk_build_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
  "source_harness_delta": "Actual copied Parent phase2 harness corrected secure event path and native pre-upstream settings; committed in evidence_source_head; mounted/source/build SHAs never relabelled."
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962875711476473/controller-result.json` — SHA256 `194ace415157c71f0fb0c93f86a0ddf33417380f5e6ee75fe85cede45d042ae5`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962875711476473/data/patched-p2/summary.json` — SHA256 `94db60a8a24f5f7716ca66b661cd79da46ec2a62f42ec399e4d12477509038b4`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791962875711476473/data/executed-source-delta.json` — SHA256 `86e073aaca0bd94582ae280423ef67fc21ca82d0ac89b301df103232d807d420`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/patched-v2/preparation.json` — SHA256 `8d1187207f7c889b1593bb5d18865b0a49b93733d4f54898f8af1d87091bf86f`.
### lighttpd-stock-native-control

```json
{
  "current_config_probe_count": 8,
  "diagnostic_only": true,
  "http_fixture_count": null,
  "literal_exit_matched_config_count": 1,
  "literal_negative_exitcode": 255,
  "selected_diagnostic_ids": 78
}
```

- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/isolation/attempt-1791965490885259819/controller-result.json` — SHA256 `157afaf2097f51e49b3224a6776a7a2a50947fd0801353fa22f42f6f38142a37`.
- `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/config-raw-audit.json` — SHA256 `677154baca5471d4918b694ea70618e920416d2e7483316b35ad0d0803af7131`.

## Checks

| Check | Command | Exit | Scope SHA |
| --- | --- | --- | --- |
| focused:0 | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_haproxy_combined_spop_htx_harness_contract connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarLauncherContractTest tests.test_sonar_zero_gate tests.test_sonar_duplication_gate` | 0 | `1a40c9109f7aef3373ec24019000eb9ebe4dc27b` |
| focused:1 | `rtk proxy git diff --check` | 0 | `1a40c9109f7aef3373ec24019000eb9ebe4dc27b` |
| focused-02:0 | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_haproxy_combined_spop_htx_harness_contract connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarLauncherContractTest tests.test_sonar_zero_gate tests.test_sonar_duplication_gate` | 0 | `4f59d1632322a78676e224ef40c0ab7c8e96286c` |
| focused-02:1 | `rtk proxy git diff --check` | 0 | `4f59d1632322a78676e224ef40c0ab7c8e96286c` |
| harness-05:0 | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_traefik_native_local_plugin tests.test_native_lifecycle_observer` | 0 | `aba76c1b44ddc5b76a40ed4cff7ccdce2d95864c` |
| harness-05:1 | `rtk proxy git diff --check` | 0 | `aba76c1b44ddc5b76a40ed4cff7ccdce2d95864c` |
| regression-02:0 | `rtk proxy make check-i09-native-routes check-i10-adapter-errors check-native-engine-body-inspection check-common-helpers-c17 check-apache-event-sink check-haproxy-spop-event-sink PYTHON=/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/pr410-sonar-host-repair-20261014/modules/ModSecurity-test-Framework` | 0 | `aba76c1b44ddc5b76a40ed4cff7ccdce2d95864c` |
| quick-04:0 | `rtk proxy make quick-check check-bilingual-docs check-doc-links check-variable-documentation PYTHON=/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/pr410-sonar-host-repair-20261014/modules/ModSecurity-test-Framework` | 0 | `7abd61f6dc30f21b62f7b89902c28d319d0108b9` |
| nginx-final-01 (116 affected tests) | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_nginx_worker_self_maps tests.test_nginx_common_input_fault_driver tests.test_nginx_common_input_fault_scope tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases tests.test_nginx_sequence_transport tests.test_nginx_configtest_driver tests.test_nginx_valid_rules_driver` | 0 | `10102fcf26e05f64f0e7408e668bdde390ec9c07` |
| nginx-final-02 (116 affected tests) | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_nginx_worker_self_maps tests.test_nginx_common_input_fault_driver tests.test_nginx_common_input_fault_scope tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases tests.test_nginx_sequence_transport tests.test_nginx_configtest_driver tests.test_nginx_valid_rules_driver` | 0 | `7abd61f6dc30f21b62f7b89902c28d319d0108b9` |
| capability-source-only:0 | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python ci/evidence/collectors/connector_capabilities.py check` | 0 | `7abd61f6dc30f21b62f7b89902c28d319d0108b9` |
| capability-source-only:1 | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python ci/evidence/collectors/connector_capabilities.py generate --output-dir /var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/capability-source-current/generated` | 0 | `7abd61f6dc30f21b62f7b89902c28d319d0108b9` |
| offline-Go:native_middleware-race | `rtk proxy /usr/local/go/bin/go test -count=1 -race ./...` | 0 | `a9d48bb58aa948aea7d79e20cdf09d3f239b7808` |
| offline-Go:native_middleware-vet | `rtk proxy /usr/local/go/bin/go vet ./...` | 0 | `a9d48bb58aa948aea7d79e20cdf09d3f239b7808` |
| offline-Go:response_observer-race | `rtk proxy /usr/local/go/bin/go test -count=1 -race ./...` | 0 | `a9d48bb58aa948aea7d79e20cdf09d3f239b7808` |
| offline-Go:response_observer-vet | `rtk proxy /usr/local/go/bin/go vet ./...` | 0 | `a9d48bb58aa948aea7d79e20cdf09d3f239b7808` |
| patched P2 gate contract tests (27) | `Retained unittest output for connectors.lighttpd.tests.test_patched_p2_gate and related harness controls; full original argv not independently retained in this receipt.` | 0 | `None` |
| authenticated Sonar:7abd61f6-issues | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=410&resolved=false&ps=100'` | 0 | `7abd61f6dc30f21b62f7b89902c28d319d0108b9` |
| authenticated Sonar:7abd61f6-gate | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-conector&pullRequest=410'` | 0 | `7abd61f6dc30f21b62f7b89902c28d319d0108b9` |
| authenticated Sonar:7abd61f6-measures | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/measures/component?component=Easton97-Jens_ModSecurity-conector&pullRequest=410&metricKeys=new_security_rating,new_violations,new_accepted_issues,new_security_hotspots,new_duplicated_lines,new_duplicated_blocks,new_duplicated_lines_density'` | 0 | `7abd61f6dc30f21b62f7b89902c28d319d0108b9` |
| harness-09:0 (66 current harness/observer tests) | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_traefik_native_local_plugin tests.test_native_lifecycle_observer` | 0 | `bdaca57df9f8166dfc74615d9b3f11b5b97c084c` |
| harness-09:1 (66 current harness/observer tests) | `rtk proxy git diff --check` | 0 | `bdaca57df9f8166dfc74615d9b3f11b5b97c084c` |
| harness-10:0 (66 final affected harness/observer tests) | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_traefik_native_local_plugin tests.test_native_lifecycle_observer` | 0 | `dd61b70d8752e4530d686ec19d54e442710eadb6` |
| harness-10:1 (66 final affected harness/observer tests) | `rtk proxy git diff --check` | 0 | `dd61b70d8752e4530d686ec19d54e442710eadb6` |
| quick-05: final code quick-check and EN/DE/docs/variables | `rtk proxy make quick-check check-bilingual-docs check-doc-links check-variable-documentation PYTHON=/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/pr410-sonar-host-repair-20261014/modules/ModSecurity-test-Framework` | 0 | `6b472cab6c18dfb5d6034461e1df5609e4ec3606` |
| authenticated Sonar:6b472cab-issues | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=410&resolved=false&ps=100'` | 0 | `6b472cab6c18dfb5d6034461e1df5609e4ec3606` |
| authenticated Sonar:6b472cab-gate | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-conector&pullRequest=410'` | 0 | `6b472cab6c18dfb5d6034461e1df5609e4ec3606` |
| authenticated Sonar:6b472cab-measures | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/measures/component?component=Easton97-Jens_ModSecurity-conector&pullRequest=410&metricKeys=new_security_rating,new_violations,new_accepted_issues,new_security_hotspots,new_duplicated_lines,new_duplicated_blocks,new_duplicated_lines_density'` | 0 | `6b472cab6c18dfb5d6034461e1df5609e4ec3606` |
| quick-06:0 | `rtk proxy make quick-check check-bilingual-docs check-doc-links check-variable-documentation PYTHON=/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/pr410-sonar-host-repair-20261014/modules/ModSecurity-test-Framework` | 0 | `93b4023234b8b3340464f5424b6e4d44e5d5dfdf` |
| apache-empty-header-root-01:0 | `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/python-runtime/venv/bin/python -m unittest -v tests.test_apache_empty_header_driver` | 0 | `93b4023234b8b3340464f5424b6e4d44e5d5dfdf` |
| apache-empty-header-root-01:1 | `rtk proxy sh -n connectors/apache/harness/run_apache_smoke.sh` | 0 | `93b4023234b8b3340464f5424b6e4d44e5d5dfdf` |
| apache-empty-header-root-01:2 | `rtk proxy git diff --check` | 0 | `93b4023234b8b3340464f5424b6e4d44e5d5dfdf` |
| 93b authenticated checkpoint:checkpoint93b4023-issues | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=410&resolved=false&ps=100'` | 0 | `93b4023234b8b3340464f5424b6e4d44e5d5dfdf` |
| 93b authenticated checkpoint:checkpoint93b4023-gate | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-conector&pullRequest=410'` | 0 | `93b4023234b8b3340464f5424b6e4d44e5d5dfdf` |
| 93b authenticated checkpoint:checkpoint93b4023-measures | `rtk proxy /usr/local/bin/sonar-with-env api get '/api/measures/component?component=Easton97-Jens_ModSecurity-conector&pullRequest=410&metricKeys=new_security_rating,new_violations,new_accepted_issues,new_security_hotspots,new_duplicated_lines,new_duplicated_blocks,new_duplicated_lines_density'` | 0 | `93b4023234b8b3340464f5424b6e4d44e5d5dfdf` |

`focused:0`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`focused:1`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`focused-02:0`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`focused-02:1`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`harness-05:0`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`harness-05:1`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`regression-02:0`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`quick-04:0`: Observed head and retained per-command evidence; never promoted to a different final delivery head.

`capability-source-only:0`: Current source contract/check/regeneration only; no runtime capability or I12 case promotion.

`capability-source-only:1`: Current source contract/check/regeneration only; no runtime capability or I12 case promotion.

`offline-Go:native_middleware-race`: Actual Go1.27.2 local/offline test-race or vet on unchanged product sources.

`offline-Go:native_middleware-vet`: Actual Go1.27.2 local/offline test-race or vet on unchanged product sources.

`offline-Go:response_observer-race`: Actual Go1.27.2 local/offline test-race or vet on unchanged product sources.

`offline-Go:response_observer-vet`: Actual Go1.27.2 local/offline test-race or vet on unchanged product sources.

`patched P2 gate contract tests (27)`: Root reported actual exit0; retained log proves27 tests/OK. Exact process invocation metadata is unavailable.

`authenticated Sonar:7abd61f6-issues`: Actual authenticated PR410 GateOK/SecurityA/newissues0/accepted0/hotspots0/duplication0; final documentation delivery head requires fresh separate provider attestation.

`authenticated Sonar:7abd61f6-gate`: Actual authenticated PR410 GateOK/SecurityA/newissues0/accepted0/hotspots0/duplication0; final documentation delivery head requires fresh separate provider attestation.

`authenticated Sonar:7abd61f6-measures`: Actual authenticated PR410 GateOK/SecurityA/newissues0/accepted0/hotspots0/duplication0; final documentation delivery head requires fresh separate provider attestation.

`harness-09:0 (66 current harness/observer tests)`: Observed working-source suite before ordinary dd61 commit; exact v4 executed smoke delta retained separately. Historic head is not relabelled.

`harness-09:1 (66 current harness/observer tests)`: Observed working-source suite before ordinary dd61 commit; exact v4 executed smoke delta retained separately. Historic head is not relabelled.

`harness-10:0 (66 final affected harness/observer tests)`: Observed final affected suite before ordinary6b472ca code commit; exact executed v5 smoke producer delta retained separately. No head relabelling.

`harness-10:1 (66 final affected harness/observer tests)`: Observed final affected suite before ordinary6b472ca code commit; exact executed v5 smoke producer delta retained separately. No head relabelling.

`authenticated Sonar:6b472cab-issues`: Actual authenticated code-head0/A/GateOK, independently matched to successful exact-head GitHub Sonar provider. Final documentation head requires its own attestation.

`authenticated Sonar:6b472cab-gate`: Actual authenticated code-head0/A/GateOK, independently matched to successful exact-head GitHub Sonar provider. Final documentation head requires its own attestation.

`authenticated Sonar:6b472cab-measures`: Actual authenticated code-head0/A/GateOK, independently matched to successful exact-head GitHub Sonar provider. Final documentation head requires its own attestation.

`quick-06:0`: Actual working Apache harness/test delta checked on prior93b checkpoint; new delivery requires fresh CI.

`apache-empty-header-root-01:0`: Actual working Apache harness/test delta checked on prior93b checkpoint; new delivery requires fresh CI.

`apache-empty-header-root-01:1`: Actual working Apache harness/test delta checked on prior93b checkpoint; new delivery requires fresh CI.

`apache-empty-header-root-01:2`: Actual working Apache harness/test delta checked on prior93b checkpoint; new delivery requires fresh CI.

`93b authenticated checkpoint:checkpoint93b4023-issues`: Actual historical93b terminal26-success/two-skip and authenticated strict-zero SecurityA/GateOK; subsequent working delta is not covered.

`93b authenticated checkpoint:checkpoint93b4023-gate`: Actual historical93b terminal26-success/two-skip and authenticated strict-zero SecurityA/GateOK; subsequent working delta is not covered.

`93b authenticated checkpoint:checkpoint93b4023-measures`: Actual historical93b terminal26-success/two-skip and authenticated strict-zero SecurityA/GateOK; subsequent working delta is not covered.

`focused:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/results.json` — SHA256 `0fbd29afadfce50edd82f44800ab223330c94c4f6db06a1c84604a23db2805b4`.

`focused:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/0.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`focused:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/0.stderr.log` — SHA256 `42822c626e9478f631904a25094f79fe1d84513e09d6e72081b591fd9b31f06d`.

`focused:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/results.json` — SHA256 `0fbd29afadfce50edd82f44800ab223330c94c4f6db06a1c84604a23db2805b4`.

`focused:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/1.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`focused:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/1.stderr.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`focused-02:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused-02/results.json` — SHA256 `b1b35a4f1f64417f5d2fda15a8dd23029e980a21c6a2c8021185f0e154899851`.

`focused-02:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused-02/0.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`focused-02:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused-02/0.stderr.log` — SHA256 `6374e580bbd8eb7c630014c26c7a95a91b9b1f6d93957334090c2b73bcdd48b5`.

`focused-02:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused-02/results.json` — SHA256 `b1b35a4f1f64417f5d2fda15a8dd23029e980a21c6a2c8021185f0e154899851`.

`focused-02:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused-02/1.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`focused-02:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused-02/1.stderr.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-05:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-05/results.json` — SHA256 `2ceaabe658d2ffaa6603341ef6413d5239ef7c87143bc93bfa04229191a653b3`.

`harness-05:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-05/0.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-05:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-05/0.stderr.log` — SHA256 `9ff4894412bda21198896234ef52bf95cf4ce99040dcd15f52b6009d6df85c5d`.

`harness-05:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-05/results.json` — SHA256 `2ceaabe658d2ffaa6603341ef6413d5239ef7c87143bc93bfa04229191a653b3`.

`harness-05:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-05/1.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-05:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-05/1.stderr.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`regression-02:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/regression-02/results.json` — SHA256 `2f4cd83004108b357392c0e1924bc7d98ba0cb8461d64de0060e99350797a537`.

`regression-02:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/regression-02/0.stdout.log` — SHA256 `1ee5834b56e871a3edf0b09680174274efcdf075ea61d918188cb6ef806c9a6c`.

`regression-02:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/regression-02/0.stderr.log` — SHA256 `d2a453710e5d0ec8bd2a06f6847866f066e94b4c31788ed6396df9f708503a59`.

`quick-04:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-04/results.json` — SHA256 `53ea1b823597f1a836bc260d3c562addc957a2055ccc6fd7e1a17681f420d542`.

`quick-04:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-04/0.stdout.log` — SHA256 `d24e407c3005d585a34e181595161189c379beeba8899d252f207b64598dd6f5`.

`quick-04:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-04/0.stderr.log` — SHA256 `dc8b65d3ade0c3bb73bf6f5ed5e465212271641b6c2de6f60827d3b24632057a`.

`nginx-final-01 (116 affected tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/nginx-final-01/receipt.json` — SHA256 `9b0cb63c311c3f3313baf49b44bee8455b8cce73f750cac58bfb33bbec83a290`.

`nginx-final-01 (116 affected tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/nginx-final-01/stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`nginx-final-01 (116 affected tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/nginx-final-01/stderr.log` — SHA256 `d9669c6f052d7c2d9d25d9f218113fa36679b074152b4f528a96629f75275a45`.

`nginx-final-02 (116 affected tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/nginx-final-02/receipt.json` — SHA256 `b2e464d5c0be7fe6a468584715cafe1416d9a372573567671c70ba90cc0d3dd5`.

`nginx-final-02 (116 affected tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/nginx-final-02/stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`nginx-final-02 (116 affected tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/nginx-final-02/stderr.log` — SHA256 `d076a518f21cb68da629c5eab2e68fc73e9faf3b00e88c492bd99266fc02edc4`.

`capability-source-only:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/capability-source-current/receipt.json` — SHA256 `bde64f58c34279ea8b0f2798eed53557743bb9e564074f2e3383ffcb822581cc`.

`capability-source-only:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/capability-source-current/0.stdout` — SHA256 `dc75525eec5c0c4ad310dca8e57a17d99cefeb2bd128fdb75e0cce8666ac8987`.

`capability-source-only:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/capability-source-current/0.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`capability-source-only:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/capability-source-current/receipt.json` — SHA256 `bde64f58c34279ea8b0f2798eed53557743bb9e564074f2e3383ffcb822581cc`.

`capability-source-only:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/capability-source-current/1.stdout` — SHA256 `0da65acee894f354193acc3242cd7dc1609b75010f66161328ef1f381074fb17`.

`capability-source-only:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/capability-source-current/1.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`offline-Go:native_middleware-race`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-preparation/race-vet-receipts.json` — SHA256 `009373a19d1cfdf2dfff86d89c3e2aa34debb3a6a32213f98b170d0c977e5861`.

`offline-Go:native_middleware-vet`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-preparation/race-vet-receipts.json` — SHA256 `009373a19d1cfdf2dfff86d89c3e2aa34debb3a6a32213f98b170d0c977e5861`.

`offline-Go:response_observer-race`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-preparation/race-vet-receipts.json` — SHA256 `009373a19d1cfdf2dfff86d89c3e2aa34debb3a6a32213f98b170d0c977e5861`.

`offline-Go:response_observer-vet`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/traefik-preparation/race-vet-receipts.json` — SHA256 `009373a19d1cfdf2dfff86d89c3e2aa34debb3a6a32213f98b170d0c977e5861`.

`patched P2 gate contract tests (27)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/remaining-hosts-preparation/patched-source-tests-02.log` — SHA256 `3602997c99d4a138f421b3f767ebf0073e4813be070c3134b0f5f5090cfb3db2`.

`authenticated Sonar:7abd61f6-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-query-receipts.json` — SHA256 `c3be8c52f06f20724be9f1e289314b327c0ed390b8c750d41cd1b178e2b5179b`.

`authenticated Sonar:7abd61f6-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-issues.stdout` — SHA256 `a0df6fcd7aa349a218b37a27f84117fe80387cdc20a27e459c0f4d71b699c70d`.

`authenticated Sonar:7abd61f6-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-issues.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`authenticated Sonar:7abd61f6-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-query-receipts.json` — SHA256 `c3be8c52f06f20724be9f1e289314b327c0ed390b8c750d41cd1b178e2b5179b`.

`authenticated Sonar:7abd61f6-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-gate.stdout` — SHA256 `8cfb48611758ee377cd6c00ebee6ae6470fa1ffba0a0e53797d780bbc275955f`.

`authenticated Sonar:7abd61f6-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-gate.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`authenticated Sonar:7abd61f6-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-query-receipts.json` — SHA256 `c3be8c52f06f20724be9f1e289314b327c0ed390b8c750d41cd1b178e2b5179b`.

`authenticated Sonar:7abd61f6-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-measures.stdout` — SHA256 `73ce55b1b93f0fd469f4bbe4bf03d454052245f0a9d9201fae56fd2da2f25569`.

`authenticated Sonar:7abd61f6-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/7abd61f6-measures.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-09:0 (66 current harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-09/results.json` — SHA256 `868c661ac66f06a587b97e4d0484dff29283fce3d5ba1b03ef6733ba2668289b`.

`harness-09:0 (66 current harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-09/0.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-09:0 (66 current harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-09/0.stderr.log` — SHA256 `2356be46a51048aea523657107dfbfec94786f8334847573546d270ece9c2423`.

`harness-09:1 (66 current harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-09/results.json` — SHA256 `868c661ac66f06a587b97e4d0484dff29283fce3d5ba1b03ef6733ba2668289b`.

`harness-09:1 (66 current harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-09/1.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-09:1 (66 current harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-09/1.stderr.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-10:0 (66 final affected harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-10/results.json` — SHA256 `35ef9dfc4e68103731658c8da81907d2b89c87a20a1941883b94216d8ad3f18c`.

`harness-10:0 (66 final affected harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-10/0.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-10:0 (66 final affected harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-10/0.stderr.log` — SHA256 `2799c9aa2a31e9b4c6fcf3cdc067a50411ade89f56aa28b3c91e55b0b0c8bfce`.

`harness-10:1 (66 final affected harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-10/results.json` — SHA256 `35ef9dfc4e68103731658c8da81907d2b89c87a20a1941883b94216d8ad3f18c`.

`harness-10:1 (66 final affected harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-10/1.stdout.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`harness-10:1 (66 final affected harness/observer tests)`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/harness-10/1.stderr.log` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`quick-05: final code quick-check and EN/DE/docs/variables`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-05/results.json` — SHA256 `6ea3dd8bdcd65cbe733225178fafc6b22d520155179c97c4bb6c36271f92a1a5`.

`quick-05: final code quick-check and EN/DE/docs/variables`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-05/0.stdout.log` — SHA256 `1e6363cf6956e18dd3a53108637ea2b9cecdf03543d6024241e8c61380065be8`.

`quick-05: final code quick-check and EN/DE/docs/variables`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-05/0.stderr.log` — SHA256 `a327066303c9723c747fd370f4cdda5895e7f2544fa668d6dc2c6c8b8f6dd471`.

`authenticated Sonar:6b472cab-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-query-receipts.json` — SHA256 `736c48380459ea58c3580856c2170e0b828ae178be5676b00fdf02013662dd2c`.

`authenticated Sonar:6b472cab-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-issues.stdout` — SHA256 `a0df6fcd7aa349a218b37a27f84117fe80387cdc20a27e459c0f4d71b699c70d`.

`authenticated Sonar:6b472cab-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-issues.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`authenticated Sonar:6b472cab-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-query-receipts.json` — SHA256 `736c48380459ea58c3580856c2170e0b828ae178be5676b00fdf02013662dd2c`.

`authenticated Sonar:6b472cab-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-gate.stdout` — SHA256 `8cfb48611758ee377cd6c00ebee6ae6470fa1ffba0a0e53797d780bbc275955f`.

`authenticated Sonar:6b472cab-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-gate.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`authenticated Sonar:6b472cab-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-query-receipts.json` — SHA256 `736c48380459ea58c3580856c2170e0b828ae178be5676b00fdf02013662dd2c`.

`authenticated Sonar:6b472cab-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-measures.stdout` — SHA256 `73ce55b1b93f0fd469f4bbe4bf03d454052245f0a9d9201fae56fd2da2f25569`.

`authenticated Sonar:6b472cab-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/6b472cab-measures.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`quick-06:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-06/results.json` — SHA256 `130115fc8c08d70ebdea42b3993cc8cc30f15fd4d6ac6368552791b45ffa73d6`.

`quick-06:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-06/0.stdout.log` — SHA256 `f2bceb4f3233af7ea95c5e53baf26f0d4490eda8d09955adf63aef334f9c4d0d`.

`quick-06:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/quick-06/0.stderr.log` — SHA256 `2e6f9321153a1842b64480a70c7b5f895a80e4089a45277f2e331e56bfe55a21`.

`apache-empty-header-root-01:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/receipt.json` — SHA256 `b3e38d343c92054b590a3357bfcda31ea91d1b50e5d0cc84512d82924aa0cbac`.

`apache-empty-header-root-01:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/0.stdout` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`apache-empty-header-root-01:0`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/0.stderr` — SHA256 `42d1cfa5b55f24f4fa3072c148b15a53f282e1eb5cd22a71670a6635cd6a6368`.

`apache-empty-header-root-01:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/receipt.json` — SHA256 `b3e38d343c92054b590a3357bfcda31ea91d1b50e5d0cc84512d82924aa0cbac`.

`apache-empty-header-root-01:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/1.stdout` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`apache-empty-header-root-01:1`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/1.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`apache-empty-header-root-01:2`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/receipt.json` — SHA256 `b3e38d343c92054b590a3357bfcda31ea91d1b50e5d0cc84512d82924aa0cbac`.

`apache-empty-header-root-01:2`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/2.stdout` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`apache-empty-header-root-01:2`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/apache-empty-header-root-01/2.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`93b authenticated checkpoint:checkpoint93b4023-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-query-receipts.json` — SHA256 `cc217b73abe5b318b062dbdfb19383c7c7e0ece4e6a31b991cc6f28451561fdf`.

`93b authenticated checkpoint:checkpoint93b4023-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-issues.stdout` — SHA256 `a0df6fcd7aa349a218b37a27f84117fe80387cdc20a27e459c0f4d71b699c70d`.

`93b authenticated checkpoint:checkpoint93b4023-issues`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-issues.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`93b authenticated checkpoint:checkpoint93b4023-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-query-receipts.json` — SHA256 `cc217b73abe5b318b062dbdfb19383c7c7e0ece4e6a31b991cc6f28451561fdf`.

`93b authenticated checkpoint:checkpoint93b4023-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-gate.stdout` — SHA256 `8cfb48611758ee377cd6c00ebee6ae6470fa1ffba0a0e53797d780bbc275955f`.

`93b authenticated checkpoint:checkpoint93b4023-gate`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-gate.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`93b authenticated checkpoint:checkpoint93b4023-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-query-receipts.json` — SHA256 `cc217b73abe5b318b062dbdfb19383c7c7e0ece4e6a31b991cc6f28451561fdf`.

`93b authenticated checkpoint:checkpoint93b4023-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-measures.stdout` — SHA256 `73ce55b1b93f0fd469f4bbe4bf03d454052245f0a9d9201fae56fd2da2f25569`.

`93b authenticated checkpoint:checkpoint93b4023-measures`: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/sonar/checkpoint93b4023-measures.stderr` — SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Release: **RELEASE_BLOCKED_SECRET_HISTORY**. Historic PR #382 secret-history range check remains independently failed; current host evidence does not remediate immutable history. Both PRs remain Draft.

[Complete case index](pr-382-i12-missing-case-index-20261014.md).

## Generator and raw evidence

Run: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion`.

Generator SHA256: `134f3df11974c7a6bb3cb34a432a47b7ded10d0f0f97747c9bc6100441d10cc9`.

Catalog SHA256: `ddf5a766fbcc10d33f36c21c548fe8b09649e36b23487b8404a86dc62c18e3a4`.

Ordered ID stream SHA256: `a74761d9722b646873325ecd27ea99661f00bee67052980fa04ede0e1f1a0f6f`.

The original 79 raw records and historic runs remain unchanged. `summary.json`, `requirements.json` and reviewed file hashes are retained in the new `final-reconciliation/`.

Release: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/final-reconciliation/github-pr382-final-checks.json` — SHA256 `2c9ce2dcfd5d4e5fb904c24fd1364f05887bde880d3729c56bb206f67a9a047e`.
