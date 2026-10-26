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

Die automatische Auswahl umfasst jetzt 100 expandierte Fälle / 80 Ausführungen einschließlich dreier Schutzkontrollen. Weitere 1893 Fälle / 839 Ausführungen sind ausschließlich ausdrücklich auf Abruf verfügbar. Automatische Coverage-Katalogbefehle wurden entfernt; der erhaltene Collector verlangt `--on-demand`. Coverage ist laut Benutzeranweisung für den Merge irrelevant. Breite Quell-/Scanner-/Gate-Analyse bleibt aktiv; nur root `modules/**` und root `reports/**` sind ausgeschlossen.

Framework-Revision `03da9353561bf632a1f7bfc71b0a2671ec7aa257` bestand alle zwölf CI-Workflows und Sonar und ist Ready; kein Framework-Merge wurde durchgeführt. Parent behält Framework-Gitlink `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS bleibt unverändert. Broker-PR #422 ist bereits benutzerautorisiert bei `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` integriert; kein weiterer Master-Merge ist autorisiert. Geschützter manueller Lauf, Connector-E2E-Erweiterung und historische I12-Kampagnen wurden nicht ausgeführt.

## Security-Auswirkung

Der Source-/Credential-Vertrag lehnt geänderten Checkout, quellersetzende Schritte, ungeprüfte Umgebungen, alternative Scanner-/Projekt-/SCM-Einstellungen und Token-Wiederverwendung ab. SDK-Wiederherstellung ist auf den geprüften Prefix desselben Laufs begrenzt. Parent-Header müssen tatsächliche Compilerabhängigkeiten und keine reinen Scope-Aliase sein. Go-Producerübergänge und die enge Apache-Internal-LTO-Grenze bewahren ausdrückliche Nachweisgrenzen. Negativkontrollen prüfen reale Zulassungspfade; diese Konfiguration beweist keine Schwachstellenfreiheit der Anwendung.

## Runtime-Evidence

Am veröffentlichten Parent `011cb197` schloss [Lauf 40392396874](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40392396874) SDK-Vorbereitung und alle zwölf nativen Build-/Capture-/Index-/CTU-/Taint-Analysen ab: insgesamt 611 Compilation Units, keine partiellen Units und 100 % Indexierung je Ziel. Vor Einzeltriage bestanden drei native Gates, neun scheiterten. Zwanzig von 22 Workflows bestanden; die breiten C++17/20/23-Gates scheiterten. Die Quellprüfung bestätigte zwölf Python-Security-Issues und 39 native Issue-Instanzen als False Positives; alle 36 Main-/Advisory-Python-Instanzen und 39 nativen Instanzen sind einzeln als False Positive aufgelöst und frisch zurückgelesen. Ursprüngliche Job-Ergebnisse bleiben unverändert. Diese Analyse liegt vor dem endlichen Abschlusscommit und ist keine Abnahme des finalen Heads. Siehe [zentralen Status](../../../docs/pr-382-merge-readiness.de.md).

Für diese Erfassungen wurde keine Anwendung, kein Evaluator und keine Connector-Host-, Lifecycle-, Matrix- oder Oracle-Kampagne ausgeführt. Entwicklungskompilierung/-export und C++-Artefaktgleichheit belegen nur ihre eigenen Buildschichten. Sie erzeugen weder I12_COMPLETE noch Host-Qualifikation.

## Bekannte Einschränkungen

Die historischen Entwicklungserfassungen verwenden Produktrevision `542a98bc20a16f885f114375bfa5225a9364dcf2` mit Entwicklungsständen der Hilfswerkzeuge und `import_eligible=false`. Apache verwendet installierten APXS-/APR-Kontext und bewahrt interne temporäre GCC-LTO-/Debug-Bytes nicht auf. Externe SDK-/Upstream-Implementierung, Go/C-sprachübergreifendes Taint, nicht konsumierte reine C++-Header-Wrapper und drei I12-Instrumentierungsquellen in C++ liegen außerhalb des neuen nativen Taint-Nachweises; gepflegte Parent-Dateien bleiben im breiten Quellscope. Vollständige Grenzen und abgeleitete Erfassungszahlen stehen im gepaarten nativen Leitfaden.

## Verbleibende Risiken

Die beobachtete Zwölf-Ziele-Analyse ist bei `011cb197` vollständig; alle einzeln quellgeprüften Python-/nativen Dispositionen sind bestätigend zurückgelesen; alte Job-Ergebnisse bleiben unverändert. Aus dem Build-/Analyzer-Nachweis folgt kein finales Head-Gate-PASS oder Anspruch auf Schwachstellenfreiheit. Zentrale Readiness bindet die exakte finale Lieferung.

## Nicht ausgeführte Prüfungen mit Begründung

Diese Dokumentationsänderung führte keine funktionalen Tests, Builds, Scanner oder Provider-/Git-Mutationen aus. Hosted-Analyse wurde an der veröffentlichten Revision beobachtet; finale Head-Abnahme und Dispositions-Readback bleiben im [zentralen Status](../../../docs/pr-382-merge-readiness.de.md). Historische I12-Kampagnen bleiben geschlossen.

## Finaler Diff- und Review-Status

Veröffentlichter Parent `011cb197` besitzt beobachtete Zwölf-Ziele-Analyse, keine Abnahme des finalen Heads. Quellgeprüfte False-positive-Dispositionen sind einzeln frisch zurückgelesen; finale Checks am veröffentlichten Head bleiben Lieferkriterium. Kein Parent-#382-Merge, Release oder Deployment ist autorisiert.
