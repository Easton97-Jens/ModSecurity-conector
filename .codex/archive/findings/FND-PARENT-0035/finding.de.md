# Finding: Rohe native Regeln verleihen LibModSecurity Dateisystem- und Prozessausgabeautorität außerhalb der Case-Wurzel

**Sprache:** [English](finding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0035` |
| Kategorie | `security_validated` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P0` / `high` / `reproduced` |
| Status | `fixed` |
| Release-Blocker / sicherheitsrelevant | ja / ja |

## Zusammenfassung, Verhalten und Auswirkung

Rohe native Regeln konnten `SecDebugLog`/`SecAuditLog` überschreiben und
ressourcen-/prozess-/CWD-sensitive Library-Verhalten anfordern. Ein
kontrollierter Case erzeugte externe benachbarte Library-Ausgabe selbst nach
Parent-Case-Root-Vorbereitung. Ein Case-Autor konnte außerhalb der
verifizierten nativen Wurzel schreiben, Seiteneffekte auslösen oder
veränderbaren CWD-relativen State konsumieren.

Erwartet sind ausschließlich Parent-besessene Ergebnis-/Server-Log-
Deskriptoren und ein verifizierter 0700-deskriptorbesessener CWD; Regeln dürfen
keine Library-Pfad-, Ressourcen-, Prozess- oder unbesessene-State-Autorität
verleihen.

## Betroffener Umfang und Voraussetzungen

- Dateien/Symbole: `run-native-case-comparison.py`,
  `native_modsecurity_oracle.c`, native Rule-Materialisierung,
  `run_oracle_with_owned_outputs`, `fchdir` und `open_output_fd`.
- Eine rohe native Regel erreicht den Comparison-Runner, und LibModSecurity
  parst sie vor dem gefixten Authority-Gate.

## Reproduktion und Evidenz

1. `SecDebugLog` oder `SecAuditLog` mit einem benachbarten externen Pfad
   liefern.
2. Einen nativen Case laufen lassen; mit finalem Link auf fremden Sentinel
   wiederholen.
3. Die erhaltene Exact-Head-Evidenz hat den historischen Pfad
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/native-rule-output-revalidation.md`
   (nicht in diesem Reconciliation-Checkout verteilt),
   SHA-256 `54aeaa1474c35daa8793da3d5254f01fb9e751be338daf11e0e14b3620db3b0e`.
   21 Tests bestanden auf `0e55bb5e8444b99a9b4eaf50cd22679fe5d6f273`; die
   echte LibModSecurity-3.0.16-Kontrolle erreichte Status 200, während
   unsichere Varianten vor dem C-Oracle abgewiesen wurden und Sentinels
   bewahrten.

## Root Cause und Remediation

Sichere Case-Root-Allokation wurde gefolgt von der Behandlung untrusted Regeln
als Autorität für Library-Datei-/Ressourcen-/Prozess-APIs. PR C weist unsichere
Direktiven/Operatoren/Aktionen fail-closed ab, entfernt die Library-Audit- /
Debug-Pfadpräambel, behält Parent-besessene Output-FDs und prüft einen privaten
State-FD vor `fchdir`.

## Akzeptanz, Validierung und Kontrollen

- Originale und finale-Link-Audit-/Debug-Varianten scheitern vor dem C-Oracle.
- Ressourcen-/Prozess-/Output-Escapes scheitern; eine `initcol`/`setvar`-
  Status-200-Kontrolle gelingt mit deskriptorbesessenem CWD/FDS.
- `tests/test_runtime_env_snapshot_contract.py` bestand 21/21; Clang C17 und
  GCC C17 `-fanalyzer` bestanden.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Dies nutzt PR-A-Descriptor-Primitive (`FND-PARENT-0033`), ist aber nicht
derselbe Root Cause. `FND-PARENT-0036` ist ein getrennter C-Lifetime-Defekt.
Vollständige Framework-/MRTS-Native-Matrix-Integration ist
`blocked_missing_evidence`; der lokale Fix ist delivery-pending bis Exact-PR-
CI-/Review-Evidenz vorliegt. Kein Risk Acceptance oder Merge ist autorisiert.

## Historie

- `2026-07-18T14:46:42Z`: reale Library-Escape-Evidenz und Exact-PR-C-Head-
  Kontrollen bestanden; Status auf `fixed` pending verified PR gesetzt.
