# Change Record: CR-20261009-nginx-exception-test-isolation

**Sprache:** [English](CR-20261009-nginx-exception-test-isolation.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-exception-test-isolation |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |

## Motivation und Problemstellung

Drei `python:S5778`-Findings betreffen Fixture-Erzeugung innerhalb von
Exception-Assertions. Ein Fixture-Fehler könnte die erwartete Exception erfüllen,
statt den Fehler der eigentlich geprüften Operation nachzuweisen.

## Akzeptanzkriterien

Jede gemeldete Assertion enthält nur ihren geprüften Aufruf. Exakte
Exception-Typen/-Meldungen, Descriptor-Close-Prüfungen und die Ablehnung der
Projection-Wiederverwendung bleiben erhalten. Beide betroffenen Testmodule
müssen ohne Suppressions weiterhin bestehen.

## Implementierungsentscheidung und Begründung

`PreparedInvocation` und Validator-`Mock` werden vor den Cleanup- und
fsync-Exception-Kontexten vorbereitet. Projection-Quellpfad, Worker-GID und
Avoid-Roots-Liste werden vor dem Wiederverwendungs-Exception-Kontext berechnet.
Fixture-Fehler scheitern damit außerhalb der erwarteten Exception-Grenze.
Produkt- und Framework-Code bleiben unverändert.

## Geänderte Dateien

- `tests/test_nginx_sequence_driver_phases.py`
- `tests/test_nginx_selected_native_projection.py`
- `reports/audits/change-records/CR-20261009-nginx-exception-test-isolation.md`
- `reports/audits/change-records/CR-20261009-nginx-exception-test-isolation.de.md`

## Ausgeführte Befehle

Die Befehle verwendeten `rtk proxy`, den expliziten vorhandenen
Parent-Virtual-Environment-Interpreter (`$PARENT_PYTHON`), `PYTHONNOUSERSITE=1`,
`PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1` sowie externe
`TMPDIR`, `RUNNER_TEMP`, `PYTHONPYCACHEPREFIX`.

- Begrenzte externe AST-Charakterisierung der drei gemeldeten Assertions:
  unveränderte Basis Exit 1 mit fünf Mehrdeutigkeitsdiagnosen; korrigiert Exit 0,
  drei Assertions mit jeweils einem geprüften Aufruf.
- `$PARENT_PYTHON -m unittest -v tests.test_nginx_sequence_driver_phases tests.test_nginx_selected_native_projection`:
  unveränderte Basis Exit 0, 25 Tests in 2.924s; korrigiert Exit 0, 25 Tests in
  3.686s; in beiden Läufen keine SKIPs.
- Natives `ci/tools/new-change-record.py create --name nginx-exception-test-isolation --base-revision 240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee --date 2026-10-09`:
  Exit 0; beide Vorlagen vor der sachlichen Bearbeitung erzeugt.
- `make check-bilingual-docs PYTHON=$PARENT_PYTHON FRAMEWORK_ROOT=$FRAMEWORK_ROOT`:
  Exit 2 wegen bereits fehlender verlinkter Framework-Pfade in diesem isolierten
  Worktree. `make check-doc-links` mit denselben expliziten Overrides: Exit 2
  aufgrund derselben Checkout-Einschränkung. Kein Submodul oder Symlink ergänzt.
- Natives `ci/tools/new-change-record.py check`: Exit 0, nur die Struktur des
  gepaarten Archivs. `git diff --check`, `py_compile` beider geänderter Tests
  und ShellCheck der externen Validierungshelfer: Exit 0. `rtk --version`:
  `0.51.0`; `rtk gain` verfügbar; keine Hook- oder Tool-Installation durchgeführt.

Logs liegen im externen Task-Analyseverzeichnis
`analysis/nginx-all-required-20261008T124555Z/sonar-exception-r1`.

## Security-Auswirkung

Verhindert falsch positive Exception-Tests. Keine Produktberechtigung,
Freshness-Guardrail, Validator, Exception-Anforderung, Abhängigkeit oder
Quality Gate wird abgeschwächt.

## Runtime-Evidence

Keine. Kontrollierte Unit-Kollaboratoren und Dateisystem-Projection-Vorbereitung
beweisen keine gehosteten NGINX-Requests, Root/nobody-Prozessrollen oder
Canonical-Coverage.

## Bekannte Einschränkungen

Die AST-Prüfung charakterisiert nur die drei gemeldeten Kontexte, nicht den
vollständigen Sonar-Analyzer. Remote-Schließung erfordert eine frische Analyse
der veröffentlichten Revision. Vollständige Dokumentations-Linkprüfungen
benötigen einen bestückten Integrations-Checkout.

## Verbleibende Risiken

Unabhängige Integrationsvalidierung und Remote-Sonar-Readback bleiben erforderlich.
Das Ergebnis der 25 Tests belegt kein vollständiges Repository- oder Runtime-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Build, gehostete Runtime, vollständige Repository-Suite,
Scanner-Authentifizierung, privilegierter Test oder administrativer Vorgang
wurde in diesem isolierten Slice ausgeführt. Root verantwortet die parallele
Exact-Head-Integration/Runtime und anschließende Veröffentlichung.

## Finaler Diff- und Review-Status

Minimaler Fixture-Diff mit allen bestehenden negativen Assertions geprüft;
technische EN/DE-Fakten stimmen überein. Dieser Task hat keinen Commit, Push,
PR-Statuswechsel, Framework/MRTS-Eingriff oder Runtime-Nachweis vorgenommen.
Die abschließende Archiv-/Whitespace-Validierung steht im externen Handoff;
vollständige Dokumentations-Linkprüfungen bleiben wie beschrieben eingeschränkt.
