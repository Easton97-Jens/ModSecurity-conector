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

Die zugelassene integrierte Auswahl bestand **79 Ausführungen / 298 expandierte Fälle ohne Skips**, beim Inventar `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be`. Dieses deklariert 1956 Fälle / 911 Ausführungen: 97 Kernfälle / 77 Ausführungen plus 1859 autorisierte Offline-Fälle / 834 Ausführungen, mit 613 Quellbindungen und 1.654.103 Bytes. Die aufbewahrte Zusammenfassung ist `targeted-offline/active-tests-v3oeoia0/summary.json` im externen Lauf `parent-ubuntu26-20261026`. Enthalten sind der korrigierte NGINX-Test zum veralteten archivierten Vertrag unter Erhalt der Isolation und 97 statische Lighttpd-Grenzvarianten. Die Prüfung reproduzierte einen echten Helper-Fehler: Der Validator lehnte dessen nicht unterstütztes Capture-Schema ab; nach Korrektur des Capture-Pfads bestand die zugelassene Ein-Fall-Regression. Unabhängige Prüfung fand keinen weiteren konkreten Befund. Das erste Teilergebnis 78/297 und der frühere Native12-Zwischenstand 34/98 bei `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578` bleiben historisch und sind keine aktuellen Fehler. Statische AST-Prüfungen für 14 Dateien, Zweisprachigkeits-/Pfadprüfungen und natives actionlint bestanden; zizmor meldete keine Findings. Das sind lokale Nachweise, keine Hosted-Native12-Analyse.

Die Ubuntu-Migration steht im [Change Record](CR-20261026-ubuntu26-workflow-migration.de.md). Parent-Hosted-Deklarationen wählen 26.04; geschütztes Self-hosted-Routing bleibt explizit. Der eingesetzte unveränderliche NGINX-Broker-Pin `49c40779a7b6de9f699391bcd524ea069787df42` lehnt den migrierten Aufrufer weiterhin ab. Der getrennte [Draft-PR #422](https://github.com/Easton97-Jens/ModSecurity-conector/pull/422) ist jetzt bei `3d633ee27b48b64b940042e278c157f1aa629679` veröffentlicht. Sein vorheriger Head `89e3342c112ad9c23821413243dd7586432528c6` bestand sieben zugelassene Methoden / 36 expandierte Fälle / 33 Subtests ohne Skips oder Gitleaks-Findings; das Sonar-Gate scheiterte ausschließlich an null Coverage, bei null Issues und fünf bestandenen Nicht-Coverage-Bedingungen. Der Folgestand wendet die geltende Coverage-Abwahl `sonar.coverage.exclusions=**` an, ohne weitere Gate-Änderungen; CI am neuen Head steht aus. Der Benutzer genehmigte ausdrücklich ausschließlich die Integration von #422 nach grünen Prüfungen und finalem Review, danach den geprüften unveränderlichen Pin in #382. Kein Merge ist erfolgt; diese Bedingungen bleiben verbindlich.

[Framework-Draft-PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) ist getrennt bei `5ef4dc3c815c97121578cd34382b80088b9c61ec` veröffentlicht, mit 31 Ubuntu-26.04-Runner-Feldern. Tatsächlicher SDK-/Native-Build, Scanner-/JRE-Authentifizierung und Analyse waren erfolgreich: Eine C-TU mit acht Taint-Regeln sowie Python mit 32 Taint-Regeln wurden analysiert. CE-Task `AaF5sxOo8Px5fiPcdsNi` und Analyse `eb2599ca-c449-4e33-8cb3-e643eb0b593d` endeten mit `SUCCESS`. Das Gate ist ausschließlich wegen Security-Rating 3 `ERROR`; vier CLI-Flow-Behauptungen werden triagiert, Qualitätskorrekturen sind getrennte Arbeit. Elf andere CI-Workflows bestanden. Das ist echter Framework-Analyzer-Nachweis, kein bestandenes Security-Gate oder importierter Parent-Gitlink-Nachweis.

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
