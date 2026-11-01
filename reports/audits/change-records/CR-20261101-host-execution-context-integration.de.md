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

Die `.codex`-Kontext- und Routingänderungen sind unabhängig von #348 und anderen PRs. Die #348-Abhängigkeit betrifft ausschließlich die Produkt-/Testverträglichkeit des ausgewählten Framework-Pins und die finale Paarqualifikation; sie ist keine Voraussetzung für die Kontextanleitung selbst.

## Akzeptanzkriterien

Die Draft-Lieferung erfordert einen auftragsbezogenen Diff, einen konsistenten Framework-Gitlink samt registrierten Projektionen, aktuelle Pin-/Provenienz- und Dokumentationsprüfungen, Secret-Scanning und die ausdrückliche Benennung der Abhängigkeit. Freigabereife erfordert zusätzlich den Apache-Vertrag, das eingecheckte Parent-/Framework-Paar, Artefaktzulassung, frischen NGINX-Hostlauf mit Launcher-/Cleanup-Nachweisen sowie aktuelle CI-/Sonar-Ergebnisse am exakten Head. Dieser Auftrag autorisiert keinen Merge.

## Implementierungsentscheidung und Begründung

Der ausgewählte Framework-Pin ist `b85280278310f4034af78149ac13671438965c7b`, der direkt integrierte Nachfolger des angeforderten `5ef57603a4933f18c988f1f9f32b93f478182440` aus [Framework-PR #150](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/150). Die Abweichung ist konkret erforderlich: Bei `5ef57603a4933f18c988f1f9f32b93f478182440` war das Spezialistenarchiv nach Framework-PR #147 nicht neu generiert worden. Es enthielt 7946 statt 7957 Definitionen und ließ die neuen Preflight-Tests sowie den blockierten Sequenzfall aus. Dies verursachte Connector-CI-Fehler in Common, Quick, NGINX und Scaffold; es war eine auftragsbezogene Auslassung, keine #348-Inkompatibilität.

Das Archiv von `b85280278310f4034af78149ac13671438965c7b` stimmt bytegenau mit dem zuständigen Generator überein und enthält 7957 Definitionen. Die zehn geprüften Hostimplementierungs-, Harness-, Test- und Anleitungspfade sind bytegleich zum angeforderten Commit. Im Quelleninventar ändert sich ausschließlich ein Compiler-Test-Bindungsdigest; Selektoren und Fälle bleiben gleich. Alle fünf Master-Workflows des ausgewählten Commits bestanden. Sonar bestätigte diesen exakten Commit mit Analyse `b8bd5d2c-57a5-4bca-8086-36237aa1bcba` vom `2026-11-01T20:24:20Z` und Quality Gate OK. Dies ist kein Erfolgsnachweis für den neuen Connector-Head.

Framework-PR #150 wurde unabhängig integriert; dieser Auftrag verändert oder integriert keinen Framework-Code. Generierte Parent-Projektionen werden ausschließlich durch `ci/tools/sync-framework-component-versions.py` aktualisiert. Der getrennte Framework-Code-Scanning-PR, Produktänderungen aus #348 und MRTS bleiben außerhalb dieses Diffs.

## Geänderte Dateien

- `.codex/context/index.md` leitet Entscheidungen zum nativen Hostkontext an `.codex/context/security-runtime-preflight.md`; diese Datei verlinkt die dauerhafte Framework-Anleitung.
- `.codex/inheritance-manifest.toml` erneuert nur die beiden auftragsbezogenen Katalog-Hashes.
- `modules/ModSecurity-test-Framework` wählt den integrierten Framework-Commit; `project-versions.lock.json` und 22 registrierte `.github/workflows/`-Dateien enthalten die generierten gewöhnlichen SHA-Projektionen. Die 23 Projektionsziele ändern ausschließlich die registrierte alte Revision zur ausgewählten Framework-Revision: 54 Workflow-Verweise und ein Lock-Verweis. Geschützte und historische Identitäten bleiben unverändert.
- Dieser Bericht und `CR-20261101-host-execution-context-integration.md` dokumentieren die Parent-Liefergrenze.

Die versionierte dauerhafte Anleitung liegt unter `modules/ModSecurity-test-Framework/docs/host-execution-context.md` mit ihrer `.de.md`-Begleitung. Connector-Produktquellcode und MRTS-Dateien gehören nicht zu diesem Diff.

## Ausgeführte Befehle

Frische Prüfungen des Pin-Kandidaten mit Framework `b85280278310f4034af78149ac13671438965c7b` und Parent-Ausgangshead `e03bc528c90c52974a5dc615da19070e33a72a86` bestanden ohne Skips: 13 Preflight-Tests (5.610 s), sieben Integrationstests (0.732 s) und neun Pin-/Provenienz-Vertragstests mit Fixtures (14.413 s). Der native Projektionscheck meldete `changed=[]`; der Kandidatenvertrag bestätigte die tatsächliche und erwartete Framework-Revision. `make check-active-inventory` und der separate Archivcheck bestanden mit exakt 7957 Definitionen. Dies prüft den Worktree-Kandidaten vor dem Folgecommit, nicht dessen noch unbekannten endgültigen Head.

Der frische Apache-Vertrag scheiterte mit Exit 2 an `apache_response_protocol`; auch die explizite Common-C17-Kompilierung mit `ON_DEMAND_TESTS=1` scheiterte mit Exit 2 an fehlenden Protokoll-/Spätinterventions-APIs, darunter `msconnector_late_intervention_context`, `protocol_kind_parse` und `STREAM_RESET`. Erwartungen wurden nicht angepasst. Der Traefik-Vertrag benötigt außerdem `Summary.ResponseIncomplete` aus der separaten Produktarbeit.

Alle lokalen Befehle verwenden RTK und den vorgeschriebenen Framework-Interpreter. Vor Quellzugriffen bestand das auftragsbezogene Secret-Scanning mit der vorhandenen Framework-Konfiguration ohne neue Ausnahmen oder Konfigurationsänderungen. Der finale Scan des geänderten b852-Kandidaten und die erneuten Dokumentationsprüfungen werden nach Abschluss der Berichtsänderungen durchgeführt; ihr tatsächliches Ergebnis und spätere PR-Head-Prüfungen gehören zur externen Evidence und PR-Beschreibung. Private Berichte und Rohlogs werden nicht eingecheckt.

Die folgende Übertragung fasst das identische beobachtete RTK-/Umgebungspräfix in `checked` zusammen. Pfadaliase bezeichnen den ausgewählten Parent-Worktree, seine Framework-Wurzel, den vorgeschriebenen Interpreter und die genehmigte externe Taskwurzel. `CONNECTOR_REVISION` ist der Ausgangshead vor dem Pin-Folgecommit. `framework-common-b852.sh` wurde aus dem ausgewählten Framework-Commit extrahiert.

```sh
checked() {
  rtk bypass env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=$TASK_ROOT/private TMPDIR=$TASK_ROOT/tests PYTHONPATH=$FRAMEWORK_ROOT:$FRAMEWORK_ROOT/connector_suite TEST_ROOT=$FRAMEWORK_ROOT FRAMEWORK_ROOT=$FRAMEWORK_ROOT FRAMEWORK_REVISION=b85280278310f4034af78149ac13671438965c7b CONNECTOR_ROOT=$PARENT_ROOT CONNECTOR_REVISION=e03bc528c90c52974a5dc615da19070e33a72a86 CONNECTOR_TEST_PROFILE=h1 CONNECTOR_TEST_OUTPUT_ROOT=$TASK_ROOT/tests EXECUTION_CONTEXT_TEST_ROOT=$TASK_ROOT/tests "$@"
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
checked $FRAMEWORK_PYTHON -P ci/tools/sync-framework-component-versions.py --check --framework-common $TASK_ROOT/private/framework-common-b852.sh --framework-sha b85280278310f4034af78149ac13671438965c7b
checked $FRAMEWORK_PYTHON -P ci/tools/verify-framework-candidate-contract.py --repo-root $PARENT_ROOT --candidate-sha b85280278310f4034af78149ac13671438965c7b --framework-common $TASK_ROOT/private/framework-common-b852.sh --candidate-framework-root $FRAMEWORK_ROOT --expected-parent-framework-sha b85280278310f4034af78149ac13671438965c7b
checked make -C $PARENT_ROOT check-active-inventory PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/b852-inventory TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/b852-inventory-logs
checked $FRAMEWORK_PYTHON -P $FRAMEWORK_ROOT/connector_suite/modsecurity_connector_ci/tools/update-test-archive.py --check
```

## Security-Auswirkung

Das Routing verlangt ein frisches Preflight im tatsächlichen Host-Launcher/Namespace vor identitätsabhängiger Arbeit. UID-/GID-Wechsel, private UDS-/Pfadprüfungen, Root-Master- und Nicht-Root-Worker-Anforderungen, Zulassung geschützter Broker und Cleanup-Prüfungen bleiben erhalten. Preflight PASS belegt nur Voraussetzungen. Autorisierung, Guards, Testerwartungen, CI-Bedingungen und Quality Gates werden nicht abgeschwächt.

## Runtime-Evidence

Die frische Preflight-Suite am ausgewählten b852-Kandidaten enthielt eine separate Daemon-Launcher-Probe. Sie prüft den Launcher-Ausführungskontext, nicht das endgültige eingecheckte Produktpaar. Ein frischer NGINX-Hostnachweis am endgültigen Commitpaar wird nicht behauptet. Erforderlich sind Master UID/GID 0, Worker 65534, Readiness, HTTP `200→403→200`, Regel-/Transaktionskorrelation und verifiziertes Prozess-/Listener-Cleanup. Auch die separate Nicht-Root-Launcher-Probe muss frisch sein. Für Envoy liegt in dieser Änderung kein Host-Ausführungsnachweis vor.

## Bekannte Einschränkungen

Der zusätzliche Migrationskartencheck scheitert für dieses Paar: 12 Envoy-Makefile-Aufruferpositionen und neun zugehörige Fallverweise unterscheiden sich von der Framework-Karte, die gegen den externen #348-Stand `b43faa78` erzeugt wurde. Das Parent-Makefile ist gegenüber Basis `2abad408` unverändert; Inventar, Archiv, Quellbindungen und Anzahlen stimmen überein. Dieser unabhängige Unterschied der Eingabepositionen bleibt fehlgeschlagen und wird weder durch Übernahme von Produktänderungen noch durch Umschreiben von Framework-Projektionen im Parent behoben.

Der aktuellen Basis fehlen außerdem `Summary.ResponseIncomplete` für den Traefik-Vertrag sowie die Common-APIs für Protokoll/Spätinterventionskontext sowie Apache `apache_response_protocol`, die das ausgewählte Framework voraussetzt. PR #348 ist ein separater, nicht integrierter Draft und eine Integrationsabhängigkeit. Nach dessen separater Integration muss aktueller `master` in diesen Branch übernommen und die Qualifikation am endgültigen eingecheckten Paar wiederholt werden. Die Draft-Veröffentlichung belegt keine Kompatibilität.

## Verbleibende Risiken

Bereits wiederverwendete NGINX-Artefakte benötigen passende Produktquell-, Build- und Artefaktnachweise gegen die endgültige Produktrevision; alte Runtime-Evidence ersetzt diese nicht. Fünf unabhängige vorbestehende Inheritance-Abweichungen bleiben unverändert: `PARENT-CHANGE-WORKFLOW`, `PARENT-CONNECTOR-MATRIX`, `PARENT-DEFINITION-OF-DONE`, `PARENT-PHASE4-TARGET-SEMANTICS` und `PARENT-TESTING-AND-EVIDENCE`. Die beiden erneuerten Katalogeinträge sind keine Framework-Kind-Inheritance-Pins. Eine separate vorbestehende Framework-Kind-Inheritance-Abweichung bei `PARENT-COMMAND-EXECUTION` bleibt ebenfalls erhalten; sie ist von den fünf veralteten Parent-Katalogeinträgen getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Der vollständige lokale Revisionsleser ist durch das nicht initialisierte MRTS-Checkout blockiert. MRTS wird in diesem Auftrag weder initialisiert noch verändert. Übereinstimmende statische eingecheckte Pins ersetzen diese vollständige materialisierte Revisionskette nicht.

Der erfolgreiche Apache-Vertrag, die vollständige Qualifikation des eingecheckten Paars, NGINX-Artefaktzulassung, frische NGINX-Sequenz, separate Launcher-Probe, verifiziertes Cleanup und finale CI-/Sonar-Qualifikation am PR-Head stehen aus. Fehlende Produkt-APIs blockieren die Freigabereife. Ein Envoy-Hostlauf wurde nicht ausgeführt. Bei einem späteren Merge müssen null neue Sonar-Issues einschließlich akzeptierter Issues und null neue Hotspots erhalten bleiben; dieser Draft behauptet dieses finale Ergebnis nicht.

## Finaler Diff- und Review-Status

[Connector-PR #436](https://github.com/Easton97-Jens/ModSecurity-conector/pull/436) ist bereits als getrennter Draft veröffentlicht. Die begründete Pin-Korrektur wird als normaler Folgecommit geliefert. Solange #348 fehlt, bleibt der Draft ohne Freigabereife. Der isolierte Worktree erhält die lokalen Änderungen des ursprünglichen Checkouts; ausgewählt werden nur Kontext-, Pin-/Projektions- und gepaarte Berichtsänderungen. Aktuelle erfolgreiche PR-Head-CI-/Sonar-Ergebnisse oder ein Merge-Ergebnis werden nicht behauptet. Ein Merge ist in diesem Auftrag nicht autorisiert.
