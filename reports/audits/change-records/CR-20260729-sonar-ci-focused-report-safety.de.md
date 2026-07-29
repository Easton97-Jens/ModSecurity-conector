# Change Record: Parent-CI-Focused-Report-Helper-Deduplizierung und Request-Body-Pfadbegrenzung

**Sprache:** [English](CR-20260729-sonar-ci-focused-report-safety.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-focused-report-safety` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Bewertete Source-Revision | Lokaler Working-Tree-Diff von der Basis-Revision. Der versiegelte anfängliche fokussierte Source-/Test-Snapshot ist `codex-security-snapshot/v1:sha256:c18a44b023c66ffc8ae6489f0735941d7d95ab635d055e9e1543525badd8ce8b`; der finale Diff besitzt außerdem einen ergänzenden Nolog-Import-only-Review. |
| Grenze | Ausschließlich die vier genannten Parent-`ci/`-Report-Generatoren, `ci/lib/focused_analysis_utils.py`, ihr direkter Parent-Test, dieses englisch/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`-, `scripts/`-, Framework-, MRTS-, Gitlink-, Scanner-Konfigurations-, Quality-Gate-, Exclusion-, Suppression- oder Default-Branch-Änderung ist enthalten. |
| SonarQube-Cloud-Verknüpfung | Zielt auf zwei aktuelle `python:S1192`-Body-Processor-Literale und die exakt ausgewählten `action_value`-/`log_paths`-Duplikatblöcke aus Parent-`ci/`; keine Scanner-Policy oder Issue-Disposition wird geändert. |

## Motivation und Problemstellung

Das aktuelle Parent-`ci/`-Inventar enthält zwei `python:S1192`-Literal-Findings
im Body-Processor und doppelte Parsing-/Pfadauswahl-Helper über die ausgewählten
fokussierten Report-Generatoren. Diese können nur sicher reduziert werden, wenn die Helper
ihr bisheriges First-Match-, Ordnungs- und Safe-Root-Verhalten exakt behalten.

Während des verpflichtenden Security-Reviews wurde über die echte
Body-Processor-Report-Grenze ein separater, bereits bestehender Defekt
reproduziert: Ein artefaktabgeleiteter traversal-förmiger `case_id` wählte eine
Out-of-Root-`conf/request-body.bin`, deren Bytes, Vorschau und SHA-256 in den
generierten Record gelangten. Das kanonische lokale Finding ist
`FND-PARENT-0065`; dieses Change Record schließt es nicht und beansprucht keine
gehostete Verifikation.

## Implementierungsentscheidung und Begründung

`ci/lib/focused_analysis_utils.py` besitzt jetzt die verhaltensidentischen
Helper `action_value()` und `log_paths()`. Die vier betroffenen Report-Generatoren
importieren den jeweils benötigten Helper direkt: `action_value()` wird von allen vier,
`log_paths()` von den drei Evidence-Log-Consumern geteilt. Die exakten Body-Processor-Literale
`multipart/form-data` und `conf/modsecurity-smoke.conf` werden durch benannte
Konstanten besessen, wobei jeder bisherige Vergleich und generierte Pfad
erhalten bleibt.

Die enge Sicherheitsreparatur liegt an der abgeleiteten Request-Body-Lesegrenze.
`generated_body_length()` und `request_body_bytes()` rufen jetzt den
vorhandenen Control `safe_existing_file()` auf, bevor sie den Kandidaten
verwenden. Damit bleibt ein gewöhnlicher generierter In-Root-Body erhalten,
während Traversal oder ein außerhalb registrierter Roots auflösender Symlink den
bestehenden Request-Body-Fallback nutzen, statt den Kandidaten zu lesen.

Der Patch lehnt bewusst nicht global jeden Case-ID-Text ab, verändert keine
Safe-Root-Registrierung, keine Evidence-/Output-Roots, zentralisiert kein
unabhängiges Report-Verhalten, verändert keine Subprocess-/Import-Pfade und
schwächt keinen Validierungs-Control.

## Akzeptanzkriterien

- Die vier früheren `action_value()`-Implementierungen behalten
  case-insensitive First-Match-Wertauswahl und den `"-"`-Fallback.
- Das frühere `log_paths()`-Verhalten behält Evidence-Einfügereihenfolge,
  akzeptierte Keys und den `safe_existing_file()`-Gate.
- Die zwei ausgewählten Literale behalten ihre exakten Strings und das
  bestehende Output-Verhalten.
- Ein traversal-abgeleiteter Request-Body-Pfad und ein In-Root-Symlink, der
  außerhalb der Safe Roots auflöst, können den Outside-Sentinel nicht über den
  Report offenlegen.
- Ein gewöhnlicher generierter In-Root-Request-Body bleibt verfügbar.
- Der exakte künftige PR-Head muss null neue SonarQube-Cloud-Issues und `0.0%`
  New-Code-Duplikation zeigen, ohne Rule-, Quality-Gate-, Exclusion-,
  Suppression- oder Coverage-Policy-Änderung.

## Geänderte Dateien

- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/lib/focused_analysis_utils.py`
- `tests/test_focused_analysis_utils.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-focused-report-safety.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-focused-report-safety.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| Pre-Fix fokussierte Regression | Als Reproducer bestanden: Der Test schlug exakt fehl, weil `outside-root-sentinel` die Body-Vorschau erreichte. |
| Kontrollierter Pre-Fix-Pfad-Probe | Als Reproducer bestanden: `vulnerability_reproduced` war `true`; der Out-of-Root-Sentinel-Hash entsprach dem generierten Record-Hash, während ein In-Root-Control lesbar blieb. |
| Fokussierte Utility-Regression-/Control-Suite | Bestanden: `14` Tests, einschließlich Traversal-, Symlink- und legitimer In-Root-Controls. |
| Conditional-Remediation-Report-Suite | Bestanden: `9` Tests. |
| Presentation-Literal-Report-Suite | Bestanden: `3` Tests. |
| Kontrollierter Post-Fix-Pfad-Probe | Bestanden: `vulnerability_reproduced` ist `false`; Traversal und Symlink verwenden beide `fallback-body`, und der In-Root-Body bleibt lesbar. |
| Selected-File-`py_compile` mit task-eigenem Bytecode-Cache | Bestanden. |
| `git diff --check origin/master` | Bestanden. |
| Formaler Codex-Security-Final-Diff-Review | Bestanden: Der anfängliche Five-File-Review und der ergänzende Nolog-Import-only-Review fanden keinen diff-eingeführten Kandidaten. |
| Vollständiges `make lint` | Vor der geänderten Source blockiert, weil dem isolierten Task-Worktree die Framework-Submodule-Datei `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py` fehlt; kein Check wurde geschwächt. |

## Security-Auswirkung

Die relevante Invariante ist, dass artefaktabgeleitete Pfade einen Read erst
nach kanonischer Safe-Root-Validierung erreichen dürfen. Vor der Änderung
umging `request_body_bytes()` diesen Control und las den abgeleiteten Kandidaten
direkt. Der lokale Patch stellt den bestehenden Control an der engstmöglichen
Read-/Byte-Sink-Grenze wieder her.

Der kombinierte finale und ergänzende Security-Review fand keinen neu eingeführten Kandidaten. Das aktuelle
repositoryweite Safe-File-Modell behält seine dokumentierte gewöhnliche
TOCTOU-Annahme für vertrauenswürdige Artefakt-Roots; diese Bedingung bestand vor
diesem Patch, wurde weder erweitert noch hier als behoben dargestellt.

## Runtime-Evidence

Keine Connector-Runtime, netzwerkgestützte Vorbereitung oder vollständige
Host-Matrix wird beansprucht. Die retained Probes üben die tatsächliche
Report-Generator-Metadatengrenze in einem temporären,
Safe-Root-eingeschränkten Dateisystem aus, ohne generierte Report-Artefakte zu
schreiben. Der formale finale Source-Security-Report wird außerhalb des
Repositorys im task-eigenen Security-Scan-Evidence-Verzeichnis retained.

## Bekannte Einschränkungen

- Der isolierte Task-Worktree enthält keinen initialisierten Framework-Checkout,
  deshalb ist vollständiges `make lint` vor der geänderten Source blockiert;
  fokussierte Owner-Checks sind getrennt retained.
- Dieses Change Record beansprucht nicht, dass der breite aktuelle Parent-`ci/`
  Backlog erschöpft ist; es dokumentiert nur diesen nicht überlappenden
  CI-A-Cluster.

## Abgleich des Delivery-Status

PR #175 wurde nach seinem anfänglichen lokalen Evidence-Snapshot aus dieser
abgegrenzten Änderung erzeugt. Dieses Record bewahrt nur jene lokale Evidence;
aktuelle Exact-Head-GitHub-Actions-, SonarQube-Cloud-, Review-, Thread- und
Merge-Evidence wird durch den kontrollierten Integrationstask aufbewahrt und
muss nach jeder Head-Aktualisierung erneut geprüft werden. Es beansprucht nicht,
dass ein für einen früheren Head abgeschlossenes Hosted-Ergebnis für einen
späteren weiterhin gültig ist.

## Verbleibende Risiken

`FND-PARENT-0065` bleibt `validated`, bis sein Lifecycle die notwendige
Exact-Head-Delivery-Evidence erhält. Lokale Tests und Probes zeigen, dass der
aktuelle Working-Tree-Patch die dokumentierte Reproduktion schließt, aber dieses
Record beansprucht selbst keinen aktuellen Exact-Head-Commit-, Push-, PR-,
Hosted-Check-, Hosted-SonarQube-Cloud-, Review-, Thread- oder Merge-Status. Die
bestehende TOCTOU-Annahme für vertrauenswürdige Artefakt-Roots bleibt ebenfalls
außerhalb dieses engen Patches.

## Nicht ausgeführte Prüfungen mit Begründung

- Gehostete GitHub Actions, Exact-Head-SonarQube-Cloud-Issue-/Duplikatresultate,
  Review-, Thread- und Merge-Status wurden im anfänglichen lokalen Snapshot
  nicht ausgeführt; der kontrollierte Integrationstask prüft sie gegen den
  aktuellen exakten PR-Head erneut.
- Keine Connector-Runtime, netzwerkgestützte Vorbereitung oder vollständige
  Host-Matrix wurde ausgeführt: Die Source-Änderung ist eine fokussierte
  CI-Evidence-/Report-Reparatur, und die retained Real-Boundary-Probes sind die
  engste relevante Runtime-Evidence.

## Finaler Diff- und Review-Status

Der Working-Tree-Diff ist lokal validiert und hat einen abgeschlossenen kombinierten
Security-Review mit null reportbaren Diff-Findings. Der task-eigene PR existiert
jetzt; sein aktueller exakter committeter Head muss gegen aktuellen Master-Base,
GitHub Actions, SonarQube Cloud, Reviews, Threads und Mergeability erneut
geprüft werden. Keine Default-Branch-Aktion ist autorisiert oder impliziert.
