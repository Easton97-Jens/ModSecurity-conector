# Change Record: Parent-Test-Assertion-Order-Remediation für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-s3415-parent-test-assertions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-s3415-parent-test-assertions |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`-Code-Smells: 112 aktuelle OPEN-Receipt-Keys in neun reinen Testmodulen. |
| Grenze | Parent-Testquellen und dieses englisch/deutsche Change-Record-Paar. Produktquellen, Workflows, Framework, MRTS, Gitlinks, SonarQube-Cloud-Konfiguration, Quality Gates, Suppressions, externer Issue-Status, Push, Pull Request und Merge bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Inventur enthält 112 offene `python:S3415`-
Befunde in neun reinen Parent-Testmodulen. Die betroffenen `assertEqual`-
Aufrufe zeigen den erwarteten Wert vor dem beobachteten Wert, wodurch
Fehlerausgaben weniger nützlich werden und die Assertion-Order-Konvention des
Repositories verletzt wird.

## Akzeptanzkriterien

- Alle 112 Receipt-basierten `python:S3415`-Aufrufe verwenden die Reihenfolge
  `actual, expected`.
- Es sind keine Änderungen an Produktquellen, Workflows, Framework-Quellen,
  MRTS-Quellen oder Gitlinks enthalten.
- Jedes geänderte fokussierte Testmodul besteht, die Receipt-basierte statische
  Reihenfolgeprüfung besteht und der Patch enthält keine Whitespace-Fehler.
- Ein gleichwertiges englisch/deutsches Change-Record-Paar pflegen; keinen
  Sonar-Issue vor einer exakten Kandidaten-Head-Analyse als geschlossen
  behaupten.

## Implementierungsentscheidung und Begründung

Jede Assertion wurde ausschließlich an Ort und Stelle umgeordnet. Assertion-
Typ, Operanden, Nachrichten, Fixtures, Testnamen und Kontrollfluss blieben
erhalten. Dadurch bleibt das getestete Verhalten unverändert, während der
beobachtete Laufzeitwert in einer Fehlerdiagnose zuerst erscheint.

## Geänderte Dateien

- connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py
- tests/test_collect_no_crs_source.py
- tests/test_connector_capabilities.py
- tests/test_nginx_phase4_runner_wiring.py
- tests/test_prepare_runtime_components.py
- tests/test_response_header_backend.py
- tests/test_runtime_path_policy.py
- tests/test_traefik_transport_hardening_contract.py
- tests/test_transport_lifecycle_artifacts.py
- reports/audits/change-records/CR-20260727-sonar-s3415-parent-test-assertions.md
- reports/audits/change-records/CR-20260727-sonar-s3415-parent-test-assertions.de.md

## Ausgeführte Befehle

Der Task-Worktree initialisierte den vom Parent festgeschriebenen Framework-
Gitlink auf `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`, ohne Framework-Quellen
oder den Parent-Gitlink zu ändern. Für jedes Modul wurde derselbe
Befehlspräfix verwendet:

```sh
rtk proxy env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/sonar-s3415-test-assertions-20260727/tmp /root/git/ModSecurity-conector/.venv/bin/python3 -B -m unittest -v
```

- `connectors.haproxy.harness.test_haproxy_htx_smoke_helper`
- `tests.test_collect_no_crs_source`
- `tests.test_connector_capabilities`
- `tests.test_nginx_phase4_runner_wiring`
- `tests.test_prepare_runtime_components`
- `tests.test_response_header_backend`
- `tests.test_runtime_path_policy`
- `tests.test_traefik_transport_hardening_contract`
- `tests.test_transport_lifecycle_artifacts`
- `rtk proxy git diff --check`
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs`

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussierte Testmodule | bestanden: neun Befehle endeten mit 0; 8 + 34 + 13 + 6 + 28 + 5 + 6 + 7 + 5 = 112 Tests. |
| Receipt-basierte Assertion-Prüfung | bestanden: `receipt_open_python_S3415=112`, `static_ordering_failures=0`. |
| `git diff --check` | bestanden: kein Whitespace-Fehler. |
| Direkter Source-Diff-Review | bestanden: nur 112 In-Place-Assertion-Argument-Swaps in den neun abgegrenzten Testmodulen. |
| `make check-bilingual-docs` vor der Record-Layout-Korrektur | fehlgeschlagen: Der erste Draft dieses Records entsprach nicht dem Repository-Change-Record-Schema; der Fehlschlag wird aufbewahrt und der Record in diesem Kandidaten korrigiert. |
| `make check-bilingual-docs` nach der Korrektur | bestanden: `bilingual docs ok`. |
| `make check-doc-links` | bestanden: `repository path references: PASS` und `doc links ok`. |

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet `not_applicable`: keine
Änderungen an Produkt-Sicherheitsgrenzen. Die betroffenen Tests decken
weiterhin ihre vorhandenen Sicherheits- und Lifecycle-Kontrollen ab; geändert
wurde nur die Argumentreihenfolge der Assertion-Diagnostik.

## Dokumentationsstatus

Dieses englisch/deutsche Change-Record-Paar dokumentiert den test-only
Refactor. Beide Dateien enthalten denselben Source-Scope, dieselben
Testergebnisse, Validierungsgrenzen und Delivery-Status.
`make check-bilingual-docs` und `make check-doc-links` bestehen nach der
Vorbereitung des korrigierten Paars und seiner Indizes.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll-, Report-Generation- oder
Produktions-Runtime-Verhalten geändert oder behauptet. Die fokussierten
Unit-Tests sind keine Runtime-Evidence.

## Bekannte Einschränkungen

SonarQube Cloud hat diesen uncommitteten Kandidaten noch nicht analysiert; die
112 aktuellen Befunde können erst nach einer exact-head Analyse verschwinden.

## Verbleibende Risiken

Ein versehentlich vertauschter Operand kann einen Test schwächen. Jedes
geänderte Modul wurde erneut ausgeführt und die Receipt-basierte statische
Reihenfolgeprüfung als fokussierte Evidenz aufbewahrt. Aus dieser test-only
Bereinigung folgt keine Aussage über nicht verwandte Sonar-Zeilen oder
Sicherheitsbefunde.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Builds, Host-Konfigurationsprüfungen, Runtime-Smokes,
  Protokollmatrizen, Framework-Checks und MRTS-Checks sind nicht anwendbar,
  weil keine Connector-/Runtime-Implementierung oder Cross-Repository-Inhalte
  geändert wurden.
- Es wurde keine gehostete SonarQube-Cloud-Analyse, GitHub-CI, Commit, Push,
  Pull Request oder Merge durchgeführt. Diese Aufgabe hat keine
  Master-Integrationsautorisierung.

## Finaler Diff- und Review-Status

Der lokale Kandidat im Task-Worktree ist uncommitted und enthält die
Assertion-Order-Bereinigung sowie erforderliches Traceability-Material. Im
autoritativen Parent-Checkout wird keine Source geändert. Es gab keine
Framework- oder MRTS-Source-Aktion, kein Gitlink-Update, keine
Scanner-Control-Änderung, keine externe Issue-Disposition, keinen Push, Pull
Request oder Master-Merge. Spätere Dokumentationsvalidierung und
Delivery-Evidence werden ausschließlich aus beobachteten Ergebnissen
aufgenommen.
