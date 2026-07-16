# Change Record: CI-Sicherheits-Härtung

**Sprache:** [English](CR-20260716-ci-security-hardening.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260716-ci-security-hardening` |
| Datum (UTC) | `2026-07-16` |
| Basis-Revision | `c8450a9feaef3da9c999586ea60398653601f037` |
| Grenze | Nur Parent-CI, Dokumentation und Nachvollziehbarkeit; Framework und MRTS unverändert. |

## Motivation und Problemstellung

Das Repository verwendete veränderliche GitHub-Action-Tags und hatte keine
saubere, dokumentierte allgemeine CI-Sicherheitsbasis. Der alte Sicherheits-PR
mischte diesen nützlichen Umfang mit repository-eigenen Codex-Agenten, Skills,
Hooks, Extension-Verträgen und historischen Records, die absichtlich nicht
übernommen werden.

## Akzeptanzkriterien

- Alle Remote-GitHub-Actions-Workflow-Referenzen verwenden aufgezeichnete
  unveränderliche SHAs.
- Workflow-Linting, redigiertes PR-Range-Secret-Scanning, advisory
  Full-History-Scanning, exakter-SHA-OSV-Vergleich, begrenztes CodeQL und
  vertrauensbegrenzte Scorecard-Workflows sind vorhanden.
- Die Go-Module verwenden festes Go `1.24.0`; der C/C++-CodeQL-Scope ist als
  begrenzt beschrieben.
- Tool-Provenienz, Checksums, Lizenzen und minimale Berechtigungen sind
  aufgezeichnet.
- Englische/deutsche Dokumentation und dieses Change-Record-Paar beschreiben
  nur den erhaltenen allgemeinen CI-Sicherheitsumfang.

## Implementierungsentscheidung und Begründung

Es werden checksum-verifizierte offizielle Release-Binaries für `actionlint`,
`zizmor` und Gitleaks statt repository-eigener Codex-Werkzeuge verwendet.
GitHub Actions werden auf offizielle Tag-Commits festgelegt und die
Provenienz wird aufgezeichnet. OSV vergleicht die exakten Base- und Head-SHAs
des Events und ändert keine Dependency. Full-History-Gitleaks und zeitgesteuertes
OSV sind advisory, bis historische Findings triagiert sind.

## Geänderte Dateien

Geänderte Dateien beschränken sich auf Parent `.github/workflows/`, generische
CI-Sicherheitswerkzeuge und Fixtures, fokussierte CI-Sicherheitstests/Make-Target,
englische/deutsche CI-Sicherheits- und Audit-Dokumentation sowie dieses
Change-Record-Paar. Keine `.agents/**`-, Codex-Skill-, Agent-, Hook-Policy-,
Extension-Vertrags-, Framework-, MRTS- oder Gitlink-Datei wird geändert.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | bestanden: 5 fokussierte statische Tests und alle drei Downloaded-Binary-Lock-Einträge validiert. |
| `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | bestanden. |
| `PYTHONDONTWRITEBYTECODE=1 make check-doc-links` | bestanden, einschließlich des Framework-Dokumentationslink-Checkers. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile ci/tools/fetch_security_tool.py tests/test_ci_security_workflows.py` | bestanden. |
| Checksum-verifiziertes `actionlint` mit verfügbarem ShellCheck über alle Workflow-Dateien | bestanden. |
| Checksum-verifiziertes `zizmor --offline .github/workflows` | bestanden: keine Findings (die Upstream-Baseline weist 77 konfigurierte Suppressions aus). |
| `zizmor`-sichere und absichtlich unsichere Fixtures | bestanden: sichere Fixture akzeptiert; unsichere Fixture erwartungsgemäß abgelehnt. |
| Checksum-verifiziertes Gitleaks über `c8450a9feaef3da9c999586ea60398653601f037..HEAD` mit Redaction | bestanden: ein Commit gescannt; keine Leaks gefunden. |
| `git diff --check` | bestanden. |

Die lokal heruntergeladenen Validierungs-Binaries wurden nur über den
checksum-prüfenden Fetch-Helper in den registrierten task-eigenen temporären
Speicher bezogen. Die erforderliche GitHub-Workflow-Validierung gilt weiterhin
für den exakten Head-SHA des Ersatz-PRs.

## Security-Auswirkung

Der erhaltene Umfang führt nur CI-Analysen mit minimalen Leserechten ein. Er
aktiviert keine automatische Dependency-Remediation, Branch-Protection-Änderung,
Merge, Review-Umgehung oder Ausführung eines Fork-Heads. Tool-Downloads prüfen
einen aufgezeichneten SHA-256 vor dem Entpacken; die Workflow-Dokumentation
nennt die verbleibenden Scope- und Vertrauensgrenzen.

## Runtime-Evidence

Nicht anwendbar. Diese Änderung verändert keinen Connector-Code und etabliert
keine HTTP/1.1-, HTTP/2-, HTTP/3-, CRS-, MRTS- oder Host-Runtime-Evidence.

## Bekannte Einschränkungen

Die C/C++-CodeQL-Analyse ist auf reproduzierbare Common-Helper-C17-Prüfungen
begrenzt. Fork-Pull-Requests führen Scorecard nicht gegen einen nicht
vertrauenswürdigen Head aus. Gitleaks-Full-History und zeitgesteuerte OSV-Scans
sind bis zur historischen Triagierung advisory.

## Verbleibende Risiken

SHA-Pins beseitigen keine Risiken in Downstream-Action-Runtime-Abhängigkeiten
oder Container-Images. Statische und Dependency-Scanner können nicht
verfügbare, unerreichbare oder nicht quellbezogene Risiken übersehen; ihr
Ergebnis bleibt begrenzte Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Connector-Build, keine Runtime-, Protokoll-, Sanitizer-, vollständige
CRS/MRTS-Matrix- oder Dependency-Update-Prüfung läuft, weil dies
CI-Sicherheitsinfrastruktur ist. Erforderliche GitHub-Checks, Reviews und
SonarQube-Evidence des Ersatz-PRs werden nur für dessen exakten finalen
PR-Head-SHA erhoben.

## Finaler Diff- und Review-Status

Fokussierte lokale Validierung und begrenzte Diff-Prüfung bestanden.
Exact-SHA-Draft-PR-Prüfung, Review und SonarQube-Disposition stehen noch aus.
Alte PR-#44-Checks sind keine Evidence für diesen Record.
