# Change Record: CR-20261008-nginx-native-operation-collection

**Sprache:** [English](CR-20261008-nginx-native-operation-collection.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-operation-collection |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `63d2f9a38c506e5122ace9ba36927add7f47e377` |

## Motivation und Problemstellung

Der generische Collector verwirft native Wrapper und kann referenzierte Event-Logs interpretieren oder scrubben. Native Records benötigen eine eigene geschlossene Route vor generischer Status-, Event- und Alias-Verarbeitung.

## Akzeptanzkriterien

Originale begrenzte native Wrapper-/Identitäts-/Revisions-/Actual-Exit-Felder unter expliziter Caller-Autorität erhalten; keine kanonischen Events oder PASS erzeugen. Fehlende/fremde Autorität, unsichere Pfade, unbekannte Felder, doppelte Identitäten und ungültige Exit-Werte scheitern geschlossen. Bestehende Config- und Harness-Sammlung erhalten.

## Implementierungsentscheidung und Begründung

`--allowed-native-operation-root` hat den Default None und wird niemals aus einer Row abgeleitet. `case_row_observations` und `case_observations` akzeptieren den optionalen Parameter `allowed_native_operation_root`. `nginx_native_collection.collect_native_row` prüft die bestehende geschlossene 42-Case-Dispatch-Zuordnung und Referenzsicherheit; Framework bleibt für Canonical-/Runtime-Proof zuständig. Actual-Exit 0 erhält NOT_EXECUTED; ein von null verschiedener tatsächlicher Exit bleibt erhalten und wird FAIL. Beide Routen liefern keine nativen Events oder Aliase.

## Geänderte Dateien

`ci/runtime/lifecycle/collect-no-crs-source.py`, neu `ci/runtime/lifecycle/nginx_native_collection.py`, neu `tests/test_nginx_native_operation_collection.py` und dieser EN/DE-Nachweis. Bestehende Config-Receipt-Konstanten/-Helper und Host-/Baseline-Wrapper werden nicht geändert; Roots separate Config3-Änderungen müssen bei der Integration erhalten bleiben.

## Ausgeführte Befehle

`rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_native_operation_collection` endete zunächst mit 1 (fehlende CLI/API und fehlende Autoritätsablehnung), danach bestanden alle 13 gezielten Tests. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PARENT_TEST_FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_nginx_native_operation_collection tests.test_collect_no_crs_source tests.test_collect_no_crs_source_helpers tests.test_nginx_configtest_collection tests.test_nginx_native_operation_dispatch -v` bestand mit 91 Tests, Exit 0, und drei Gitlink-Trust-Skips. Die breitere Selected-Runner-Wiring-Suite hatte zwei bestehende Fehler durch fehlende Apache-Submodule-Fixtures; sie wird nicht als grün behauptet. Drei geänderte Python-Dateien wurden mit `ast.parse` geparst; `rtk git diff --check` bestand. Parent-Archive- und Paarprüfungen validieren Dokumentstruktur, keinen Runtime-Proof.

## Security-Auswirkung

Autoritäts- und Bundle-Pfade müssen absolute externe Kinder von `/var/tmp/codex/ModSecurity-conector`, im eigenen Besitz und für andere nicht schreibbar sein, ohne Checkout oder gefolgten Symlink. Original-Receipts müssen begrenzte, owner-only, reguläre Single-Link-Dateien sein und den Wrapper-Hashes entsprechen. E-Parent-/Child-Pfade und Seals sind geschlossen. Native Raw-Logs/Captures bleiben unverändert; native Pfade werden vor Scrubbing aus generischen Source-Event- und Consumed-Event-Listen abgelehnt.

## Runtime-Evidence

Nur kontrollierte Collection-/Fixture-Tests liefen. Kein NGINX-Build, Live-Native-Request, kanonisches Required-Case-PASS oder Exact-Head-Proof wird behauptet.

## Bekannte Einschränkungen

Diese Schicht validiert sichere Collection-Referenzen, keine tatsächlichen Engine-Callbacks, finale Artefaktautorität oder kanonische Case-Semantik. Drei Framework-Prüfungen wurden übersprungen, weil der bereitgestellte Framework-HEAD vom Parent-Gitlink abweicht.

## Verbleibende Risiken

Root muss die explizite Autorität durch Host-/Baseline-Orchestrierung verdrahten und strikten Framework-Proof/Retention integrieren. Die erforderliche Source-Hash-Closure muss gegebenenfalls den neuen Collection-Helper berücksichtigen. Fehlende Autorität oder ein von null verschiedener Exit darf nicht promotet werden.

## Nicht ausgeführte Prüfungen mit Begründung

Native Build/Runtime, vollständiges E2E, Wrapper-/Baseline-Wiring und Canonical-Proof-Validierung wurden nicht ausgeführt oder geändert, da sie außerhalb dieses begrenzten Collection-Umfangs liegen. Keine Pakete wurden installiert; Ruff war nicht verfügbar und wurde nicht installiert.

## Finaler Diff- und Review-Status

Nur Collector-Seam, eigene Helper/Tests und gepaarter Nachweis wurden geprüft. Raw-Evidence bleibt original; Config-/Harness-Verhalten bleibt getrennt. Frische fokussierte und Collector-Regressionsresultate stützen diesen Umfang; Runtime- und isolierte Submodule-Lücken bleiben explizit.
