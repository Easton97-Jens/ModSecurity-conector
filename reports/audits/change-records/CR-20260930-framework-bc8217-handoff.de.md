# Change Record: Framework-Candidate-Übergabe bc8217d

**Sprache:** [English](CR-20260930-framework-bc8217-handoff.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-framework-bc8217-handoff |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `9bc87cbdb600b09c6edd02667a75b117a1f09eea` |

## Motivation und Problemstellung

[GitHub-Actions-Job 109955091216](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36735191087/job/109955091216) verwirft Framework-Candidate `bc8217d325809b9aba9a1d8c16964d71a01933ee` mit `Framework common.sh differs from approved reviewed structure`. Der Candidate überschreitet den im Parent freigegebenen normalisierten Strukturhash; deshalb kann der Submodule-Updater keine konsistente Übergabe veröffentlichen.

## Akzeptanzkriterien

Den exakt geprüften Framework-Candidate pinnen, nur seine registrierten Parent-Projektionen und die generierten zweisprachigen Compiler-Guides aktualisieren und den unabhängig berechneten normalisierten Candidate-Hash in Verifier und Regressionstest übernehmen. Quellfeld-Allowlist, Candidate-Validierung, Workflow-Rechte und No-Auto-Merge-Verhalten unverändert lassen. Erforderliche CI- und Runtime-Prüfungen müssen vor einem Merge bestehen.

## Implementierungsentscheidung und Begründung

Den Parent-Framework-Gitlink von `0290a979ba4bc63a7abed175a53471367b385553` auf `bc8217d325809b9aba9a1d8c16964d71a01933ee` anheben. Im Candidate ändern sich 17 Zuweisungswerte in `common.sh`, jedoch kein Shell-Kontrollfluss; ModSecurity-v3- und HAProxy-Quellfelder sind bereits registriert, während PCRE2, OpenSSL, Node, CodeQL und Ruff absichtlich der exakten Strukturprüfung unterliegen. Den freigegebenen normalisierten Hash `eed16dbe606c2770cf830cdb06884c7a5f68544e13c7f5ebb3106d3107e11fdc` in Verifier und Test setzen, ohne die Allowlist veränderbarer Felder zu erweitern. Die sechs geschlossenen Parent-Ziele synchronisieren, einschließlich HAProxy 3.2.23 auf 3.2.25 und ModSecurity v3.0.16 auf v3.0.17 (`1925753989ccce977cdaae417b55c9726c7cf02c`). Guide-Generator-Konstanten und die zugehörigen englischen/deutschen Ausgaben gemeinsam aktualisieren.

## Geänderte Dateien

- `modules/ModSecurity-test-Framework`
- `ci/tools/verify-framework-candidate-contract.py`
- `tests/test_verify_framework_candidate_contract.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/haproxy/htx-overlay/version-contract.json`
- `scripts/generate_compiler_guides.py`
- `tests/test_compiler_guides.py`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `tests/test_ci_security_workflows.py`
- `docs/build/compilers/libmodsecurity.md`
- `docs/build/compilers/libmodsecurity.de.md`
- `reports/audits/change-records/CR-20260930-framework-bc8217-handoff.md`
- `reports/audits/change-records/CR-20260930-framework-bc8217-handoff.de.md`

## Ausgeführte Befehle

Der fehlgeschlagene Job-Log, aktuelle Parent- und Framework-Revisionen, Candidate-`common.sh`, registrierte Synchronisierungsziele und betroffene Parent-Dateien wurden über die GitHub-Verbindung geprüft. Die Änderungen exakter Werte wurden im Speicher gegen die geschlossenen Registries abgeglichen. Es wurde kein lokaler Repository-Befehl ausgeführt; bei Erstellung dieses Records wird kein Hosted-Check als bestanden behauptet.

## Security-Auswirkung

Dies ist eine explizite Freigabe des exakten Framework-Candidate, der auch Änderungen an Security-Workflows und der Updater-Policy enthält. Der Parent-Candidate-Verifier behandelt `common.sh` weiterhin als Daten und behält seine Validierungs- und Pfadgrenzen bei. Keine Regel, Berechtigung, Quality Gate oder Allowlist veränderbarer Felder wird gelockert. Framework-Submodule-Diff und Release-Provenienz vor einem Merge prüfen.

## Runtime-Evidence

Allein durch Pin- und Dokumentationsänderung wird kein neues Connector-Runtime-, ABI- oder WAF-Verhalten nachgewiesen. Dafür sind Hosted-Tests und Runtime-Prüfungen für den PR-Head erforderlich.

## Bekannte Einschränkungen

Die unabhängige Prüfung bestätigte die PCRE2-, OpenSSL- und Ruff-Asset-Hashes sowie die CodeQL- und ModSecurity-Tag-Commits; der HAProxy-3.2.25-Archiv-Hash wurde nicht unabhängig abgerufen. Der SonarQube-MCP-Server war in dieser Task-Umgebung nicht erreichbar.

## Verbleibende Risiken

Der Framework-Candidate ändert neben ModSecurity v3.0.17 auch Upstream-Dependency-Pins und Security-Automation. Build-, Runtime- und Kompatibilitätsregressionen bleiben möglich, bis die Exact-Head-Prüfungen des PR und eine menschliche Prüfung abgeschlossen sind.

## Nicht ausgeführte Prüfungen mit Begründung

Der Repository-lokale Secrets-Scan, der offizielle Synchronisierer und Guide-Generator, fokussierte Unittests, zweisprachige Dokumentationsprüfungen, `git diff --check`, SonarQube-Analyse und Runtime-Prüfungen konnten in dieser projektlosen Windows-Task nicht laufen: SonarQube-MCP startete nicht, die vorhandene CLI war nicht authentifiziert, und eine neue Credential-Freigabe wurde nicht erteilt. Statische Diff-Prüfung ersetzt diese Prüfungen nicht.

## Finaler Diff- und Review-Status

Als Draft PR gegen `master` ausliefern. Kein Merge oder direkter Schreibzugriff auf `master` ist autorisiert. Finalen Diff und Hosted-Checks des aktuellen Heads prüfen und diesen Record vor jedem Merge um tatsächliche Ergebnisse ergänzen.
