# Change Record: CR-20261001-pr370-refresh-relevance

**Sprache:** [English](CR-20261001-pr370-refresh-relevance.md) | Deutsch

PR-Wartung, keine Readiness-Promotion für zehn Profile.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261001-pr370-refresh-relevance |
| Datum (UTC) | 2026-10-01 |
| Basis-Revision | `e0b6cab3f46d73da0a10d7b4afca73e0cb584448` |

## Motivation und Problemstellung

Der Benutzer verlangte Aktualisierung und Relevanzprüfung des bestehenden Draft-PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370). Sein veröffentlichter Head hatte Konflikte mit Master; die Beschreibung war veraltet. Zwei unabhängige Source-Audits fanden Apache-P2/APXS-, Envoy-ext_authz-Pfad-, Stock-lighttpd-Endpunkt-, Traefik-Native-Endpunkt- und NGINX-Receipt-Korrekturen weiterhin nicht auf Master.

## Akzeptanzkriterien

Veröffentlichte Historie erhalten; beobachteten Master `b0f3bdab429717b5b0311c30c5b4d1153c672ac0` normal integrieren; aktuelle Pins und Security-/Phase-4-Verhalten erhalten; Konflikte lösen; relevante Prüfungen wiederholen; Exact-Head-CI/Sonar und zweisprachigen Delivery-Status veröffentlichen. Kein Merge ist autorisiert.

## Implementierungsentscheidung und Begründung

Der frühere Worktree fehlt; daher neuen task-eigenen Worktree vom veröffentlichten Head verwenden. Beide NGINX-Konflikte mit `EXPECTED_NGINX_VERSION = "1.31.6"` lösen, gemeinsam für Source-Root und beide Receipts; HAProxy `3.2.25` erhalten. Nur zwei ungenutzte `read_event_jsonl`-Ergebniszuweisungen (`c:S1854`) entfernen. Die Stock-Assertion an das modusabhängige Phase-4-Budget anpassen. Notwendige Apache-Bootstrap-P2-Marker-/Default-Limit-, Audit-Redaction-, Recovery- und Non-Root-Kontrollen wiederherstellen; finalen curl-Status statt erster Headerzeile (`100 Continue`) erhalten. Alle anderen veröffentlichten Korrekturen und eingehenden Master-Security-/Phase-4-Änderungen bleiben erhalten.

## Geänderte Dateien

- `tests/run_nginx_body_buffer_fixture.py`, `tests/test_nginx_body_buffer_fixture.py`
- `tests/transaction_phase_runtime_companion_test.c`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`, `tests/test_apache_request_transaction_cleanup.py`
- Dieser EN/DE-Record, EN/DE-Archivindex und Querverweise im früheren EN/DE-Readiness-Record. Andere eingehende Master-Dateien sind Integrationshistorie, keine separat ausgewählten Edits.

## Scope-Abgleich vom 2026-10-03

Die NGINX-Aussagen oben beschreiben den Zwischenstand vom 1. Oktober. Der
Benutzer schloss NGINX anschließend aus. Alle vier NGINX-Fixture-/Contract-
Test-Pfade entsprechen nun `origin/master`; der finale PR liefert oder
verwertet diese Receipt-Identitätskorrektur nicht. Die verbleibende Arbeit an
neun Profilen ist von diesen Dateien unabhängig.

## Ausgeführte Befehle

Alle Shell-Befehle liefen RTK-wrapped. Vorhandenes `python3` ist exakt `3.14.7`; keine Dependency-Installation. Task-Ausgabe: `/var/tmp/codex/ModSecurity-conector/runs/pr370-refresh-20261001`.

| Prüfung | Beobachtetes Ergebnis vor Delivery |
| --- | --- |
| Fokussierte Python-Suite einschließlich aktueller Security-Regressionen | 224 Fälle: 217 bestanden, sechs übersprungen, ein Umgebungsfehler bei `mkdtemp` der fest auf `/tmp` gelegten Fixture, vor Produktausführung. |
| Stock/Pins/Body-Buffer/Phase-4/forwardAuth-Suite | 143 Fälle: 137 bestanden, sechs Prerequisite-Skips. |
| Apache-Bootstrap-Source-Regression und Shell-Syntax | 21/21 bestanden; `sh -n` bestanden. |
| `make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-apache-common-adoption` | Bestanden; Apache-Adoption führte zusätzlich 12 fokussierte Fälle aus. |
| `make check-apache-c17 check-remaining-connectors-c17` | Mit Warnings-as-Errors und expliziter externer Ausgabe bestanden. Der erste Apache-Default-Output-Versuch scheiterte auf einem nicht freigegebenen Read-Only-Pfad; der Wiederholungslauf verwendete task-eigene Ausgabe. |
| Direkter Companion-C-Test mit `cc` und `clang` | Beide strikten C17-Builds und Ausführungen gegen System-libmodsecurity bestanden, jeweils auf 120 Sekunden begrenzt. |
| `make -C connectors/traefik test-native-middleware` | Go-Tests und vet bestanden. |
| `python3 ci/tools/generate-connector-config-reference.py --check` | Bestanden: 21 generierte Dateien aktuell. |
| `git diff --check` | Vor Record-Erstellung bestanden. |
| `make check-apache-autotools-bootstrap` | Modulbuild/-konfiguration bestanden; Non-Root-Start durch `chown` der Task-Verzeichnisse mit `EINVAL` blockiert. Kein bestandener Host-Runtime-Lauf. |
| `make check-bilingual-docs` und `make check-doc-links` | Versucht; nur fehlende lokale Framework-Linkziele gemeldet. Der Strukturcheck für neuen Record/Archiv bestand. |

## Security-Auswirkung

Keine Suppression, Exclusion, Quality-Gate-Lockerung, Dependency-Änderung oder Compiler-Warning-Reduktion. Trusted-Socket-/Pfad- und Body-Limit-Kontrollen bleiben geschützt. Unabhängiges Merged-Source-Review bestätigte Apache-P4-Effective-Budgets und Stock-P4-OFF/LOG_ONLY/shutdown neben erhaltenen PR-Korrekturen. Keine Framework-/MRTS-Source-Writes; ihre Gitlinks folgen nur eingehender Master-Historie.

## Runtime-Evidence

Das direkte Common-Companion-Binary validiert Escaped-Event-Hashing und buffered-forwardAuth-P2-zu-P3/P4-Transfer gegen libmodsecurity. Es umgeht Host-HTTP-Parsing, verwendet `safe` und ist kein Host-/Readiness-B-Ergebnis. Es ist nicht in Routine-CI eingebunden. Final-Head-Apache-, NGINX- und Runtime-Cell-Ergebnisse werden nach Push in PR #370 erfasst, nicht aus historischen September-Läufen abgeleitet.

## Bekannte Einschränkungen

Der Worktree besitzt keinen materialisierten Framework-Checkout. Fünf Pin-Bound-Fälle und der Stock-Runtime-Identity-Prerequisite-Skip sind explizite lokale Lücken. Die neuere Verzeichnisregression kann ihre fest auf `/tmp` gelegte Fixture in dieser Sandbox nicht erstellen. Vollständige lokale Framework-abhängige Lint-/Docs-Prüfungen und G1–G9-Evidenz für alle zehn Profile sind nicht erbracht.

## Verbleibende Risiken

Hosted-Prüfungen und Sonar müssen an die ausgelieferte SHA gebunden sein. Alte grüne Runtime-Cells und alte 0,0-%-Duplikation validieren nicht den Nachfolger. Das umfassendere Readiness-B-Ziel bleibt unvollständig; der PR ist weiterhin ein begrenzter Korrekturschritt.

## Nicht ausgeführte Prüfungen mit Begründung

Keine G1–G9-Kampagne für alle zehn Profile, Dependency-Installation, Framework-/MRTS-Schreibarbeit, direkter Master-Push, Merge oder Force-Push. Exact-Head-CI ist erst nach Push verfügbar; die Live-Ergebnisse werden bei Übergabe in PR #370 veröffentlicht. Vollständiger lokaler Framework-abhängiger Lint wurde nicht ausgeführt; lokale native Apache-Start- und repositoryweite Docs-Versuche haben die oben aufgeführten Umgebungsgrenzen und werden niemals als bestanden gewertet.

## Finaler Diff- und Review-Status

Relevanz wurde unabhängig gegen aktuellen Master auditiert; der zusammengeführte Apache-/Stock-Overlap wurde unabhängig geprüft. Main verantwortet finalen Diff, zweisprachiges Review, Delivery und CI-/Sonar-Abgleich. Beobachtete Delivery-Ergebnisse werden in PR #370 statt einer selbstreferenziellen Commit-SHA in diesem Record gepflegt.
