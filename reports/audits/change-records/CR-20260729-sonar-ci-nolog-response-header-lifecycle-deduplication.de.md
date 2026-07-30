# Change Record: Parent-CI-Nolog- und Response-Header-Report-Lifecycle-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `fda62539b6f0a710865707e3003b73ed4469f20e` |
| Bewertete Source-Revision | Aktueller lokaler Task-Working-Tree-Diff von der Basis-Revision; Draft-PR #188 existiert, aber dieses Record beansprucht keinen aktuellen exakten Head, Hosted Check oder Merge. |
| Grenze | Ausschließlich zwei Parent-`ci/`-Evidence-Report-Generatoren, ihr enger Parent-`ci/lib`-Helper, ein direkter Parent-Test, dieses englisch/deutsche Change-Record-Paar und gepaarte Indizes. Keine `.github/`-, `scripts/`-, Framework-, MRTS-, Gitlink-, Scanner-Konfigurations-, Quality-Gate-, Exclusion-, Suppression- oder Default-Branch-Änderung ist enthalten. |
| SonarQube-Cloud-Verknüpfung | Zielt auf den aktuellen Nolog-/Response-Header-CPD-Cluster: den 13-Zeilen-Connector-Work-Queue-Markdown-Lifecycle, die 39-Zeilen-Phase-Work-Regeneration, den 19-Zeilen-finalen Report-Output-Lifecycle und den gehosteten 23-Zeilen-`main()`-Restblock, der anfänglich zehn neue Duplikatzeilen erzeugte. Keine Scanner-Policy oder Issue-Disposition wird geändert. |

## Motivation und Problemstellung

Das aktuelle Parent-`ci/`-Inventar meldet einen 71-Zeilen-Nolog-/Response-Header-Duplikationscluster. Der doppelte Code erzeugt feste registrierte Reports, passt den Framework-Phase-Work-Callback vorübergehend an und schreibt Report-Paare. Er kann nur reduziert werden, wenn jeder Generator seine eigene Klassifikation, Callback-Logik, Marker-Updates, Safe-Root-Einrichtung, Report-Identität und Metadaten behält.

## Implementierungsentscheidung und Begründung

`ci/lib/focused_analysis_utils.py` besitzt jetzt vier enge Report-Lifecycle-Helper: feste Connector-Work-Queue-Markdown-Regeneration, feste Phase-Work-Regeneration mit Caller-eigenem Direction-Callback, den finalen Write eines generierten Report-Paars und den festen Generator-Einstiegspunkt-Lifecycle. Letzterer verwendet weiterhin die etablierten Controls für registrierte Pfade und den fail-closed Safe Writer.

Die beiden Generatoren behalten ihre jeweilige Klassifikation und `full_run_evidence`-Marker-Updates. Ihre `main()`-Funktionen übergeben nur feste Report-Identität, Metadaten, Builder- und Renderer-Werte an den Einstiegspunkt-Helper. Dieser behält die frühere Reihenfolge von Parser, Root-Auflösung, begrenztem Output, Safe-Root, Report-Root, Verzeichnis, Analyse und Safe Writer. Er verwendet das intern feste `GENERATED_ROOT` und akzeptiert bewusst keinen Caller-übergebenen Report-Root. Der Phase-Helper ersetzt den importierten Framework-Callback nur während des Payload-Builds und stellt ihn in `finally` wieder her, auch bei einem Payload-Fehler. Nolog verwendet für seinen Sonderfall weiterhin das `as_list()`-Verhalten des dynamisch importierten Framework-Moduls; Response-Header behält seine separaten Direction-Regeln.

Der Patch zentralisiert bewusst keine Queue-Klassifikation, akzeptiert keine dynamischen Report-Roots, Namen oder Pfade, ändert keine Framework-Skripte, lockert keine Safe-Root-Controls und ändert keine Scanner-Regel, kein Quality Gate, keine Exclusion, Suppression oder Coverage-Policy.

## Akzeptanzkriterien

- Die ausgewählten festen Report-Lifecycles einschließlich des festen Einstiegspunkt-Lifecycles besitzen parameterisierte Parent-Helper, während beide Generatoren ihre verschiedenen Report-Namen, Metadaten, Callback-Semantik, Klassifikationen und Marker-Updates behalten.
- Tests beweisen feste registrierte Output-Pfade, generierte Metadaten, fail-closed Safe-Root-Verhalten, Phase-Payload-Output, Callback-Wiederherstellung nach Erfolg und Fehler, Nologs Framework-spezifische Listennormalisierung sowie einen abgewiesenen externen Output-Pfad vor Analyse oder Schreiben.
- Der exakte künftige Pull-Request-Head muss null neue SonarQube-Cloud-Issues, null neue Duplikatzeilen und `0.0%` New-Code-Duplikation zeigen, ohne die Scanner-Policy zu ändern.
- Ohne gesonderte ausdrückliche Benutzerautorisierung erfolgt keine Default-Branch-Integration.

## Geänderte Dateien

- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/lib/focused_analysis_utils.py`
- `tests/test_focused_analysis_utils.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-nolog-response-header-lifecycle-deduplication.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| Fokussierte Report-Helper- und Conditional-Remediation-Tests | Bestanden: `29` Tests nach Ergänzung des festen Einstiegspunkt-Lifecycles und der Outside-Output-Controls. |
| Fokussierter Report-Helper-Security-Control-Test | Bestanden: `20` Tests im finalen erweiterten Security-Control-Review. |
| Selected-File-`py_compile` mit task-eigenem Bytecode-Cache | Bestanden. |
| Beide Generator-`--help`-Contracts | Bestanden; die drei bisherigen CLI-Optionen bleiben unverändert. |
| `git diff --check` | Bestanden. |
| Fokussierter finaler Source-Security-Review | Bestanden: Der anfänglich zu generische Report-Root-Parameter wurde entfernt; nur das interne feste `GENERATED_ROOT`, registrierte Pfade, Safe Writer und `finally`-Callback-Wiederherstellung bleiben in Kraft. |
| Fokussierter finaler Test-Security-Review | Bestanden: keine Regression der Test-Grenzcontrols; externer Output wird vor Analyse/Schreiben abgewiesen und hinterlässt kein Artefakt. |
| `make check-bilingual-docs` | Externe Abhängigkeit blockiert: Der Check meldet nur bereits bestehende fehlende Framework-Submodule-Link-Targets, keinen geänderten Change-Record-Fehler; kein Checker und keine Link-Policy wurde geschwächt. |
| Vollständiges `make lint` | Externe Abhängigkeit blockiert, nachdem Shell-Syntax und sämtliche `ci/`-Python-Kompilierung bestanden: `check-no-crs-source-normalization` kann die fehlende Framework-Submodule-Datei `ci/checks/catalog/no_crs_baseline.py` nicht importieren; kein Check wurde geschwächt. |
| Vollständige Connector-/Framework-Runtime | Nicht ausgeführt: Der isolierte Task-Worktree besitzt keinen initialisierten Framework-Checkout, und die fokussierten temporären Root-Tests sind der engste anwendbare Control. |

## Security-Auswirkung

Die relevante Grenze ist Report-Generierung aus CI-Evidence. Neue Helper akzeptieren nur Source-eigene Report-Identifier und feste Report-Keys; sie akzeptieren keinen Report-Root-Parameter, registrieren keinen dynamischen Root, wählen keine dynamischen Framework-Skripte und umgehen weder `resolve_output_dir()`, `report_path_from_root()` noch `write_text_file()`. Der Einstiegspunkt-Helper behält die frühere Safe-Root- und Report-Root-Registrierungsreihenfolge intern.

Die temporäre Mutation des Callback des importierten Moduls durch den Phase-Work-Helper ist mittels `try`/`finally` begrenzt. Fokussierte Tests beweisen, dass der originale Callback wiederhergestellt wird, wenn der Framework-Payload-Builder auslöst. Der finale Source-Security-Review fand keinen plausiblen diff-eingeführten Kandidaten.

## Runtime-Evidence

Fokussierte Tests führen die Report-Lifecycle-Helper gegen temporäre Connector- und Framework-Roots aus. Sie beweisen, dass der Writer die Nutzung vor konfigurierten Safe Roots ablehnt, danach nur die registrierten Report-Pfade schreibt, Metadaten erhält, den temporären Callback nach Erfolg und kontrolliertem Fehler wiederherstellt und einen externen `--output-dir` vor Analyse, Schreiben oder Artefakterstellung abweist. Der Nolog-Callback-Test beweist zusätzlich, dass sein Sonderpfad den Listennormalizer des dynamisch importierten Frameworks nutzt. Es werden kein Connector-Server, keine netzwerkgestützte Vorbereitung, keine Framework-Runtime-Matrix und kein generiertes Repository-Artefakt beansprucht.

## Bekannte Einschränkungen

- Dieses Record beansprucht nicht, dass der breitere Parent-`ci/`-SonarQube-Cloud-Backlog erschöpft ist. Es dokumentiert nur einen nicht überlappenden CPD-Cluster.
- Der anfängliche PR-Head maß zehn neue Duplikatzeilen im Einstiegspunkt-Restblock. Dieses Record dokumentiert die lokal validierte Fixed-Root-Extraktion; frische gehostete SonarQube-Cloud-Evidence bleibt erforderlich.
- Hosted-GitHub-Actions- und SonarQube-Cloud-Evidence müssen nach jedem Head-Update am exakten Pull-Request-Head erneut gelesen werden.

## Abgleich des Delivery-Status

Draft-PR [#188](https://github.com/Easton97-Jens/ModSecurity-conector/pull/188) wurde vom anfänglichen Task-Commit `ed06eb84a07b0d50988dc308087e85da589311e1` erstellt. Beim exakten späteren Head `6bd1d57dec320265a1b98956adfa4c008a6d709e` waren lokaler, Remote- und GitHub-Head gleich, alle `33` GitHub-Checks bestanden, und SonarQube Cloud meldete `new_violations=0`, `new_duplicated_lines=0` sowie `new_duplicated_lines_density=0.0`. Dieses Dokumentations-Evidence-Follow-up verschiebt den PR-Head, deshalb müssen diese exakten Checks danach erneut gelesen werden. Hier werden kein Review, Thread, Mergeability-Ergebnis oder Merge beansprucht.

## Verbleibende Risiken

Die Shared-Helper-Grenze hängt von den bestehenden vertrauenswürdigen Parent- und Framework-Report-Roots ab. Dieser Patch erweitert diese Roots weder noch beansprucht er, die repositoryweite TOCTOU-Annahme für vertrauenswürdige Artefakt-Roots zu beseitigen. Der aktuelle SonarQube-Cloud-Bericht ist ein Auswahlinput, kein Beweis für das Resultat des exakten künftigen PR-Heads.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine komplette Framework-Runtime wurde nicht ausgeführt, weil dem isolierten Task-Worktree der initialisierte Framework-Checkout fehlt, der für bestehende Repository-Checks benötigt wird. Kein Check wurde geschwächt; direkte Owner-Tests, Kompilierung, Whitespace und fokussierter Security-Review wurden stattdessen genutzt.
- Dieser Dokumentations-Evidence-Commit verschiebt den verifizierten Head; Hosted-GitHub-Actions-, SonarQube-Cloud-, Review-, Thread-, Mergeability- und Merge-Status müssen am resultierenden exakten PR-Head erneut gelesen werden.

## Finaler Diff- und Review-Status

Der lokale Diff besitzt fokussierte Tests, Kompilierung, Whitespace-Validierung, abgeschlossene Source-/Test-Security-Reviews ohne reportbaren Kandidaten und einen Bilingual-Dokumentationscheck, der nur durch bereits fehlende Framework-Submodule-Targets blockiert ist. Draft-PR #188 hatte alle `33` Checks und SonarQube-Cloud-New-Code-Werte null/null/`0.0` am exakten Head `6bd1d57d…`; dieser Evidence-Commit erfordert eine finale Exact-Head-Nachprüfung. Keine Default-Branch-Aktion ist autorisiert oder impliziert.
