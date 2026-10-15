# I12 aktuelle Host-Evidenz

**Sprache:** [English](pr-382-i12-host-evidence-20261014.md) | Deutsch

Status: **I12_PARTIAL**.

Die folgenden Zahlen stammen aus dem geprüften aktuellen Ledger. Konfigurations-PASS und vollständige Host-Lifecycle-Abnahme bleiben getrennt.

## Aktuelle Zähler

```json
{
  "actually_executed_ids": 151,
  "configuration_only_pass": 37,
  "full_lifecycle_fail": 0,
  "full_lifecycle_pass": 21,
  "oracle_counts": {
    "actually_retested_original_oracles": 21,
    "baseline_config_parser_pass": 37,
    "baseline_observed_ids": 130,
    "by_profile": {
      "apache-native": 54,
      "envoy-ext-authz-request": 40,
      "envoy-ext-authz-response-companion": 34,
      "envoy-ext-proc": 51,
      "haproxy-native-htx": 48,
      "haproxy-spop-htx-response-companion": 32,
      "haproxy-spop-request": 44,
      "lighttpd-patched-native": 52,
      "lighttpd-stock-native-control": 23,
      "lighttpd-stock-sidecar": 51,
      "nginx-native": 43,
      "traefik-forwardauth-request": 39,
      "traefik-forwardauth-response-companion": 30,
      "traefik-native-uds": 55
    },
    "categories": {
      "SOURCE_CONFIRMED_EXPECTATION": 21,
      "UNRESOLVED_ORACLE": 575
    },
    "full_lifecycle_qualification_performed": false,
    "original_diagnostic_ids": 78,
    "original_ids": 1484,
    "original_open_oracles": 596,
    "original_required_ids": 1406,
    "resolved_original_oracles": 21,
    "rootcause_groups": {
      "commit_action": 34,
      "correlation_lease": 10,
      "historical_fixture_binding": 29,
      "missing_effective_fixture_and_oracle": 84,
      "native_body_semantics": 279,
      "physical_event_sink": 70,
      "resource_identity": 5,
      "sample_frame_scope": 22,
      "transport_cleanup": 63
    },
    "supplemental_original_oracle_dispositions": 21,
    "unresolved_original_oracles": 575,
    "unsupported_original_oracles": 0
  },
  "original_ids": 1484,
  "required_full_lifecycle_fail": 0,
  "required_full_lifecycle_pass": 21,
  "required_qualified_fail": 0,
  "required_qualified_pass": 57,
  "required_routes_with_full_case": 13,
  "unqualified_ids": 1426
}
```

## 13 Pflichtrouten

| Route | IDs | Ausgeführt | Config PASS | Lifecycle PASS | Lifecycle FAIL | Unqualifiziert |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| apache-native | 155 | 25 | 9 | 1 | 0 | 145 |
| nginx-native | 140 | 67 | 10 | 1 | 0 | 129 |
| haproxy-native-htx | 112 | 5 | 0 | 5 | 0 | 107 |
| haproxy-spop-request | 94 | 6 | 0 | 3 | 0 | 91 |
| haproxy-spop-htx-response-companion | 72 | 1 | 0 | 1 | 0 | 71 |
| envoy-ext-proc | 117 | 2 | 0 | 1 | 0 | 116 |
| envoy-ext-authz-request | 94 | 9 | 8 | 1 | 0 | 85 |
| envoy-ext-authz-response-companion | 73 | 1 | 0 | 1 | 0 | 72 |
| traefik-native-uds | 118 | 2 | 1 | 1 | 0 | 116 |
| traefik-forwardauth-request | 93 | 9 | 8 | 1 | 0 | 84 |
| traefik-forwardauth-response-companion | 69 | 1 | 0 | 1 | 0 | 68 |
| lighttpd-stock-sidecar | 153 | 12 | 0 | 2 | 0 | 151 |
| lighttpd-patched-native | 116 | 3 | 0 | 2 | 0 | 114 |

## Getrennte diagnostische Kontrolle

| Route | IDs | Ausgeführt | Config PASS | Lifecycle PASS | Lifecycle FAIL | Unqualifiziert |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| lighttpd-stock-native-control | 78 | 8 | 1 | 0 | 0 | 77 |

## Aktueller Quellen-, CI- und Release-Stand

```json
{
  "actual_host_revisions": {
    "Apache": "2.4.66/APR1.7.6",
    "Envoy": "b579d07d3ad7ee11d32b105e91a5a39ad24718d7/1.39.1",
    "HAProxy": "3.2.25",
    "Lighttpd": "1.4.85",
    "NGINX": "1.31.6",
    "Traefik": "3.7.13",
    "libModSecurity": "3.0.14/SHA32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
  },
  "current_ledger": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/twentyone-qualified-08.json",
  "current_reconciliation": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/oracles/twentyone-source-confirmed-13/oracle-reconciliation.json",
  "evidence_root": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle",
  "i12_status": "I12_PARTIAL",
  "local_stack_merge": "eca03db3b9ec780fc58b028343d5213fbe54f14d",
  "local_validation": {
    "product_broad": "Actual I09/I10/I11/native/body/CommonC17/APX/HAP sink delivery02 PASS; full product Native suite392.411s PASS. Latest combined stack Quick06 and Docs10 (ENDE, links, Change Records) PASS with Framework read-only. Only source-bound report metadata changes follow these checks.",
    "product_nginx": "151 integrated,46 focused,77 sourceguards/33 C17 TUs plus115 complete checker mutations and5 portable compiled mapper regressions PASS; initial600s mutation timeout preserved.",
    "renderer": "Root13 independent tests PASS after precise status/execution/history invariant repair; no unobserved/config/partial PASS promotion.",
    "root_lifecycle": "Root90 tests PASS/no skips:32 actual native-observer controls,12 APR/SDK,8 oracle,10 lifecycle ledger,13 renderer,15 capture guards. Stable38 C ad8/H f9; native append has no EOS argument.",
    "scaffold_followup": "Obsolete mapper400 assertion reproduced FAIL first; typed default500/propagated status/client-header400 controls now38+5 compiled PASS, receipt ci382-scaffold-followup/after-receipt.json.",
    "source_capture": "Root05:150 registry objects,9 copy-only variants,45 exact native patch applications,15 guards and3 Envoy capture+2 gRPC source groups PASS. No raw runtime artifacts or credentials in source package."
  },
  "new_full_evidence": "Actual EOS/finish/free/physicalevent/client/backend/hash/commit/loadedimage/UID/neighbor/cleanup per selected packet; native append has noEOSargument. HAP nativeReject16/Partial16, four body/header additions and two emptyLighttpd cases add obligations without connector-owned WAF limits.",
  "original_source_and_history": "Old20261013/20261014 raw records and checksums preserved. Framework99a read-only, actual pinned MRTS8a metadata only; no MRTS checkout/execution or Gitlink changes.",
  "pr382_current_ci": "9980eb049dde0643da6a4f04e3b6712801b670b3 is published; fresh hosted checks pending. e47 Sonar was zero/A with strictzero/dupPASS but scaffold failed its obsolete all400 assertion. The single test is corrected in9980 and actual38 contracts+5 compiled mapper tests PASS. Historical Gitleaks remains an independent release blocker.",
  "pr382_sonar_receipt": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/verification/product382-e47-sonar-01/receipt.json",
  "pr410_current_ci_sonar": "Remote410 still027540; no source changes in this round have hosted results yet. Old green cannot be transferred.",
  "pr410_current_working_changes": "Unpublished independent observer38/snapshot, Source-bound Oracle/ledger/report producers, Apache header oracle fixture and reproducible source-copy capture packages. Final-head hosted CI/Sonar will be checked after publication.",
  "product_pr382_head": "9980eb049dde0643da6a4f04e3b6712801b670b3",
  "product_scope": "Published typed NGX mapper internal500 versus existing client400 repair12756; e47 checker regex/CI portability follow-up normally merged into410. Actual module/SDK host retakes independently confirm500,400 and supported full single-chunk lifecycle. Runtime source bytes are unchanged by e47.",
  "release_status": "RELEASE_BLOCKED_SECRET_HISTORY",
  "remote_pr410_head": "02754040bced960cfc1857416cd7101bb3116ef4",
  "repository": "Easton97-Jens/ModSecurity-conector",
  "required_case_status": "21 separately qualified original required lifecycle cases cover13/13 logical routeparts; this does not qualify all1406 required IDs. Original596:21 SOURCE_CONFIRMED_EXPECTATION/actualretakes,575 unresolved; no unsupported relabels.",
  "security_scope": "No further deep scan. Existing proven historical release blocker preserved; no history rewrite, no broad exception.",
  "supplemental_disposition_summary": {
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/catalog-conflicts/final-supplemental20/disposition-summary.json",
    "sha256": "d68c2535d5ece0990670b3e01f173df9d98ad26684fef1f7bf39ca37cc436021"
  },
  "supplemental_scope": "Apache duplicate source-confirmed outside596; NGX parser/staleSafe/typed500 and actual400 separate, BodyP2/injectedP1 unresolved. Twenty additional exact known IDs have Root-confirmed HARNESS_DEFECT_CONFIRMED layer bindings: generic catalog config_rejected/1 stays unchanged; actual native waited exits255x8,78x9,2x1,77x2 from9 parser-only plus11 service-start failures. Actual nine sidecar first causes remain null because stderr is empty. Two complete scope-file inputs prove rejection of an unknown Common key, not MIME/wildcard parsing. Three companion parser entrypoints remain unbound; two service SIGTERM-15 exits are not parser0; Apache parser0 does not prove runtime sink open. The separate29 original596 historical bindings and23 stock-native diagnostic unknowns are not relabelled unsupported. Envoy transport evidence is actual local HTTP2 closed2, with remote status/peerEOF unknown."
}
```

## Physische Lifecycle-Pakete

### I12::apache-native::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 83487,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-lifecycle-command.json",
          "role": "cleanup_observer",
          "sha256": "186c7a4dd98f6ce8f8315419e36d11599af88488e127b7af252f70b69c129ec0"
        },
        {
          "bytes": 4495,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "ccb129bdd9080e77cbe201d9ec6582f458056bf98be858ad8e8cf17215440558"
        }
      ],
      "value": {
        "host_final": {
          "actual_apr_bucket_is_eos": false,
          "actual_apr_bucket_present": false,
          "allocation_scope_call": 4,
          "contract_cleanup_complete": 1,
          "contract_error_class": 0,
          "contract_initialized": 0,
          "contract_last_completed_phase": 5,
          "event_sink_error": 0,
          "gid": 65534,
          "host_context_present": true,
          "invalid": false,
          "kind": "host_context_retired",
          "monotonic_ns": 100939415974074,
          "native_mime_selection": null,
          "native_transaction_present": false,
          "owner_request_matches": false,
          "pid": 373,
          "request_body_processed": 1,
          "request_eos_released": 1,
          "request_method": "POST",
          "request_uri": "/i12/apache/eos",
          "response_body_processed": 1,
          "response_committed": 1,
          "response_eos_released": 1,
          "response_eos_seen": 1,
          "schema": "apache-host-observer-v1",
          "sequence": 9,
          "terminal_event_attempted": 0,
          "uid": 65534
        },
        "native_observer_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-eos-once",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 100942177245292,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 373,
          "profile": "apache-native",
          "result": null,
          "run": "20261014T182400Z-apache-lifecycle",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 112,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792010575966650806,
          "wall_sample_end_monotonic_ns": 100942177245468
        },
        "sampler_thread_stopped": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 112216,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-native-api.jsonl",
          "role": "native_api",
          "sha256": "8c3b4e1e754fc90a715752b3425acc1f6e4ac69403a6b1be01b8e1a3ee198f84"
        }
      ],
      "value": {
        "common_finish": 1,
        "native_logging": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 13493,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-host-eos.jsonl",
          "role": "host_callback",
          "sha256": "9d8852ab754787b71984e7dec765664aec922887ebf3a7f5b0e3c01c8c91a94d"
        }
      ],
      "value": {
        "host_rows": [
          {
            "actual_apr_bucket_is_eos": false,
            "actual_apr_bucket_present": false,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": -1,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "host_context_associated",
            "monotonic_ns": 100939406420897,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 0,
            "request_eos_released": 0,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 0,
            "response_committed": 0,
            "response_eos_released": 0,
            "response_eos_seen": 0,
            "schema": "apache-host-observer-v1",
            "sequence": 1,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": true,
            "actual_apr_bucket_present": true,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": 2,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "actual_request_apr_eos",
            "monotonic_ns": 100939407702653,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 0,
            "request_eos_released": 0,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 0,
            "response_committed": 0,
            "response_eos_released": 0,
            "response_eos_seen": 0,
            "schema": "apache-host-observer-v1",
            "sequence": 2,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": false,
            "actual_apr_bucket_present": false,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": 4,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "output_prefix_release_enter",
            "monotonic_ns": 100939415095831,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 1,
            "request_eos_released": 1,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 0,
            "response_committed": 1,
            "response_eos_released": 0,
            "response_eos_seen": 0,
            "schema": "apache-host-observer-v1",
            "sequence": 3,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": false,
            "actual_apr_bucket_present": false,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": 4,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "output_prefix_release_return_ok",
            "monotonic_ns": 100939415123849,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 1,
            "request_eos_released": 1,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 0,
            "response_committed": 1,
            "response_eos_released": 0,
            "response_eos_seen": 0,
            "schema": "apache-host-observer-v1",
            "sequence": 4,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": true,
            "actual_apr_bucket_present": true,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": 4,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "actual_response_apr_eos",
            "monotonic_ns": 100939415137570,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 1,
            "request_eos_released": 1,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 0,
            "response_committed": 1,
            "response_eos_released": 0,
            "response_eos_seen": 1,
            "schema": "apache-host-observer-v1",
            "sequence": 5,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": false,
            "actual_apr_bucket_present": false,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": 5,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "output_terminal_release_enter",
            "monotonic_ns": 100939415412032,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 1,
            "request_eos_released": 1,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 1,
            "response_committed": 1,
            "response_eos_released": 1,
            "response_eos_seen": 1,
            "schema": "apache-host-observer-v1",
            "sequence": 6,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": false,
            "actual_apr_bucket_present": false,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": 5,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "output_terminal_release_return_ok",
            "monotonic_ns": 100939415434652,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 1,
            "request_eos_released": 1,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 1,
            "response_committed": 1,
            "response_eos_released": 1,
            "response_eos_seen": 1,
            "schema": "apache-host-observer-v1",
            "sequence": 7,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": false,
            "actual_apr_bucket_present": false,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 0,
            "contract_error_class": 0,
            "contract_initialized": 1,
            "contract_last_completed_phase": 5,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "host_cleanup_before",
            "monotonic_ns": 100939415786272,
            "native_mime_selection": null,
            "native_transaction_present": true,
            "owner_request_matches": true,
            "pid": 373,
            "request_body_processed": 1,
            "request_eos_released": 1,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 1,
            "response_committed": 1,
            "response_eos_released": 1,
            "response_eos_seen": 1,
            "schema": "apache-host-observer-v1",
            "sequence": 8,
            "terminal_event_attempted": 0,
            "uid": 65534
          },
          {
            "actual_apr_bucket_is_eos": false,
            "actual_apr_bucket_present": false,
            "allocation_scope_call": 4,
            "contract_cleanup_complete": 1,
            "contract_error_class": 0,
            "contract_initialized": 0,
            "contract_last_completed_phase": 5,
            "event_sink_error": 0,
            "gid": 65534,
            "host_context_present": true,
            "invalid": false,
            "kind": "host_context_retired",
            "monotonic_ns": 100939415974074,
            "native_mime_selection": null,
            "native_transaction_present": false,
            "owner_request_matches": false,
            "pid": 373,
            "request_body_processed": 1,
            "request_eos_released": 1,
            "request_method": "POST",
            "request_uri": "/i12/apache/eos",
            "response_body_processed": 1,
            "response_committed": 1,
            "response_eos_released": 1,
            "response_eos_seen": 1,
            "schema": "apache-host-observer-v1",
            "sequence": 9,
            "terminal_event_attempted": 0,
            "uid": 65534
          }
        ],
        "physical_actual_apr_request_eos": 1,
        "physical_actual_apr_response_eos": 1
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 112216,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-native-api.jsonl",
          "role": "native_api",
          "sha256": "8c3b4e1e754fc90a715752b3425acc1f6e4ac69403a6b1be01b8e1a3ee198f84"
        },
        {
          "bytes": 13493,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-host-eos.jsonl",
          "role": "host_callback",
          "sha256": "9d8852ab754787b71984e7dec765664aec922887ebf3a7f5b0e3c01c8c91a94d"
        }
      ],
      "value": {
        "actual_request_apr_eos": 1,
        "actual_response_apr_eos": 1,
        "definition": "Physical APR EOS branches and same typed host allocation native finalization calls; native append has no EOS argument, null retained.",
        "native_append_eos_argument": null,
        "native_request_body_finalization": 1,
        "native_response_body_finalization": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 112216,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-native-api.jsonl",
          "role": "native_api",
          "sha256": "8c3b4e1e754fc90a715752b3425acc1f6e4ac69403a6b1be01b8e1a3ee198f84"
        }
      ],
      "value": {
        "common_cleanup": 1,
        "host_retire_bookkeeping": 1,
        "native_cleanup": 1
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 39098,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/native-process/100939401558261.maps",
          "role": "loaded_image",
          "sha256": "3163c57073ac77af0300c9160232e72ee6b5e1bc65add4c3bd1ab482985925ce"
        },
        {
          "bytes": 1492,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/native-process/100939401558261.status",
          "role": "loaded_image",
          "sha256": "84d5f874e7b61d38e76cda7092146931e42d91095469bb82753c701a8dc2f56f"
        },
        {
          "bytes": 8202,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/admission.original.json",
          "role": "isolation_receipt",
          "sha256": "a8bbf4c79f73b746d491e8ae49ef3d79cb7aa700d6d350708a10136ee561da47"
        }
      ],
      "value": {
        "actual_nonroot_zero_capabilities": true,
        "actual_pid": 373,
        "actual_starttime": "10093636",
        "apache_binary_sha256": "32226a96ed9257837341b7909edae8da368922565f4662b1f76624e7c74e4a3d",
        "gid": 65534,
        "selected_sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
        "selected_sdk_version": "3.0.14",
        "test_module_sha256": "d4244dde8ebfae13fe513ee8464522acbbf1bab4a239f00d2315de40688a1a01",
        "uid": 65534
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 242761,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/source-v5-ledger.json",
          "role": "source_manifest",
          "sha256": "b6e2725c9817b1d722ed9c2aa85025e70bd09196e256a0d43c4415f6b950361e"
        },
        {
          "bytes": 26134,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/observed-module-07/link-receipt.json",
          "role": "source_manifest",
          "sha256": "70c741e2bd79cbb8bdfea6e52bd848cfff4cc963157ed415763ec93ab525b38d"
        },
        {
          "bytes": 1490,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-lifecycle/runtime/conf/httpd.conf",
          "role": "effective_configuration",
          "sha256": "57ebbd43960fce3be57302be27e34c2da6f0adaa938bffc7ceb6dad3e7f962b0"
        },
        {
          "bytes": 901,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792010525870895956/data/apache-lifecycle/runtime/conf/modsecurity-smoke.conf",
          "role": "effective_configuration",
          "sha256": "8aa78608aac36d53034fa7814c5e9f497adbdfdea575cda21107682cd252eeb8"
        },
        {
          "bytes": 116,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-readonly-revisions-01.json",
          "role": "source_manifest",
          "sha256": "7626580d3e02904f25e1ebc03852abab8596c3d78cf092a2e3b2658f5514a0cf"
        }
      ],
      "value": {
        "mrts_scope": "Actual Framework pinned Gitlink metadata read only; MRTS not checked out or executed in this run.",
        "real_parent_base": "02754040bced960cfc1857416cd7101bb3116ef4",
        "source_compile_and_link_manifest": "Genuine historical objects plus three source-copy APX callbacks and test observers; not relabeled byte-identical product module.",
        "source_ledger_sha256": "b6e2725c9817b1d722ed9c2aa85025e70bd09196e256a0d43c4415f6b950361e",
        "working_and_test_overlay_explicit": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "57ebbd43960fce3be57302be27e34c2da6f0adaa938bffc7ceb6dad3e7f962b0",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "02754040bced960cfc1857416cd7101bb3116ef4",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "8aa78608aac36d53034fa7814c5e9f497adbdfdea575cda21107682cd252eeb8",
    "run_id": "20261014T182400Z-apache-lifecycle"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 89709,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-apache-01.json",
    "sha256": "7f42f44d2446570ae731021bfa58f29439c8b59fdf3f7c5e4ae316cec57cc102"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::nginx-native::NEED-request-single-chunk

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 7477,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/full-observation-receipt.json",
          "role": "cleanup_observer",
          "sha256": "20a17f5446928730209a5622eb42d7fb41e3d5a3522a18d3dde0bafbdb297663"
        },
        {
          "bytes": 4560,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "ef1511ea494fd6c9157cc8329fd4a4524add23a51ba4f660e7880dc96a71b504"
        }
      ],
      "value": {
        "host": {
          "listener_open": false,
          "master_pid": 303,
          "master_running": false,
          "run_id": "20261014-nginx-need-single-chunk",
          "verified": true,
          "worker_pid": 304,
          "worker_running": false
        },
        "observer_finals": [
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 0,
            "canonical_transaction_id": null,
            "case": "I12::nginx-native::NEED-request-single-chunk",
            "contract_state": null,
            "edge": "final",
            "function": "observer",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 107575728116024,
            "native_mime_selection": null,
            "pending_calls": 0,
            "phase": 0,
            "pid": 304,
            "profile": "nginx-native",
            "result": null,
            "run": "20261014-nginx-need-single-chunk",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 114,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792017209517521548,
            "wall_sample_end_monotonic_ns": 107575728116203
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 0,
            "canonical_transaction_id": null,
            "case": "I12::nginx-native::NEED-request-single-chunk",
            "contract_state": null,
            "edge": "final",
            "function": "observer",
            "gid": 0,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 107575730598723,
            "native_mime_selection": null,
            "pending_calls": 0,
            "phase": 0,
            "pid": 303,
            "profile": "nginx-native",
            "result": null,
            "run": "20261014-nginx-need-single-chunk",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 2,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 0,
            "wall_ns": 1792017209520004234,
            "wall_sample_end_monotonic_ns": 107575730598887
          }
        ]
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 117281,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/physical-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "6c940f30ada64a172521dc46992c2ba9c4473cb5a6809c82465b725578dbcaaf"
        }
      ],
      "value": {
        "common_finish": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": "txc-0000000006697918-0000000000000000",
            "case": "I12::nginx-native::NEED-request-single-chunk",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 107575580,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 107575580944757,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 304,
            "profile": "nginx-native",
            "result": 0,
            "run": "20261014-nginx-need-single-chunk",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "2-1",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792017209370350203,
            "wall_sample_end_monotonic_ns": 107575580944862
          }
        ],
        "native_logging": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 50,
            "canonical_transaction_id": null,
            "case": "I12::nginx-native::NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_logging",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "2-1",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 107575581200853,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 304,
            "profile": "nginx-native",
            "result": 1,
            "run": "20261014-nginx-need-single-chunk",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 51,
            "transaction_id": "2-1",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792017209370606429,
            "wall_sample_end_monotonic_ns": 107575581201100
          }
        ]
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2311,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/physical-host.jsonl",
          "role": "host_callback",
          "sha256": "86185f008fb36ea2d80413972bc1598fda98de02e2f385c81fd171e075a3664e"
        }
      ],
      "value": {
        "request": {
          "allocation_scope_call": 2,
          "connection_sent": 0,
          "fd_count": 15,
          "header_sent": 0,
          "last_buf": 1,
          "last_in_chain": 0,
          "monotonic_ns": 107575577769143,
          "operation": "request_eos",
          "pid": 304,
          "realtime_ns": 1792017209367174595,
          "remaining": 0
        },
        "response": {
          "allocation_scope_call": 2,
          "connection_sent": 194,
          "fd_count": 15,
          "header_sent": 1,
          "last_buf": 1,
          "last_in_chain": 0,
          "monotonic_ns": 107575580234528,
          "operation": "response_eos",
          "pid": 304,
          "realtime_ns": 1792017209369640029,
          "remaining": -1
        },
        "response_remaining": null,
        "response_remaining_reason": "Response branch directly observes last_buf/last_in_chain; response remaining not exposed (-1 in raw)"
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 117281,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/physical-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "6c940f30ada64a172521dc46992c2ba9c4473cb5a6809c82465b725578dbcaaf"
        },
        {
          "bytes": 2311,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/physical-host.jsonl",
          "role": "host_callback",
          "sha256": "86185f008fb36ea2d80413972bc1598fda98de02e2f385c81fd171e075a3664e"
        }
      ],
      "value": {
        "append_api_eos_argument": null,
        "request_actual_source_branch": {
          "allocation_scope_call": 2,
          "connection_sent": 0,
          "fd_count": 15,
          "header_sent": 0,
          "last_buf": 1,
          "last_in_chain": 0,
          "monotonic_ns": 107575577769143,
          "operation": "request_eos",
          "pid": 304,
          "realtime_ns": 1792017209367174595,
          "remaining": 0
        },
        "request_native_finalization_enter": {
          "allocation_join_verified": true,
          "allocation_scope_call": 2,
          "allocation_scope_kind": "host",
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 22,
          "canonical_transaction_id": null,
          "case": "I12::nginx-native::NEED-request-single-chunk",
          "contract_state": null,
          "edge": "enter",
          "function": "native_process_request_body",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": "2-1",
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 3,
          "monotonic_ns": 107575577791223,
          "native_mime_selection": null,
          "pending_calls": 1,
          "phase": 2,
          "pid": 304,
          "profile": "nginx-native",
          "result": null,
          "run": "20261014-nginx-need-single-chunk",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 22,
          "transaction_id": "2-1",
          "transaction_id_origin": "sdk_public_m_id",
          "uid": 65534,
          "wall_ns": 1792017209367196670,
          "wall_sample_end_monotonic_ns": 107575577791318
        },
        "response_actual_source_branch": {
          "allocation_scope_call": 2,
          "connection_sent": 194,
          "fd_count": 15,
          "header_sent": 1,
          "last_buf": 1,
          "last_in_chain": 0,
          "monotonic_ns": 107575580234528,
          "operation": "response_eos",
          "pid": 304,
          "realtime_ns": 1792017209369640029,
          "remaining": -1
        },
        "response_native_finalization_enter": {
          "allocation_join_verified": true,
          "allocation_scope_call": 2,
          "allocation_scope_kind": "host",
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 42,
          "canonical_transaction_id": null,
          "case": "I12::nginx-native::NEED-request-single-chunk",
          "contract_state": null,
          "edge": "enter",
          "function": "native_process_response_body",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": "2-1",
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 3,
          "monotonic_ns": 107575580309902,
          "native_mime_selection": null,
          "pending_calls": 1,
          "phase": 4,
          "pid": 304,
          "profile": "nginx-native",
          "result": null,
          "run": "20261014-nginx-need-single-chunk",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 42,
          "transaction_id": "2-1",
          "transaction_id_origin": "sdk_public_m_id",
          "uid": 65534,
          "wall_ns": 1792017209369715346,
          "wall_sample_end_monotonic_ns": 107575580309994
        },
        "scope": "Host terminal callback precedes actual native phase finalization; append API has no EOS argument, no synthetic native EOS boolean"
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 117281,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/physical-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "6c940f30ada64a172521dc46992c2ba9c4473cb5a6809c82465b725578dbcaaf"
        }
      ],
      "value": {
        "actual_calls": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 54,
            "canonical_transaction_id": null,
            "case": "I12::nginx-native::NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "2-1",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 2,
            "monotonic_ns": 107575581495369,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 304,
            "profile": "nginx-native",
            "result": null,
            "run": "20261014-nginx-need-single-chunk",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 55,
            "transaction_id": "2-1",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792017209370900835,
            "wall_sample_end_monotonic_ns": 107575581495495
          }
        ],
        "count": 1,
        "void_return_is_not_synthetic_zero": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 29786,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/worker-self-maps.raw",
          "role": "loaded_image",
          "sha256": "707a7de07c8aef8d4d54a0c9f8c84521caaacd2295842baa32567ce1dc1a62ee"
        },
        {
          "bytes": 4560,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "ef1511ea494fd6c9157cc8329fd4a4524add23a51ba4f660e7880dc96a71b504"
        }
      ],
      "value": {
        "all_file_backed_images": [
          {
            "inode": 51167691,
            "mode": "0o444",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/sealed-common-inputs/artifacts/nginx/sdk/lib/libmodsecurity.so.3",
            "runtime_path": "/mnt/artifacts/nginx/sdk/lib/libmodsecurity.so.3",
            "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
          },
          {
            "inode": 21594968,
            "mode": "0o755",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2",
            "sha256": "bda779ea9e9ad234f60315477d7cfd0bdde861cd8ddd9df8cdaf62f18c4cec14"
          },
          {
            "inode": 16208387,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libGeoIP.so.1.6.12",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libGeoIP.so.1.6.12",
            "sha256": "fd7579ebc1026a776b62a7df4e49e40af92bbe26793ac33875d4f4f3a49a5a92"
          },
          {
            "inode": 28479,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1.2.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1.2.0",
            "sha256": "fb353cab2ea4ecd90814b46f872c21e1034c92bd86c3c677415748b4d16b5ad1"
          },
          {
            "inode": 28480,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libbrotlidec.so.1.2.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libbrotlidec.so.1.2.0",
            "sha256": "eb8768f85e9c367cd74772919b5668bbe0045cb71b65d75aafc32828e7acb1b7"
          },
          {
            "inode": 21594971,
            "mode": "0o755",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libc.so.6",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libc.so.6",
            "sha256": "85e64f97e348786a8fb4d9f3d52fec289e2fb86bba20f0731dfe61990525e0f7"
          },
          {
            "inode": 28494,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libcom_err.so.2.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libcom_err.so.2.1",
            "sha256": "6fb3115b11fe7e14c26f3e086c4dc1fb41061130869a66c976e0ea69fdb912d6"
          },
          {
            "inode": 28495,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libcrypt.so.1.1.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libcrypt.so.1.1.0",
            "sha256": "212437df8afcd4004965550cb6df2d0eeb8cad736f7a13a89dcec455182429a6"
          },
          {
            "inode": 22767765,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libcrypto.so.3",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libcrypto.so.3",
            "sha256": "5385f0436ac2e284ba8c5fb1488874057c29c04be72dea32add832694f381e28"
          },
          {
            "inode": 22539861,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.4.8.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.4.8.0",
            "sha256": "3c2a221cca206fdc9f950799d4dfce8b3408a69b280caae9455f182fe957403d"
          },
          {
            "inode": 28526,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libffi.so.8.2.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libffi.so.8.2.0",
            "sha256": "1a0dc86f787f73e025a6e521056360afcbe70f2a82cd808132fefc2b4ee95daa"
          },
          {
            "inode": 141553,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libfuzzy.so.2.1.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libfuzzy.so.2.1.0",
            "sha256": "c9ceac0a951a108a22199a22b9c69a48810dc2fac89a417e9723b30bb6e1aa21"
          },
          {
            "inode": 28533,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libgcc_s.so.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libgcc_s.so.1",
            "sha256": "9d339ecb409578d6a5d587e6c537a8f9589b8a13fefba30d167433a4b5758bee"
          },
          {
            "inode": 28541,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libgmp.so.10.5.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libgmp.so.10.5.0",
            "sha256": "fda9699eef15deda5f1c626e9140377a7f5d88c41516a54278ac02429cb20fa5"
          },
          {
            "inode": 130585,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libgnutls.so.30.41.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libgnutls.so.30.41.1",
            "sha256": "ebcc6a4dfae904dc956feb61cef5c36917cf36c19c5718d3c2be7e377ac65d27"
          },
          {
            "inode": 13264472,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2.2",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2.2",
            "sha256": "18e2ba0b2f421b780e7265337e52996f382857df63d0f9e63f391a75a14cdbe7"
          },
          {
            "inode": 28556,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libhogweed.so.6.11",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libhogweed.so.6.11",
            "sha256": "67bdc12f1ffe643142d5e185a6a8f654fd38cd14e77bae68201cf9aa71b00b61"
          },
          {
            "inode": 28563,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libidn2.so.0.4.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libidn2.so.0.4.0",
            "sha256": "cdb48484c43a795c3722e286c31eb6238b4b7c3780043895dd9fa6b6041f78da"
          },
          {
            "inode": 13264449,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libk5crypto.so.3.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libk5crypto.so.3.1",
            "sha256": "ee77156da39841edfaa7c5fcdca4cf98ae34d60323095617b484188a4d9965e3"
          },
          {
            "inode": 28571,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libkeyutils.so.1.10",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libkeyutils.so.1.10",
            "sha256": "c0c8f8d5adec4abe76fa462d8ad7c010f50c61e2b67b9feaa6f44e462c12cf41"
          },
          {
            "inode": 13264546,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libkrb5.so.3.3",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libkrb5.so.3.3",
            "sha256": "aca607790a4349c5053390fa22b24e717b2c5ea101d7b468ece6507140c6ff7b"
          },
          {
            "inode": 13264590,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libkrb5support.so.0.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libkrb5support.so.0.1",
            "sha256": "8cc61cecc016710e7134c1621b5a6537c55eea91d2a074f6f05fa6f6e36ec8d6"
          },
          {
            "inode": 28576,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/liblber.so.2.0.200",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/liblber.so.2.0.200",
            "sha256": "e2f9e23d75b37be7bdcdc39d2f74e2355a68f2ccd86e7f6534969ad8b359834b"
          },
          {
            "inode": 28577,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libldap.so.2.0.200",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libldap.so.2.0.200",
            "sha256": "0aa894b6d72690723015f6056bb6730a1cca41a2fac8224ef38cd7880c8e7860"
          },
          {
            "inode": 16208403,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/liblua5.3.so.0.0.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/liblua5.3.so.0.0.0",
            "sha256": "05f466dd2d7966fb695eed7bf33f07715df650c881d74554982d40ea50cff3ef"
          },
          {
            "inode": 21594974,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libm.so.6",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libm.so.6",
            "sha256": "1c488db6f4fe8cecb72456bc018de000b7a9b539c2994864b0416b5e8371b3d8"
          },
          {
            "inode": 133037,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libmaxminddb.so.0.0.7",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libmaxminddb.so.0.0.7",
            "sha256": "364e2e9a13ca94aec1af1932a80bdfe8428954169e051b81e05ca8229047280e"
          },
          {
            "inode": 28598,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libnettle.so.8.11",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libnettle.so.8.11",
            "sha256": "68c2f760d329a85ce1aa5cfc5e48ffece235258159005726798ad14e6f96a789"
          },
          {
            "inode": 4606878,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libnghttp2.so.14.29.2",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libnghttp2.so.14.29.2",
            "sha256": "2655558fee787cb4724ad59c72ce75b20847efc92a1c52fc202aea1d812c9b20"
          },
          {
            "inode": 28612,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libp11-kit.so.0.4.8",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libp11-kit.so.0.4.8",
            "sha256": "2611eeb039dbed48839d90afe3d9ad3e5bd9edca2989af05dc62a93c3ff41fed"
          },
          {
            "inode": 28620,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libpcre2-8.so.0.14.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libpcre2-8.so.0.14.0",
            "sha256": "4a6b6b2078685b074869d75cb068664d7da6b3036df7bca0442b1bbbd4ac7e65"
          },
          {
            "inode": 28628,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libpsl.so.5.3.4",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libpsl.so.5.3.4",
            "sha256": "18d125c725a498d66f971ceb60bfc7cf660f6a0149b54e5caa3f4651c3d2b3c6"
          },
          {
            "inode": 21594984,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libresolv.so.2",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libresolv.so.2",
            "sha256": "6b99ecf94bcb81732ed1e81615084a5cfe7383eb89ce83106fa51077409ce609"
          },
          {
            "inode": 28639,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/librtmp.so.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/librtmp.so.1",
            "sha256": "fceac319eac32ab0d6e9d6d641f0abf2f4aa097aa1a1355ea9e7419e81d45b62"
          },
          {
            "inode": 28640,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libsasl2.so.2.0.25",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libsasl2.so.2.0.25",
            "sha256": "25163eb0a23ffe7d4170f9e219886dfdb831bbb1031a2cfac2227284a7f51e02"
          },
          {
            "inode": 21363154,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libssh2.so.1.0.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libssh2.so.1.0.1",
            "sha256": "34287a1e8942e6fdf1c154e8c615a8dab7a69dc6a4e8d76913afb323fdc6fd6f"
          },
          {
            "inode": 22767766,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libssl.so.3",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libssl.so.3",
            "sha256": "63b47f444efa588e291e9b650a5ba2ab02f856356f2d50f13a2e477db9119e09"
          },
          {
            "inode": 28654,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.35",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.35",
            "sha256": "5bb0d21308f123b6ad46c6f35b42cedfcb8d6d439a53aa3dae04d880aaffdde3"
          },
          {
            "inode": 28657,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libtasn1.so.6.6.5",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libtasn1.so.6.6.5",
            "sha256": "1255353abfae7b9f52aedb0264876cd4c852f13c2acf3e2203ebd2aab79bce02"
          },
          {
            "inode": 28665,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libunistring.so.5.2.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libunistring.so.5.2.0",
            "sha256": "c762a289c02f716a12549d544a811715126067b9a6377057671d3fad9453a1fc"
          },
          {
            "inode": 23309947,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libxml2.so.16.1.2",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libxml2.so.16.1.2",
            "sha256": "302dfa1295c6f917758243ef0f118f7144026b51a5f5cd1610fba849c968f73b"
          },
          {
            "inode": 141923,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libyajl.so.2.1.0",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libyajl.so.2.1.0",
            "sha256": "c54f554ef49cc941d85d56714930d06f39e44bb8968cecb2ee52503c834df04d"
          },
          {
            "inode": 21270049,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libz.so.1.3.1",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libz.so.1.3.1",
            "sha256": "47b61967895b30e8c0c6818dd633ffeb87711cf637c688f981896f0dd84ce23b"
          },
          {
            "inode": 28686,
            "mode": "0o644",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/usr/lib/x86_64-linux-gnu/libzstd.so.1.5.7",
            "runtime_path": "/usr/lib/x86_64-linux-gnu/libzstd.so.1.5.7",
            "sha256": "060eeb79531d435306665fd78329d8a9dd579f95876c5960bb67937825362a80"
          },
          {
            "inode": 51633798,
            "mode": "0o700",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/nginx-binary",
            "runtime_path": "/var/tmp/codex/ModSecurity-conector/nginx-need-single-chunk/observations/nginx-binary",
            "sha256": "0d2287b344a1af4c6cc986dd915c09c60f3c942ec8ae76f8bdc5456506939746"
          },
          {
            "inode": 51633799,
            "mode": "0o600",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/nginx-module.so",
            "runtime_path": "/var/tmp/codex/ModSecurity-conector/nginx-need-single-chunk/observations/nginx-module.so",
            "sha256": "f27f361f46c388f8a496ff18090f842c2c56e2d61f98de2d571ec3f2638ea191"
          },
          {
            "inode": 51633816,
            "mode": "0o600",
            "owner_gid": 0,
            "owner_uid": 0,
            "physical_source": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/worker-self-maps.so",
            "runtime_path": "/var/tmp/codex/ModSecurity-conector/nginx-need-single-chunk/observations/worker-self-maps.so",
            "sha256": "7d63d1602161d696fb2c6918360bd7e78e12f339e6d32f3dffafa437c1f89a28"
          }
        ],
        "host": "nginx/1.31.6",
        "host_binary_sha256": "0d2287b344a1af4c6cc986dd915c09c60f3c942ec8ae76f8bdc5456506939746",
        "module_sha256": "f27f361f46c388f8a496ff18090f842c2c56e2d61f98de2d571ec3f2638ea191",
        "roles": {
          "master_pid": 303,
          "master_uid": 0,
          "run_id": "20261014-nginx-need-single-chunk",
          "worker_pid": 304,
          "worker_uid": 65534
        },
        "sdk_release": "3.0.14",
        "sdk_release_binding": "Actual public m_id observer accessor requires msc_who_am_i3.0.14 before transaction dereference; SDK mapped file SHA pinned separately",
        "special_device_maps_not_executable_images": [
          "7d41daca3000-7d41daca4000 rw-s 00000000 00:01 7568                       /dev/zero (deleted)",
          "7d41db527000-7d41db528000 rw-s 00000000 00:01 7569                       /dev/zero (deleted)"
        ],
        "worker": {
          "bytes": 29692,
          "gid": 65534,
          "pid": 304,
          "ppid": 303,
          "starttime": 10757543,
          "uid": 65534,
          "version": 1
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 242247,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/nginx-lifecycle/source-8cc32dce-03-ledger.json",
          "role": "source_manifest",
          "sha256": "faacdf0e458a2f317fa50c4429683d912229ce0bdf84383103e1489e5824a8ed"
        },
        {
          "bytes": 1319,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/nginx.conf",
          "role": "effective_configuration",
          "sha256": "f6c7322a9dc9a8fac0019722f2904a3936aaf38c7efaa5db69286d3bfde30672"
        },
        {
          "bytes": 495,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017164911769753/data/nginx-need-single-chunk/observations/no-crs-baseline.conf",
          "role": "effective_configuration",
          "sha256": "3e7ad7c8ce461707a4e5d4ec4befe7ce98bffe972a40aac7adcf6cb6e86a4193"
        }
      ],
      "value": {
        "config_sha256": "f6c7322a9dc9a8fac0019722f2904a3936aaf38c7efaa5db69286d3bfde30672",
        "fixture_version": "09",
        "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
        "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
        "parent_sha": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
        "rules_sha256": "3e7ad7c8ce461707a4e5d4ec4befe7ce98bffe972a40aac7adcf6cb6e86a4193",
        "stable_observer_version": "37 wrappers sealed C52aba91/H5a34307; no current38 relabeling"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "f6c7322a9dc9a8fac0019722f2904a3936aaf38c7efaa5db69286d3bfde30672",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
    "product_contract_sha": null,
    "rules_sha256": "3e7ad7c8ce461707a4e5d4ec4befe7ce98bffe972a40aac7adcf6cb6e86a4193",
    "run_id": "20261014-nginx-need-single-chunk"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 257196,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-nginx-09-01.json",
    "sha256": "c0573aaab2114da8c93861eec71a98ab525c0d6fc9f4b4f7f99ed3ff2d62e1cb"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-native-htx::NEED-request-single-chunk

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3693,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "f9d2e0d0702187a166995dc13f4639c4a789163850bd29faa4a052e044ee3668"
        },
        {
          "bytes": 4538,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "c836ebb2c292808c48681e8e98d042a3fdc19f37943c9ec934bf63dd1c9d364a"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_and_common_cleanup_before_process_stop": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-single-chunk",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106685954562312,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-native-htx",
          "result": null,
          "run": "20261014-hap-predicate-direct-1",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016319743967824,
          "wall_sample_end_monotonic_ns": 106685954562477
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 107922,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "7a0dcebf6ad1f419b896a484f7705440d504b55ed0097ead837bc03aa420f6f4"
        }
      ],
      "value": {
        "actual_common_finish_calls": 1,
        "actual_common_finish_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-00000000065be080-0000000000000000",
            "case": "NEED-request-single-chunk",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 106684548,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106684548445765,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 0,
            "run": "20261014-hap-predicate-direct-1",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016318337851202,
            "wall_sample_end_monotonic_ns": 106684548445847
          }
        ],
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 4122,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "fe4ff98ecb91e933881e32e86399d489420ee8739e391d43b53cf758cda75d9b"
        },
        {
          "bytes": 4122,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "fe4ff98ecb91e933881e32e86399d489420ee8739e391d43b53cf758cda75d9b"
        }
      ],
      "value": {
        "actual_SPOP_registry_to_HTX_to_owner_native_scope_binding": null,
        "actual_callbacks": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016318335017696
          },
          {
            "channel_flags": 2684387329,
            "headers_committed": 1,
            "kind": "htx_response_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 1,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016318337246842
          }
        ],
        "definition": "HTX actual http_end; SPOP admitted complete finite Content-Length sample is an atomic request EOS representation, not a request streaming/TCP-close claim."
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 107922,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "7a0dcebf6ad1f419b896a484f7705440d504b55ed0097ead837bc03aa420f6f4"
        },
        {
          "bytes": 4122,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "fe4ff98ecb91e933881e32e86399d489420ee8739e391d43b53cf758cda75d9b"
        },
        {
          "bytes": 4122,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "fe4ff98ecb91e933881e32e86399d489420ee8739e391d43b53cf758cda75d9b"
        }
      ],
      "value": {
        "actual_host_handoff": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016318335017696
          },
          {
            "channel_flags": 2684387329,
            "headers_committed": 1,
            "kind": "htx_response_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 1,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016318337246842
          }
        ],
        "actual_native_P2_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 18,
            "canonical_transaction_id": null,
            "case": "NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106684545988660,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 1,
            "run": "20261014-hap-predicate-direct-1",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 19,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016318335394138,
            "wall_sample_end_monotonic_ns": 106684545988787
          }
        ],
        "actual_native_P4_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 38,
            "canonical_transaction_id": null,
            "case": "NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106684548066835,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 1,
            "run": "20261014-hap-predicate-direct-1",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 39,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016318337472305,
            "wall_sample_end_monotonic_ns": 106684548066957
          }
        ],
        "native_append_EOS_argument": null,
        "native_append_EOS_argument_reason": "Selected public native append API has no EOS argument; actual body-finalization callbacks measured independently.",
        "request_finalizations": 1,
        "response_finalizations": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 107922,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "7a0dcebf6ad1f419b896a484f7705440d504b55ed0097ead837bc03aa420f6f4"
        }
      ],
      "value": {
        "actual_sdk_cleanup_calls": 1,
        "actual_void_API_return_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106684548505479,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": null,
            "run": "20261014-hap-predicate-direct-1",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016318337910933,
            "wall_sample_end_monotonic_ns": 106684548505580
          }
        ],
        "void_return_is_not_numeric_unknown": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 28832,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/before-main.maps",
          "role": "loaded_image",
          "sha256": "0e346a78d5204e1983b2375ee5f2d7f849c1827b13c97230b1bae4f6c06c741f"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4538,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "c836ebb2c292808c48681e8e98d042a3fdc19f37943c9ec934bf63dd1c9d364a"
        }
      ],
      "value": {
        "actual_uid_gid_capabilities": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "agent_sha256": null,
        "host_sha256": "16c52af036f19f7bdb78781ab8eca5a36bbe7e99ca73fe9100b626330d409ae6",
        "host_version": "3.2.25",
        "loaded_native_sdk": {
          "actual_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "actual_public_id_accessor_version_guard": "3.0.14",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 3204,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/artifact-receipt.json",
          "role": "source_manifest",
          "sha256": "d0fb24bb177ec2a17bb91f1757102b303a300064437884e33ec50e4307bbb4bb"
        },
        {
          "bytes": 372,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        }
      ],
      "value": {
        "SDK_accessor_sha256": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
        "actual_isolation_attempt_nonce": "1792016258290531916",
        "actual_spec_sha256": "634da326846dab1408a9544a19accc1a4f864b019023408ff6ab343630e871bc",
        "compiled_wrap_symbols": 37,
        "configurations": {
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016258290531916/data/haproxy.cfg": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        },
        "delivery_parent": "02754040bced960cfc1857416cd7101bb3116ef4",
        "fixture_tls_CA_bound": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_header_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "original_runtime_product_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
        "scoped_product_inputs_equal_a9": 150,
        "source_test_overlays_declared": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "3fbd6ce0760fec8e5095106b3b178ba148d9f99a56dbed19acc5f5b23a08c527",
    "run_id": "20261014-hap-predicate-direct-1"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 166432,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-extension-v3-direct-1-01.json",
    "sha256": "8be02847b72f88a8ce50b93e33b9738dfec9b7fe88df93fdf9acaa85bd517a4f"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-native-htx::NEED-request-content-type-present

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3701,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "e1a2d487139e6c3eebad184f8c7c36dc4bc8812a50dfc7df099272a2edaf5d4a"
        },
        {
          "bytes": 4537,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "7aa62ccb1669967817e8adc84289391b64ba724ee15f752fe3ad7bb50deb3d6d"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_and_common_cleanup_before_process_stop": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-content-type-present",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106666998136933,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-native-htx",
          "result": null,
          "run": "20261014-hap-predicate-direct-3",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016300787542541,
          "wall_sample_end_monotonic_ns": 106666998137209
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 108770,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "2ccc73dac38cb57026313cabe26edf63daae53296b865dc5aeddfab8a2d05aa7"
        }
      ],
      "value": {
        "actual_common_finish_calls": 1,
        "actual_common_finish_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-00000000065b92bc-0000000000000000",
            "case": "NEED-request-content-type-present",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 106664640,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106664640732841,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 0,
            "run": "20261014-hap-predicate-direct-3",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016298430138295,
            "wall_sample_end_monotonic_ns": 106664640732945
          }
        ],
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 4064,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "abe98347e3aef056d8531eba49adf1d1220f5a568fcb082cba71a0b0b03446d7"
        },
        {
          "bytes": 4064,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "abe98347e3aef056d8531eba49adf1d1220f5a568fcb082cba71a0b0b03446d7"
        }
      ],
      "value": {
        "actual_SPOP_registry_to_HTX_to_owner_native_scope_binding": null,
        "actual_callbacks": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016298427118680
          },
          {
            "channel_flags": 2684387329,
            "headers_committed": 1,
            "kind": "htx_response_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 1,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016298429270077
          }
        ],
        "definition": "HTX actual http_end; SPOP admitted complete finite Content-Length sample is an atomic request EOS representation, not a request streaming/TCP-close claim."
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 108770,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "2ccc73dac38cb57026313cabe26edf63daae53296b865dc5aeddfab8a2d05aa7"
        },
        {
          "bytes": 4064,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "abe98347e3aef056d8531eba49adf1d1220f5a568fcb082cba71a0b0b03446d7"
        },
        {
          "bytes": 4064,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "abe98347e3aef056d8531eba49adf1d1220f5a568fcb082cba71a0b0b03446d7"
        }
      ],
      "value": {
        "actual_host_handoff": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016298427118680
          },
          {
            "channel_flags": 2684387329,
            "headers_committed": 1,
            "kind": "htx_response_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 1,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016298429270077
          }
        ],
        "actual_native_P2_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 18,
            "canonical_transaction_id": null,
            "case": "NEED-request-content-type-present",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106664637805541,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 1,
            "run": "20261014-hap-predicate-direct-3",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 19,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016298427210996,
            "wall_sample_end_monotonic_ns": 106664637805641
          }
        ],
        "actual_native_P4_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 38,
            "canonical_transaction_id": null,
            "case": "NEED-request-content-type-present",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106664640119021,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 1,
            "run": "20261014-hap-predicate-direct-3",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 39,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016298429524535,
            "wall_sample_end_monotonic_ns": 106664640119198
          }
        ],
        "native_append_EOS_argument": null,
        "native_append_EOS_argument_reason": "Selected public native append API has no EOS argument; actual body-finalization callbacks measured independently.",
        "request_finalizations": 1,
        "response_finalizations": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 108770,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "2ccc73dac38cb57026313cabe26edf63daae53296b865dc5aeddfab8a2d05aa7"
        }
      ],
      "value": {
        "actual_sdk_cleanup_calls": 1,
        "actual_void_API_return_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-request-content-type-present",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106664640875173,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": null,
            "run": "20261014-hap-predicate-direct-3",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016298430280651,
            "wall_sample_end_monotonic_ns": 106664640875305
          }
        ],
        "void_return_is_not_numeric_unknown": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 28734,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/before-main.maps",
          "role": "loaded_image",
          "sha256": "012dcf4efad380abb98b479157e4006127885338151f03d1d6d46db6f73f4272"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4537,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "7aa62ccb1669967817e8adc84289391b64ba724ee15f752fe3ad7bb50deb3d6d"
        }
      ],
      "value": {
        "actual_uid_gid_capabilities": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "agent_sha256": null,
        "host_sha256": "16c52af036f19f7bdb78781ab8eca5a36bbe7e99ca73fe9100b626330d409ae6",
        "host_version": "3.2.25",
        "loaded_native_sdk": {
          "actual_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "actual_public_id_accessor_version_guard": "3.0.14",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 3204,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/artifact-receipt.json",
          "role": "source_manifest",
          "sha256": "d0fb24bb177ec2a17bb91f1757102b303a300064437884e33ec50e4307bbb4bb"
        },
        {
          "bytes": 372,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        }
      ],
      "value": {
        "SDK_accessor_sha256": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
        "actual_isolation_attempt_nonce": "1792016265381079140",
        "actual_spec_sha256": "2898f782b0b29aab513ac443ead0edac34a4f75663acf680155e7c84f03e6cb7",
        "compiled_wrap_symbols": 37,
        "configurations": {
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016265381079140/data/haproxy.cfg": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        },
        "delivery_parent": "02754040bced960cfc1857416cd7101bb3116ef4",
        "fixture_tls_CA_bound": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_header_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "original_runtime_product_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
        "scoped_product_inputs_equal_a9": 150,
        "source_test_overlays_declared": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "2180c6dbadcc52bbe6da03071f7237bb40a9c6be51b6c71b460b419f53b8c455",
    "run_id": "20261014-hap-predicate-direct-3"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 167085,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-extension-v3-direct-3-01.json",
    "sha256": "fb24dea8604d0ea4df51a4c2036f64d950a04db4ee15baeb279386ccb70079b2"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-native-htx::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3689,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "b4d7998878dda43a29849841e7886bc3fea2b6ab3bac75e6ab9fb6e0e58d3d4e"
        },
        {
          "bytes": 4519,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "8b76857702c826b625439550ede2141b8d02b9eba430371d0359b8509c706721"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_and_common_cleanup_before_process_stop": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-eos-once",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106393894979745,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-native-htx",
          "result": null,
          "run": "20261014-haproxy-htx-01",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016027684385329,
          "wall_sample_end_monotonic_ns": 106393894979995
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 106650,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "320e242b6437348944bb528b43d2472b475e3dd33f40029a4bd82d9e866e5f1d"
        }
      ],
      "value": {
        "actual_common_finish_calls": 1,
        "actual_common_finish_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-00000000065769e4-0000000000000000",
            "case": "NEED-request-eos-once",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 106392039,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106392039925771,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 0,
            "run": "20261014-haproxy-htx-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016025829331203,
            "wall_sample_end_monotonic_ns": 106392039925849
          }
        ],
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3028,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "381ec40a05175534fd8e8c1e308ad43454635c141e2cb2d7c79db8173bc2f2da"
        },
        {
          "bytes": 3028,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "381ec40a05175534fd8e8c1e308ad43454635c141e2cb2d7c79db8173bc2f2da"
        }
      ],
      "value": {
        "actual_SPOP_registry_to_HTX_to_owner_native_scope_binding": null,
        "actual_callbacks": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016025826745379
          },
          {
            "channel_flags": 2684387329,
            "headers_committed": 1,
            "kind": "htx_response_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 1,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016025828857633
          }
        ],
        "definition": "HTX actual http_end; SPOP admitted complete finite Content-Length sample is an atomic request EOS representation, not a request streaming/TCP-close claim."
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 106650,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "320e242b6437348944bb528b43d2472b475e3dd33f40029a4bd82d9e866e5f1d"
        },
        {
          "bytes": 3028,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "381ec40a05175534fd8e8c1e308ad43454635c141e2cb2d7c79db8173bc2f2da"
        },
        {
          "bytes": 3028,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "381ec40a05175534fd8e8c1e308ad43454635c141e2cb2d7c79db8173bc2f2da"
        }
      ],
      "value": {
        "actual_host_handoff": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016025826745379
          },
          {
            "channel_flags": 2684387329,
            "headers_committed": 1,
            "kind": "htx_response_http_end",
            "producer_tag": "HAPROXY_LIFECYCLE",
            "request_finished": 1,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792016025828857633
          }
        ],
        "actual_native_P2_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 18,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106392037423516,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 1,
            "run": "20261014-haproxy-htx-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 19,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016025826828961,
            "wall_sample_end_monotonic_ns": 106392037423604
          }
        ],
        "actual_native_P4_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 38,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106392039611168,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 1,
            "run": "20261014-haproxy-htx-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 39,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016025829016629,
            "wall_sample_end_monotonic_ns": 106392039611272
          }
        ],
        "native_append_EOS_argument": null,
        "native_append_EOS_argument_reason": "Selected public native append API has no EOS argument; actual body-finalization callbacks measured independently.",
        "request_finalizations": 1,
        "response_finalizations": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 106650,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "320e242b6437348944bb528b43d2472b475e3dd33f40029a4bd82d9e866e5f1d"
        }
      ],
      "value": {
        "actual_sdk_cleanup_calls": 1,
        "actual_void_API_return_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106392039982422,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": null,
            "run": "20261014-haproxy-htx-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016025829387858,
            "wall_sample_end_monotonic_ns": 106392039982500
          }
        ],
        "void_return_is_not_numeric_unknown": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 28832,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/before-main.maps",
          "role": "loaded_image",
          "sha256": "8314aed694a83880393c43aa43a5e374002ac4bdfa534d35abf21e4a2eb4b266"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4519,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "8b76857702c826b625439550ede2141b8d02b9eba430371d0359b8509c706721"
        }
      ],
      "value": {
        "actual_uid_gid_capabilities": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "agent_sha256": null,
        "host_sha256": "16c52af036f19f7bdb78781ab8eca5a36bbe7e99ca73fe9100b626330d409ae6",
        "host_version": "3.2.25",
        "loaded_native_sdk": {
          "actual_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "actual_public_id_accessor_version_guard": "3.0.14",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 3204,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/artifact-receipt.json",
          "role": "source_manifest",
          "sha256": "d0fb24bb177ec2a17bb91f1757102b303a300064437884e33ec50e4307bbb4bb"
        },
        {
          "bytes": 372,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        }
      ],
      "value": {
        "SDK_accessor_sha256": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
        "actual_isolation_attempt_nonce": "1792015978466894736",
        "actual_spec_sha256": "df5257eb41f58bdda94150f220b08d7ca6ae651954004b790a6929894fb0bf69",
        "compiled_wrap_symbols": 37,
        "configurations": {
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015978466894736/data/haproxy.cfg": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        },
        "delivery_parent": "02754040bced960cfc1857416cd7101bb3116ef4",
        "fixture_tls_CA_bound": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_header_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "original_runtime_product_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
        "scoped_product_inputs_equal_a9": 150,
        "source_test_overlays_declared": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "eaa6afdd0a2d1791448c9d8f21ff51736676709b9b587b670aa94102ce3fdbed",
    "run_id": "20261014-haproxy-htx-01"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 162340,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-v8-direct-01.json",
    "sha256": "64e6bd6896be9b3738ebf1661652c0baa25aa3c555dfd3d662aaf218a9b9edba"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-native-htx::NEED-request-reject

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3687,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "36e5cc85fa7aa69443749d068eeabf2aa52d80a3a6a04c5d37702bb146d7bd25"
        },
        {
          "bytes": 4561,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "4f058becfda5bc93a83109981d2ede163c66a19ac01b1f60f6a184bed3b2527c"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-reject",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 107774100339426,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-native-htx",
          "result": null,
          "run": "20261014-hap-native-limit-1",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 86,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792017407889744961,
          "wall_sample_end_monotonic_ns": 107774100339619
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 86202,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "4545646329b02622d2504ebcd1550c873780692919b08d626d53a154a30c6abd"
        }
      ],
      "value": {
        "actual_Common_finish": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 26,
            "canonical_transaction_id": "txc-00000000066c7a4c-0000000000000000",
            "case": "NEED-request-reject",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 107772493,
              "completed_phase_mask": 3,
              "last_completed_phase": 3,
              "response_committed": 0,
              "status": 5
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 107772494100459,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 0,
            "run": "20261014-hap-native-limit-1",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 27,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792017406283505890,
            "wall_sample_end_monotonic_ns": 107772494100534
          }
        ],
        "actual_Common_finish_calls": 1,
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2614,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "27a76b0ec344c79c239778e07bf59d043a2f67cc01a0bb9eed9fb6e7ef719825"
        }
      ],
      "value": {
        "P4_HTX_NA_reason": "Request locally denied before native response path",
        "actual_own_HTX_http_end_callbacks": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792017406283014409
          }
        ]
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 86202,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "4545646329b02622d2504ebcd1550c873780692919b08d626d53a154a30c6abd"
        },
        {
          "bytes": 2614,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "27a76b0ec344c79c239778e07bf59d043a2f67cc01a0bb9eed9fb6e7ef719825"
        }
      ],
      "value": {
        "actual_request_finalizations": 1,
        "actual_response_finalizations": 0,
        "no_TCPclose_inferred_nativeEOS": true,
        "response_NA_reason": "Native P2 deny terminates before P3/P4",
        "response_applicable": false
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 86202,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "4545646329b02622d2504ebcd1550c873780692919b08d626d53a154a30c6abd"
        }
      ],
      "value": {
        "actual_cleanup_calls": 1,
        "actual_independent_neighbor_free_once": true,
        "actual_void_cleanup_return": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 28,
            "canonical_transaction_id": null,
            "case": "NEED-request-reject",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 107772494163179,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": null,
            "run": "20261014-hap-native-limit-1",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 29,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792017406283568619,
            "wall_sample_end_monotonic_ns": 107772494163260
          }
        ],
        "void_result_NA_reason": "Public SDK cleanup is void; no numeric return fabricated"
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 28685,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/before-main.maps",
          "role": "loaded_image",
          "sha256": "2c3a40395b4efbff54446713b4380161474c5897a79d79bece1a14d65432caea"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4561,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "4f058becfda5bc93a83109981d2ede163c66a19ac01b1f60f6a184bed3b2527c"
        }
      ],
      "value": {
        "actual_UID_GID_caps": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "actual_loaded_SDK_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
        "actual_loaded_SDK_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
        "host_sha256": "16c52af036f19f7bdb78781ab8eca5a36bbe7e99ca73fe9100b626330d409ae6",
        "host_version": "3.2.25"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 372,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        },
        {
          "bytes": 516,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017351105532218/data/rules.conf",
          "role": "effective_configuration",
          "sha256": "3a4a43820e50a54b0653155370abef66c808f5e2fcac0c5c93a5dced12606649"
        }
      ],
      "value": {
        "actual_attempt_nonce": "1792017351105532218",
        "actual_rules_byte_equal_sealed_fixture_source": true,
        "actual_spec_sha256": "6ce94a777b5fd8b6a9910905790bb9e52c6c5f0ff25eae3dd14af937777a2dfa",
        "native_limit16_NoFiles1024_transport_caps_unchanged": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_H_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "wrapped_symbols": 37
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "3a4a43820e50a54b0653155370abef66c808f5e2fcac0c5c93a5dced12606649",
    "run_id": "20261014-hap-native-limit-1"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 111423,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-native-limit-reject-01.json",
    "sha256": "7c73162806574e32da69b79f8211b552749bee79bcf1343a3f8820ab3eb51b25"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-native-htx::NEED-request-process-partial

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3696,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "07f012a24df1af671dd19ec66c60cf619d9d1056f8dd947aa71786cc4e0ac334"
        },
        {
          "bytes": 4561,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "3ea77c097f1f08b046e24e35350d694899782fe437da5fa7b3c69b3180686cf7"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-process-partial",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 107766128617155,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-native-htx",
          "result": null,
          "run": "20261014-hap-native-limit-2",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792017399918022682,
          "wall_sample_end_monotonic_ns": 107766128617362
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 107814,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "82fdb2efb49ce8b53c4b6ce4ce71508c362adc56433df8df9326068c4ab119e5"
        }
      ],
      "value": {
        "actual_Common_finish": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-00000000066c5946-0000000000000000",
            "case": "NEED-request-process-partial",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 107764045,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 107764045485487,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": 0,
            "run": "20261014-hap-native-limit-2",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792017397834890922,
            "wall_sample_end_monotonic_ns": 107764045485567
          }
        ],
        "actual_Common_finish_calls": 1,
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 4599,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "6b295d1f0bd0ef36d594335ae6163ac29450567688464024155b5696d0a9dab4"
        }
      ],
      "value": {
        "P4_HTX_NA_reason": null,
        "actual_own_HTX_http_end_callbacks": [
          {
            "channel_flags": 545292289,
            "headers_committed": 0,
            "kind": "htx_request_http_end",
            "request_finished": 0,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792017397830930058
          },
          {
            "channel_flags": 2684387329,
            "headers_committed": 1,
            "kind": "htx_response_http_end",
            "request_finished": 1,
            "response_finished": 0,
            "scope_call": 2,
            "wall_ns": 1792017397834240072
          }
        ]
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 107814,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "82fdb2efb49ce8b53c4b6ce4ce71508c362adc56433df8df9326068c4ab119e5"
        },
        {
          "bytes": 4599,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "6b295d1f0bd0ef36d594335ae6163ac29450567688464024155b5696d0a9dab4"
        }
      ],
      "value": {
        "actual_request_finalizations": 1,
        "actual_response_finalizations": 1,
        "no_TCPclose_inferred_nativeEOS": true,
        "response_NA_reason": null,
        "response_applicable": true
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 107814,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "82fdb2efb49ce8b53c4b6ce4ce71508c362adc56433df8df9326068c4ab119e5"
        }
      ],
      "value": {
        "actual_cleanup_calls": 1,
        "actual_independent_neighbor_free_once": true,
        "actual_void_cleanup_return": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-request-process-partial",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "haproxy-htx-0",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 107764045546382,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-native-htx",
            "result": null,
            "run": "20261014-hap-native-limit-2",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "haproxy-htx-0",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792017397834951828,
            "wall_sample_end_monotonic_ns": 107764045546473
          }
        ],
        "void_result_NA_reason": "Public SDK cleanup is void; no numeric return fabricated"
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 28832,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/before-main.maps",
          "role": "loaded_image",
          "sha256": "b70b3290169e48a616fae869363c151584f4e50ae59e52b57e45b0b3fe82b7ff"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4561,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "3ea77c097f1f08b046e24e35350d694899782fe437da5fa7b3c69b3180686cf7"
        }
      ],
      "value": {
        "actual_UID_GID_caps": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "actual_loaded_SDK_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
        "actual_loaded_SDK_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
        "host_sha256": "16c52af036f19f7bdb78781ab8eca5a36bbe7e99ca73fe9100b626330d409ae6",
        "host_version": "3.2.25"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 372,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3"
        },
        {
          "bytes": 897,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017354183088048/data/rules.conf",
          "role": "effective_configuration",
          "sha256": "7ba45dab995ad043799cf734cacf19a5fabb42e57e4c5e74bb20cb58d0fed942"
        }
      ],
      "value": {
        "actual_attempt_nonce": "1792017354183088048",
        "actual_rules_byte_equal_sealed_fixture_source": true,
        "actual_spec_sha256": "05fc204e048b886cd3566d688adb1ae2994c3c0902f967f63b9933523a586052",
        "native_limit16_NoFiles1024_transport_caps_unchanged": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_H_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "wrapped_symbols": 37
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8cda0d15d9d28cf1858169208a3261c89ffc82d2a46dda61dee5a18345588df3",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "7ba45dab995ad043799cf734cacf19a5fabb42e57e4c5e74bb20cb58d0fed942",
    "run_id": "20261014-hap-native-limit-2"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 157462,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-native-limit-partial-01.json",
    "sha256": "786ec599372becdaebb5aeb9a639387cc98c419986590b265dfdba2bfb6b9f1b"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-spop-request::NEED-request-single-chunk

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 5255,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "5bac6d4c44e1dd50505b8eca475ed279133a239c5560aedd6573dfef1602b3ac"
        },
        {
          "bytes": 4537,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "a55c871e7b6fce396a85e136eb2f841b7662f7d37b750c3cb446909325881c65"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_and_common_cleanup_before_process_stop": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-single-chunk",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106678237552268,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-spop-request",
          "result": null,
          "run": "20261014-hap-predicate-request-2",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016312026957787,
          "wall_sample_end_monotonic_ns": 106678237552438
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 310,
            "reaped": true,
            "signal": null
          },
          {
            "exit": 0,
            "label": "agent-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 111690,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "cc6b0c0c1665c9b7bd01207c1e036e51b6748ecd08f440e464830d9ee1f8ced9"
        }
      ],
      "value": {
        "actual_common_finish_calls": 1,
        "actual_common_finish_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-00000000065bbef3-0000000000000000",
            "case": "NEED-request-single-chunk",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 106676016,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106676016101474,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 0,
            "run": "20261014-hap-predicate-request-2",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "1b1dd0dd-e53a-439c-bd32-5db48cb8f2b2",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016309805506916,
            "wall_sample_end_monotonic_ns": 106676016101563
          }
        ],
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "ab02cfee55b4b3e523421407670e403514941ab99b75b22590da9e28ff3d2715"
        },
        {
          "bytes": 4880,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent.stderr",
          "role": "host_callback",
          "sha256": "6bd8df028638b82f712df9b8a234e4e753d9458ae1b79980b25ac733e5927541"
        }
      ],
      "value": {
        "actual_SPOP_registry_to_HTX_to_owner_native_scope_binding": {
          "actual_HTX_response_http_end": {
            "actual_operation": 2684387329,
            "capability_sha256": "2d54380a03b267f693172b5eb788e81dd01bf66a2ebb6f4e3eaf3b0cd59666cb",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016309803971821
          },
          "actual_owner_EOS_received": {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016309804279128
          },
          "actual_request_evaluated": {
            "kind": "spop_atomic_request_evaluated",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 2,
            "wall_ns": 1792016309745984490
          },
          "finite_request_sample_accepted": {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016309744168114
          },
          "opaque_capability_raw_not_retained": true,
          "owner_registry_handoff": {
            "actual_operation": 0,
            "capability_sha256": "2d54380a03b267f693172b5eb788e81dd01bf66a2ebb6f4e3eaf3b0cd59666cb",
            "kind": "spop_registry_handoff",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 2,
            "wall_ns": 1792016309748270082
          },
          "shared_Runtime_session_claim_not_made": true
        },
        "actual_callbacks": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016309744168114
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "2d54380a03b267f693172b5eb788e81dd01bf66a2ebb6f4e3eaf3b0cd59666cb",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016309803971821
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016309804279128
          }
        ],
        "definition": "HTX actual http_end; SPOP admitted complete finite Content-Length sample is an atomic request EOS representation, not a request streaming/TCP-close claim."
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 111690,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "cc6b0c0c1665c9b7bd01207c1e036e51b6748ecd08f440e464830d9ee1f8ced9"
        },
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "ab02cfee55b4b3e523421407670e403514941ab99b75b22590da9e28ff3d2715"
        },
        {
          "bytes": 4880,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent.stderr",
          "role": "host_callback",
          "sha256": "6bd8df028638b82f712df9b8a234e4e753d9458ae1b79980b25ac733e5927541"
        }
      ],
      "value": {
        "actual_host_handoff": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016309744168114
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "2d54380a03b267f693172b5eb788e81dd01bf66a2ebb6f4e3eaf3b0cd59666cb",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016309803971821
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016309804279128
          }
        ],
        "actual_native_P2_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 18,
            "canonical_transaction_id": null,
            "case": "NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "1b1dd0dd-e53a-439c-bd32-5db48cb8f2b2",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106675956475936,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 1,
            "run": "20261014-hap-predicate-request-2",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 19,
            "transaction_id": "1b1dd0dd-e53a-439c-bd32-5db48cb8f2b2",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016309745881415,
            "wall_sample_end_monotonic_ns": 106675956476066
          }
        ],
        "actual_native_P4_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 38,
            "canonical_transaction_id": null,
            "case": "NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "1b1dd0dd-e53a-439c-bd32-5db48cb8f2b2",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106676015132817,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 1,
            "run": "20261014-hap-predicate-request-2",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 39,
            "transaction_id": "1b1dd0dd-e53a-439c-bd32-5db48cb8f2b2",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016309804538281,
            "wall_sample_end_monotonic_ns": 106676015132933
          }
        ],
        "native_append_EOS_argument": null,
        "native_append_EOS_argument_reason": "Selected public native append API has no EOS argument; actual body-finalization callbacks measured independently.",
        "request_finalizations": 1,
        "response_finalizations": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 111690,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "cc6b0c0c1665c9b7bd01207c1e036e51b6748ecd08f440e464830d9ee1f8ced9"
        }
      ],
      "value": {
        "actual_sdk_cleanup_calls": 1,
        "actual_void_API_return_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-request-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "1b1dd0dd-e53a-439c-bd32-5db48cb8f2b2",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106676016183753,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": null,
            "run": "20261014-hap-predicate-request-2",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "1b1dd0dd-e53a-439c-bd32-5db48cb8f2b2",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016309805589207,
            "wall_sample_end_monotonic_ns": 106676016183852
          }
        ],
        "void_return_is_not_numeric_unknown": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 27388,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent-before-main.maps",
          "role": "loaded_image",
          "sha256": "a3e12887f5fa961cd45e430152603ef746568bd713951f6c6dda6f3fcd1493e5"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4537,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "a55c871e7b6fce396a85e136eb2f841b7662f7d37b750c3cb446909325881c65"
        }
      ],
      "value": {
        "actual_uid_gid_capabilities": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "agent_sha256": "10d8d9f3d0422c9ce745d6a5566b2bff07f82372daba25b2c4efc02046e79b34",
        "host_sha256": "88aaff32806f256db0fe9c69b7c4e848fb6bb5deb16cb5dd06867d039be074e7",
        "host_version": "3.2.25",
        "loaded_native_sdk": {
          "actual_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "actual_public_id_accessor_version_guard": "3.0.14",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 3204,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/artifact-receipt.json",
          "role": "source_manifest",
          "sha256": "d0fb24bb177ec2a17bb91f1757102b303a300064437884e33ec50e4307bbb4bb"
        },
        {
          "bytes": 968,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e"
        },
        {
          "bytes": 411,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent.conf",
          "role": "effective_configuration",
          "sha256": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc"
        },
        {
          "bytes": 666,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/spoe.cfg",
          "role": "effective_configuration",
          "sha256": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        }
      ],
      "value": {
        "SDK_accessor_sha256": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
        "actual_isolation_attempt_nonce": "1792016261810346941",
        "actual_spec_sha256": "4015f639f2dbea297698b8ff78ed8dfbfa0408aeccf11180069cad85101ba576",
        "compiled_wrap_symbols": 37,
        "configurations": {
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/agent.conf": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/haproxy.cfg": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016261810346941/data/spoe.cfg": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        },
        "delivery_parent": "02754040bced960cfc1857416cd7101bb3116ef4",
        "fixture_tls_CA_bound": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_header_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "original_runtime_product_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
        "scoped_product_inputs_equal_a9": 150,
        "source_test_overlays_declared": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "3fbd6ce0760fec8e5095106b3b178ba148d9f99a56dbed19acc5f5b23a08c527",
    "run_id": "20261014-hap-predicate-request-2"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 174551,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-extension-v3-request-2-01.json",
    "sha256": "80ad51bd2a5cad5a589071ded8852a026da0a42c7ac3c3389b9d514e94e6b58e"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-spop-request::NEED-request-charset-missing

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 5258,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "3a78f7073bd53308250a8cad57edd1e8864cd01803d535977fc7598c7e1184a7"
        },
        {
          "bytes": 4537,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "f32fca283cbbc42c9a229c7b286dbcbec7898ba6b43a8a994326f70a94a1f8b3"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_and_common_cleanup_before_process_stop": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-charset-missing",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106681067620804,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-spop-request",
          "result": null,
          "run": "20261014-hap-predicate-request-4",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016314857026318,
          "wall_sample_end_monotonic_ns": 106681067620970
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 310,
            "reaped": true,
            "signal": null
          },
          {
            "exit": 0,
            "label": "agent-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 112008,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "869b8738ba4dd6f116bdc36703a6162db3081aee52b1b9ca185619d1c12d72a8"
        }
      ],
      "value": {
        "actual_common_finish_calls": 1,
        "actual_common_finish_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-00000000065bc872-0000000000000000",
            "case": "NEED-request-charset-missing",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 106678446,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106678446972434,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 0,
            "run": "20261014-hap-predicate-request-4",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "eb052019-b85e-4055-9320-c14e62c3bf50",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016312236377898,
            "wall_sample_end_monotonic_ns": 106678446972582
          }
        ],
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "51b901e842ec8c82313a385872cc5716baccab11ef4e38e0789f86e00ac8ec57"
        },
        {
          "bytes": 4822,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent.stderr",
          "role": "host_callback",
          "sha256": "c594e8f6a2cce008545b73bf6b72f28ead2da61d79121eab4d9dfbe3baef6386"
        }
      ],
      "value": {
        "actual_SPOP_registry_to_HTX_to_owner_native_scope_binding": {
          "actual_HTX_response_http_end": {
            "actual_operation": 2684387329,
            "capability_sha256": "73dd7ddc4a0f0ad0b961fbeacab4c9b3b6c8c9491580574229feee813d8acc9c",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016312234630509
          },
          "actual_owner_EOS_received": {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016312234951410
          },
          "actual_request_evaluated": {
            "kind": "spop_atomic_request_evaluated",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 2,
            "wall_ns": 1792016312177047556
          },
          "finite_request_sample_accepted": {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016312175628333
          },
          "opaque_capability_raw_not_retained": true,
          "owner_registry_handoff": {
            "actual_operation": 0,
            "capability_sha256": "73dd7ddc4a0f0ad0b961fbeacab4c9b3b6c8c9491580574229feee813d8acc9c",
            "kind": "spop_registry_handoff",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 2,
            "wall_ns": 1792016312179333623
          },
          "shared_Runtime_session_claim_not_made": true
        },
        "actual_callbacks": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016312175628333
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "73dd7ddc4a0f0ad0b961fbeacab4c9b3b6c8c9491580574229feee813d8acc9c",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016312234630509
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016312234951410
          }
        ],
        "definition": "HTX actual http_end; SPOP admitted complete finite Content-Length sample is an atomic request EOS representation, not a request streaming/TCP-close claim."
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 112008,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "869b8738ba4dd6f116bdc36703a6162db3081aee52b1b9ca185619d1c12d72a8"
        },
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "51b901e842ec8c82313a385872cc5716baccab11ef4e38e0789f86e00ac8ec57"
        },
        {
          "bytes": 4822,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent.stderr",
          "role": "host_callback",
          "sha256": "c594e8f6a2cce008545b73bf6b72f28ead2da61d79121eab4d9dfbe3baef6386"
        }
      ],
      "value": {
        "actual_host_handoff": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016312175628333
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "73dd7ddc4a0f0ad0b961fbeacab4c9b3b6c8c9491580574229feee813d8acc9c",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016312234630509
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016312234951410
          }
        ],
        "actual_native_P2_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 18,
            "canonical_transaction_id": null,
            "case": "NEED-request-charset-missing",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "eb052019-b85e-4055-9320-c14e62c3bf50",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106678387545335,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 1,
            "run": "20261014-hap-predicate-request-4",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 19,
            "transaction_id": "eb052019-b85e-4055-9320-c14e62c3bf50",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016312176950777,
            "wall_sample_end_monotonic_ns": 106678387545427
          }
        ],
        "actual_native_P4_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 38,
            "canonical_transaction_id": null,
            "case": "NEED-request-charset-missing",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "eb052019-b85e-4055-9320-c14e62c3bf50",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106678445880306,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 1,
            "run": "20261014-hap-predicate-request-4",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 39,
            "transaction_id": "eb052019-b85e-4055-9320-c14e62c3bf50",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016312235285810,
            "wall_sample_end_monotonic_ns": 106678445880493
          }
        ],
        "native_append_EOS_argument": null,
        "native_append_EOS_argument_reason": "Selected public native append API has no EOS argument; actual body-finalization callbacks measured independently.",
        "request_finalizations": 1,
        "response_finalizations": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 112008,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "869b8738ba4dd6f116bdc36703a6162db3081aee52b1b9ca185619d1c12d72a8"
        }
      ],
      "value": {
        "actual_sdk_cleanup_calls": 1,
        "actual_void_API_return_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-request-charset-missing",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "eb052019-b85e-4055-9320-c14e62c3bf50",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106678447127427,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": null,
            "run": "20261014-hap-predicate-request-4",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "eb052019-b85e-4055-9320-c14e62c3bf50",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016312236532906,
            "wall_sample_end_monotonic_ns": 106678447127582
          }
        ],
        "void_return_is_not_numeric_unknown": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 27241,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent-before-main.maps",
          "role": "loaded_image",
          "sha256": "0315e7317a4e26f28b5cf4ad4f8ce0ef01e8fe3ee493f8f9a9eb4006c1d5c224"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4537,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "f32fca283cbbc42c9a229c7b286dbcbec7898ba6b43a8a994326f70a94a1f8b3"
        }
      ],
      "value": {
        "actual_uid_gid_capabilities": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "agent_sha256": "10d8d9f3d0422c9ce745d6a5566b2bff07f82372daba25b2c4efc02046e79b34",
        "host_sha256": "88aaff32806f256db0fe9c69b7c4e848fb6bb5deb16cb5dd06867d039be074e7",
        "host_version": "3.2.25",
        "loaded_native_sdk": {
          "actual_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "actual_public_id_accessor_version_guard": "3.0.14",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 3204,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/artifact-receipt.json",
          "role": "source_manifest",
          "sha256": "d0fb24bb177ec2a17bb91f1757102b303a300064437884e33ec50e4307bbb4bb"
        },
        {
          "bytes": 968,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e"
        },
        {
          "bytes": 411,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent.conf",
          "role": "effective_configuration",
          "sha256": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc"
        },
        {
          "bytes": 666,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/spoe.cfg",
          "role": "effective_configuration",
          "sha256": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        }
      ],
      "value": {
        "SDK_accessor_sha256": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
        "actual_isolation_attempt_nonce": "1792016268085004516",
        "actual_spec_sha256": "dedfeff4c8bb47adc481b36b79317d520417988329bcb79f71cbc629ad3f3232",
        "compiled_wrap_symbols": 37,
        "configurations": {
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/agent.conf": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/haproxy.cfg": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792016268085004516/data/spoe.cfg": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        },
        "delivery_parent": "02754040bced960cfc1857416cd7101bb3116ef4",
        "fixture_tls_CA_bound": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_header_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "original_runtime_product_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
        "scoped_product_inputs_equal_a9": 150,
        "source_test_overlays_declared": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "2180c6dbadcc52bbe6da03071f7237bb40a9c6be51b6c71b460b419f53b8c455",
    "run_id": "20261014-hap-predicate-request-4"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 174844,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-extension-v3-request-4-01.json",
    "sha256": "5a63eeed5e90c27fb971e16e0c454564d29338df343d412a1afda2388a9dfd00"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-spop-request::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 5251,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "8791f1a1962fe671e42c28faed88c710359c3b2d837e13005164c9676ce7b729"
        },
        {
          "bytes": 4522,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "473aef5684dbbc2a8e92acd3ca2fa2b4ffd951c0f7762f50bbb19df230d83f2c"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_and_common_cleanup_before_process_stop": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-eos-once",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106419726177084,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-spop-request",
          "result": null,
          "run": "20261014-hap-spop-request-01",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016053515582600,
          "wall_sample_end_monotonic_ns": 106419726177253
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 310,
            "reaped": true,
            "signal": null
          },
          {
            "exit": 0,
            "label": "agent-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 110842,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "5c94b33986ff23ad17e98543a8adbd488a4f8a009a58eeb0e3d5947c2c038b98"
        }
      ],
      "value": {
        "actual_common_finish_calls": 1,
        "actual_common_finish_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-000000000657cded-0000000000000000",
            "case": "NEED-request-eos-once",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 106417705,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106417705461608,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 0,
            "run": "20261014-hap-spop-request-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "1f344da2-522f-4ea8-995d-36025fc8bf20",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016051494867048,
            "wall_sample_end_monotonic_ns": 106417705461698
          }
        ],
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "b9bb3d7609283b2a5190b1532daa309e3d72a5d8d0426416261da975459c004c"
        },
        {
          "bytes": 3694,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent.stderr",
          "role": "host_callback",
          "sha256": "d6fb1c512f0e25e3ad89c9aa14a984763bb068e61e92a6b2054de811a7019390"
        }
      ],
      "value": {
        "actual_SPOP_registry_to_HTX_to_owner_native_scope_binding": {
          "actual_HTX_response_http_end": {
            "actual_operation": 2684387329,
            "capability_sha256": "958f55953a0655a9f8810cc8c77ab0da699bc7b69655ade94cffa0f76f1f914f",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016051493210477
          },
          "actual_owner_EOS_received": {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016051493564035
          },
          "actual_request_evaluated": {
            "kind": "spop_atomic_request_evaluated",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 2,
            "wall_ns": 1792016051435835647
          },
          "finite_request_sample_accepted": {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016051434366910
          },
          "opaque_capability_raw_not_retained": true,
          "owner_registry_handoff": {
            "actual_operation": 0,
            "capability_sha256": "958f55953a0655a9f8810cc8c77ab0da699bc7b69655ade94cffa0f76f1f914f",
            "kind": "spop_registry_handoff",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 2,
            "wall_ns": 1792016051438175171
          },
          "shared_Runtime_session_claim_not_made": true
        },
        "actual_callbacks": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016051434366910
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "958f55953a0655a9f8810cc8c77ab0da699bc7b69655ade94cffa0f76f1f914f",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016051493210477
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016051493564035
          }
        ],
        "definition": "HTX actual http_end; SPOP admitted complete finite Content-Length sample is an atomic request EOS representation, not a request streaming/TCP-close claim."
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 110842,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "5c94b33986ff23ad17e98543a8adbd488a4f8a009a58eeb0e3d5947c2c038b98"
        },
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "b9bb3d7609283b2a5190b1532daa309e3d72a5d8d0426416261da975459c004c"
        },
        {
          "bytes": 3694,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent.stderr",
          "role": "host_callback",
          "sha256": "d6fb1c512f0e25e3ad89c9aa14a984763bb068e61e92a6b2054de811a7019390"
        }
      ],
      "value": {
        "actual_host_handoff": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016051434366910
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "958f55953a0655a9f8810cc8c77ab0da699bc7b69655ade94cffa0f76f1f914f",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016051493210477
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016051493564035
          }
        ],
        "actual_native_P2_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 18,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "1f344da2-522f-4ea8-995d-36025fc8bf20",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106417646328859,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 1,
            "run": "20261014-hap-spop-request-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 19,
            "transaction_id": "1f344da2-522f-4ea8-995d-36025fc8bf20",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016051435734306,
            "wall_sample_end_monotonic_ns": 106417646328956
          }
        ],
        "actual_native_P4_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 38,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "1f344da2-522f-4ea8-995d-36025fc8bf20",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106417704419393,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": 1,
            "run": "20261014-hap-spop-request-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 39,
            "transaction_id": "1f344da2-522f-4ea8-995d-36025fc8bf20",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016051493824874,
            "wall_sample_end_monotonic_ns": 106417704419527
          }
        ],
        "native_append_EOS_argument": null,
        "native_append_EOS_argument_reason": "Selected public native append API has no EOS argument; actual body-finalization callbacks measured independently.",
        "request_finalizations": 1,
        "response_finalizations": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 110842,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "5c94b33986ff23ad17e98543a8adbd488a4f8a009a58eeb0e3d5947c2c038b98"
        }
      ],
      "value": {
        "actual_sdk_cleanup_calls": 1,
        "actual_void_API_return_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "1f344da2-522f-4ea8-995d-36025fc8bf20",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106417705549827,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-request",
            "result": null,
            "run": "20261014-hap-spop-request-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "1f344da2-522f-4ea8-995d-36025fc8bf20",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016051494955278,
            "wall_sample_end_monotonic_ns": 106417705549927
          }
        ],
        "void_return_is_not_numeric_unknown": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 27339,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent-before-main.maps",
          "role": "loaded_image",
          "sha256": "f5848aee168b8b6716642c0aaa5de07ac25eda2793f0cf8711721fc94fb6ae92"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4522,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "473aef5684dbbc2a8e92acd3ca2fa2b4ffd951c0f7762f50bbb19df230d83f2c"
        }
      ],
      "value": {
        "actual_uid_gid_capabilities": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "agent_sha256": "10d8d9f3d0422c9ce745d6a5566b2bff07f82372daba25b2c4efc02046e79b34",
        "host_sha256": "88aaff32806f256db0fe9c69b7c4e848fb6bb5deb16cb5dd06867d039be074e7",
        "host_version": "3.2.25",
        "loaded_native_sdk": {
          "actual_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "actual_public_id_accessor_version_guard": "3.0.14",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 3204,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/artifact-receipt.json",
          "role": "source_manifest",
          "sha256": "d0fb24bb177ec2a17bb91f1757102b303a300064437884e33ec50e4307bbb4bb"
        },
        {
          "bytes": 968,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e"
        },
        {
          "bytes": 411,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent.conf",
          "role": "effective_configuration",
          "sha256": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc"
        },
        {
          "bytes": 666,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/spoe.cfg",
          "role": "effective_configuration",
          "sha256": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        }
      ],
      "value": {
        "SDK_accessor_sha256": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
        "actual_isolation_attempt_nonce": "1792015981905720205",
        "actual_spec_sha256": "3e74d8a263a18f8f470600edcc0c2bebbfae2459c6ddaf4252288629d70c8beb",
        "compiled_wrap_symbols": 37,
        "configurations": {
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/agent.conf": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/haproxy.cfg": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015981905720205/data/spoe.cfg": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        },
        "delivery_parent": "02754040bced960cfc1857416cd7101bb3116ef4",
        "fixture_tls_CA_bound": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_header_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "original_runtime_product_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
        "scoped_product_inputs_equal_a9": 150,
        "source_test_overlays_declared": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "eaa6afdd0a2d1791448c9d8f21ff51736676709b9b587b670aa94102ce3fdbed",
    "run_id": "20261014-hap-spop-request-01"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 170609,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-v8-request-01.json",
    "sha256": "a1bcbd83b5fe8bb603148602fc2bbea073275b71db65a5b68cef3c9faf436a1f"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::haproxy-spop-htx-response-companion::NEED-response-single-chunk

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 5271,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/execution.json",
          "role": "cleanup_observer",
          "sha256": "73e3a6d249d770bec6ad1b3ef2c14f239fc563571db33a9fed762df7f2e9c081"
        },
        {
          "bytes": 4529,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "75ff4cb4a8342b817ea3e6f24676de301553175cf3a1479d8e0e64f8e89c1b6f"
        }
      ],
      "value": {
        "actual_controller_clean": true,
        "actual_native_and_common_cleanup_before_process_stop": true,
        "actual_native_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-response-single-chunk",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106409849520950,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 307,
          "profile": "haproxy-spop-htx-response-companion",
          "result": null,
          "run": "20261014-hap-spop-companion-01",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 106,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016043638926456,
          "wall_sample_end_monotonic_ns": 106409849521109
        },
        "actual_waits": [
          {
            "exit": 0,
            "label": "haproxy-wait",
            "pid": 310,
            "reaped": true,
            "signal": null
          },
          {
            "exit": 0,
            "label": "agent-wait",
            "pid": 307,
            "reaped": true,
            "signal": null
          },
          {
            "exit": -15,
            "label": "backend-wait",
            "pid": 303,
            "reaped": true,
            "signal": 15
          }
        ],
        "backend_SIGTERM_minus15_not_normalized": true
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 113174,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "aa00aab86c2560e62a135072e5716766ec2ffee5d4eed1a98cd6985622862cb7"
        }
      ],
      "value": {
        "actual_common_finish_calls": 1,
        "actual_common_finish_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 46,
            "canonical_transaction_id": "txc-000000000657a696-0000000000000000",
            "case": "NEED-response-single-chunk",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 0,
              "cleanup_complete": 0,
              "cleanup_started": 0,
              "completed_at_ms": 106407638,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 3
            },
            "edge": "return",
            "function": "common_finish",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106407638511101,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-htx-response-companion",
            "result": 0,
            "run": "20261014-hap-spop-companion-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 47,
            "transaction_id": "4fe34c38-34bb-4570-990d-1cf1a4465a9f",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016041427916543,
            "wall_sample_end_monotonic_ns": 106407638511191
          }
        ],
        "actual_native_logging_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "c11e321b0acdc15c560f2f9344ac2938617ef6f8ee1b6e9b71615b7892a037c6"
        },
        {
          "bytes": 3694,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent.stderr",
          "role": "host_callback",
          "sha256": "994cf9d77ccc8be12dcf8d5f0da2713d36dfa4b6a79a609d5dc074f10aec253a"
        }
      ],
      "value": {
        "actual_SPOP_registry_to_HTX_to_owner_native_scope_binding": {
          "actual_HTX_response_http_end": {
            "actual_operation": 2684387329,
            "capability_sha256": "9df787ebf85817c1286162f766a5dde3458638ad5466424727ab9cdf97911996",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016041426193791
          },
          "actual_owner_EOS_received": {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016041426572520
          },
          "actual_request_evaluated": {
            "kind": "spop_atomic_request_evaluated",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 2,
            "wall_ns": 1792016041364890729
          },
          "finite_request_sample_accepted": {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016041363341863
          },
          "opaque_capability_raw_not_retained": true,
          "owner_registry_handoff": {
            "actual_operation": 0,
            "capability_sha256": "9df787ebf85817c1286162f766a5dde3458638ad5466424727ab9cdf97911996",
            "kind": "spop_registry_handoff",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 2,
            "wall_ns": 1792016041367867842
          },
          "shared_Runtime_session_claim_not_made": true
        },
        "actual_callbacks": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016041363341863
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "9df787ebf85817c1286162f766a5dde3458638ad5466424727ab9cdf97911996",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016041426193791
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016041426572520
          }
        ],
        "definition": "HTX actual http_end; SPOP admitted complete finite Content-Length sample is an atomic request EOS representation, not a request streaming/TCP-close claim."
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 113174,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "aa00aab86c2560e62a135072e5716766ec2ffee5d4eed1a98cd6985622862cb7"
        },
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/haproxy.stderr",
          "role": "host_callback",
          "sha256": "c11e321b0acdc15c560f2f9344ac2938617ef6f8ee1b6e9b71615b7892a037c6"
        },
        {
          "bytes": 3694,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent.stderr",
          "role": "host_callback",
          "sha256": "994cf9d77ccc8be12dcf8d5f0da2713d36dfa4b6a79a609d5dc074f10aec253a"
        }
      ],
      "value": {
        "actual_host_handoff": [
          {
            "kind": "spop_complete_request_sample_accepted",
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "sample_advertised_body_bytes": 23,
            "sample_body_bytes": 23,
            "sample_has_body": 1,
            "sample_has_body_length": 1,
            "scope_call": 0,
            "wall_ns": 1792016041363341863
          },
          {
            "actual_operation": 2684387329,
            "capability_sha256": "9df787ebf85817c1286162f766a5dde3458638ad5466424727ab9cdf97911996",
            "kind": "htx_companion_response_http_end",
            "producer_tag": "HAPROXY_COMPANION_LIFECYCLE",
            "scope_call": 0,
            "wall_ns": 1792016041426193791
          },
          {
            "body_started": 0,
            "headers_sent": 0,
            "kind": "spop_owner_response_eos_received",
            "owner_operation": 3,
            "producer_tag": "HAPROXY_SPOP_LIFECYCLE",
            "reserved_zero": 0,
            "scope_call": 2,
            "wall_ns": 1792016041426572520
          }
        ],
        "actual_native_P2_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 18,
            "canonical_transaction_id": null,
            "case": "NEED-response-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "4fe34c38-34bb-4570-990d-1cf1a4465a9f",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106407575385372,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 307,
            "profile": "haproxy-spop-htx-response-companion",
            "result": 1,
            "run": "20261014-hap-spop-companion-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 19,
            "transaction_id": "4fe34c38-34bb-4570-990d-1cf1a4465a9f",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016041364790822,
            "wall_sample_end_monotonic_ns": 106407575385469
          }
        ],
        "actual_native_P4_finalization": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 38,
            "canonical_transaction_id": null,
            "case": "NEED-response-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_process_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "4fe34c38-34bb-4570-990d-1cf1a4465a9f",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106407637418871,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 307,
            "profile": "haproxy-spop-htx-response-companion",
            "result": 1,
            "run": "20261014-hap-spop-companion-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 39,
            "transaction_id": "4fe34c38-34bb-4570-990d-1cf1a4465a9f",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016041426824341,
            "wall_sample_end_monotonic_ns": 106407637418996
          }
        ],
        "native_append_EOS_argument": null,
        "native_append_EOS_argument_reason": "Selected public native append API has no EOS argument; actual body-finalization callbacks measured independently.",
        "request_finalizations": 1,
        "response_finalizations": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 113174,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent-native-api.jsonl",
          "role": "native_api",
          "sha256": "aa00aab86c2560e62a135072e5716766ec2ffee5d4eed1a98cd6985622862cb7"
        }
      ],
      "value": {
        "actual_sdk_cleanup_calls": 1,
        "actual_void_API_return_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "host",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 48,
            "canonical_transaction_id": null,
            "case": "NEED-response-single-chunk",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "4fe34c38-34bb-4570-990d-1cf1a4465a9f",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106407638620871,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 307,
            "profile": "haproxy-spop-htx-response-companion",
            "result": null,
            "run": "20261014-hap-spop-companion-01",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 49,
            "transaction_id": "4fe34c38-34bb-4570-990d-1cf1a4465a9f",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016041428026322,
            "wall_sample_end_monotonic_ns": 106407638620968
          }
        ],
        "void_return_is_not_numeric_unknown": true
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 27339,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent-before-main.maps",
          "role": "loaded_image",
          "sha256": "5d4bf7403dd262531a68cbd38ae406e17bc296f4145d2b9dc88578092096657c"
        },
        {
          "bytes": 3100,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/identity.stdout",
          "role": "loaded_image",
          "sha256": "3f1592922f50fc12caf6e82d9ac414243e60fbfe185b632a035bd71d1b149319"
        },
        {
          "bytes": 4529,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "75ff4cb4a8342b817ea3e6f24676de301553175cf3a1479d8e0e64f8e89c1b6f"
        }
      ],
      "value": {
        "actual_uid_gid_capabilities": {
          "CapBnd": "0000000000000000",
          "CapEff": "0000000000000000",
          "Gid": "65534\t65534\t65534\t65534",
          "NoNewPrivs": "1",
          "Uid": "65534\t65534\t65534\t65534"
        },
        "agent_sha256": "10d8d9f3d0422c9ce745d6a5566b2bff07f82372daba25b2c4efc02046e79b34",
        "host_sha256": "88aaff32806f256db0fe9c69b7c4e848fb6bb5deb16cb5dd06867d039be074e7",
        "host_version": "3.2.25",
        "loaded_native_sdk": {
          "actual_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "actual_public_id_accessor_version_guard": "3.0.14",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 241803,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/source-v2-ledger.json",
          "role": "source_manifest",
          "sha256": "4a878befe3ad7f197a01a53a9fc37ad59ad1628e21654f23f25bc05c7b534d07"
        },
        {
          "bytes": 3204,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/haproxy-lifecycle/artifact-receipt.json",
          "role": "source_manifest",
          "sha256": "d0fb24bb177ec2a17bb91f1757102b303a300064437884e33ec50e4307bbb4bb"
        },
        {
          "bytes": 968,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/haproxy.cfg",
          "role": "effective_configuration",
          "sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e"
        },
        {
          "bytes": 411,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent.conf",
          "role": "effective_configuration",
          "sha256": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc"
        },
        {
          "bytes": 666,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/spoe.cfg",
          "role": "effective_configuration",
          "sha256": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        }
      ],
      "value": {
        "SDK_accessor_sha256": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
        "actual_isolation_attempt_nonce": "1792015985385962996",
        "actual_spec_sha256": "e27f67ae867170932f4c8eaa2b5ccc5907562eb6d7282083b75e75d20430951c",
        "compiled_wrap_symbols": 37,
        "configurations": {
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/agent.conf": "f4502d8a9b1c289ec4eb53518767b2aee60b333ca2757397962a25fe7f0e95bc",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/haproxy.cfg": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015985385962996/data/spoe.cfg": "4fc773c9096a2bd9f872da8d0911ee47f78cb3d16f2005881575f59841b85d60"
        },
        "delivery_parent": "02754040bced960cfc1857416cd7101bb3116ef4",
        "fixture_tls_CA_bound": true,
        "observer_C_sha256": "52aba91c92a8d1a3b1f2b4acf50db6acb103d6d0cd63c45a0e75bcf5fa8553e6",
        "observer_header_sha256": "5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060",
        "original_runtime_product_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
        "scoped_product_inputs_equal_a9": 150,
        "source_test_overlays_declared": true
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "90e3fdcb89975b43c8d4ea2a2aa67eb795b355f414b415fee2356091780b752e",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "eaa6afdd0a2d1791448c9d8f21ff51736676709b9b587b670aa94102ce3fdbed",
    "run_id": "20261014-hap-spop-companion-01"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 172225,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-haproxy-v8-companion-01.json",
    "sha256": "d3aa47f99e985186e4797feb371baa587042c3c9616861cd691955fbd9f762bc"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::envoy-ext-proc::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 151564,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/native-lifecycle.jsonl",
          "role": "cleanup_observer",
          "sha256": "96f4231d8e5bc7d65899d81afb9f7eb194a1166a1a1adc439fd205c1e942fc8e"
        },
        {
          "bytes": 1871,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/result.json",
          "role": "cleanup_observer",
          "sha256": "3c4746d508367a32d17fc243dd3ebf6becfcb5b381ff5355566fc63bc3dcb005"
        },
        {
          "bytes": 4556,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "0b12cd38e4db12562d685777cef75093deecdfc4a8d95844149e336b277e182d"
        }
      ],
      "value": {
        "Go_C_atexit_absent_actual_snapshot_used": true,
        "actual_collector_snapshot_after_real_engine_close": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "I12::envoy-ext-proc::NEED-request-eos-once",
          "contract_state": null,
          "edge": "snapshot",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 107981944994344,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 266,
          "profile": "envoy-ext-proc",
          "result": null,
          "run": "envoy-i12-env-extproc-c2cc4f40",
          "runtime_eos_handoff": null,
          "runtime_finalize_snapshot": null,
          "schema": "native-lifecycle-v1",
          "sequence": 142,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792017615734399788,
          "wall_sample_end_monotonic_ns": 107981944994438
        },
        "actual_runtime_destroy_return": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 66,
            "canonical_transaction_id": null,
            "case": "I12::envoy-ext-proc::NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 107978276126274,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 266,
            "profile": "envoy-ext-proc",
            "result": null,
            "run": "envoy-i12-env-extproc-c2cc4f40",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 71,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792017612065531779,
            "wall_sample_end_monotonic_ns": 107978276126432
          }
        ],
        "driver_actual_waited_process_exits": {
          "backend": {
            "forced_kill": false,
            "pid": 262,
            "proxy_pid": 261,
            "signal_sent": 15,
            "waited_exit_code": 0
          },
          "engine": {
            "forced_kill": false,
            "pid": 266,
            "proxy_pid": 265,
            "signal_sent": 15,
            "waited_exit_code": 0
          },
          "envoy": {
            "forced_kill": false,
            "pid": 277,
            "proxy_pid": 276,
            "signal_sent": 15,
            "waited_exit_code": 0
          }
        }
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 151564,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "96f4231d8e5bc7d65899d81afb9f7eb194a1166a1a1adc439fd205c1e942fc8e"
        }
      ],
      "value": {
        "actual_common_finish_calls": 2,
        "actual_native_logging_calls": 1,
        "common_finish_idempotent_second_call": true,
        "observed_public_runtime_finish_wrapper_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 4915,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "4da6a8893436f5be5c644366338b23c696531da8659a2d3c50e49fa7b17b01ed"
        }
      ],
      "value": {
        "actual_finite_authz_sample": [],
        "actual_request_body_input": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107978261702306,
            "operation": 1,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017612051107638
          }
        ],
        "actual_response_body_end_of_stream_input": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107978274322910,
            "operation": 1,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017612063728237
          }
        ],
        "actual_route": "standalone protobuf body.end_of_stream request/response, finite sample/lease not this route",
        "native_raw_host_eos_fields": null,
        "transport_eof_is_separate": true
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 151564,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "96f4231d8e5bc7d65899d81afb9f7eb194a1166a1a1adc439fd205c1e942fc8e"
        },
        {
          "bytes": 4915,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "4da6a8893436f5be5c644366338b23c696531da8659a2d3c50e49fa7b17b01ed"
        }
      ],
      "value": {
        "actual_finish_entry_return_callbacks": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107978261962192,
            "operation": 3,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017612051367545
          },
          {
            "actual_result": 1,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107978262252895,
            "operation": 4,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017612051658244
          },
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107978274630981,
            "operation": 3,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017612064036330
          },
          {
            "actual_result": 1,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107978275186505,
            "operation": 4,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017612064591857
          }
        ],
        "actual_nested_runtime_native_finish_spans": [
          {
            "actually_nested_native_returns": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 23,
                "canonical_transaction_id": null,
                "case": "I12::envoy-ext-proc::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "env-extproc-c2cc4f40",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 107978262129520,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 266,
                "profile": "envoy-ext-proc",
                "result": 1,
                "run": "envoy-i12-env-extproc-c2cc4f40",
                "runtime_eos_handoff": null,
                "runtime_finalize_snapshot": null,
                "schema": "native-lifecycle-v1",
                "sequence": 24,
                "transaction_id": "env-extproc-c2cc4f40",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792017612051534979,
                "wall_sample_end_monotonic_ns": 107978262129626
              }
            ],
            "entry": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 22,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-proc::NEED-request-eos-once",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107978261994546,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 266,
              "profile": "envoy-ext-proc",
              "result": null,
              "run": "envoy-i12-env-extproc-c2cc4f40",
              "runtime_eos_handoff": "request_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 22,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017612051399990,
              "wall_sample_end_monotonic_ns": 107978261994636
            },
            "return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 22,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-proc::NEED-request-eos-once",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107978262234423,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 266,
              "profile": "envoy-ext-proc",
              "result": 1,
              "run": "envoy-i12-env-extproc-c2cc4f40",
              "runtime_eos_handoff": "request_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 29,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017612051639859,
              "wall_sample_end_monotonic_ns": 107978262234506
            }
          },
          {
            "actually_nested_native_returns": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 51,
                "canonical_transaction_id": null,
                "case": "I12::envoy-ext-proc::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "env-extproc-c2cc4f40",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 107978275043225,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 266,
                "profile": "envoy-ext-proc",
                "result": 1,
                "run": "envoy-i12-env-extproc-c2cc4f40",
                "runtime_eos_handoff": null,
                "runtime_finalize_snapshot": null,
                "schema": "native-lifecycle-v1",
                "sequence": 52,
                "transaction_id": "env-extproc-c2cc4f40",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792017612064448749,
                "wall_sample_end_monotonic_ns": 107978275043398
              }
            ],
            "entry": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 50,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-proc::NEED-request-eos-once",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107978274660591,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 266,
              "profile": "envoy-ext-proc",
              "result": null,
              "run": "envoy-i12-env-extproc-c2cc4f40",
              "runtime_eos_handoff": "response_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 50,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017612064066030,
              "wall_sample_end_monotonic_ns": 107978274660674
            },
            "return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 50,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-proc::NEED-request-eos-once",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107978275171824,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 266,
              "profile": "envoy-ext-proc",
              "result": 1,
              "run": "envoy-i12-env-extproc-c2cc4f40",
              "runtime_eos_handoff": "response_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 57,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017612064577263,
              "wall_sample_end_monotonic_ns": 107978275171914
            }
          }
        ],
        "raw_argument_eos_and_host_eos_fields_preserved_null": true,
        "selected_official_native_complete_body_contract": "processRequestBody/processResponseBody invoked once only after direct host body EOS; SDK appends have no EOS argument"
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 151564,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "96f4231d8e5bc7d65899d81afb9f7eb194a1166a1a1adc439fd205c1e942fc8e"
        }
      ],
      "value": {
        "actual_common_cleanup_calls": 1,
        "actual_native_cleanup_calls": 1,
        "actual_runtime_destroy_calls": 1
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3499,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/before-request.json",
          "role": "loaded_image",
          "sha256": "d83bba838dc429e1e5ad9e81b3e50da29490d022bea6064e5eac4c4c20364d3e"
        },
        {
          "bytes": 227,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/bootstrap-observation.json",
          "role": "isolation_receipt",
          "sha256": "6180f3d4849ea55a37b61b7f66521a77f3f10eef950e276f3c10547f3b263d03"
        }
      ],
      "value": {
        "actual_processes": {
          "backend": {
            "executable": "/usr/local/bin/python3.14",
            "executable_sha256": "aa4ec29748e8f5cfd800a83448daa49b3dc384dd9ddaea9823677181238dd1f2",
            "fd_count": 4,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2265121]",
              "2": "pipe:[2265122]",
              "3": "socket:[2263223]"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [],
            "pid": 262,
            "proxy_pid": 261,
            "vanished_during_snapshot": []
          },
          "engine": {
            "executable": "/task/cache/msconnector_envoy_ext_proc",
            "executable_sha256": "19f0f7bb1f48edfa86e2567ae107d01ceb7f9fafa6c3d87d0d25d8242ea56b1c",
            "fd_count": 11,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2259586]",
              "10": "/task/runtime/adapter-events.jsonl",
              "2": "pipe:[2259587]",
              "3": "/task/runtime/native-lifecycle.jsonl",
              "4": "/task/runtime/native-audit.log",
              "5": "anon_inode:[eventpoll]",
              "6": "anon_inode:[eventfd]",
              "7": "/task/runtime/native-debug.log",
              "8": "socket:[2261611]",
              "9": "/task/runtime/common-events.jsonl"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [
              {
                "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
                "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
              }
            ],
            "pid": 266,
            "proxy_pid": 265,
            "vanished_during_snapshot": []
          },
          "envoy": {
            "executable": "/task/cache/envoy",
            "executable_sha256": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
            "fd_count": 25,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2261618]",
              "10": "pipe:[2261626]",
              "11": "pipe:[2261626]",
              "12": "anon_inode:[eventfd]",
              "13": "/dev/null",
              "14": "socket:[2261627]",
              "15": "/task/runtime/envoy-access.jsonl",
              "16": "socket:[2261637]",
              "17": "anon_inode:[eventpoll]",
              "18": "pipe:[2261638]",
              "19": "pipe:[2261638]",
              "2": "pipe:[2261619]",
              "20": "anon_inode:[eventfd]",
              "21": "anon_inode:[eventpoll]",
              "22": "pipe:[2261641]",
              "23": "pipe:[2261641]",
              "24": "anon_inode:[eventfd]",
              "3": "anon_inode:[eventpoll]",
              "4": "anon_inode:[eventfd]",
              "5": "anon_inode:[eventpoll]",
              "6": "pipe:[2261625]",
              "7": "pipe:[2261625]",
              "8": "anon_inode:[eventfd]",
              "9": "anon_inode:[eventpoll]"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [],
            "pid": 277,
            "proxy_pid": 276,
            "vanished_during_snapshot": []
          }
        },
        "actual_uid_gid": [
          65534,
          65534
        ],
        "host_version": "/task/cache/envoy  version: b579d07d3ad7ee11d32b105e91a5a39ad24718d7/1.39.1/Clean/RELEASE/BoringSSL",
        "native_who": "ModSecurity v3.0.14 (Linux)"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 40026,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/build-manifest.json",
          "role": "source_manifest",
          "sha256": "f17aed16f1d6ac8bd3ae107526814081dfeeff4b6ec019f649508dcb126e9920"
        },
        {
          "bytes": 54602,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/scoped-product-source-equality.json",
          "role": "source_manifest",
          "sha256": "40ddedbe31c9b7bf55f48b2906f29c2a245ad726a9b4523964e3b2e2f9bc84cb"
        },
        {
          "bytes": 241161,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/source-ledger-v1.json",
          "role": "source_manifest",
          "sha256": "6b4ba0985efbda2f4dded97c5be54933c6d5d2c185b46862e660628d662f49b4"
        },
        {
          "bytes": 399,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/native.conf",
          "role": "effective_configuration",
          "sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb"
        },
        {
          "bytes": 961,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/extproc-v3/fixtures/native.rules",
          "role": "effective_configuration",
          "sha256": "ddf5a99206fd053fea66ac923bc18584610ac96c8272864382951a4398ed4dff"
        },
        {
          "bytes": 5782,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017569281949623/data/runtime/envoy.yaml",
          "role": "effective_configuration",
          "sha256": "c47bd1be9b18189b56a4a4a648274c23155f1b277d5b2d9348e88af1461d1abe"
        }
      ],
      "value": {
        "actual_build": {
          "actual_external_build_provenance": {
            "actual_build_receipt": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/build-control-07/receipt.json",
            "actual_build_receipt_sha256": "8dcf87861e481f33051d52bc0617052b125f49071620bcaae70be3f83bc6fbc3",
            "actual_host_not_launched": true,
            "binary_hashes": {
              "envoy": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
              "msconnector_composite": "719a9ddd277e9b04482d55684266a96989b384e37789df6d8482549a46e7fcc8",
              "msconnector_envoy_ext_proc": "19f0f7bb1f48edfa86e2567ae107d01ceb7f9fafa6c3d87d0d25d8242ea56b1c"
            },
            "scope": "fresh external actual native build; reused pinned realEnvoyhost binary only",
            "scoped_product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
            "selected_sdk_image_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
            "source_baseline_git": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness + declared private overlays",
            "source_sha256": {
              "ci/runtime/lifecycle/aggregate-five-connector-no-crs.py": "641b11df919f35412de9d287e734f07c8027100cbff596cf54ff0f572a0890f9",
              "ci/runtime/lifecycle/aggregate-five-connector-with-crs-no-mrts.py": "43b22adfe39bed7c1bbd7aa0b2d3b70c6af40850579f4b6d598d7fd07d1ac556",
              "ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py": "af83ee477c71ef9da7e75820615e6dd4c3423b5bab21df585655f85549e98a52",
              "ci/runtime/lifecycle/cases/apache-phase4-response/allow.yaml": "f7a63436fa8b874e5395f3e3bfa9cc89296eb0693622a0fcfcd4f8509ec69315",
              "ci/runtime/lifecycle/cases/apache-phase4-response/custom-mime-deny.yaml": "86103d9de76ada3a496cc32b19cb58cb78fbdc6b02a2154dc960d555be701168",
              "ci/runtime/lifecycle/cases/apache-phase4-response/empty-allow.yaml": "9f164c02f5a95f4f22d7d8c6be467ab4e5c923c79008cb0388d9dcb68c6b407a",
              "ci/runtime/lifecycle/cases/apache-phase4-response/empty-deny.yaml": "5d924a1106bf3a06cfa1c579784e9d8aa9e0cec09d9a4d0150e5531211c2b811",
              "ci/runtime/lifecycle/cases/apache-phase4-response/engine-limit-process-partial.yaml": "4f38b6398eb211da297f71c3a1ad8d5d8fe88808c18926e8aa3b9bddcae6c91f",
              "ci/runtime/lifecycle/cases/apache-phase4-response/limit-reject.yaml": "fb6fcb54b443ba6fe661607c07cc4fc2c29f0b89d52b06f098893890661f96cd",
              "ci/runtime/lifecycle/cases/apache-phase4-response/log-only.yaml": "c6cb64c259226c5a65d755deb5ea7f196a2da18fd121844b781b76e2e94b5ebd",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-deny.yaml": "0f5f3ad1c29229d47de25bdfcaf8fbe67f5acbff44899866e3a7c4ebe275874c",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-phase3-deny.yaml": "ff042a9a5e71d1ee48ffe26397f7b67cf99ca7b464ec624c6681d30dc0195f82",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-phase3-header-freeze.yaml": "1b1ddecef36454f0dbd8444cae1baf49ae41ff9c38abd6affb4e90a2d967cc3d",
              "ci/runtime/lifecycle/cases/apache-phase4-response/redirect-uri-policy.yaml": "b9244adda39713af220b7e05f97746015c4248ea281db692d431a2bc773482ce",
              "ci/runtime/lifecycle/collect-no-crs-source.py": "132df7f2292847ebca9688eaa33bf14b5ce5f09cb4bdbb4b5006afab32f5da65",
              "ci/runtime/lifecycle/consume-no-crs-selected-cases.sh": "8f99d061c30e9124782346667bd55936759c96887afdf75840d9540003d62655",
              "ci/runtime/lifecycle/five-connector-no-crs-profile.py": "39d492145ac7e8b03de8b2e089f6eb0a6ee5c065313201238acd561df154247c",
              "ci/runtime/lifecycle/native-lifecycle-observer.c": "ad8e5e36a17e746cf202c685dbb529fc09717f5c25441b713fa369420aa55ac6",
              "ci/runtime/lifecycle/native-lifecycle-observer.h": "f9f63b62ba8efc555dc20e673cc02251d5ab6c2ab17d8f5efa760d0d97146dcd",
              "ci/runtime/lifecycle/native-lifecycle-sdk.cpp": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
              "ci/runtime/lifecycle/nginx-native-operation-source.py": "3cf60b721a35540d28e91f03b3e78a0066d7983ccac02937428a2b4b688961c4",
              "ci/runtime/lifecycle/nginx_native_authority.py": "7e38a25917e38f99d8c9c102ba62093b4b50d161243926e5dde8da986d1353ca",
              "ci/runtime/lifecycle/nginx_native_collection.py": "b39b3132f36739a6e68596ebaad90ec3ebd102185f728b375f9a5ff5a0c494ca",
              "ci/runtime/lifecycle/nginx_sequence_client.py": "3f8f2220295e7c6c60351dc27525b273040ccaa3bb4e848cd28dc49fe3ca49e0",
              "ci/runtime/lifecycle/nginx_sequence_upstream.py": "8c52f8592037955c9c4cbcf919a066e30be7920eb8d34ab77724f8b7c9b466f7",
              "ci/runtime/lifecycle/normalize-with-crs-no-mrts.py": "5cb7ab24b61a2a590bf9768d2654bff721702ded2f4a90b90d3fa5ef94d928ec",
              "ci/runtime/lifecycle/plan_full_matrix_ports.py": "741760d3154845591e9a9707e0780da6d8ec3a2b020d17393ff95ee9ac63ed40",
              "ci/runtime/lifecycle/prepare-fresh-crs-source.sh": "fdb553b7ccf385fd990141821c678ca9289af66eae1e9ee9e717d2bcd5529f7f",
              "ci/runtime/lifecycle/prepare-verified-runtime-paths.py": "c8dbb1ecd0ff5e953dae40ca29102f091c6c8b05d48b63f7bc119e97e18f89c2",
              "ci/runtime/lifecycle/prepare-with-crs-no-mrts-upload.py": "57b7a2493293f5c49b0b440d8374758e107a610944260731de13168cafc7fec1",
              "ci/runtime/lifecycle/project-haproxy-runtime-evidence.py": "700c12482a563b4d8872ee8717adf9c6e6f5c321fc8361faf8e98f0bc524de6a",
              "ci/runtime/lifecycle/reserve-runtime-env-snapshot.sh": "a5a2153d8b50f1b6d2926659b364c92ebe726b0caaa9a06ab0bfc1b910a6ee02",
              "ci/runtime/lifecycle/resolve-full-lifecycle-profile.py": "474fe90d7bec9610f52c84e490708a0cf86cc27cba1675525c6290fae20a11b5",
              "ci/runtime/lifecycle/resolve-lighttpd-host-binary.py": "39dbf6ff78ba18b83fb18a4b529d96b98ed7879fdd5e0ab0afa1b59459c529e6",
              "ci/runtime/lifecycle/resolve-traefik-host-binary.py": "2d667abb8b167d2de1a254e6a873f262af4d004bd129d9e7bf57eb59f6eb9b96",
              "ci/runtime/lifecycle/run-apache-phase4-response-regression.sh": "78f2a5bf2999f54753af9d6141398259cfccd216a026d5c11670befa9addd295",
              "ci/runtime/lifecycle/run-bounded-nginx-cases.py": "3f4cfa011fe5f14eef36c3683a07994265dfb65fb6d636374a2e73dbae192262",
              "ci/runtime/lifecycle/run-connector-stage.sh": "3904616de7539858a396227e14b0bb5537026b7044719889a360d3e0955d78dd",
              "ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh": "e36c1a937e1c52b070f4247549993e07234e87f1cca7c4ddfb71ba34b65d3408",
              "ci/runtime/lifecycle/run-full-matrix-job.py": "d5f33cb3416e747567a6bda924df1d01ad1a8d7f156a8eb441b6afef463cb56b",
              "ci/runtime/lifecycle/run-full-matrix-parallel.sh": "a20fb467ccc18119573a7b58191421d26be795aff7eddc63724d54e68c080e10",
              "ci/runtime/lifecycle/run-full-matrix-resume.py": "5ce95bfe1ff0c7ea7cf0e7bda0111efde1425ac067af1fab534aa74aea419ddb",
              "ci/runtime/lifecycle/run-full-mrts-runtime-matrix.sh": "4badc2bdf2bad27f0a7c8f3fc563633792459fdf5f56773b94d3f014fcfda6db",
              "ci/runtime/lifecycle/run-legacy-open-connector-smoke.sh": "5d0330ded4e6056466c75e8e31dc571a40926adf296718339f0264f8bed2e529",
              "ci/runtime/lifecycle/run-mrts-native-full.sh": "83dc3ed6cf300cc8aa34aa1497846c1da13942d9e7f5f07e7ba972a9686a6b48",
              "ci/runtime/lifecycle/run-native-case-comparison.py": "1b9e0917c255b5d18cd41e2b03945f7136b6e6989110afde9b332bf8a707516d",
              "ci/runtime/lifecycle/run-native-first-byte.sh": "6c60df7102afea95972c2dcb2dee1685033cc99bc9b06ec369ae81053afcec91",
              "ci/runtime/lifecycle/run-nginx-common-input-fault.py": "a77af00e0c851c2b92e36ac6742dc8ea7a12c02466956ef59fba9f5f00c2458f",
              "ci/runtime/lifecycle/run-nginx-configtest.py": "aed2542ad0bf72af9fd25c3f6f18ecb6f656ef699d615fdf032fe5b3ffe9869f",
              "ci/runtime/lifecycle/run-nginx-event-boundary-cases.py": "9c2475c2c64d48611f62301a581d5e920cfbfbc3693949c40b37cc9cecd39c14",
              "ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py": "73829a2b184c92d3c771334efd0363f72a6ea8f95756ac7b3c6159e4e54b45d8",
              "ci/runtime/lifecycle/run-nginx-mime-cases.py": "75c63cad1de90401b33552715d4a02bb25eca55783b033e831d5430ecbd75fd7",
              "ci/runtime/lifecycle/run-nginx-phase4-cases.py": "32f9fb88a546eec9bd6dece0b86686f312729844c7960ddb5a2c1f49084064fa",
              "ci/runtime/lifecycle/run-nginx-raw-h1.py": "29a7d386ed6755f4e2f6a8226ee168d40809b69043cdc5fbcd6d9a74b6eebd1c",
              "ci/runtime/lifecycle/run-nginx-selected-host.sh": "7f77dffdda373e423a9c43076c30c44d13af1a10aca3763bc652620c11f68bce",
              "ci/runtime/lifecycle/run-nginx-valid-rules.py": "f22b5bf4ed5ac4cef52db9c8590ddede79b48043ed25de5f2ffee8260ad4b69c",
              "ci/runtime/lifecycle/run-no-crs-baseline.sh": "d520534d0acb18cb75d2e00c5b7d666a1398a4144b535a07fd452b74d799afe3",
              "ci/runtime/lifecycle/run-remaining-connector-target.sh": "163127a02f4caca1f860e86681da34e6b60c20d8d0d99f79026591482048db3d",
              "ci/runtime/lifecycle/run-selected-nginx-configtests.py": "d7f394649365631716f6c9077fc02c40091b0ec4d94e72648a58e13d2468062c",
              "ci/runtime/lifecycle/run-selected-nginx-native-operations.py": "97b8609b6aad9c558dfb2d1133331a9aef28d346d8245fc2eb44af31fcf45489",
              "ci/runtime/lifecycle/run-verified-case.py": "534bbd1e5e2cbd21abfe883acc727466c1f16f7e88ae2ca363534f97bbcdb221",
              "ci/runtime/lifecycle/run-verified-report-run.py": "9e39fed4c6210cfb6ccdd0f7f982aebdb50ffd056ae4486886bfc573c75e9211",
              "ci/runtime/lifecycle/run-with-crs-no-mrts.sh": "34ffabcd66507c7abc05950ce7c4719680dafc1da99665ed0a7a31d0519ad160",
              "ci/runtime/lifecycle/sanitize-full-lifecycle-log.py": "a64ea3251e076db075fc4693d0edc7f24de8d0ac4356a8ae9f8b3a849e5d1cfc",
              "ci/runtime/lifecycle/stage-traefik-runtime-artifacts.py": "52b790c6c56c5b1bd37ea9528fa4bc1768ba0edc7f61252cba85c849ca8b7cc3",
              "ci/runtime/lifecycle/summarize-with-crs-no-mrts-workflow.py": "4a20bcf3b17c4c57cc9a77351cffd8e2e22c5de35b9aade5739aa5ca7cbc040e",
              "ci/runtime/lifecycle/trusted_lighttpd_runtime_supervisor.py": "cc74f460fa8a7704ccd95c1d0b9c0d5157d7ed7e3b026fd5158e0485ef5df208",
              "ci/runtime/lifecycle/with-crs-no-mrts-profile.py": "2da241985aa2be3be6ca8557b46d7ef7287e924d4e4be87d6f6a3751fd419bdb",
              "ci/runtime/lifecycle/with-private-sockets.py": "e426b95376db97b98df3e455482e39780078d50ae9d563994e3da04b0b9472eb",
              "ci/runtime/lifecycle/write-engine-lifecycle-artifacts.py": "4ee3e0fa57ec5c9e7a16d9d17c82d535d6f09a44a805106faf86097de1d0fdf7",
              "ci/runtime/lifecycle/write-first-byte-host-metadata.py": "68673de809f4437a5c38ddbda4c7fa6e936c82a7b5389982471e5a3b71af0377",
              "ci/runtime/lifecycle/write-first-byte-source-results.py": "360e0606a76c0eba8b0c331e897e86492801bdf0321a89d3460ee4ca000b0cdc",
              "ci/runtime/lifecycle/write-hostruntime-record.py": "053385a6f95e15006dc0fd0608cdb5128c5aba4ab13b8d83d4306e1d269e9027",
              "ci/runtime/lifecycle/write-nginx-functional-a-evidence.py": "4f12aea27f5354164bca673665b567f135427753bae1c41c7fbcf2c55a2a017f",
              "ci/runtime/lifecycle/write-transport-lifecycle-artifacts.py": "46ca6319e819e76a660ca0513f5273405690015a471cfdd34123e3e4224a8195",
              "common/README.de.md": "5cf445954bc4071ed103471d4f2d562d91225972181f1f5715e04a56b09427ef",
              "common/README.md": "2e7e7fd6070d544ab003107aadc19bd98c223d1bad18c6cec9fa8153fb13f35e",
              "common/docs/design.de.md": "30e5ebf761f8f35cf0f086ceebe6017ff361434fd73899f7ebe593ade9b32920",
              "common/docs/design.md": "af3a6fc164e94a1d0802369b0f00f8a33a4a8c395dae582bdf31b3b2dc0df58d",
              "common/docs/transaction-phase-contract.de.md": "b50d175ef2417dee0a5185605a2159fb42b4f91c2935b3e5276bbc9fd85cb858",
              "common/docs/transaction-phase-contract.md": "aaeed679658ce63698687e1f8d1257be2bce1373917046877bccbe0413077291",
              "common/include/msconnector/adapter.h": "ecaff425e0dae033614a7dc6f143d4c9308a36b8f0f26d15fe87614152f7fbd9",
              "common/include/msconnector/adapter_contract.h": "01e08a1e8cdafcd77a534073d133b48a661295e24c3dfdc966977200797417be",
              "common/include/msconnector/adapter_metadata.h": "5644007681e90c19e6191e88c5398f23d591135413d559a7895477e6c8ca7c63",
              "common/include/msconnector/artifact_layout.h": "a12ea7e38f203fb4ffe0f0b83d63a518a4e3ede2aae2ae69487dec0b3398690f",
              "common/include/msconnector/artifacts.h": "75e3f0b94a4c08238d94bd9e92c0b0e403dd6d3f193feee998713c5d7489f66b",
              "common/include/msconnector/block_statuses.h": "604a6fd7c172016a9411b2aca8703a18b411a61d6b58e52a021ab9114c988f1c",
              "common/include/msconnector/blocking.h": "f400e887a204e38a6ec381e548c3c75e5abc789196aea688081bd9b853a27f82",
              "common/include/msconnector/body_policy.h": "8e7084e4ab112ff6566738ac2a46b4467f8defa1f52c3da113d4b1657f9e7575",
              "common/include/msconnector/build_contract.h": "030c417781f76d7807401022d635e0f0329e44813f6c693676aff74ffc50cb25",
              "common/include/msconnector/capabilities.h": "60997cbd4967d2d0d318ca53cc1af7ad299ee464487404a33064c2f1afce55b4",
              "common/include/msconnector/capabilities.hpp": "af279aadc9bc2fdaf2c69eeb29309d460132bd891f8438429101c72f3cbe6898",
              "common/include/msconnector/capability_matrix.h": "faaaf5496f6ee3db4c9f8e6336f9584b464c4e3b8032a26610d118be2ce9d041",
              "common/include/msconnector/config.h": "3a81652676b81bd97d4d392543db84cb69729c012745fa7f1807eb4319f31d3b",
              "common/include/msconnector/config_parser.h": "dd9f88f70eb20914fb97899de90864b1e56f55cb6710af9cb27fb94847a67231",
              "common/include/msconnector/connector_manifest.h": "84f63cba49eff679194c6e142df179a23c6e15bfecce0308fcbb051dfb1d67ef",
              "common/include/msconnector/crs.h": "cfb1ff7fce3e8f5cdfb63f02002e9dbe9a56197d92914257da77c774845ce1c1",
              "common/include/msconnector/decision.h": "a29c08ee67caa83a3eb146508ed1d6bcc8dc7b27c13cc221a8d074a9b735f722",
              "common/include/msconnector/decision_action.h": "16dc56d9add80ffe51ca987dbda7326e9fb06fea17637c1b87f02b06f94a604e",
              "common/include/msconnector/directive_adapter.h": "2d961c11680bbb49139fb4ec846a28b74e3bc90e1ad4433d6fe547870f97ee9c",
              "common/include/msconnector/directive_spec.h": "4c6eae37390971f41797ae6a1216759e27668b83e4ddbcaaa27a3cd1f3f0e404",
              "common/include/msconnector/directives.h": "d79780a9339de70d7d7746c2918b792fdb3e6ce0dd8a62d29050b8760a142731",
              "common/include/msconnector/dos_guard.h": "2f906760eb2a76ef1aa93d43a2bfc661d317f60d5478209523b3cd90ce3fd297",
              "common/include/msconnector/error.h": "1cc9ca56d2d51eb74056f463abcce951a8079e93b451944c34ac2c97e2914d47",
              "common/include/msconnector/event.h": "acbb5ea952e80f88ce43a6f63d24006f6c6703568ec1dc273a56bced2896a195",
              "common/include/msconnector/event_jsonl.h": "4df864ff98970d8012e29d600bde1b0417c77d3ba9f063fbbadc838b624a6752",
              "common/include/msconnector/event_protocol.h": "2214e119ec6cdca01e1fb5b695495f80823703eec3fa09bc45f905be53a25148",
              "common/include/msconnector/flow_guard.h": "bd16ae73483f19df6cb790bdaf707ecb6467e2ef2a5ce88710fc50519ead161b",
              "common/include/msconnector/generic_mapper.h": "21bc95cb0f637f77210751c65eb912f9936868b4ca1164aa879f6318169309e4",
              "common/include/msconnector/headers.h": "17372f1cec75d33610cd340baa608ba317f6bf6f0f17a562ab5827bc037a3320",
              "common/include/msconnector/http_status.h": "e4f13f7cfae1223aa56673c7c448a25e1a4c6cad78ffa68326d1093d86ad78ed",
              "common/include/msconnector/integrity_event.h": "83a57b7ae647f75b9f05a2614f5b4bb53cd3cb0ee2d097b33d586734c73ed15c",
              "common/include/msconnector/intervention.h": "7cd3f5af2141bd8221205f5f51acdae9df159e83e52f5ee729153ef24f4ee19a",
              "common/include/msconnector/intervention.hpp": "5ef289fc59d723ff1115a33298689ab17d97511b697e79c6bdb890bf16c64334",
              "common/include/msconnector/json_escape.h": "97a2335e648a751cffea08aefd78c40ae114373ff31a7c0d85a419af582c7cf7",
              "common/include/msconnector/late_intervention.h": "c0fccf1a18483d85ce1c50d1cbacde54f3800e554bda0dc2483cfacdbd0ad266",
              "common/include/msconnector/lifecycle_status.h": "a6da04c7e7a69ebbdf88aedeb41b3d525701092b99a3ec5dc5930e086c76a841",
              "common/include/msconnector/limits.h": "c50c6f87869719366226624efabc1feb5452f3a3511d58a7c3eab425cacea3d0",
              "common/include/msconnector/log_sanitize.h": "7de8322a5fdf114edfc8b00bdb2eaed8c62a6bd2ce8f6f870e8400918510532e",
              "common/include/msconnector/logging.h": "c068c9f4dd19cd8410ea760b145dac979933dab3d48fffd89f5cb9abcd49b62e",
              "common/include/msconnector/logging.hpp": "6bdb2d4ad3df381112d10ae8c0162c7d1941045ad6fd6ac420e25e051bd643e5",
              "common/include/msconnector/memory.h": "8e12e78b3fcf31d36d42dae1e3aba069906b8ea10c52e4f84b909b423cf76c1f",
              "common/include/msconnector/modsecurity_engine.h": "e5de4580184c72d54844d724aca55e180db2ec3c2200a2fb78fdd5f383f4f304",
              "common/include/msconnector/native_result.h": "a16c7f5d3661416aa95aed0b5856b2d71728b917b9480f4bb3e0781abb2327bc",
              "common/include/msconnector/options.h": "1dbb1807ab8cb90150be605d57371ecccabfed1ba142c2abcd0ec0dedb1e1301",
              "common/include/msconnector/origin.h": "be8e938fd1f72a6a0c7905347d1c7020ba93c60dad41b171d8be52d2f5c9b88b",
              "common/include/msconnector/origin.hpp": "de70d4483295980612b3e3d894c1abbc979d87939affcc15d6bce266d9a32c0a",
              "common/include/msconnector/origin_governance.h": "7e87ee19f3afaf6be288d0679c39b7539b6740fadd588fee433069ac6a92036b",
              "common/include/msconnector/path_policy.h": "019e24186f9fa9ce692a127ce3e34df37d629f26db24a4c3152e9baf92be4a3c",
              "common/include/msconnector/phase.h": "c3097da8b1d1cf6480a7a7ceb3d97301da06668a082c40e550dd2e79f7149c37",
              "common/include/msconnector/redaction.h": "e3a1c203c8b2be9a4bee476e50c3764a6eee64715baf4de5ee0ec999ea394880",
              "common/include/msconnector/request.h": "f4508228e6964f1620d9e98dc4d7137cc1c575d3b36d862803b773c1056d3e90",
              "common/include/msconnector/request.hpp": "0991512a4ff9116d2d51586777bd770de92a5640bce1fa6dab5d3513718ebf03",
              "common/include/msconnector/request_helpers.h": "de3194debde952645cc27b71b7c82952c0eaa760f38070e5a93439af6ae1f75b",
              "common/include/msconnector/request_mapper_contract.h": "71714b2f289225992cd07d2da8c810618f89a97fa949772006a7345752659440",
              "common/include/msconnector/resource_limits.h": "9daa3c67ea6808f5ce0f0c9381e287ad045aed1668a9e3b1ab41d354c017019c",
              "common/include/msconnector/response.h": "4ef1a7b000097edeeae920904c0deaa88be4dfac9a85ad18c2a8e829cdbf3d55",
              "common/include/msconnector/response.hpp": "dabc8933fc38759c72fa4fa052f05fc2357064c79089160cc54a13bfee56590f",
              "common/include/msconnector/response_helpers.h": "dddb5bb998ac2b447ab8e9db10cd5ba83c8b53ab205ca90e52fe3bce2342e143",
              "common/include/msconnector/response_mapper_contract.h": "bcfb70b93384f711cf751af3a84ab835f079bec0f9c5fba3a22725ef04f9b6e8",
              "common/include/msconnector/rule_error.h": "af251cb2686a0fffe92446d3ac428bea1076e2afa6a559e44f272e37e64110d6",
              "common/include/msconnector/rule_event.h": "bde25165fd2967d26646a2abb35c62947100d9f7d2f2fb43801ccd3ffaa9ce52",
              "common/include/msconnector/rule_id.h": "a00c7a1dd97cee368af7e30df043ebb150756edc98766471d65b73e3ab25c94d",
              "common/include/msconnector/rule_load_stats.h": "12c501883a5c1798fea3d3064c0f7e3a8c29c31552aef40a11035f245d6b06ea",
              "common/include/msconnector/rule_loader.h": "a9529a7c0189207613b04b0d329dcb0ce9402b692363a7ccff20a400d783771d",
              "common/include/msconnector/rule_merge.h": "e8ca8cae33fb824940667b19ff7abeff5edd02ece64e96397e9d96cd5ef26310",
              "common/include/msconnector/runtime_paths.h": "f0368755817351ec8fd6278e7f539a6053ab9c2de0c4ef6d73e2873e713b5d42",
              "common/include/msconnector/runtime_report.h": "38413741b9cea29cde986c169a86ba9e11675b51f9896784141c90ff3c37af0f",
              "common/include/msconnector/status.h": "47943b4baa61990f8bfa1a2e0a6f82d2a3a159145b4fc85a9702c347cb4ef256",
              "common/include/msconnector/status.hpp": "aae1d9eb582ebbd029b9faf256e7b389c722e35243d5a864f3e3d3e51740efe3",
              "common/include/msconnector/test_result.h": "208132abcbfb4d1cb228dbf895ba42e6cf73911cde004d675947e4f2b80e9807",
              "common/include/msconnector/test_result_json.h": "62b7931ff4eac1cf867943689aefac7d52bf2dea4e1cf1781467608120d9490f",
              "common/include/msconnector/transaction.h": "4a9af32abd6458c6be9e339ccba2f5ecc15cc0c782ccad9a402df0e4f363b76d",
              "common/include/msconnector/transaction.hpp": "739489f2b452da87390702e11cab3d9e11a09dfd2dbfabdaa0020964d4979d86",
              "common/include/msconnector/transaction_contract.h": "803cc283e89740f980bcfa98b46907302ed8e30502d0b9168ddecf41193ab8fe",
              "common/include/msconnector/transaction_id.h": "ecede908d5127bf8032ce4180d19b2b229b2b405e94d178f4142e463068b8eb0",
              "common/include/msconnector/transaction_state.h": "00a455c2d1523c1ab6cfd027f9fb2a9f85be2fecdbaaf2d62f039c7532104547",
              "common/rules/modsecurity_p1_p4_vectors.conf": "00ac195a80131405971f278c4eb87c9d125388d140476c1297915e6bbac02973",
              "common/rules/modsecurity_request_body_smoke.conf": "91d66822bec2a6f4abf30ede91b7f494f28235c5bc729936b6a0dd36c28af13d",
              "common/rules/modsecurity_response_companion_smoke.conf": "7aa57b053e725ec567c799eda73db7f071e601ab5a5ce0839d8c30e47f6b0b8c",
              "common/rules/modsecurity_targeted_smoke.conf": "f97e14ab1e1b739b2fc4abf3959c51ae9d76c53550d86b2162f3fccb71e0730e",
              "common/rules/p1_p4_traffic_vectors.json": "6298353b8725ef69ea740bddefdfde0ab704d9c2719c62bd702e8fa4673cbe05",
              "common/runtime/http_authorization_service.c": "7f1544f1f36042c68359c7caed7d5dc4ce8cc77d44282debdc3955ea725a5e9c",
              "common/runtime/http_authorization_service.h": "1c5996cca00ee2b89673a5157f598dc2ce06203f91941b9f44cc019e063de64a",
              "common/runtime/msconnector_runtime.c": "0fa85f5658be96a25204adf489b2e18149a5f826b5ed528e55ec7b2ffe410aa4",
              "common/runtime/msconnector_runtime.h": "202ac41d732d8ac5c1fec266bd7b49ae4cec1e0f5727c3c0d38832c6d58ceb3b",
              "common/runtime/response_companion_client.c": "8534bbde095b46507c7f4ad109c521fb8c9c03c76c43daa391fe1c44cdfbbc60",
              "common/runtime/response_companion_client.h": "581ff79c969225ebb768d9a2477f83716ee97a61f20ae6fbeee0c442ae7bc7a4",
              "common/runtime/response_companion_protocol.h": "634529f2801423b411b303e408f9735f4e1123294c4cba6dde79957ebb594188",
              "common/runtime/response_companion_transport.c": "268e522789b77af2d4942d6b5981c7ce582a4fad03a2822b79c26f1065e8ffc4",
              "common/runtime/response_companion_transport.h": "606e8a7c9d7ce1772cab3a638de7e48e3e025949be3bb0237fb658cb84989e8f",
              "common/scripts/modsecurity_targeted_eval.cc": "f0def448dba5107735c75262ae7568aec1fd2a6de18355902120c0d74b0afb18",
              "common/scripts/run_blocked_runtime_smoke.sh": "9308998ad3d2cba6b28709b373d2719a655dc77d32be71481ef41f8cf7028ca4",
              "common/scripts/run_local_runtime_smoke.py": "f06c33fc6f9084a4a36218153de944f523f42d5c0cc89469f9244efaa02b87dd",
              "common/scripts/write_smoke_result.py": "35d2d86164672dfbe0fc2c648e41ba03df38ad9a335cd655995d650f769cda77",
              "common/src/README.de.md": "760a994ec35908128f9a6beb68733d07af17d8d59de7061f06757a9042afaab7",
              "common/src/README.md": "7a7c5b9ddd534d333a3a212fd25602f0c84499d73822349f8cf97e7f9573b778",
              "common/src/adapter.c": "516e776a748c5a586089f429827215782cdb71b759b82bd7eec724cd5de1555c",
              "common/src/adapter_contract.c": "61c07a434ac5ffb3bb30ae0b50a146f5cbe783f69842a384f76e049e3fc124fb",
              "common/src/adapter_metadata.c": "56d5890cff7c152297688d00d994f6945c00397303d5f459cb9dfa7805eaeefb",
              "common/src/artifact_layout.c": "6468d87635446a35035a5aa2569d3b2341fc55a35e4ee2f27a3e32648455e453",
              "common/src/artifacts.c": "04859ebe04ffaedf894bdfe3e06cde921b8e527588b5ac53dca45f950fd4ed00",
              "common/src/block_statuses.c": "ea691e18cfb3ab2733b878f41cd802332b60d8eb9c8f3f56548c37495de736bf",
              "common/src/blocking.c": "4f2776c88c7b95ebc7c3adfdb12e147dad002594dd3f95e6a38051c615717460",
              "common/src/body_policy.c": "735027686a02d2e867e00bbd9d7eafc445c1f343eac1ec93b4289d4d4813cdb5",
              "common/src/build_contract.c": "792123920f333f0dc3505125df2d194b2319cffd3fb3d9adc5ef877a960497d0",
              "common/src/capabilities.c": "801d8f0d58c70a987104098fcb4e04d147d4ccd1dccc14e9accd6253efff6e3b",
              "common/src/capability_matrix.c": "fa01a76c4b0f4184b25710da06823ded6c0a38700b539864c892c717f7f0f277",
              "common/src/config.c": "3e5f6c0130b0c1f79a540444a96bb051596e6072843888f7b5aad8ae61560c27",
              "common/src/config_parser.c": "8dca03ec371a52681d1721bf76e8b4098599bf654755b7f489191cb5290168b6",
              "common/src/connector_manifest.c": "4a9e5456b6fd8c20dcd0eeff8ca3048cfdc7577f8da4ffa71a918c309e367f75",
              "common/src/crs.c": "d0a394d9e29df1bf80c4b7276bbd3bd7b12192d275856117d82615a9946263ef",
              "common/src/decision.c": "e42a17aa86541ecf573b336d049f57014a1a1a8e257613491a9d5e05cb44d174",
              "common/src/decision_action.c": "7c75f3b45f661300d8cdb328dec57ef4f403ba0ed0fa3fc8400d9aa55481b9a2",
              "common/src/directive_adapter.c": "402bd6fe396f774df3e990849882bcdce5d2e52abcb7973c4a8e0a6da4835263",
              "common/src/directive_spec.c": "8c75a3e97f781965ed023df99cc11adc0013e78f4bdaec0c9e26c664823b43ef",
              "common/src/dos_guard.c": "bfc304695a6801a5ab1256f9703429a506f80519fef15a7f9e6a271c004e17d7",
              "common/src/error.c": "4509eb4b33820c2ca6300b314f88c99e06d8a5e6361900783b8f7aafcee33f86",
              "common/src/event.c": "0032e25cac8dd310eee620f606f598db830a84898baf26575cfee19b03166e03",
              "common/src/event_jsonl.c": "dc3a21fa47075fe96f19d7b12c8015db7a8d2b407d65a678ab0f1487de1ddcef",
              "common/src/flow_guard.c": "8e43183bf42ace059c16ef7984fe5b835a822cd2b439f73f17cb96261ed7dc72",
              "common/src/generic_mapper.c": "ceacbb368c5bd35212a9a613b63b01b9e71158dd1aed3a6e0905febdee0ed850",
              "common/src/header_validation_internal.h": "b9ca7130e184913c10b3b24cfae18415eef411a908b1af5f926af6b695ed11e7",
              "common/src/headers.c": "1bc8351188daf20a9b8f0db47f73ec5a64afedef59776b56206b35f43666bc12",
              "common/src/http_status.c": "b6ad0c69ae47150170919096eaf7b444a097b0e8b88d25b0b7be13bbe9777a69",
              "common/src/integrity_event.c": "c2ad7f26cf051321e269f50d0e8afb9f3aa5a8a3a416f55e63e1278392753041",
              "common/src/intervention.c": "91c7fbd9cf158a2e46c59af2b534f0b77dae2cee84fff038509c129b471db4a2",
              "common/src/json_escape.c": "d9d8e7e1cfc6ad5e82e227044f5c8ebbbb8489f13caab99a8e3f02cf5d279e0b",
              "common/src/late_intervention.c": "aa29b1ad82f176320fdadbf2357ee616cc7ca1ff6966063911a4eb2c5cacc812",
              "common/src/lifecycle_status.c": "3dab0f986e7ed1959bb5d1425c666061bad6816dc8262c27a64e3ba49ff1c971",
              "common/src/limits.c": "3282ce8e7143a7d481e831cf02ec9d08729dd2f7c0015bccfdf336a409767aa0",
              "common/src/log_sanitize.c": "9fc0b1e53225fc95f3a43ec7ff0df4d2f0eb4bb363eee19ca3e693e0a958a943",
              "common/src/memory.c": "f38f868c0355a3722c027a477f0bd762f6c1a9a08a12c5c7b814aeec58cbe9af",
              "common/src/modsecurity_engine.c": "a77b04c3e2deaf5146e0e164efb56f32dc76eebab9e3eccc6604f0e9483fedd1",
              "common/src/origin.c": "559ec9880e83cd386f5986cfc155ea3dd8edfa7f379a39ebca7839f0cdbc7130",
              "common/src/origin_governance.c": "313e09a5b2865315a932d7243d9e5eee85b9a1c4dfb4276e60fb5c2d3fab32b2",
              "common/src/path_policy.c": "790146307f4600359ef3d6d573e6fc1b674b9b8e796ddfa67579f2d4b2086802",
              "common/src/redaction.c": "e7b74654e806615ee61569e8c6424be01bfeea61448cfebbb8c1be7f26c16c6f",
              "common/src/request_helpers.c": "f3c3d4ddd6693bc330a3ec24a1d1491af64ac2544a26696cf010babd1a4ce790",
              "common/src/request_mapper_contract.c": "df427fc2e28a4a94cf252470654a46453335cf361919f229c0f328d54f9a746a",
              "common/src/resource_limits.c": "0affa0f5ad598aa94dc6ce8b480c178adcf7b2be4b9a12f9fed6ee82a17c0767",
              "common/src/response_helpers.c": "d24c987d55e2b362035d04dda5a81889026aafdad9d1a1541c741cba9ed19cda",
              "common/src/response_mapper_contract.c": "e7d71677bbc94f21268502cb64163038d17bdad8307049df66ad07b2597574dd",
              "common/src/rule_error.c": "0e6e1756e43fc946bec2c2ee090681d6398339da240121595e891aaf76e90735",
              "common/src/rule_event.c": "18676a24a88c33a7f991b777d96d151ba364541153b6265498a6be6cb5b54387",
              "common/src/rule_id.c": "6cf8cc24a6de62e74376edf73bd589b3f4c26f66dc0a53ae92b626d5ac70435b",
              "common/src/rule_loader.c": "e837121b19b1239e2667cc97b5c3279066f36c20b63afd2ca1e6c544407a4e56",
              "common/src/rule_merge.c": "db7b8097adaffa612d19ccf23253b2e583db161904fa1b9a9e3ee37e48330b15",
              "common/src/runtime_paths.c": "168de23208e3b00647caf543307bec0e3029db5ac78e18e3c8e1be23e4340b07",
              "common/src/runtime_report.c": "e7e61cf66cc7c64adeda7449b480a96b49f1b0efa758c5b8fe3536db6720a30e",
              "common/src/status.c": "8cae41d98f3ee4f8978e01100c59b2882a078e683fae38c42839d3bf3566ccca",
              "common/src/test_result.c": "997b5f047b7d3fd77e457135945961314fc64e21beb636685761dde85bbed86a",
              "common/src/test_result_json.c": "d904738d35db3579b6cd4ea3b12ff14caabd0090754fb30bb1da8f7072cc1c78",
              "common/src/transaction.c": "b6f621703ef7238295eb49257666e6d6a4249333bf4ae939d1fbab9a06712bdf",
              "common/src/transaction_id.c": "64630d1671bf58fec7f208aa43b957da915d9f2cbcd65a1ffba2ab06c741beaa",
              "common/src/transaction_state.c": "b4f35347531cc380f8bf71c3c7192ddb46442974a14374d332037373b6ffe860",
              "connectors/envoy/ext_proc/README.de.md": "379168c919b0583350f44bb0048b0aecb9d5b7f3ae154e516254b4c0be581cf6",
              "connectors/envoy/ext_proc/README.md": "84eee6a0c2e813b8cf737006853780c70253d6030959442b98716c087eddae7b",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_common.go": "019d7149165a5f1709d1dc4228581e6aba64c453654d70a7c541a6400602ac09",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_passthrough.go": "e8ca083f672809f0ad410f49b3c91df735415cd92ff5ea021e196664a216729f",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_passthrough_test.go": "9d9c571342716ce1303a531f26e6b8f28632e07fe89e8c23ff73bec5cada1707",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/main.go": "c07f99755bb1a1fbad95fc2f70941937a4a517bcfbf19865c8ddef8d64dbe1d0",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/main_test.go": "6fcafd2256758062d620e4c8633b31fbea3cca7793363e29dba8b97e41a95954",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/observer.go": "d86e8a45d3329a04317d9447d4f1e2efeea8146053bbbb3d6285341fee3e9ec4",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/observer_test.go": "c26b6281069fb364fef756d6b496ccc8d3ad837ff17775126e493d7a367ba9f9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/engine_common.go": "2442966b3c81b188be15753a0c9829b43299ee747eae5b9b86054ce9a9eb1758",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/engine_passthrough.go": "5447b3e4ac36aca83e7567d9ac602283f923c9e7e5a155f9fc88fccedacb3c65",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go": "d356dcbf1007e62d7b973c9bdc055015b64bab060d558162b3e96771dc664d52",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main_test.go": "5c1840c4d051031d36b1ccd86f95c6cfc06142ba476122bdbfe697b6f3db3848",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main.go": "8ef1046f9549b46a1fa88bf399696f263e7c2faee107e52c0c4a30ced6f41db9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main_test.go": "5ec9223b304dd63932d05cc6a51839a6fd9d59598d178b2afd177134da3520d9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/peercred_test.go": "44991db7bd1bf9c0c8262c9c97b9be6bcf6130c20a74b42deda7894cb6ff9ac5",
              "connectors/envoy/ext_proc/go.mod": "9a52853f5e3839f500655c1d6cc8785b7cd379da55fe8e9a6374ac8ff0ece7c6",
              "connectors/envoy/ext_proc/go.sum": "66100e55eddccb812d04e1b841a7721c25cbab30b0cd5e690242368b7d2f5963",
              "connectors/envoy/ext_proc/internal/composite/coordinator.go": "507b4b2117a1b6582b0e0eacc8a4723b466bedf26b4b8d0752dc2ba3d8f3f9fe",
              "connectors/envoy/ext_proc/internal/composite/coordinator_test.go": "cc8c9b2c37a896b4e03177d073e6a8074896f663f4cbc77475856b2de6f69ab4",
              "connectors/envoy/ext_proc/internal/composite/i12_envoy_observer_test.go": "7a12e7dc914899a337b42defbebb793d1fb96757e170d4a8bbfb4a95a5d7e07c",
              "connectors/envoy/ext_proc/internal/compositeenvoy/common_body_completeness_test.go": "a2559bba9226e56b312b111b33aea7651c6160b8064e9d78fd000d941cf79992",
              "connectors/envoy/ext_proc/internal/compositeenvoy/common_runtime_integration_test.go": "8ae2100dfbfa6b64bc0b1b4b04765272e62ec261db3127a1342a053f9aa33bf9",
              "connectors/envoy/ext_proc/internal/compositeenvoy/server.go": "028e1e21cf1e1313cee0e951b82fd8fcb9c492bbf1dd63401455585d01c6db4a",
              "connectors/envoy/ext_proc/internal/compositeenvoy/server_test.go": "595be39d20afa24ab6fa4e747d5b397d0c1948b61bb6e5272f24cf3720e6a5d0",
              "connectors/envoy/ext_proc/internal/compositeenvoy/technical_error_test.go": "6cfbc98bad68ab30fffa836db5c47a60a9312b9864f0251eed1667c711eb0055",
              "connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go": "7f7a2776032b702a101222ef38db60d012f263aedac9fa67a721613e5c606e2d",
              "connectors/envoy/ext_proc/internal/compositetraefik/forwardauth_test.go": "01e82e24837612a493e9d48469a4440ace95fd79b9f7e55c10e767381a99678b",
              "connectors/envoy/ext_proc/internal/compositetraefik/uds.go": "07202ce16684e08d3ab4b46f0c3385a50491b4c6a59d6028bd5e29cccec2151b",
              "connectors/envoy/ext_proc/internal/compositetraefik/uds_test.go": "aa0215397c66b8d33ab6c5b65883a2bfaffbc154031ffde0e596f55c6a78fef8",
              "connectors/envoy/ext_proc/internal/processor/body_limit_host_action_test.go": "1ac63d7c8ecfbff3481a03be9f536124069e6dda043ed308afaff9877d729e4e",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c": "6449bd0d2cb2a71676d09bf6f8d464bfa1d68f0dbab73f61887c028fedd8ccec",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.h": "c06ab9f8ef468f241186232caf47fafc5cf12eef2d76b57cd016825573520783",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_commit_test.go": "3811b81a35710cda0723c6451032c0a2e7008f8b360bb93aa38077c2355be25c",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go": "3df8f38891d9a9ee0053ac5beba6615cdce5772661af8cffe8c0c62506daa1d8",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go": "7e9a89cb1e233dcbc23c740a8636786c4bd65f57aa6fae6efe07f2aacbcac455",
              "connectors/envoy/ext_proc/internal/processor/config.go": "321b16b82919ec43b0f12dc59b5de55058496930e1a4cfcea8a51d7c55da8851",
              "connectors/envoy/ext_proc/internal/processor/config_test.go": "4140137ebcefd1e04da6cb728d8a2284640142f68a5464b39f50e61c27c04dec",
              "connectors/envoy/ext_proc/internal/processor/i12_envoy_observer_test.go": "433b6d3ece97401bb7f910d8b29860f8ece7931e88be7f1155082f68b8942130",
              "connectors/envoy/ext_proc/internal/processor/jsonl.go": "1ff55bf56bfb02f594cc8f2a09b7efa128f106d404c32568716845add50117d6",
              "connectors/envoy/ext_proc/internal/processor/jsonl_test.go": "c784a60e1ede32bc40ce3df11a1b16ec5850f75f74432a905a45567222fdca8a",
              "connectors/envoy/ext_proc/internal/processor/phase4_budget_test.go": "6f8ff027396578421764374d5e88a0e29e52a547e651f6cda5b5211bd3f9f064",
              "connectors/envoy/ext_proc/internal/processor/processor.go": "6c8461d73cd43b2a789ca69a2477c0e1f2440b3346bd27ad9bccc469d48b1762",
              "connectors/envoy/ext_proc/internal/processor/processor_test.go": "3848137c942fab9593ee227a2c73494cc262b4867ebadc014ba35b90f73af449",
              "connectors/envoy/ext_proc/internal/processor/technical_error_test.go": "3653bd940540c94ee799f50c2b09556cc7027b131cf4d1929c61f8051e7890cd",
              "connectors/envoy/ext_proc/internal/responseobserver/client.go": "8869025eec2ad73e330291c96d2812bb52ff6f79b14d5fef6c195661070b3473",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_linux.go": "77238e197fec60ec668ceeafde35d27a577da4e8d6ff3f48b3a742d4d7cbbaf6",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_linux_test.go": "de350e573b0d62f5ea31a76a318226217092f69ac653505d87d6376a14621e7f",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_other.go": "74349b4b04faadbfbf3d40644474700543120f5539e445202ae25176f1c5b36a",
              "connectors/envoy/ext_proc/internal/responseobserver/protocol.go": "f497571a69479edbc68094594e6d75f6633d238662e42be6640412d9d04ce0cb",
              "connectors/envoy/ext_proc/internal/responseobserver/protocol_test.go": "a6c489c75f18ca8062b43455c6c7d533738b05ef2249f13f4004a29a77b15537",
              "connectors/envoy/ext_proc/internal/responseobserver/service.go": "6e96afed63fd7343e9bc1188950b38d23371f08063c50dba4f276eda2d74c633"
            }
          },
          "case": "I12::envoy-ext-proc::NEED-request-eos-once",
          "delivery_scoped_verified": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
          "delivery_source_baseline": "02754040bced960cfc1857416cd7101bb3116ef4",
          "engine_sha256": "19f0f7bb1f48edfa86e2567ae107d01ceb7f9fafa6c3d87d0d25d8242ea56b1c",
          "fixture_configuration": {
            "/mnt/fixtures/native.rules": "ddf5a99206fd053fea66ac923bc18584610ac96c8272864382951a4398ed4dff",
            "/mnt/fixtures/shape.json": "e4db8156eae18724c387d0b638964fade9fa3ad4bff2dc439f3148a10d64bacf",
            "/task/runtime/envoy.yaml": "c47bd1be9b18189b56a4a4a648274c23155f1b277d5b2d9348e88af1461d1abe",
            "/task/runtime/loopback.crt": "5f84405e4c30faf833b519ca05dcc6b5fe53de9599befaccef6a96ed3317aef7",
            "/task/runtime/loopback.key": "1ffeeb9df5ad52798f65b5ad1c483a1f8c5bf9ca9720e5f2907149f92b117c6b",
            "/task/runtime/native.conf": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb"
          },
          "host_sha256": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
          "product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
          "rules_original_sha256": "ddf5a99206fd053fea66ac923bc18584610ac96c8272864382951a4398ed4dff",
          "run": "envoy-i12-env-extproc-c2cc4f40",
          "runtime_backend_profile_actual_source": "envoy-ext-proc Common runtime backend reused by actual composite adapters",
          "source_git_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness and declared private overlays",
          "source_scope_count": 167,
          "wrap_symbols": [
            "msconnector_transaction_contract_init",
            "msconnector_transaction_contract_finish",
            "msconnector_transaction_contract_cleanup",
            "msconnector_transaction_contract_complete_phase",
            "msconnector_transaction_contract_set_response_committed",
            "msconnector_transaction_contract_record_response_metadata",
            "msc_new_transaction",
            "msc_new_transaction_with_id",
            "msc_transaction_cleanup",
            "msc_process_request_body",
            "msc_process_response_body",
            "msc_process_logging",
            "msc_append_request_body",
            "msc_append_response_body",
            "msc_process_request_headers",
            "msc_process_response_headers",
            "msc_intervention",
            "msconnector_runtime_transaction_begin",
            "msconnector_runtime_transaction_begin_request_stream",
            "msconnector_runtime_transaction_append_request_body_chunk",
            "msconnector_runtime_transaction_finish_request_body",
            "msconnector_runtime_transaction_process_response_headers",
            "msconnector_runtime_transaction_append_response_body_chunk",
            "msconnector_runtime_transaction_finish_response_body",
            "msconnector_runtime_transaction_finish",
            "msconnector_runtime_transaction_destroy",
            "msconnector_runtime_transaction_finalize_and_snapshot",
            "msconnector_runtime_response_companion_handoff_with_handle",
            "msconnector_runtime_response_companion_claim_handle",
            "msconnector_runtime_response_companion_revoke_handle",
            "msconnector_runtime_response_companion_session_process_response_headers",
            "msconnector_runtime_response_companion_session_append_response_body_chunk",
            "msconnector_runtime_response_companion_session_finish_response_body",
            "msconnector_runtime_response_companion_session_set_response_commit_state",
            "msconnector_runtime_response_companion_session_record_host_action",
            "msconnector_runtime_response_companion_session_fail",
            "msconnector_runtime_response_companion_session_cancel",
            "msconnector_runtime_response_companion_session_release"
          ]
        },
        "actual_scoped_baseline_inputs": 167,
        "delivery_scope_verified": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
        "git_source_base": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness and declared private overlays",
        "native_config_sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb",
        "product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "rules_sha256": "ddf5a99206fd053fea66ac923bc18584610ac96c8272864382951a4398ed4dff"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "ddf5a99206fd053fea66ac923bc18584610ac96c8272864382951a4398ed4dff",
    "run_id": "envoy-i12-env-extproc-c2cc4f40"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 332250,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-envoy-extproc-01.json",
    "sha256": "d67e7992a966f1f75e416c5340a1d566e753114689a3adce117040e7dc918f2f"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::envoy-ext-authz-request::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 158021,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/native-lifecycle.jsonl",
          "role": "cleanup_observer",
          "sha256": "a4a241d68523061431233c06407a604eb2e1cb273dfb6a905a36fd3f9559b447"
        },
        {
          "bytes": 1880,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/result.json",
          "role": "cleanup_observer",
          "sha256": "a7ae2e617f951bbf9eb363713daf5eb1f9dff4408847ac729e58a27092d50ae0"
        },
        {
          "bytes": 4557,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "9c89a3be4f6ace1156a5d9f2c3713d7c7e5681e9a4eb60765918d0b7acc69a04"
        }
      ],
      "value": {
        "Go_C_atexit_absent_actual_snapshot_used": true,
        "actual_collector_snapshot_after_real_engine_close": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
          "contract_state": null,
          "edge": "snapshot",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 107763403525009,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 266,
          "profile": "envoy-ext-authz-request",
          "result": null,
          "run": "envoy-i12-env-request-fb9cdd12",
          "runtime_eos_handoff": null,
          "runtime_finalize_snapshot": null,
          "schema": "native-lifecycle-v1",
          "sequence": 142,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792017397192930455,
          "wall_sample_end_monotonic_ns": 107763403525178
        },
        "actual_runtime_destroy_return": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 66,
            "canonical_transaction_id": null,
            "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 107758229960156,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 266,
            "profile": "envoy-ext-authz-request",
            "result": null,
            "run": "envoy-i12-env-request-fb9cdd12",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 71,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792017392019365630,
            "wall_sample_end_monotonic_ns": 107758229960278
          }
        ],
        "driver_actual_waited_process_exits": {
          "backend": {
            "forced_kill": false,
            "pid": 262,
            "proxy_pid": 261,
            "signal_sent": 15,
            "waited_exit_code": 0
          },
          "engine": {
            "forced_kill": false,
            "pid": 266,
            "proxy_pid": 265,
            "signal_sent": 15,
            "waited_exit_code": 0
          },
          "envoy": {
            "forced_kill": false,
            "pid": 278,
            "proxy_pid": 277,
            "signal_sent": 15,
            "waited_exit_code": 0
          }
        }
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 158021,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "a4a241d68523061431233c06407a604eb2e1cb273dfb6a905a36fd3f9559b447"
        }
      ],
      "value": {
        "actual_common_finish_calls": 2,
        "actual_native_logging_calls": 1,
        "common_finish_idempotent_second_call": true,
        "observed_public_runtime_finish_wrapper_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 6325,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "75643e95d19d9be9af3ac2e09f2adbeb454df893a025d2f6bf5d889769d4ef4f"
        }
      ],
      "value": {
        "actual_finite_authz_sample": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": null,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": true,
            "declared_size": 13,
            "grpc_send_error": null,
            "monotonic_ns": 107758210515485,
            "operation": 11,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017391999920813
          }
        ],
        "actual_request_body_input": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107758210594652,
            "operation": 1,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017391999999980
          }
        ],
        "actual_response_body_end_of_stream_input": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107758227738884,
            "operation": 1,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017392017144238
          }
        ],
        "native_raw_host_eos_fields": null,
        "transport_eof_is_separate": true
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 158021,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "a4a241d68523061431233c06407a604eb2e1cb273dfb6a905a36fd3f9559b447"
        },
        {
          "bytes": 6325,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "75643e95d19d9be9af3ac2e09f2adbeb454df893a025d2f6bf5d889769d4ef4f"
        }
      ],
      "value": {
        "actual_finish_entry_return_callbacks": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107758210906322,
            "operation": 3,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017392000311626
          },
          {
            "actual_result": 1,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107758211211353,
            "operation": 4,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017392000616705
          },
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107758228084181,
            "operation": 3,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017392017489511
          },
          {
            "actual_result": 1,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107758228664274,
            "operation": 4,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017392018069623
          }
        ],
        "actual_nested_runtime_native_finish_spans": [
          {
            "actually_nested_native_returns": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 23,
                "canonical_transaction_id": null,
                "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "iaZg0W6RGSjwHIRT-kelX8wyYp-y0cKPbwtH9Q8hjBw",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 107758211087285,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 266,
                "profile": "envoy-ext-authz-request",
                "result": 1,
                "run": "envoy-i12-env-request-fb9cdd12",
                "runtime_eos_handoff": null,
                "runtime_finalize_snapshot": null,
                "schema": "native-lifecycle-v1",
                "sequence": 24,
                "transaction_id": "iaZg0W6RGSjwHIRT-kelX8wyYp-y0cKPbwtH9Q8hjBw",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792017392000492868,
                "wall_sample_end_monotonic_ns": 107758211087526
              }
            ],
            "entry": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 22,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107758210940357,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 266,
              "profile": "envoy-ext-authz-request",
              "result": null,
              "run": "envoy-i12-env-request-fb9cdd12",
              "runtime_eos_handoff": "request_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 22,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017392000345804,
              "wall_sample_end_monotonic_ns": 107758210940468
            },
            "return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 22,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107758211197044,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 266,
              "profile": "envoy-ext-authz-request",
              "result": 1,
              "run": "envoy-i12-env-request-fb9cdd12",
              "runtime_eos_handoff": "request_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 29,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017392000602483,
              "wall_sample_end_monotonic_ns": 107758211197146
            }
          },
          {
            "actually_nested_native_returns": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 51,
                "canonical_transaction_id": null,
                "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "iaZg0W6RGSjwHIRT-kelX8wyYp-y0cKPbwtH9Q8hjBw",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 107758228536720,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 266,
                "profile": "envoy-ext-authz-request",
                "result": 1,
                "run": "envoy-i12-env-request-fb9cdd12",
                "runtime_eos_handoff": null,
                "runtime_finalize_snapshot": null,
                "schema": "native-lifecycle-v1",
                "sequence": 52,
                "transaction_id": "iaZg0W6RGSjwHIRT-kelX8wyYp-y0cKPbwtH9Q8hjBw",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792017392017942205,
                "wall_sample_end_monotonic_ns": 107758228536853
              }
            ],
            "entry": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 50,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107758228115798,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 266,
              "profile": "envoy-ext-authz-request",
              "result": null,
              "run": "envoy-i12-env-request-fb9cdd12",
              "runtime_eos_handoff": "response_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 50,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017392017521243,
              "wall_sample_end_monotonic_ns": 107758228115894
            },
            "return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 50,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107758228645266,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 266,
              "profile": "envoy-ext-authz-request",
              "result": 1,
              "run": "envoy-i12-env-request-fb9cdd12",
              "runtime_eos_handoff": "response_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 57,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017392018050700,
              "wall_sample_end_monotonic_ns": 107758228645349
            }
          }
        ],
        "raw_argument_eos_and_host_eos_fields_preserved_null": true,
        "selected_official_native_complete_body_contract": "processRequestBody/processResponseBody invoked once only after direct host body EOS; SDK appends have no EOS argument"
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 158021,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "a4a241d68523061431233c06407a604eb2e1cb273dfb6a905a36fd3f9559b447"
        }
      ],
      "value": {
        "actual_common_cleanup_calls": 1,
        "actual_native_cleanup_calls": 1,
        "actual_runtime_destroy_calls": 1
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3494,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/before-request.json",
          "role": "loaded_image",
          "sha256": "9a71e33bdde52d0a864b9000f3f597bb8f7c4e6d354f9c186b92accb483bb2e6"
        },
        {
          "bytes": 227,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/bootstrap-observation.json",
          "role": "isolation_receipt",
          "sha256": "15459d71017ca2f3f00417e6ef1b654aefca42f85607d7c99671c768ea0a14db"
        }
      ],
      "value": {
        "actual_processes": {
          "backend": {
            "executable": "/usr/local/bin/python3.14",
            "executable_sha256": "aa4ec29748e8f5cfd800a83448daa49b3dc384dd9ddaea9823677181238dd1f2",
            "fd_count": 4,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2253162]",
              "2": "pipe:[2253163]",
              "3": "socket:[2255172]"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [],
            "pid": 262,
            "proxy_pid": 261,
            "vanished_during_snapshot": []
          },
          "engine": {
            "executable": "/task/cache/msconnector_composite",
            "executable_sha256": "719a9ddd277e9b04482d55684266a96989b384e37789df6d8482549a46e7fcc8",
            "fd_count": 11,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2252409]",
              "10": "socket:[2255186]",
              "2": "pipe:[2252410]",
              "3": "/task/runtime/native-lifecycle.jsonl",
              "4": "/task/runtime/native-audit.log",
              "5": "anon_inode:[eventpoll]",
              "6": "anon_inode:[eventfd]",
              "7": "/task/runtime/native-debug.log",
              "8": "/task/runtime/adapter-events.jsonl",
              "9": "/task/runtime/common-events.jsonl"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [
              {
                "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
                "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
              }
            ],
            "pid": 266,
            "proxy_pid": 265,
            "vanished_during_snapshot": []
          },
          "envoy": {
            "executable": "/task/cache/envoy",
            "executable_sha256": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
            "fd_count": 25,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2255193]",
              "10": "pipe:[2252417]",
              "11": "pipe:[2252417]",
              "12": "anon_inode:[eventfd]",
              "13": "/dev/null",
              "14": "socket:[2252418]",
              "15": "/task/runtime/envoy-access.jsonl",
              "16": "socket:[2252428]",
              "17": "anon_inode:[eventpoll]",
              "18": "pipe:[2252429]",
              "19": "pipe:[2252429]",
              "2": "pipe:[2255194]",
              "20": "anon_inode:[eventfd]",
              "21": "anon_inode:[eventpoll]",
              "22": "pipe:[2252432]",
              "23": "pipe:[2252432]",
              "24": "anon_inode:[eventfd]",
              "3": "anon_inode:[eventpoll]",
              "4": "anon_inode:[eventfd]",
              "5": "anon_inode:[eventpoll]",
              "6": "pipe:[2252416]",
              "7": "pipe:[2252416]",
              "8": "anon_inode:[eventfd]",
              "9": "anon_inode:[eventpoll]"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [],
            "pid": 278,
            "proxy_pid": 277,
            "vanished_during_snapshot": []
          }
        },
        "actual_uid_gid": [
          65534,
          65534
        ],
        "host_version": "/task/cache/envoy  version: b579d07d3ad7ee11d32b105e91a5a39ad24718d7/1.39.1/Clean/RELEASE/BoringSSL",
        "native_who": "ModSecurity v3.0.14 (Linux)"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 40035,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/build-manifest.json",
          "role": "source_manifest",
          "sha256": "918ad320967983b7dfea45687d2e4a2f54c45ab39daf9503d7c44be616455015"
        },
        {
          "bytes": 54602,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/scoped-product-source-equality.json",
          "role": "source_manifest",
          "sha256": "40ddedbe31c9b7bf55f48b2906f29c2a245ad726a9b4523964e3b2e2f9bc84cb"
        },
        {
          "bytes": 241161,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/source-ledger-v1.json",
          "role": "source_manifest",
          "sha256": "6b4ba0985efbda2f4dded97c5be54933c6d5d2c185b46862e660628d662f49b4"
        },
        {
          "bytes": 399,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/native.conf",
          "role": "effective_configuration",
          "sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb"
        },
        {
          "bytes": 961,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/request-v2/fixtures/native.rules",
          "role": "effective_configuration",
          "sha256": "8e271f02c84fb6aa0671fb8f2b18144903da6b33764a5f676eac11dcb51de42d"
        },
        {
          "bytes": 7559,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017342224404569/data/runtime/envoy.yaml",
          "role": "effective_configuration",
          "sha256": "cc78f9be754480a54340275ff9fb0963b511e4bb63b08593fbefac28a31d45b3"
        }
      ],
      "value": {
        "actual_build": {
          "actual_external_build_provenance": {
            "actual_build_receipt": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/build-control-07/receipt.json",
            "actual_build_receipt_sha256": "8dcf87861e481f33051d52bc0617052b125f49071620bcaae70be3f83bc6fbc3",
            "actual_host_not_launched": true,
            "binary_hashes": {
              "envoy": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
              "msconnector_composite": "719a9ddd277e9b04482d55684266a96989b384e37789df6d8482549a46e7fcc8",
              "msconnector_envoy_ext_proc": "19f0f7bb1f48edfa86e2567ae107d01ceb7f9fafa6c3d87d0d25d8242ea56b1c"
            },
            "scope": "fresh external actual native build; reused pinned realEnvoyhost binary only",
            "scoped_product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
            "selected_sdk_image_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
            "source_baseline_git": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness + declared private overlays",
            "source_sha256": {
              "ci/runtime/lifecycle/aggregate-five-connector-no-crs.py": "641b11df919f35412de9d287e734f07c8027100cbff596cf54ff0f572a0890f9",
              "ci/runtime/lifecycle/aggregate-five-connector-with-crs-no-mrts.py": "43b22adfe39bed7c1bbd7aa0b2d3b70c6af40850579f4b6d598d7fd07d1ac556",
              "ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py": "af83ee477c71ef9da7e75820615e6dd4c3423b5bab21df585655f85549e98a52",
              "ci/runtime/lifecycle/cases/apache-phase4-response/allow.yaml": "f7a63436fa8b874e5395f3e3bfa9cc89296eb0693622a0fcfcd4f8509ec69315",
              "ci/runtime/lifecycle/cases/apache-phase4-response/custom-mime-deny.yaml": "86103d9de76ada3a496cc32b19cb58cb78fbdc6b02a2154dc960d555be701168",
              "ci/runtime/lifecycle/cases/apache-phase4-response/empty-allow.yaml": "9f164c02f5a95f4f22d7d8c6be467ab4e5c923c79008cb0388d9dcb68c6b407a",
              "ci/runtime/lifecycle/cases/apache-phase4-response/empty-deny.yaml": "5d924a1106bf3a06cfa1c579784e9d8aa9e0cec09d9a4d0150e5531211c2b811",
              "ci/runtime/lifecycle/cases/apache-phase4-response/engine-limit-process-partial.yaml": "4f38b6398eb211da297f71c3a1ad8d5d8fe88808c18926e8aa3b9bddcae6c91f",
              "ci/runtime/lifecycle/cases/apache-phase4-response/limit-reject.yaml": "fb6fcb54b443ba6fe661607c07cc4fc2c29f0b89d52b06f098893890661f96cd",
              "ci/runtime/lifecycle/cases/apache-phase4-response/log-only.yaml": "c6cb64c259226c5a65d755deb5ea7f196a2da18fd121844b781b76e2e94b5ebd",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-deny.yaml": "0f5f3ad1c29229d47de25bdfcaf8fbe67f5acbff44899866e3a7c4ebe275874c",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-phase3-deny.yaml": "ff042a9a5e71d1ee48ffe26397f7b67cf99ca7b464ec624c6681d30dc0195f82",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-phase3-header-freeze.yaml": "1b1ddecef36454f0dbd8444cae1baf49ae41ff9c38abd6affb4e90a2d967cc3d",
              "ci/runtime/lifecycle/cases/apache-phase4-response/redirect-uri-policy.yaml": "b9244adda39713af220b7e05f97746015c4248ea281db692d431a2bc773482ce",
              "ci/runtime/lifecycle/collect-no-crs-source.py": "132df7f2292847ebca9688eaa33bf14b5ce5f09cb4bdbb4b5006afab32f5da65",
              "ci/runtime/lifecycle/consume-no-crs-selected-cases.sh": "8f99d061c30e9124782346667bd55936759c96887afdf75840d9540003d62655",
              "ci/runtime/lifecycle/five-connector-no-crs-profile.py": "39d492145ac7e8b03de8b2e089f6eb0a6ee5c065313201238acd561df154247c",
              "ci/runtime/lifecycle/native-lifecycle-observer.c": "ad8e5e36a17e746cf202c685dbb529fc09717f5c25441b713fa369420aa55ac6",
              "ci/runtime/lifecycle/native-lifecycle-observer.h": "f9f63b62ba8efc555dc20e673cc02251d5ab6c2ab17d8f5efa760d0d97146dcd",
              "ci/runtime/lifecycle/native-lifecycle-sdk.cpp": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
              "ci/runtime/lifecycle/nginx-native-operation-source.py": "3cf60b721a35540d28e91f03b3e78a0066d7983ccac02937428a2b4b688961c4",
              "ci/runtime/lifecycle/nginx_native_authority.py": "7e38a25917e38f99d8c9c102ba62093b4b50d161243926e5dde8da986d1353ca",
              "ci/runtime/lifecycle/nginx_native_collection.py": "b39b3132f36739a6e68596ebaad90ec3ebd102185f728b375f9a5ff5a0c494ca",
              "ci/runtime/lifecycle/nginx_sequence_client.py": "3f8f2220295e7c6c60351dc27525b273040ccaa3bb4e848cd28dc49fe3ca49e0",
              "ci/runtime/lifecycle/nginx_sequence_upstream.py": "8c52f8592037955c9c4cbcf919a066e30be7920eb8d34ab77724f8b7c9b466f7",
              "ci/runtime/lifecycle/normalize-with-crs-no-mrts.py": "5cb7ab24b61a2a590bf9768d2654bff721702ded2f4a90b90d3fa5ef94d928ec",
              "ci/runtime/lifecycle/plan_full_matrix_ports.py": "741760d3154845591e9a9707e0780da6d8ec3a2b020d17393ff95ee9ac63ed40",
              "ci/runtime/lifecycle/prepare-fresh-crs-source.sh": "fdb553b7ccf385fd990141821c678ca9289af66eae1e9ee9e717d2bcd5529f7f",
              "ci/runtime/lifecycle/prepare-verified-runtime-paths.py": "c8dbb1ecd0ff5e953dae40ca29102f091c6c8b05d48b63f7bc119e97e18f89c2",
              "ci/runtime/lifecycle/prepare-with-crs-no-mrts-upload.py": "57b7a2493293f5c49b0b440d8374758e107a610944260731de13168cafc7fec1",
              "ci/runtime/lifecycle/project-haproxy-runtime-evidence.py": "700c12482a563b4d8872ee8717adf9c6e6f5c321fc8361faf8e98f0bc524de6a",
              "ci/runtime/lifecycle/reserve-runtime-env-snapshot.sh": "a5a2153d8b50f1b6d2926659b364c92ebe726b0caaa9a06ab0bfc1b910a6ee02",
              "ci/runtime/lifecycle/resolve-full-lifecycle-profile.py": "474fe90d7bec9610f52c84e490708a0cf86cc27cba1675525c6290fae20a11b5",
              "ci/runtime/lifecycle/resolve-lighttpd-host-binary.py": "39dbf6ff78ba18b83fb18a4b529d96b98ed7879fdd5e0ab0afa1b59459c529e6",
              "ci/runtime/lifecycle/resolve-traefik-host-binary.py": "2d667abb8b167d2de1a254e6a873f262af4d004bd129d9e7bf57eb59f6eb9b96",
              "ci/runtime/lifecycle/run-apache-phase4-response-regression.sh": "78f2a5bf2999f54753af9d6141398259cfccd216a026d5c11670befa9addd295",
              "ci/runtime/lifecycle/run-bounded-nginx-cases.py": "3f4cfa011fe5f14eef36c3683a07994265dfb65fb6d636374a2e73dbae192262",
              "ci/runtime/lifecycle/run-connector-stage.sh": "3904616de7539858a396227e14b0bb5537026b7044719889a360d3e0955d78dd",
              "ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh": "e36c1a937e1c52b070f4247549993e07234e87f1cca7c4ddfb71ba34b65d3408",
              "ci/runtime/lifecycle/run-full-matrix-job.py": "d5f33cb3416e747567a6bda924df1d01ad1a8d7f156a8eb441b6afef463cb56b",
              "ci/runtime/lifecycle/run-full-matrix-parallel.sh": "a20fb467ccc18119573a7b58191421d26be795aff7eddc63724d54e68c080e10",
              "ci/runtime/lifecycle/run-full-matrix-resume.py": "5ce95bfe1ff0c7ea7cf0e7bda0111efde1425ac067af1fab534aa74aea419ddb",
              "ci/runtime/lifecycle/run-full-mrts-runtime-matrix.sh": "4badc2bdf2bad27f0a7c8f3fc563633792459fdf5f56773b94d3f014fcfda6db",
              "ci/runtime/lifecycle/run-legacy-open-connector-smoke.sh": "5d0330ded4e6056466c75e8e31dc571a40926adf296718339f0264f8bed2e529",
              "ci/runtime/lifecycle/run-mrts-native-full.sh": "83dc3ed6cf300cc8aa34aa1497846c1da13942d9e7f5f07e7ba972a9686a6b48",
              "ci/runtime/lifecycle/run-native-case-comparison.py": "1b9e0917c255b5d18cd41e2b03945f7136b6e6989110afde9b332bf8a707516d",
              "ci/runtime/lifecycle/run-native-first-byte.sh": "6c60df7102afea95972c2dcb2dee1685033cc99bc9b06ec369ae81053afcec91",
              "ci/runtime/lifecycle/run-nginx-common-input-fault.py": "a77af00e0c851c2b92e36ac6742dc8ea7a12c02466956ef59fba9f5f00c2458f",
              "ci/runtime/lifecycle/run-nginx-configtest.py": "aed2542ad0bf72af9fd25c3f6f18ecb6f656ef699d615fdf032fe5b3ffe9869f",
              "ci/runtime/lifecycle/run-nginx-event-boundary-cases.py": "9c2475c2c64d48611f62301a581d5e920cfbfbc3693949c40b37cc9cecd39c14",
              "ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py": "73829a2b184c92d3c771334efd0363f72a6ea8f95756ac7b3c6159e4e54b45d8",
              "ci/runtime/lifecycle/run-nginx-mime-cases.py": "75c63cad1de90401b33552715d4a02bb25eca55783b033e831d5430ecbd75fd7",
              "ci/runtime/lifecycle/run-nginx-phase4-cases.py": "32f9fb88a546eec9bd6dece0b86686f312729844c7960ddb5a2c1f49084064fa",
              "ci/runtime/lifecycle/run-nginx-raw-h1.py": "29a7d386ed6755f4e2f6a8226ee168d40809b69043cdc5fbcd6d9a74b6eebd1c",
              "ci/runtime/lifecycle/run-nginx-selected-host.sh": "7f77dffdda373e423a9c43076c30c44d13af1a10aca3763bc652620c11f68bce",
              "ci/runtime/lifecycle/run-nginx-valid-rules.py": "f22b5bf4ed5ac4cef52db9c8590ddede79b48043ed25de5f2ffee8260ad4b69c",
              "ci/runtime/lifecycle/run-no-crs-baseline.sh": "d520534d0acb18cb75d2e00c5b7d666a1398a4144b535a07fd452b74d799afe3",
              "ci/runtime/lifecycle/run-remaining-connector-target.sh": "163127a02f4caca1f860e86681da34e6b60c20d8d0d99f79026591482048db3d",
              "ci/runtime/lifecycle/run-selected-nginx-configtests.py": "d7f394649365631716f6c9077fc02c40091b0ec4d94e72648a58e13d2468062c",
              "ci/runtime/lifecycle/run-selected-nginx-native-operations.py": "97b8609b6aad9c558dfb2d1133331a9aef28d346d8245fc2eb44af31fcf45489",
              "ci/runtime/lifecycle/run-verified-case.py": "534bbd1e5e2cbd21abfe883acc727466c1f16f7e88ae2ca363534f97bbcdb221",
              "ci/runtime/lifecycle/run-verified-report-run.py": "9e39fed4c6210cfb6ccdd0f7f982aebdb50ffd056ae4486886bfc573c75e9211",
              "ci/runtime/lifecycle/run-with-crs-no-mrts.sh": "34ffabcd66507c7abc05950ce7c4719680dafc1da99665ed0a7a31d0519ad160",
              "ci/runtime/lifecycle/sanitize-full-lifecycle-log.py": "a64ea3251e076db075fc4693d0edc7f24de8d0ac4356a8ae9f8b3a849e5d1cfc",
              "ci/runtime/lifecycle/stage-traefik-runtime-artifacts.py": "52b790c6c56c5b1bd37ea9528fa4bc1768ba0edc7f61252cba85c849ca8b7cc3",
              "ci/runtime/lifecycle/summarize-with-crs-no-mrts-workflow.py": "4a20bcf3b17c4c57cc9a77351cffd8e2e22c5de35b9aade5739aa5ca7cbc040e",
              "ci/runtime/lifecycle/trusted_lighttpd_runtime_supervisor.py": "cc74f460fa8a7704ccd95c1d0b9c0d5157d7ed7e3b026fd5158e0485ef5df208",
              "ci/runtime/lifecycle/with-crs-no-mrts-profile.py": "2da241985aa2be3be6ca8557b46d7ef7287e924d4e4be87d6f6a3751fd419bdb",
              "ci/runtime/lifecycle/with-private-sockets.py": "e426b95376db97b98df3e455482e39780078d50ae9d563994e3da04b0b9472eb",
              "ci/runtime/lifecycle/write-engine-lifecycle-artifacts.py": "4ee3e0fa57ec5c9e7a16d9d17c82d535d6f09a44a805106faf86097de1d0fdf7",
              "ci/runtime/lifecycle/write-first-byte-host-metadata.py": "68673de809f4437a5c38ddbda4c7fa6e936c82a7b5389982471e5a3b71af0377",
              "ci/runtime/lifecycle/write-first-byte-source-results.py": "360e0606a76c0eba8b0c331e897e86492801bdf0321a89d3460ee4ca000b0cdc",
              "ci/runtime/lifecycle/write-hostruntime-record.py": "053385a6f95e15006dc0fd0608cdb5128c5aba4ab13b8d83d4306e1d269e9027",
              "ci/runtime/lifecycle/write-nginx-functional-a-evidence.py": "4f12aea27f5354164bca673665b567f135427753bae1c41c7fbcf2c55a2a017f",
              "ci/runtime/lifecycle/write-transport-lifecycle-artifacts.py": "46ca6319e819e76a660ca0513f5273405690015a471cfdd34123e3e4224a8195",
              "common/README.de.md": "5cf445954bc4071ed103471d4f2d562d91225972181f1f5715e04a56b09427ef",
              "common/README.md": "2e7e7fd6070d544ab003107aadc19bd98c223d1bad18c6cec9fa8153fb13f35e",
              "common/docs/design.de.md": "30e5ebf761f8f35cf0f086ceebe6017ff361434fd73899f7ebe593ade9b32920",
              "common/docs/design.md": "af3a6fc164e94a1d0802369b0f00f8a33a4a8c395dae582bdf31b3b2dc0df58d",
              "common/docs/transaction-phase-contract.de.md": "b50d175ef2417dee0a5185605a2159fb42b4f91c2935b3e5276bbc9fd85cb858",
              "common/docs/transaction-phase-contract.md": "aaeed679658ce63698687e1f8d1257be2bce1373917046877bccbe0413077291",
              "common/include/msconnector/adapter.h": "ecaff425e0dae033614a7dc6f143d4c9308a36b8f0f26d15fe87614152f7fbd9",
              "common/include/msconnector/adapter_contract.h": "01e08a1e8cdafcd77a534073d133b48a661295e24c3dfdc966977200797417be",
              "common/include/msconnector/adapter_metadata.h": "5644007681e90c19e6191e88c5398f23d591135413d559a7895477e6c8ca7c63",
              "common/include/msconnector/artifact_layout.h": "a12ea7e38f203fb4ffe0f0b83d63a518a4e3ede2aae2ae69487dec0b3398690f",
              "common/include/msconnector/artifacts.h": "75e3f0b94a4c08238d94bd9e92c0b0e403dd6d3f193feee998713c5d7489f66b",
              "common/include/msconnector/block_statuses.h": "604a6fd7c172016a9411b2aca8703a18b411a61d6b58e52a021ab9114c988f1c",
              "common/include/msconnector/blocking.h": "f400e887a204e38a6ec381e548c3c75e5abc789196aea688081bd9b853a27f82",
              "common/include/msconnector/body_policy.h": "8e7084e4ab112ff6566738ac2a46b4467f8defa1f52c3da113d4b1657f9e7575",
              "common/include/msconnector/build_contract.h": "030c417781f76d7807401022d635e0f0329e44813f6c693676aff74ffc50cb25",
              "common/include/msconnector/capabilities.h": "60997cbd4967d2d0d318ca53cc1af7ad299ee464487404a33064c2f1afce55b4",
              "common/include/msconnector/capabilities.hpp": "af279aadc9bc2fdaf2c69eeb29309d460132bd891f8438429101c72f3cbe6898",
              "common/include/msconnector/capability_matrix.h": "faaaf5496f6ee3db4c9f8e6336f9584b464c4e3b8032a26610d118be2ce9d041",
              "common/include/msconnector/config.h": "3a81652676b81bd97d4d392543db84cb69729c012745fa7f1807eb4319f31d3b",
              "common/include/msconnector/config_parser.h": "dd9f88f70eb20914fb97899de90864b1e56f55cb6710af9cb27fb94847a67231",
              "common/include/msconnector/connector_manifest.h": "84f63cba49eff679194c6e142df179a23c6e15bfecce0308fcbb051dfb1d67ef",
              "common/include/msconnector/crs.h": "cfb1ff7fce3e8f5cdfb63f02002e9dbe9a56197d92914257da77c774845ce1c1",
              "common/include/msconnector/decision.h": "a29c08ee67caa83a3eb146508ed1d6bcc8dc7b27c13cc221a8d074a9b735f722",
              "common/include/msconnector/decision_action.h": "16dc56d9add80ffe51ca987dbda7326e9fb06fea17637c1b87f02b06f94a604e",
              "common/include/msconnector/directive_adapter.h": "2d961c11680bbb49139fb4ec846a28b74e3bc90e1ad4433d6fe547870f97ee9c",
              "common/include/msconnector/directive_spec.h": "4c6eae37390971f41797ae6a1216759e27668b83e4ddbcaaa27a3cd1f3f0e404",
              "common/include/msconnector/directives.h": "d79780a9339de70d7d7746c2918b792fdb3e6ce0dd8a62d29050b8760a142731",
              "common/include/msconnector/dos_guard.h": "2f906760eb2a76ef1aa93d43a2bfc661d317f60d5478209523b3cd90ce3fd297",
              "common/include/msconnector/error.h": "1cc9ca56d2d51eb74056f463abcce951a8079e93b451944c34ac2c97e2914d47",
              "common/include/msconnector/event.h": "acbb5ea952e80f88ce43a6f63d24006f6c6703568ec1dc273a56bced2896a195",
              "common/include/msconnector/event_jsonl.h": "4df864ff98970d8012e29d600bde1b0417c77d3ba9f063fbbadc838b624a6752",
              "common/include/msconnector/event_protocol.h": "2214e119ec6cdca01e1fb5b695495f80823703eec3fa09bc45f905be53a25148",
              "common/include/msconnector/flow_guard.h": "bd16ae73483f19df6cb790bdaf707ecb6467e2ef2a5ce88710fc50519ead161b",
              "common/include/msconnector/generic_mapper.h": "21bc95cb0f637f77210751c65eb912f9936868b4ca1164aa879f6318169309e4",
              "common/include/msconnector/headers.h": "17372f1cec75d33610cd340baa608ba317f6bf6f0f17a562ab5827bc037a3320",
              "common/include/msconnector/http_status.h": "e4f13f7cfae1223aa56673c7c448a25e1a4c6cad78ffa68326d1093d86ad78ed",
              "common/include/msconnector/integrity_event.h": "83a57b7ae647f75b9f05a2614f5b4bb53cd3cb0ee2d097b33d586734c73ed15c",
              "common/include/msconnector/intervention.h": "7cd3f5af2141bd8221205f5f51acdae9df159e83e52f5ee729153ef24f4ee19a",
              "common/include/msconnector/intervention.hpp": "5ef289fc59d723ff1115a33298689ab17d97511b697e79c6bdb890bf16c64334",
              "common/include/msconnector/json_escape.h": "97a2335e648a751cffea08aefd78c40ae114373ff31a7c0d85a419af582c7cf7",
              "common/include/msconnector/late_intervention.h": "c0fccf1a18483d85ce1c50d1cbacde54f3800e554bda0dc2483cfacdbd0ad266",
              "common/include/msconnector/lifecycle_status.h": "a6da04c7e7a69ebbdf88aedeb41b3d525701092b99a3ec5dc5930e086c76a841",
              "common/include/msconnector/limits.h": "c50c6f87869719366226624efabc1feb5452f3a3511d58a7c3eab425cacea3d0",
              "common/include/msconnector/log_sanitize.h": "7de8322a5fdf114edfc8b00bdb2eaed8c62a6bd2ce8f6f870e8400918510532e",
              "common/include/msconnector/logging.h": "c068c9f4dd19cd8410ea760b145dac979933dab3d48fffd89f5cb9abcd49b62e",
              "common/include/msconnector/logging.hpp": "6bdb2d4ad3df381112d10ae8c0162c7d1941045ad6fd6ac420e25e051bd643e5",
              "common/include/msconnector/memory.h": "8e12e78b3fcf31d36d42dae1e3aba069906b8ea10c52e4f84b909b423cf76c1f",
              "common/include/msconnector/modsecurity_engine.h": "e5de4580184c72d54844d724aca55e180db2ec3c2200a2fb78fdd5f383f4f304",
              "common/include/msconnector/native_result.h": "a16c7f5d3661416aa95aed0b5856b2d71728b917b9480f4bb3e0781abb2327bc",
              "common/include/msconnector/options.h": "1dbb1807ab8cb90150be605d57371ecccabfed1ba142c2abcd0ec0dedb1e1301",
              "common/include/msconnector/origin.h": "be8e938fd1f72a6a0c7905347d1c7020ba93c60dad41b171d8be52d2f5c9b88b",
              "common/include/msconnector/origin.hpp": "de70d4483295980612b3e3d894c1abbc979d87939affcc15d6bce266d9a32c0a",
              "common/include/msconnector/origin_governance.h": "7e87ee19f3afaf6be288d0679c39b7539b6740fadd588fee433069ac6a92036b",
              "common/include/msconnector/path_policy.h": "019e24186f9fa9ce692a127ce3e34df37d629f26db24a4c3152e9baf92be4a3c",
              "common/include/msconnector/phase.h": "c3097da8b1d1cf6480a7a7ceb3d97301da06668a082c40e550dd2e79f7149c37",
              "common/include/msconnector/redaction.h": "e3a1c203c8b2be9a4bee476e50c3764a6eee64715baf4de5ee0ec999ea394880",
              "common/include/msconnector/request.h": "f4508228e6964f1620d9e98dc4d7137cc1c575d3b36d862803b773c1056d3e90",
              "common/include/msconnector/request.hpp": "0991512a4ff9116d2d51586777bd770de92a5640bce1fa6dab5d3513718ebf03",
              "common/include/msconnector/request_helpers.h": "de3194debde952645cc27b71b7c82952c0eaa760f38070e5a93439af6ae1f75b",
              "common/include/msconnector/request_mapper_contract.h": "71714b2f289225992cd07d2da8c810618f89a97fa949772006a7345752659440",
              "common/include/msconnector/resource_limits.h": "9daa3c67ea6808f5ce0f0c9381e287ad045aed1668a9e3b1ab41d354c017019c",
              "common/include/msconnector/response.h": "4ef1a7b000097edeeae920904c0deaa88be4dfac9a85ad18c2a8e829cdbf3d55",
              "common/include/msconnector/response.hpp": "dabc8933fc38759c72fa4fa052f05fc2357064c79089160cc54a13bfee56590f",
              "common/include/msconnector/response_helpers.h": "dddb5bb998ac2b447ab8e9db10cd5ba83c8b53ab205ca90e52fe3bce2342e143",
              "common/include/msconnector/response_mapper_contract.h": "bcfb70b93384f711cf751af3a84ab835f079bec0f9c5fba3a22725ef04f9b6e8",
              "common/include/msconnector/rule_error.h": "af251cb2686a0fffe92446d3ac428bea1076e2afa6a559e44f272e37e64110d6",
              "common/include/msconnector/rule_event.h": "bde25165fd2967d26646a2abb35c62947100d9f7d2f2fb43801ccd3ffaa9ce52",
              "common/include/msconnector/rule_id.h": "a00c7a1dd97cee368af7e30df043ebb150756edc98766471d65b73e3ab25c94d",
              "common/include/msconnector/rule_load_stats.h": "12c501883a5c1798fea3d3064c0f7e3a8c29c31552aef40a11035f245d6b06ea",
              "common/include/msconnector/rule_loader.h": "a9529a7c0189207613b04b0d329dcb0ce9402b692363a7ccff20a400d783771d",
              "common/include/msconnector/rule_merge.h": "e8ca8cae33fb824940667b19ff7abeff5edd02ece64e96397e9d96cd5ef26310",
              "common/include/msconnector/runtime_paths.h": "f0368755817351ec8fd6278e7f539a6053ab9c2de0c4ef6d73e2873e713b5d42",
              "common/include/msconnector/runtime_report.h": "38413741b9cea29cde986c169a86ba9e11675b51f9896784141c90ff3c37af0f",
              "common/include/msconnector/status.h": "47943b4baa61990f8bfa1a2e0a6f82d2a3a159145b4fc85a9702c347cb4ef256",
              "common/include/msconnector/status.hpp": "aae1d9eb582ebbd029b9faf256e7b389c722e35243d5a864f3e3d3e51740efe3",
              "common/include/msconnector/test_result.h": "208132abcbfb4d1cb228dbf895ba42e6cf73911cde004d675947e4f2b80e9807",
              "common/include/msconnector/test_result_json.h": "62b7931ff4eac1cf867943689aefac7d52bf2dea4e1cf1781467608120d9490f",
              "common/include/msconnector/transaction.h": "4a9af32abd6458c6be9e339ccba2f5ecc15cc0c782ccad9a402df0e4f363b76d",
              "common/include/msconnector/transaction.hpp": "739489f2b452da87390702e11cab3d9e11a09dfd2dbfabdaa0020964d4979d86",
              "common/include/msconnector/transaction_contract.h": "803cc283e89740f980bcfa98b46907302ed8e30502d0b9168ddecf41193ab8fe",
              "common/include/msconnector/transaction_id.h": "ecede908d5127bf8032ce4180d19b2b229b2b405e94d178f4142e463068b8eb0",
              "common/include/msconnector/transaction_state.h": "00a455c2d1523c1ab6cfd027f9fb2a9f85be2fecdbaaf2d62f039c7532104547",
              "common/rules/modsecurity_p1_p4_vectors.conf": "00ac195a80131405971f278c4eb87c9d125388d140476c1297915e6bbac02973",
              "common/rules/modsecurity_request_body_smoke.conf": "91d66822bec2a6f4abf30ede91b7f494f28235c5bc729936b6a0dd36c28af13d",
              "common/rules/modsecurity_response_companion_smoke.conf": "7aa57b053e725ec567c799eda73db7f071e601ab5a5ce0839d8c30e47f6b0b8c",
              "common/rules/modsecurity_targeted_smoke.conf": "f97e14ab1e1b739b2fc4abf3959c51ae9d76c53550d86b2162f3fccb71e0730e",
              "common/rules/p1_p4_traffic_vectors.json": "6298353b8725ef69ea740bddefdfde0ab704d9c2719c62bd702e8fa4673cbe05",
              "common/runtime/http_authorization_service.c": "7f1544f1f36042c68359c7caed7d5dc4ce8cc77d44282debdc3955ea725a5e9c",
              "common/runtime/http_authorization_service.h": "1c5996cca00ee2b89673a5157f598dc2ce06203f91941b9f44cc019e063de64a",
              "common/runtime/msconnector_runtime.c": "0fa85f5658be96a25204adf489b2e18149a5f826b5ed528e55ec7b2ffe410aa4",
              "common/runtime/msconnector_runtime.h": "202ac41d732d8ac5c1fec266bd7b49ae4cec1e0f5727c3c0d38832c6d58ceb3b",
              "common/runtime/response_companion_client.c": "8534bbde095b46507c7f4ad109c521fb8c9c03c76c43daa391fe1c44cdfbbc60",
              "common/runtime/response_companion_client.h": "581ff79c969225ebb768d9a2477f83716ee97a61f20ae6fbeee0c442ae7bc7a4",
              "common/runtime/response_companion_protocol.h": "634529f2801423b411b303e408f9735f4e1123294c4cba6dde79957ebb594188",
              "common/runtime/response_companion_transport.c": "268e522789b77af2d4942d6b5981c7ce582a4fad03a2822b79c26f1065e8ffc4",
              "common/runtime/response_companion_transport.h": "606e8a7c9d7ce1772cab3a638de7e48e3e025949be3bb0237fb658cb84989e8f",
              "common/scripts/modsecurity_targeted_eval.cc": "f0def448dba5107735c75262ae7568aec1fd2a6de18355902120c0d74b0afb18",
              "common/scripts/run_blocked_runtime_smoke.sh": "9308998ad3d2cba6b28709b373d2719a655dc77d32be71481ef41f8cf7028ca4",
              "common/scripts/run_local_runtime_smoke.py": "f06c33fc6f9084a4a36218153de944f523f42d5c0cc89469f9244efaa02b87dd",
              "common/scripts/write_smoke_result.py": "35d2d86164672dfbe0fc2c648e41ba03df38ad9a335cd655995d650f769cda77",
              "common/src/README.de.md": "760a994ec35908128f9a6beb68733d07af17d8d59de7061f06757a9042afaab7",
              "common/src/README.md": "7a7c5b9ddd534d333a3a212fd25602f0c84499d73822349f8cf97e7f9573b778",
              "common/src/adapter.c": "516e776a748c5a586089f429827215782cdb71b759b82bd7eec724cd5de1555c",
              "common/src/adapter_contract.c": "61c07a434ac5ffb3bb30ae0b50a146f5cbe783f69842a384f76e049e3fc124fb",
              "common/src/adapter_metadata.c": "56d5890cff7c152297688d00d994f6945c00397303d5f459cb9dfa7805eaeefb",
              "common/src/artifact_layout.c": "6468d87635446a35035a5aa2569d3b2341fc55a35e4ee2f27a3e32648455e453",
              "common/src/artifacts.c": "04859ebe04ffaedf894bdfe3e06cde921b8e527588b5ac53dca45f950fd4ed00",
              "common/src/block_statuses.c": "ea691e18cfb3ab2733b878f41cd802332b60d8eb9c8f3f56548c37495de736bf",
              "common/src/blocking.c": "4f2776c88c7b95ebc7c3adfdb12e147dad002594dd3f95e6a38051c615717460",
              "common/src/body_policy.c": "735027686a02d2e867e00bbd9d7eafc445c1f343eac1ec93b4289d4d4813cdb5",
              "common/src/build_contract.c": "792123920f333f0dc3505125df2d194b2319cffd3fb3d9adc5ef877a960497d0",
              "common/src/capabilities.c": "801d8f0d58c70a987104098fcb4e04d147d4ccd1dccc14e9accd6253efff6e3b",
              "common/src/capability_matrix.c": "fa01a76c4b0f4184b25710da06823ded6c0a38700b539864c892c717f7f0f277",
              "common/src/config.c": "3e5f6c0130b0c1f79a540444a96bb051596e6072843888f7b5aad8ae61560c27",
              "common/src/config_parser.c": "8dca03ec371a52681d1721bf76e8b4098599bf654755b7f489191cb5290168b6",
              "common/src/connector_manifest.c": "4a9e5456b6fd8c20dcd0eeff8ca3048cfdc7577f8da4ffa71a918c309e367f75",
              "common/src/crs.c": "d0a394d9e29df1bf80c4b7276bbd3bd7b12192d275856117d82615a9946263ef",
              "common/src/decision.c": "e42a17aa86541ecf573b336d049f57014a1a1a8e257613491a9d5e05cb44d174",
              "common/src/decision_action.c": "7c75f3b45f661300d8cdb328dec57ef4f403ba0ed0fa3fc8400d9aa55481b9a2",
              "common/src/directive_adapter.c": "402bd6fe396f774df3e990849882bcdce5d2e52abcb7973c4a8e0a6da4835263",
              "common/src/directive_spec.c": "8c75a3e97f781965ed023df99cc11adc0013e78f4bdaec0c9e26c664823b43ef",
              "common/src/dos_guard.c": "bfc304695a6801a5ab1256f9703429a506f80519fef15a7f9e6a271c004e17d7",
              "common/src/error.c": "4509eb4b33820c2ca6300b314f88c99e06d8a5e6361900783b8f7aafcee33f86",
              "common/src/event.c": "0032e25cac8dd310eee620f606f598db830a84898baf26575cfee19b03166e03",
              "common/src/event_jsonl.c": "dc3a21fa47075fe96f19d7b12c8015db7a8d2b407d65a678ab0f1487de1ddcef",
              "common/src/flow_guard.c": "8e43183bf42ace059c16ef7984fe5b835a822cd2b439f73f17cb96261ed7dc72",
              "common/src/generic_mapper.c": "ceacbb368c5bd35212a9a613b63b01b9e71158dd1aed3a6e0905febdee0ed850",
              "common/src/header_validation_internal.h": "b9ca7130e184913c10b3b24cfae18415eef411a908b1af5f926af6b695ed11e7",
              "common/src/headers.c": "1bc8351188daf20a9b8f0db47f73ec5a64afedef59776b56206b35f43666bc12",
              "common/src/http_status.c": "b6ad0c69ae47150170919096eaf7b444a097b0e8b88d25b0b7be13bbe9777a69",
              "common/src/integrity_event.c": "c2ad7f26cf051321e269f50d0e8afb9f3aa5a8a3a416f55e63e1278392753041",
              "common/src/intervention.c": "91c7fbd9cf158a2e46c59af2b534f0b77dae2cee84fff038509c129b471db4a2",
              "common/src/json_escape.c": "d9d8e7e1cfc6ad5e82e227044f5c8ebbbb8489f13caab99a8e3f02cf5d279e0b",
              "common/src/late_intervention.c": "aa29b1ad82f176320fdadbf2357ee616cc7ca1ff6966063911a4eb2c5cacc812",
              "common/src/lifecycle_status.c": "3dab0f986e7ed1959bb5d1425c666061bad6816dc8262c27a64e3ba49ff1c971",
              "common/src/limits.c": "3282ce8e7143a7d481e831cf02ec9d08729dd2f7c0015bccfdf336a409767aa0",
              "common/src/log_sanitize.c": "9fc0b1e53225fc95f3a43ec7ff0df4d2f0eb4bb363eee19ca3e693e0a958a943",
              "common/src/memory.c": "f38f868c0355a3722c027a477f0bd762f6c1a9a08a12c5c7b814aeec58cbe9af",
              "common/src/modsecurity_engine.c": "a77b04c3e2deaf5146e0e164efb56f32dc76eebab9e3eccc6604f0e9483fedd1",
              "common/src/origin.c": "559ec9880e83cd386f5986cfc155ea3dd8edfa7f379a39ebca7839f0cdbc7130",
              "common/src/origin_governance.c": "313e09a5b2865315a932d7243d9e5eee85b9a1c4dfb4276e60fb5c2d3fab32b2",
              "common/src/path_policy.c": "790146307f4600359ef3d6d573e6fc1b674b9b8e796ddfa67579f2d4b2086802",
              "common/src/redaction.c": "e7b74654e806615ee61569e8c6424be01bfeea61448cfebbb8c1be7f26c16c6f",
              "common/src/request_helpers.c": "f3c3d4ddd6693bc330a3ec24a1d1491af64ac2544a26696cf010babd1a4ce790",
              "common/src/request_mapper_contract.c": "df427fc2e28a4a94cf252470654a46453335cf361919f229c0f328d54f9a746a",
              "common/src/resource_limits.c": "0affa0f5ad598aa94dc6ce8b480c178adcf7b2be4b9a12f9fed6ee82a17c0767",
              "common/src/response_helpers.c": "d24c987d55e2b362035d04dda5a81889026aafdad9d1a1541c741cba9ed19cda",
              "common/src/response_mapper_contract.c": "e7d71677bbc94f21268502cb64163038d17bdad8307049df66ad07b2597574dd",
              "common/src/rule_error.c": "0e6e1756e43fc946bec2c2ee090681d6398339da240121595e891aaf76e90735",
              "common/src/rule_event.c": "18676a24a88c33a7f991b777d96d151ba364541153b6265498a6be6cb5b54387",
              "common/src/rule_id.c": "6cf8cc24a6de62e74376edf73bd589b3f4c26f66dc0a53ae92b626d5ac70435b",
              "common/src/rule_loader.c": "e837121b19b1239e2667cc97b5c3279066f36c20b63afd2ca1e6c544407a4e56",
              "common/src/rule_merge.c": "db7b8097adaffa612d19ccf23253b2e583db161904fa1b9a9e3ee37e48330b15",
              "common/src/runtime_paths.c": "168de23208e3b00647caf543307bec0e3029db5ac78e18e3c8e1be23e4340b07",
              "common/src/runtime_report.c": "e7e61cf66cc7c64adeda7449b480a96b49f1b0efa758c5b8fe3536db6720a30e",
              "common/src/status.c": "8cae41d98f3ee4f8978e01100c59b2882a078e683fae38c42839d3bf3566ccca",
              "common/src/test_result.c": "997b5f047b7d3fd77e457135945961314fc64e21beb636685761dde85bbed86a",
              "common/src/test_result_json.c": "d904738d35db3579b6cd4ea3b12ff14caabd0090754fb30bb1da8f7072cc1c78",
              "common/src/transaction.c": "b6f621703ef7238295eb49257666e6d6a4249333bf4ae939d1fbab9a06712bdf",
              "common/src/transaction_id.c": "64630d1671bf58fec7f208aa43b957da915d9f2cbcd65a1ffba2ab06c741beaa",
              "common/src/transaction_state.c": "b4f35347531cc380f8bf71c3c7192ddb46442974a14374d332037373b6ffe860",
              "connectors/envoy/ext_proc/README.de.md": "379168c919b0583350f44bb0048b0aecb9d5b7f3ae154e516254b4c0be581cf6",
              "connectors/envoy/ext_proc/README.md": "84eee6a0c2e813b8cf737006853780c70253d6030959442b98716c087eddae7b",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_common.go": "019d7149165a5f1709d1dc4228581e6aba64c453654d70a7c541a6400602ac09",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_passthrough.go": "e8ca083f672809f0ad410f49b3c91df735415cd92ff5ea021e196664a216729f",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_passthrough_test.go": "9d9c571342716ce1303a531f26e6b8f28632e07fe89e8c23ff73bec5cada1707",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/main.go": "c07f99755bb1a1fbad95fc2f70941937a4a517bcfbf19865c8ddef8d64dbe1d0",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/main_test.go": "6fcafd2256758062d620e4c8633b31fbea3cca7793363e29dba8b97e41a95954",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/observer.go": "d86e8a45d3329a04317d9447d4f1e2efeea8146053bbbb3d6285341fee3e9ec4",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/observer_test.go": "c26b6281069fb364fef756d6b496ccc8d3ad837ff17775126e493d7a367ba9f9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/engine_common.go": "2442966b3c81b188be15753a0c9829b43299ee747eae5b9b86054ce9a9eb1758",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/engine_passthrough.go": "5447b3e4ac36aca83e7567d9ac602283f923c9e7e5a155f9fc88fccedacb3c65",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go": "d356dcbf1007e62d7b973c9bdc055015b64bab060d558162b3e96771dc664d52",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main_test.go": "5c1840c4d051031d36b1ccd86f95c6cfc06142ba476122bdbfe697b6f3db3848",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main.go": "8ef1046f9549b46a1fa88bf399696f263e7c2faee107e52c0c4a30ced6f41db9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main_test.go": "5ec9223b304dd63932d05cc6a51839a6fd9d59598d178b2afd177134da3520d9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/peercred_test.go": "44991db7bd1bf9c0c8262c9c97b9be6bcf6130c20a74b42deda7894cb6ff9ac5",
              "connectors/envoy/ext_proc/go.mod": "9a52853f5e3839f500655c1d6cc8785b7cd379da55fe8e9a6374ac8ff0ece7c6",
              "connectors/envoy/ext_proc/go.sum": "66100e55eddccb812d04e1b841a7721c25cbab30b0cd5e690242368b7d2f5963",
              "connectors/envoy/ext_proc/internal/composite/coordinator.go": "507b4b2117a1b6582b0e0eacc8a4723b466bedf26b4b8d0752dc2ba3d8f3f9fe",
              "connectors/envoy/ext_proc/internal/composite/coordinator_test.go": "cc8c9b2c37a896b4e03177d073e6a8074896f663f4cbc77475856b2de6f69ab4",
              "connectors/envoy/ext_proc/internal/composite/i12_envoy_observer_test.go": "7a12e7dc914899a337b42defbebb793d1fb96757e170d4a8bbfb4a95a5d7e07c",
              "connectors/envoy/ext_proc/internal/compositeenvoy/common_body_completeness_test.go": "a2559bba9226e56b312b111b33aea7651c6160b8064e9d78fd000d941cf79992",
              "connectors/envoy/ext_proc/internal/compositeenvoy/common_runtime_integration_test.go": "8ae2100dfbfa6b64bc0b1b4b04765272e62ec261db3127a1342a053f9aa33bf9",
              "connectors/envoy/ext_proc/internal/compositeenvoy/server.go": "028e1e21cf1e1313cee0e951b82fd8fcb9c492bbf1dd63401455585d01c6db4a",
              "connectors/envoy/ext_proc/internal/compositeenvoy/server_test.go": "595be39d20afa24ab6fa4e747d5b397d0c1948b61bb6e5272f24cf3720e6a5d0",
              "connectors/envoy/ext_proc/internal/compositeenvoy/technical_error_test.go": "6cfbc98bad68ab30fffa836db5c47a60a9312b9864f0251eed1667c711eb0055",
              "connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go": "7f7a2776032b702a101222ef38db60d012f263aedac9fa67a721613e5c606e2d",
              "connectors/envoy/ext_proc/internal/compositetraefik/forwardauth_test.go": "01e82e24837612a493e9d48469a4440ace95fd79b9f7e55c10e767381a99678b",
              "connectors/envoy/ext_proc/internal/compositetraefik/uds.go": "07202ce16684e08d3ab4b46f0c3385a50491b4c6a59d6028bd5e29cccec2151b",
              "connectors/envoy/ext_proc/internal/compositetraefik/uds_test.go": "aa0215397c66b8d33ab6c5b65883a2bfaffbc154031ffde0e596f55c6a78fef8",
              "connectors/envoy/ext_proc/internal/processor/body_limit_host_action_test.go": "1ac63d7c8ecfbff3481a03be9f536124069e6dda043ed308afaff9877d729e4e",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c": "6449bd0d2cb2a71676d09bf6f8d464bfa1d68f0dbab73f61887c028fedd8ccec",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.h": "c06ab9f8ef468f241186232caf47fafc5cf12eef2d76b57cd016825573520783",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_commit_test.go": "3811b81a35710cda0723c6451032c0a2e7008f8b360bb93aa38077c2355be25c",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go": "3df8f38891d9a9ee0053ac5beba6615cdce5772661af8cffe8c0c62506daa1d8",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go": "7e9a89cb1e233dcbc23c740a8636786c4bd65f57aa6fae6efe07f2aacbcac455",
              "connectors/envoy/ext_proc/internal/processor/config.go": "321b16b82919ec43b0f12dc59b5de55058496930e1a4cfcea8a51d7c55da8851",
              "connectors/envoy/ext_proc/internal/processor/config_test.go": "4140137ebcefd1e04da6cb728d8a2284640142f68a5464b39f50e61c27c04dec",
              "connectors/envoy/ext_proc/internal/processor/i12_envoy_observer_test.go": "433b6d3ece97401bb7f910d8b29860f8ece7931e88be7f1155082f68b8942130",
              "connectors/envoy/ext_proc/internal/processor/jsonl.go": "1ff55bf56bfb02f594cc8f2a09b7efa128f106d404c32568716845add50117d6",
              "connectors/envoy/ext_proc/internal/processor/jsonl_test.go": "c784a60e1ede32bc40ce3df11a1b16ec5850f75f74432a905a45567222fdca8a",
              "connectors/envoy/ext_proc/internal/processor/phase4_budget_test.go": "6f8ff027396578421764374d5e88a0e29e52a547e651f6cda5b5211bd3f9f064",
              "connectors/envoy/ext_proc/internal/processor/processor.go": "6c8461d73cd43b2a789ca69a2477c0e1f2440b3346bd27ad9bccc469d48b1762",
              "connectors/envoy/ext_proc/internal/processor/processor_test.go": "3848137c942fab9593ee227a2c73494cc262b4867ebadc014ba35b90f73af449",
              "connectors/envoy/ext_proc/internal/processor/technical_error_test.go": "3653bd940540c94ee799f50c2b09556cc7027b131cf4d1929c61f8051e7890cd",
              "connectors/envoy/ext_proc/internal/responseobserver/client.go": "8869025eec2ad73e330291c96d2812bb52ff6f79b14d5fef6c195661070b3473",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_linux.go": "77238e197fec60ec668ceeafde35d27a577da4e8d6ff3f48b3a742d4d7cbbaf6",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_linux_test.go": "de350e573b0d62f5ea31a76a318226217092f69ac653505d87d6376a14621e7f",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_other.go": "74349b4b04faadbfbf3d40644474700543120f5539e445202ae25176f1c5b36a",
              "connectors/envoy/ext_proc/internal/responseobserver/protocol.go": "f497571a69479edbc68094594e6d75f6633d238662e42be6640412d9d04ce0cb",
              "connectors/envoy/ext_proc/internal/responseobserver/protocol_test.go": "a6c489c75f18ca8062b43455c6c7d533738b05ef2249f13f4004a29a77b15537",
              "connectors/envoy/ext_proc/internal/responseobserver/service.go": "6e96afed63fd7343e9bc1188950b38d23371f08063c50dba4f276eda2d74c633"
            }
          },
          "case": "I12::envoy-ext-authz-request::NEED-request-eos-once",
          "delivery_scoped_verified": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
          "delivery_source_baseline": "02754040bced960cfc1857416cd7101bb3116ef4",
          "engine_sha256": "719a9ddd277e9b04482d55684266a96989b384e37789df6d8482549a46e7fcc8",
          "fixture_configuration": {
            "/mnt/fixtures/native.rules": "8e271f02c84fb6aa0671fb8f2b18144903da6b33764a5f676eac11dcb51de42d",
            "/mnt/fixtures/shape.json": "cc7d18304897199c27bbd081b1dfb944ff5bcf9976993beb96ce5ca1a6ca222c",
            "/task/runtime/envoy.yaml": "cc78f9be754480a54340275ff9fb0963b511e4bb63b08593fbefac28a31d45b3",
            "/task/runtime/loopback.crt": "cf78894309f99745e67d2867fbbaf5a901d90c140b6cedfeef57b3dcd652bd6e",
            "/task/runtime/loopback.key": "b60c52142d0ff3cfaa6d3cb8cd83762a298777f61505953dad3dadd5091d368f",
            "/task/runtime/native.conf": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb"
          },
          "host_sha256": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
          "product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
          "rules_original_sha256": "8e271f02c84fb6aa0671fb8f2b18144903da6b33764a5f676eac11dcb51de42d",
          "run": "envoy-i12-env-request-fb9cdd12",
          "runtime_backend_profile_actual_source": "envoy-ext-proc Common runtime backend reused by actual composite adapters",
          "source_git_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness and declared private overlays",
          "source_scope_count": 167,
          "wrap_symbols": [
            "msconnector_transaction_contract_init",
            "msconnector_transaction_contract_finish",
            "msconnector_transaction_contract_cleanup",
            "msconnector_transaction_contract_complete_phase",
            "msconnector_transaction_contract_set_response_committed",
            "msconnector_transaction_contract_record_response_metadata",
            "msc_new_transaction",
            "msc_new_transaction_with_id",
            "msc_transaction_cleanup",
            "msc_process_request_body",
            "msc_process_response_body",
            "msc_process_logging",
            "msc_append_request_body",
            "msc_append_response_body",
            "msc_process_request_headers",
            "msc_process_response_headers",
            "msc_intervention",
            "msconnector_runtime_transaction_begin",
            "msconnector_runtime_transaction_begin_request_stream",
            "msconnector_runtime_transaction_append_request_body_chunk",
            "msconnector_runtime_transaction_finish_request_body",
            "msconnector_runtime_transaction_process_response_headers",
            "msconnector_runtime_transaction_append_response_body_chunk",
            "msconnector_runtime_transaction_finish_response_body",
            "msconnector_runtime_transaction_finish",
            "msconnector_runtime_transaction_destroy",
            "msconnector_runtime_transaction_finalize_and_snapshot",
            "msconnector_runtime_response_companion_handoff_with_handle",
            "msconnector_runtime_response_companion_claim_handle",
            "msconnector_runtime_response_companion_revoke_handle",
            "msconnector_runtime_response_companion_session_process_response_headers",
            "msconnector_runtime_response_companion_session_append_response_body_chunk",
            "msconnector_runtime_response_companion_session_finish_response_body",
            "msconnector_runtime_response_companion_session_set_response_commit_state",
            "msconnector_runtime_response_companion_session_record_host_action",
            "msconnector_runtime_response_companion_session_fail",
            "msconnector_runtime_response_companion_session_cancel",
            "msconnector_runtime_response_companion_session_release"
          ]
        },
        "actual_scoped_baseline_inputs": 167,
        "delivery_scope_verified": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
        "git_source_base": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness and declared private overlays",
        "native_config_sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb",
        "product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "rules_sha256": "8e271f02c84fb6aa0671fb8f2b18144903da6b33764a5f676eac11dcb51de42d"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "8e271f02c84fb6aa0671fb8f2b18144903da6b33764a5f676eac11dcb51de42d",
    "run_id": "envoy-i12-env-request-fb9cdd12"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 344751,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-envoy-request-01.json",
    "sha256": "0170accf177dc79bf4da15d48e9502b16c4080fb0147a79dbba8391b0edcc2e1"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::envoy-ext-authz-response-companion::NEED-lease-claim

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 160719,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/native-lifecycle.jsonl",
          "role": "cleanup_observer",
          "sha256": "03bd7a2f511dbf0c01cdf3816874871a8bd1a28318847b998caf2e69df8a5370"
        },
        {
          "bytes": 1886,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/result.json",
          "role": "cleanup_observer",
          "sha256": "5c95f23eafcbaa4abf453ab755c2eb1c5e5372a6b740f7c1a7642f5ef06aa8ff"
        },
        {
          "bytes": 4568,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "5a76af51698adf5fd59bde25e9ee238c25338dbd2b7dcd7ab9c2c987d3ce6c44"
        }
      ],
      "value": {
        "Go_C_atexit_absent_actual_snapshot_used": true,
        "actual_collector_snapshot_after_real_engine_close": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
          "contract_state": null,
          "edge": "snapshot",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 107759999951482,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 266,
          "profile": "envoy-ext-authz-response-companion",
          "result": null,
          "run": "envoy-i12-env-companion-b99d9ec5",
          "runtime_eos_handoff": null,
          "runtime_finalize_snapshot": null,
          "schema": "native-lifecycle-v1",
          "sequence": 142,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792017393789356927,
          "wall_sample_end_monotonic_ns": 107759999951607
        },
        "actual_runtime_destroy_return": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 66,
            "canonical_transaction_id": null,
            "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 107755174765858,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 266,
            "profile": "envoy-ext-authz-response-companion",
            "result": null,
            "run": "envoy-i12-env-companion-b99d9ec5",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 71,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792017388964171329,
            "wall_sample_end_monotonic_ns": 107755174765978
          }
        ],
        "driver_actual_waited_process_exits": {
          "backend": {
            "forced_kill": false,
            "pid": 262,
            "proxy_pid": 261,
            "signal_sent": 15,
            "waited_exit_code": 0
          },
          "engine": {
            "forced_kill": false,
            "pid": 266,
            "proxy_pid": 265,
            "signal_sent": 15,
            "waited_exit_code": 0
          },
          "envoy": {
            "forced_kill": false,
            "pid": 278,
            "proxy_pid": 277,
            "signal_sent": 15,
            "waited_exit_code": 0
          }
        }
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 160719,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "03bd7a2f511dbf0c01cdf3816874871a8bd1a28318847b998caf2e69df8a5370"
        }
      ],
      "value": {
        "actual_common_finish_calls": 2,
        "actual_native_logging_calls": 1,
        "common_finish_idempotent_second_call": true,
        "observed_public_runtime_finish_wrapper_calls": 1
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 6325,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "49bcca6b56e81fba01ca66e0961adfc6fd91de97f184022401cc705e27daab99"
        }
      ],
      "value": {
        "actual_finite_authz_sample": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": null,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": true,
            "declared_size": 13,
            "grpc_send_error": null,
            "monotonic_ns": 107755156959114,
            "operation": 11,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017388946364458
          }
        ],
        "actual_request_body_input": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107755157050344,
            "operation": 1,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017388946455698
          }
        ],
        "actual_response_body_end_of_stream_input": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107755172683560,
            "operation": 1,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017388962088894
          }
        ],
        "native_raw_host_eos_fields": null,
        "transport_eof_is_separate": true
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 160719,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "03bd7a2f511dbf0c01cdf3816874871a8bd1a28318847b998caf2e69df8a5370"
        },
        {
          "bytes": 6325,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "49bcca6b56e81fba01ca66e0961adfc6fd91de97f184022401cc705e27daab99"
        }
      ],
      "value": {
        "actual_finish_entry_return_callbacks": [
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107755157290961,
            "operation": 3,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017388946696303
          },
          {
            "actual_result": 1,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 13,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107755157524633,
            "operation": 4,
            "pid": 266,
            "response_direction": 0,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017388946929985
          },
          {
            "actual_result": null,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107755172990022,
            "operation": 3,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017388962395361
          },
          {
            "actual_result": 1,
            "allocation_scope_call": 2,
            "body_end_of_stream_argument": true,
            "body_size": 25,
            "companion_claim_succeeded": null,
            "declared_length_known": null,
            "declared_size": null,
            "grpc_send_error": null,
            "monotonic_ns": 107755173643835,
            "operation": 4,
            "pid": 266,
            "response_direction": 1,
            "schema": "i12.envoy.physical-host.v1",
            "wall_ns": 1792017388963049185
          }
        ],
        "actual_nested_runtime_native_finish_spans": [
          {
            "actually_nested_native_returns": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 23,
                "canonical_transaction_id": null,
                "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "v_lZPihoUax6jL_ewk25AOVlR3URq4QJdm2YM9kOUeo",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 107755157405644,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 266,
                "profile": "envoy-ext-authz-response-companion",
                "result": 1,
                "run": "envoy-i12-env-companion-b99d9ec5",
                "runtime_eos_handoff": null,
                "runtime_finalize_snapshot": null,
                "schema": "native-lifecycle-v1",
                "sequence": 24,
                "transaction_id": "v_lZPihoUax6jL_ewk25AOVlR3URq4QJdm2YM9kOUeo",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792017388946811092,
                "wall_sample_end_monotonic_ns": 107755157405739
              }
            ],
            "entry": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 22,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107755157318581,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 266,
              "profile": "envoy-ext-authz-response-companion",
              "result": null,
              "run": "envoy-i12-env-companion-b99d9ec5",
              "runtime_eos_handoff": "request_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 22,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017388946724040,
              "wall_sample_end_monotonic_ns": 107755157318690
            },
            "return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 22,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107755157510323,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 266,
              "profile": "envoy-ext-authz-response-companion",
              "result": 1,
              "run": "envoy-i12-env-companion-b99d9ec5",
              "runtime_eos_handoff": "request_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 29,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017388946915763,
              "wall_sample_end_monotonic_ns": 107755157510412
            }
          },
          {
            "actually_nested_native_returns": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 51,
                "canonical_transaction_id": null,
                "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "v_lZPihoUax6jL_ewk25AOVlR3URq4QJdm2YM9kOUeo",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 107755173511456,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 266,
                "profile": "envoy-ext-authz-response-companion",
                "result": 1,
                "run": "envoy-i12-env-companion-b99d9ec5",
                "runtime_eos_handoff": null,
                "runtime_finalize_snapshot": null,
                "schema": "native-lifecycle-v1",
                "sequence": 52,
                "transaction_id": "v_lZPihoUax6jL_ewk25AOVlR3URq4QJdm2YM9kOUeo",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792017388962916957,
                "wall_sample_end_monotonic_ns": 107755173511604
              }
            ],
            "entry": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 50,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107755173088963,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 266,
              "profile": "envoy-ext-authz-response-companion",
              "result": null,
              "run": "envoy-i12-env-companion-b99d9ec5",
              "runtime_eos_handoff": "response_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 50,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017388962494478,
              "wall_sample_end_monotonic_ns": 107755173089156
            },
            "return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 50,
              "canonical_transaction_id": null,
              "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 107755173628692,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 266,
              "profile": "envoy-ext-authz-response-companion",
              "result": 1,
              "run": "envoy-i12-env-companion-b99d9ec5",
              "runtime_eos_handoff": "response_body_finish",
              "runtime_finalize_snapshot": null,
              "schema": "native-lifecycle-v1",
              "sequence": 57,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792017388963034132,
              "wall_sample_end_monotonic_ns": 107755173628782
            }
          }
        ],
        "raw_argument_eos_and_host_eos_fields_preserved_null": true,
        "selected_official_native_complete_body_contract": "processRequestBody/processResponseBody invoked once only after direct host body EOS; SDK appends have no EOS argument"
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 160719,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "03bd7a2f511dbf0c01cdf3816874871a8bd1a28318847b998caf2e69df8a5370"
        }
      ],
      "value": {
        "actual_common_cleanup_calls": 1,
        "actual_native_cleanup_calls": 1,
        "actual_runtime_destroy_calls": 1
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 3494,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/before-request.json",
          "role": "loaded_image",
          "sha256": "2ed29823eff534332311814bb2c3123ab13dfb811adca1cb2cf4f11f6fd37c75"
        },
        {
          "bytes": 227,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/bootstrap-observation.json",
          "role": "isolation_receipt",
          "sha256": "573cdb4639f8414470a51c5a2c96deaf0e95b57eaa6dd48d95bad5ae74e28b08"
        }
      ],
      "value": {
        "actual_processes": {
          "backend": {
            "executable": "/usr/local/bin/python3.14",
            "executable_sha256": "aa4ec29748e8f5cfd800a83448daa49b3dc384dd9ddaea9823677181238dd1f2",
            "fd_count": 4,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2255900]",
              "2": "pipe:[2255901]",
              "3": "socket:[2253134]"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [],
            "pid": 262,
            "proxy_pid": 261,
            "vanished_during_snapshot": []
          },
          "engine": {
            "executable": "/task/cache/msconnector_composite",
            "executable_sha256": "719a9ddd277e9b04482d55684266a96989b384e37789df6d8482549a46e7fcc8",
            "fd_count": 11,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2252330]",
              "10": "socket:[2254043]",
              "2": "pipe:[2252331]",
              "3": "/task/runtime/native-lifecycle.jsonl",
              "4": "/task/runtime/native-audit.log",
              "5": "anon_inode:[eventpoll]",
              "6": "anon_inode:[eventfd]",
              "7": "/task/runtime/native-debug.log",
              "8": "/task/runtime/adapter-events.jsonl",
              "9": "/task/runtime/common-events.jsonl"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [
              {
                "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
                "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
              }
            ],
            "pid": 266,
            "proxy_pid": 265,
            "vanished_during_snapshot": []
          },
          "envoy": {
            "executable": "/task/cache/envoy",
            "executable_sha256": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
            "fd_count": 25,
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2253140]",
              "10": "pipe:[2252339]",
              "11": "pipe:[2252339]",
              "12": "anon_inode:[eventfd]",
              "13": "/dev/null",
              "14": "socket:[2252340]",
              "15": "/task/runtime/envoy-access.jsonl",
              "16": "socket:[2252350]",
              "17": "anon_inode:[eventpoll]",
              "18": "pipe:[2252351]",
              "19": "pipe:[2252351]",
              "2": "pipe:[2253141]",
              "20": "anon_inode:[eventfd]",
              "21": "anon_inode:[eventpoll]",
              "22": "pipe:[2252354]",
              "23": "pipe:[2252354]",
              "24": "anon_inode:[eventfd]",
              "3": "anon_inode:[eventpoll]",
              "4": "anon_inode:[eventfd]",
              "5": "anon_inode:[eventpoll]",
              "6": "pipe:[2252338]",
              "7": "pipe:[2252338]",
              "8": "anon_inode:[eventfd]",
              "9": "anon_inode:[eventpoll]"
            },
            "identity": {
              "CapBnd": "0000000000000000",
              "CapEff": "0000000000000000",
              "Gid": "65534\t65534\t65534\t65534",
              "NoNewPrivs": "1",
              "Uid": "65534\t65534\t65534\t65534"
            },
            "native_libraries": [],
            "pid": 278,
            "proxy_pid": 277,
            "vanished_during_snapshot": []
          }
        },
        "actual_uid_gid": [
          65534,
          65534
        ],
        "host_version": "/task/cache/envoy  version: b579d07d3ad7ee11d32b105e91a5a39ad24718d7/1.39.1/Clean/RELEASE/BoringSSL",
        "native_who": "ModSecurity v3.0.14 (Linux)"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 40043,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/build-manifest.json",
          "role": "source_manifest",
          "sha256": "d25c3f43d63932152c047037d680c25451bd31c690a63d666ae2c9c99b2bb120"
        },
        {
          "bytes": 54602,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/scoped-product-source-equality.json",
          "role": "source_manifest",
          "sha256": "40ddedbe31c9b7bf55f48b2906f29c2a245ad726a9b4523964e3b2e2f9bc84cb"
        },
        {
          "bytes": 241161,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/source-ledger-v1.json",
          "role": "source_manifest",
          "sha256": "6b4ba0985efbda2f4dded97c5be54933c6d5d2c185b46862e660628d662f49b4"
        },
        {
          "bytes": 399,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/native.conf",
          "role": "effective_configuration",
          "sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb"
        },
        {
          "bytes": 967,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/companion-v2/fixtures/native.rules",
          "role": "effective_configuration",
          "sha256": "b23c5d07aa8bcd39d6f7f208234c62e3866b1132331987264c2325b2a562c789"
        },
        {
          "bytes": 7559,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792017345010229081/data/runtime/envoy.yaml",
          "role": "effective_configuration",
          "sha256": "cc78f9be754480a54340275ff9fb0963b511e4bb63b08593fbefac28a31d45b3"
        }
      ],
      "value": {
        "actual_build": {
          "actual_external_build_provenance": {
            "actual_build_receipt": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/envoy-authz-lifecycle/build-control-07/receipt.json",
            "actual_build_receipt_sha256": "8dcf87861e481f33051d52bc0617052b125f49071620bcaae70be3f83bc6fbc3",
            "actual_host_not_launched": true,
            "binary_hashes": {
              "envoy": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
              "msconnector_composite": "719a9ddd277e9b04482d55684266a96989b384e37789df6d8482549a46e7fcc8",
              "msconnector_envoy_ext_proc": "19f0f7bb1f48edfa86e2567ae107d01ceb7f9fafa6c3d87d0d25d8242ea56b1c"
            },
            "scope": "fresh external actual native build; reused pinned realEnvoyhost binary only",
            "scoped_product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
            "selected_sdk_image_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
            "source_baseline_git": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness + declared private overlays",
            "source_sha256": {
              "ci/runtime/lifecycle/aggregate-five-connector-no-crs.py": "641b11df919f35412de9d287e734f07c8027100cbff596cf54ff0f572a0890f9",
              "ci/runtime/lifecycle/aggregate-five-connector-with-crs-no-mrts.py": "43b22adfe39bed7c1bbd7aa0b2d3b70c6af40850579f4b6d598d7fd07d1ac556",
              "ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py": "af83ee477c71ef9da7e75820615e6dd4c3423b5bab21df585655f85549e98a52",
              "ci/runtime/lifecycle/cases/apache-phase4-response/allow.yaml": "f7a63436fa8b874e5395f3e3bfa9cc89296eb0693622a0fcfcd4f8509ec69315",
              "ci/runtime/lifecycle/cases/apache-phase4-response/custom-mime-deny.yaml": "86103d9de76ada3a496cc32b19cb58cb78fbdc6b02a2154dc960d555be701168",
              "ci/runtime/lifecycle/cases/apache-phase4-response/empty-allow.yaml": "9f164c02f5a95f4f22d7d8c6be467ab4e5c923c79008cb0388d9dcb68c6b407a",
              "ci/runtime/lifecycle/cases/apache-phase4-response/empty-deny.yaml": "5d924a1106bf3a06cfa1c579784e9d8aa9e0cec09d9a4d0150e5531211c2b811",
              "ci/runtime/lifecycle/cases/apache-phase4-response/engine-limit-process-partial.yaml": "4f38b6398eb211da297f71c3a1ad8d5d8fe88808c18926e8aa3b9bddcae6c91f",
              "ci/runtime/lifecycle/cases/apache-phase4-response/limit-reject.yaml": "fb6fcb54b443ba6fe661607c07cc4fc2c29f0b89d52b06f098893890661f96cd",
              "ci/runtime/lifecycle/cases/apache-phase4-response/log-only.yaml": "c6cb64c259226c5a65d755deb5ea7f196a2da18fd121844b781b76e2e94b5ebd",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-deny.yaml": "0f5f3ad1c29229d47de25bdfcaf8fbe67f5acbff44899866e3a7c4ebe275874c",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-phase3-deny.yaml": "ff042a9a5e71d1ee48ffe26397f7b67cf99ca7b464ec624c6681d30dc0195f82",
              "ci/runtime/lifecycle/cases/apache-phase4-response/precommit-phase3-header-freeze.yaml": "1b1ddecef36454f0dbd8444cae1baf49ae41ff9c38abd6affb4e90a2d967cc3d",
              "ci/runtime/lifecycle/cases/apache-phase4-response/redirect-uri-policy.yaml": "b9244adda39713af220b7e05f97746015c4248ea281db692d431a2bc773482ce",
              "ci/runtime/lifecycle/collect-no-crs-source.py": "132df7f2292847ebca9688eaa33bf14b5ce5f09cb4bdbb4b5006afab32f5da65",
              "ci/runtime/lifecycle/consume-no-crs-selected-cases.sh": "8f99d061c30e9124782346667bd55936759c96887afdf75840d9540003d62655",
              "ci/runtime/lifecycle/five-connector-no-crs-profile.py": "39d492145ac7e8b03de8b2e089f6eb0a6ee5c065313201238acd561df154247c",
              "ci/runtime/lifecycle/native-lifecycle-observer.c": "ad8e5e36a17e746cf202c685dbb529fc09717f5c25441b713fa369420aa55ac6",
              "ci/runtime/lifecycle/native-lifecycle-observer.h": "f9f63b62ba8efc555dc20e673cc02251d5ab6c2ab17d8f5efa760d0d97146dcd",
              "ci/runtime/lifecycle/native-lifecycle-sdk.cpp": "89ff282b7287ab30a4194bc06c04835f104b8037442e89b35a68fd1253dcfcfc",
              "ci/runtime/lifecycle/nginx-native-operation-source.py": "3cf60b721a35540d28e91f03b3e78a0066d7983ccac02937428a2b4b688961c4",
              "ci/runtime/lifecycle/nginx_native_authority.py": "7e38a25917e38f99d8c9c102ba62093b4b50d161243926e5dde8da986d1353ca",
              "ci/runtime/lifecycle/nginx_native_collection.py": "b39b3132f36739a6e68596ebaad90ec3ebd102185f728b375f9a5ff5a0c494ca",
              "ci/runtime/lifecycle/nginx_sequence_client.py": "3f8f2220295e7c6c60351dc27525b273040ccaa3bb4e848cd28dc49fe3ca49e0",
              "ci/runtime/lifecycle/nginx_sequence_upstream.py": "8c52f8592037955c9c4cbcf919a066e30be7920eb8d34ab77724f8b7c9b466f7",
              "ci/runtime/lifecycle/normalize-with-crs-no-mrts.py": "5cb7ab24b61a2a590bf9768d2654bff721702ded2f4a90b90d3fa5ef94d928ec",
              "ci/runtime/lifecycle/plan_full_matrix_ports.py": "741760d3154845591e9a9707e0780da6d8ec3a2b020d17393ff95ee9ac63ed40",
              "ci/runtime/lifecycle/prepare-fresh-crs-source.sh": "fdb553b7ccf385fd990141821c678ca9289af66eae1e9ee9e717d2bcd5529f7f",
              "ci/runtime/lifecycle/prepare-verified-runtime-paths.py": "c8dbb1ecd0ff5e953dae40ca29102f091c6c8b05d48b63f7bc119e97e18f89c2",
              "ci/runtime/lifecycle/prepare-with-crs-no-mrts-upload.py": "57b7a2493293f5c49b0b440d8374758e107a610944260731de13168cafc7fec1",
              "ci/runtime/lifecycle/project-haproxy-runtime-evidence.py": "700c12482a563b4d8872ee8717adf9c6e6f5c321fc8361faf8e98f0bc524de6a",
              "ci/runtime/lifecycle/reserve-runtime-env-snapshot.sh": "a5a2153d8b50f1b6d2926659b364c92ebe726b0caaa9a06ab0bfc1b910a6ee02",
              "ci/runtime/lifecycle/resolve-full-lifecycle-profile.py": "474fe90d7bec9610f52c84e490708a0cf86cc27cba1675525c6290fae20a11b5",
              "ci/runtime/lifecycle/resolve-lighttpd-host-binary.py": "39dbf6ff78ba18b83fb18a4b529d96b98ed7879fdd5e0ab0afa1b59459c529e6",
              "ci/runtime/lifecycle/resolve-traefik-host-binary.py": "2d667abb8b167d2de1a254e6a873f262af4d004bd129d9e7bf57eb59f6eb9b96",
              "ci/runtime/lifecycle/run-apache-phase4-response-regression.sh": "78f2a5bf2999f54753af9d6141398259cfccd216a026d5c11670befa9addd295",
              "ci/runtime/lifecycle/run-bounded-nginx-cases.py": "3f4cfa011fe5f14eef36c3683a07994265dfb65fb6d636374a2e73dbae192262",
              "ci/runtime/lifecycle/run-connector-stage.sh": "3904616de7539858a396227e14b0bb5537026b7044719889a360d3e0955d78dd",
              "ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh": "e36c1a937e1c52b070f4247549993e07234e87f1cca7c4ddfb71ba34b65d3408",
              "ci/runtime/lifecycle/run-full-matrix-job.py": "d5f33cb3416e747567a6bda924df1d01ad1a8d7f156a8eb441b6afef463cb56b",
              "ci/runtime/lifecycle/run-full-matrix-parallel.sh": "a20fb467ccc18119573a7b58191421d26be795aff7eddc63724d54e68c080e10",
              "ci/runtime/lifecycle/run-full-matrix-resume.py": "5ce95bfe1ff0c7ea7cf0e7bda0111efde1425ac067af1fab534aa74aea419ddb",
              "ci/runtime/lifecycle/run-full-mrts-runtime-matrix.sh": "4badc2bdf2bad27f0a7c8f3fc563633792459fdf5f56773b94d3f014fcfda6db",
              "ci/runtime/lifecycle/run-legacy-open-connector-smoke.sh": "5d0330ded4e6056466c75e8e31dc571a40926adf296718339f0264f8bed2e529",
              "ci/runtime/lifecycle/run-mrts-native-full.sh": "83dc3ed6cf300cc8aa34aa1497846c1da13942d9e7f5f07e7ba972a9686a6b48",
              "ci/runtime/lifecycle/run-native-case-comparison.py": "1b9e0917c255b5d18cd41e2b03945f7136b6e6989110afde9b332bf8a707516d",
              "ci/runtime/lifecycle/run-native-first-byte.sh": "6c60df7102afea95972c2dcb2dee1685033cc99bc9b06ec369ae81053afcec91",
              "ci/runtime/lifecycle/run-nginx-common-input-fault.py": "a77af00e0c851c2b92e36ac6742dc8ea7a12c02466956ef59fba9f5f00c2458f",
              "ci/runtime/lifecycle/run-nginx-configtest.py": "aed2542ad0bf72af9fd25c3f6f18ecb6f656ef699d615fdf032fe5b3ffe9869f",
              "ci/runtime/lifecycle/run-nginx-event-boundary-cases.py": "9c2475c2c64d48611f62301a581d5e920cfbfbc3693949c40b37cc9cecd39c14",
              "ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py": "73829a2b184c92d3c771334efd0363f72a6ea8f95756ac7b3c6159e4e54b45d8",
              "ci/runtime/lifecycle/run-nginx-mime-cases.py": "75c63cad1de90401b33552715d4a02bb25eca55783b033e831d5430ecbd75fd7",
              "ci/runtime/lifecycle/run-nginx-phase4-cases.py": "32f9fb88a546eec9bd6dece0b86686f312729844c7960ddb5a2c1f49084064fa",
              "ci/runtime/lifecycle/run-nginx-raw-h1.py": "29a7d386ed6755f4e2f6a8226ee168d40809b69043cdc5fbcd6d9a74b6eebd1c",
              "ci/runtime/lifecycle/run-nginx-selected-host.sh": "7f77dffdda373e423a9c43076c30c44d13af1a10aca3763bc652620c11f68bce",
              "ci/runtime/lifecycle/run-nginx-valid-rules.py": "f22b5bf4ed5ac4cef52db9c8590ddede79b48043ed25de5f2ffee8260ad4b69c",
              "ci/runtime/lifecycle/run-no-crs-baseline.sh": "d520534d0acb18cb75d2e00c5b7d666a1398a4144b535a07fd452b74d799afe3",
              "ci/runtime/lifecycle/run-remaining-connector-target.sh": "163127a02f4caca1f860e86681da34e6b60c20d8d0d99f79026591482048db3d",
              "ci/runtime/lifecycle/run-selected-nginx-configtests.py": "d7f394649365631716f6c9077fc02c40091b0ec4d94e72648a58e13d2468062c",
              "ci/runtime/lifecycle/run-selected-nginx-native-operations.py": "97b8609b6aad9c558dfb2d1133331a9aef28d346d8245fc2eb44af31fcf45489",
              "ci/runtime/lifecycle/run-verified-case.py": "534bbd1e5e2cbd21abfe883acc727466c1f16f7e88ae2ca363534f97bbcdb221",
              "ci/runtime/lifecycle/run-verified-report-run.py": "9e39fed4c6210cfb6ccdd0f7f982aebdb50ffd056ae4486886bfc573c75e9211",
              "ci/runtime/lifecycle/run-with-crs-no-mrts.sh": "34ffabcd66507c7abc05950ce7c4719680dafc1da99665ed0a7a31d0519ad160",
              "ci/runtime/lifecycle/sanitize-full-lifecycle-log.py": "a64ea3251e076db075fc4693d0edc7f24de8d0ac4356a8ae9f8b3a849e5d1cfc",
              "ci/runtime/lifecycle/stage-traefik-runtime-artifacts.py": "52b790c6c56c5b1bd37ea9528fa4bc1768ba0edc7f61252cba85c849ca8b7cc3",
              "ci/runtime/lifecycle/summarize-with-crs-no-mrts-workflow.py": "4a20bcf3b17c4c57cc9a77351cffd8e2e22c5de35b9aade5739aa5ca7cbc040e",
              "ci/runtime/lifecycle/trusted_lighttpd_runtime_supervisor.py": "cc74f460fa8a7704ccd95c1d0b9c0d5157d7ed7e3b026fd5158e0485ef5df208",
              "ci/runtime/lifecycle/with-crs-no-mrts-profile.py": "2da241985aa2be3be6ca8557b46d7ef7287e924d4e4be87d6f6a3751fd419bdb",
              "ci/runtime/lifecycle/with-private-sockets.py": "e426b95376db97b98df3e455482e39780078d50ae9d563994e3da04b0b9472eb",
              "ci/runtime/lifecycle/write-engine-lifecycle-artifacts.py": "4ee3e0fa57ec5c9e7a16d9d17c82d535d6f09a44a805106faf86097de1d0fdf7",
              "ci/runtime/lifecycle/write-first-byte-host-metadata.py": "68673de809f4437a5c38ddbda4c7fa6e936c82a7b5389982471e5a3b71af0377",
              "ci/runtime/lifecycle/write-first-byte-source-results.py": "360e0606a76c0eba8b0c331e897e86492801bdf0321a89d3460ee4ca000b0cdc",
              "ci/runtime/lifecycle/write-hostruntime-record.py": "053385a6f95e15006dc0fd0608cdb5128c5aba4ab13b8d83d4306e1d269e9027",
              "ci/runtime/lifecycle/write-nginx-functional-a-evidence.py": "4f12aea27f5354164bca673665b567f135427753bae1c41c7fbcf2c55a2a017f",
              "ci/runtime/lifecycle/write-transport-lifecycle-artifacts.py": "46ca6319e819e76a660ca0513f5273405690015a471cfdd34123e3e4224a8195",
              "common/README.de.md": "5cf445954bc4071ed103471d4f2d562d91225972181f1f5715e04a56b09427ef",
              "common/README.md": "2e7e7fd6070d544ab003107aadc19bd98c223d1bad18c6cec9fa8153fb13f35e",
              "common/docs/design.de.md": "30e5ebf761f8f35cf0f086ceebe6017ff361434fd73899f7ebe593ade9b32920",
              "common/docs/design.md": "af3a6fc164e94a1d0802369b0f00f8a33a4a8c395dae582bdf31b3b2dc0df58d",
              "common/docs/transaction-phase-contract.de.md": "b50d175ef2417dee0a5185605a2159fb42b4f91c2935b3e5276bbc9fd85cb858",
              "common/docs/transaction-phase-contract.md": "aaeed679658ce63698687e1f8d1257be2bce1373917046877bccbe0413077291",
              "common/include/msconnector/adapter.h": "ecaff425e0dae033614a7dc6f143d4c9308a36b8f0f26d15fe87614152f7fbd9",
              "common/include/msconnector/adapter_contract.h": "01e08a1e8cdafcd77a534073d133b48a661295e24c3dfdc966977200797417be",
              "common/include/msconnector/adapter_metadata.h": "5644007681e90c19e6191e88c5398f23d591135413d559a7895477e6c8ca7c63",
              "common/include/msconnector/artifact_layout.h": "a12ea7e38f203fb4ffe0f0b83d63a518a4e3ede2aae2ae69487dec0b3398690f",
              "common/include/msconnector/artifacts.h": "75e3f0b94a4c08238d94bd9e92c0b0e403dd6d3f193feee998713c5d7489f66b",
              "common/include/msconnector/block_statuses.h": "604a6fd7c172016a9411b2aca8703a18b411a61d6b58e52a021ab9114c988f1c",
              "common/include/msconnector/blocking.h": "f400e887a204e38a6ec381e548c3c75e5abc789196aea688081bd9b853a27f82",
              "common/include/msconnector/body_policy.h": "8e7084e4ab112ff6566738ac2a46b4467f8defa1f52c3da113d4b1657f9e7575",
              "common/include/msconnector/build_contract.h": "030c417781f76d7807401022d635e0f0329e44813f6c693676aff74ffc50cb25",
              "common/include/msconnector/capabilities.h": "60997cbd4967d2d0d318ca53cc1af7ad299ee464487404a33064c2f1afce55b4",
              "common/include/msconnector/capabilities.hpp": "af279aadc9bc2fdaf2c69eeb29309d460132bd891f8438429101c72f3cbe6898",
              "common/include/msconnector/capability_matrix.h": "faaaf5496f6ee3db4c9f8e6336f9584b464c4e3b8032a26610d118be2ce9d041",
              "common/include/msconnector/config.h": "3a81652676b81bd97d4d392543db84cb69729c012745fa7f1807eb4319f31d3b",
              "common/include/msconnector/config_parser.h": "dd9f88f70eb20914fb97899de90864b1e56f55cb6710af9cb27fb94847a67231",
              "common/include/msconnector/connector_manifest.h": "84f63cba49eff679194c6e142df179a23c6e15bfecce0308fcbb051dfb1d67ef",
              "common/include/msconnector/crs.h": "cfb1ff7fce3e8f5cdfb63f02002e9dbe9a56197d92914257da77c774845ce1c1",
              "common/include/msconnector/decision.h": "a29c08ee67caa83a3eb146508ed1d6bcc8dc7b27c13cc221a8d074a9b735f722",
              "common/include/msconnector/decision_action.h": "16dc56d9add80ffe51ca987dbda7326e9fb06fea17637c1b87f02b06f94a604e",
              "common/include/msconnector/directive_adapter.h": "2d961c11680bbb49139fb4ec846a28b74e3bc90e1ad4433d6fe547870f97ee9c",
              "common/include/msconnector/directive_spec.h": "4c6eae37390971f41797ae6a1216759e27668b83e4ddbcaaa27a3cd1f3f0e404",
              "common/include/msconnector/directives.h": "d79780a9339de70d7d7746c2918b792fdb3e6ce0dd8a62d29050b8760a142731",
              "common/include/msconnector/dos_guard.h": "2f906760eb2a76ef1aa93d43a2bfc661d317f60d5478209523b3cd90ce3fd297",
              "common/include/msconnector/error.h": "1cc9ca56d2d51eb74056f463abcce951a8079e93b451944c34ac2c97e2914d47",
              "common/include/msconnector/event.h": "acbb5ea952e80f88ce43a6f63d24006f6c6703568ec1dc273a56bced2896a195",
              "common/include/msconnector/event_jsonl.h": "4df864ff98970d8012e29d600bde1b0417c77d3ba9f063fbbadc838b624a6752",
              "common/include/msconnector/event_protocol.h": "2214e119ec6cdca01e1fb5b695495f80823703eec3fa09bc45f905be53a25148",
              "common/include/msconnector/flow_guard.h": "bd16ae73483f19df6cb790bdaf707ecb6467e2ef2a5ce88710fc50519ead161b",
              "common/include/msconnector/generic_mapper.h": "21bc95cb0f637f77210751c65eb912f9936868b4ca1164aa879f6318169309e4",
              "common/include/msconnector/headers.h": "17372f1cec75d33610cd340baa608ba317f6bf6f0f17a562ab5827bc037a3320",
              "common/include/msconnector/http_status.h": "e4f13f7cfae1223aa56673c7c448a25e1a4c6cad78ffa68326d1093d86ad78ed",
              "common/include/msconnector/integrity_event.h": "83a57b7ae647f75b9f05a2614f5b4bb53cd3cb0ee2d097b33d586734c73ed15c",
              "common/include/msconnector/intervention.h": "7cd3f5af2141bd8221205f5f51acdae9df159e83e52f5ee729153ef24f4ee19a",
              "common/include/msconnector/intervention.hpp": "5ef289fc59d723ff1115a33298689ab17d97511b697e79c6bdb890bf16c64334",
              "common/include/msconnector/json_escape.h": "97a2335e648a751cffea08aefd78c40ae114373ff31a7c0d85a419af582c7cf7",
              "common/include/msconnector/late_intervention.h": "c0fccf1a18483d85ce1c50d1cbacde54f3800e554bda0dc2483cfacdbd0ad266",
              "common/include/msconnector/lifecycle_status.h": "a6da04c7e7a69ebbdf88aedeb41b3d525701092b99a3ec5dc5930e086c76a841",
              "common/include/msconnector/limits.h": "c50c6f87869719366226624efabc1feb5452f3a3511d58a7c3eab425cacea3d0",
              "common/include/msconnector/log_sanitize.h": "7de8322a5fdf114edfc8b00bdb2eaed8c62a6bd2ce8f6f870e8400918510532e",
              "common/include/msconnector/logging.h": "c068c9f4dd19cd8410ea760b145dac979933dab3d48fffd89f5cb9abcd49b62e",
              "common/include/msconnector/logging.hpp": "6bdb2d4ad3df381112d10ae8c0162c7d1941045ad6fd6ac420e25e051bd643e5",
              "common/include/msconnector/memory.h": "8e12e78b3fcf31d36d42dae1e3aba069906b8ea10c52e4f84b909b423cf76c1f",
              "common/include/msconnector/modsecurity_engine.h": "e5de4580184c72d54844d724aca55e180db2ec3c2200a2fb78fdd5f383f4f304",
              "common/include/msconnector/native_result.h": "a16c7f5d3661416aa95aed0b5856b2d71728b917b9480f4bb3e0781abb2327bc",
              "common/include/msconnector/options.h": "1dbb1807ab8cb90150be605d57371ecccabfed1ba142c2abcd0ec0dedb1e1301",
              "common/include/msconnector/origin.h": "be8e938fd1f72a6a0c7905347d1c7020ba93c60dad41b171d8be52d2f5c9b88b",
              "common/include/msconnector/origin.hpp": "de70d4483295980612b3e3d894c1abbc979d87939affcc15d6bce266d9a32c0a",
              "common/include/msconnector/origin_governance.h": "7e87ee19f3afaf6be288d0679c39b7539b6740fadd588fee433069ac6a92036b",
              "common/include/msconnector/path_policy.h": "019e24186f9fa9ce692a127ce3e34df37d629f26db24a4c3152e9baf92be4a3c",
              "common/include/msconnector/phase.h": "c3097da8b1d1cf6480a7a7ceb3d97301da06668a082c40e550dd2e79f7149c37",
              "common/include/msconnector/redaction.h": "e3a1c203c8b2be9a4bee476e50c3764a6eee64715baf4de5ee0ec999ea394880",
              "common/include/msconnector/request.h": "f4508228e6964f1620d9e98dc4d7137cc1c575d3b36d862803b773c1056d3e90",
              "common/include/msconnector/request.hpp": "0991512a4ff9116d2d51586777bd770de92a5640bce1fa6dab5d3513718ebf03",
              "common/include/msconnector/request_helpers.h": "de3194debde952645cc27b71b7c82952c0eaa760f38070e5a93439af6ae1f75b",
              "common/include/msconnector/request_mapper_contract.h": "71714b2f289225992cd07d2da8c810618f89a97fa949772006a7345752659440",
              "common/include/msconnector/resource_limits.h": "9daa3c67ea6808f5ce0f0c9381e287ad045aed1668a9e3b1ab41d354c017019c",
              "common/include/msconnector/response.h": "4ef1a7b000097edeeae920904c0deaa88be4dfac9a85ad18c2a8e829cdbf3d55",
              "common/include/msconnector/response.hpp": "dabc8933fc38759c72fa4fa052f05fc2357064c79089160cc54a13bfee56590f",
              "common/include/msconnector/response_helpers.h": "dddb5bb998ac2b447ab8e9db10cd5ba83c8b53ab205ca90e52fe3bce2342e143",
              "common/include/msconnector/response_mapper_contract.h": "bcfb70b93384f711cf751af3a84ab835f079bec0f9c5fba3a22725ef04f9b6e8",
              "common/include/msconnector/rule_error.h": "af251cb2686a0fffe92446d3ac428bea1076e2afa6a559e44f272e37e64110d6",
              "common/include/msconnector/rule_event.h": "bde25165fd2967d26646a2abb35c62947100d9f7d2f2fb43801ccd3ffaa9ce52",
              "common/include/msconnector/rule_id.h": "a00c7a1dd97cee368af7e30df043ebb150756edc98766471d65b73e3ab25c94d",
              "common/include/msconnector/rule_load_stats.h": "12c501883a5c1798fea3d3064c0f7e3a8c29c31552aef40a11035f245d6b06ea",
              "common/include/msconnector/rule_loader.h": "a9529a7c0189207613b04b0d329dcb0ce9402b692363a7ccff20a400d783771d",
              "common/include/msconnector/rule_merge.h": "e8ca8cae33fb824940667b19ff7abeff5edd02ece64e96397e9d96cd5ef26310",
              "common/include/msconnector/runtime_paths.h": "f0368755817351ec8fd6278e7f539a6053ab9c2de0c4ef6d73e2873e713b5d42",
              "common/include/msconnector/runtime_report.h": "38413741b9cea29cde986c169a86ba9e11675b51f9896784141c90ff3c37af0f",
              "common/include/msconnector/status.h": "47943b4baa61990f8bfa1a2e0a6f82d2a3a159145b4fc85a9702c347cb4ef256",
              "common/include/msconnector/status.hpp": "aae1d9eb582ebbd029b9faf256e7b389c722e35243d5a864f3e3d3e51740efe3",
              "common/include/msconnector/test_result.h": "208132abcbfb4d1cb228dbf895ba42e6cf73911cde004d675947e4f2b80e9807",
              "common/include/msconnector/test_result_json.h": "62b7931ff4eac1cf867943689aefac7d52bf2dea4e1cf1781467608120d9490f",
              "common/include/msconnector/transaction.h": "4a9af32abd6458c6be9e339ccba2f5ecc15cc0c782ccad9a402df0e4f363b76d",
              "common/include/msconnector/transaction.hpp": "739489f2b452da87390702e11cab3d9e11a09dfd2dbfabdaa0020964d4979d86",
              "common/include/msconnector/transaction_contract.h": "803cc283e89740f980bcfa98b46907302ed8e30502d0b9168ddecf41193ab8fe",
              "common/include/msconnector/transaction_id.h": "ecede908d5127bf8032ce4180d19b2b229b2b405e94d178f4142e463068b8eb0",
              "common/include/msconnector/transaction_state.h": "00a455c2d1523c1ab6cfd027f9fb2a9f85be2fecdbaaf2d62f039c7532104547",
              "common/rules/modsecurity_p1_p4_vectors.conf": "00ac195a80131405971f278c4eb87c9d125388d140476c1297915e6bbac02973",
              "common/rules/modsecurity_request_body_smoke.conf": "91d66822bec2a6f4abf30ede91b7f494f28235c5bc729936b6a0dd36c28af13d",
              "common/rules/modsecurity_response_companion_smoke.conf": "7aa57b053e725ec567c799eda73db7f071e601ab5a5ce0839d8c30e47f6b0b8c",
              "common/rules/modsecurity_targeted_smoke.conf": "f97e14ab1e1b739b2fc4abf3959c51ae9d76c53550d86b2162f3fccb71e0730e",
              "common/rules/p1_p4_traffic_vectors.json": "6298353b8725ef69ea740bddefdfde0ab704d9c2719c62bd702e8fa4673cbe05",
              "common/runtime/http_authorization_service.c": "7f1544f1f36042c68359c7caed7d5dc4ce8cc77d44282debdc3955ea725a5e9c",
              "common/runtime/http_authorization_service.h": "1c5996cca00ee2b89673a5157f598dc2ce06203f91941b9f44cc019e063de64a",
              "common/runtime/msconnector_runtime.c": "0fa85f5658be96a25204adf489b2e18149a5f826b5ed528e55ec7b2ffe410aa4",
              "common/runtime/msconnector_runtime.h": "202ac41d732d8ac5c1fec266bd7b49ae4cec1e0f5727c3c0d38832c6d58ceb3b",
              "common/runtime/response_companion_client.c": "8534bbde095b46507c7f4ad109c521fb8c9c03c76c43daa391fe1c44cdfbbc60",
              "common/runtime/response_companion_client.h": "581ff79c969225ebb768d9a2477f83716ee97a61f20ae6fbeee0c442ae7bc7a4",
              "common/runtime/response_companion_protocol.h": "634529f2801423b411b303e408f9735f4e1123294c4cba6dde79957ebb594188",
              "common/runtime/response_companion_transport.c": "268e522789b77af2d4942d6b5981c7ce582a4fad03a2822b79c26f1065e8ffc4",
              "common/runtime/response_companion_transport.h": "606e8a7c9d7ce1772cab3a638de7e48e3e025949be3bb0237fb658cb84989e8f",
              "common/scripts/modsecurity_targeted_eval.cc": "f0def448dba5107735c75262ae7568aec1fd2a6de18355902120c0d74b0afb18",
              "common/scripts/run_blocked_runtime_smoke.sh": "9308998ad3d2cba6b28709b373d2719a655dc77d32be71481ef41f8cf7028ca4",
              "common/scripts/run_local_runtime_smoke.py": "f06c33fc6f9084a4a36218153de944f523f42d5c0cc89469f9244efaa02b87dd",
              "common/scripts/write_smoke_result.py": "35d2d86164672dfbe0fc2c648e41ba03df38ad9a335cd655995d650f769cda77",
              "common/src/README.de.md": "760a994ec35908128f9a6beb68733d07af17d8d59de7061f06757a9042afaab7",
              "common/src/README.md": "7a7c5b9ddd534d333a3a212fd25602f0c84499d73822349f8cf97e7f9573b778",
              "common/src/adapter.c": "516e776a748c5a586089f429827215782cdb71b759b82bd7eec724cd5de1555c",
              "common/src/adapter_contract.c": "61c07a434ac5ffb3bb30ae0b50a146f5cbe783f69842a384f76e049e3fc124fb",
              "common/src/adapter_metadata.c": "56d5890cff7c152297688d00d994f6945c00397303d5f459cb9dfa7805eaeefb",
              "common/src/artifact_layout.c": "6468d87635446a35035a5aa2569d3b2341fc55a35e4ee2f27a3e32648455e453",
              "common/src/artifacts.c": "04859ebe04ffaedf894bdfe3e06cde921b8e527588b5ac53dca45f950fd4ed00",
              "common/src/block_statuses.c": "ea691e18cfb3ab2733b878f41cd802332b60d8eb9c8f3f56548c37495de736bf",
              "common/src/blocking.c": "4f2776c88c7b95ebc7c3adfdb12e147dad002594dd3f95e6a38051c615717460",
              "common/src/body_policy.c": "735027686a02d2e867e00bbd9d7eafc445c1f343eac1ec93b4289d4d4813cdb5",
              "common/src/build_contract.c": "792123920f333f0dc3505125df2d194b2319cffd3fb3d9adc5ef877a960497d0",
              "common/src/capabilities.c": "801d8f0d58c70a987104098fcb4e04d147d4ccd1dccc14e9accd6253efff6e3b",
              "common/src/capability_matrix.c": "fa01a76c4b0f4184b25710da06823ded6c0a38700b539864c892c717f7f0f277",
              "common/src/config.c": "3e5f6c0130b0c1f79a540444a96bb051596e6072843888f7b5aad8ae61560c27",
              "common/src/config_parser.c": "8dca03ec371a52681d1721bf76e8b4098599bf654755b7f489191cb5290168b6",
              "common/src/connector_manifest.c": "4a9e5456b6fd8c20dcd0eeff8ca3048cfdc7577f8da4ffa71a918c309e367f75",
              "common/src/crs.c": "d0a394d9e29df1bf80c4b7276bbd3bd7b12192d275856117d82615a9946263ef",
              "common/src/decision.c": "e42a17aa86541ecf573b336d049f57014a1a1a8e257613491a9d5e05cb44d174",
              "common/src/decision_action.c": "7c75f3b45f661300d8cdb328dec57ef4f403ba0ed0fa3fc8400d9aa55481b9a2",
              "common/src/directive_adapter.c": "402bd6fe396f774df3e990849882bcdce5d2e52abcb7973c4a8e0a6da4835263",
              "common/src/directive_spec.c": "8c75a3e97f781965ed023df99cc11adc0013e78f4bdaec0c9e26c664823b43ef",
              "common/src/dos_guard.c": "bfc304695a6801a5ab1256f9703429a506f80519fef15a7f9e6a271c004e17d7",
              "common/src/error.c": "4509eb4b33820c2ca6300b314f88c99e06d8a5e6361900783b8f7aafcee33f86",
              "common/src/event.c": "0032e25cac8dd310eee620f606f598db830a84898baf26575cfee19b03166e03",
              "common/src/event_jsonl.c": "dc3a21fa47075fe96f19d7b12c8015db7a8d2b407d65a678ab0f1487de1ddcef",
              "common/src/flow_guard.c": "8e43183bf42ace059c16ef7984fe5b835a822cd2b439f73f17cb96261ed7dc72",
              "common/src/generic_mapper.c": "ceacbb368c5bd35212a9a613b63b01b9e71158dd1aed3a6e0905febdee0ed850",
              "common/src/header_validation_internal.h": "b9ca7130e184913c10b3b24cfae18415eef411a908b1af5f926af6b695ed11e7",
              "common/src/headers.c": "1bc8351188daf20a9b8f0db47f73ec5a64afedef59776b56206b35f43666bc12",
              "common/src/http_status.c": "b6ad0c69ae47150170919096eaf7b444a097b0e8b88d25b0b7be13bbe9777a69",
              "common/src/integrity_event.c": "c2ad7f26cf051321e269f50d0e8afb9f3aa5a8a3a416f55e63e1278392753041",
              "common/src/intervention.c": "91c7fbd9cf158a2e46c59af2b534f0b77dae2cee84fff038509c129b471db4a2",
              "common/src/json_escape.c": "d9d8e7e1cfc6ad5e82e227044f5c8ebbbb8489f13caab99a8e3f02cf5d279e0b",
              "common/src/late_intervention.c": "aa29b1ad82f176320fdadbf2357ee616cc7ca1ff6966063911a4eb2c5cacc812",
              "common/src/lifecycle_status.c": "3dab0f986e7ed1959bb5d1425c666061bad6816dc8262c27a64e3ba49ff1c971",
              "common/src/limits.c": "3282ce8e7143a7d481e831cf02ec9d08729dd2f7c0015bccfdf336a409767aa0",
              "common/src/log_sanitize.c": "9fc0b1e53225fc95f3a43ec7ff0df4d2f0eb4bb363eee19ca3e693e0a958a943",
              "common/src/memory.c": "f38f868c0355a3722c027a477f0bd762f6c1a9a08a12c5c7b814aeec58cbe9af",
              "common/src/modsecurity_engine.c": "a77b04c3e2deaf5146e0e164efb56f32dc76eebab9e3eccc6604f0e9483fedd1",
              "common/src/origin.c": "559ec9880e83cd386f5986cfc155ea3dd8edfa7f379a39ebca7839f0cdbc7130",
              "common/src/origin_governance.c": "313e09a5b2865315a932d7243d9e5eee85b9a1c4dfb4276e60fb5c2d3fab32b2",
              "common/src/path_policy.c": "790146307f4600359ef3d6d573e6fc1b674b9b8e796ddfa67579f2d4b2086802",
              "common/src/redaction.c": "e7b74654e806615ee61569e8c6424be01bfeea61448cfebbb8c1be7f26c16c6f",
              "common/src/request_helpers.c": "f3c3d4ddd6693bc330a3ec24a1d1491af64ac2544a26696cf010babd1a4ce790",
              "common/src/request_mapper_contract.c": "df427fc2e28a4a94cf252470654a46453335cf361919f229c0f328d54f9a746a",
              "common/src/resource_limits.c": "0affa0f5ad598aa94dc6ce8b480c178adcf7b2be4b9a12f9fed6ee82a17c0767",
              "common/src/response_helpers.c": "d24c987d55e2b362035d04dda5a81889026aafdad9d1a1541c741cba9ed19cda",
              "common/src/response_mapper_contract.c": "e7d71677bbc94f21268502cb64163038d17bdad8307049df66ad07b2597574dd",
              "common/src/rule_error.c": "0e6e1756e43fc946bec2c2ee090681d6398339da240121595e891aaf76e90735",
              "common/src/rule_event.c": "18676a24a88c33a7f991b777d96d151ba364541153b6265498a6be6cb5b54387",
              "common/src/rule_id.c": "6cf8cc24a6de62e74376edf73bd589b3f4c26f66dc0a53ae92b626d5ac70435b",
              "common/src/rule_loader.c": "e837121b19b1239e2667cc97b5c3279066f36c20b63afd2ca1e6c544407a4e56",
              "common/src/rule_merge.c": "db7b8097adaffa612d19ccf23253b2e583db161904fa1b9a9e3ee37e48330b15",
              "common/src/runtime_paths.c": "168de23208e3b00647caf543307bec0e3029db5ac78e18e3c8e1be23e4340b07",
              "common/src/runtime_report.c": "e7e61cf66cc7c64adeda7449b480a96b49f1b0efa758c5b8fe3536db6720a30e",
              "common/src/status.c": "8cae41d98f3ee4f8978e01100c59b2882a078e683fae38c42839d3bf3566ccca",
              "common/src/test_result.c": "997b5f047b7d3fd77e457135945961314fc64e21beb636685761dde85bbed86a",
              "common/src/test_result_json.c": "d904738d35db3579b6cd4ea3b12ff14caabd0090754fb30bb1da8f7072cc1c78",
              "common/src/transaction.c": "b6f621703ef7238295eb49257666e6d6a4249333bf4ae939d1fbab9a06712bdf",
              "common/src/transaction_id.c": "64630d1671bf58fec7f208aa43b957da915d9f2cbcd65a1ffba2ab06c741beaa",
              "common/src/transaction_state.c": "b4f35347531cc380f8bf71c3c7192ddb46442974a14374d332037373b6ffe860",
              "connectors/envoy/ext_proc/README.de.md": "379168c919b0583350f44bb0048b0aecb9d5b7f3ae154e516254b4c0be581cf6",
              "connectors/envoy/ext_proc/README.md": "84eee6a0c2e813b8cf737006853780c70253d6030959442b98716c087eddae7b",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_common.go": "019d7149165a5f1709d1dc4228581e6aba64c453654d70a7c541a6400602ac09",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_passthrough.go": "e8ca083f672809f0ad410f49b3c91df735415cd92ff5ea021e196664a216729f",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/engine_passthrough_test.go": "9d9c571342716ce1303a531f26e6b8f28632e07fe89e8c23ff73bec5cada1707",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/main.go": "c07f99755bb1a1fbad95fc2f70941937a4a517bcfbf19865c8ddef8d64dbe1d0",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/main_test.go": "6fcafd2256758062d620e4c8633b31fbea3cca7793363e29dba8b97e41a95954",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/observer.go": "d86e8a45d3329a04317d9447d4f1e2efeea8146053bbbb3d6285341fee3e9ec4",
              "connectors/envoy/ext_proc/cmd/msconnector-composite/observer_test.go": "c26b6281069fb364fef756d6b496ccc8d3ad837ff17775126e493d7a367ba9f9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/engine_common.go": "2442966b3c81b188be15753a0c9829b43299ee747eae5b9b86054ce9a9eb1758",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/engine_passthrough.go": "5447b3e4ac36aca83e7567d9ac602283f923c9e7e5a155f9fc88fccedacb3c65",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go": "d356dcbf1007e62d7b973c9bdc055015b64bab060d558162b3e96771dc664d52",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main_test.go": "5c1840c4d051031d36b1ccd86f95c6cfc06142ba476122bdbfe697b6f3db3848",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main.go": "8ef1046f9549b46a1fa88bf399696f263e7c2faee107e52c0c4a30ced6f41db9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main_test.go": "5ec9223b304dd63932d05cc6a51839a6fd9d59598d178b2afd177134da3520d9",
              "connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/peercred_test.go": "44991db7bd1bf9c0c8262c9c97b9be6bcf6130c20a74b42deda7894cb6ff9ac5",
              "connectors/envoy/ext_proc/go.mod": "9a52853f5e3839f500655c1d6cc8785b7cd379da55fe8e9a6374ac8ff0ece7c6",
              "connectors/envoy/ext_proc/go.sum": "66100e55eddccb812d04e1b841a7721c25cbab30b0cd5e690242368b7d2f5963",
              "connectors/envoy/ext_proc/internal/composite/coordinator.go": "507b4b2117a1b6582b0e0eacc8a4723b466bedf26b4b8d0752dc2ba3d8f3f9fe",
              "connectors/envoy/ext_proc/internal/composite/coordinator_test.go": "cc8c9b2c37a896b4e03177d073e6a8074896f663f4cbc77475856b2de6f69ab4",
              "connectors/envoy/ext_proc/internal/composite/i12_envoy_observer_test.go": "7a12e7dc914899a337b42defbebb793d1fb96757e170d4a8bbfb4a95a5d7e07c",
              "connectors/envoy/ext_proc/internal/compositeenvoy/common_body_completeness_test.go": "a2559bba9226e56b312b111b33aea7651c6160b8064e9d78fd000d941cf79992",
              "connectors/envoy/ext_proc/internal/compositeenvoy/common_runtime_integration_test.go": "8ae2100dfbfa6b64bc0b1b4b04765272e62ec261db3127a1342a053f9aa33bf9",
              "connectors/envoy/ext_proc/internal/compositeenvoy/server.go": "028e1e21cf1e1313cee0e951b82fd8fcb9c492bbf1dd63401455585d01c6db4a",
              "connectors/envoy/ext_proc/internal/compositeenvoy/server_test.go": "595be39d20afa24ab6fa4e747d5b397d0c1948b61bb6e5272f24cf3720e6a5d0",
              "connectors/envoy/ext_proc/internal/compositeenvoy/technical_error_test.go": "6cfbc98bad68ab30fffa836db5c47a60a9312b9864f0251eed1667c711eb0055",
              "connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go": "7f7a2776032b702a101222ef38db60d012f263aedac9fa67a721613e5c606e2d",
              "connectors/envoy/ext_proc/internal/compositetraefik/forwardauth_test.go": "01e82e24837612a493e9d48469a4440ace95fd79b9f7e55c10e767381a99678b",
              "connectors/envoy/ext_proc/internal/compositetraefik/uds.go": "07202ce16684e08d3ab4b46f0c3385a50491b4c6a59d6028bd5e29cccec2151b",
              "connectors/envoy/ext_proc/internal/compositetraefik/uds_test.go": "aa0215397c66b8d33ab6c5b65883a2bfaffbc154031ffde0e596f55c6a78fef8",
              "connectors/envoy/ext_proc/internal/processor/body_limit_host_action_test.go": "1ac63d7c8ecfbff3481a03be9f536124069e6dda043ed308afaff9877d729e4e",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c": "6449bd0d2cb2a71676d09bf6f8d464bfa1d68f0dbab73f61887c028fedd8ccec",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.h": "c06ab9f8ef468f241186232caf47fafc5cf12eef2d76b57cd016825573520783",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_commit_test.go": "3811b81a35710cda0723c6451032c0a2e7008f8b360bb93aa38077c2355be25c",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go": "3df8f38891d9a9ee0053ac5beba6615cdce5772661af8cffe8c0c62506daa1d8",
              "connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go": "7e9a89cb1e233dcbc23c740a8636786c4bd65f57aa6fae6efe07f2aacbcac455",
              "connectors/envoy/ext_proc/internal/processor/config.go": "321b16b82919ec43b0f12dc59b5de55058496930e1a4cfcea8a51d7c55da8851",
              "connectors/envoy/ext_proc/internal/processor/config_test.go": "4140137ebcefd1e04da6cb728d8a2284640142f68a5464b39f50e61c27c04dec",
              "connectors/envoy/ext_proc/internal/processor/i12_envoy_observer_test.go": "433b6d3ece97401bb7f910d8b29860f8ece7931e88be7f1155082f68b8942130",
              "connectors/envoy/ext_proc/internal/processor/jsonl.go": "1ff55bf56bfb02f594cc8f2a09b7efa128f106d404c32568716845add50117d6",
              "connectors/envoy/ext_proc/internal/processor/jsonl_test.go": "c784a60e1ede32bc40ce3df11a1b16ec5850f75f74432a905a45567222fdca8a",
              "connectors/envoy/ext_proc/internal/processor/phase4_budget_test.go": "6f8ff027396578421764374d5e88a0e29e52a547e651f6cda5b5211bd3f9f064",
              "connectors/envoy/ext_proc/internal/processor/processor.go": "6c8461d73cd43b2a789ca69a2477c0e1f2440b3346bd27ad9bccc469d48b1762",
              "connectors/envoy/ext_proc/internal/processor/processor_test.go": "3848137c942fab9593ee227a2c73494cc262b4867ebadc014ba35b90f73af449",
              "connectors/envoy/ext_proc/internal/processor/technical_error_test.go": "3653bd940540c94ee799f50c2b09556cc7027b131cf4d1929c61f8051e7890cd",
              "connectors/envoy/ext_proc/internal/responseobserver/client.go": "8869025eec2ad73e330291c96d2812bb52ff6f79b14d5fef6c195661070b3473",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_linux.go": "77238e197fec60ec668ceeafde35d27a577da4e8d6ff3f48b3a742d4d7cbbaf6",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_linux_test.go": "de350e573b0d62f5ea31a76a318226217092f69ac653505d87d6376a14621e7f",
              "connectors/envoy/ext_proc/internal/responseobserver/peercred_other.go": "74349b4b04faadbfbf3d40644474700543120f5539e445202ae25176f1c5b36a",
              "connectors/envoy/ext_proc/internal/responseobserver/protocol.go": "f497571a69479edbc68094594e6d75f6633d238662e42be6640412d9d04ce0cb",
              "connectors/envoy/ext_proc/internal/responseobserver/protocol_test.go": "a6c489c75f18ca8062b43455c6c7d533738b05ef2249f13f4004a29a77b15537",
              "connectors/envoy/ext_proc/internal/responseobserver/service.go": "6e96afed63fd7343e9bc1188950b38d23371f08063c50dba4f276eda2d74c633"
            }
          },
          "case": "I12::envoy-ext-authz-response-companion::NEED-lease-claim",
          "delivery_scoped_verified": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
          "delivery_source_baseline": "02754040bced960cfc1857416cd7101bb3116ef4",
          "engine_sha256": "719a9ddd277e9b04482d55684266a96989b384e37789df6d8482549a46e7fcc8",
          "fixture_configuration": {
            "/mnt/fixtures/native.rules": "b23c5d07aa8bcd39d6f7f208234c62e3866b1132331987264c2325b2a562c789",
            "/mnt/fixtures/shape.json": "e8113475def914947c8d720cc069d2f5c2c261935d5270e0813d635d437432cf",
            "/task/runtime/envoy.yaml": "cc78f9be754480a54340275ff9fb0963b511e4bb63b08593fbefac28a31d45b3",
            "/task/runtime/loopback.crt": "dc1e56ec0121f66d895606caaa16f88f0b2712ac57d858c46a76988581ec4bad",
            "/task/runtime/loopback.key": "cba53939369aa8e21610fbd0bc4eb86fc3846e6bee883a7c65ad957927dd8bde",
            "/task/runtime/native.conf": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb"
          },
          "host_sha256": "002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8",
          "product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
          "rules_original_sha256": "b23c5d07aa8bcd39d6f7f208234c62e3866b1132331987264c2325b2a562c789",
          "run": "envoy-i12-env-companion-b99d9ec5",
          "runtime_backend_profile_actual_source": "envoy-ext-proc Common runtime backend reused by actual composite adapters",
          "source_git_baseline": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness and declared private overlays",
          "source_scope_count": 167,
          "wrap_symbols": [
            "msconnector_transaction_contract_init",
            "msconnector_transaction_contract_finish",
            "msconnector_transaction_contract_cleanup",
            "msconnector_transaction_contract_complete_phase",
            "msconnector_transaction_contract_set_response_committed",
            "msconnector_transaction_contract_record_response_metadata",
            "msc_new_transaction",
            "msc_new_transaction_with_id",
            "msc_transaction_cleanup",
            "msc_process_request_body",
            "msc_process_response_body",
            "msc_process_logging",
            "msc_append_request_body",
            "msc_append_response_body",
            "msc_process_request_headers",
            "msc_process_response_headers",
            "msc_intervention",
            "msconnector_runtime_transaction_begin",
            "msconnector_runtime_transaction_begin_request_stream",
            "msconnector_runtime_transaction_append_request_body_chunk",
            "msconnector_runtime_transaction_finish_request_body",
            "msconnector_runtime_transaction_process_response_headers",
            "msconnector_runtime_transaction_append_response_body_chunk",
            "msconnector_runtime_transaction_finish_response_body",
            "msconnector_runtime_transaction_finish",
            "msconnector_runtime_transaction_destroy",
            "msconnector_runtime_transaction_finalize_and_snapshot",
            "msconnector_runtime_response_companion_handoff_with_handle",
            "msconnector_runtime_response_companion_claim_handle",
            "msconnector_runtime_response_companion_revoke_handle",
            "msconnector_runtime_response_companion_session_process_response_headers",
            "msconnector_runtime_response_companion_session_append_response_body_chunk",
            "msconnector_runtime_response_companion_session_finish_response_body",
            "msconnector_runtime_response_companion_session_set_response_commit_state",
            "msconnector_runtime_response_companion_session_record_host_action",
            "msconnector_runtime_response_companion_session_fail",
            "msconnector_runtime_response_companion_session_cancel",
            "msconnector_runtime_response_companion_session_release"
          ]
        },
        "actual_scoped_baseline_inputs": 167,
        "delivery_scope_verified": "8cc32dceb06121f589150a9794f28878c5e4ba2a",
        "git_source_base": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness and declared private overlays",
        "native_config_sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb",
        "product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "rules_sha256": "b23c5d07aa8bcd39d6f7f208234c62e3866b1132331987264c2325b2a562c789"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "af2262cdd63a00a19e1e28bd18c6c63c1a87a1cfd611dd0c7dfb872a092e55bb",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "b23c5d07aa8bcd39d6f7f208234c62e3866b1132331987264c2325b2a562c789",
    "run_id": "envoy-i12-env-companion-b99d9ec5"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 347099,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-envoy-companion-01.json",
    "sha256": "61fa58bc0af158e60a7143e9e54e5ebaf7c2ebc421e984b9872d5932d5bd9f85"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::traefik-native-uds::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 579,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/result.json",
          "role": "cleanup_observer",
          "sha256": "53faaa068a63d6e81f179f00cc3a9b82a8b7974d8c33cb53aadbc51060b887a8"
        },
        {
          "bytes": 4601,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "83b457b6c0365e7debe1969ad3c5ef7c6b3fa836b6dd7195699e1101cca82268"
        }
      ],
      "value": {
        "driver": {
          "case": "I12::traefik-native-uds::NEED-request-eos-once",
          "neighbor_health_probe_count": 1,
          "processes": {
            "backend": {
              "actual_pid": 871,
              "exit_code": 0,
              "proxy_pid": 870
            },
            "engine": {
              "actual_pid": 875,
              "exit_code": 0,
              "proxy_pid": 874
            },
            "traefik": {
              "actual_pid": 879,
              "exit_code": 0,
              "proxy_pid": 878
            }
          },
          "qualification": "unreviewed_measurements",
          "selected_case_count": 1,
          "socket_directory_cleanup": true,
          "socket_removed": true,
          "target_and_neighbor_commands_exit": 0
        },
        "observer_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "I12::traefik-native-uds::NEED-request-eos-once",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 98938943765221,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 875,
          "profile": "traefik-native-uds",
          "result": null,
          "run": "tf-i12-eos-20261014",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 142,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792008572733170688,
          "wall_sample_end_monotonic_ns": 98938943765334
        },
        "retained_artifacts": "exact source/build/config/stage evidence retained; metadata retirement is not APR memory-free evidence"
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 143862,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "588a950cb74ac479de9842089080182b9140cba2aacfd7c031e8796d73a527b6"
        }
      ],
      "value": {
        "actual_common_finish_calls": 2,
        "actual_native_logging_calls": 1,
        "actual_runtime_finish_calls": 1,
        "common_idempotent_calls_are_not_new_completion_transitions": true
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 14802,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/runtime/logs/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "c302eb4815b393569cf5483c3233440060b21cef9a5665e6d131ef55fce51a8b"
        }
      ],
      "value": {
        "actual_callback_end_true": [
          {
            "elapsed_monotonic_ns": 1343146408,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "end_argument": true,
              "error": false,
              "input_bytes": 39
            },
            "operation": "request_body_callback_return",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568538868644
          },
          {
            "elapsed_monotonic_ns": 1350201181,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "end_argument": true,
              "error": false,
              "input_bytes": 0
            },
            "operation": "response_body_callback_return",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568545923404
          }
        ],
        "actual_explicit_eos_frames": [
          {
            "elapsed_monotonic_ns": 1342497951,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "error": false,
              "opcode": 3,
              "payload_bytes": 0
            },
            "operation": "uds_frame_write_return",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568538220145
          },
          {
            "elapsed_monotonic_ns": 1342998999,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "error": false,
              "opcode": 3
            },
            "operation": "uds_result_parsed",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568538721220
          },
          {
            "elapsed_monotonic_ns": 1349215907,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "error": false,
              "opcode": 6,
              "payload_bytes": 0
            },
            "operation": "uds_frame_write_return",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568544938091
          },
          {
            "elapsed_monotonic_ns": 1350055017,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "error": false,
              "opcode": 6
            },
            "operation": "uds_result_parsed",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568545777216
          }
        ],
        "actual_request_reader_returns": [
          {
            "elapsed_monotonic_ns": 1341275204,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "bytes": 39,
              "eof": true,
              "error": false
            },
            "operation": "request_reader_return",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568536997417
          },
          {
            "elapsed_monotonic_ns": 1343398356,
            "epoch_wall_ns": 1792008567195722178,
            "fields": {
              "bytes": 0,
              "eof": true,
              "error": false
            },
            "operation": "request_reader_return",
            "pid": 879,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-eos-target-53b4c671",
            "wall_ns": 1792008568539120583
          }
        ],
        "reader_eof_count_is_distinct_from_eos_handoff_count": true
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 143862,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "588a950cb74ac479de9842089080182b9140cba2aacfd7c031e8796d73a527b6"
        },
        {
          "bytes": 14802,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/runtime/logs/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "c302eb4815b393569cf5483c3233440060b21cef9a5665e6d131ef55fce51a8b"
        }
      ],
      "value": {
        "actual_native_process_body_returns": [
          {
            "argument_committed": null,
            "argument_response_status": null,
            "call": 23,
            "function": "native_process_request_body",
            "input_size": null,
            "monotonic_ns": 98934748974927,
            "phase": 2,
            "result": 1,
            "runtime_eos_handoff": null,
            "sequence": 24,
            "wall_ns": 1792008568538380397,
            "wall_sample_end_monotonic_ns": 98934748975069
          },
          {
            "argument_committed": null,
            "argument_response_status": null,
            "call": 51,
            "function": "native_process_response_body",
            "input_size": null,
            "monotonic_ns": 98934756051905,
            "phase": 4,
            "result": 1,
            "runtime_eos_handoff": null,
            "sequence": 52,
            "wall_ns": 1792008568545457413,
            "wall_sample_end_monotonic_ns": 98934756052088
          }
        ],
        "actual_runtime_finish_body_returns": [
          {
            "argument_committed": null,
            "argument_response_status": null,
            "call": 22,
            "function": "runtime_finish_request_body",
            "input_size": null,
            "monotonic_ns": 98934749160085,
            "phase": 2,
            "result": 1,
            "runtime_eos_handoff": "request_body_finish",
            "sequence": 29,
            "wall_ns": 1792008568538565537,
            "wall_sample_end_monotonic_ns": 98934749160210
          },
          {
            "argument_committed": null,
            "argument_response_status": null,
            "call": 50,
            "function": "runtime_finish_response_body",
            "input_size": null,
            "monotonic_ns": 98934756169004,
            "phase": 4,
            "result": 1,
            "runtime_eos_handoff": "response_body_finish",
            "sequence": 57,
            "wall_ns": 1792008568545574434,
            "wall_sample_end_monotonic_ns": 98934756169079
          }
        ],
        "append_eos_argument": "N/A: selected public append APIs have no EOS argument",
        "definition": "Actual accepted host EOS frames, observed public body-finish callbacks and their nested native body-finalization calls. Native append has no EOS parameter; the original observer null field is retained rather than converted into an inferred flag.",
        "observed_nested_finish_body_spans": [
          {
            "actual_native_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 23,
                "canonical_transaction_id": null,
                "case": "I12::traefik-native-uds::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-eos-target-53b4c671",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 98934748873995,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 875,
                "profile": "traefik-native-uds",
                "result": null,
                "run": "tf-i12-eos-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 23,
                "transaction_id": "tf-eos-target-53b4c671",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792008568538279482,
                "wall_sample_end_monotonic_ns": 98934748874155
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 23,
                "canonical_transaction_id": null,
                "case": "I12::traefik-native-uds::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-eos-target-53b4c671",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 98934748974927,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 875,
                "profile": "traefik-native-uds",
                "result": 1,
                "run": "tf-i12-eos-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 24,
                "transaction_id": "tf-eos-target-53b4c671",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792008568538380397,
                "wall_sample_end_monotonic_ns": 98934748975069
              }
            ],
            "allocation_scope_call": 2,
            "pid": 875,
            "runtime_call": 22,
            "runtime_enter_sequence": 22,
            "runtime_function": "runtime_finish_request_body",
            "runtime_return_sequence": 29
          },
          {
            "actual_native_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 51,
                "canonical_transaction_id": null,
                "case": "I12::traefik-native-uds::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-eos-target-53b4c671",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 98934755618210,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 875,
                "profile": "traefik-native-uds",
                "result": null,
                "run": "tf-i12-eos-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 51,
                "transaction_id": "tf-eos-target-53b4c671",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792008568545023687,
                "wall_sample_end_monotonic_ns": 98934755618339
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 51,
                "canonical_transaction_id": null,
                "case": "I12::traefik-native-uds::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-eos-target-53b4c671",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 98934756051905,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 875,
                "profile": "traefik-native-uds",
                "result": 1,
                "run": "tf-i12-eos-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 52,
                "transaction_id": "tf-eos-target-53b4c671",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792008568545457413,
                "wall_sample_end_monotonic_ns": 98934756052088
              }
            ],
            "allocation_scope_call": 2,
            "pid": 875,
            "runtime_call": 50,
            "runtime_enter_sequence": 50,
            "runtime_function": "runtime_finish_response_body",
            "runtime_return_sequence": 57
          }
        ],
        "original_observer_host_eos_field": null
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 143862,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "588a950cb74ac479de9842089080182b9140cba2aacfd7c031e8796d73a527b6"
        }
      ],
      "value": {
        "actual_cleanup_calls": 1
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2712,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/before-target.json",
          "role": "loaded_image",
          "sha256": "997568067faaa34d01009ac3edce70aca1de1be7e10b58ef82749b6da254c897"
        },
        {
          "bytes": 4601,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "83b457b6c0365e7debe1969ad3c5ef7c6b3fa836b6dd7195699e1101cca82268"
        },
        {
          "bytes": 28,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/sdk-who.stdout",
          "role": "loaded_image",
          "sha256": "583153ddf24a3db48f4b8373cb1a5b606792fa983ca3b4c9dec380ec7a12ca65"
        }
      ],
      "value": {
        "actual_host_version": "3.7.13",
        "actual_uid_gid_capabilities": {
          "backend": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          },
          "engine": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          },
          "traefik": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          }
        },
        "engine_sha256": "c0b92692e02d2ced490f18322f9804d1cf45b81e5ed433cf28a582d024acc5ba",
        "host_sha256": "327314f5a64a9b25aba05bf83b0942ab3bfde65573cee8cc1a9e5b49d268cd63",
        "loaded_sdk": {
          "after-neighbor": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ],
          "after-target": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ],
          "before-target": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ]
        },
        "sdk_version_proof": "Actual selected image maps plus standalone WHO; the actual SDK public m_id accessor succeeds only after the same-image version guard.",
        "selected_sdk_version": "3.0.14",
        "uid": 65534
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 9141,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/build-manifest.json",
          "role": "source_manifest",
          "sha256": "af26114979ec108fb89895b304f0879729fbca8c1387430a93999c48dcb4e011"
        },
        {
          "bytes": 388,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/runtime/effective-config/traefik-native-engine.conf",
          "role": "effective_configuration",
          "sha256": "dbcac6c8463c8de10514f722daed6ac0bd7de1fb45918dc360170da37a885654"
        },
        {
          "bytes": 42212,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792008466352356234/data/prepared-product-source-equality.json",
          "role": "source_manifest",
          "sha256": "7273e38d515911dafe47eaad1362a400a7a24ed133ea945720ba28ae55b3e2f3"
        },
        {
          "bytes": 241128,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/traefik-lifecycle/execution-review/inputs-v4/source-ledger.json",
          "role": "source_manifest",
          "sha256": "1b1096c9ee964eb7981f8cabe0402ed72153e21f8c5875f9cce4b3cff818c738"
        },
        {
          "bytes": 713,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/traefik-lifecycle/execution-review/inputs-v4/fixtures/approved-product-test-overlays.json",
          "role": "source_manifest",
          "sha256": "30be4551c108b54c4b4d0cc7740cb8cc01d9637a9b185abb93636fdb6e37d83d"
        }
      ],
      "value": {
        "configurations": {
          "/task/rules.conf": "f0fa76938cc70139fb82b7504dccc6e9f7fabbd1ba9eea98fd2731312c33ed4d",
          "/task/runtime/effective-config/traefik-native-dynamic.yaml": "6cbfd89948f397486c4d7164c5264390aad8db54ed90e49ceb74280b098340d4",
          "/task/runtime/effective-config/traefik-native-engine.conf": "dbcac6c8463c8de10514f722daed6ac0bd7de1fb45918dc360170da37a885654",
          "/task/runtime/effective-config/traefik-native-static.yaml": "98b238400cb42d6e5ab00f360ece827ad6951748438a01807e05ab068b147859"
        },
        "delivery_base": "02754040bced960cfc1857416cd7101bb3116ef4",
        "private_go_overlays_scope": "two approved instrumentation overlays outside185 baseline equality scope; helper/test additions in sealed source ledger",
        "product_base": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "scoped_baseline_product_inputs_equal_a9": 185,
        "sealed_source_base": "3a1 plus v5 harness and declared private test overlays",
        "source_files": 66,
        "source_files_meaning": "66 actual native service compilation inputs",
        "spec_sha256": "a7f22e9b74022dba177e76d7b46c7ce656e1f2e9dedebe26a3d820a78ed1cf8c"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "dbcac6c8463c8de10514f722daed6ac0bd7de1fb45918dc360170da37a885654",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "f0fa76938cc70139fb82b7504dccc6e9f7fabbd1ba9eea98fd2731312c33ed4d",
    "run_id": "tf-i12-eos-20261014"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 87049,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-traefik-native-01.json",
    "sha256": "5db5f42fa062fd63f0ebbd2496dca047b1ba0ca3a16c7dea72591036cc7336e1"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::traefik-forwardauth-request::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 619,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/result.json",
          "role": "cleanup_observer",
          "sha256": "42f39d2adc66f046a74975904d95e24b26a3c9a5f99ce55c533ae8668f3e48a7"
        },
        {
          "bytes": 4580,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "a9d4c7db875c3d2cb501fb540c203c6c887608def5d278a4f595cd3d63a30ebc"
        }
      ],
      "value": {
        "driver": {
          "actual_extra_response_phases_not_transferred_to_sibling": true,
          "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
          "neighbor_health_probe_count": 1,
          "processes": {
            "backend": {
              "actual_pid": 895,
              "exit_code": 0,
              "proxy_pid": 894
            },
            "engine": {
              "actual_pid": 899,
              "exit_code": 0,
              "proxy_pid": 898
            },
            "traefik": {
              "actual_pid": 904,
              "exit_code": 0,
              "proxy_pid": 903
            }
          },
          "qualification": "unreviewed_measurements",
          "selected_case_count": 1,
          "socket_removed": true,
          "target_and_neighbor_commands_exit": 0
        },
        "observer_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 102021780317899,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 899,
          "profile": "traefik-forwardauth-request",
          "result": null,
          "run": "tf-i12-request-20261014",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 162,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792011655569723476,
          "wall_sample_end_monotonic_ns": 102021780318128
        },
        "retained_artifacts": "exact source/build/config/stage evidence retained; metadata retirement is not APR memory-free evidence"
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 171094,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "ee1b7998e954b80b9788afa3a25fad578ae281cbc1fb1b93daa989f50ac18f64"
        }
      ],
      "value": {
        "actual_common_finish_calls": 2,
        "actual_companion_session_release_calls": 1,
        "actual_native_logging_calls": 1,
        "actual_same_TU_runtime_finish_call_count": {
          "reason": "GNU --wrap does not intercept these same-TU runtime.c calls; no optional actual call-count claim. Actual native SDK logging1, Commonfinish2/idempotent, SESSIONrelease1 and completion transition1 are independently observed.",
          "value": null
        },
        "common_idempotent_calls_are_not_new_completion_transitions": true,
        "observed_public_runtime_finish_wrapper_calls": 0,
        "ordinary_runtime_finish_in_same_TU_not_claimed_intercepted": true
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 171094,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/logs/native-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "ee1b7998e954b80b9788afa3a25fad578ae281cbc1fb1b93daa989f50ac18f64"
        },
        {
          "bytes": 8400,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/logs/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "bc69d739cddf06537d92ee1f5850f0252fe10d9b8a1058b74af8df40bd020a02"
        }
      ],
      "value": {
        "actual_host_finite_framing": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 22,
            "canonical_transaction_id": null,
            "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "authorization_request_eos",
            "gid": 65534,
            "host_eos": null,
            "host_framing": {
              "buffered_body_size": 42,
              "content_length": 42,
              "remaining": 0
            },
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 102017107356358,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 899,
            "profile": "traefik-forwardauth-request",
            "result": 1,
            "run": "tf-i12-request-20261014",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 23,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792011650896761792,
            "wall_sample_end_monotonic_ns": 102017107356435
          }
        ],
        "actual_response_eos_frames": [
          {
            "elapsed_monotonic_ns": 1839309407,
            "epoch_wall_ns": 1792011649072291053,
            "fields": {
              "error": false,
              "opcode": 4,
              "payload_bytes": 0
            },
            "operation": "companion_frame_write_return",
            "pid": 904,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-fa-req-target-6c428a1e",
            "wall_ns": 1792011650911600497
          },
          {
            "elapsed_monotonic_ns": 1840108697,
            "epoch_wall_ns": 1792011649072291053,
            "fields": {
              "decision": 0,
              "error": false,
              "opcode": 4,
              "request_opcode": 4,
              "result_code": 0
            },
            "operation": "companion_result_parsed",
            "pid": 904,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-fa-req-target-6c428a1e",
            "wall_ns": 1792011650912399739
          }
        ],
        "original_shared_host_eos_and_append_argument_eos_fields": null,
        "source_boundary": "finite Content-Length loop remaining0 before actual runtime request finish; actual opResponseEOS send/parse separate"
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 171094,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "ee1b7998e954b80b9788afa3a25fad578ae281cbc1fb1b93daa989f50ac18f64"
        },
        {
          "bytes": 8400,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/logs/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "bc69d739cddf06537d92ee1f5850f0252fe10d9b8a1058b74af8df40bd020a02"
        },
        {
          "bytes": 171094,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/logs/native-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "ee1b7998e954b80b9788afa3a25fad578ae281cbc1fb1b93daa989f50ac18f64"
        }
      ],
      "value": {
        "actual_companion_session_finish": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 60,
            "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
            "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "companion_session_finish_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 5,
            "monotonic_ns": 102017122748877,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 899,
            "profile": "traefik-forwardauth-request",
            "result": 1,
            "run": "tf-i12-request-20261014",
            "runtime_eos_handoff": "companion_response_body_finish",
            "schema": "native-lifecycle-v1",
            "sequence": 67,
            "transaction_id": "tf-fa-req-target-6c428a1e",
            "transaction_id_origin": "observed_common_association",
            "uid": 65534,
            "wall_ns": 1792011650912154308,
            "wall_sample_end_monotonic_ns": 102017122748956
          }
        ],
        "actual_nested_native_eos_spans": [
          {
            "actual_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 25,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102017107386996,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 25,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650896792427,
                "wall_sample_end_monotonic_ns": 102017107387072
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 25,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102017107481462,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 1,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 26,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650896886909,
                "wall_sample_end_monotonic_ns": 102017107481554
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 27,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102017107503872,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 27,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650896909310,
                "wall_sample_end_monotonic_ns": 102017107503954
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 27,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102017107519340,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 0,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 28,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650896924771,
                "wall_sample_end_monotonic_ns": 102017107519413
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 29,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": 3,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017107,
                  "completed_phase_mask": 1,
                  "last_completed_phase": 2,
                  "response_committed": 0,
                  "status": 1
                },
                "edge": "enter",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102017107535731,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 3,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 29,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650896941162,
                "wall_sample_end_monotonic_ns": 102017107535804
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 29,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017107,
                  "completed_phase_mask": 3,
                  "last_completed_phase": 3,
                  "response_committed": 0,
                  "status": 2
                },
                "edge": "return",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102017107560384,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 3,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 0,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 30,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650896965815,
                "wall_sample_end_monotonic_ns": 102017107560458
              }
            ],
            "parent_enter": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 24,
              "canonical_transaction_id": null,
              "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 102017107371260,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 899,
              "profile": "traefik-forwardauth-request",
              "result": null,
              "run": "tf-i12-request-20261014",
              "runtime_eos_handoff": "request_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 24,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792011650896776690,
              "wall_sample_end_monotonic_ns": 102017107371335
            },
            "parent_return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 24,
              "canonical_transaction_id": null,
              "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 102017107581716,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 899,
              "profile": "traefik-forwardauth-request",
              "result": 1,
              "run": "tf-i12-request-20261014",
              "runtime_eos_handoff": "request_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 31,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792011650896987148,
              "wall_sample_end_monotonic_ns": 102017107581794
            }
          },
          {
            "actual_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 61,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017122296314,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 61,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650911701751,
                "wall_sample_end_monotonic_ns": 102017122296398
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 61,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017122652127,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 1,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 62,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650912057597,
                "wall_sample_end_monotonic_ns": 102017122652242
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 63,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017122669289,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 63,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650912074721,
                "wall_sample_end_monotonic_ns": 102017122669363
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 63,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017122691720,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 0,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 64,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650912097148,
                "wall_sample_end_monotonic_ns": 102017122691789
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 65,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": 5,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017119,
                  "completed_phase_mask": 7,
                  "last_completed_phase": 4,
                  "response_committed": 1,
                  "status": 1
                },
                "edge": "enter",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017122712091,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 5,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 65,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650912117523,
                "wall_sample_end_monotonic_ns": 102017122712164
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 65,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017122,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "return",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017122728333,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 5,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 0,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 66,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650912133762,
                "wall_sample_end_monotonic_ns": 102017122728403
              }
            ],
            "parent_enter": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 60,
              "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
              "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "enter",
              "function": "companion_session_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 5,
              "monotonic_ns": 102017122262048,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 899,
              "profile": "traefik-forwardauth-request",
              "result": null,
              "run": "tf-i12-request-20261014",
              "runtime_eos_handoff": "companion_response_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 60,
              "transaction_id": "tf-fa-req-target-6c428a1e",
              "transaction_id_origin": "observed_common_association",
              "uid": 65534,
              "wall_ns": 1792011650911667516,
              "wall_sample_end_monotonic_ns": 102017122262161
            },
            "parent_return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 60,
              "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
              "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "return",
              "function": "companion_session_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 5,
              "monotonic_ns": 102017122748877,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 899,
              "profile": "traefik-forwardauth-request",
              "result": 1,
              "run": "tf-i12-request-20261014",
              "runtime_eos_handoff": "companion_response_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 67,
              "transaction_id": "tf-fa-req-target-6c428a1e",
              "transaction_id_origin": "observed_common_association",
              "uid": 65534,
              "wall_ns": 1792011650912154308,
              "wall_sample_end_monotonic_ns": 102017122748956
            }
          },
          {
            "actual_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 69,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017122,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "enter",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017123383912,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 69,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650912789392,
                "wall_sample_end_monotonic_ns": 102017123384055
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 69,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017123,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "return",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017123416365,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 0,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 70,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650912821840,
                "wall_sample_end_monotonic_ns": 102017123416498
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 71,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017123,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "enter",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017123446267,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 71,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650912851730,
                "wall_sample_end_monotonic_ns": 102017123446392
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 71,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017123,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "return",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017123493582,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 0,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 72,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650912899052,
                "wall_sample_end_monotonic_ns": 102017123493716
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 73,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_logging",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017123533314,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 73,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650912938784,
                "wall_sample_end_monotonic_ns": 102017123533437
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 73,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_logging",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017124059858,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 1,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 74,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650913465412,
                "wall_sample_end_monotonic_ns": 102017124060078
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 75,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "native_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017124219784,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 75,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650913625266,
                "wall_sample_end_monotonic_ns": 102017124219922
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 75,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "native_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-req-target-6c428a1e",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102017124318835,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 76,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011650913724318,
                "wall_sample_end_monotonic_ns": 102017124318983
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 77,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102017123,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "enter",
                "function": "common_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 4,
                "monotonic_ns": 102017124361341,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 77,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650913766796,
                "wall_sample_end_monotonic_ns": 102017124361454
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 77,
                "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 102017124,
                  "cleanup_complete": 1,
                  "cleanup_started": 1,
                  "completed_at_ms": 102017123,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 6
                },
                "edge": "return",
                "function": "common_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 4,
                "monotonic_ns": 102017124396707,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 0,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 78,
                "transaction_id": "tf-fa-req-target-6c428a1e",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011650913802167,
                "wall_sample_end_monotonic_ns": 102017124396812
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 79,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "enter",
                "function": "companion_retired",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102017124655837,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": null,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 79,
                "transaction_id": null,
                "transaction_id_origin": "unknown",
                "uid": 65534,
                "wall_ns": 1792011650914061322,
                "wall_sample_end_monotonic_ns": 102017124655975
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 79,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
                "contract_state": null,
                "edge": "return",
                "function": "companion_retired",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 1,
                "monotonic_ns": 102017124702830,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 899,
                "profile": "traefik-forwardauth-request",
                "result": 1,
                "run": "tf-i12-request-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 80,
                "transaction_id": null,
                "transaction_id_origin": "unknown",
                "uid": 65534,
                "wall_ns": 1792011650914108285,
                "wall_sample_end_monotonic_ns": 102017124702950
              }
            ],
            "parent_enter": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 68,
              "canonical_transaction_id": "txc-000000000614a852-0000000000000000",
              "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "enter",
              "function": "companion_session_release",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 5,
              "monotonic_ns": 102017123323289,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 0,
              "pid": 899,
              "profile": "traefik-forwardauth-request",
              "result": null,
              "run": "tf-i12-request-20261014",
              "runtime_eos_handoff": null,
              "schema": "native-lifecycle-v1",
              "sequence": 68,
              "transaction_id": "tf-fa-req-target-6c428a1e",
              "transaction_id_origin": "observed_common_association",
              "uid": 65534,
              "wall_ns": 1792011650912728831,
              "wall_sample_end_monotonic_ns": 102017123323512
            },
            "parent_return": {
              "allocation_join_verified": false,
              "allocation_scope_call": null,
              "allocation_scope_kind": null,
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 68,
              "canonical_transaction_id": null,
              "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
              "contract_state": null,
              "edge": "return",
              "function": "companion_session_release",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 0,
              "monotonic_ns": 102017124835808,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 0,
              "pid": 899,
              "profile": "traefik-forwardauth-request",
              "result": 1,
              "run": "tf-i12-request-20261014",
              "runtime_eos_handoff": null,
              "schema": "native-lifecycle-v1",
              "sequence": 81,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792011650914241293,
              "wall_sample_end_monotonic_ns": 102017124835961
            }
          }
        ],
        "actual_request_runtime_finish": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 24,
            "canonical_transaction_id": null,
            "case": "I12::traefik-forwardauth-request::NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finish_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 102017107581716,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 899,
            "profile": "traefik-forwardauth-request",
            "result": 1,
            "run": "tf-i12-request-20261014",
            "runtime_eos_handoff": "request_body_finish",
            "schema": "native-lifecycle-v1",
            "sequence": 31,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792011650896987148,
            "wall_sample_end_monotonic_ns": 102017107581794
          }
        ],
        "native_append_eos_argument": "N/A: selected APIs have no EOS argument",
        "ordinary_same_TU_runtime_finish_response_body_not_claimed_intercepted": true
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 171094,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "ee1b7998e954b80b9788afa3a25fad578ae281cbc1fb1b93daa989f50ac18f64"
        }
      ],
      "value": {
        "actual_cleanup_calls": 1
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2766,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/before-target.json",
          "role": "loaded_image",
          "sha256": "37908c9db4c0cc70822cbf0e3c069c3e01a5d8d0929fc0a0410ee655f95c2e0b"
        },
        {
          "bytes": 4580,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "a9d4c7db875c3d2cb501fb540c203c6c887608def5d278a4f595cd3d63a30ebc"
        }
      ],
      "value": {
        "actual_host_version": "3.7.13",
        "actual_uid_gid_capabilities": {
          "backend": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          },
          "engine": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          },
          "traefik": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          }
        },
        "engine_sha256": "5acdaedc226b94ff5dff6af1d739a373fde8d87898047348553372922b008aad",
        "host_sha256": "327314f5a64a9b25aba05bf83b0942ab3bfde65573cee8cc1a9e5b49d268cd63",
        "loaded_sdk": {
          "after-neighbor": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ],
          "after-target": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ],
          "before-target": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ]
        },
        "uid": 65534
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 11052,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/build-manifest.json",
          "role": "source_manifest",
          "sha256": "0fc4a837e873a5765b19811dbc4fb8a396d87a989e7c7010db86ddd5579bd9c9"
        },
        {
          "bytes": 386,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/runtime/effective-config/traefik-forwardauth.conf",
          "role": "effective_configuration",
          "sha256": "8461fbacb3f11f2ce6814964913468c82f386d54782e3f723555fc04c6fac8d0"
        },
        {
          "bytes": 42212,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/prepared-product-source-equality.json",
          "role": "source_manifest",
          "sha256": "6fb6b2986f5348805fe08ea2bc39e41748e617471f34d54709030a2057c8adc1"
        },
        {
          "bytes": 638,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011523429119983/data/approved-product-test-overlays.json",
          "role": "source_manifest",
          "sha256": "ab69810e2be4c96421f6b2b8640f646826ed71ee2fa51e5324b96b735a035f0d"
        },
        {
          "bytes": 241128,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/traefik-forwardauth-lifecycle/source-ledger-v1.json",
          "role": "source_manifest",
          "sha256": "650ddd1cb029828e996a7ce1c3b4e1d0da53f72cf74d9a5df49f71a895ad77b3"
        },
        {
          "bytes": 116,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-readonly-revisions-01.json",
          "role": "source_manifest",
          "sha256": "7626580d3e02904f25e1ebc03852abab8596c3d78cf092a2e3b2658f5514a0cf"
        }
      ],
      "value": {
        "actual_native_compilation_input_count": 69,
        "configurations": {
          "/task/rules.conf": "b8841d0f41877d73158a7e99f2c7d7d71c6c8b98624abe9968ffe2b958d7b251",
          "/task/runtime/effective-config/traefik-forwardauth-dynamic.yaml": "66109a5b8b8cf4a34f85e23bd682017786a85817adc03972fde54d9defd1d303",
          "/task/runtime/effective-config/traefik-forwardauth.conf": "8461fbacb3f11f2ce6814964913468c82f386d54782e3f723555fc04c6fac8d0"
        },
        "delivery_base": "02754040bced960cfc1857416cd7101bb3116ef4",
        "explicit_overlay_rows": [
          {
            "expected": "7f1544f1f36042c68359c7caed7d5dc4ce8cc77d44282debdc3955ea725a5e9c",
            "observed": "64b124e36358f0341446aa56aecf987d44f1cfe7f213d247412ffd368174d588",
            "path": "common/runtime/http_authorization_service.c"
          },
          {
            "expected": "0fa85f5658be96a25204adf489b2e18149a5f826b5ed528e55ec7b2ffe410aa4",
            "observed": "0e2484f610347462c315f30ac65b4227a1cdb8fb0f4a2f8f9535ce406c44ec63",
            "path": "common/runtime/msconnector_runtime.c"
          }
        ],
        "git_source_base": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness; declared private test overlays",
        "product_base": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "scoped_a9_baseline_input_count": 185,
        "sealed_source_base": "3a1 plus v5 harness and declared private test overlays",
        "source_files": 69,
        "spec_sha256": "55b5a7260b9c327ca7449678f372f6d2e053da4d69d75a880d75e263606f9458"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8461fbacb3f11f2ce6814964913468c82f386d54782e3f723555fc04c6fac8d0",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "b8841d0f41877d73158a7e99f2c7d7d71c6c8b98624abe9968ffe2b958d7b251",
    "run_id": "tf-i12-request-20261014"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 200902,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-forwardauth-request-01.json",
    "sha256": "aa2d18e292bb6f6aa8f1d3877c36f6afdecda14e701ad15f21842cf925e00697"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::traefik-forwardauth-response-companion::NEED-observer-response-eos

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 635,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/result.json",
          "role": "cleanup_observer",
          "sha256": "622158dac3582908d5342476e3c5e3467601a1815e2ba339e3f9f53e4f682b11"
        },
        {
          "bytes": 4592,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "d4bc61afb638781444a47f1f2cc2971cc279168099f5000298e6edc2512c476d"
        }
      ],
      "value": {
        "driver": {
          "actual_extra_response_phases_not_transferred_to_sibling": true,
          "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
          "neighbor_health_probe_count": 1,
          "processes": {
            "backend": {
              "actual_pid": 894,
              "exit_code": 0,
              "proxy_pid": 893
            },
            "engine": {
              "actual_pid": 898,
              "exit_code": 0,
              "proxy_pid": 897
            },
            "traefik": {
              "actual_pid": 903,
              "exit_code": 0,
              "proxy_pid": 902
            }
          },
          "qualification": "unreviewed_measurements",
          "selected_case_count": 1,
          "socket_removed": true,
          "target_and_neighbor_commands_exit": 0
        },
        "observer_final": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 102008827577427,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 898,
          "profile": "traefik-forwardauth-response-companion",
          "result": null,
          "run": "tf-i12-companion-20261014",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 162,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792011642616982934,
          "wall_sample_end_monotonic_ns": 102008827577582
        },
        "retained_artifacts": "exact source/build/config/stage evidence retained; metadata retirement is not APR memory-free evidence"
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 175792,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "caf2acb8bded3357408950644910db57ecae9a58ee0054178d7d6d198afd6b9b"
        }
      ],
      "value": {
        "actual_common_finish_calls": 2,
        "actual_companion_session_release_calls": 1,
        "actual_native_logging_calls": 1,
        "actual_same_TU_runtime_finish_call_count": {
          "reason": "GNU --wrap does not intercept these same-TU runtime.c calls; no optional actual call-count claim. Actual native SDK logging1, Commonfinish2/idempotent, SESSIONrelease1 and completion transition1 are independently observed.",
          "value": null
        },
        "common_idempotent_calls_are_not_new_completion_transitions": true,
        "observed_public_runtime_finish_wrapper_calls": 0,
        "ordinary_runtime_finish_in_same_TU_not_claimed_intercepted": true
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 175792,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/logs/native-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "caf2acb8bded3357408950644910db57ecae9a58ee0054178d7d6d198afd6b9b"
        },
        {
          "bytes": 8400,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/logs/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "2c4c4a337f14a356ba907c6b4a104cb09ad581fe9be617ae8fababc8ba727074"
        }
      ],
      "value": {
        "actual_host_finite_framing": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 22,
            "canonical_transaction_id": null,
            "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
            "contract_state": null,
            "edge": "return",
            "function": "authorization_request_eos",
            "gid": 65534,
            "host_eos": null,
            "host_framing": {
              "buffered_body_size": 42,
              "content_length": 42,
              "remaining": 0
            },
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 102003806925670,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 898,
            "profile": "traefik-forwardauth-response-companion",
            "result": 1,
            "run": "tf-i12-companion-20261014",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 23,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792011637596331107,
            "wall_sample_end_monotonic_ns": 102003806925752
          }
        ],
        "actual_response_eos_frames": [
          {
            "elapsed_monotonic_ns": 1854573316,
            "epoch_wall_ns": 1792011635752449108,
            "fields": {
              "error": false,
              "opcode": 4,
              "payload_bytes": 0
            },
            "operation": "companion_frame_write_return",
            "pid": 903,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-fa-cmp-target-21f603ab",
            "wall_ns": 1792011637607022466
          },
          {
            "elapsed_monotonic_ns": 1855322171,
            "epoch_wall_ns": 1792011635752449108,
            "fields": {
              "decision": 0,
              "error": false,
              "opcode": 4,
              "request_opcode": 4,
              "result_code": 0
            },
            "operation": "companion_result_parsed",
            "pid": 903,
            "schema": "traefik-host-observed-v1",
            "transaction_id": "tf-fa-cmp-target-21f603ab",
            "wall_ns": 1792011637607771297
          }
        ],
        "original_shared_host_eos_and_append_argument_eos_fields": null,
        "source_boundary": "finite Content-Length loop remaining0 before actual runtime request finish; actual opResponseEOS send/parse separate"
      }
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 175792,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "caf2acb8bded3357408950644910db57ecae9a58ee0054178d7d6d198afd6b9b"
        },
        {
          "bytes": 8400,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/logs/host-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "2c4c4a337f14a356ba907c6b4a104cb09ad581fe9be617ae8fababc8ba727074"
        },
        {
          "bytes": 175792,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/logs/native-lifecycle.jsonl",
          "role": "host_callback",
          "sha256": "caf2acb8bded3357408950644910db57ecae9a58ee0054178d7d6d198afd6b9b"
        }
      ],
      "value": {
        "actual_companion_session_finish": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 60,
            "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
            "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
            "contract_state": null,
            "edge": "return",
            "function": "companion_session_finish_response_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 5,
            "monotonic_ns": 102003818195991,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 4,
            "pid": 898,
            "profile": "traefik-forwardauth-response-companion",
            "result": 1,
            "run": "tf-i12-companion-20261014",
            "runtime_eos_handoff": "companion_response_body_finish",
            "schema": "native-lifecycle-v1",
            "sequence": 67,
            "transaction_id": "tf-fa-cmp-target-21f603ab",
            "transaction_id_origin": "observed_common_association",
            "uid": 65534,
            "wall_ns": 1792011637607601423,
            "wall_sample_end_monotonic_ns": 102003818196067
          }
        ],
        "actual_nested_native_eos_spans": [
          {
            "actual_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 25,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102003806974813,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 25,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637596380254,
                "wall_sample_end_monotonic_ns": 102003806974900
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 25,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_request_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102003807110948,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 2,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 1,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 26,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637596516446,
                "wall_sample_end_monotonic_ns": 102003807111091
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 27,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "enter",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102003807129445,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 27,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637596534887,
                "wall_sample_end_monotonic_ns": 102003807129532
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 27,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "return",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102003807145133,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 0,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 28,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637596550566,
                "wall_sample_end_monotonic_ns": 102003807145217
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 29,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": 3,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003806,
                  "completed_phase_mask": 1,
                  "last_completed_phase": 2,
                  "response_committed": 0,
                  "status": 1
                },
                "edge": "enter",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102003807174683,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 3,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 29,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637596580117,
                "wall_sample_end_monotonic_ns": 102003807174757
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 29,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003807,
                  "completed_phase_mask": 3,
                  "last_completed_phase": 3,
                  "response_committed": 0,
                  "status": 2
                },
                "edge": "return",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102003807199546,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 3,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 0,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 30,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637596604995,
                "wall_sample_end_monotonic_ns": 102003807199637
              }
            ],
            "parent_enter": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 24,
              "canonical_transaction_id": null,
              "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
              "contract_state": null,
              "edge": "enter",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 102003806940076,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 898,
              "profile": "traefik-forwardauth-response-companion",
              "result": null,
              "run": "tf-i12-companion-20261014",
              "runtime_eos_handoff": "request_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 24,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792011637596345512,
              "wall_sample_end_monotonic_ns": 102003806940156
            },
            "parent_return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 24,
              "canonical_transaction_id": null,
              "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
              "contract_state": null,
              "edge": "return",
              "function": "runtime_finish_request_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 3,
              "monotonic_ns": 102003807216644,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 2,
              "pid": 898,
              "profile": "traefik-forwardauth-response-companion",
              "result": 1,
              "run": "tf-i12-companion-20261014",
              "runtime_eos_handoff": "request_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 31,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792011637596622079,
              "wall_sample_end_monotonic_ns": 102003807216721
            }
          },
          {
            "actual_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 61,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003817674415,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 61,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637607079847,
                "wall_sample_end_monotonic_ns": 102003817674490
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 61,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_response_body",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818074922,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 4,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 1,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 62,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637607480500,
                "wall_sample_end_monotonic_ns": 102003818075163
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 63,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "enter",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818103335,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 63,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637607508792,
                "wall_sample_end_monotonic_ns": 102003818103433
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 63,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "return",
                "function": "native_intervention",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818128412,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 0,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 64,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637607533849,
                "wall_sample_end_monotonic_ns": 102003818128493
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 65,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": 5,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003814,
                  "completed_phase_mask": 7,
                  "last_completed_phase": 4,
                  "response_committed": 1,
                  "status": 1
                },
                "edge": "enter",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818146550,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 5,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 65,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637607551982,
                "wall_sample_end_monotonic_ns": 102003818146625
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 65,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003818,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "return",
                "function": "common_complete_phase",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818170886,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 5,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 0,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 66,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637607576346,
                "wall_sample_end_monotonic_ns": 102003818170986
              }
            ],
            "parent_enter": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 60,
              "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
              "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
              "contract_state": null,
              "edge": "enter",
              "function": "companion_session_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 5,
              "monotonic_ns": 102003817627460,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 898,
              "profile": "traefik-forwardauth-response-companion",
              "result": null,
              "run": "tf-i12-companion-20261014",
              "runtime_eos_handoff": "companion_response_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 60,
              "transaction_id": "tf-fa-cmp-target-21f603ab",
              "transaction_id_origin": "observed_common_association",
              "uid": 65534,
              "wall_ns": 1792011637607032935,
              "wall_sample_end_monotonic_ns": 102003817627582
            },
            "parent_return": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 60,
              "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
              "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
              "contract_state": null,
              "edge": "return",
              "function": "companion_session_finish_response_body",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 5,
              "monotonic_ns": 102003818195991,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 4,
              "pid": 898,
              "profile": "traefik-forwardauth-response-companion",
              "result": 1,
              "run": "tf-i12-companion-20261014",
              "runtime_eos_handoff": "companion_response_body_finish",
              "schema": "native-lifecycle-v1",
              "sequence": 67,
              "transaction_id": "tf-fa-cmp-target-21f603ab",
              "transaction_id_origin": "observed_common_association",
              "uid": 65534,
              "wall_ns": 1792011637607601423,
              "wall_sample_end_monotonic_ns": 102003818196067
            }
          },
          {
            "actual_nested_rows": [
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 69,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003818,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "enter",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818793096,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 69,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637608198534,
                "wall_sample_end_monotonic_ns": 102003818793177
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 69,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003818,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "return",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818826091,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 0,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 70,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637608231558,
                "wall_sample_end_monotonic_ns": 102003818826200
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 71,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003818,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "enter",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818855739,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 71,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637608261173,
                "wall_sample_end_monotonic_ns": 102003818855816
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 71,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003818,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "return",
                "function": "common_finish",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818872448,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 0,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 72,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637608277880,
                "wall_sample_end_monotonic_ns": 102003818872524
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 73,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "enter",
                "function": "native_process_logging",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003818894677,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 73,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637608300114,
                "wall_sample_end_monotonic_ns": 102003818894756
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 73,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "return",
                "function": "native_process_logging",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003819224279,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 1,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 74,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637608629849,
                "wall_sample_end_monotonic_ns": 102003819224509
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 75,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "enter",
                "function": "native_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003819341063,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 75,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637608746500,
                "wall_sample_end_monotonic_ns": 102003819341145
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 75,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "return",
                "function": "native_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": "tf-fa-cmp-target-21f603ab",
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 5,
                "monotonic_ns": 102003819395268,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 76,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "sdk_public_m_id",
                "uid": 65534,
                "wall_ns": 1792011637608800731,
                "wall_sample_end_monotonic_ns": 102003819395378
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 77,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 0,
                  "cleanup_complete": 0,
                  "cleanup_started": 0,
                  "completed_at_ms": 102003818,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 3
                },
                "edge": "enter",
                "function": "common_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 4,
                "monotonic_ns": 102003819438345,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 77,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637608843778,
                "wall_sample_end_monotonic_ns": 102003819438422
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 77,
                "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": {
                  "active_phase": -1,
                  "cleanup_at_ms": 102003819,
                  "cleanup_complete": 1,
                  "cleanup_started": 1,
                  "completed_at_ms": 102003818,
                  "completed_phase_mask": 15,
                  "last_completed_phase": 5,
                  "response_committed": 1,
                  "status": 6
                },
                "edge": "return",
                "function": "common_cleanup",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 4,
                "monotonic_ns": 102003819461999,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 0,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 78,
                "transaction_id": "tf-fa-cmp-target-21f603ab",
                "transaction_id_origin": "common_public_contract",
                "uid": 65534,
                "wall_ns": 1792011637608867443,
                "wall_sample_end_monotonic_ns": 102003819462086
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 79,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "enter",
                "function": "companion_retired",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 3,
                "monotonic_ns": 102003819661073,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": null,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 79,
                "transaction_id": null,
                "transaction_id_origin": "unknown",
                "uid": 65534,
                "wall_ns": 1792011637609066507,
                "wall_sample_end_monotonic_ns": 102003819661151
              },
              {
                "allocation_join_verified": true,
                "allocation_scope_call": 2,
                "allocation_scope_kind": "runtime",
                "argument_committed": null,
                "argument_eos": null,
                "argument_response_status": null,
                "call": 79,
                "canonical_transaction_id": null,
                "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
                "contract_state": null,
                "edge": "return",
                "function": "companion_retired",
                "gid": 65534,
                "host_eos": null,
                "host_framing": null,
                "input_kind": null,
                "input_size": null,
                "input_transaction_id": null,
                "intervention_disruptive": null,
                "intervention_status": null,
                "invalid": false,
                "live_mappings": 1,
                "monotonic_ns": 102003819679882,
                "native_mime_selection": null,
                "pending_calls": 2,
                "phase": 0,
                "pid": 898,
                "profile": "traefik-forwardauth-response-companion",
                "result": 1,
                "run": "tf-i12-companion-20261014",
                "runtime_eos_handoff": null,
                "schema": "native-lifecycle-v1",
                "sequence": 80,
                "transaction_id": null,
                "transaction_id_origin": "unknown",
                "uid": 65534,
                "wall_ns": 1792011637609085314,
                "wall_sample_end_monotonic_ns": 102003819679957
              }
            ],
            "parent_enter": {
              "allocation_join_verified": true,
              "allocation_scope_call": 2,
              "allocation_scope_kind": "runtime",
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 68,
              "canonical_transaction_id": "txc-000000000614745d-0000000000000000",
              "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
              "contract_state": null,
              "edge": "enter",
              "function": "companion_session_release",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 5,
              "monotonic_ns": 102003818737296,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 0,
              "pid": 898,
              "profile": "traefik-forwardauth-response-companion",
              "result": null,
              "run": "tf-i12-companion-20261014",
              "runtime_eos_handoff": null,
              "schema": "native-lifecycle-v1",
              "sequence": 68,
              "transaction_id": "tf-fa-cmp-target-21f603ab",
              "transaction_id_origin": "observed_common_association",
              "uid": 65534,
              "wall_ns": 1792011637608142783,
              "wall_sample_end_monotonic_ns": 102003818737430
            },
            "parent_return": {
              "allocation_join_verified": false,
              "allocation_scope_call": null,
              "allocation_scope_kind": null,
              "argument_committed": null,
              "argument_eos": null,
              "argument_response_status": null,
              "call": 68,
              "canonical_transaction_id": null,
              "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
              "contract_state": null,
              "edge": "return",
              "function": "companion_session_release",
              "gid": 65534,
              "host_eos": null,
              "host_framing": null,
              "input_kind": null,
              "input_size": null,
              "input_transaction_id": null,
              "intervention_disruptive": null,
              "intervention_status": null,
              "invalid": false,
              "live_mappings": 0,
              "monotonic_ns": 102003819796099,
              "native_mime_selection": null,
              "pending_calls": 1,
              "phase": 0,
              "pid": 898,
              "profile": "traefik-forwardauth-response-companion",
              "result": 1,
              "run": "tf-i12-companion-20261014",
              "runtime_eos_handoff": null,
              "schema": "native-lifecycle-v1",
              "sequence": 81,
              "transaction_id": null,
              "transaction_id_origin": "unknown",
              "uid": 65534,
              "wall_ns": 1792011637609201576,
              "wall_sample_end_monotonic_ns": 102003819796219
            }
          }
        ],
        "actual_request_runtime_finish": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 24,
            "canonical_transaction_id": null,
            "case": "I12::traefik-forwardauth-response-companion::NEED-observer-response-eos",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finish_request_body",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 102003807216644,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 2,
            "pid": 898,
            "profile": "traefik-forwardauth-response-companion",
            "result": 1,
            "run": "tf-i12-companion-20261014",
            "runtime_eos_handoff": "request_body_finish",
            "schema": "native-lifecycle-v1",
            "sequence": 31,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792011637596622079,
            "wall_sample_end_monotonic_ns": 102003807216721
          }
        ],
        "native_append_eos_argument": "N/A: selected APIs have no EOS argument",
        "ordinary_same_TU_runtime_finish_response_body_not_claimed_intercepted": true
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 175792,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/logs/native-lifecycle.jsonl",
          "role": "native_api",
          "sha256": "caf2acb8bded3357408950644910db57ecae9a58ee0054178d7d6d198afd6b9b"
        }
      ],
      "value": {
        "actual_cleanup_calls": 1
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 2766,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/before-target.json",
          "role": "loaded_image",
          "sha256": "ec238c0232ab6ef19442dbe6f724fd01c037f398d34dc15292481872e0f8e3f8"
        },
        {
          "bytes": 4592,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "d4bc61afb638781444a47f1f2cc2971cc279168099f5000298e6edc2512c476d"
        }
      ],
      "value": {
        "actual_host_version": "3.7.13",
        "actual_uid_gid_capabilities": {
          "backend": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          },
          "engine": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          },
          "traefik": {
            "CapBnd": "0000000000000000",
            "CapEff": "0000000000000000",
            "Gid": "65534\t65534\t65534\t65534",
            "NoNewPrivs": "1",
            "Uid": "65534\t65534\t65534\t65534"
          }
        },
        "engine_sha256": "5acdaedc226b94ff5dff6af1d739a373fde8d87898047348553372922b008aad",
        "host_sha256": "327314f5a64a9b25aba05bf83b0942ab3bfde65573cee8cc1a9e5b49d268cd63",
        "loaded_sdk": {
          "after-neighbor": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ],
          "after-target": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ],
          "before-target": [
            {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            }
          ]
        },
        "uid": 65534
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 11070,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/build-manifest.json",
          "role": "source_manifest",
          "sha256": "097b8e347afd02bb3e847672705fbc846d6192224b8fca0d4748cf0d80c5d676"
        },
        {
          "bytes": 386,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/runtime/effective-config/traefik-forwardauth.conf",
          "role": "effective_configuration",
          "sha256": "8461fbacb3f11f2ce6814964913468c82f386d54782e3f723555fc04c6fac8d0"
        },
        {
          "bytes": 42212,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/prepared-product-source-equality.json",
          "role": "source_manifest",
          "sha256": "6fb6b2986f5348805fe08ea2bc39e41748e617471f34d54709030a2057c8adc1"
        },
        {
          "bytes": 638,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792011525790054951/data/approved-product-test-overlays.json",
          "role": "source_manifest",
          "sha256": "ab69810e2be4c96421f6b2b8640f646826ed71ee2fa51e5324b96b735a035f0d"
        },
        {
          "bytes": 241128,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/traefik-forwardauth-lifecycle/source-ledger-v1.json",
          "role": "source_manifest",
          "sha256": "650ddd1cb029828e996a7ce1c3b4e1d0da53f72cf74d9a5df49f71a895ad77b3"
        },
        {
          "bytes": 116,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-readonly-revisions-01.json",
          "role": "source_manifest",
          "sha256": "7626580d3e02904f25e1ebc03852abab8596c3d78cf092a2e3b2658f5514a0cf"
        }
      ],
      "value": {
        "actual_native_compilation_input_count": 69,
        "configurations": {
          "/task/rules.conf": "80b2750b005a6d26431a0034917990764a8258a4ff51cbda4d5354c5c1c55984",
          "/task/runtime/effective-config/traefik-forwardauth-dynamic.yaml": "60563b8d5ba3090998c757e0a60605c91923cef804cb656a7f75730b028ed352",
          "/task/runtime/effective-config/traefik-forwardauth.conf": "8461fbacb3f11f2ce6814964913468c82f386d54782e3f723555fc04c6fac8d0"
        },
        "delivery_base": "02754040bced960cfc1857416cd7101bb3116ef4",
        "explicit_overlay_rows": [
          {
            "expected": "7f1544f1f36042c68359c7caed7d5dc4ce8cc77d44282debdc3955ea725a5e9c",
            "observed": "64b124e36358f0341446aa56aecf987d44f1cfe7f213d247412ffd368174d588",
            "path": "common/runtime/http_authorization_service.c"
          },
          {
            "expected": "0fa85f5658be96a25204adf489b2e18149a5f826b5ed528e55ec7b2ffe410aa4",
            "observed": "0e2484f610347462c315f30ac65b4227a1cdb8fb0f4a2f8f9535ce406c44ec63",
            "path": "common/runtime/msconnector_runtime.c"
          }
        ],
        "git_source_base": "3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness; declared private test overlays",
        "product_base": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "scoped_a9_baseline_input_count": 185,
        "sealed_source_base": "3a1 plus v5 harness and declared private test overlays",
        "source_files": 69,
        "spec_sha256": "a9e0e4d01ed67895c81464db6850336bbcc7507503960b224a057311b1e8d843"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8461fbacb3f11f2ce6814964913468c82f386d54782e3f723555fc04c6fac8d0",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "3a1bafecd0c38ccf20427d580c767ed42addf4aa",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "80b2750b005a6d26431a0034917990764a8258a4ff51cbda4d5354c5c1c55984",
    "run_id": "tf-i12-companion-20261014"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 203512,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-forwardauth-companion-01.json",
    "sha256": "a0ca427eb3e14374b33ef0ac10d11bc80dddda3ce0c8db9a0ca8c3d9f9864cae"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::lighttpd-stock-sidecar::NEED-request-empty

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1534,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/execution-receipt.json",
          "role": "cleanup_observer",
          "sha256": "bc70c9969b754f2b5b8befd7ff6f7e6d2497bd585364667b4a0f7364fda368f1"
        },
        {
          "bytes": 4538,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "30b3fc49cfd39aad031d31fffe147039c6fa39d2e5b84ae881fc4f3b316044b7"
        }
      ],
      "value": {
        "actual_host_final": [],
        "actual_process_cleanup": [
          {
            "actor": "sidecar",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 308,
            "actual_launcher_starttime": "10641782",
            "actual_return_code": 143,
            "launcher_reaped": true,
            "native_pid": 309,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10641783"
          },
          {
            "actor": "host",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 304,
            "actual_launcher_starttime": "10641777",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 305,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10641778"
          },
          {
            "actor": "backend",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 296,
            "actual_launcher_starttime": "10641352",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 297,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10641353"
          }
        ],
        "all_scopes_cleanup_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 59,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "lighttpd-stock-sidecar-main",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106417963096230,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 60,
            "transaction_id": "lighttpd-stock-sidecar-main",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016051752501687,
            "wall_sample_end_monotonic_ns": 106417963096333
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 61,
            "canonical_transaction_id": "txc-000000000657cf21-0000000000000000",
            "case": "NEED-request-empty",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 106417963,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "completed_at_ms": 106417962,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 6
            },
            "edge": "return",
            "function": "common_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 2,
            "monotonic_ns": 106417963158569,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 0,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 62,
            "transaction_id": "lighttpd-stock-sidecar-main",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016051752564014,
            "wall_sample_end_monotonic_ns": 106417963158661
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 52,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finalize_and_snapshot",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 106417963422950,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 1,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": {
              "association_retired": 1,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "finished": 1,
              "handle_cleared": 1,
              "status": 6
            },
            "schema": "native-lifecycle-v1",
            "sequence": 63,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016051752828428,
            "wall_sample_end_monotonic_ns": 106417963423076
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 64,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 106417963541618,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 65,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016051752947073,
            "wall_sample_end_monotonic_ns": 106417963541718
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 66,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 123,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "lighttpd-stock-sidecar-neighbor",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106418774750524,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 124,
            "transaction_id": "lighttpd-stock-sidecar-neighbor",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016052564155998,
            "wall_sample_end_monotonic_ns": 106418774750642
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 66,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 125,
            "canonical_transaction_id": "txc-000000000657d252-0000000000000002",
            "case": "NEED-request-empty",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 106418774,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "completed_at_ms": 106418774,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 1,
              "status": 6
            },
            "edge": "return",
            "function": "common_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 2,
            "monotonic_ns": 106418774805259,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 0,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 126,
            "transaction_id": "lighttpd-stock-sidecar-neighbor",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016052564210704,
            "wall_sample_end_monotonic_ns": 106418774805349
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 66,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 116,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finalize_and_snapshot",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 106418775075172,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 1,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": {
              "association_retired": 1,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "finished": 1,
              "handle_cleared": 1,
              "status": 6
            },
            "schema": "native-lifecycle-v1",
            "sequence": 127,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016052564480655,
            "wall_sample_end_monotonic_ns": 106418775075306
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 128,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 106418775189310,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 129,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016052564594754,
            "wall_sample_end_monotonic_ns": 106418775189400
          }
        ],
        "last_actual_host_api": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 128,
          "canonical_transaction_id": null,
          "case": "NEED-request-empty",
          "contract_state": null,
          "edge": "return",
          "function": "runtime_destroy",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106418775189310,
          "native_mime_selection": null,
          "pending_calls": 1,
          "phase": 0,
          "pid": 309,
          "profile": "lighttpd-stock-sidecar",
          "result": null,
          "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
          "runtime_eos_handoff": null,
          "runtime_finalize_snapshot": null,
          "schema": "native-lifecycle-v1",
          "sequence": 129,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016052564594754,
          "wall_sample_end_monotonic_ns": 106418775189400
        },
        "stock_observer_mapping_gap": false
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 140011,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "25e2bb3e3bb0a89b2d9d16bf281bff213e92c787e3748edd15790d641a89e4ce"
        }
      ],
      "value": {
        "actual_finalize_and_snapshot_calls": 1,
        "common_finish_calls": 2,
        "external_runtime_finish_calls": 0,
        "native_logging_calls": 1,
        "stock_finalize_and_snapshot_not_wrapped": false
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1144,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "bee5b1a73627f2405fd7196d39b202d0f0205c5c42ec3c0938f18cc1c666acdd"
        }
      ],
      "value": [
        {
          "actual_eos_argument": 1,
          "entity_length": 0,
          "gid": 65534,
          "input_size": 0,
          "invalid": false,
          "kind": "stock_request_content_length_eos",
          "monotonic_ns": 106417954292974,
          "pid": 309,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 1,
          "stream_offset": 0,
          "uid": 65534
        },
        {
          "actual_eos_argument": 1,
          "entity_length": 24,
          "gid": 65534,
          "input_size": 0,
          "invalid": false,
          "kind": "stock_response_content_length_eos",
          "monotonic_ns": 106417962242960,
          "pid": 309,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 2,
          "stream_offset": 24,
          "uid": 65534
        }
      ]
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1144,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "bee5b1a73627f2405fd7196d39b202d0f0205c5c42ec3c0938f18cc1c666acdd"
        },
        {
          "bytes": 140011,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "25e2bb3e3bb0a89b2d9d16bf281bff213e92c787e3748edd15790d641a89e4ce"
        }
      ],
      "value": {
        "actual_empty_request_boundary": [
          {
            "actual_eos_argument": 1,
            "entity_length": 0,
            "gid": 65534,
            "input_size": 0,
            "invalid": false,
            "kind": "stock_request_content_length_eos",
            "monotonic_ns": 106417954292974,
            "pid": 309,
            "runtime_allocation_scope_call": 2,
            "schema": "lighttpd-physical-host-v1",
            "sequence": 1,
            "stream_offset": 0,
            "uid": 65534
          }
        ],
        "definition": "Actual accepted native patched eos argument, or actual finite Content-Length consumed branch, plus same typed Runtime/native finalization calls.",
        "native_append_eos_argument": null,
        "native_request_finalization": 1,
        "native_response_finalization": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 140011,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "25e2bb3e3bb0a89b2d9d16bf281bff213e92c787e3748edd15790d641a89e4ce"
        }
      ],
      "value": {
        "actual_finalize_snapshot_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 52,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finalize_and_snapshot",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 106417963422950,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 1,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": {
              "association_retired": 1,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "finished": 1,
              "handle_cleared": 1,
              "status": 6
            },
            "schema": "native-lifecycle-v1",
            "sequence": 63,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016051752828428,
            "wall_sample_end_monotonic_ns": 106417963423076
          }
        ],
        "common_cleanup": 1,
        "native_cleanup": 1,
        "runtime_free_correlation_known": true,
        "typed_runtime_destroy": 0,
        "unjoined_external_destroy_rows": [
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 64,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "enter",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 106417963517284,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 64,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016051752922764,
            "wall_sample_end_monotonic_ns": 106417963517419
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 64,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 106417963541618,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 65,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016051752947073,
            "wall_sample_end_monotonic_ns": 106417963541718
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 128,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "enter",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 106418775165166,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 128,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016052564570644,
            "wall_sample_end_monotonic_ns": 106418775165295
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 128,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 106418775189310,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 129,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016052564594754,
            "wall_sample_end_monotonic_ns": 106418775189400
          }
        ]
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 17209,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/receipts/before-main/backend.maps",
          "role": "loaded_image",
          "sha256": "fae197822d97bb79f1c67564ddb40ec27a3d06db307c51a67b2ebf0bb6f9e1b6"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/receipts/before-main/backend.status",
          "role": "loaded_image",
          "sha256": "8f2688421d44cf402c18e5a03b53c3f87d74002aae6191cf62d794fb5e002bdc"
        },
        {
          "bytes": 4263,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/receipts/before-main/host.maps",
          "role": "loaded_image",
          "sha256": "d586d7d9c78f362c98e93592df899758f25037869167355a0a6764ff182d9c2a"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/receipts/before-main/host.status",
          "role": "loaded_image",
          "sha256": "8fee6ad2575a192726a5eb8621e0dce7d8faa67a9d9de28e33f137b22a0af699"
        },
        {
          "bytes": 27946,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/receipts/before-main/sidecar.maps",
          "role": "loaded_image",
          "sha256": "63f00416052709a612fd6591d7f1d4c80b52b6f535418878bebd742e38a0bbf1"
        },
        {
          "bytes": 1505,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/receipts/before-main/sidecar.status",
          "role": "loaded_image",
          "sha256": "8ae1bbccc5986a3b2f6948bafae349bcbdb97d99f69ca37e47075abcbd33efb0"
        },
        {
          "bytes": 4538,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "30b3fc49cfd39aad031d31fffe147039c6fa39d2e5b84ae881fc4f3b316044b7"
        },
        {
          "bytes": 448216,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/owned/stock-host/bin/lighttpd",
          "role": "loaded_image",
          "sha256": "5746e51d8d3e6a825886b334741c0998940587c2ffc536181da894bc4045ee56"
        },
        {
          "bytes": 352040,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
          "role": "loaded_image",
          "sha256": "c0ccfd0293324d610f4bd98fb6cf0bfce37a9026c8a01c32a7e3e566b61b0c4a"
        },
        {
          "bytes": 2034032,
          "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "role": "loaded_image",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        }
      ],
      "value": {
        "actual_actors": {
          "backend": {
            "actual_launcher_pid": 296,
            "actual_launcher_starttime": "10641352",
            "argv": [
              "rtk",
              "proxy",
              "/usr/local/bin/python3",
              "/mnt/fixtures/backend-launch.py",
              "18152"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2216020]",
              "2": "pipe:[2216021]",
              "3": "socket:[2212131]"
            },
            "maps_sha256": "fae197822d97bb79f1c67564ddb40ec27a3d06db307c51a67b2ebf0bb6f9e1b6",
            "pid": 297,
            "starttime": "10641353",
            "status_sha256": "8f2688421d44cf402c18e5a03b53c3f87d74002aae6191cf62d794fb5e002bdc"
          },
          "host": {
            "actual_launcher_pid": 304,
            "actual_launcher_starttime": "10641777",
            "argv": [
              "rtk",
              "proxy",
              "/task/lighttpd/owned/stock-host/bin/lighttpd",
              "-D",
              "-m",
              "/task/lighttpd/owned/stock-host/lib",
              "-f",
              "/task/lighttpd/lighttpd.conf"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "/dev/null",
              "2": "pipe:[2211461]",
              "3": "/task/lighttpd/lighttpd.pid",
              "4": "socket:[2213105]",
              "5": "/task/lighttpd/logs/lighttpd-error.log",
              "6": "/task/lighttpd/logs/stock-access.log",
              "7": "anon_inode:[eventpoll]",
              "8": "pipe:[2213106]",
              "9": "pipe:[2213106]"
            },
            "maps_sha256": "d586d7d9c78f362c98e93592df899758f25037869167355a0a6764ff182d9c2a",
            "pid": 305,
            "starttime": "10641778",
            "status_sha256": "8fee6ad2575a192726a5eb8621e0dce7d8faa67a9d9de28e33f137b22a0af699"
          },
          "sidecar": {
            "actual_launcher_pid": 308,
            "actual_launcher_starttime": "10641782",
            "argv": [
              "rtk",
              "proxy",
              "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
              "--config",
              "/task/lighttpd/runtime.conf",
              "--listen",
              "127.0.0.1:18154",
              "--upstream",
              "127.0.0.1:18153",
              "--timeout-ms",
              "3000",
              "--spool-directory",
              "/task/lighttpd/spool"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2216971]",
              "2": "pipe:[2216972]",
              "3": "/task/native-api.jsonl",
              "4": "/task/lighttpd/audit/native-audit.log",
              "5": "/task/lighttpd/audit/native-debug.log",
              "6": "socket:[2210502]",
              "7": "/task/lighttpd/events.jsonl",
              "8": "/task/lighttpd/spool"
            },
            "maps_sha256": "63f00416052709a612fd6591d7f1d4c80b52b6f535418878bebd742e38a0bbf1",
            "pid": 309,
            "starttime": "10641783",
            "status_sha256": "8ae1bbccc5986a3b2f6948bafae349bcbdb97d99f69ca37e47075abcbd33efb0"
          }
        },
        "actual_mapped_retained_images": [
          {
            "actor": "host",
            "device_equality_claimed": false,
            "mapped_inode": 51608796,
            "mapped_namespace_device": "00:2d",
            "mapped_path": "/task/lighttpd/owned/stock-host/bin/lighttpd",
            "physical_inode": 51608796,
            "physical_path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/owned/stock-host/bin/lighttpd",
            "physical_sha256": "5746e51d8d3e6a825886b334741c0998940587c2ffc536181da894bc4045ee56"
          },
          {
            "actor": "sidecar",
            "device_equality_claimed": false,
            "mapped_inode": 51608790,
            "mapped_namespace_device": "00:2d",
            "mapped_path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
            "physical_inode": 51608790,
            "physical_path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
            "physical_sha256": "c0ccfd0293324d610f4bd98fb6cf0bfce37a9026c8a01c32a7e3e566b61b0c4a"
          },
          {
            "actor": "sidecar",
            "device_equality_claimed": false,
            "mapped_inode": 16208420,
            "mapped_namespace_device": "00:22",
            "mapped_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
            "physical_inode": 16208420,
            "physical_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
            "physical_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
          }
        ],
        "native_actor": {
          "actual_launcher_pid": 308,
          "actual_launcher_starttime": "10641782",
          "argv": [
            "rtk",
            "proxy",
            "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
            "--config",
            "/task/lighttpd/runtime.conf",
            "--listen",
            "127.0.0.1:18154",
            "--upstream",
            "127.0.0.1:18153",
            "--timeout-ms",
            "3000",
            "--spool-directory",
            "/task/lighttpd/spool"
          ],
          "fds": {
            "0": "/dev/null",
            "1": "pipe:[2216971]",
            "2": "pipe:[2216972]",
            "3": "/task/native-api.jsonl",
            "4": "/task/lighttpd/audit/native-audit.log",
            "5": "/task/lighttpd/audit/native-debug.log",
            "6": "socket:[2210502]",
            "7": "/task/lighttpd/events.jsonl",
            "8": "/task/lighttpd/spool"
          },
          "maps_sha256": "63f00416052709a612fd6591d7f1d4c80b52b6f535418878bebd742e38a0bbf1",
          "pid": 309,
          "starttime": "10641783",
          "status_sha256": "8ae1bbccc5986a3b2f6948bafae349bcbdb97d99f69ca37e47075abcbd33efb0"
        },
        "raw_loaded_maps_and_status_retained": true,
        "sdk_version": "3.0.14",
        "selected_sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 242701,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/lighttpd-next-empty/runtime-source-ledger.json",
          "role": "source_manifest",
          "sha256": "53d05ae91153f033ad59ae0854a28f02619865a358f45ee909ad5c2b971f9800"
        },
        {
          "bytes": 242988,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/lighttpd-next-empty/source-compilation-binding.json",
          "role": "source_manifest",
          "sha256": "0a1d7a2ff2de7777f7869ccb699937bd4d0710296057ad945980cbef3ba4aa3a"
        },
        {
          "bytes": 17072,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/baseline-product-equality.json",
          "role": "source_manifest",
          "sha256": "020f0fe06179fa1bce00a806b07a13c2c4963fbb54a6892e6dccf0c526c7a4fb"
        },
        {
          "bytes": 18680,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/build-receipt.json",
          "role": "source_manifest",
          "sha256": "4b7068f0def2856db27a70f14df2e2f80925fbc204e72f55eff746778e819951"
        },
        {
          "bytes": 374,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/runtime.conf",
          "role": "effective_configuration",
          "sha256": "1e3669c9d6244f86e66134d8b72f5cd1acb5a86b6487cf0fc46a3a63dfe7a33f"
        },
        {
          "bytes": 470,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/lighttpd.conf",
          "role": "effective_configuration",
          "sha256": "8946903e782682ce4d9f0562b4d650512a0deef703476a17e538e1b575bbae60"
        },
        {
          "bytes": 882,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015988037131802/data/lighttpd/rules.conf",
          "role": "effective_configuration",
          "sha256": "e8b74efe52b322ab5be39620e1aaf541f49377416741ef35dfc8cbef98311290"
        }
      ],
      "value": {
        "actual_baseline_product_input_equality_count": 149,
        "baseline_product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "direct_supplement": true,
        "immutable_test_only_callbacks_explicit": true,
        "legacy_whole_harness_namespace_blocker_preserved": false,
        "real_parent_base": "02754040bced960cfc1857416cd7101bb3116ef4"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8946903e782682ce4d9f0562b4d650512a0deef703476a17e538e1b575bbae60",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "02754040bced960cfc1857416cd7101bb3116ef4",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "e8b74efe52b322ab5be39620e1aaf541f49377416741ef35dfc8cbef98311290",
    "run_id": "20261014T182400Z-lighttpd-empty-stock-sidecar"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 367635,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-lighttpd-empty-stock-sidecar-01.json",
    "sha256": "c96dba0f35d61965676f0af88e27d1a0be447a166990d16f2536486af1b8f8f8"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::lighttpd-stock-sidecar::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1537,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/execution-receipt.json",
          "role": "cleanup_observer",
          "sha256": "295fe5f2615ae18561424ccd3fc9950c233d3c2ca0178beecbd77fcd0f0a6622"
        },
        {
          "bytes": 4622,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "7408f6f87e16ab3428aae82826ef26bfa044590fddba56aa20d1250969a2b4a2"
        }
      ],
      "value": {
        "actual_all_scopes_finalize_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 58,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finalize_and_snapshot",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 104556811451226,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 1,
            "run": "20261014T182400Z-lighttpd-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": {
              "association_retired": 1,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "finished": 1,
              "handle_cleared": 1,
              "status": 6
            },
            "schema": "native-lifecycle-v1",
            "sequence": 69,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792014190600856666,
            "wall_sample_end_monotonic_ns": 104556811451308
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 72,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 122,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finalize_and_snapshot",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 104557426298199,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 1,
            "run": "20261014T182400Z-lighttpd-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": {
              "association_retired": 1,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "finished": 1,
              "handle_cleared": 1,
              "status": 6
            },
            "schema": "native-lifecycle-v1",
            "sequence": 133,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792014191215703678,
            "wall_sample_end_monotonic_ns": 104557426298326
          }
        ],
        "actual_host_final": [],
        "actual_process_cleanup": [
          {
            "actor": "sidecar",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 308,
            "actual_launcher_starttime": "10455666",
            "actual_return_code": 143,
            "launcher_reaped": true,
            "native_pid": 309,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10455667"
          },
          {
            "actor": "host",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 304,
            "actual_launcher_starttime": "10455662",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 305,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10455662"
          },
          {
            "actor": "backend",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 296,
            "actual_launcher_starttime": "10455283",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 297,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10455284"
          }
        ],
        "last_actual_host_api": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 134,
          "canonical_transaction_id": null,
          "case": "NEED-request-eos-once",
          "contract_state": null,
          "edge": "return",
          "function": "runtime_destroy",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 104557426431099,
          "native_mime_selection": null,
          "pending_calls": 1,
          "phase": 0,
          "pid": 309,
          "profile": "lighttpd-stock-sidecar",
          "result": null,
          "run": "20261014T182400Z-lighttpd-stock-sidecar",
          "runtime_eos_handoff": null,
          "runtime_finalize_snapshot": null,
          "schema": "native-lifecycle-v1",
          "sequence": 135,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792014191215836546,
          "wall_sample_end_monotonic_ns": 104557426431196
        },
        "stock_observer_mapping_gap": false
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 145730,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "b59d549d49b2327e2e6bc456ddf96dade5c1dd4ad8fc7c59463849444004cec4"
        }
      ],
      "value": {
        "actual_finalize_and_snapshot_calls": 1,
        "common_finish_calls": 2,
        "external_runtime_finish_calls": 0,
        "native_logging_calls": 1,
        "stock_finalize_and_snapshot_not_wrapped": false
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1146,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "399d06a81c2736a1938c37a306245c95104fe8c458594cab8efec715343803db"
        }
      ],
      "value": [
        {
          "actual_eos_argument": 1,
          "entity_length": 23,
          "gid": 65534,
          "input_size": 0,
          "invalid": false,
          "kind": "stock_request_content_length_eos",
          "monotonic_ns": 104556800865505,
          "pid": 309,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 1,
          "stream_offset": 23,
          "uid": 65534
        },
        {
          "actual_eos_argument": 1,
          "entity_length": 24,
          "gid": 65534,
          "input_size": 0,
          "invalid": false,
          "kind": "stock_response_content_length_eos",
          "monotonic_ns": 104556810220777,
          "pid": 309,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 2,
          "stream_offset": 24,
          "uid": 65534
        }
      ]
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1146,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "399d06a81c2736a1938c37a306245c95104fe8c458594cab8efec715343803db"
        },
        {
          "bytes": 145730,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "b59d549d49b2327e2e6bc456ddf96dade5c1dd4ad8fc7c59463849444004cec4"
        }
      ],
      "value": {
        "definition": "Actual accepted native patched eos argument, or actual finite Content-Length consumed branch, plus same typed Runtime/native finalization calls.",
        "native_append_eos_argument": null,
        "native_request_finalization": 1,
        "native_response_finalization": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 145730,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "b59d549d49b2327e2e6bc456ddf96dade5c1dd4ad8fc7c59463849444004cec4"
        }
      ],
      "value": {
        "actual_finalize_snapshot_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 58,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_finalize_and_snapshot",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 104556811451226,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": 1,
            "run": "20261014T182400Z-lighttpd-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": {
              "association_retired": 1,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "finished": 1,
              "handle_cleared": 1,
              "status": 6
            },
            "schema": "native-lifecycle-v1",
            "sequence": 69,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792014190600856666,
            "wall_sample_end_monotonic_ns": 104556811451308
          }
        ],
        "common_cleanup": 1,
        "native_cleanup": 1,
        "runtime_free_correlation_known": true,
        "typed_runtime_destroy": 0,
        "unjoined_external_destroy_rows": [
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 70,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "enter",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 104556811571781,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 70,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792014190600977246,
            "wall_sample_end_monotonic_ns": 104556811571894
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 70,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 104556811600542,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 71,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792014190601005997,
            "wall_sample_end_monotonic_ns": 104556811600639
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 134,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "enter",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 104557426400463,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 134,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792014191215805946,
            "wall_sample_end_monotonic_ns": 104557426400598
          },
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 134,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 104557426431099,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 309,
            "profile": "lighttpd-stock-sidecar",
            "result": null,
            "run": "20261014T182400Z-lighttpd-stock-sidecar",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 135,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792014191215836546,
            "wall_sample_end_monotonic_ns": 104557426431196
          }
        ]
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 17160,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/backend.maps",
          "role": "loaded_image",
          "sha256": "c7a397b5024bd1cbe1e006da4eb7a3c645a908cec8e9a03c112b4730b7daaa5f"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/backend.status",
          "role": "loaded_image",
          "sha256": "c64ac599c9720d13e2319b803d2b4564ae3e2dd77744e9aa6f75e30bd01a0e50"
        },
        {
          "bytes": 4263,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/host.maps",
          "role": "loaded_image",
          "sha256": "7850dbe69277efaeb55c7e6d54e7d18d6e599ea7feac9b42953a92657963948b"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/host.status",
          "role": "loaded_image",
          "sha256": "9e51cd34d8b3ec176e2fdfd12821b1f1a61fe41566b8a7708c626075550df622"
        },
        {
          "bytes": 27897,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/sidecar.maps",
          "role": "loaded_image",
          "sha256": "02f1a625a4ade15fc8c0f1feec911528a0d8b5a05a2e07d6127c29759642fb9d"
        },
        {
          "bytes": 1505,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/sidecar.status",
          "role": "loaded_image",
          "sha256": "cbc1aed4c7808746dca12b4a95342332f5c0d7180ff7905fc80c8a7c0f55211a"
        },
        {
          "bytes": 4622,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "7408f6f87e16ab3428aae82826ef26bfa044590fddba56aa20d1250969a2b4a2"
        },
        {
          "bytes": 448216,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/owned/stock-host/bin/lighttpd",
          "role": "loaded_image",
          "sha256": "5746e51d8d3e6a825886b334741c0998940587c2ffc536181da894bc4045ee56"
        },
        {
          "bytes": 352040,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
          "role": "loaded_image",
          "sha256": "c0ccfd0293324d610f4bd98fb6cf0bfce37a9026c8a01c32a7e3e566b61b0c4a"
        },
        {
          "bytes": 2034032,
          "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "role": "loaded_image",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        },
        {
          "bytes": 4218,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/lighttpd-stock-sidecar-mapped-image-version-01.json",
          "role": "loaded_image",
          "sha256": "a8c0bf60a61f51faa7c0722dac49db5f1f5389d9269766fd8066c74aa12a40f2"
        }
      ],
      "value": {
        "actual_actors": {
          "backend": {
            "actual_launcher_pid": 296,
            "actual_launcher_starttime": "10455283",
            "argv": [
              "rtk",
              "proxy",
              "/usr/local/bin/python3",
              "/mnt/fixtures/backend-launch.py",
              "18152"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2159093]",
              "2": "pipe:[2159094]",
              "3": "socket:[2159852]"
            },
            "maps_sha256": "c7a397b5024bd1cbe1e006da4eb7a3c645a908cec8e9a03c112b4730b7daaa5f",
            "pid": 297,
            "starttime": "10455284",
            "status_sha256": "c64ac599c9720d13e2319b803d2b4564ae3e2dd77744e9aa6f75e30bd01a0e50"
          },
          "host": {
            "actual_launcher_pid": 304,
            "actual_launcher_starttime": "10455662",
            "argv": [
              "rtk",
              "proxy",
              "/task/lighttpd/owned/stock-host/bin/lighttpd",
              "-D",
              "-m",
              "/task/lighttpd/owned/stock-host/lib",
              "-f",
              "/task/lighttpd/lighttpd.conf"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "/dev/null",
              "2": "pipe:[2155519]",
              "3": "/task/lighttpd/lighttpd.pid",
              "4": "socket:[2159860]",
              "5": "/task/lighttpd/logs/lighttpd-error.log",
              "6": "/task/lighttpd/logs/stock-access.log",
              "7": "anon_inode:[eventpoll]",
              "8": "pipe:[2159861]",
              "9": "pipe:[2159861]"
            },
            "maps_sha256": "7850dbe69277efaeb55c7e6d54e7d18d6e599ea7feac9b42953a92657963948b",
            "pid": 305,
            "starttime": "10455662",
            "status_sha256": "9e51cd34d8b3ec176e2fdfd12821b1f1a61fe41566b8a7708c626075550df622"
          },
          "sidecar": {
            "actual_launcher_pid": 308,
            "actual_launcher_starttime": "10455666",
            "argv": [
              "rtk",
              "proxy",
              "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
              "--config",
              "/task/lighttpd/runtime.conf",
              "--listen",
              "127.0.0.1:18154",
              "--upstream",
              "127.0.0.1:18153",
              "--timeout-ms",
              "3000",
              "--spool-directory",
              "/task/lighttpd/spool"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2162696]",
              "2": "pipe:[2162697]",
              "3": "/task/native-api.jsonl",
              "4": "/task/lighttpd/audit/native-audit.log",
              "5": "/task/lighttpd/audit/native-debug.log",
              "6": "socket:[2160770]",
              "7": "/task/lighttpd/events.jsonl",
              "8": "/task/lighttpd/spool"
            },
            "maps_sha256": "02f1a625a4ade15fc8c0f1feec911528a0d8b5a05a2e07d6127c29759642fb9d",
            "pid": 309,
            "starttime": "10455667",
            "status_sha256": "cbc1aed4c7808746dca12b4a95342332f5c0d7180ff7905fc80c8a7c0f55211a"
          }
        },
        "actual_host_version": "lighttpd/1.4.85 - a light and fast webserver",
        "mapped_image_identity": {
          "connector_sidecar": {
            "actual_loaded_inode": 51573133,
            "actual_loaded_paths": [
              "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar"
            ],
            "actual_mapping": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/sidecar.maps",
              "sha256": "02f1a625a4ade15fc8c0f1feec911528a0d8b5a05a2e07d6127c29759642fb9d"
            },
            "captured_namespace_map_devices": [
              "00:2d"
            ],
            "device_scope": "Captured namespace mapping and later tool stat expose different device aliases. No cross-environment device equality is claimed. Exact mapped path, retained inode, sealed input/copy guards and physical image SHA bind the image.",
            "physical_image": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
              "role": "loaded_image",
              "sha256": "c0ccfd0293324d610f4bd98fb6cf0bfce37a9026c8a01c32a7e3e566b61b0c4a"
            },
            "retained_file_current_device": [
              0,
              47
            ]
          },
          "host_binary": {
            "actual_loaded_inode": 51573142,
            "actual_loaded_paths": [
              "/task/lighttpd/owned/stock-host/bin/lighttpd"
            ],
            "actual_mapping": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/host.maps",
              "sha256": "7850dbe69277efaeb55c7e6d54e7d18d6e599ea7feac9b42953a92657963948b"
            },
            "captured_namespace_map_devices": [
              "00:2d"
            ],
            "device_scope": "Captured namespace mapping and later tool stat expose different device aliases. No cross-environment device equality is claimed. Exact mapped path, retained inode, sealed input/copy guards and physical image SHA bind the image.",
            "physical_image": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/owned/stock-host/bin/lighttpd",
              "role": "loaded_image",
              "sha256": "5746e51d8d3e6a825886b334741c0998940587c2ffc536181da894bc4045ee56"
            },
            "retained_file_current_device": [
              0,
              47
            ]
          },
          "loaded_native_sdk": {
            "actual_loaded_inode": 16208420,
            "actual_loaded_paths": [
              "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14"
            ],
            "actual_mapping": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/receipts/before-main/sidecar.maps",
              "sha256": "02f1a625a4ade15fc8c0f1feec911528a0d8b5a05a2e07d6127c29759642fb9d"
            },
            "captured_namespace_map_devices": [
              "00:22"
            ],
            "device_scope": "Captured namespace mapping and later tool stat expose different device aliases. No cross-environment device equality is claimed. Exact mapped path, retained inode, sealed input/copy guards and physical image SHA bind the image.",
            "physical_image": {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "role": "loaded_image",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            },
            "retained_file_current_device": [
              0,
              35
            ]
          }
        },
        "native_actor": {
          "actual_launcher_pid": 308,
          "actual_launcher_starttime": "10455666",
          "argv": [
            "rtk",
            "proxy",
            "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/stock-sidecar/lighttpd-stock-sidecar",
            "--config",
            "/task/lighttpd/runtime.conf",
            "--listen",
            "127.0.0.1:18154",
            "--upstream",
            "127.0.0.1:18153",
            "--timeout-ms",
            "3000",
            "--spool-directory",
            "/task/lighttpd/spool"
          ],
          "fds": {
            "0": "/dev/null",
            "1": "pipe:[2162696]",
            "2": "pipe:[2162697]",
            "3": "/task/native-api.jsonl",
            "4": "/task/lighttpd/audit/native-audit.log",
            "5": "/task/lighttpd/audit/native-debug.log",
            "6": "socket:[2160770]",
            "7": "/task/lighttpd/events.jsonl",
            "8": "/task/lighttpd/spool"
          },
          "maps_sha256": "02f1a625a4ade15fc8c0f1feec911528a0d8b5a05a2e07d6127c29759642fb9d",
          "pid": 309,
          "starttime": "10455667",
          "status_sha256": "cbc1aed4c7808746dca12b4a95342332f5c0d7180ff7905fc80c8a7c0f55211a"
        },
        "raw_loaded_maps_and_status_retained": true,
        "sdk_version": "3.0.14",
        "selected_sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 242701,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/source-05-ledger.json",
          "role": "source_manifest",
          "sha256": "eb433790254c38bb6c337b8a9607594e0880fa0fb4679c32a7ef96d278b28808"
        },
        {
          "bytes": 243014,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/source-05-compilation-binding.json",
          "role": "source_manifest",
          "sha256": "4e3dd326d56d43fcb9a10e82274eca4bc513acfbdf8aa657b43684b23e691801"
        },
        {
          "bytes": 17072,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/baseline-product-equality.json",
          "role": "source_manifest",
          "sha256": "020f0fe06179fa1bce00a806b07a13c2c4963fbb54a6892e6dccf0c526c7a4fb"
        },
        {
          "bytes": 18680,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-04/build-receipt.json",
          "role": "source_manifest",
          "sha256": "4b7068f0def2856db27a70f14df2e2f80925fbc204e72f55eff746778e819951"
        },
        {
          "bytes": 374,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/runtime.conf",
          "role": "effective_configuration",
          "sha256": "1e3669c9d6244f86e66134d8b72f5cd1acb5a86b6487cf0fc46a3a63dfe7a33f"
        },
        {
          "bytes": 470,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/lighttpd.conf",
          "role": "effective_configuration",
          "sha256": "8946903e782682ce4d9f0562b4d650512a0deef703476a17e538e1b575bbae60"
        },
        {
          "bytes": 639,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792014145015075707/data/lighttpd/rules.conf",
          "role": "effective_configuration",
          "sha256": "29e3c335c0b6c4a3603de704bc5ffe3bfc6ddb74bfacb4ac37f521ad72da943a"
        },
        {
          "bytes": 116,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-readonly-revisions-01.json",
          "role": "source_manifest",
          "sha256": "7626580d3e02904f25e1ebc03852abab8596c3d78cf092a2e3b2658f5514a0cf"
        }
      ],
      "value": {
        "actual_baseline_product_input_equality_count": 149,
        "baseline_product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "direct_supplement": true,
        "immutable_test_only_callbacks_explicit": true,
        "legacy_whole_harness_namespace_blocker_preserved": false,
        "real_parent_base": "02754040bced960cfc1857416cd7101bb3116ef4"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "8946903e782682ce4d9f0562b4d650512a0deef703476a17e538e1b575bbae60",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "02754040bced960cfc1857416cd7101bb3116ef4",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "29e3c335c0b6c4a3603de704bc5ffe3bfc6ddb74bfacb4ac37f521ad72da943a",
    "run_id": "20261014T182400Z-lighttpd-stock-sidecar"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 378529,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-lighttpd-stock-sidecar-02.json",
    "sha256": "19ea6ae209da049b5757ee96269c3839aabc8df5bd9946504242085ef87eb0db"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::lighttpd-patched-native::NEED-request-empty

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1202,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/execution-receipt.json",
          "role": "cleanup_observer",
          "sha256": "829069450f31f00a0ac2f394e2002561f75bc11fd05e6895cbe71eb8cb9696fb"
        },
        {
          "bytes": 4540,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "d79d018c6bc470f5ac693db1dcdb459c9a4b05e22c13abee34ba913255ed854e"
        }
      ],
      "value": {
        "actual_host_final": [
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 0,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "final",
            "function": "observer",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 106409471635789,
            "native_mime_selection": null,
            "pending_calls": 0,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-patched-native",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 134,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016043261041299,
            "wall_sample_end_monotonic_ns": 106409471635954
          }
        ],
        "actual_process_cleanup": [
          {
            "actor": "host",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 297,
            "actual_launcher_starttime": "10640756",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 298,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10640757"
          },
          {
            "actor": "backend",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 289,
            "actual_launcher_starttime": "10640345",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 290,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10640346"
          }
        ],
        "all_scopes_cleanup_rows": [
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 63,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "lighttpd-298-1",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106407723306152,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-patched-native",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 64,
            "transaction_id": "lighttpd-298-1",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016041512711598,
            "wall_sample_end_monotonic_ns": 106407723306244
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 65,
            "canonical_transaction_id": "txc-000000000657a723-0000000000000000",
            "case": "NEED-request-empty",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 106407723,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "completed_at_ms": 106407722,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 0,
              "status": 6
            },
            "edge": "return",
            "function": "common_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 2,
            "monotonic_ns": 106407723365317,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": 0,
            "run": "20261014T182400Z-lighttpd-empty-patched-native",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 66,
            "transaction_id": "lighttpd-298-1",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016041512770758,
            "wall_sample_end_monotonic_ns": 106407723365409
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 2,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 62,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 106407723594054,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-patched-native",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 67,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016041512999555,
            "wall_sample_end_monotonic_ns": 106407723594219
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 68,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 129,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "native_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": "lighttpd-298-2",
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 3,
            "monotonic_ns": 106408631795236,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-patched-native",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 130,
            "transaction_id": "lighttpd-298-2",
            "transaction_id_origin": "sdk_public_m_id",
            "uid": 65534,
            "wall_ns": 1792016042421200686,
            "wall_sample_end_monotonic_ns": 106408631795333
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 68,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 131,
            "canonical_transaction_id": "txc-000000000657aab4-0000000000000002",
            "case": "NEED-request-empty",
            "contract_state": {
              "active_phase": -1,
              "cleanup_at_ms": 106408631,
              "cleanup_complete": 1,
              "cleanup_started": 1,
              "completed_at_ms": 106408631,
              "completed_phase_mask": 15,
              "last_completed_phase": 5,
              "response_committed": 0,
              "status": 6
            },
            "edge": "return",
            "function": "common_cleanup",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 2,
            "monotonic_ns": 106408631845534,
            "native_mime_selection": null,
            "pending_calls": 2,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": 0,
            "run": "20261014T182400Z-lighttpd-empty-patched-native",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 132,
            "transaction_id": "lighttpd-298-2",
            "transaction_id_origin": "common_public_contract",
            "uid": 65534,
            "wall_ns": 1792016042421250973,
            "wall_sample_end_monotonic_ns": 106408631845624
          },
          {
            "allocation_join_verified": true,
            "allocation_scope_call": 68,
            "allocation_scope_kind": "runtime",
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 128,
            "canonical_transaction_id": null,
            "case": "NEED-request-empty",
            "contract_state": null,
            "edge": "return",
            "function": "runtime_destroy",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 1,
            "monotonic_ns": 106408632097647,
            "native_mime_selection": null,
            "pending_calls": 1,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": null,
            "run": "20261014T182400Z-lighttpd-empty-patched-native",
            "runtime_eos_handoff": null,
            "runtime_finalize_snapshot": null,
            "schema": "native-lifecycle-v1",
            "sequence": 133,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792016042421503128,
            "wall_sample_end_monotonic_ns": 106408632097776
          }
        ],
        "last_actual_host_api": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-empty",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 106409471635789,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 298,
          "profile": "lighttpd-patched-native",
          "result": null,
          "run": "20261014T182400Z-lighttpd-empty-patched-native",
          "runtime_eos_handoff": null,
          "runtime_finalize_snapshot": null,
          "schema": "native-lifecycle-v1",
          "sequence": 134,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792016043261041299,
          "wall_sample_end_monotonic_ns": 106409471635954
        },
        "stock_observer_mapping_gap": false
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 145523,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "ce31bdd2f462848a57685bd5d71b1b055a6a34be708b5a97e656dc0e812c3385"
        }
      ],
      "value": {
        "actual_finalize_and_snapshot_calls": 0,
        "common_finish_calls": 2,
        "external_runtime_finish_calls": 1,
        "native_logging_calls": 1,
        "stock_finalize_and_snapshot_not_wrapped": false
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1877,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "3b20da395c305787e4e6f53e1f7b4513a9e5614ac8c695ac44a156dac1bdbbb3"
        }
      ],
      "value": [
        {
          "actual_eos_argument": null,
          "empty_request_boundary": true,
          "entity_length": 0,
          "gid": 65534,
          "input_size": 0,
          "invalid": false,
          "kind": "patched_empty_request_boundary",
          "monotonic_ns": 106407716299611,
          "pid": 298,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 1,
          "stream_offset": 0,
          "uid": 65534
        },
        {
          "actual_eos_argument": 0,
          "empty_request_boundary": false,
          "entity_length": -1,
          "gid": 65534,
          "input_size": 24,
          "invalid": false,
          "kind": "patched_response_body_hook",
          "monotonic_ns": 106407722137432,
          "pid": 298,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 2,
          "stream_offset": 0,
          "uid": 65534
        },
        {
          "actual_eos_argument": 1,
          "empty_request_boundary": false,
          "entity_length": -1,
          "gid": 65534,
          "input_size": 0,
          "invalid": false,
          "kind": "patched_response_body_hook",
          "monotonic_ns": 106407722337131,
          "pid": 298,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 3,
          "stream_offset": 24,
          "uid": 65534
        }
      ]
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1877,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "3b20da395c305787e4e6f53e1f7b4513a9e5614ac8c695ac44a156dac1bdbbb3"
        },
        {
          "bytes": 145523,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "ce31bdd2f462848a57685bd5d71b1b055a6a34be708b5a97e656dc0e812c3385"
        }
      ],
      "value": {
        "actual_empty_request_boundary": [
          {
            "actual_eos_argument": null,
            "empty_request_boundary": true,
            "entity_length": 0,
            "gid": 65534,
            "input_size": 0,
            "invalid": false,
            "kind": "patched_empty_request_boundary",
            "monotonic_ns": 106407716299611,
            "pid": 298,
            "runtime_allocation_scope_call": 2,
            "schema": "lighttpd-physical-host-v1",
            "sequence": 1,
            "stream_offset": 0,
            "uid": 65534
          }
        ],
        "definition": "Actual accepted native patched eos argument, or actual finite Content-Length consumed branch, plus same typed Runtime/native finalization calls.",
        "native_append_eos_argument": null,
        "native_request_finalization": 1,
        "native_response_finalization": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 145523,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "ce31bdd2f462848a57685bd5d71b1b055a6a34be708b5a97e656dc0e812c3385"
        }
      ],
      "value": {
        "actual_finalize_snapshot_rows": [],
        "common_cleanup": 1,
        "native_cleanup": 1,
        "runtime_free_correlation_known": true,
        "typed_runtime_destroy": 1,
        "unjoined_external_destroy_rows": []
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 17111,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/receipts/before-main/backend.maps",
          "role": "loaded_image",
          "sha256": "34a54621ce69c632b82ca937a7bc69215fe555457947cfae18afd2df2548c893"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/receipts/before-main/backend.status",
          "role": "loaded_image",
          "sha256": "893d493906114221e7d5246ea4192b5a632f77eac472fe45998ecc88a4f1eb08"
        },
        {
          "bytes": 28450,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/receipts/before-main/host.maps",
          "role": "loaded_image",
          "sha256": "60dd4d4f016e164c2e2492392bb9ecab5b9a295abea202c8e07a814cbc7e1fa0"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/receipts/before-main/host.status",
          "role": "loaded_image",
          "sha256": "c64f95ce5b28a87cd52801c4bf9a480336651037b519e06c5407086271fb563c"
        },
        {
          "bytes": 4540,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "d79d018c6bc470f5ac693db1dcdb459c9a4b05e22c13abee34ba913255ed854e"
        },
        {
          "bytes": 1766976,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/owned/patched-host/bin/lighttpd",
          "role": "loaded_image",
          "sha256": "b82f8c0c70c419c30446faad1a3f8094722ff18b37add72270ae716d48d6f2ce"
        },
        {
          "bytes": 2034032,
          "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "role": "loaded_image",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        },
        {
          "bytes": 380440,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/owned/patched-host/modules/mod_msconnector.so",
          "role": "loaded_image",
          "sha256": "6d389bf8dc4dc637db32b8a870d502a77800b2724e5bc728ee53a0a0a97691cd"
        }
      ],
      "value": {
        "actual_actors": {
          "backend": {
            "actual_launcher_pid": 289,
            "actual_launcher_starttime": "10640345",
            "argv": [
              "rtk",
              "proxy",
              "/usr/local/bin/python3",
              "/mnt/fixtures/backend-launch.py",
              "18152"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2214131]",
              "2": "pipe:[2214132]",
              "3": "socket:[2215971]"
            },
            "maps_sha256": "34a54621ce69c632b82ca937a7bc69215fe555457947cfae18afd2df2548c893",
            "pid": 290,
            "starttime": "10640346",
            "status_sha256": "893d493906114221e7d5246ea4192b5a632f77eac472fe45998ecc88a4f1eb08"
          },
          "host": {
            "actual_launcher_pid": 297,
            "actual_launcher_starttime": "10640756",
            "argv": [
              "rtk",
              "proxy",
              "/task/lighttpd/owned/patched-host/bin/lighttpd",
              "-D",
              "-m",
              "/task/lighttpd/owned/patched-host/modules",
              "-f",
              "/task/lighttpd/lighttpd.conf"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "/dev/null",
              "10": "/task/lighttpd/events.jsonl",
              "11": "pipe:[2211372]",
              "12": "pipe:[2211372]",
              "2": "pipe:[2212098]",
              "3": "/task/native-api.jsonl",
              "4": "/task/lighttpd/lighttpd.pid",
              "5": "socket:[2211370]",
              "6": "/task/lighttpd/logs/lighttpd-error.log",
              "7": "/task/lighttpd/audit/native-audit.log",
              "8": "/task/lighttpd/audit/native-debug.log",
              "9": "anon_inode:[eventpoll]"
            },
            "maps_sha256": "60dd4d4f016e164c2e2492392bb9ecab5b9a295abea202c8e07a814cbc7e1fa0",
            "pid": 298,
            "starttime": "10640757",
            "status_sha256": "c64f95ce5b28a87cd52801c4bf9a480336651037b519e06c5407086271fb563c"
          }
        },
        "actual_mapped_retained_images": [
          {
            "actor": "host",
            "device_equality_claimed": false,
            "mapped_inode": 51608596,
            "mapped_namespace_device": "00:2d",
            "mapped_path": "/task/lighttpd/owned/patched-host/bin/lighttpd",
            "physical_inode": 51608596,
            "physical_path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/owned/patched-host/bin/lighttpd",
            "physical_sha256": "b82f8c0c70c419c30446faad1a3f8094722ff18b37add72270ae716d48d6f2ce"
          },
          {
            "actor": "host",
            "device_equality_claimed": false,
            "mapped_inode": 16208420,
            "mapped_namespace_device": "00:22",
            "mapped_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
            "physical_inode": 16208420,
            "physical_path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
            "physical_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
          },
          {
            "actor": "host",
            "device_equality_claimed": false,
            "mapped_inode": 51608598,
            "mapped_namespace_device": "00:2d",
            "mapped_path": "/task/lighttpd/owned/patched-host/modules/mod_msconnector.so",
            "physical_inode": 51608598,
            "physical_path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/owned/patched-host/modules/mod_msconnector.so",
            "physical_sha256": "6d389bf8dc4dc637db32b8a870d502a77800b2724e5bc728ee53a0a0a97691cd"
          }
        ],
        "native_actor": {
          "actual_launcher_pid": 297,
          "actual_launcher_starttime": "10640756",
          "argv": [
            "rtk",
            "proxy",
            "/task/lighttpd/owned/patched-host/bin/lighttpd",
            "-D",
            "-m",
            "/task/lighttpd/owned/patched-host/modules",
            "-f",
            "/task/lighttpd/lighttpd.conf"
          ],
          "fds": {
            "0": "/dev/null",
            "1": "/dev/null",
            "10": "/task/lighttpd/events.jsonl",
            "11": "pipe:[2211372]",
            "12": "pipe:[2211372]",
            "2": "pipe:[2212098]",
            "3": "/task/native-api.jsonl",
            "4": "/task/lighttpd/lighttpd.pid",
            "5": "socket:[2211370]",
            "6": "/task/lighttpd/logs/lighttpd-error.log",
            "7": "/task/lighttpd/audit/native-audit.log",
            "8": "/task/lighttpd/audit/native-debug.log",
            "9": "anon_inode:[eventpoll]"
          },
          "maps_sha256": "60dd4d4f016e164c2e2492392bb9ecab5b9a295abea202c8e07a814cbc7e1fa0",
          "pid": 298,
          "starttime": "10640757",
          "status_sha256": "c64f95ce5b28a87cd52801c4bf9a480336651037b519e06c5407086271fb563c"
        },
        "raw_loaded_maps_and_status_retained": true,
        "sdk_version": "3.0.14",
        "selected_sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 242701,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/lighttpd-next-empty/runtime-source-ledger.json",
          "role": "source_manifest",
          "sha256": "53d05ae91153f033ad59ae0854a28f02619865a358f45ee909ad5c2b971f9800"
        },
        {
          "bytes": 242988,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/lighttpd-next-empty/source-compilation-binding.json",
          "role": "source_manifest",
          "sha256": "0a1d7a2ff2de7777f7869ccb699937bd4d0710296057ad945980cbef3ba4aa3a"
        },
        {
          "bytes": 17072,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/baseline-product-equality.json",
          "role": "source_manifest",
          "sha256": "020f0fe06179fa1bce00a806b07a13c2c4963fbb54a6892e6dccf0c526c7a4fb"
        },
        {
          "bytes": 5310,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/lighttpd-next-empty/patched-build/receipt.json",
          "role": "source_manifest",
          "sha256": "66c53efbaf247bb0e5fee8e68165fc96dc5838ca1484d57a31f57e698660a48e"
        },
        {
          "bytes": 374,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/runtime.conf",
          "role": "effective_configuration",
          "sha256": "1e3669c9d6244f86e66134d8b72f5cd1acb5a86b6487cf0fc46a3a63dfe7a33f"
        },
        {
          "bytes": 578,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/lighttpd.conf",
          "role": "effective_configuration",
          "sha256": "99e40c6484f0aef7874ac6f000ee4da6623f4a817b1d4e6cf7f64cbbc821eae4"
        },
        {
          "bytes": 882,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792015991720084429/data/lighttpd/rules.conf",
          "role": "effective_configuration",
          "sha256": "e8b74efe52b322ab5be39620e1aaf541f49377416741ef35dfc8cbef98311290"
        }
      ],
      "value": {
        "actual_baseline_product_input_equality_count": 149,
        "baseline_product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "direct_supplement": true,
        "immutable_test_only_callbacks_explicit": true,
        "legacy_whole_harness_namespace_blocker_preserved": true,
        "real_parent_base": "02754040bced960cfc1857416cd7101bb3116ef4"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "99e40c6484f0aef7874ac6f000ee4da6623f4a817b1d4e6cf7f64cbbc821eae4",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "02754040bced960cfc1857416cd7101bb3116ef4",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "e8b74efe52b322ab5be39620e1aaf541f49377416741ef35dfc8cbef98311290",
    "run_id": "20261014T182400Z-lighttpd-empty-patched-native"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 362667,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-lighttpd-empty-patched-native-01.json",
    "sha256": "5958fd2902a6552cc121f033012af56e4b5dc8959f52cf03fb60478bef223788"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

### I12::lighttpd-patched-native::NEED-request-eos-once

```json
{
  "observations": {
    "cleanup_receipts": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1205,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/execution-receipt.json",
          "role": "cleanup_observer",
          "sha256": "b1578cc13c9e4cb18a833af275ccbb0c4ed1b40da6d0a0c558d5ca460e9319b2"
        },
        {
          "bytes": 4626,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "19e316e0c4243a407fb7139b4eb4f4c8dddff8fbbbd399f4bede2506a71606ba"
        }
      ],
      "value": {
        "actual_host_final": [
          {
            "allocation_join_verified": false,
            "allocation_scope_call": null,
            "allocation_scope_kind": null,
            "argument_committed": null,
            "argument_eos": null,
            "argument_response_status": null,
            "call": 0,
            "canonical_transaction_id": null,
            "case": "NEED-request-eos-once",
            "contract_state": null,
            "edge": "final",
            "function": "observer",
            "gid": 65534,
            "host_eos": null,
            "host_framing": null,
            "input_kind": null,
            "input_size": null,
            "input_transaction_id": null,
            "intervention_disruptive": null,
            "intervention_status": null,
            "invalid": false,
            "live_mappings": 0,
            "monotonic_ns": 103686249380750,
            "native_mime_selection": null,
            "pending_calls": 0,
            "phase": 0,
            "pid": 298,
            "profile": "lighttpd-patched-native",
            "result": null,
            "run": "20261014T182400Z-lighttpd-patched-native",
            "runtime_eos_handoff": null,
            "schema": "native-lifecycle-v1",
            "sequence": 140,
            "transaction_id": null,
            "transaction_id_origin": "unknown",
            "uid": 65534,
            "wall_ns": 1792013320038786369,
            "wall_sample_end_monotonic_ns": 103686249381031
          }
        ],
        "actual_process_cleanup": [
          {
            "actor": "host",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 297,
            "actual_launcher_starttime": "10368455",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 298,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10368455"
          },
          {
            "actor": "backend",
            "actual_before_cleanup_exit": null,
            "actual_launcher_pid": 289,
            "actual_launcher_starttime": "10368081",
            "actual_return_code": 0,
            "launcher_reaped": true,
            "native_pid": 290,
            "native_same_starttime_pid_gone": true,
            "native_starttime": "10368081"
          }
        ],
        "last_actual_host_api": {
          "allocation_join_verified": false,
          "allocation_scope_call": null,
          "allocation_scope_kind": null,
          "argument_committed": null,
          "argument_eos": null,
          "argument_response_status": null,
          "call": 0,
          "canonical_transaction_id": null,
          "case": "NEED-request-eos-once",
          "contract_state": null,
          "edge": "final",
          "function": "observer",
          "gid": 65534,
          "host_eos": null,
          "host_framing": null,
          "input_kind": null,
          "input_size": null,
          "input_transaction_id": null,
          "intervention_disruptive": null,
          "intervention_status": null,
          "invalid": false,
          "live_mappings": 0,
          "monotonic_ns": 103686249380750,
          "native_mime_selection": null,
          "pending_calls": 0,
          "phase": 0,
          "pid": 298,
          "profile": "lighttpd-patched-native",
          "result": null,
          "run": "20261014T182400Z-lighttpd-patched-native",
          "runtime_eos_handoff": null,
          "schema": "native-lifecycle-v1",
          "sequence": 140,
          "transaction_id": null,
          "transaction_id_origin": "unknown",
          "uid": 65534,
          "wall_ns": 1792013320038786369,
          "wall_sample_end_monotonic_ns": 103686249381031
        },
        "stock_observer_mapping_gap": false
      }
    },
    "finish_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 146443,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "10a469886c82dbd4c8d906cefa7a181fbfe795847facd0c06ba1363ea7d88565"
        }
      ],
      "value": {
        "common_finish_calls": 2,
        "external_runtime_finish_calls": 1,
        "native_logging_calls": 1,
        "stock_finalize_and_snapshot_not_wrapped": false
      }
    },
    "host_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1401,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "bd5e5fb1febba25a1d8cd3ed60e4ebbe186fd9a62613cf8beba406742a670d86"
        }
      ],
      "value": [
        {
          "actual_eos_argument": 1,
          "entity_length": 23,
          "gid": 65534,
          "input_size": 23,
          "invalid": false,
          "kind": "patched_request_body_hook",
          "monotonic_ns": 103684697161559,
          "pid": 298,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 1,
          "stream_offset": 0,
          "uid": 65534
        },
        {
          "actual_eos_argument": 0,
          "entity_length": -1,
          "gid": 65534,
          "input_size": 24,
          "invalid": false,
          "kind": "patched_response_body_hook",
          "monotonic_ns": 103684704297760,
          "pid": 298,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 2,
          "stream_offset": 0,
          "uid": 65534
        },
        {
          "actual_eos_argument": 1,
          "entity_length": -1,
          "gid": 65534,
          "input_size": 0,
          "invalid": false,
          "kind": "patched_response_body_hook",
          "monotonic_ns": 103684704484927,
          "pid": 298,
          "runtime_allocation_scope_call": 2,
          "schema": "lighttpd-physical-host-v1",
          "sequence": 3,
          "stream_offset": 24,
          "uid": 65534
        }
      ]
    },
    "native_eos": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 1401,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/host-eos.jsonl",
          "role": "host_callback",
          "sha256": "bd5e5fb1febba25a1d8cd3ed60e4ebbe186fd9a62613cf8beba406742a670d86"
        },
        {
          "bytes": 146443,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "10a469886c82dbd4c8d906cefa7a181fbfe795847facd0c06ba1363ea7d88565"
        }
      ],
      "value": {
        "definition": "Actual accepted native patched eos argument, or actual finite Content-Length consumed branch, plus same typed Runtime/native finalization calls.",
        "native_append_eos_argument": null,
        "native_request_finalization": 1,
        "native_response_finalization": 1
      }
    },
    "native_free_calls": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 146443,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/native-api.jsonl",
          "role": "native_api",
          "sha256": "10a469886c82dbd4c8d906cefa7a181fbfe795847facd0c06ba1363ea7d88565"
        }
      ],
      "value": {
        "common_cleanup": 1,
        "native_cleanup": 1,
        "runtime_free_correlation_known": true,
        "typed_runtime_destroy": 1,
        "unjoined_external_destroy_rows": []
      }
    },
    "product_host_identity": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 17111,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/receipts/before-main/backend.maps",
          "role": "loaded_image",
          "sha256": "aa179607d14195ca0f956e43d2855e41eb996850166ce3ea073b666efb6b2975"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/receipts/before-main/backend.status",
          "role": "loaded_image",
          "sha256": "af32dbf693b4304ef07f1578dd0dded5b1cc764f08b73637c9bbe04b3ec747ba"
        },
        {
          "bytes": 28401,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/receipts/before-main/host.maps",
          "role": "loaded_image",
          "sha256": "2357a28cab33ed125b9fee8f83ed55ea7a1c47d52965fe0a7ea68656860100b5"
        },
        {
          "bytes": 1498,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/receipts/before-main/host.status",
          "role": "loaded_image",
          "sha256": "106b855b72fa01e6275d9d1ad757027fc3ea1741098ce64659081fe253b26f50"
        },
        {
          "bytes": 4626,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/controller-result.json",
          "role": "isolation_receipt",
          "sha256": "19e316e0c4243a407fb7139b4eb4f4c8dddff8fbbbd399f4bede2506a71606ba"
        },
        {
          "bytes": 1766976,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/owned/patched-host/bin/lighttpd",
          "role": "loaded_image",
          "sha256": "b82f8c0c70c419c30446faad1a3f8094722ff18b37add72270ae716d48d6f2ce"
        },
        {
          "bytes": 380280,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/owned/patched-host/modules/mod_msconnector.so",
          "role": "loaded_image",
          "sha256": "2ca714ffab2866fc996cf10cc9a68e22447629a08a30286ac26e73a7b8d50656"
        },
        {
          "bytes": 2034032,
          "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
          "role": "loaded_image",
          "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
        },
        {
          "bytes": 4031,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/lighttpd-patched-native-mapped-image-version-01.json",
          "role": "loaded_image",
          "sha256": "1d66789aa116550ef3927cd38ffa0955e8a3c5362c5a1cf2672f0e2a24d87f24"
        }
      ],
      "value": {
        "actual_actors": {
          "backend": {
            "actual_launcher_pid": 289,
            "actual_launcher_starttime": "10368081",
            "argv": [
              "rtk",
              "proxy",
              "/usr/local/bin/python3",
              "/mnt/fixtures/backend-launch.py",
              "18152"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "pipe:[2103235]",
              "2": "pipe:[2103236]",
              "3": "socket:[2108712]"
            },
            "maps_sha256": "aa179607d14195ca0f956e43d2855e41eb996850166ce3ea073b666efb6b2975",
            "pid": 290,
            "starttime": "10368081",
            "status_sha256": "af32dbf693b4304ef07f1578dd0dded5b1cc764f08b73637c9bbe04b3ec747ba"
          },
          "host": {
            "actual_launcher_pid": 297,
            "actual_launcher_starttime": "10368455",
            "argv": [
              "rtk",
              "proxy",
              "/task/lighttpd/owned/patched-host/bin/lighttpd",
              "-D",
              "-m",
              "/task/lighttpd/owned/patched-host/modules",
              "-f",
              "/task/lighttpd/lighttpd.conf"
            ],
            "fds": {
              "0": "/dev/null",
              "1": "/dev/null",
              "10": "/task/lighttpd/events.jsonl",
              "11": "pipe:[2109473]",
              "12": "pipe:[2109473]",
              "2": "pipe:[2105870]",
              "3": "/task/native-api.jsonl",
              "4": "/task/lighttpd/lighttpd.pid",
              "5": "socket:[2109471]",
              "6": "/task/lighttpd/logs/lighttpd-error.log",
              "7": "/task/lighttpd/audit/native-audit.log",
              "8": "/task/lighttpd/audit/native-debug.log",
              "9": "anon_inode:[eventpoll]"
            },
            "maps_sha256": "2357a28cab33ed125b9fee8f83ed55ea7a1c47d52965fe0a7ea68656860100b5",
            "pid": 298,
            "starttime": "10368455",
            "status_sha256": "106b855b72fa01e6275d9d1ad757027fc3ea1741098ce64659081fe253b26f50"
          }
        },
        "actual_host_version": "lighttpd/1.4.85 - a light and fast webserver",
        "mapped_image_identity": {
          "connector_module": {
            "actual_loaded_inode": 51517128,
            "actual_loaded_paths": [
              "/task/lighttpd/owned/patched-host/modules/mod_msconnector.so"
            ],
            "actual_mapping": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/receipts/before-main/host.maps",
              "sha256": "2357a28cab33ed125b9fee8f83ed55ea7a1c47d52965fe0a7ea68656860100b5"
            },
            "captured_namespace_map_devices": [
              "00:2d"
            ],
            "device_scope": "Captured namespace mapping and later tool stat expose different device aliases. No cross-environment device equality is claimed. Exact mapped path, retained inode, sealed input/copy guards and physical image SHA bind the image.",
            "physical_image": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/owned/patched-host/modules/mod_msconnector.so",
              "role": "loaded_image",
              "sha256": "2ca714ffab2866fc996cf10cc9a68e22447629a08a30286ac26e73a7b8d50656"
            },
            "retained_file_current_device": [
              0,
              47
            ]
          },
          "host_binary": {
            "actual_loaded_inode": 51517126,
            "actual_loaded_paths": [
              "/task/lighttpd/owned/patched-host/bin/lighttpd"
            ],
            "actual_mapping": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/receipts/before-main/host.maps",
              "sha256": "2357a28cab33ed125b9fee8f83ed55ea7a1c47d52965fe0a7ea68656860100b5"
            },
            "captured_namespace_map_devices": [
              "00:2d"
            ],
            "device_scope": "Captured namespace mapping and later tool stat expose different device aliases. No cross-environment device equality is claimed. Exact mapped path, retained inode, sealed input/copy guards and physical image SHA bind the image.",
            "physical_image": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/owned/patched-host/bin/lighttpd",
              "role": "loaded_image",
              "sha256": "b82f8c0c70c419c30446faad1a3f8094722ff18b37add72270ae716d48d6f2ce"
            },
            "retained_file_current_device": [
              0,
              47
            ]
          },
          "loaded_native_sdk": {
            "actual_loaded_inode": 16208420,
            "actual_loaded_paths": [
              "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14"
            ],
            "actual_mapping": {
              "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/receipts/before-main/host.maps",
              "sha256": "2357a28cab33ed125b9fee8f83ed55ea7a1c47d52965fe0a7ea68656860100b5"
            },
            "captured_namespace_map_devices": [
              "00:22"
            ],
            "device_scope": "Captured namespace mapping and later tool stat expose different device aliases. No cross-environment device equality is claimed. Exact mapped path, retained inode, sealed input/copy guards and physical image SHA bind the image.",
            "physical_image": {
              "path": "/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14",
              "role": "loaded_image",
              "sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
            },
            "retained_file_current_device": [
              0,
              35
            ]
          }
        },
        "native_actor": {
          "actual_launcher_pid": 297,
          "actual_launcher_starttime": "10368455",
          "argv": [
            "rtk",
            "proxy",
            "/task/lighttpd/owned/patched-host/bin/lighttpd",
            "-D",
            "-m",
            "/task/lighttpd/owned/patched-host/modules",
            "-f",
            "/task/lighttpd/lighttpd.conf"
          ],
          "fds": {
            "0": "/dev/null",
            "1": "/dev/null",
            "10": "/task/lighttpd/events.jsonl",
            "11": "pipe:[2109473]",
            "12": "pipe:[2109473]",
            "2": "pipe:[2105870]",
            "3": "/task/native-api.jsonl",
            "4": "/task/lighttpd/lighttpd.pid",
            "5": "socket:[2109471]",
            "6": "/task/lighttpd/logs/lighttpd-error.log",
            "7": "/task/lighttpd/audit/native-audit.log",
            "8": "/task/lighttpd/audit/native-debug.log",
            "9": "anon_inode:[eventpoll]"
          },
          "maps_sha256": "2357a28cab33ed125b9fee8f83ed55ea7a1c47d52965fe0a7ea68656860100b5",
          "pid": 298,
          "starttime": "10368455",
          "status_sha256": "106b855b72fa01e6275d9d1ad757027fc3ea1741098ce64659081fe253b26f50"
        },
        "raw_loaded_maps_and_status_retained": true,
        "sdk_version": "3.0.14",
        "selected_sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"
      }
    },
    "source_config_binding": {
      "applicable": true,
      "evidence": [
        {
          "bytes": 242701,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/source-03-ledger.json",
          "role": "source_manifest",
          "sha256": "71dc56eda9ad0c4978b2d8b7457ebc0311d94406718e74a4dbc56fee214664da"
        },
        {
          "bytes": 536,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/source-03-compilation-binding.json",
          "role": "source_manifest",
          "sha256": "604252f51f18bb7d11a06a64c6c1f958a4a30a5cfb1272ee00631ce0b4352abf"
        },
        {
          "bytes": 17072,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/baseline-product-equality.json",
          "role": "source_manifest",
          "sha256": "020f0fe06179fa1bce00a806b07a13c2c4963fbb54a6892e6dccf0c526c7a4fb"
        },
        {
          "bytes": 19717,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/apache-lifecycle/lighttpd-preparation/build-03/build-receipt.json",
          "role": "source_manifest",
          "sha256": "2ef9d307cb0e8b06be0cfae1ccdb07bdc190002c2c15eda4ee83e513283f4188"
        },
        {
          "bytes": 374,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/runtime.conf",
          "role": "effective_configuration",
          "sha256": "1e3669c9d6244f86e66134d8b72f5cd1acb5a86b6487cf0fc46a3a63dfe7a33f"
        },
        {
          "bytes": 578,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/lighttpd.conf",
          "role": "effective_configuration",
          "sha256": "99e40c6484f0aef7874ac6f000ee4da6623f4a817b1d4e6cf7f64cbbc821eae4"
        },
        {
          "bytes": 639,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/isolation/attempt-1792013292009528678/data/lighttpd/rules.conf",
          "role": "effective_configuration",
          "sha256": "29e3c335c0b6c4a3603de704bc5ffe3bfc6ddb74bfacb4ac37f521ad72da943a"
        },
        {
          "bytes": 116,
          "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-readonly-revisions-01.json",
          "role": "source_manifest",
          "sha256": "7626580d3e02904f25e1ebc03852abab8596c3d78cf092a2e3b2658f5514a0cf"
        }
      ],
      "value": {
        "actual_baseline_product_input_equality_count": 149,
        "baseline_product_contract": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
        "direct_supplement": true,
        "immutable_test_only_callbacks_explicit": true,
        "legacy_whole_harness_namespace_blocker_preserved": true,
        "real_parent_base": "02754040bced960cfc1857416cd7101bb3116ef4"
      }
    }
  },
  "packet_identity": {
    "effective_config_sha256": "99e40c6484f0aef7874ac6f000ee4da6623f4a817b1d4e6cf7f64cbbc821eae4",
    "framework_sha": "99a7985c1be92a2297b1b59208f64df6768f2cbf",
    "mrts_sha": "8a6bb546c4c81d8ffc7be801dceac60c6925685f",
    "parent_sha": "02754040bced960cfc1857416cd7101bb3116ef4",
    "product_contract_sha": "a9d48bb58aa948aea7d79e20cdf09d3f239b7808",
    "rules_sha256": "29e3c335c0b6c4a3603de704bc5ffe3bfc6ddb74bfacb4ac37f521ad72da943a",
    "run_id": "20261014T182400Z-lighttpd-patched-native"
  },
  "qualification_scope": "full_host_lifecycle",
  "receipt": {
    "bytes": 366484,
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/root-approved-lighttpd-patched-native-02.json",
    "sha256": "362b0ff4370582872d51360dfdab081bcf66c22eb92535bf9cb93261c7e37c6f"
  },
  "status": "PASS",
  "unknown_fields": []
}
```

## Geprüfte Eingabequellen

- ledger: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/twentyone-qualified-08.json` — SHA256 `a3a901db7d70884d2f491c95246629071cd55280ad94ee0fd86049c2e954c7ff`.
- reconciliation: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/oracles/twentyone-source-confirmed-13/oracle-reconciliation.json` — SHA256 `cfe5c3dbd5b54c1199f070b5b206066862451a08f634a1ac2a16f0c678b7fd50`.
- source-status: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/source-status-05.json` — SHA256 `50a54854c8af34c3e8f51eeb234d91d04be6c3c7b0f6db995fcd30edf78f1554`.

## Unveränderte historische Quellen

Die verlinkten unveränderten Berichte dokumentieren den historischen Stand. Ihre CI-/Sonar-Ergebnisse gelten nur für den dort bezeichneten alten Head.

- historical-host-de: [historical-host-de](history/pr-382-i12-host-evidence-20261014.de.md) — SHA256 `79c499a98e8e7e46793eb8cf8abf6121f84c3e52941bbb309c1daba341de1e57`.
- historical-index-de: [historical-index-de](history/pr-382-i12-missing-case-index-20261014.de.md) — SHA256 `cfa30ce15d975e87de6d5241577de1f90eda45f2ec9ee85340d9569c09b7c8f1`.

[Vollständiger geordneter Index](pr-382-i12-missing-case-index-20261014.de.md).
