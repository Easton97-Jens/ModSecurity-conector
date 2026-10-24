# I12 NGINX-Nachweise, 2026-10-15

**Sprache:** [English](pr-410-i12-nginx-evidence-20261015.md) | Deutsch

Generiert durch `ci/runtime/lifecycle/i12/nginx/report.py`; Eingaben oder Generator ändern.

## Status und Nachweisgrenzen

Die 140 ausgewählten ursprünglichen IDs bleiben maßgeblich. Nur ein freigegebenes vollständiges ausgewähltes Hostpaket qualifiziert einen Lifecycle-PASS. Kandidatenbeobachtungen, native Unit-Tests, Konfigurationsprüfungen und Aliase qualifizieren keine zusätzlichen Requests.

Die aktuelle vollständige Qualifikation umfasst **71/140 ursprüngliche IDs**: **67 PASS** und **4 FAIL**. **69 IDs** haben weiterhin keine vollständige Lifecycle-Qualifikation. Die Basisqualifikation löste 1 der ursprünglich 43 offenen Oracle-Erwartungen auf, und neue Nachweise lösen 33 auf; **9 bleiben offen**.

```json
{
  "original_ids": 140,
  "original_open_oracles": 43,
  "baseline_resolved_original_oracles": 1,
  "baseline_unresolved_original_oracles": 42,
  "newly_resolved_original_oracles": 33,
  "new_source_confirmed_original_oracles": 33,
  "remaining_original_open_oracles": 9,
  "historical_rows_with_partial_execution": 97,
  "historical_execution_composition": {
    "native": 42,
    "canonical": 14,
    "configuration": 10,
    "derived": 31
  },
  "new_qualified_original_ids": 71,
  "newly_qualified_original_ids": 70,
  "retested_previously_qualified_original_ids": 1,
  "new_selected_physical_host_requests": 71,
  "distinct_full_lifecycle_qualified_original_ids": 71,
  "full_lifecycle_pass": 67,
  "full_lifecycle_fail": 4
}
```

Die ursprünglich 43 offenen Oracle-Erwartungen und ihre Basisabstimmung bleiben ohne explizite geprüfte Ergänzung unverändert. Eine Quellinterpretation allein erzeugt keinen neuen erfolgreichen Hostrequest.

## Historische Nachweise und Oracle-Semantik

Die historischen 60-Fall-Batches behalten 57 vom Harness gemeldete bestandene Fälle, zwei Konfigurationsfehler und ein veraltetes Log-Oracle; diese Harness-Ergebnisse sind keine vollständige Lifecycle-Qualifikation. Fixture-/Oraclefehler bleiben von echten Hostausführungen und Produktfehlern getrennt. Die ursprünglichen 42 nativen und 14 kanonischen Ausführungen behalten ihre ursprünglichen Revisionen: Hostbasis `3a1bafecd0c38ccf20427d580c767ed42addf4aa`, Produktvertrag `a9d48bb58aa948aea7d79e20cdf09d3f239b7808`. Die 31 abgeleiteten Zeilen, Aliase und wiederverwendeten YAML-Dateien sind keine unabhängigen zusätzlichen Requests.

Technischer Mapperfehler ergibt HTTP 500; tatsächlich ungültige Clientheader ergeben HTTP 400. Native-Override-, P1- und P2-Erwartungen erfordern die tatsächliche ausgewählte Quell-/Hostbindung; widersprüchliche ursprüngliche P2-Erwartungen dürfen nicht stillschweigend zur beobachteten P1-Ablehnung umetikettiert werden. Die SDK-3.0.14-MIME-Fixture09 behält ihre MIME-Listensemantik ohne erfundenen `Clear`-Reset; separat gemessene Fixture08 ersetzt Fixture09 nicht.

Die Body-Null-Mapper-Fixture erreicht die technische Validierung in P1, obwohl ihr ursprüngliches ausgewähltes Oracle P2 verlangt. Ihre HTTP-500-Regression belegt die reparierte Statuszuordnung; sie erfüllt diesen ursprünglichen Phasenvertrag nicht. Der separat reproduzierte Fehler `NEED-request-empty` ist ein Produktfehler: NGINX liefert einen gültigen leeren Terminalbuffer mit Nullzeigern für `pos`/`last`, den der Connector vor P2 als ungültigen Requestbody-Bufferbereich ablehnt. Reguläres und beobachtetes Modul reproduzieren dieses Verhalten. Die produktive Korrektur gehört separat zu #382.

Geprüfte Oracle-Korrekturen unterscheiden P1-Timeout vor Commit (HTTP 504), P4-Timeout nach Commit (sichtbares HTTP 200 mit abgebrochenem Body) und natives Responsebody-Reject nach Commit (sichtbares HTTP 200 mit unvollständigem Framing). Diesen Ergebnissen wird kein erfundener Regelmatch zugeordnet. Native Invalid-Return-Injektion bleibt von einer SDK-Regelintervention getrennt. ProcessPartial und Reject werden anhand nativer Rückgaben und physischer Events des ausgewählten Requests beurteilt.

Die ursprünglichen verpflichtenden Eventfelder bleiben durch diese Korrekturen unverändert. `phase4_body_reject` besteht mit seinen ursprünglich verlangten Feldern. Beide Timeoutfälle sind vollständig beobachtete FAIL: Die ursprünglichen Eventmetadaten `run_id`, `transport_case_id` und `connection_id` fehlen. Zusammen mit dem Body-Null-P2-Fixturekonflikt und `NEED-request-empty` ergeben sich die vier qualifizierten FAIL-Ergebnisse; nur der Fall mit leerem Request wird hier als bestätigter Produktfehler eingestuft. Der Request-ProcessPartial-Fall erfasst zwei native Append-Rückgaben von 0, gefolgt von nativem Requestbody-Processing mit Rückgabe 1; eine Null-Append-Rückgabe ist selbst kein EOS.

Der unabhängige SDK-3.0.14-Probe misst eine leere MIME-Menge für `Clear` gefolgt von Add in einem Ladevorgang, einen Eintrag für Add allein und eine leere Menge für Add gefolgt von `Clear`. Fixture09 verzichtet bewusst auf `Clear`; ihr NGINX-spezifisches MIME-Verhalten bleibt erhalten. Charset- und nicht unterstützte MIME-Beobachtungen erzeugen weder einen Konfigurationsreset noch ein Requestbody-MIME-Gate.

## Physische Lifecycle-Beobachtungen

Die referenzierten Kandidatenzusammenfassungen behalten tatsächliche Root-Master-/Nobody-Worker-Identität, geladene Connector-/SDK-Mappings, Clientprozess-Exit/Signal, exakte Bytes und Framing, native API-Rückgaben, physische Events, Commitreihenfolge, Finish/Free sowie Nachbar-/Cleanup-Messungen soweit verfügbar. Unbekannte Messungen bleiben unbekannt. Host-Terminalcallbacks zusammen mit nativem Process-Body-Eintritt belegen die gemessene EOS-Grenze; Client-EOF und Nullbyte-Append belegen kein natives EOS. HTTP/1-Beobachtungen beweisen kein HTTP/2-Resetverhalten.

```json
{
  "input": {
    "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/review-suite04-v2/candidate-summary.json",
    "sha256": "377da25733fc659195c14eb16a43343c8ac89228aea65bbde39b439cbf412a55",
    "bytes": 144605
  },
  "scope": "PROPOSED only; no oracle evaluation or PASS",
  "attempt": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/isolation/attempt-1792074468580254910",
  "controller_exit": 0,
  "driver_exit": 0,
  "proposed_packets": 93,
  "full_lifecycle_qualified": false
}
```

```json
{
  "input": {
    "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/final-provenance.json",
    "sha256": "c658a12ca5e73330afc984d7f042bb6ed656ed05185241f9801cdcd7d664a7af",
    "bytes": 460786
  },
  "source_head": "f27eb59b53beff6f65384fc2e5037881a3052c01",
  "branch": "codex/i12-nginx-410-20261015",
  "base": "work/pr382-i12-host-evidence-20261011",
  "scope": "Final derived NGINX-only evidence provenance; partial host observations never imply PASS.",
  "sdk_mime": {
    "receipt": {
      "passed": true,
      "scope": "Actual native SDK3.0.14 MIME merge: Clear+add and add+Clear both empty; add alone text/plain retained. No host qualification.",
      "sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
      "source_sha256": "3f0ada7c405a54a28462359711f800ff4e18d0f2bb205b217fb5dfac82a05e0a",
      "steps": [
        {
          "argv": [
            "rtk",
            "proxy",
            "c++",
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-isystem",
            "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk/include",
            "/var/tmp/codex/ModSecurity-conector/worktrees/i12-nginx-410-20261015/ci/runtime/lifecycle/i12/objects/text/3f0ada7c405a54a28462359711f800ff4e18d0f2bb205b217fb5dfac82a05e0a-test-sdk-mime-merge09.cpp",
            "-L/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk/lib",
            "-Wl,-rpath,/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk/lib",
            "-lmodsecurity",
            "-o",
            "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/sdk-mime/mime-merge"
          ],
          "exit": 0,
          "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        },
        {
          "argv": [
            "rtk",
            "proxy",
            "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/sdk-mime/mime-merge"
          ],
          "exit": 0,
          "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "stdout_sha256": "5e357346d4858b6c9a54cb7674e282b9ddbb1dec667224055fc864b9eaa9e12c"
        }
      ]
    },
    "semantics": "SDK 3.0.14: Clear+add yields zero entries, add alone retains text/plain, add+Clear yields zero entries; NGINX fixture09 deliberately omits Clear. No reset-to-default result is inferred."
  },
  "product_defect": {
    "case_id": "I12::nginx-native::NEED-request-empty",
    "semantics": "NGINX core constructs a valid zero-length terminal buffer; NULL pos/last rejected by connector before native P2. Product source unchanged in this I12 branch.",
    "source_references": [
      {
        "bytes": 75919,
        "kind": "native_engine_contract",
        "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/nginx-lifecycle/upstream-oracle-v3.0.14/transaction.cc",
        "revision": "libModSecurity-3.0.14",
        "sha256": "328ffa3b4517f0242450293a916aba4f512b4defc3bd1fcc7465e0778adc725c"
      },
      {
        "bytes": 8057,
        "kind": "independent_host_probe",
        "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/isolation/attempt-1792074468580254910/data/nginx-suite/NEED-request-empty/full-observation-receipt.json",
        "revision": "attempt-1792074468580254910",
        "sha256": "6584371e0a842d2a62abe43d3dcdf64aa56e9d85ff09b84ce27e0d55a007a79f"
      },
      {
        "bytes": 35486,
        "kind": "official_host_contract",
        "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/nginx-src/src/http/ngx_http_request_body.c",
        "revision": "nginx-1.31.6",
        "sha256": "5faaeede37d3a56f9d0f0ba35015fd19a0c78cd6c453f90eb14173d213834c2d"
      },
      {
        "bytes": 38944,
        "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/build/current/source-observed/connectors/nginx/src/ngx_http_modsecurity_access.c",
        "sha256": "b1de59b6e42576dcf865142f06dd4e600302fbe8510b4fc1b69598c65d2309f6"
      },
      {
        "bytes": 47429,
        "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/build/current/source-observed/connectors/nginx/src/ngx_http_modsecurity_body_filter.c",
        "sha256": "932c719390c7a42b7421e85c61b130b474d1c5d0a473301443783c25cc89feae"
      },
      {
        "bytes": 11602,
        "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/build/current/source-observed/connectors/nginx/src/ngx_http_modsecurity_mapper.c",
        "sha256": "f6e81c6a53c10849c92538158951f61137cc180ec287aa1e337bf32d0ec5618f"
      },
      {
        "bytes": 38520,
        "kind": "uninstrumented_product_source",
        "lines": [
          779,
          788
        ],
        "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/build/current/source-ordinary/connectors/nginx/src/ngx_http_modsecurity_access.c",
        "sha256": "3ad4e4d801672b0aec1c94326e6e0a2e12e2422e57d1e747121a0bbc2c1b73c8"
      }
    ],
    "target": "#382 separate product fix"
  },
  "remaining_original_open_oracle_ids": [
    "I12::nginx-native::NEED-missing-eos",
    "I12::nginx-native::NEED-invalid-metadata",
    "I12::nginx-native::NEED-physical-event-sink-open",
    "I12::nginx-native::NEED-physical-event-sink-write",
    "I12::nginx-native::NEED-physical-event-sink-short-write",
    "I12::nginx-native::NEED-physical-event-sink-flush",
    "I12::nginx-native::NEED-physical-event-sink-close",
    "I12::nginx-native::NEED-cancel",
    "I12::nginx-native::NEED-current-h1-matrix-not-r17"
  ],
  "build_identity": {
    "nginx_binary_sha256": "0d2287b344a1af4c6cc986dd915c09c60f3c942ec8ae76f8bdc5456506939746",
    "observed_module_sha256": "ed3dceae9faeee87c17009d8f3bf1d541e6abd53e7541b906bb9fc4b9cd78b49",
    "ordinary_module_sha256": "cf17829a9e21a9f0a5cc9e86a6b0c43e81398913fe3283259532e70419cdb748",
    "sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
    "sdk_version": "3.0.14"
  },
  "compiled_parent_unit_count": 33,
  "compiled_nginx_generated_unit_count": 1,
  "suite": {
    "candidates_with_gaps_or_unknowns": 4,
    "cleanup_verified_count": 93,
    "client_exit_counts": {
      "0": 84,
      "2": 9
    },
    "client_signal_counts": {
      "None": 93
    },
    "complete_observation_candidates": 89,
    "diagnostic_requests": 1,
    "direct_wait_pid_matches": 93,
    "framing_complete_counts": {
      "False": 9,
      "True": 84
    },
    "framing_counts": {
      "http1.1-chunked": 2,
      "http1.1-content-length": 82,
      "unknown": 9
    },
    "http_status_counts": {
      "200": 60,
      "302": 3,
      "400": 4,
      "403": 17,
      "429": 2,
      "500": 5,
      "504": 2
    },
    "master_signal_counts": {
      "None": 93
    },
    "master_wait_counts": {
      "0": 93
    },
    "measured_assertion_counts": {
      "actual_loaded_image_binding": {
        "True": 93
      },
      "callbacks_owned_by_worker": {
        "False": 4,
        "True": 89
      },
      "client_body_digest_size_match": {
        "True": 93
      },
      "common_finish_once": {
        "True": 89,
        "unknown": 4
      },
      "config_loaded": {
        "True": 93
      },
      "host_cleanup_verified": {
        "True": 93
      },
      "native_cleanup_once": {
        "True": 89,
        "unknown": 4
      },
      "native_invalid_rows_absent": {
        "True": 93
      },
      "native_logging_once": {
        "True": 89,
        "unknown": 4
      },
      "raw_artifact_digests_match": {
        "True": 93
      },
      "receipt_errors_empty": {
        "True": 93
      },
      "request_terminal_to_p2_once": {
        "False": 18,
        "True": 71,
        "unknown": 4
      },
      "response_terminal_to_p4_once": {
        "False": 30,
        "True": 59,
        "unknown": 4
      },
      "scoped_fixture_traces_bind_selected_transaction": {
        "True": 89,
        "unknown": 4
      },
      "selected_allocation_unique": {
        "False": 4,
        "True": 89
      },
      "selected_native_nobody": {
        "False": 4,
        "True": 89
      },
      "selected_transaction_unique": {
        "False": 4,
        "True": 89
      }
    },
    "neighbor_success_count": 93,
    "physical_host_requests": 93,
    "receipt_errors": [],
    "root_master_nobody_worker_count": 93,
    "selected_original_requests": 92
  },
  "qualified_failures": [
    {
      "case_id": "I12::nginx-native::NEED-request-empty",
      "cause": "Confirmed product defect: valid empty terminal NGINX body buffer has NULL pos/last; connector rejects before P2 with HTTP 500. Separately reproduced with ordinary module; product fix belongs to #382."
    },
    {
      "case_id": "I12::nginx-native::body_size_nonzero_with_null_data",
      "cause": "Fixture/contract phase conflict: injected technical body mapper fault is HTTP 500 in P1; selected original requirement expects P2."
    },
    {
      "case_id": "I12::nginx-native::engine_timeout_before_commit",
      "cause": "Original timeout metadata contract is unsatisfied; native/host timeout behavior and approved phase/status correction do not waive original mandatory physical event fields."
    },
    {
      "case_id": "I12::nginx-native::engine_timeout_after_commit",
      "cause": "Original timeout metadata contract is unsatisfied; native/host timeout behavior and approved phase/status correction do not waive original mandatory physical event fields."
    }
  ]
}
```

## Verifikation

Jede folgende Prüfung nennt ihr beobachtetes Ergebnis einschließlich fehlgeschlagener Setupversuche. Kompilierte/native/Mutationsprüfungen belegen ihre eigene Ebene und qualifizieren keinen Host-Lifecycle.

| Prüfung | Exit | Status | Befehl |
| --- | --- | --- | --- |
| adoption-security-contracts | 0 | passed | `rtk proxy make check-nginx-common-adoption check-nginx-c-standard-wiring check-common-security-contract PYTHON=python3` |
| cleanup-omission-compiled-mutation | 1 | failed | `rtk proxy python3 /var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/verification-native/cleanup_mutation_probe.py` |
| cleanup-omission-compiled-mutation-valid | 0 | passed | `rtk proxy python3 /var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/verification-native/cleanup_mutation_probe.py` |
| native-after-fixture-repair | 0 | passed | `rtk proxy python3 -m unittest -v tests.test_nginx_request_mapper_status tests.test_nginx_request_native_results tests.test_nginx_request_phase_completion tests.test_nginx_request_error_events tests.test_nginx_response_body_limit tests.test_nginx_body_buffer_fixture tests.test_nginx_p3_header_fixture tests.test_nginx_native_cleanup_bridge tests.test_nginx_phase4_native_body_source tests.test_nginx_phase4_mode_budget tests.test_nginx_engine_budget_bridge tests.test_nginx_merge_conf_c17 tests.test_nginx_native_security_contract tests.test_nginx_header_iteration_contract tests.test_nginx_intervention_url_ownership tests.test_nginx_error_page_intervention tests.test_nginx_native_logging tests.test_nginx_context_accounting tests.test_nginx_late_error_results` |
| native-c17-with-headers | 0 | passed | `rtk proxy python3 -m unittest -v tests.test_nginx_merge_conf_c17` |
| native-compiled-negative | 1 | failed | `rtk proxy python3 -m unittest -v tests.test_nginx_request_mapper_status tests.test_nginx_request_native_results tests.test_nginx_request_phase_completion tests.test_nginx_request_error_events tests.test_nginx_response_body_limit tests.test_nginx_body_buffer_fixture tests.test_nginx_p3_header_fixture tests.test_nginx_native_cleanup_bridge tests.test_nginx_phase4_native_body_source tests.test_nginx_phase4_mode_budget tests.test_nginx_engine_budget_bridge tests.test_nginx_merge_conf_c17 tests.test_nginx_native_security_contract tests.test_nginx_header_iteration_contract tests.test_nginx_intervention_url_ownership tests.test_nginx_error_page_intervention tests.test_nginx_native_logging tests.test_nginx_context_accounting tests.test_nginx_late_error_results` |
| nginx-adoption-mutations | 0 | passed | `rtk proxy python3 -m unittest -v tests.test_nginx_common_adoption` |

```json
{
  "input": {
    "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/sdk-mime/receipt.json",
    "sha256": "7a3f3ae3e168d70419bdb711f4d9396f81653f44689d91f0a0236a44d6fa4a90",
    "bytes": 1804
  },
  "summary": {
    "scope": "Actual native SDK3.0.14 MIME merge: Clear+add and add+Clear both empty; add alone text/plain retained. No host qualification.",
    "source_sha256": "3f0ada7c405a54a28462359711f800ff4e18d0f2bb205b217fb5dfac82a05e0a",
    "sdk_sha256": "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407",
    "steps": [
      {
        "argv": [
          "rtk",
          "proxy",
          "c++",
          "-std=c++17",
          "-Wall",
          "-Wextra",
          "-Werror",
          "-isystem",
          "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk/include",
          "/var/tmp/codex/ModSecurity-conector/worktrees/i12-nginx-410-20261015/ci/runtime/lifecycle/i12/objects/text/3f0ada7c405a54a28462359711f800ff4e18d0f2bb205b217fb5dfac82a05e0a-test-sdk-mime-merge09.cpp",
          "-L/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk/lib",
          "-Wl,-rpath,/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk/lib",
          "-lmodsecurity",
          "-o",
          "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/sdk-mime/mime-merge"
        ],
        "exit": 0,
        "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      },
      {
        "argv": [
          "rtk",
          "proxy",
          "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/sdk-mime/mime-merge"
        ],
        "exit": 0,
        "stdout_sha256": "5e357346d4858b6c9a54cb7674e282b9ddbb1dec667224055fc864b9eaa9e12c",
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      }
    ],
    "passed": true
  }
}
```


## Vollständiges 140-ID-Ledger

Das [Maschinenartefakt](../ci/runtime/lifecycle/i12/nginx/evidence-20261015.json) behält jeden ursprünglichen ausgewählten Vertrag als lesbare Projektion mit seinem kanonischen Vollvertragshash, Basisstatus, neuem Status und externen Rohbeleg-Locators. Pfadbezogene Quellhashes bleiben in der extern gebundenen Basis. Externe Basis und vollständiges Ledger sind unten durch SHA256 gebunden; schwere Rohdateien bleiben außerhalb von Git.

```json
{
  "baseline": {
    "path": "/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/ledger/twentyone-qualified-08.json",
    "sha256": "a3a901db7d70884d2f491c95246629071cd55280ad94ee0fd86049c2e954c7ff",
    "bytes": 34634475
  },
  "full_ledger": {
    "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/ledger/nginx-140-final.json",
    "sha256": "7fbe20b783d9b236ea6a66a26c60b34b99114459c72179a8a0cab003779a09c8",
    "bytes": 47957556
  },
  "observations": [
    {
      "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/review-suite04-v2/candidate-summary.json",
      "sha256": "377da25733fc659195c14eb16a43343c8ac89228aea65bbde39b439cbf412a55",
      "bytes": 144605
    },
    {
      "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/final-provenance.json",
      "sha256": "c658a12ca5e73330afc984d7f042bb6ed656ed05185241f9801cdcd7d664a7af",
      "bytes": 460786
    }
  ],
  "verification": [
    {
      "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/verification-native/verification-summary.json",
      "sha256": "2ed06585cc8d0d8926ec8336ce55472fbae1c573d6fdd097adfcd7b18b366315",
      "bytes": 19067
    },
    {
      "path": "/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015/sdk-mime/receipt.json",
      "sha256": "7a3f3ae3e168d70419bdb711f4d9396f81653f44689d91f0a0236a44d6fa4a90",
      "bytes": 1804
    }
  ]
}
```

### Qualifizierte ursprüngliche IDs

Jede folgende Zeile ist eine ursprüngliche ausgewählte ID. Pakethashes und unabhängige Requestidentitäten stehen im Maschinenartefakt; der erneute Test einer bereits qualifizierten ID fügt keine weitere ursprüngliche Anforderung hinzu.

| Ursprüngliche ID | Basis | Aktuell |
| --- | --- | --- |
| `I12::nginx-native::allow_without_marker` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::deny_header_marker_403` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::deny_with_alternative_status` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::deny_request_body_marker_403` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_rule_observed` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_deny_after_commit_log_only` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_deny_after_commit_abort` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_event_contains_original_status` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_event_contains_late_intervention_action` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::body_size_nonzero_with_null_data` | NOT_EXECUTED_UNQUALIFIED | FAIL |
| `I12::nginx-native::header_count_nonzero_with_null_headers` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::event_contains_connector` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::event_contains_transaction_id` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::event_contains_rule_id` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::event_contains_phase` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::event_contains_status` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::event_has_no_request_body_payload` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::event_has_no_response_body_payload` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::single_request_cleanup` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::allow` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::deny` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::log_only` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::redirect_if_supported` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase1_allow` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase1_deny_403` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase1_alternative_status` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase1_redirect` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase2_request_body_rule` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase2_no_payload_event` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_deny_after_commit_log_only_safe` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_deny_after_commit_abort_strict` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_status_metadata` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_action_metadata` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_no_payload_event` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::phase4_body_reject` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::engine_timeout_before_commit` | NOT_EXECUTED_UNQUALIFIED | FAIL |
| `I12::nginx-native::engine_timeout_after_commit` | NOT_EXECUTED_UNQUALIFIED | FAIL |
| `I12::nginx-native::NEED-request-empty` | NOT_EXECUTED_UNQUALIFIED | FAIL |
| `I12::nginx-native::NEED-request-single-chunk` | PASS | PASS |
| `I12::nginx-native::NEED-request-multiple-chunks` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-file` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-streaming` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-content-type-present` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-content-type-missing` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-charset-present` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-charset-missing` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-mime-scope-in` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-mime-scope-out` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-csv` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-eos-once` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-reject` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-process-partial` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-above-former-connector-limit` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-request-marker-at-payload-end` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-empty` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-single-chunk` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-file` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-streaming` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-charset-missing` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-csv` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-above-former-connector-limit` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-response-marker-at-payload-end` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-invalid-native-return` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-timeout` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-client-exit-signal` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-incomplete-framing` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-abort-reset-observation` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-neighbor-connection-stream` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-root-master-nobody-worker` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-native-memory-body` | NOT_EXECUTED_UNQUALIFIED | PASS |
| `I12::nginx-native::NEED-native-file-body` | NOT_EXECUTED_UNQUALIFIED | PASS |

### Ursprüngliche IDs weiterhin ohne vollständige Lifecycle-Qualifikation

Die zehn historischen Konfigurations-PASS bleiben Konfigurationsnachweise. Die Spalte für offene Oracles kennzeichnet ursprünglich offene Erwartungen ohne aufgelöstes geprüftes Oracle; andere Zeilen können ein bekanntes Oracle, aber unvollständige physische Belege besitzen. Die englischen Lückenbegründungen geben die kanonische hashgebundene Zuordnung unverändert wieder.

| Ursprüngliche ID | Aktuell | Ursprüngliches Oracle weiterhin offen | Fehlender Nachweis |
| --- | --- | --- | --- |
| `I12::nginx-native::transaction_id_present` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: transaction_id, rule_id. |
| `I12::nginx-native::transaction_id_generated_or_fallback` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: transaction_id, rule_id, phase. |
| `I12::nginx-native::deny_response_header_marker_403` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Original phase/rule/action/status and event-field semantics still require independent exact-contract review. |
| `I12::nginx-native::multiple_headers` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: rule_id, phase. |
| `I12::nginx-native::duplicate_header_names` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: rule_id, phase. |
| `I12::nginx-native::empty_header_value` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: rule_id, phase. |
| `I12::nginx-native::case_insensitive_header_name` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::invalid_content_length` | NOT_EXECUTED_UNQUALIFIED | false | Actual malformed-client HTTP 400 precedes connector transaction creation; no selected native transaction/allocation join or full lifecycle packet. |
| `I12::nginx-native::conflicting_content_length` | NOT_EXECUTED_UNQUALIFIED | false | Actual malformed-client HTTP 400 precedes connector transaction creation; no selected native transaction/allocation join or full lifecycle packet. |
| `I12::nginx-native::duplicate_transfer_encoding` | NOT_EXECUTED_UNQUALIFIED | false | Actual malformed-client HTTP 400 precedes connector transaction creation; no selected native transaction/allocation join or full lifecycle packet. |
| `I12::nginx-native::content_length_overflow` | NOT_EXECUTED_UNQUALIFIED | false | Actual malformed-client HTTP 400 precedes connector transaction creation; no selected native transaction/allocation join or full lifecycle packet. |
| `I12::nginx-native::event_metadata_truncation` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: truncated. |
| `I12::nginx-native::event_json_limit` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: truncated. |
| `I12::nginx-native::valid_rules_file` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::missing_rules_file` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::invalid_rule_syntax` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::unknown_config_key` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::invalid_boolean` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::invalid_status` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::invalid_size` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::unsafe_event_path` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::multiple_sequential_requests` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::keep_alive_requests_if_supported` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::early_mapping_failure_cleanup` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::transaction_begin_failure_cleanup` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::finish_failure_propagation` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::clean_shutdown` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::phase1_transaction_id` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. |
| `I12::nginx-native::phase3_response_header_rule` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Original phase/rule/action/status and event-field semantics still require independent exact-contract review. |
| `I12::nginx-native::phase3_deny_before_commit` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Original phase/rule/action/status and event-field semantics still require independent exact-contract review. |
| `I12::nginx-native::phase3_redirect_before_commit` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Original phase/rule/action/status and event-field semantics still require independent exact-contract review. |
| `I12::nginx-native::phase3_original_and_visible_status` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Original phase/rule/action/status and event-field semantics still require independent exact-contract review. |
| `I12::nginx-native::phase4_marker_split_across_chunks` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: marker_split_across_chunks, end_of_stream_evaluation. |
| `I12::nginx-native::phase4_end_of_stream_evaluation` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: end_of_stream_evaluation. |
| `I12::nginx-native::phase4_deny_after_commit_log_only_minimal` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: event, message_id, rule_id, phase, http_status, requested_action, actual_action, original_http_status, visible_http_status, late_intervention, late_intervention_mode, headers_sent, connection_aborted, transport_result. |
| `I12::nginx-native::phase4_invalid_scope_file` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::phase4_wildcard_scope_rejected` | PASS | false | Configuration-only historical result; no selected HTTP request/native lifecycle packet. Config PASS is retained at its original layer. |
| `I12::nginx-native::phase4_in_scope_content_type` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: content_type_scope. |
| `I12::nginx-native::phase4_content_type_with_charset` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: content_type_scope. |
| `I12::nginx-native::phase4_out_of_scope_content_type` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: content_type_scope. |
| `I12::nginx-native::phase4_missing_content_type` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: content_type_scope. |
| `I12::nginx-native::phase4_no_full_response_buffering` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: event, message_id, rule_id, phase, no_full_response_buffering, client_first_byte_received, first_byte_before_response_end, first_chunk_size, upstream_paused, upstream_eos_sent_at_first_byte, upstream_response_finished_at_first_byte, response_committed, body_bytes_seen, body_bytes_inspected. |
| `I12::nginx-native::phase4_first_byte_before_response_end` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: event, message_id, rule_id, phase, client_first_byte_received, first_byte_before_response_end, first_chunk_size, upstream_paused, upstream_eos_sent_at_first_byte, upstream_response_finished_at_first_byte, response_committed, body_bytes_seen, body_bytes_inspected. |
| `I12::nginx-native::transport_http11_content_length` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: transport_protocol, transfer_encoding. |
| `I12::nginx-native::transport_http11_chunked` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: transport_protocol, transfer_encoding. |
| `I12::nginx-native::transport_keep_alive` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: connection_reused, transport_protocol. |
| `I12::nginx-native::transport_sequential_requests` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: connection_reused, transaction_id. |
| `I12::nginx-native::phase4_body_at_limit` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: event, message_id, rule_id, phase, body_limit_outcome, body_bytes_seen, body_bytes_inspected, truncated. |
| `I12::nginx-native::phase4_body_over_limit` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: event, message_id, rule_id, phase, body_limit_outcome, body_bytes_seen, body_bytes_inspected, truncated. |
| `I12::nginx-native::phase4_body_process_partial` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: body_limit_outcome. |
| `I12::nginx-native::full_lifecycle_event_metadata_bounded` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: truncated, body_bytes_seen, body_bytes_inspected. |
| `I12::nginx-native::phase4_strict_http1_client_abort` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: run_id, transport_case_id, connection_id. |
| `I12::nginx-native::phase4_strict_host_survives` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: run_id, transport_case_id, connection_id. |
| `I12::nginx-native::phase4_strict_followup_request_succeeds` | NOT_EXECUTED_UNQUALIFIED | false | Own physical host request retained, but exact original oracle remains unqualified. Missing original physical event fields: run_id, transport_case_id, connection_id. |
| `I12::nginx-native::keepalive_allow_allow` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: run_id, integration_mode, transaction_id, rule_id, phase, event, message_id, requested_action, actual_action, transport_result, transport_case_id, connection_id, connection_reused, eos_seen, cleanup_reason. |
| `I12::nginx-native::keepalive_allow_deny_allow` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: run_id, integration_mode, transaction_id, rule_id, phase, event, message_id, requested_action, actual_action, transport_result, transport_case_id, connection_id, connection_reused, eos_seen, cleanup_reason. |
| `I12::nginx-native::keepalive_safe_followup` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: run_id, integration_mode, transaction_id, rule_id, phase, event, message_id, requested_action, actual_action, transport_result, transport_case_id, connection_id, connection_reused, eos_seen, cleanup_reason. |
| `I12::nginx-native::keepalive_after_strict_new_connection` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: run_id, integration_mode, transaction_id, rule_id, phase, event, message_id, requested_action, actual_action, transport_result, transport_case_id, connection_id, connection_reused, eos_seen, cleanup_reason. |
| `I12::nginx-native::response_short_write_resume` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: run_id, integration_mode, transaction_id, rule_id, phase, event, message_id, requested_action, actual_action, transport_result, transport_case_id, connection_id, write_result, eos_seen, cleanup_reason. |
| `I12::nginx-native::response_write_would_block_resume` | NOT_EXECUTED_UNQUALIFIED | false | No independently qualified distinct current host request for this exact original ID; retained historical or derived/alias observations cannot be transferred. Original required event fields: run_id, integration_mode, transaction_id, rule_id, phase, event, message_id, requested_action, actual_action, transport_result, transport_case_id, connection_id, write_result, eos_seen, cleanup_reason. |
| `I12::nginx-native::NEED-missing-eos` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-invalid-metadata` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-physical-event-sink-open` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-physical-event-sink-write` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-physical-event-sink-short-write` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-physical-event-sink-flush` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-physical-event-sink-close` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-cancel` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |
| `I12::nginx-native::NEED-current-h1-matrix-not-r17` | NOT_EXECUTED_UNQUALIFIED | true | Original mandatory scenario still lacks an independently reviewed exact effective fixture/oracle and its own complete selected lifecycle packet. |

## Verbleibende Arbeit und Risiken

Jede unqualifizierte Zeile benötigt weiterhin die oben konkret genannten physischen Nachweise. Nur die neun weiterhin offenen Oracle-Erwartungen benötigen zusätzlich ein aufgelöstes geprüftes Oracle. Native Reject-/ProcessPartial-Grenzen, Speicher-/Dateibuffer, MIME/Charset, P1–P4, technische Fehler vor/nach Commit, P4 Safe/unterstütztes Strict, leere/einzelne/mehrteilige Bodys und genau einmal EOS sind je ursprünglicher ID zu beurteilen und dürfen nie aus einem anderen Fall abgeleitet werden. Der bestehende Release-Secret-Blocker bleibt ungelöst. Jede bestätigte Produktkorrektur gehört separat zu #382. Diese Änderung autorisiert keinen Produktfix, Master-Merge oder Release.

Siehe auch [aktuellen I12-Index](pr-382-i12-missing-case-index-20261014.de.md) und [historische Nachweise](pr-382-i12-host-evidence-20261014.de.md).
