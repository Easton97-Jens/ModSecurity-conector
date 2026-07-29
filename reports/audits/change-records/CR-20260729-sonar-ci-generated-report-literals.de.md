# Change Record — Parent-CI-Generated-Report-Literal-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-ci-generated-report-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-generated-report-literals` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345` |
| Bewertete Source-Revision | Aktueller lokaler Task-Working-Tree-Diff von der Basis-Revision; beim Schreiben dieses Records werden kein Commit, Push, Pull Request, Hosted Check oder Merge beansprucht. |
| Grenze | Ausschließlich Parent-`ci/lib/generated_report_utils.py`, direkte Parent-Generated-Report-Evidence-Tests, dieses englisch/deutsche Change-Record-Paar und gepaarte Change-Record-Indizes. Keine `.github`-, `scripts`-, Framework-, MRTS-, Gitlink-, Generated-Report-, Scanner-Policy-, Quality-Gate-, Exclusion-, Suppression- oder Default-Branch-Änderung ist enthalten. |
| SonarQube-Cloud-Verknüpfung | Behebt fünf offene `python:S1192`-Literalcluster in `generated_report_utils.py`: Local-Home-Display-Token; Refresh-Report-Generator; Remaining-Failure-Generator; Framework-Case-Matrix-Generator; und Framework-Native-MRTS-Generator. |

## Motivation und Problemstellung

Der Parent-CI-Generated-Report-Helper enthielt fünf unabhängige wiederholte
statische Literalcluster, die SonarQube Cloud meldet. Die Strings sind
vertrauenswürdige, source-eigene Präsentations- oder Provenance-Labels; eine
inhaltliche Änderung könnte Path-Portability oder Report-Registry-Inferenz
gefährden. Die erforderliche Behebung bleibt eng: genau ein statischer privater
Owner je Wert, bei unveränderten Werten und unverändertem sichtbaren Verhalten.

## Akzeptanzkriterien

- Jeder der fünf genannten Werte besitzt genau einen statischen privaten
  Source-Owner in `generated_report_utils.py`; keine Regel-, Exclusion-,
  Suppression- oder Quality-Gate-Änderung.
- `/root`, `/home/<user>` und `/Users/<user>` behalten ihre portable
  Markdown-Darstellung einschließlich Unterpfaden; `/home` und relative Pfade
  bleiben unverändert.
- Jeder betroffene `GeneratedReport.generator`-Wert und seine vollständige
  Registry-Zuordnung bleiben unverändert.
- Der exakte künftige Pull-Request-Head muss null neue SonarQube-Cloud-Issues,
  null neue Duplikatzeilen und `0.0%` New-Code-Duplizierung melden.

## Implementierungsentscheidung und Begründung

- Fünf private Modulkonstanten direkt neben vorhandenen statischen
  Generated-Report-Konstanten ergänzt. Sie sind keine Konfigurations-,
  Umgebungs-, Manifest- oder CLI-Eingaben.
- Ausschließlich die genannten doppelten String-Verwendungen ersetzt. Der Code
  rendert Local-Home-Referenzen weiterhin nur in der Markdown-Präsentation;
  rohe Evidence-Pfade, Hashing und JSON-Provenance bleiben unberührt.
- Einen tabellengetriebenen direkten Control über den tatsächlichen
  Generated-Report-Layout-Importpfad ergänzt. Er prüft alle unterstützten
  Home-Root-Varianten samt sicheren Controls und validiert exakte
  Report-Generator-Gruppen statt privater Konstantennamen.

## Geänderte Dateien

- `ci/lib/generated_report_utils.py`
- `tests/test_generated_report_evidence_integrity.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-generated-report-literals.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-generated-report-literals.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

Die Befehle wurden im Task-Worktree ausgeführt. Task-eigene Host-Pfade sind
unten als portable Redaktionen dargestellt; Befehlsidentität und beobachtete
Ergebnisse sind unverändert.

- Bestanden — fokussierte Tests, `Ran 2 tests in 0.001s`, `OK`:

  ```text
  rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> <repository-venv-python> -m unittest -v tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_generated_markdown_home_paths_remain_portable tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_registry_generator_provenance_groups_remain_stable
  ```

- Bestanden — vollständiges Modul, `Ran 76 tests in 20.590s`, `OK`; sein
  kontrollierter `check-generated-report-layout`-Control bestand ebenfalls:

  ```text
  rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> <repository-venv-python> -m unittest -v tests.test_generated_report_evidence_integrity
  ```

- Bestanden — selektierte Kompilierung für geänderten Helper/Test und finale
  Whitespace-Validierung, beide ohne Ausgabe:

  ```text
  rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> <repository-venv-python> -m py_compile ci/lib/generated_report_utils.py tests/test_generated_report_evidence_integrity.py
  rtk proxy -- git -C <task-worktree> diff --check
  ```
- Blocked Evidence: das direkte `make check-generated-report-layout` liest
  committed Generated-Report-Evidence, die aktuell auf nicht verfügbare
  Verified-Runtime-Artefakte und stale Report-Inputs verweist. Es meldet diese
  bestehenden Evidence-/Freshness-Fehler; dieser Task ändert weder Reports noch
  Evidence.
- Blocked External Dependency: `make lint` beendete Shell-Syntax und
  Parent-CI-Python-Kompilierung, stoppte dann an der im isolierten Worktree
  fehlenden Framework-`no_crs_baseline.py`. Kein Control wurde geschwächt.

## Security-Auswirkung

Dies ist ein Static-Data-Refactor in einem Path-Redaction- und
Report-Provenance-Helper. Der Local-Home-Ersatz bleibt bytegenau
`<local-home-root>` und wird ausschließlich an den bestehenden
Markdown-Präsentationspunkten verwendet. Die Generatorwerte behalten das
`framework:`-Präfix und exakte Pfade, die Report-Key-Inferenz, Metadaten-,
Hash-, Verified-Run- und Framework-Gitlink-Controls verwenden. Kein
unvertrauenswürdiger Input, keine Auflösung, kein Hashing, keine
JSON-Serialisierung und keine Policy-Oberfläche ändern sich.

## Runtime-Evidence

Kein Connector-Runtime-, Netzwerk-, Protokoll-, Build-, Framework- oder
MRTS-Verhalten ändert sich. Runtime-/Matrix-Ausführung ist für statische
Python-Literal-Extraktion nicht erforderlich; die direkte
Generated-Report-Evidence-Suite liefert die proportionierten
Regression-Controls.

## Bekannte Einschränkungen

Der committed Generated-Report-Snapshot ist in diesem isolierten Worktree
nicht fresh gegenüber seinen referenzierten Verified-Runtime-Artefakten. Der
eigenständige Layout-Make-Target kann daher hier kein sauberes aggregiertes
Control sein. Sein In-Memory-/direkter Test-Control besteht, und kein Generated
Report wird aktualisiert oder verändert, um die unabhängige Evidence-Lücke zu
verbergen.

## Verbleibende Risiken

- Hosted GitHub Actions und SonarQube Cloud müssen den exakten künftigen
  Pull-Request-Head noch validieren.
- Die Change-Record-Indizes könnten einen Routine-Rebase benötigen, falls
  parallele Parent-Change-Record-Arbeit zuerst landet; ein Source-Konflikt wird
  nicht erwartet.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-/Runtime-/Matrix-Ausführung: für statische Helper-
  Literale nicht anwendbar und würde unabhängige Runtime-Evidence erfordern.
- Framework-/MRTS-Checks: nicht anwendbar und außerhalb dieses Parent-only
  Tasks.
- Scanner-Policy-, Quality-Gate-, Exclusion- oder Suppression-Änderungen:
  verboten und nicht durchgeführt.

## Finaler Diff- und Review-Status

Der aktuelle Diff beschränkt sich auf den Parent-CI-Helper, seine direkten
Parent-Generated-Report-Evidence-Tests und zweisprachige Traceability. Der
fokussierte Security-Preflight fand keine validierte Schwachstelle und verlangt
nur Exact-Value-Erhaltung, die die direkten Tests abdecken. Lokaler Commit,
Draft PR, Hosted Checks, SonarQube-Cloud-Result, Review-Status und Merge werden
beim Schreiben dieses Records nicht beansprucht. Keine Default-Branch-Aktion
ist autorisiert oder impliziert.
