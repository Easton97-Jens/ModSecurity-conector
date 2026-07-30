# Change Record: Parent-CI-Komplexitätsbehebung für Repository-Pfadreferenzen

**Sprache:** [English](CR-20260729-sonar-ci-repository-path-reference-complexity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-repository-path-reference-complexity` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `5a345e3ff90cf5405caea5ff7ae4536b52f826c9` |
| Tracking | Offener SonarQube-Cloud-Befund `python:S3776` `AZ9cRyWvHhV2CayPTPuo` bei `main()` in `ci/checks/documentation/check-repository-path-references.py`, der eine Reduzierung der kognitiven Komplexität von 17 auf 15 verlangt. |
| Grenze | Ausschließlich Parent-`ci/`-Checker, sein direkter Parent-Test, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine Änderung an `.github`, `scripts`, Framework, MRTS, Gitlink, Product-Source, Sonar-Regel/Profil/Gate/Exclusion/Suppression oder `master`. |

## Motivation und Problemstellung

Der portable Dokumentationschecker hatte eine `main()`-Funktion, die sowohl
das dokumentweise Parsing als auch Repository-weite Traversierung, Filterung,
Aggregation, Ausgabe und Exit-Verhalten verantwortete. SonarQube Cloud meldet
die daraus resultierende kognitive Komplexität als 17, während 15 erlaubt sind.
Die Behebung darf ausschließlich diese strukturelle Komplexität entfernen und
muss jede Pfaddiagnose und jedes Kompatibilitätsverhalten unverändert bewahren.

## Akzeptanzkriterien

- Ein privater dokumentweiser Helper bewahrt UTF-8-Lesen, Erkennung lokaler
  Developer-Pfade, Erkennung veralteter `COMPILE_*`-Guides, Link-Extraktion,
  die zwei Legacy-Placeholder-Ausnahmen, den rohen Missing-Target-Text und
  propagierte Lesefehler.
- `main()` bewahrt dasselbe Dokumentinventar, die Behandlung ignorierter
  generierter Dokumente, die deterministische `sorted(set(errors))`-
  Aggregation, stderr-Fehlerausgabe, stdout-Erfolgsausgabe und Return-Codes.
- Direkte Tests decken lokale/encoded/gewinkelte/parent-relative/Fragment-
  Links, Scheme-/Netloc-Links, rohe Missing-Targets, literales Query-Verhalten,
  Fehler, ignorierte Dokumente, Deduplizierung, Ordnung, Streams und Exit-
  Status ab.
- Der exakte Draft-PR-Head muss später ein SonarQube-Cloud-Quality-Gate `OK`,
  null neue Issues, null neue Duplicate Lines und `0.0%` New-Code-Duplizierung
  erhalten, ohne Regel-, Profil-, Gate-, Exclusion-, Suppression- oder False-
  Positive-Änderung.

## Implementierungsentscheidung und Begründung

`document_diagnostics(path)` verantwortet jetzt exakt die bestehende
dokumentweise Read/Scan/Diagnostic-Schleife. `main()` wählt weiterhin aktuelle
Dokumente, überspringt ignorierte Pfade, aggregiert Diagnosen und steuert
Ausgabe sowie Exit-Status. `local_target()` wird nicht geändert: Die Funktion
trimmt/entpackt weiter, dekodiert Prozentzeichen, überspringt Fragment-only-
und Scheme-/Netloc-Targets, entfernt Fragmente und löst verbleibende Pfade
relativ zum Quelldokument auf. Dies ist eine enge Extraktion und keine Änderung
an Path-Containment oder Link-Policy.

## Geänderte Dateien

- `ci/checks/documentation/check-repository-path-references.py`
- `tests/test_repository_path_references.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-repository-path-reference-complexity.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-repository-path-reference-complexity.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_repository_path_references` | bestanden: 6 direkte Tests. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m py_compile ci/checks/documentation/check-repository-path-references.py tests/test_repository_path_references.py` | bestanden. |
| `git diff --check` für die Source-/Test-Implementierung vor diesem Traceability-Update | bestanden. |
| Direkter Parent-Checker mit deaktiviertem Bytecode | `blocked_external_dependency`: Er meldet ausschließlich vorhandene Links auf fehlende Parent-gepinnte Framework-README-/Rule-Dateien in diesem isolierten Worktree; kein task-eigenes Dokument wird genannt. |
| Direktes `check-bilingual-docs.py` | `blocked_external_dependency`: 20 Diagnosen benennen ausschließlich vorhandene fehlende Framework-Gitlink-Targets; dieses Change-Record-Paar und die Indizes werden nicht genannt. |
| `make check-doc-links` mit deaktiviertem Bytecode | `blocked_external_dependency`: Der direkte Parent-Checker gibt dieselben 16 vorhandenen fehlenden Framework-README-/Rule-Targets aus und endet vor dem Framework-Checker. |
| Fokussierter Security-Preflight | bestanden / `already_safe`: Die Extraktion fügt keinen Source-Type, kein Privileg, keinen Sink und keinen Control-Bypass hinzu; fokussierter Post-Diff-Review bleibt erforderlich. |
| Fokussierter finaler Security-Diff-Review | bestanden / `already_safe`: Vollständiger Review des geänderten Checker-/Test-Flows bestätigt, dass `local_target()`, Dokumentroots, Ignored-Path-Grenze, rohe Diagnosen, bestehende Read-/Resolve-/Exists-Calls, Streams und Exit-Verhalten unverändert sind; es existiert kein neuer Filesystem-, Process-, Network-, Privilege-, Cache- oder Logging-Pfad. |
| Draft-PR-Erstellung | bestanden: [#194](https://github.com/Easton97-Jens/ModSecurity-conector/pull/194) ist offen/Draft gegen `master`; sein initialer lokaler, Remote- und PR-Head stimmen bei `fd4e9902bb00df20ca97e7b38bcf1231afdcdb06` überein. Hosted-Exact-Head-Checks, Review- und SonarQube-Cloud-Evidence stehen aus. |

## Security-Auswirkung

Repository-kontrolliertes Markdown bleibt der relevante Input. Seine Links
durchlaufen weiter den unveränderten `local_target()`-Parser in die bestehenden
lokalen `Path.resolve()`- und `Path.exists()`-Prüfungen;
`document_diagnostics()` verschiebt ausschließlich den bereits vorhandenen
UTF-8-Read und die Diagnostic-Schleife in einen privaten Helper. Es gibt keinen
neuen Traversal-Root, File-Write, Process, Network-Request, Cache, Log oder
Output-Channel. Die Test-Suite bewahrt negative und legitime Path-/Link-
Kontrollen. Ein vorhandener POSIX-absoluter Link kann weiterhin eine
Existenzprüfung außerhalb des Repositorys erzeugen; es wurde keine
Confidentiality-, Integrity- oder Execution-Auswirkung nachgewiesen, und eine
Änderung dieser Semantik ist out of scope.

## Runtime-Evidence

Keine Connector-, Host-, Network- oder Protocol-Runtime ist anwendbar. Die
direkte Unit-Suite ist ausschließlich In-Process-Dokumentationschecker-
Evidence. Der direkte Whole-Tree-Checker wurde versucht, ist aber wegen
fehlendem Framework-Gitlink-Content blockiert und wird daher nicht als
erfolgreiches Runtime- oder Dokumentationsbaum-Ergebnis dargestellt.

## Bekannte Einschränkungen

Diese Aufgabe stellt die fehlenden Framework-Gitlink-Dateien nicht wieder her
und materialisiert sie nicht. Deshalb kann der isolierte Worktree aktuell kein
erfolgreiches Whole-Tree-Ergebnis von `check-repository-path-references.py`,
`check-bilingual-docs.py` oder `make check-doc-links` liefern, obwohl die
neuen checker-spezifischen Unit-Tests und die direkte Change-Record-
Validierung bestehen.

## Verbleibende Risiken

Eine zukünftige Änderung an Dokumentenumerierung, `local_target()` oder
Output-Handling muss den URL-/Path- und Aggregationsvertrag der Tests bewahren.
Hosted-Analyse ist weiterhin nötig, um zu zeigen, dass SonarQube Cloud dem
exakten ausgelieferten Head keine neue Issue oder Duplizierung zuordnet.

## Nicht ausgeführte Prüfungen mit Begründung

- Breites `make lint` wird nicht ausgeführt, weil der bereits ausgeführte
  direkte Checker und `make check-doc-links` denselben fehlenden Framework-
  Blocker belegen, bevor unverbundene Validierungsebenen task-irrelevante
  Fehler hinzufügen können.
- Kein Framework-, MRTS-, Gitlink-, `.github`-, `scripts`-, Product-Source-,
  Connector-Runtime- oder Matrix-Befehl ist in diesem Parent-`ci/`-Scope.
- Exact-Head-GitHub-Actions-, Review- und SonarQube-Cloud-Evidence benötigen
  einen gepushten Draft PR und werden nicht lokal hergeleitet.

## Finaler Diff- und Review-Status

Der Working Candidate enthält den privaten Helper, sechs direkte Regression-
Tests und dieses bilinguale Traceability-Update. Der finale lokale Source-/
Test- und Security-Diff-Review bestand, während Whole-Tree-
Dokumentationschecks wahrheitsgemäß durch fehlende Framework-Gitlink-Targets
blockiert bleiben. Draft PR
[#194](https://github.com/Easton97-Jens/ModSecurity-conector/pull/194) ist
offen und bleibt Draft; es wird kein Hosted-Pass, Approval, Ready-for-Review-
Status oder Merge beansprucht. Ein reiner Record-Delivery-Follow-up erzeugt
absichtlich einen neuen PR-Head, nach dem Exact-Head-Hosted-Verifikation nötig
ist.
