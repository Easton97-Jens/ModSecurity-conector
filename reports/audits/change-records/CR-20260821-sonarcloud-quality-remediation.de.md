# Change Record CR-20260821: SonarCloud-Quality-Remediation

**Sprache:** [English](CR-20260821-sonarcloud-quality-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260821-sonarcloud-quality-remediation` |
| Datum (UTC) | `2026-08-21` |
| Basis-Revision | `c2e2c6a77edd0f1ccc3d41fc4e133974a630e518` |
| Scope | Nur Parent-Repository; keine Framework-, MRTS-, Gitlink-, Sonar-Exclusion-, Suppression- oder Quality-Gate-Konfigurationsänderung |

## Motivation und Problemstellung

Die angefragten SonarCloud-Pfade enthielten zehn aktuelle, bearbeitbare
Code-Smell-Instanzen: ein `python:S1192`, zwei `python:S5713`, zwei
`python:S5778` und fünf `cpp:S5945`. Der Updater und sein Test hatten null
aktuelle Issue-Instanzen; ihre Duplizierungsblöcke sind getrennt besessenen
Framework-Spiegeln zugeordnet.

## Akzeptanzkriterien

- Die zehn direkt zugeordneten Parent-Sonar-Issue-Instanzen ohne Suppressions,
  Exclusions, `NOSONAR`, Testlöschung oder Quality-Gate-Änderungen beheben.
- Fail-Closed-Verhalten des Collectors und seine No-Follow-Symlink-Controls
  erhalten.
- Header-Bytes/-Längen des Targeted Evaluators und sein erlaubtes/blockierendes
  ModSecurity-Verhalten erhalten.
- Fokussierte Test-, Kompilierungs-, Runtime-, Security-, Dokumentations- und
  Hosted-PR/Sonar-Evidence liefern sowie nicht ausgeführte Checks und
  Ownership-Limits offenlegen.
- Framework, MRTS, Gitlink und die gespiegelten Updater-Dateien nicht ändern.

## Implementierungsentscheidung und Begründung

- Das wiederholte Status-Output-Label des Collectors zentralisiert und den
  bestehenden `ValueError`-Fail-Closed-Catch erhalten; redundante Subklassen
  entfernt.
- `ProfileSpec` vor den zwei Exception-Assertions konstruiert, sodass jedes
  `assertRaises` nur `collect` auswertet; einen Fail-Closed-Regressionstest für
  fehlerhaften Status ergänzt.
- Die fünf C-Style-Header-Arrays des Evaluators durch einen einzigen
  längenerhaltenden `std::string_view`-Helper um die libmodsecurity-API ersetzt.
- `ci/tools/update-workflow-tools.py` und sein Test unverändert gelassen: null
  repositoryübergreifende Duplizierung erfordert eine separat autorisierte
  Parent/Framework-Architekturentscheidung, keinen kosmetischen Rewrite oder
  eine Sonar-Einstellung.

## Security-Auswirkung

Der Collector bleibt bei fehlerhaftem Preflight-Status fail closed, und die
vorhandenen No-Follow-Symlink-Rejection-Controls bestanden. Der Evaluator
übergibt weiterhin explizite Header-Byte-Längen; die Source-Prüfung von
libmodsecurity bestätigte, dass die API diese Bytes synchron kopiert. Der
fokussierte Security-Diff-Scan deckte alle geänderten Produktionspfade ab und
lieferte null reportierbare Findings.

## Geänderte Dateien

- `ci/runtime/common/collect_hostruntime_preflight_evidence.py`
- `tests/test_collect_hostruntime_preflight_evidence.py`
- `common/scripts/modsecurity_targeted_eval.cc`
- `reports/audits/change-records/CR-20260821-sonarcloud-quality-remediation.md`
- `reports/audits/change-records/CR-20260821-sonarcloud-quality-remediation.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Collector-Unittest-Suite | Bestanden: 6 Tests einschließlich fehlerhaftem Status und beiden No-Follow-Symlink-Controls |
| C/C++-Diagnostics-Unittest-Suite | Bestanden: 7 Tests |
| `make check-targeted-evaluator-cpp17` | Bestanden: C++17-Evaluator erfolgreich kompiliert |
| Gehärtete Evaluator-Kompilierung | Bestanden mit Warnings-as-Errors, Stack Protection, Fortify, PIE, RELRO und NOW-Linker-Flags |
| Erlaubter Evaluator-Control | Bestanden: Kein Smoke-Header ergab nicht-disruptives HTTP 200 |
| Blockierender Evaluator-Control | Bestanden: `X-Modsec-Smoke: block` ergab disruptives HTTP 403 |
| `git diff --check` | Vor der Change-Record-Delivery-Prüfung bestanden; auf dem finalen Staging-Diff erneut auszuführen |
| Fokussierter Security-Diff-Scan | Bestanden: vollständige Abdeckung und null reportierbare Findings |

## Runtime-Evidence

Der reale Targeted Evaluator wurde gegen
`common/rules/modsecurity_targeted_smoke.conf` ausgeführt. Er lud Regel
`1000001`, lieferte 200 für den erlaubten Control und 403 für den blockierenden
Control. Der aufbewahrte Security-Report liegt unter
`/var/tmp/codex/ModSecurity-conector/runs/sonarcloud-quality-remediation-20260821/security-diff-scan/report.md`
(SHA-256 `ee826f3aa20f24d6e61ac771e14d9237efe33a6d2fc993228d6713a7e9b6e78d`).

## Nicht ausgeführte Prüfungen mit Begründung

- Die vollständige Repository-Suite wurde nicht ausgeführt; die Änderung wird
  durch die engen Collector- und Evaluator-Suites sowie direkte
  Evaluator-Controls abgedeckt.
- Ruff war lokal nicht installiert; es wurde keine Installation oder Umgehung
  verwendet.
- Kein HTTP/1.1-, HTTP/2- oder HTTP/3-Host wurde gestartet: Der Patch ändert
  In-Process-Evaluator-Header-Marshalling, wofür die realen Evaluator-Controls
  die passende Runtime-Evidence sind.
- Kein Sanitizer-Runtime-Lauf wurde ausgeführt, weil kein task-eigener
  Host-Harness vorhanden ist; stattdessen liefen normale und gehärtete
  Kompilierungen.
- Ein lokaler Sonar-Scanner war nicht konfiguriert. Hosted-Exact-PR-Head- und
  Resulting-Master-SonarCloud-Analyse bleiben die autoritative Messung.

## Bekannte Einschränkungen

Die zwei Updater-Pfade behalten repositoryübergreifende Duplizierungsdichte,
bis der User Framework-Arbeit und ein gemeinsames Ownership-, Packaging- oder
Synchronisationsdesign ausdrücklich autorisiert. Die Aufgabe verwendet bewusst
keine Exclusions, Suppressions oder Konfigurationsänderungen, um diese Metrik
künstlich zu senken.

## Verbleibende Risiken

Lokale Evidence belegt das beabsichtigte Source-, Test-, Kompilierungs- und
Runtime-Verhalten; die zehn Sonar-Issue-Instanzen bleiben aber `fixed` statt
`verified`, bis der exakte PR-Head und der resultierende `master` von gehostetem
SonarCloud analysiert wurden. Kein Security-Finding überlebte die fokussierte
Security-Prüfung.

## Finaler Diff- und Review-Status

Der Parent-only-Diff ist bereit für die finale Dokumentations- und Git-Prüfung
und danach für ein Draft-PR. Er autorisiert keinen Merge, keine Framework-
Änderung, kein Gitlink-Update und keine Sonar-Konfigurationsänderung.
