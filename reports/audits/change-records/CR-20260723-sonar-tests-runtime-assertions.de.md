# Change Record: Runtime-Test-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260723-sonar-tests-runtime-assertions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-tests-runtime-assertions |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Grenze | Ausschließlich Parent-Testquelle, dieses englische/deutsche Change-Record-Paar und Indizes. Framework, MRTS, Gitlinks, produktiver Connector-Quellcode, Scanner-Konfiguration, Quality Gates, Suppressions und Runtime-Verhalten bleiben unverändert. |
| Finding-Verknüpfung | Neun aktive Parent python:S3415 Code-Smells in den drei aufgeführten Testmodulen. AZ-KYVTnfYmbqbBXVNF9 bei tests/test_runtime_path_policy.py:184 ist als umgebungsblockiert ausgeschlossen und als FND-SONAR-0031 erfasst. |

## Motivation und Problemstellung

SonarQube Cloud meldet neun geprüfte python:S3415 Befunde in drei unabhängigen
Parent-Testmodulen. Jede ausgewählte unittest Assertion setzte einen festen
Expected-Wert vor ihr beobachtetes Prozessergebnis, geparste Payload,
Komponentenidentität oder einen Runtime-Pfad-Wert. Die Prädikate sind korrekt;
nur die diagnostische Operandenreihenfolge nicht.

Die exakten Keys sind AZ-KYVS5fYmbqbBXVNFm und AZ-KYVS5fYmbqbBXVNFn auf den
Zeilen 50 und 51 in tests/test_make_runtime_defaults.py; AZ-KYVUrfYmbqbBXVNGh,
AZ-KYVUrfYmbqbBXVNGi und AZ-KYVUrfYmbqbBXVNGj auf den Zeilen 89, 93 und 126
in tests/test_runtime_component_cache_identity.py; sowie AZ-KYVSKfYmbqbBXVNFQ,
AZ-KYVSKfYmbqbBXVNFR, AZ-KYVSKfYmbqbBXVNFS und AZ-KYVSKfYmbqbBXVNFT auf den
Zeilen 45, 214, 216 und 228 in tests/test_resolve_runtime_paths.py.

Der benachbarte Runtime-Path-Policy-Key bleibt getrennt, weil seine unveränderte
Baseline scheitert, wenn der isolierte Parent-Worktree
modules/ModSecurity-test-Framework/ci/lib/common.sh nicht laden kann. Eine
reine Diagnoseänderung ohne gültige Baseline könnte einen Path-Policy-Control-
Fehler verdecken.

## Akzeptanzkriterien

- Nur bei neun ausgewählten Assertions die ersten zwei Operanden tauschen.
- Prädikate, Fehlermeldungen, Subprocess-Aufrufe, Fixtures, Expected-Werte und
  Testergebnisse bewahren.
- Das vollständige Drei-Modul-Subset und ein AST-/Source-Inventar bestehen
  lassen, das genau neun Actual-first Aufrufe zeigt.
- Die negativen Runtime-Path-Resolver-Controls bewahren.
- Englische/deutsche Change Records und Indizes äquivalent halten.
- Exakte-Head-SonarQube-Cloud- und Hosted-Check-Evidence erhalten, bevor ein
  ausgewählter Key im Draft PR als gelöst gilt.

## Implementierungsentscheidung und Begründung

Nur die ersten zwei Positionsargumente ändern sich. Beobachtete Returncodes,
Payload-Felder, Shell-Werte, Component-Werte und Status stehen zuerst;
vorhandene Integer-, String-, List- und Set-Konstanten bleiben Expected. Drei
Returncode-Meldungen bleiben dritte Argumente. RuntimePaths.shell_values() wurde
als Frozen-Data-Konstruktion ohne relevante Nebenwirkung im Source geprüft.

Dies ist ein Drei-Dateien-Maintainability-Batch. Der blockierte Path-Policy-Test
wird nicht verändert und keine produktive Runtime-Source oder Security-Control-
Implementierung ändert sich.

## Geänderte Dateien

- tests/test_make_runtime_defaults.py
- tests/test_runtime_component_cache_identity.py
- tests/test_resolve_runtime_paths.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Offizielle SonarQube Cloud api/issues/search für zehn zunächst ausgewählte Keys | bestanden: alle zehn waren offene Parent MAJOR python:S3415 Code-Smells; neun sind hier umsetzbar. |
| Vier-Modul-Parent-Baseline vor der Änderung | blocked_environment: 20 Tests liefen, 19 bestanden und nur tests.test_runtime_path_policy scheiterte, weil Framework common.sh fehlt. |
| Unabhängige Drei-Modul-Baseline mit explizitem .venv, isoliertem TMPDIR und deaktiviertem Bytecode | bestanden: 14 Tests. |
| Kandidaten-Drei-Modul-Subset | bestanden: 14 Tests. |
| In-Memory-AST-Parse und Inventar | bestanden: genau neun ausgewählte assertEqual/assertNotEqual Aufrufe sind Actual-first; drei Fehlermeldungen bleiben. |
| Scoped git diff --stat, git diff --check und pyc-Scan | bestanden: drei Testdateien, neun Hinzufügungen/neun Entfernungen, keine Whitespace-Diagnose und keine Bytecode-Artefakte. |
| make check-bilingual-docs | blocked_environment: die einzigen 20 Diagnosen sind bereits vorhandene fehlende Framework-Gitlink-Link-Ziele; keine Diagnose nannte einen geänderten Change Record oder Index. |
| tests.test_bilingual_docs | bestanden: 11 Tests. |
| make check-doc-links | blocked_environment: die einzigen 16 Diagnosen sind bereits vorhandene fehlende Framework-Gitlink-Link-Ziele. |
| Fokussierter Codex-Security-Staged-Diff-Scan | bestanden: alle sieben gestagten Dateien erhielten Closure-Receipts; der kanonische Bericht hat vollständige Abdeckung und null berichtsfähige Befunde. |
| Exact-Head-Hosted-Checks | bis zur Draft-PR-Erstellung ausstehend. |

## Security-Auswirkung

Nur Parent-Tests änderten sich. Der Resolver-Test besteht weiterhin seine
vorhandenen Controls für breite oder systemeigene beschreibbare Roots,
Symlink-Escapes, Traversal, Foreign-Connectors, überlappende Basen und einen
Invocation-Root-Escape. Kein produktiver Parser, kein Untrusted-Input-Pfad,
keine File-Access-Kontrolle, kein Subprocess-Argument, keine
Executable-Auswahl, keine Konfiguration, Authentifizierung, Autorisierung,
Netzwerkoperation oder Runtime-Path-Policy-Implementierung änderte sich. Die
umgebungsblockierte Path-Policy-Assertion bleibt unverändert. Es wird kein
Security-Finding als behoben beansprucht. Ein fokussierter Codex-Security-
Staged-Diff-Review deckte alle sieben gestagten Dateien ab und fand keinen
berichtsfähigen Security-Kandidaten; sein deterministischer Bericht ist bei der
Task-Evidence abgelegt. Dieser Review ersetzt weder die ausstehenden
Exact-Head-Hosted-Checks noch die separat blockierte Path-Policy-Baseline.

## Runtime-Evidence

Es änderte sich kein Connector-Runtime-Verhalten und keines wird beansprucht.
Die fokussierten Parent-Tests nutzen Temporary-Fixtures und Resolver-
Subprozesse; sie sind weder Host-Deployment noch Framework-Run, MRTS-Run oder
vollständige Connector-/Runtime-Matrix.

## Bekannte Einschränkungen

Dieser Batch behandelt nur neun Parent-Testdiagnostik-Befunde. Er beseitigt
weder den breiteren SonarQube-Cloud-Backlog noch Framework- oder MRTS-Befunde
und beweist kein Connector-Runtime-Verhalten über fokussierte Unit-Tests hinaus.
Der zehnte geprüfte Key bleibt als FND-SONAR-0031 offen, bis eine autorisierte
saubere Baseline verfügbar ist.

## Verbleibende Risiken

Ein Tausch außerhalb des Umfangs könnte eine Fehlermeldung irreführend machen
oder die Evaluierungsreihenfolge ändern. Live-Key-/Source-Inventar,
Purity-Review, Neun-Aufrufe-AST-Inventar, Drei-Dateien-Diff-Review und das
vollständige fokussierte Subset reduzieren dieses Risiko. Hosted-Sonar-Analyse
und CI benötigen noch Evidence für den exakten Draft-PR-Head.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein vollständiger tests.test_runtime_path_policy Pass: Seine unveränderte
  Baseline ist wegen fehlendem Framework common.sh blocked_environment; keine
  Framework-/MRTS-Aktion ist autorisiert.
- Kein voller Connector-Build oder Host-/Runtime-Matrix: Nur Testdiagnostik
  ändert sich.
- Kein Framework- oder MRTS-Test und keine Änderung: Beide liegen außerhalb
  dieses Parent-Tasks.
- Keine exakte-PR-Head-GitHub-Actions-, CodeQL-, Sonar-Quality-Gate-, PR-Issue-
  Query- oder Review-Thread-Prüfung existiert vor dem Draft PR.

## Finaler Diff- und Review-Status

Die lokale Source-, fokussierte Test- und Bilingual-Paar-Validierung ist
abgeschlossen. Die Repository-Bilingual- und Link-Befehle bleiben nur durch die
erfassten fehlenden Framework-Gitlink-Ziele blockiert; kein Produkt- oder
Grenz-Workaround wurde verwendet. Danach dürfen normaler Push und ein
ungemergter Draft PR erfolgen. Es werden weder Merge, Default-Branch-Update,
Framework-/MRTS-Änderung, Suppression noch Alert-Closure beansprucht oder
autorisiert.
