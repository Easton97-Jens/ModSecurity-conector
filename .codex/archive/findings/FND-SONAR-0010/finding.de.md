# FND-SONAR-0010 — Parent-PR-#90-Go-Updater-Quality-Gate-Blocker

## Klassifikation

- **Kategorie:** `sonarqube_finding` (`reliability_and_duplication`)
- **Repository / Ownership:** `parent` / `parent`
- **Priorität / Schwere / Confidence:** `P1` / `not_applicable` / `confirmed`
- **Status / Feasibility:** `verified` / `feasible_now`
- **Release-Blocker:** ja
- **Security-relevant:** nein; die Remediation berührt dennoch sicherheitsrelevante Updater-Mechaniken und verlangt einen fokussierten Security-Diff-Review.

## Zusammenfassung

Parent-Draft-PR #90 beim exakten Head
`d99eafd76d9fdbef5b63a19d084fd2d7caff6c08` scheitert an seinem anwendbaren
SonarQube-Cloud-Quality-Gate. Das Gate meldet 15,9 % duplizierten neuen Code
(Maximum 3 %) und Reliability C (erforderlich A). Der einzige neue
Reliability-Bug ist `AZ-LhTtmzOcepZz2Zxpc`, Regel `python:S5850`, bei
`ci/checks/common/check-go-version-contract.py:24`. Der duplizierte Code
umfasst vor allem 183 von 451 neuen Zeilen in `scripts/update-go-version.py`
und 55 von 207 neuen Zeilen in `tests/test_update_go_version.py`. Die
Exact-Head-Evidence ordnet beide Bedingungen der ursprünglichen
Go-Zentralisierungs-Implementierung zu, nicht dem späteren dreidateiigen
Framework-Kompatibilitäts-Follow-up.

Die Reparatur extrahiert die gemeinsamen Updater- und Test-Support-Mechaniken,
belässt die getrennten Go-/Python-Endpoint-/Schema-/Version-Policy-Adapter und
macht das CodeQL-Go-Selector-Mapping exakt. Sie ist am exakten Head
`06a4e71408a60e5a72a55065a653b9c4e79a1ecf` verifiziert: Quality Gate ist
`OK`, New Reliability ist `A` und die Dichte duplizierten neuen Codes ist
0,0 %.

## Beobachtetes und erwartetes Verhalten

GitHub-Check-Run `89053617816` gehört zum aktuellen exakten PR-Head und meldet
Quality Gate `ERROR`. Der aufbewahrte Receipt erfasst 238 duplizierte Zeilen
von 1497 neuen Zeilen (15,898 %) sowie den einen `python:S5850`-Reliability-
Bug.

Der PR muss seinen fail-closed Central-Version-Contract, die offizielle
Release-Autorität, den begrenzten No-Redirect-JSON-Parser und symlink-sichere
atomare Version-File-Updates bewahren, während sein aktueller Head ein Quality
Gate ohne neuen Reliability-Bug und mit höchstens 3 % dupliziertem neuen Code
erreicht. Keine Regel, kein Quality Gate, keine Exclusion, Suppression,
False-Positive-Disposition oder Risikoakzeptanz darf geändert werden, um
dieses Ergebnis zu erzielen.

## Auswirkung

PR #90 kann nicht als verifizierter Delivery-Kandidat dargestellt werden,
solange sein aktueller Head das erforderliche Quality Gate nicht besteht.
Parallele Implementierungen sicherheitsrelevanter Release-Transport- und
Safe-File-Update-Mechaniken belassen zudem ein unnötiges Divergenzrisiko.

## Betroffener Scope und Voraussetzungen

- `ci/checks/common/check-go-version-contract.py` (`SETUP_GO_STEP`)
- `scripts/update-go-version.py` und `scripts/update-python-version.py`
- `tests/test_update_go_version.py` und `tests/test_update_python_version.py`
- Parent-Draft-PR #90 bleibt bei
  `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08` offen.
- GitHub-Check-Run `89053617816` und die SonarQube-Cloud-PR-Integration gelten
  für diesen exakten Head.

## Reproduktion und Evidence

1. PR #90 und Check-Run `89053617816` inspizieren; exakten Head
   `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08` bestätigen.
2. Die aufgezeichnete read-only-Abfrage ausführen:
   `rtk proxy curl -fsSL 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=90&ps=500'`.
3. `python:S5850` und die betroffenen Component-Measures mit dem PR-Diff
   vergleichen.

Aufbewahrte Evidence: `sonar-pr90-d99eafd-quality-gate.json` (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/sonar-pr90-d99eafd-quality-gate.json`), SHA-256
`e4d465b8cc49131866942eecc6f854bf578d5689a0f95131cab33d0fa797427b`.

## Grundursache und Remediation

Die ursprüngliche Go-Implementierung kopierte die Python-Updater-Mechaniken
für Transport, striktes JSON, Regular-File, atomisches Schreiben, CLI,
Fixture und Test-Harness in parallele Go-spezifische Dateien. Dadurch blieb
das Verhalten erhalten, jedoch entstand der gemeldete Klon. Der statische
CodeQL-Parser verwendet außerdem eine mehrzeilige Regex-Grenze mit
mehrdeutiger Präzedenz. Der spätere `d99eafd`-Follow-up ändert nur
Framework-Cache-Kompatibilitätstests und zweisprachige Change Records.

Die Remediation ersetzt die mehrdeutige Grenze durch einen expliziten sicheren
Parser oder eine gruppierte Grenze und extrahiert gemeinsame Updater-Mechaniken
und Test-Support in interne Parent-Module. Python und Go behalten getrennte
Endpoint-, Schema- und Version-Policy-Adapter. Kein Updater-Sicherheitscontrol
und kein Sonar-Control darf abgeschwächt werden.

## Akzeptanz und Validierung

- `python:S5850` fehlt am exakten PR-Head, während Static-Contract-
  Rejection-Verhalten erhalten bleibt.
- Gemeinsame Logik behält Endpoint-Equality vor `open`, No-Redirect, 2-MiB-
  begrenztes striktes JSON-Parsing, sichere Regular-File-Checks und atomische
  Updates.
- Beide Sprachadapter behalten CLI, JSON, Version-Schema und fail-closed-
  Verhalten.
- Exact-Head-SonarQube-Cloud hat keinen aufgabeneigenen Reliability-Bug und
  0,0 % duplizierten neuen Code ohne verbotenen Workaround.
- Fokussierte Updater-, Contract-, CI-Security-, Bilingual-, Diff- und
  Security-Diff-Validierung bestand lokal; gewöhnliche Exact-Head-Hosted-
  Checks sind terminal erfolgreich oder übersprungen.

Die finale lokale Validierungszusammenfassung erfasst 100 bestandene
fokussierte Tests, Python-Syntaxkompilierung, alle drei statischen Contract-
Targets, sichere Updater-`--help`-Smokes und Whitespace-Validierung:
sonar-remediation-final-local-validation.md (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/sonar-remediation-final-local-validation.md`)
(SHA-256 `444a215b5cf98118daf3032e38485b07b3d100ddb8e422cb41ebbeca92d5a624`).
Der vollständige finale Security-Diff-Scan meldet keinen reportable Finding:
report.md (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/tmp/codex-security-scans/ModSecurity-conector/d99eafd76d9_20260722T221118Z/report.md`)
(SHA-256 `12df4f3ed8d6f850feaf644a512d7bd1de0c3b41b6fffb5e99e021e21a25e1b4`).
Der frische Hosted-Receipt ist
hosted-pr90-06a4e71-validation.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/hosted-pr90-06a4e71-validation.json`)
(SHA-256 `db38c89e5c1646e343ec022466d7fec899998dda05558ccf85789196d273ea20`).

## Abhängigkeiten, Blocker und verwandte Findings

Frische Exact-Head-SonarQube-Cloud- und GitHub-Actions-Validierung bestanden.
Es gibt keinen aktuellen Implementierungsblocker. Dieses Finding ist von
`FND-PARENT-0045` (Update-submodules-Candidate-Kompatibilität) getrennt und
nur klassifikatorisch mit dem historischen Sonar-Remediation-Record
`FND-SONAR-0006` verwandt. Die nicht gate-blockierenden offenen Test-
Code-Smells werden getrennt durch `FND-SONAR-0011` erfasst.

`Update submodules` wird nicht ausgelöst, keine Master-Integration ist
autorisiert, und es erfolgten keine Framework-, MRTS-, Gitlink-, Regel-,
Quality-Gate-, Suppression- oder Risikoakzeptanz-Aktion.

## Verlauf

- `2026-07-22T21:25:24Z`: Aus aktueller Exact-Head-PR-#90-Evidence als
  bestätigter aufgabeneigener P1-Quality-Gate-Blocker angelegt; die fokussierte
  Remediation läuft.
- `2026-07-22T22:47:54Z`: Die lokale Remediation ist fixed: gemeinsame
  Updater-/Test-Mechaniken, exakter Selector-Contract, 100 fokussierte Tests,
  statische Contracts und ein vollständiger Security-Diff-Scan ohne Befunde
  bestanden. Die Aufgabe benötigt weiter Commit, normalen Push und ein
  frisches Exact-Head-Hosted-Quality-Gate.
- `2026-07-22T23:02:27Z`: Der exakte Head `06a4e71` bestand Quality Gate und
  gewöhnliche Hosted-Checks; dieses Finding ist verifiziert. Keine Master-
  Integration oder Update-submodules-Dispatch erfolgte.
