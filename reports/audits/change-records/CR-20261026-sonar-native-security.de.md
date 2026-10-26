# Change Record: CR-20261026-sonar-native-security

**Sprache:** [English](CR-20261026-sonar-native-security.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261026-sonar-native-security |
| Datum (UTC) | 2026-10-26 |
| Basis-Revision | `542a98bc20a16f885f114375bfa5225a9364dcf2` |

## Motivation und Problemstellung

Der breite CFamily-AutoConfig-Scan kann keine C/C++-Taintanalyse durchführen. Der Nutzer verlangt eine vollständige Sicherheitsprüfung über die gepflegten Sprachen, einschließlich echter C/C++-Buildkontexte, bei Erhalt der maßgeblichen Master-Pipeline. Coverage ist ausdrücklich für Security- und Merge-Entscheidung irrelevant.

## Akzeptanzkriterien

Breite Parent-Analyse und ihre Root-Modules-/Reports-Ausschlüsse erhalten. Jedes der zwölf unabhängigen nativen Ziele mit echten Compilerargumenten, exakter Quell-/Header-Mitgliedschaft und sauberer analysierter Revision erfassen; SDK-Identität und Credentials begrenzen. Abschluss verlangt tatsächliche Hosted-Taint-/CTU-, Parse-/Index- und abschließende Server-/Gate-Nachweise sowie quellbasierte Finding-Behandlung. Core-Obergrenze 100, Connector-E2E 26, geschlossene historische I12-Kampagnen, unveränderten Parent-Gitlink und read-only MRTS erhalten. Diese Abschlusskriterien sind noch nicht vollständig erfüllt.

## Implementierungsentscheidung und Begründung

Separaten nativen Workflow mit zwölf Projekten ergänzen, statt den breiten Scan durch eine unvollständige oder kombinierte Datenbank zu ersetzen. Kanonisches gemeinsames ModSecurity-SDK 3.0.17 sowie Artefakt-ID-/Producer-Root-Outputs desselben Laufs verwenden. Revision, Quell-/Build-Provenienz und Archiv-/Bibliotheksdigests prüfen; ausbrechende Archiveinträge/Links und unsichere externe Output-Abstammung ablehnen. Erfolgreiche echte Compileraufrufe erfassen, Äquivalenz ursprünglicher Quellen/Includes vor Ausführung bewahren und einen deklarierten Linkgraphen je Ziel validieren. Taint und CTU mit Dateisystemcache, Ressourcen-Vorprüfung und Gate-Warten anfordern. Der reine Coverage-Ausschluss folgt der ausdrücklichen Nutzerentscheidung; keine Security-Regel, kein Profil und kein Gate wird gelockert.

## Geänderte Dateien

- `.github/workflows/sonar-native-security.yml`; `ci/checks/analysis/prepare-sonar-native-ci.py`; die sieben Werkzeuge unter `ci/checks/analysis/sonar-native-security/`.
- Fünf fokussierte Testmodule: `tests/test_sonar_native_security.py`, `tests/test_sonar_native_security_capture.py`, `tests/test_sonar_native_security_go.py`, `tests/test_sonar_native_security_mapping.py`, `tests/test_sonar_native_ci.py`; bestehendes `tests/test_ci_security_workflows.py`.
- Exakte Updater-Allowlist-/Staging-Einträge in `ci/tools/update-workflow-tools.py` und `.github/workflows/update-workflow-tools.yml`; koordinatoreigenes Inventar und generiertes Archiv über ihre Verträge aktualisiert.
- `docs/sonarqube-native-security.md` / `.de.md`, enge Korrekturen der aktuellen Modi in `docs/sonarqube-analysis.md` / `.de.md` und dieses Record-Paar. Der finale Koordinator-Diff bestimmt den vollständig ausgelieferten Quellsatz.

## Ausgeführte Befehle

Der Dokumentationsagent erzeugte dieses Paar über `rtk bypass` und `ci/tools/new-change-record.py create --name sonar-native-security --base-revision 542a98bc20a16f885f114375bfa5225a9364dcf2 --date 2026-10-26`. Quellen-/Workflow- und aufbewahrte JSON-Lesezugriffe verwendeten RTK. Native Dokumentationsprüfungen bestanden: `rtk make check-bilingual-docs` und `rtk make check-doc-links` mit explizitem Parent-Interpreter `PYTHON=/var/tmp/codex/ModSecurity-conector/runs/pr382-integrate410-20261024/python315/venv/bin/python`; die Linkprüfung verwendete zusätzlich `FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework`. RTK-gekapseltes `ci/tools/new-change-record.py check` bestand (nur Struktur), ebenso abgegrenztes `git diff --check`.

Beobachtete Koordinator-Zusammenfassung: 34 Ausführungen / 98 expandierte Fälle bestanden ohne Skips bei Inventar `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578`; die Zusammenfassung wurde aus dem aufbewahrten externen Lauf gelesen. Dieser Zwischenstand enthält Native12-Integration, liegt aber vor Ubuntu-Migration und späteren Helper-Änderungen; er validiert den aktuellen uncommitteten Baum nicht. Zwölf Entwicklungsbuilds/-exporte umfassen insgesamt 611 Parent-TU-Kompilierungen, keine eindeutigen Dateien. Der kanonische Artefaktvergleich des C++17-Evaluators bestand ohne Ausführung des Evaluators; SHA-256 `6846b788f1eb1f56e0514ed8e49130d2c045e09e852726683bb2beb4f87e24a4`. Exakte Build-/Testverfahren und Receipts verbleiben beim Koordinator; kein rekonstruierter Befehl wird als ausgeführt ausgegeben.

Die integrierte Auswahl nach Master-Übernahme bestand **94 Ausführungen / 342 expandierte Fälle ohne Skips**, beim Inventar `e13c73b981fd1399fbe0c161a8abd753d6cbc4d429957caa86d7c33e1f59bf7c`. Das Inventar deklariert 1992 Fälle / 918 Ausführungen: 97 Kernfälle / 77 Ausführungen plus 1895 autorisierte Offline-Fälle / 841 Ausführungen, mit 614 Quellbindungen und 1.672.802 Bytes. Die Auswahl enthält acht Inventarkontrollen einschließlich Überlauf-Abweisung und sieben Broker-Selektoren / 36 Fälle sowie korrigierte Helper-Capture-Pfad- und isolierte NGINX-Archivvertragskontrollen. Das frühere PASS 79/298 bei `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be` ist ein Vor-Merge-Zwischenstand. Lokale grüne Ergebnisse belegen keine Hosted-Native12-Analyse.

Der benutzerfreigegebene Broker-[PR #422](https://github.com/Easton97-Jens/ModSecurity-conector/pull/422) wurde regulär vom erwarteten Head `3d633ee27b48b64b940042e278c157f1aa629679` nach Master-Revision `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` gesquasht; Provider-Readback bestätigte den Merge. Unabhängiges finales Review aller sieben Dateien fand keinen konkreten Befund. Alle sechs PR-Ruleset-Prüfungen und terminalen C++17/20/23-Sonar-Ergebnisse bestanden an genau diesem PR-Head. Der Parent-Aufrufer pinnt jetzt Broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` und dessen tatsächliches Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; der Parent-Gitlink bleibt unverändert. Geschützte Self-hosted-Labels und Masters einheitlicher Runner-Validator bleiben erhalten; die doppelte Coverage-Ausschlussproperty wurde auf eine Deklaration reduziert. Kein geschützter manueller Broker-Lauf oder erweiterter Connector-E2E wurde gestartet. Die Autorisierung umfasste nur #422 und den anschließenden Aufrufer-Pin, keinen #382-Merge.

Alle sechs Master-Ruleset-Prüfungen bestanden bei `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`. Masters C++17-Sonar scheiterte tatsächlich mit Security E / Reliability E gegen eine `previous_version`-Baseline vom 14. Mai; die schreibgeschützte Prüfung fand 20 bereits bestehende Security-/Reliability-Befunde, keinen durch #422 eingeführten; fünf native Auslöser sind in #382 bereits entfernt. Kein bestandenes Master-Sonar-Gate wird behauptet. Diese Master-Ergebnisse bleiben von der erfolgreichen Analyse des exakten PR-Heads getrennt. Der PR-Liefernachweis muss den exakten Parent-Native12-/Ubuntu-Commit und frische CI binden, ohne ältere Erfolge zu übertragen.

Der getrennte [Framework-Draft-PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) ist jetzt bei `5bffa21d3dd49d3ca647e89eebe005b8421b0812` veröffentlicht und behält 31 Ubuntu-26.04-Runner-Felder. Der Koordinator bestand 86 lokale Methoden ohne Skips; beim letzten Readback waren zehn von zwölf CI-Workflows erfolgreich, Sonar-SDK- und Scaffold-Prüfungen standen aus. Die frühere Analyse von `5ef4dc3c815c97121578cd34382b80088b9c61ec` führte C-/Python-Taint tatsächlich aus und ihr Gate wurde nach quellbasiertem False-positive-Readback `OK`; das Ergebnis ist für den neuen Head veraltet. Kein aktuelles finales Framework-Gate oder Parent-Gitlink-Import wird behauptet.

## Security-Auswirkung

Der Source-/Credential-Vertrag lehnt geänderten Checkout, quellersetzende Schritte, ungeprüfte Umgebungen, alternative Scanner-/Projekt-/SCM-Einstellungen und Token-Wiederverwendung ab. SDK-Wiederherstellung ist auf den geprüften Prefix desselben Laufs begrenzt. Parent-Header müssen tatsächliche Compilerabhängigkeiten und keine reinen Scope-Aliase sein. Go-Producerübergänge und die enge Apache-Internal-LTO-Grenze bewahren ausdrückliche Nachweisgrenzen. Negativkontrollen prüfen reale Zulassungspfade; diese Konfiguration beweist keine Schwachstellenfreiheit der Anwendung.

## Runtime-Evidence

Für diese Erfassungen wurde keine Anwendung, kein Evaluator und keine Connector-Host-, Lifecycle-, Matrix- oder Oracle-Kampagne ausgeführt. Entwicklungskompilierung/-export und C++-Artefaktgleichheit belegen nur ihre eigenen Buildschichten. Sie erzeugen weder I12_COMPLETE noch Host-Qualifikation.

## Bekannte Einschränkungen

Alle zwölf aufbewahrten Entwicklungserfassungen verwenden Produktrevision `542a98bc20a16f885f114375bfa5225a9364dcf2` mit Entwicklungsständen der Hilfswerkzeuge und `import_eligible=false`. Apache verwendet installierten APXS-/APR-Kontext und bewahrt interne temporäre GCC-LTO-/Debug-Bytes nicht auf. Externe SDK-/Upstream-Implementierung, Go/C-sprachübergreifendes Taint, nicht konsumierte reine C++-Header-Wrapper und drei I12-Instrumentierungsquellen in C++ liegen außerhalb des neuen nativen Taint-Nachweises; gepflegte Parent-Dateien bleiben im breiten Quellscope. Erste native Projektanalysen können echte Default-Branch-Baselines und autorisierte Tokens benötigen. Vollständige Grenzen und abgeleitete Erfassungszahlen stehen im gepaarten nativen Leitfaden.

## Verbleibende Risiken

Hosted-Compiler-/Parser-Kompatibilität, beibehaltener CTU-Kontext, tatsächliche Parent-Indexierung, Taint-Aktivierung und Live-Findings sind unbestätigt. Ein erfolgreicher Upload oder älteres breites Gate schließt diese Lücken nicht. Keine erfundene Baseline, kein Source-Mapping, keine Whole-Program-Behauptung und kein behauptetes PASS darf fehlende Evidence ersetzen.

## Nicht ausgeführte Prüfungen mit Begründung

Der Dokumentationsagent führte keine funktionalen Tests, Builds, Scanner, Provider-Mutationen, Git-Schreibzugriffe oder Runtime-Kampagnen aus. Die aktuelle zugelassene Offline-Auswahl bestand; saubere Published-Head-Hosted-/Serverergebnisse bleiben koordinatoreigen und ausstehend. Historische I12-Kampagnen bleiben bewusst geschlossen. Framework-CLI-/Updater-Arbeit gehört zum separaten Framework-PR #138; Parent-Gitlink und MRTS bleiben unverändert.

## Finaler Diff- und Review-Status

Vorbereitete Dokumentation und native Implementierung befinden sich weiterhin in Koordinator-Integration und Review. Kein nativer Hosted-Abschluss, Ready-for-review oder verified_pr wird behauptet. Kein Parent-PR-#382-Merge, Release oder Deployment ist autorisiert.
