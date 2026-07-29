# Change Record: Parent-CI-Deduplizierung des Case-Metadata-Parsings

**Sprache:** [English](CR-20260729-sonar-ci-case-metadata-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-case-metadata-duplication` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `fda62539b6f0a710865707e3003b73ed4469f20e` |
| Bewertete Source-Revision | Lokaler Task-Patch gegen die genannte Basis-Revision. |
| Grenze | Nur die unten genannten Parent-`ci`-Quellen, direkter Parent-Test, dieses EN/DE-Paar und Indizes. Keine `.github`-, `scripts`-, Framework-, MRTS-, Gitlink-, Scanner-Konfigurations-, Quality-Gate-, Exclusion-, Suppression- oder Default-Branch-Aktion. |
| SonarQube-Cloud-Verknüpfung | Zielt auf das aktuelle 17-Zeilen-Duplikatpaar des Case-Document-Parsings zwischen den zwei Parent-Report-Generatoren; keine Scanner-Kontrolle und kein Issue-Status wird geändert. |

## Motivation und Problemstellung

Die zwei Generatoren parsten unabhängig bereits gelesenen YAML-Case-Text, akzeptierten nur Mapping-Resultate, wählten `request`/`expect`/`metadata` und trennten Request-Pfade von Query-Strings. Das ausgewählte 17-Zeilen-Paar war ein aktuelles SonarQube-Cloud-Duplikatziel, liegt jedoch neben Evidence-Path- und YAML-Trust-Controls.

## Implementierungsentscheidung und Begründung

`parse_case_document()` besitzt nur dieses reine Textparsing. Er erhält Raw-Text und das optionale YAML-Modul und führt keine Pfadauflösung, keinen Datei-Read, keine Root-Registrierung, keine Ausgabe, keinen Subprocess und keinen Netzwerkzugriff aus.

`parse_empty=True` erhält den bisherigen Parsing-Versuch des Remaining-Failure-Generators bei leerem Text. Phase 4 behält sein bisheriges Nicht-Parsen bei leerem Text. Beide Caller behalten ihre eigene Safe-Evidence-/Case-Path-Behandlung, Rule-/Phase-Priorität, erwartete Intervention/Body, Phase-4-Classification, Runtime-Verification-Status und Pending-/Non-Promoted-Felder.

## Akzeptanzkriterien

- Gültige Mappings erhalten Request-Methode, Path/Query, Expectation und Metadata; fehlerhafte, skalare, Parser-lose und leere Eingaben behalten sichere Defaults.
- Beide Generatoren nutzen den Helper, bewahren jedoch ihre beabsichtigte Evidence-first- beziehungsweise YAML-first-Priorität.
- In-Root-Case-Daten bleiben lesbar; Out-of-Root-Pfade, ausbrechende Symlinks und externe Evidence-Dateien behalten Default-Metadaten vor dem Parsen.
- Der exakte künftige PR-Head muss null neue SonarQube-Cloud-Issues und `0.0%` New-Code-Duplizierung ohne Scanner-Policy-Änderung zeigen.

## Geänderte Dateien

- `ci/lib/case_metadata_utils.py`
- `ci/evidence/reports/generate-phase4-hard-abort-capability.py`
- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `tests/test_case_metadata_utils.py`
- dieses englisch/deutsche Change-Record-Paar und seine Indizes

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| Fokussierte Helper-, Remaining-Failure- und Focused-Analysis-Utility-Suites | bestanden: 19 Tests, einschließlich Mappings, Parser-Fallbacks, Query-only-Pfaden, Caller-Priorität, In-Root-, Out-of-Root-, Symlink- und abgelehnter-Evidence-Controls. |
| Selected-File-`py_compile` mit task-eigenem Bytecode-Cache | bestanden. |
| `git diff --check` | bestanden. |
| Unabhängige finale Source- und Test-Security-Diff-Reviews | bestanden: kein plausibler diff-eingeführter Sicherheitskandidat. |
| `make check-bilingual-docs` | `blocked_external_dependency`: alle neuen Change-Record-Section-Checks bestanden; bestehende Repository-Links benötigen fehlende Framework-Submodul-Targets, und kein geänderter Dokument-Link wurde gemeldet. |

## Security-Auswirkung

Case-YAML und Evidence-Metadaten sind nicht vertrauenswürdige CI-Report-Eingaben. Bestehende Caller behalten `safe_existing_file()` vor Reads; Production-Entry-Points behalten das Safe-Root-Setup. Der Helper behält `yaml.safe_load()` und einen Failure-to-Empty-Fallback. Senken bleiben generierte JSON-/Markdown-Reports; keine Connector-Enforcement- oder Runtime-PASS-/FAIL-Werte ändern sich.

## Runtime-Evidence

Keine Connector-Runtime, keine netzwerkgestützte Vorbereitung, kein Report-Generator-Main und keine Framework-/MRTS-Ausführung liefen. Der fokussierte Test verwendet ein privates temporäres Dateisystem und schreibt keinen Repository-Report. Hosted-GitHub-Actions, SonarQube Cloud, Review, Freigabe, Merge und Master-Verifikation sind noch nicht beobachtet oder beansprucht.

## Bekannte Einschränkungen

Der isolierte Worktree enthält nicht die Framework-Submodul-Targets, die bestehende Repository-Dokumentation referenziert; deshalb kann der repositoryweite Dokumentationscheck extern blockiert sein. Dieses Record beansprucht nicht, dass der breite Parent-`ci`-Backlog erschöpft ist.

## Verbleibende Risiken

Der Helper bewahrt die bestehende Trusted-Artifact-Root- und Bounded-Input-Annahme. Er belegt kein vollständiges Connector-Runtime-, Hosted-Quality-Gate- oder Master-State-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine Connector-Runtime, kein Report-Generator-Main und keine netzwerkgestützte Vorbereitung liefen, weil dies ein reiner Metadata-Refaktor ist und jene Befehle generierte Evidence sowie nicht verfügbaren Framework-Inhalt benötigen.
- Hosted-GitHub-Actions, SonarQube Cloud, Review, Freigabe, Merge und Master-Checks liefen noch nicht für einen PR-Head, weil noch kein PR erstellt wurde.

## Delivery-Status

Vor der Verifikation muss der exakte PR-Head mit Master abgeglichen werden und frische Hosted-Checks sowie SonarQube-Cloud-Resultate erhalten. Keine direkte Master-Änderung oder kein Merge ist autorisiert oder impliziert.

## Finaler Diff- und Review-Status

Der lokale Source-/Test-Diff bestand fokussierte Tests, ausgewählte Kompilierung, Whitespace-Validierung und unabhängige Source-/Test-Security-Diff-Reviews ohne plausiblen diff-eingeführten Kandidaten. Die finale Exact-PR-Head-Hosted-Verifikation steht aus.
