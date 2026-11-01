# Change Record: CR-20261101-host-execution-context-integration

**Sprache:** [English](CR-20261101-host-execution-context-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261101-host-execution-context-integration |
| Datum (UTC) | 2026-11-01 |
| Basis-Revision | `2abad408cae7e5a103d12a9a9e432129bfe0468f` |

## Motivation und Problemstellung

Die vorbereitete Parent-Routing-Anpassung für den Host-Ausführungskontext und das integrierte Framework-Preflight werden über einen eigenen Connector-Draft-PR geliefert. Fehlende Protokoll-APIs im aktuellen Parent-Quellcode verhindern die Freigabequalifikation. Diese Abhängigkeit bleibt sichtbar; Produktänderungen aus [PR #348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348) werden nicht übernommen.

## Akzeptanzkriterien

Die Draft-Lieferung erfordert einen auftragsbezogenen Diff, einen konsistenten Framework-Gitlink samt registrierten Projektionen, aktuelle Pin-/Provenienz- und Dokumentationsprüfungen, Secret-Scanning und die ausdrückliche Benennung der Abhängigkeit. Freigabereife erfordert zusätzlich den Apache-Vertrag, das eingecheckte Parent-/Framework-Paar, Artefaktzulassung, frischen NGINX-Hostlauf mit Launcher-/Cleanup-Nachweisen sowie aktuelle CI-/Sonar-Ergebnisse am exakten Head. Dieser Auftrag autorisiert keinen Merge.

## Implementierungsentscheidung und Begründung

Ausgewählt wird der integrierte Framework-Commit `5ef57603a4933f18c988f1f9f32b93f478182440` aus [Framework-PR #147](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/147), kein beweglicher Branch. Sein geprüfter PR-Head war `20f8d5bc36614d21dae1635a08c9206fc09da96b`; alle fünf Master-Workflows am Merge-Commit bestanden. Dieser PR-Head hatte Quality Gate OK, null neue Issues einschließlich akzeptierter Issues und null neue Security-Hotspots. Diese historischen Framework-Ergebnisse qualifizieren den neuen Connector-Head nicht. Generierte Projektionen werden ausschließlich durch `ci/tools/sync-framework-component-versions.py` aktualisiert. Der getrennte Framework-Code-Scanning-PR, #348 und MRTS bleiben außerhalb dieser Änderung.

## Geänderte Dateien

- `.codex/context/index.md` leitet Entscheidungen zum nativen Hostkontext an `.codex/context/security-runtime-preflight.md`; diese Datei verlinkt die dauerhafte Framework-Anleitung.
- `.codex/inheritance-manifest.toml` erneuert nur die beiden auftragsbezogenen Katalog-Hashes.
- `modules/ModSecurity-test-Framework` wählt den integrierten Framework-Commit; `project-versions.lock.json` und 22 registrierte `.github/workflows/`-Dateien enthalten die generierten gewöhnlichen SHA-Projektionen. Die 23 Projektionsziele ändern ausschließlich die registrierte alte Revision zur ausgewählten Framework-Revision: 54 Workflow-Verweise und ein Lock-Verweis. Geschützte und historische Identitäten bleiben unverändert.
- Dieser Bericht und `CR-20261101-host-execution-context-integration.md` dokumentieren die Parent-Liefergrenze.

Die versionierte dauerhafte Anleitung liegt unter `modules/ModSecurity-test-Framework/docs/host-execution-context.md` mit ihrer `.de.md`-Begleitung. Connector-Produktquellcode und MRTS-Dateien gehören nicht zu diesem Diff.

## Ausgeführte Befehle

Frische Prüfungen an Worktree-Basis `2abad408cae7e5a103d12a9a9e432129bfe0468f` mit Framework `5ef57603a4933f18c988f1f9f32b93f478182440` bestanden ohne Skips: 13 Preflight-Tests (4.609 s), sieben Integrationstests (0.681 s) und neun Pin-/Provenienz-Vertragstests (13.577 s). Der native Projektionscheck meldete `changed=[]`; der Kandidatenvertrag bestätigte die tatsächliche und erwartete Framework-Revision. Der Apache-Vertrag scheiterte mit Exit 2, weil seine geerbte Phase-3-Assertion den fehlenden Helfer für das ausgehandelte Protokoll verlangt. Auch die explizite Common-C17-API-Kompilierung mit `ON_DEMAND_TESTS=1` scheiterte mit Exit 2: unbekannter `msconnector_late_intervention_context`, fehlende `protocol_kind_parse`/`name`/`is_multiplexed`/`context_init`/`resolve_for_context` sowie nicht deklarierte HTTP-Enums und `STREAM_RESET`. Dies sind Kompatibilitätsblocker; Erwartungen wurden nicht angepasst. Diese Worktree-Prüfungen sind keine Qualifikation des endgültigen eingecheckten Heads.

Alle lokalen Befehle verwenden RTK und den vorgeschriebenen Framework-Interpreter; Quellzugriffe folgen dem Secret-Scanning-Protokoll des Repositorys. Private Berichte, exakte Befehlsbelege und Rohlogs bleiben außerhalb von Git. Das quellbezogene Secret-Scanning bestand vor Zugriff mit der vorhandenen Framework-Konfiguration, ohne neue oder geänderte Scanner-Ausnahmen oder Konfiguration. Gitleaks 8.30.1 bestand außerdem für alle 28 geänderten regulären Dateien vor dem Staging. Das Manifest der gescannten Bytes bleibt extern und muss den gestagten Blobs entsprechen. Native Prüfungen für Zweisprachigkeit, Pfade/Links und Change-Record-Struktur bestanden. Tatsächliche CI-/Sonar-Ergebnisse am PR-Head bleiben von dieser lokalen Evidenz getrennt.

Die folgende Übertragung fasst das identische beobachtete RTK-/Umgebungspräfix in `checked` zusammen; Pfadaliase bezeichnen den ausgewählten Parent-Worktree, seine Framework-Wurzel, den vorgeschriebenen Interpreter und die genehmigte externe Taskwurzel. Ausgeführte Selektoren und Flags bleiben erhalten. `CONNECTOR_REVISION` bezeichnet die Worktree-Basis, keinen künftigen Liefer-Head. Das zugelassene `framework-common-merged.sh` wurde aus dem ausgewählten Framework-Commit extrahiert. Das Common-Standardziel endete für seine ausgewählten Standardszenarien mit Exit 0; es führte nicht den vollständigen Compilercheck der fehlenden APIs aus.

```sh
checked() {
  rtk bypass env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=$TASK_ROOT/private TMPDIR=$TASK_ROOT/tests PYTHONPATH=$FRAMEWORK_ROOT:$FRAMEWORK_ROOT/connector_suite TEST_ROOT=$FRAMEWORK_ROOT FRAMEWORK_ROOT=$FRAMEWORK_ROOT FRAMEWORK_REVISION=5ef57603a4933f18c988f1f9f32b93f478182440 CONNECTOR_ROOT=$PARENT_ROOT CONNECTOR_REVISION=2abad408cae7e5a103d12a9a9e432129bfe0468f CONNECTOR_TEST_PROFILE=h1 CONNECTOR_TEST_OUTPUT_ROOT=$TASK_ROOT/tests EXECUTION_CONTEXT_TEST_ROOT=$TASK_ROOT/tests "$@"
}
checked $FRAMEWORK_PYTHON -P -m unittest -v \
    modsecurity_connector_tests.test_execution_context_preflight \
    modsecurity_connector_tests.test_hostruntime_preflight.HostruntimePreflightTests.test_missing_binary_is_blocked \
    modsecurity_connector_tests.test_hostruntime_preflight.HostruntimePreflightTests.test_incomplete_identity_evidence_cannot_pass \
    modsecurity_connector_tests.test_hostruntime_preflight.HostruntimePreflightTests.test_valid_lock_drives_version_and_safe_artifact_metadata
checked $FRAMEWORK_PYTHON -P -m unittest -v \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_harness_validates_authority_before_root_mutation_sinks \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_worker_path_authority_precedes_the_non_root_handoff \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_worker_preflight_uses_the_rendered_nginx_group \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_worker_helpers_use_only_fixed_runuser_capabilities \
    modsecurity_connector_tests.test_nginx_sequence_driver_phases.SequenceDriverPhasesTests.test_success_receipts_are_raw_bound_without_canonical_promotion \
    modsecurity_connector_tests.test_nginx_sequence_driver_phases.SequenceDriverPhasesTests.test_config_rejection_never_starts_client_and_still_attempts_cleanup \
    modsecurity_connector_tests.test_nginx_sequence_driver_phases.SequenceDriverPhasesTests.test_blocked_context_precedes_projection_configtest_and_child
checked $FRAMEWORK_PYTHON -P -m unittest -v \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_exact_repository_chain_is_accepted \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_uncommitted_lock_rewrite_is_rejected_even_when_semantically_identical \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_lock_cannot_override_parent_framework_gitlink \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_framework_and_mrts_materialized_head_mismatches_are_rejected \
    modsecurity_connector_tests.test_update_framework_versions.SyncFrameworkVersionsTests.test_framework_sha_projection_updates_only_revision_lock \
    modsecurity_connector_tests.test_update_framework_versions.SyncFrameworkVersionsTests.test_framework_sha_projection_rejects_malformed_lock_without_writes \
    modsecurity_connector_tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_current_parent_contract_matches_the_candidate_without_writing \
    modsecurity_connector_tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_candidate_mrts_gitlink_must_match_locked_selection \
    modsecurity_connector_tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_each_unprotected_handoff_layer_rejects_a_representative_drift
checked $FRAMEWORK_PYTHON -P ci/tools/sync-framework-component-versions.py --check --framework-common $TASK_ROOT/private/framework-common-merged.sh --framework-sha 5ef57603a4933f18c988f1f9f32b93f478182440
checked $FRAMEWORK_PYTHON -P ci/tools/verify-framework-candidate-contract.py --repo-root $PARENT_ROOT --candidate-sha 5ef57603a4933f18c988f1f9f32b93f478182440 --framework-common $TASK_ROOT/private/framework-common-merged.sh --candidate-framework-root $FRAMEWORK_ROOT --expected-parent-framework-sha 5ef57603a4933f18c988f1f9f32b93f478182440
checked make -C $PARENT_ROOT check-apache-common-adoption PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/build TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/logs
checked make -C $PARENT_ROOT check-common-helpers-c17 PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/common-build TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/common-logs
checked make -C $PARENT_ROOT check-common-helpers-c17 ON_DEMAND_TESTS=1 PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/common-api-build TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/common-api-logs
```

## Security-Auswirkung

Das Routing verlangt ein frisches Preflight im tatsächlichen Host-Launcher/Namespace vor identitätsabhängiger Arbeit. UID-/GID-Wechsel, private UDS-/Pfadprüfungen, Root-Master- und Nicht-Root-Worker-Anforderungen, Zulassung geschützter Broker und Cleanup-Prüfungen bleiben erhalten. Preflight PASS belegt nur Voraussetzungen. Autorisierung, Guards, Testerwartungen, CI-Bedingungen und Quality Gates werden nicht abgeschwächt.

## Runtime-Evidence

Die frische Preflight-Suite enthielt eine separate Daemon-Launcher-Probe. Sie prüft den Launcher-Ausführungskontext, nicht das endgültige eingecheckte Produktpaar. Ein frischer NGINX-Hostnachweis am endgültigen Commitpaar wird nicht behauptet. Erforderlich sind Master UID/GID 0, Worker 65534, Readiness, HTTP `200→403→200`, Regel-/Transaktionskorrelation und verifiziertes Prozess-/Listener-Cleanup. Auch die separate Nicht-Root-Launcher-Probe muss frisch sein. Für Envoy liegt in dieser Änderung kein Host-Ausführungsnachweis vor.

## Bekannte Einschränkungen

Der aktuellen Basis fehlen die Common-APIs für Protokoll/Spätinterventionskontext sowie Apache `apache_response_protocol`, die das ausgewählte Framework voraussetzt. PR #348 ist ein separater, nicht integrierter Draft und eine Integrationsabhängigkeit. Nach dessen separater Integration muss aktueller `master` in diesen Branch übernommen und die Qualifikation am endgültigen eingecheckten Paar wiederholt werden. Die Draft-Veröffentlichung belegt keine Kompatibilität.

## Verbleibende Risiken

Bereits wiederverwendete NGINX-Artefakte benötigen passende Produktquell-, Build- und Artefaktnachweise gegen die endgültige Produktrevision; alte Runtime-Evidence ersetzt diese nicht. Fünf unabhängige vorbestehende Inheritance-Abweichungen bleiben unverändert: `PARENT-CHANGE-WORKFLOW`, `PARENT-CONNECTOR-MATRIX`, `PARENT-DEFINITION-OF-DONE`, `PARENT-PHASE4-TARGET-SEMANTICS` und `PARENT-TESTING-AND-EVIDENCE`. Die beiden erneuerten Katalogeinträge sind keine Framework-Kind-Inheritance-Pins. Eine separate vorbestehende Framework-Kind-Inheritance-Abweichung bei `PARENT-COMMAND-EXECUTION` bleibt ebenfalls erhalten; sie ist von den fünf veralteten Parent-Katalogeinträgen getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Der erfolgreiche Apache-Vertrag, die vollständige Qualifikation des eingecheckten Paars, NGINX-Artefaktzulassung, frische NGINX-Sequenz, separate Launcher-Probe, verifiziertes Cleanup und finale CI-/Sonar-Qualifikation am PR-Head stehen aus. Fehlende Produkt-APIs blockieren die Freigabereife. Ein Envoy-Hostlauf wurde nicht ausgeführt. Bei einem späteren Merge müssen null neue Sonar-Issues einschließlich akzeptierter Issues und null neue Hotspots erhalten bleiben; dieser Draft behauptet dieses finale Ergebnis nicht.

## Finaler Diff- und Review-Status

Der isolierte Worktree erhält die lokalen Änderungen des ursprünglichen Checkouts. Ausgewählt werden nur die auftragsbezogenen Kontext-, Pin-/Projektions- und gepaarten Berichtsänderungen. Solange #348 fehlt, soll der PR Draft bleiben; eine Connector-Liefer-SHA, erfolgreiche aktuelle CI-/Sonar-Ergebnisse oder ein Merge-Ergebnis werden hier nicht behauptet.
