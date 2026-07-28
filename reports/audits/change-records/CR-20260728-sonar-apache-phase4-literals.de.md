# Change Record: Parent-Apache-Phase-4-Control-Literal-Ownership für SonarQube Cloud S1192

**Sprache:** [English](CR-20260728-sonar-apache-phase4-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260728-sonar-apache-phase4-literals` |
| Datum (UTC) | `2026-07-28` |
| Basis-Revision | `8e8acb8dab1cd03723de269cab7da7dd62e5e010` |
| Kandidatenbezeichnung | Parent-Task-Kandidat. Diese lokale Bezeichnung behauptet keinen gehosteten Pull Request, Remote-Head, Review, Quality Gate oder Delivery-Ergebnis. |
| Tracking | `AZ98JczJLJyjbmyNA5LT` und `AZ98JczJLJyjbmyNA5LN`; beide sind vor diesem Kandidaten Live-Parent-`shelldre:S1192`-Findings. |
| Grenze | Parent-Apache-Phase-4-Smoke-Harness, sein direkter Source-Wiring-Test, dieses englisch/deutsche Change-Record-Paar und seine zwei Indizes. Framework, MRTS, Gitlinks, Workflows, Reports, Scanner-Policy und gehosteter Status bleiben unverändert. |

## Motivation und Problemstellung

Der Apache-Phase-4-Smoke-Harness wiederholte das feste Response-Präfix
`first-byte-prefix` in vier Body-Leak-Prüfungen und die feste fail-closed
Log-Meldung `request transaction cannot be safely rebound to the target URI` in
sechs Redirect-/ErrorDocument-Prüfungen. SonarQube Cloud meldet beide
Wiederholungen als S1192-Maintainability-Findings. Dies sind Response- und
Redirect-Integritätskontrollen; Literal-Ownership darf deshalb weder eine
Assertion abschwächen noch ein Grep-Argument ändern oder einen Non-success- /
Refusal-Pfad erfolgreich machen.

## Akzeptanzkriterien

- `PHASE4_FIRST_BYTE_PREFIX` besitzt genau die vier ausgewählten festen
  Grep-Patterns, und jede Verwendung bleibt ein quoted `grep -F`-Argument
  gegen den Response-Body.
- `PHASE4_TRANSACTION_REBIND_REFUSAL` besitzt genau die sechs ausgewählten
  festen Grep-Patterns, und jede Verwendung bleibt ein quoted `grep -F`-
  Argument gegen das Apache-Error-Log.
- Bypass-, Precommit-Deny-, Custom-MIME-Deny-, Engine-Append-Failure-, Internal-
  Redirect-, Nested-ErrorDocument- und Preoutput-ErrorDocument-Controls
  behalten ihre bestehenden Fehlerbedingungen und Diagnosemeldungen.
- Shell-Syntax, direkte Source-Wiring-Tests, Whitespace, Security-Review,
  bilinguale Dokumentation und spätere Exact-Head-Hosted-Evidence werden
  wahrheitsgemäß festgehalten.

## Implementierungsentscheidung und Begründung

Der Harness deklariert zwei POSIX-`readonly`-Werte nahe seiner file-local
Runtime-Konfiguration:

- `PHASE4_FIRST_BYTE_PREFIX`
- `PHASE4_TRANSACTION_REBIND_REFUSAL`

Jeder Wert wird aus seinem exakten früheren single-quoted Literal initialisiert
und nur durch eine double-quoted Expansion verwendet. Die Refaktorierung
erhält Fixed-String-Matching, genau ein Shell-Argument, die durchsuchte Datei,
Redirects, `|| fail`-Control-Flow und alle bestehenden Fehlermeldungen. Die
zwei vollständigen Expected-Response-Body-Literale bleiben bewusst getrennt,
weil sie vollständigen erlaubten Body-Content statt der vier gemeldeten
Prefix-Search-Calls prüfen.

Der direkte Source-Wiring-Test verifiziert eine Deklaration pro Konstante, das
Fehlen der alten raw Grep-Formen, das Fehlen unquoted Variable-Formen, genau
vier/sechs quoted Grep-Verwendungen sowie die erhaltenen Response-Leak- und
Transaction-Rebind-Diagnose-Contracts.

## Geänderte Dateien

- `connectors/apache/harness/run_apache_smoke.sh`
- `tests/test_apache_phase4_response_regression_wiring.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-phase4-literals.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-phase4-literals.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Tatsächliches Ergebnis |
| --- | --- |
| `sh -n connectors/apache/harness/run_apache_smoke.sh` im exakten Task-Worktree | bestanden. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B tests/test_apache_phase4_response_regression_wiring.py` mit `PYTHONNOUSERSITE=1` und `PYTHONDONTWRITEBYTECODE=1` im exakten Task-Worktree | bestanden: 11/11 Tests. |
| `git diff --check` | bestanden; kein Whitespace-Fehler. |
| Fokussierte Shell-/Protocol-Sicherheitsreview | genehmigt; kein plausibles oder validiertes Finding. |
| Disposable Exact-Candidate-Parent-/Framework-Dokumentationsoverlay | bestanden: bilinguale Dokumentation, Repository-Pfad-Referenzen und Framework-Dokumentlinks. |

## Security-Auswirkung

Die geänderten Werte sind feste Grep-Patterns an einer Response-Body-Leak-
Erkennung und einer fail-closed Redirect-Grenze. Die Review verifizierte, dass
kein Request-, Response-, Environment- oder Command-Substitution-Wert eines der
Patterns beeinflussen kann: Beide sind hard-coded `readonly`-Werte und jede
Expansion ist double quoted. `grep -F` behandelt Response-Bodies und Logs
weiterhin als durchsuchte Daten, nicht als Shell-Code.

Der Bypass-Branch verlangt weiterhin das Präfix. Precommit-Deny, Custom-MIME-
Deny und Engine-Append-Failure schlagen weiterhin fehl, wenn es erscheint.
Alle sechs Redirect-/ErrorDocument-Pfade verlangen weiterhin den Rebind-
Refusal-Log-Eintrag und behalten ihre Non-success- und Body-Leak-Assertions.
Es wurde keine gebrochene Kontrolle und kein reportable Security-Finding
identifiziert.

## Runtime-Evidence

Es wurde keine Apache-Host-Runtime, Connector-Matrix-, Framework- oder MRTS-
Runtime gestartet. Shell-Syntax und der direkte Source-Wiring-Test belegen nur
den statischen Harness-Contract; sie belegen weder Deployment-Kompatibilität
noch ein End-to-End-Apache-Runtime-Ergebnis.

## Bekannte Einschränkungen

Dieser Record besitzt noch keine gehostete Exact-Head-Pull-Request-,
SonarQube-Cloud-Post-Change-Issue-, Quality-Gate-, Workflow-, Review-, Merge-
oder Default-Branch-Evidence. Die bestehende Apache-Runtime/Matrix bleibt
absichtlich außerhalb dieses Literal-Extraction-Scopes.

## Verbleibende Risiken

Eine spätere Harness-Änderung könnte ein äquivalentes nicht besessenes
Grep-Literal hinzufügen oder einen Body-/Redirect-Contract außerhalb dieses
Scopes ändern. Die file-local Owner, der direkte Test, der Shell-Syntax-Check
und die fokussierte Security-Review reduzieren dieses Risiko. Frische
Exact-Head-Hosted-Analyse bleibt erforderlich, bevor die zitierten SonarQube-
Cloud-Receipts als behoben gelten können.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Apache-Host-Build, Real-Smoke-Runtime, Full-Matrix, Report-Generierung,
  Workflow-Ausführung, Framework-Source-Check oder MRTS-Check wurde ausgeführt;
  jeder liegt außerhalb dieser Parent-only statischen Extraktion.
- `make check-bilingual-docs` wird im Task-Worktree nicht direkt ausgeführt,
  weil sein gepinnter Framework-Gitlink absichtlich fehlt. Stattdessen bestand
  der exakte Kandidat zusammen mit dem read-only Parent-gepinnten Framework-
  Archiv die drei Repository-Dokumentationschecks in einem disposable externen
  Overlay.
- Gehostete PR-/Sonar-Evidence liegt noch nicht vor. Ein Exact-Head-Hosted-
  Zyklus ist erforderlich, bevor die Delivery als verifiziert gilt.

## Finaler Diff- und Review-Status

Der lokale Kandidat ändert nur die zwei festen Literal-Owner, ihre vier und
sechs bestehenden Grep-Verwendungen, direktes Wiring-Coverage und dieses
gepaarte Traceability-Update. Die oben genannte Syntax-/Test-/Whitespace- /
Security-Evidence besteht. Es werden weder Commit, Push, Pull Request,
gehosteter Check, Quality Gate, Review, Merge, Master-Änderung, Framework-/
MRTS-Änderung, Gitlink-Update, Workflow-Änderung noch Scanner-Policy-Aktion
behauptet.
