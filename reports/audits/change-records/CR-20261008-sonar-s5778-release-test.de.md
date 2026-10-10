# Change Record: CR-20261008-sonar-s5778-release-test

**Sprache:** [English](CR-20261008-sonar-s5778-release-test.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-sonar-s5778-release-test |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `3ddeb8f6bfab3c619e6db50c2b0621dc0a504c19` |

## Motivation und Problemstellung

Die aktuelle PR396-Analyse gehört zu 810a9b5621b04c79d58b1429c3182f1668e672c9. Sonar-Issue AaEX3Mmerf44IvJc6hHr, python:S5778, meldet mehrere potenziell fehlschlagende Aufrufe im Release-Tupel-Exception-Test in Zeilen 501–502. Lint-Run 37675358566 scheitert in Zero-Findings-/Duplication-Voraussetzungsprüfungen an genau diesem Issue; Lightweight-Lint wurde übersprungen, kein gemessener Ruff-Fehler.

## Akzeptanzkriterien

Nur die beabsichtigte Operation `candidate_manifest()` verbleibt innerhalb der Exception-Assertion. Derselbe LauncherError, dieselbe Meldung und alle drei Negativkontrollen alter/gekreuzter Versionen/Digests bleiben geprüft. Keine Suppression oder Qualitätsvertragsänderung.

## Implementierungsentscheidung und Begründung

`dispatcher_payload()` vor Eintritt in die Assertion vorbereiten. Der Test prüft weiterhin genau die Release-Ablehnung des Candidate-Manifests; ein Setupfehler kann nicht mehr die falsche Assertion erfüllen.

## Geänderte Dateien

`tests/test_nginx_exact_head_root_launcher.py` und dieses EN/DE-Nachweispaar. Keine Änderungen an Produktivsource, Framework/MRTS, Gitlinks oder Release-Digest.

## Ausgeführte Befehle

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_exact_head_root_launcher` vor und nach der Änderung: 47 Tests PASS, 0 SKIP, Exit 0. Die offizielle Sonar-Regel wurde per authentifizierter API gelesen. Syntax, Dokumentationsprüfungen und `git diff --check` sind vor dem Commit erforderlich.

## Security-Auswirkung

Release-Version-/Digest-Ablehnung bleibt strikt; alle drei ungültigen Tupel-Kontrollen behalten erwartete Exception und Regex. Keine Issue-Akzeptanz, NOSONAR, Exclusion, abgeschwächte Assertion oder Runtime-Evidence-Änderung.

## Runtime-Evidence

Eine Teststrukturkorrektur belegt keine Runtime. Der frische lokale Standard-Lifecycle ist eine getrennte nachfolgende Validierung.

## Bekannte Einschränkungen

Das Basis-Quality-Gate ist OK mit einem offenen Code Smell. Erst eine frische Analyse des veröffentlichten neuen Heads kann die Behebung nachweisen; grüne lokale Unit-Tests sind kein Sonar-PASS.

## Verbleibende Risiken

Weitere unabhängige Coverage-Lücken und Protected-Freigaben bleiben außerhalb dieses Fixes. Remote-Analyse kann weiterhin warten oder laufen.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger nativer Lint und CI/Sonar des frischen Heads folgen der stabilen Veröffentlichung; ihre Zustände werden nicht aus Basis-Ergebnissen abgeleitet.

## Finaler Diff- und Review-Status

Minimaler Drei-Zeilen-Testdiff gegen aktuelles Issue und offizielle Regel geprüft. Eigenständiger C-Commit folgt den Fokustests; keine fremde Source oder Evidence enthalten.
