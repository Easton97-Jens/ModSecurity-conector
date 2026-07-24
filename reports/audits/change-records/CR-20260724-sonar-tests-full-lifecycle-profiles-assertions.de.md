# Change Record: Parent-Full-Lifecycle-Profil-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260724-sonar-tests-full-lifecycle-profiles-assertions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260724-sonar-tests-full-lifecycle-profiles-assertions |
| Datum (UTC) | 2026-07-24 |
| Basis-Revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Sieben aktive Parent-SonarQube-Cloud-`python:S3415`-Code-Smells: AZ-KYVRvfYmbqbBXVNFH, AZ-KYVRvfYmbqbBXVNFI, AZ-KYVRvfYmbqbBXVNFJ, AZ-KYVRvfYmbqbBXVNFK, AZ-KYVRvfYmbqbBXVNFL, AZ-KYVRvfYmbqbBXVNFM und AZ-KYVRvfYmbqbBXVNFN. |
| Grenze | Parent-Testquellcode sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Der Lifecycle-Profile-Helper, Connector-Verhalten, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und generierte Artefakte bleiben unverändert. |

## Motivation und Problemstellung

Die ausgewählten SonarQube-Cloud-Zeilen melden, dass sieben bestehende `unittest`-Assertions im Parent-Full-Lifecycle-Profil-Test ihren erwarteten Wert vor dem beobachteten Ergebnis platzieren. Die Assertions prüfen bereits die beabsichtigten Profil- und Capability-Invarianten; allein das Umkehren ihrer ersten zwei Operanden verbessert die Fehlerdiagnostik, ohne akzeptiertes oder abgewiesenes Verhalten zu verändern.

## Akzeptanzkriterien

- Nur die sieben ausgewählten SonarQube-Cloud-Assertions auf tatsächlichen Wert zuerst und erwarteten Wert danach korrigieren.
- Jedes Manifest-Fixture, jede Profilzuordnung, jeden Capability-Status, jede Nachricht, jeden temporären JSON-Write und jede Produktionsquelldatei bewahren.
- Das vollständige fokussierte Parent-Unit-Modul, die Selected-File-Syntaxprüfung, die Sieben-Aufruf-AST-Inventur und die Diff-Hygiene bestehen.
- Vollständige synchronisierte englisch/deutsche Change Records und Indizes pflegen.
- Exact-Head-GitHub- und SonarQube-Cloud-Draft-PR-Evidenz einholen, bevor die ausgewählten Keys als verifiziert beschrieben werden.

## Implementierungsentscheidung und Begründung

Jeder ausgewählte `assertEqual`- oder `assertNotEqual`-Aufruf übergibt jetzt seinen bestehenden beobachteten Ausdruck zuerst und sein unverändertes erwartetes Literal oder seine unveränderte Collection danach. Es wurden kein Helper, Fixture, erwarteter Wert, Assertion-Nachricht, Profil, Capability-Status oder Runtime-Bedingung geändert. Dies ist die kleinste repository-native Korrektur für `python:S3415` und bewahrt die `unittest`-Prädikatsemantik.

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet `not_applicable`: Dies ist allein diagnostische Argument-Reihenfolge in Parent-Testcode. Der read-only angrenzende Lifecycle-Helper besitzt zwar atomisches File-Writing-Verhalten, bleibt aber unverändert. Das direkte Modul nutzt In-Memory-Manifeste und einen task-local temporären JSON-Output; es ruft weder Framework, MRTS, eine Connector-Runtime, einen Netzwerk-Client, einen Subprozess noch eine Dependency-Operation auf. Es wird kein Sicherheitsbefund als behoben behauptet.

## Geänderte Dateien

- tests/test_full_lifecycle_profiles.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Die fokussierten Kommandos nutzten Parent-.venv-Python, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1` und ein task-owned externes `TMPDIR`; die Selected-File-Syntax leitete `PYTHONPYCACHEPREFIX` außerhalb des Checkouts um:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_full_lifecycle_profiles
- rtk proxy -- env ... <Parent .venv python> -m py_compile tests/test_full_lifecycle_profiles.py
- rtk proxy -- env ... <Parent .venv python> -c <AST-Inventur der sieben ausgewählten Assertions>
- rtk proxy -- git diff --check

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussiertes Full-Lifecycle-Profile-Unit-Modul vor und nach der Änderung | bestanden: tests.test_full_lifecycle_profiles, jeweils 5 Tests. |
| Selected-File-Python-Syntax | bestanden: tests/test_full_lifecycle_profiles.py wurde mit Pycache außerhalb des Checkouts kompiliert. |
| AST-Inventur der ausgewählten Assertions | bestanden: Genau sieben ausgewählte Anker (60, 68, 85, 98, 103, 117 und 129) haben jetzt Actual-First-Operanden und unveränderte Expected-Werte. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| Bytecode-Scan des aktuellen Batch-Worktrees | bestanden: keine `*.pyc`-Datei. |
| tests.test_bilingual_docs | bestanden: 11 Tests. |
| Direkter Change-Record-Paar-Review | bestanden: Beide Dateien haben 13 Level-two-Abschnitte sowie passende ID-, Basis-Revision-, Issue-Key- und Affected-Path-Literale. |
| make check-bilingual-docs | blocked_environment: Genau 20 vorhandene fehlende Framework-Gitlink-Linkziele; die Ausgabe enthält keinen neuen Change-Record-Fehler. |
| make check-doc-links | blocked_environment: Genau 16 vorhandene fehlende Framework-Gitlink-Linkziele; es wurde kein Framework-Quellcode, Gitlink oder generiertes Artefakt geändert. |
| Hosted-Delivery-Checks | ausstehend: Draft PR [#113](https://github.com/Easton97-Jens/ModSecurity-conector/pull/113) wurde offen und `isDraft: true` vom initialen Remote-Head `8a97eb963bd16ff4c7fbc187bbe3f8396c036736` erstellt. Dieses Delivery-Observation-Update erzeugt einen neuen finalen Head; Checks, Quality Gate, PR-Issues und Review-Status müssen danach frisch beobachtet werden und werden nicht vorab behauptet. |

## Runtime-Evidence

Es wurde kein Connector-Runtime-Verhalten geändert oder behauptet. Das fokussierte Modul testet nur Parent-Lifecycle-Profile-Transformationen und einen task-local atomischen JSON-Write; es ist weder Host-Traffic- noch Produktions-Runtime-Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Builds, Konfigurationsprüfungen, Host-Runtime-Smoke-Tests, Protokollmatrizen, Framework-Checks und MRTS-Checks sind nicht anwendbar, weil keine Connector-/Runtime-Implementierung geändert wurde und Framework/MRTS ausgeschlossen sind.
- Ruff und Pyright sind nicht anwendbar: Es gibt keine Parent-Konfiguration und keines der beiden Executables existiert in der ausgewählten Parent `.venv`; es wurde kein Tool installiert und keine Konfiguration nur für diese Diagnostik-Reihenfolgenänderung verändert.
- Draft PR #113 existiert, aber sein finaler Dokument-Update-Head benötigt vor
  `verified_pr` eine frische Beobachtung von GitHub-Checks,
  SonarQube-Cloud-Quality-Gate, PR-Issues und Review-Status; kein Ergebnis
  eines vorherigen Heads wird als final behandelt.

## Bekannte Einschränkungen

Dieser Batch korrigiert nur sieben ausgewählte Parent-SonarQube-Cloud-Befunde. Er behauptet nicht, den breiteren SonarQube-Cloud-Backlog mit 1.474 Befunden zu beheben.

## Verbleibende Risiken

Eine unbeabsichtigte Änderung eines Assertion-Werts könnte einen Profil- oder Capability-Control abschwächen. Der enge Diff, die exakte Sieben-Aufruf-AST-Inventur, das vollständige fokussierte Modul und die noch ausstehende Exact-Head-Hosted-Validierung reduzieren dieses Risiko. Aus dieser reinen Test-Diagnostikänderung wird kein Runtime- oder Security-Verhalten abgeleitet.

## Finaler Diff- und Review-Status

Die Source-Korrektur und das anfängliche englisch/deutsche Traceability-Material
liegen im atomaren Commit `65c40bc`, gefolgt vom Traceability-Commit der
beobachteten lokalen Delivery `8a97eb9`, auf
`codex/sonar-tests-full-lifecycle-profiles-assertions-20260724-master-5b8db00`,
dessen initialer Parent `5b8db00d44ab24f3a9f4216a00f7edee977b6898` ist. Der
Branch wurde normal gepusht und als Draft PR #113 auf initial beobachtetem Head
`8a97eb963bd16ff4c7fbc187bbe3f8396c036736` eröffnet; er ist offen und
ungemergt. Dieser Dokument-Update-Commit erfordert bewusst einen frischen
Exact-Head-Hosted-Verifikationszyklus. Es gab keinen Merge, kein
Default-Branch-Update, keine Framework-Action, keine MRTS-Action, keine
Scanner-Control-Änderung und keine Suppression. Finale Delivery-Fakten werden
erst nach ihrer Beobachtung ergänzt.
