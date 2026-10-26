# Change Record: CR-20261026-pr382-master421-merge

**Sprache:** [English](CR-20261026-pr382-master421-merge.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261026-pr382-master421-merge |
| Datum (UTC) | 2026-10-26 |
| Basis-Revision | `209ab41a16cc34c88e3dc23d312eada0a38a8169` |

## Motivation und Problemstellung

Der wiederaufgenommene Nutzerauftrag verlangt zuerst den Merge des neuen Masterstands `7a44f18edac729291d6551d068da64fa3fec4e1e` (PR #421). PR #382 muss der neuen Master-Sonar-Implementierung folgen und dabei eigenständige Parent-Arbeit sowie die vorherige Entfernung eigener Sonar-Komponenten erhalten.

## Akzeptanzkriterien

Vollständigen Parent-Scope und verpflichtendes C++17-Gate mit C++20/23-Advisory-Scans erhalten. Aktuelle Toolchain und unverändertes Parent-Inventar mit 932 Fällen / 536 Ausführungen erhalten: 89 Kernfälle / 69 Ausführungen plus 843 Offline-Fälle / 467 Ausführungen; Connector-E2E bleibt 26. Quellgebundene PR-#421-Ergebnisse von neuen Merge-Head-Aussagen trennen. Gesicherte WIP nicht wiederherstellen und I12-Kampagnen nicht neu eröffnen. Erforderliche Prüfungen am aktuellen Head bleiben Abschlusskriterien des Integrationskoordinators.

## Implementierungsentscheidung und Begründung

Regulären Merge von obiger Basis verwenden; neue Master-Scope-Sicherung, echte Python-/Go-/Common-Native-Coverage und gepinnte Native-Kontextvorbereitung erhalten. Python `3.15.1`, Go `1.27.3`, Modul-Sprachversion `1.26.9`, setup-python `7.1.0` und Master-Scanner `8.2.0.6438` beibehalten. Master dokumentiert 80 Python-Methoden und 37 Go-Szenarien; Methoden sind keine expandierten Fälle. Die feste `PYTHON_TESTS`-Auswahl mit 13 Einträgen erhält ausschließlich im Kind explizit `ON_DEMAND_TESTS=1`; geschützte Standard-Discovery bleibt erhalten. Matrixwiederholungen erhöhen Ausführungskosten. Alter PR-Collector, Quellrollen-Pipeline und eigene Null-/Duplikations-Gates bleiben entfernt.

## Geänderte Dateien

- `.github/workflows/sonarqube.yml`, `sonar-project.properties`, Master-Analyse-/Coverage-/Native-Kontexthelper und Tests, Evidence-Input-/Report- und ausgewählte Shell-Korrekturen aus PR #421.
- Parent-Integrationsverträge, Test-Discovery-Zuständigkeit, Inventar-Quellbindungen und generiertes Archiv; diese gehören dem Integrationskoordinator.
- `docs/pr-382-merge-readiness.md` / `.de.md`, `docs/sonarqube-analysis.md` / `.de.md`, `ci/README.md` / `.de.md`, `tests/README.md` / `.de.md`, `docs/testing-and-evidence.md` / `.de.md` und dieses Change-Record-Paar.
- Übernommene `docs/sonarqube-pr421-closeout.md` / `.de.md`, `docs/sonarqube-pr421-triage.md` / `.de.md` und der ursprüngliche PR-#421-Change-Record behalten ihre historischen Quellidentitäten.

## Ausgeführte Befehle

Während des Abgleichs ausgeführt: RTK-gewrapptes `git diff --stat 9f44647593bac7947113558c6ad183ab118e80af 7a44f18e`, unveränderliche `git show`-Lesezugriffe auf Master-Workflow/Helper und EN/DE-Analyse/Abschluss/Triage; Repository-Quell-/Dokumentlesezugriffe und begrenzte statische Suchen. Die neue Record-Struktur folgt dem versionierten kanonischen Überschriften-/Identitätsschema. Der Dokumentationsworker führte keine Projektimporte, Tests, Hostprozesse oder Provider-Schreibzugriffe aus. Das begrenzte `rtk bypass git diff --check` bestand. Ein ausschließlich mit der Standardbibliothek ausgeführter statischer Vergleich bestätigte gleiche Überschriftenebenen in allen sechs bearbeiteten EN/DE-Paaren (13 Überschriften in diesem Record); dies ist nicht die Repository-Bilingual-/Linkprüfung. Finale Dokumentations-, Inventar- und Merge-Head-Prüfergebnisse werden hier nicht behauptet; der Koordinator erfasst beobachtete Ergebnisse getrennt.

## Security-Auswirkung

Diese Dokumentation ändert keinen Secretwert, keine Scannerschwelle, Regel, New-Code-Baseline oder Gatebedingung. Master-Coverage ist eine getrennte Pflichtprüfung mit Prozessen, Go und nativer Kompilierung; sie ist keine Python-Offline-Ausnahme. Offline-Prozess-/Netzwerkguards bleiben erhalten. Passive Framework-Vertrags-/Headerbeschaffung am exakten Gitlink gewährt keine Framework-/MRTS-Schreibrechte.

## Runtime-Evidence

Es entstehen keine neuen Runtime-Nachweise. PR-#421-Runtime-Evidence gehört zu Source `900dddb49c43ec4479c4b75a91071cadb97893c4` und ausschließlich dessen ausgewähltem Runtime-Scope. I12-Host-/Matrix-/Oracle-Kampagnen bleiben geschlossen, ohne neues `I12_COMPLETE`; Framework-/MRTS-Checkouts/Gitlinks bleiben unverändert.

## Bekannte Einschränkungen

PR-#421-Source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8` maß Gates OK bei 83.5% PR-/84.6% Advisory-New-Code-Coverage, 179 FIXED plus 24 FALSE_POSITIVE-IDs und null OPEN/CONFIRMED-Befunden/Hotspots, mit 136 nativen Einheiten und Parsing-/Include-Qualität 100/100. Diese Beobachtungen qualifizieren PR #382 oder dessen Merge-Revision nicht. Architektur-HTTP-415, CFamily-AutoConfig-Taint-/unabhängige-Ziel-Grenzen, Python-/FIFO-Analyzergrenzen und TLS-Änderungszeilenwarnung bleiben getrennt bestehen. Historische 31.0583536721% der eigenen Pipeline bleiben ausschließlich Vor-Merge-Evidence.

## Verbleibende Risiken

Der reguläre Merge läuft während der Erstellung dieses Records. Finale Quellbindungen, lokale Prüfungen, Veröffentlichung und exakte Head-Serververarbeitung/Gates müssen noch beobachtet werden. Weder alte grüne PR-#421-Gates noch frühere PR-#382-Metriken belegen Merge-Bereitschaft. Die Parent-Kerngrenze von 100 Fällen schließt die getrennte Master-Prüfung aus; keine globale Höchstzahl wird behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Für den Dokumentationsabgleich wurden keine neue vollständige lokale Coverage, native Hostkampagne, I12-Qualifikation oder Serverzustandsoperation gestartet. Der aktuelle Auftrag ist zuerst Masterintegration, keine Wiederaufnahme eigener Coverage- oder 80%-Arbeit. Bilinguale/Link- und finale Integrationsprüfungen bleiben dem Koordinator nach Source-Freeze vorbehalten; kein unbeobachtetes PASS wird behauptet.

## Finaler Diff- und Review-Status

Dieses Paar dokumentiert Integrationsvertrag und Dokumentationsabgleich, keine abschließend verifizierte Auslieferung. Tatsächlicher Merge-SHA, veröffentlichter Head und Providerergebnisse müssen nach Koordinatorreview/Veröffentlichung in der PR-Beschreibung gebunden werden. PR #382 bleibt Draft; kein Ready/verified_pr, Masterintegration von PR #382, Release oder Deployment wird behauptet. Frühere unveröffentlichte WIP bleibt in benanntem Stash/Checkpoint.

## Kompatibilitätskorrektur nach dem ersten Merge

Master wurde regulär als c7c60a83 zusammengeführt und gepusht. Tatsächliche lokale Merge-Prüfungen bestanden:80 Master-Python-Methoden / 118 beobachtete Test-/Subtestfälle,19 Parent-Ausführungen / 21 Fälle, Zulassung/Archiv/Python 50 Jobs/Quellscope/actionlint/zizmor/Sprach-/Links-/Diffprüfung und gestagtesGitleaks (958.987 Byte, keine Leaks). Der erste Sonar-Lauf 40274906525 am aktuellen Head bestand Python-Erfassung und lehnte danach vor Scannerupload den veralteten Go-Testnamen ab. Der Selektor nennt nun die vorhandene PR-Regression; alle 37 Master-Go-Selektoren bestanden lokal mit vier echten Profilberichten. Lokale Dirty-Reports werden nicht als Scannernachweis übernommen.

Zwei neue EvidenceInputs-Regressionen wurden vor Korrektur mit tatsächlichen privaten Datei-Readern/-Writern nachgewiesen. Eine explizite externe Commands-Datei erhält exakte lexikalische Dateifreigabe (keine Symlinkauflösung vor Autorisierung); Diagnosen verwenden ausschließlich den unabhängig konfigurierten Build-Root, durchgereicht durch Producer/CLI. Evidence-Außenpfade und finale/zwischengeschaltete Receipt-Links bleiben abgelehnt. Fünf zugelassene Offline-Ausführungen / sechs Fälle bestanden nach Korrektur; die 80 Master-Methoden bestanden erneut. Parent-Auswahl jetzt 938 Fälle / 541 Ausführungen = 89 Kernfälle / 69 + 849 offline / 472, E2E 26 unverändert. Unabhängiges Read-only-Review fand keinen Blocker. Finaler veröffentlichter Folge-SHA und frische Pflicht-CI/Sonar bleiben erforderlich und werden im PR dokumentiert.
