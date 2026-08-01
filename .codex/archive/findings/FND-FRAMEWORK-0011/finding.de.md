# FND-FRAMEWORK-0011 — Protocol-URL-Command-Evidence kann einen undurchsichtigen Pfadabschnitt behalten

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0011` |
| Titel / Title | `Protocol-URL-Command-Evidence kann einen undurchsichtigen Pfadabschnitt behalten` |
| Kategorie / Category | `security_candidate` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priorität / Priority | `P2` |
| Schweregrad / Severity | `medium` |
| Konfidenz / Confidence | `candidate` |
| Status | `closed` |
| Machbarkeit / Feasibility | `requires_user_decision` |
| Release-Blocker / Release blocker | `false` |
| Security-Relevanz / Security relevance | `true` |

## Zusammenfassung / Summary

Das öffentliche `protocol-client`-Target kann nach Redaction nur von Userinfo/Query einen `PROTOCOL_URL`-Pfadabschnitt in `client-command.txt` behalten, und ein Full-Lifecycle-Pfad kann das Artefakt in kanonische Evidence kopieren.

## Beobachtetes Verhalten / Observed behavior

`_safe_url_for_command()` behält `parsed.path`; `_redacted_command()` rendert ihn; `_write_artifacts()` schreibt ihn; und `copy_protocol_client_artifacts()` kann das Command-Artefakt ohne weiteren Pfad-Redaction-Pass kopieren. Bestehende Tests beweisen nur Query-Redaction.

## Erwartetes Verhalten / Expected behavior

Evidence-Command-Artefakte dürfen keine undurchsichtigen URL-Pfadsecrets oder sensiblen direkten CLI-Resolution-Mappings behalten. Eine nützliche nicht-sensitive Endpoint-Repräsentation darf nur bei expliziter Sicherheit verbleiben.

## Auswirkung / Impact

Ein Aufrufer, der ein Token oder einen Personenwert in einen dokumentierten Protocol-URL-Pfad einbettet, könnte Retention und Kopie in Evidence auslösen. Tatsächliche produktive Pfadsensitivität und Evidence-Lesezugriff wurden nicht belegt.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `ci/checks/protocol/protocol_client.py`
- `ci/checks/catalog/no_crs_baseline.py`
- `ci/checks/protocol/check_protocol_evidence.py`
- `tests/protocol_client/test_protocol_client.py`
- `docs/reference/variables.md`
- `docs/testing-and-evidence.md`

### Symbole / Symbols

- `_safe_url_for_command`
- `_redacted_command`
- `_write_artifacts`
- `copy_protocol_client_artifacts`
- `PROTOCOL_URL`

## Voraussetzungen / Preconditions

- Ein Aufrufer liefert einen sensiblen undurchsichtigen Pfad über dokumentiertes `PROTOCOL_URL` oder die direkte CLI-URL-Option.
- Der Protocol-Client schreibt sein verwaltetes Artefakt-Bundle.
- Der Full-Lifecycle-Artefakt-Copy-Pfad ist für kanonische Retention ausgewählt.

## Reproduktion / Reproduction

- `protocol_client.py:589-631,1186-1201` und `no_crs_baseline.py:3956-3998` prüfen.
- Query-only-Unit-Coverage in `tests/protocol_client/test_protocol_client.py` prüfen.
- Kein Live-Artefakt mit einem Secret erzeugen, bis ein sicherer synthetischer Validierungsplan autorisiert ist.

## Evidence / Evidence

- Run-ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/protocol-url-redaction-candidate.md`
  - Typ: `static_source_to_sink_security_review`; SHA-256: `94fdd47764c82a3453e7b599212cd66f636f8d8468bcb57adef074894c7ad7bd`
  - Befehl: `rtk sed -n '589,631p;1186,1201p;1472,1475p' ci/checks/protocol/protocol_client.py; rtk sed -n '3956,3998p' ci/checks/catalog/no_crs_baseline.py`
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-common-structure`; Exit-Code: `0`
  - Beobachtet am: `2026-07-18T09:27:57Z`; Retention: `retained_task_evidence`

## Grundursachenanalyse / Root-cause analysis

Die Command-Artefakt-Redaction schützt Query-Strings und Userinfo, behält aber alle Pfadabschnitte. Copier und Validator bieten keine unabhängige Pfad- oder `--resolve`-Redaction-Kontrolle.

## Vorgeschlagene Remediation / Proposed remediation

Nach fokussierter Validierung Artefakt-URLs auf sichere Authority plus expliziten redigierten Pfadmarker reduzieren, direkte `--resolve`-Werte redigieren, synthetische Pfad-/Percent-Encoding-/IPv6-Coverage ergänzen und harmlose Diagnostik nur bei Begründung erhalten.

## Akzeptanzkriterien / Acceptance criteria

- Synthetische secret-ähnliche Pfade erscheinen nicht in `client-command.txt` oder kopierter kanonischer Evidence.
- Direkte `--resolve`-Werte sind redigiert oder nachweislich ausgeschlossen.
- Query, Userinfo, harmloser Health-Pfad, IPv6 und legitime Protocol-Client-Controls bestehen.
- Kein aktuell benutzerautorisierter Remediation-Scope wird überschritten.

## Validierungsplan / Validation plan

- Vor einem Fix Codex-Security-Validation nutzen, um Boundary, synthetische Artefaktpersistenz und Reader-Exposure-Annahmen festzustellen.
- Bei Bestätigung und separater Autorisierung `fix-finding` mit fokussierten Protocol-Client- und Artifact-Copy-Regressionen nutzen.
- Den protocol-contract-Workflow am exakten zukünftigen PR-Head ausführen.

## Regressionstests / Regression tests

- `tests/protocol_client/test_protocol_client.py` mit synthetischen undurchsichtigen, percent-encoded, IPv6- und `--resolve`-Fällen.
- Eine Full-Lifecycle-Copied-Artifact-Redaction-Kontrolle.

## Legitime Kontrolltests / Legitimate control tests

- Eine harmlose `/health`-URL bleibt ohne sensiblen Pfadwert diagnostisch nützlich.
- Bestehende Query- und Userinfo-Redaction bleibt intakt.

## Abhängigkeiten / Dependencies

- Aktuelle Benutzerautorisierung für eine separate Remediation, wenn Validation eine reportable unterstützte Boundary bestätigt.

## Blocker / Blockers

- Der aktuelle Task-Scope ist die unabhängige common-structure-CI-Reparatur.
- Pfadsensitivität, Evidence-Reader-Zugriff und dynamische Artefaktpersistenz sind noch nicht validiert.

## Verwandte Findings / Related findings

- `FND-FRAMEWORK-0001`
- `FND-SONAR-0002`

## Restrisiko / Residual risk

Die Resulting-Master-Regression prüft die Redaction undurchsichtiger Pfade und `--resolve`-Werte bei Erhalt harmloser Health-, Query-, Userinfo-, IPv6- und Protocol-Client-Kontrollen. Es wurde keine Risikoakzeptanz verwendet.

## Historie / History

- `2026-07-18T09:27:57Z`: `current_task_static_candidate_triaged` — Statische Source-to-Sink-Evidence fand einen öffentlichen Protocol-URL-Pfad-Retention-Kandidaten. Kein Live-Secret-Artefakt, Exploit oder Remediation wurde ausgeführt; der Kandidat ist getrennt von common-structure- und Sonar-Remediation.
- `2026-07-26T16:13:56Z`: `remediation_fixed` und `resulting_master_verified_and_closed` — Framework-PR #50 ergänzte begrenzte Command-Artefakt- und `--resolve`-Redaction plus unabhängigen Evidence-Validator. Exakter Framework-Master `de705a5efb872f95f010346fe2e6143c88876ad4` bestand 28 fokussierte Protocol-/Evidence-Tests; PR-#50-SonarQube-Cloud ist `OK` mit null ungelösten Issues. Receipt: `.codex/runs/20260726T160903Z-framework-pr50-pr51-master-verification/finding-closure-evidence.md` (SHA-256 `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`).
