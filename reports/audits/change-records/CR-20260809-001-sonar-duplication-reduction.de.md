# Change Record CR-20260809-001: Sonar-Duplikatreduzierung

**Sprache:** [English](CR-20260809-001-sonar-duplication-reduction.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260809-001` |
| Datum (UTC) | `2026-08-09` |
| Basis-Revision | `27e8756e212fd9452d99e285743dbadc43c814a6` |
| Umfang | Nur Parent-Repository; keine Änderung an Framework, MRTS, Gitlink, Workflow, Lock-Datei oder Quality Gate |

## Motivation und Problemstellung

SonarCloud meldete eine Duplikatcodedichte oberhalb des angeforderten
Grenzwerts im Workflow-Tool-Updater und seinem Testmodul sowie zwei doppelte
C-Quellcode-Parserhelfer in NGINX-Vertragstests. Die Änderung entfernt nur
nachgewiesene strukturelle Duplikate und erhält die Sicherheitsprüfpunkte des
Updaters.

Die vor der Änderung erfassten SonarCloud-Metriken waren:

| Komponente | Duplizierte-Zeilen-Dichte | Duplizierte Zeilen | Duplizierte Blöcke |
| --- | ---: | ---: | ---: |
| `tests/ci_security/test_update_workflow_tools.py` | 67.2% | 709 | 13 |
| `ci/tools/update-workflow-tools.py` | 62.1% | 1,305 | 15 |
| `tests/test_nginx_intervention_url_ownership.py` | 18.1% | 25 | 2 |
| `tests/test_nginx_upstream_security_contract.py` | 6.6% | 25 | 2 |

## Akzeptanzkriterien

- Ausschließlich den freigegebenen Parent-Quell- und Testumfang mit kleiner
  gemeinsamer Testunterstützung bei Bedarf refaktorieren.
- Update-CLI-Flags, YAML-/Lock-Serialisierung, kanonisches Candidate-JSON,
  SHA-256-Eingaben, Exit-Codes, Ablehnungsverhalten und Ausgabepfade erhalten.
- Strenge Vertrauensgrenzen für Action-/Tool-Identität, unveränderliche Pins,
  Release-Commits, URLs, Asset-Pfade, Hashes und Runner-Temporärpfade erhalten.
- Kein `NOSONAR`, keine Sonar-Ausschlüsse, Suppression-Anmerkungen,
  Testlöschung, schwächeren Assertions, Quality-Gate-Änderungen oder
  generischen Lock-Record-Merges verwenden.
- Fokussierte Tests, Kompilierung, Vertragsprüfungen, Dokumentationsprüfungen,
  einen Security-Diff-Scan und gehostete PR-/SonarCloud-Validierung ausführen.

## Implementierungsentscheidung und Begründung

- `CandidateGroupSpec` und unveränderliche Candidate-Payload-Konstruktion
  hinzugefügt, um das geprüfte Action-/Tool-Schema zu zentralisieren und die
  getrennten Action-/Tool-Identitäts- und Release-Auflösungspfade explizit zu
  lassen.
- Alle öffentlichen Hilfsfunktionsnamen an ihren bestehenden Aufrufstellen
  beibehalten; ihre Implementierungen delegieren an eng abgegrenzte
  unveränderliche Boundary-Objekte für Runner-Temporärpfade,
  Workflow-Inventar und die GitHub-API.
- `tests/c_source_contract.py` für ausgeglichene C-Definitions-Extraktion und
  seine Unit-Tests hinzugefügt und beide NGINX-Tests auf diesen Helfer umgestellt.
- Wiederholte Test-Fixture-Maps durch explizite Fixtures und tabellengesteuerte
  Fälle ersetzt. Bestehende Testmethoden bleiben vorhanden; zusätzliche
  Ablehnungs- und Unveränderlichkeitsfälle wurden ergänzt.

## Security-Auswirkung

Der geänderte Updater überschreitet Eingabe-, Dateisystem-, Netzwerk-,
Serialisierungs- und Lock-Datei-Vertrauensgrenzen. Der Refaktor erhält strenge
Candidate-Gruppen-Felder, die Validierung unveränderlicher Action-Pins und
Tool-Release-Commits, die Prüfung vertrauenswürdiger GitHub-Origins und
Redirects, URL-, Asset- und SHA-256-Prüfungen, kanonisches Candidate-JSON,
sichere Relative-Pfad- und Symlink-Ablehnung sowie atomaren Lock-Datei-Ersatz.

Der fokussierte Security-Diff-Scan deckte alle sechs geänderten Codedateien ab
und lieferte null berichtspflichtige Kandidaten. Er identifizierte keinen neuen
Angriffspfad und keine abgeschwächte Kontrolle.

## Geänderte Dateien

- `ci/tools/update-workflow-tools.py`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/c_source_contract.py`
- `tests/test_c_source_contract.py`
- `tests/test_nginx_intervention_url_ownership.py`
- `tests/test_nginx_upstream_security_contract.py`
- `reports/audits/change-records/CR-20260809-001-sonar-duplication-reduction.md`
- `reports/audits/change-records/CR-20260809-001-sonar-duplication-reduction.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Unittest-Suite | Bestanden: 51 Tests in 11.926 s |
| `python -m py_compile` für die geänderten Python-Module | Bestanden |
| `make check-ci-security-contract` | Bestanden: 22 Tests; checksum-gesperrte actionlint-, zizmor- und gitleaks-Validierung bestanden |
| checksum-gesperrtes actionlint mit ShellCheck | Bestanden für `.github/workflows/*.yml` |
| checksum-gesperrtes `zizmor --offline .github/workflows` | Bestanden: keine Findings (87 vom Repository unterdrückte Findings wurden von zizmor gemeldet) |
| `git diff --check HEAD` | Bestanden |
| Fokussierter Security-Diff-Scan | Bestanden: vollständige Sechs-Dateien-Abdeckung und null berichtspflichtige Findings |
| `make check-bilingual-docs` | Nur durch 20 fehlende Framework-Link-Ziele im nicht materialisierten Task-Worktree-Gitlink blockiert; der Change Record gab keinen Überschriften-/Identitätsfehler aus |
| `make check-doc-links` mit autoritativem `FRAMEWORK_ROOT` | Nur durch dieselben lokalen Gitlink-Link-Ziele blockiert |

Die fokussierte Suite umfasst die Updater-Tests, beide NGINX-Vertragstests und
die neuen C-Quellcode-Helfertests. Sie prüft kanonische Candidate-Payload-Bytes
und SHA-256-Eingabestabilität, CLI-Parsing, Validierungs-Ablehnungspfade,
Ausgabepfade und Lock-Datei-Anwendungsverhalten.

## Runtime-Evidence

Es war keine produktive Connector-Laufzeit erforderlich oder ausgeführt, weil
dies ein Python-Refaktor statischer CI-Sicherheitswerkzeuge und Vertragstests
ist. Die anwendbare Evidenz ist die fokussierte Unit-/Vertragssuite und der
versiegelte Security-Diff-Scan unter
`/var/tmp/codex/ModSecurity-conector/tmp/codex-security-scans/ModSecurity-conector/27e8756e212fd9452d99e285743dbadc43c814a6_20260809T053956Z/report.md`.

Gehostete GitHub Actions und die SonarCloud-PR-Analyse stehen bei
Veröffentlichung dieses lokalen Records noch aus und müssen mit ihren
beobachteten Ergebnissen dokumentiert werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Das Repository hat keine Targets namens `test-ci-security-contract`,
  `test-workflow-action-pins`, `check-github-actions-workflows` oder
  `check-documentation`; die nächstliegenden vorhandenen Targets wurden, wo
  anwendbar, verwendet.
- `ruff` und `pyright` sind lokal nicht installiert und das Repository enthält
  kein konfiguriertes Ersatz-Target. Es wurde kein Tool installiert oder
  umgangen.
- actionlint, zizmor und gitleaks waren nicht vorinstalliert. Die ersten
  beiden wurden ausschließlich über den checksum-gesperrten Repository-Fetcher
  in das externe Task-Verzeichnis geladen und dann ausgeführt; der
  diff-basierte gitleaks-Lauf wird aufgeschoben, bis überprüfbare Commits einen
  exakten Git-Bereich liefern.
- Der erste `make lint`-Lauf endete mit Exit 2, weil ein Parent-Test einen
  Framework-Quellpfad relativ zum isolierten Task-Worktree fest kodiert. Der
  gepinnte Framework-Quellcode existiert im autoritativen Checkout, aber dieser
  Test ignoriert die dokumentierte `FRAMEWORK_ROOT`-Überschreibung. Weder
  Framework-Inhalt noch Gitlink wurden zur Umgehung geändert.

## Bekannte Einschränkungen

Lokale Prüfungen können weder die SonarCloud-Duplikatmetriken nach der Änderung
noch das gehostete PR-Quality-Gate beweisen. Die angeforderte gehostete Analyse
bleibt die maßgebliche Messung. Das vollständige lokale Lint-Target ist derzeit
nur durch die nicht materialisierte Framework-Gitlink-Abhängigkeit des
Task-Worktrees blockiert.

## Verbleibende Risiken

Das wichtigste Restrisiko ist Verhaltensdrift im sicherheitssensitiven Updater.
Es wird durch Erhaltungstests, explizite unveränderliche Schemaobjekte, ein
unabhängiges Diff-Audit, den fokussierten Security-Diff-Scan und die
ausstehenden gehosteten Prüfungen reduziert; es ist nicht beseitigt, bevor
diese Prüfungen und die SonarCloud-Neumessung beobachtet wurden. Das Audit
notierte, dass ein künstlicher, nicht normalisierter In-Memory-Action-Record
eine abgeleitete Release-URL als geändert einstufen könnte, bevor die
Same-Version-Validierung sie ablehnt. Gültige Lock-Normalisierung leitet diese
URL deterministisch ab; dies ist daher kein erreichbarer Lock-Datei-Pfad.

## Finaler Diff- und Review-Status

Die lokale Refaktor-Validierung ist bis auf die dokumentierten vollständigen
Lint- und Dokumentationslink-Infrastrukturblocker durch den nicht
materialisierten Framework-Gitlink abgeschlossen. Die maschinell verlangten
Überschriften und Identitätsfelder des Change Records wurden vor diesen
unabhängigen Link-Prüfungen akzeptiert. Er wartet auf überprüfbare Commits,
genau einen Draft-PR, einen diff-basierten Secret-Scan, gehostete GitHub
Actions und den SonarCloud-Metrik-/Blockvergleich nach dem PR. Er autorisiert
keinen Merge.
