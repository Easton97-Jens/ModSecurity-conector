# Change Record: Apache-Phase-4-Response-Enforcement

**Sprache:** [English](CR-20260718-apache-phase4-response.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-apache-phase4-response` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `aabde81a9a315bf3e494e595ab0399357c596f9c` |
| Scope | Nur Parent-Repository; Framework- und MRTS-Source bleiben unverändert. |
| Zugehörige Findings | `FND-PARENT-0038`, `FND-PARENT-0041`, `FND-PARENT-0042` und `FND-PARENT-0043`. |

## Motivation und Problemstellung

Apache darf kein Response-Byte freigeben, das Phase 4 berücksichtigen kann,
bevor `msc_process_response_body` und eine mögliche Intervention entschieden
haben. Vor dieser Reparatur konnte eine fragmentierte Pre-EOS-Response die
Commit-Grenze überschreiten, bevor eine späte Entscheidung vorlag. Die native
Request-Wiederverwendung bei einem normalen Internal Redirect ist ebenfalls
unsicher: Die Transaction kann nicht zuverlässig an Ziel-URI, Regeln und
Request-Variablen neu gebunden werden. Zusätzlich begrenzt ein Byte-Limit
nicht die Anzahl der bis EOS zurückgehaltenen APR-Bucket-Objekte.

Generated-Report-Metadaten hatten einen separaten Evidenzintegritätsfehler:
`git -C` aus einem nicht ausgecheckten Framework-Gitlink-Verzeichnis konnte das
darüberliegende Parent-Repository entdecken und Parent-State fälschlich als
Framework-Provenance ausgeben.

## Akzeptanzkriterien

- Eine disruptive Phase-4-Entscheidung verhindert die erste Freigabe
  ursprünglicher Response-Bytes und spätes terminales Output wird versiegelt.
- Unsichere normale Redirects schlagen fail-closed fehl, bevor ein
  Ziel-Quick-Handler oder normaler Ziel-Handler läuft; der begrenzte
  Apache-Core-ErrorDocument-Fall bleibt verfügbar.
- Der Connector hält über Filter-Aufrufe hinweg höchstens 4.096 normalisierte
  Response-Buckets und lehnt das nächste Objekt vor Append/Setaside ab.
- Die Grenze aus 4.095 Daten-Buckets plus EOS wird normal freigegeben, während
  die fragmentierte Folge aus 4.097 Buckets fail-closed scheitert.
- Framework-Provenance hält realen Checkout getrennt vom Parent-Gitlink fest
  und behandelt fehlende oder abweichende Checkout-Evidenz als stale.
- Englische und deutsche Dokumentation, generierte Referenzen und Change
  Records bestehen die Repository-Dokumentationsprüfungen ohne Abschwächung.

## Implementierungsentscheidung und Begründung

`MODSECURITY_OUT` hält normalisierte Pre-EOS-Brigades zurück, trifft die
Phase-4-Entscheidung bei EOS und gibt nur genau einmal frei, wenn das Ergebnis
sicher ist. Der Protocol-Guard versiegelt späteres Producer-Output nach Deny,
EOS oder terminalem Fehler. Ein früher Quick-Handler-Guard plus ein früher
Fallback für normale Handler verweigern unsichere `r->prev`-Redirects; der
einzige erlaubte Redirect ist ein begrenzter lokaler ErrorDocument-Übergang mit
Core-geformtem Provenance-Proof.

Die Reparatur zählt jeden normalisierten bis EOS zurückgehaltenen Bucket in
`response_brigade_bucket_count`. `MSCONNECTOR_PHASE4_MAX_HELD_BUCKETS` ist
`4096U`; der Fehler tritt vor Append/Setaside ein und Release/Discard/Cleanup
setzen den Zähler zurück.

Der Generated-Report-Helper verlangt nun, dass der von Git gemeldete
Worktree-Root dem angeforderten Pfad entspricht. Er gibt tatsächlichen
Framework-Checkout-SHA, aufgezeichneten Gitlink-SHA, Checkout-Status und
Gitlink-Beziehung als getrennte Metadaten aus. Abhängige Generated Inputs
werden stale, wenn der Framework-Checkout fehlt oder vom aufgezeichneten
Gitlink abweicht.

## Geänderte Dateien

Der vollständige PR-#60-Diff enthält 57 Pfade. Seine ausführbaren und
Test-Pfade sind `ci/checks/connectors/apache/check-apache-common-adoption.py`,
`ci/checks/documentation/connector_config_reference.py`,
`ci/lib/generated_report_utils.py`,
`ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py`,
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`, die zehn
`ci/runtime/lifecycle/cases/apache-phase4-response/*.yaml`-Controls,
`connectors/apache/harness/apache_smoke.conf`,
`connectors/apache/harness/mod_phase4_terminal_rogue.c`,
`connectors/apache/harness/run_apache_smoke.sh`,
`connectors/apache/src/mod_security3.c`,
`connectors/apache/src/mod_security3.h`,
`connectors/apache/src/msc_config.c`,
`connectors/apache/src/msc_filters.c`,
`connectors/apache/src/msc_filters.h`,
`connectors/apache/src/msc_utils.c`,
`connectors/apache/src/msc_utils.h`,
`tests/test_apache_phase4_content_type_synchronized_upstream.py`,
`tests/test_apache_phase4_response_regression_wiring.py`,
`tests/test_connector_capabilities.py` und
`tests/test_nginx_phase4_runner_wiring.py`.

Die gepaarten Dokumentations- und generierten Pfade sind
`connectors/apache/README.md`, `connectors/apache/README.de.md`,
`connectors/apache/TODO.md`, `connectors/apache/TODO.de.md`,
`connectors/apache/capabilities.json`, `docs/architecture.md`,
`docs/architecture.de.md`, `docs/connectors/apache.md`,
`docs/connectors/apache.de.md`, `docs/operations-and-security.md`,
`docs/operations-and-security.de.md`, `docs/repository-concept.md`,
`docs/repository-concept.de.md`, `examples/apache/README.md`,
`examples/apache/README.de.md`, `examples/apache/configuration-reference.md`,
`examples/apache/configuration-reference.de.md`,
`examples/apache/rules/p1-p4-safe.conf`, `examples/apache/safe/httpd.conf`,
`reports/connector-configuration-inventory.json`,
`reports/testing/generated/canonical/connector-capabilities.generated.json`,
seine englischen und deutschen Markdown-Begleitfassungen, dieses
Change-Record-Paar und das Change-Record-README-Paar.

## Ausgeführte Befehle

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_phase4_response_regression_wiring tests.test_bilingual_docs tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_metadata_uses_gitlink_when_framework_is_not_checked_out tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_framework_provenance_marks_a_matching_gitlink_checkout tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_framework_provenance_marks_a_checkout_that_differs_from_its_gitlink tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_input_record_marks_a_missing_framework_checkout_stale tests.test_connector_capabilities.ConnectorCapabilitiesTest.test_input_record_marks_a_framework_gitlink_mismatch_stale` bestand: 26 Tests.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-connector-config-reference` bestand: 21 generierte Dateien aktuell.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/evidence/collectors/connector_capabilities.py check` bestand: 6 Connectors und 60 Capabilities.
- `rtk proxy bash -n connectors/apache/harness/run_apache_smoke.sh ci/runtime/lifecycle/run-apache-phase4-response-regression.sh` bestand.
- `rtk proxy shellcheck ci/runtime/lifecycle/run-apache-phase4-response-regression.sh` bestand. Der vollständige Harness meldet weiterhin nur sieben bereits vorhandene Baseline-Diagnosen; die fokussierte Bereinigung der Audit-Log-Assertions fügt keine hinzu.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_apache_phase4_response_regression_wiring` bestand nach der fokussierten Shell-Bereinigung: 10 Tests.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` reproduzierte vor dieser Korrektur den Change-Record-Schema-Fehler; der lokale Rerun bleibt nur durch bereits vorhandene Links in den nicht ausgecheckten Framework-Gitlink blockiert und der CI-Rerun mit populiertem Framework ist erforderlich.
- `rtk proxy git diff --check` bestand vor der Dokumentations-Remediation und wird für den korrigierten Kandidaten erneut ausgeführt.

## Security-Auswirkung

Die geänderte Grenze liegt vor der ersten Freigabe ursprünglicher
Response-Bytes. Sie verhindert, dass eine disruptive `RESPONSE_BODY`-Policy
nur wegen mehrerer Brigades zu log-only degradiert wird. Unsichere
Redirect-Wiederverwendung schlägt fail-closed fehl, statt mit einer veralteten
nativen Transaction fortzufahren. Der Bucket-Cap schließt eine validierte
CWE-400-Verfügbarkeitsbedingung unterhalb des Byte-Limits. Das Provenance-Gate
verhindert, dass Parent-Git-State als Framework-Evidenz ausgegeben wird.

## Runtime-Evidence

Die aufbewahrte native Apache-Validierung reproduziert Pre-Fix-HTTP 200 für
4.097 Ein-Byte-Buckets unterhalb des Ein-MiB-Byte-Caps. Das reparierte Modul
lehnt eine aufgeteilte 4.097-Bucket-Folge mit HTTP 500 vor der Freigabe ab,
gibt 4.095 Daten-Buckets plus EOS mit HTTP 200 und exakt 4.095 Bytes frei und
bestand die serielle sichere 32-Mode-Matrix. Der versiegelte 30-Mode-Receipt
ist `runs/20260719T162259Z-pr60-exact-head-revalidation-dfba422e/evidence/pr60-exact-native-phase4-manifest.json`
mit SHA-256
`1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548`.
Der aufbewahrte 32-Mode-Report ist
`runs/20260719T183551Z-pr60-final-security-diff-93404fdd/evidence/security-diff/artifacts/05_findings/CAND-PR60-001/validation_report.md`
mit SHA-256
`79e7e1b3fcca6acdf8d02ed941eaadcea566258656abe269a54289a59e88db8c`.

## Bekannte Einschränkungen

Phase-4-Responses im Scope werden absichtlich bis EOS gehalten; progressives
Streaming ist an dieser Enforcement-Grenze nicht verfügbar. Der begrenzte
lokale ErrorDocument-Übergang beruht auf Apache-Core `no_local_copy` plus
`REDIRECT_STATUS`, nicht auf einem unforgeable Token. Der Phase-3-Snapshot
behauptet nicht, HTTP/2-Trailer einzufrieren.

## Verbleibende Risiken

`FND-PARENT-0042` ist lokal behoben, benötigt aber weiterhin Exact-Pushed-Head-
und Resulting-Master-Verifikation. `FND-PARENT-0043` bleibt P2/low: gemeinsamer
Helper und aktuelle Capability-Artefakte sind korrigiert, während vier
report-spezifische direkte Git-Senken und ein kritischer Layout-Relation-Check
als Follow-up erfasst bleiben. Lokal wurde kein High- oder Critical-Finding
identifiziert.

## Nicht ausgeführte Prüfungen mit Begründung

Das vollständige `tests.test_connector_capabilities`-Modul hat einen erwarteten
umgebungsblockierten Fall, weil diesem dedizierten Worktree
`modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`
fehlt. Die fokussierten Tests der geänderten Pfade bestehen. Die vollständige
CRS/MRTS-Matrix lief nicht erneut; die aufbewahrte fokussierte native
Apache-Validierung ist oben beschrieben. Dieser Record behauptet keinen
Direkt-Push, Force-Push, Bypass oder Master-Merge.

## Finaler Diff- und Review-Status

PR #60 zielt auf `master`. Vor dieser Change-Record-Schema-Korrektur hatte sein
Exact Head `418465645e2ceae60e842d1c3d7994d8bed93fa6` die sechs geschützten
Required Contexts, CodeQL und SonarCloud bestanden, während Change-Record-
Schema-Checks fehlschlugen. Diese Korrektur erzeugt einen neuen Kandidaten-Head
und startet den Exact-Head-CI-, Review-/Conversation- und Current-Base-
Verifikationszyklus erneut. Der PR ist bei Record-Autorenschaft nicht gemergt.
Eine nachfolgende fokussierte Shell-Lint-Bereinigung erhält die Audit-Log-
Assertions fail-closed und benötigt denselben Exact-Head-Verifikationszyklus.
