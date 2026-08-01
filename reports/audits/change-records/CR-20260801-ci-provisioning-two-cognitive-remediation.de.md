# Change Record: Finale Cognitive-Complexity-Remediation für Parent-CI-Provisioning

**Sprache:** [English](CR-20260801-ci-provisioning-two-cognitive-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-ci-provisioning-two-cognitive-remediation` |
| Datum (UTC) | `2026-08-01` |
| Basis-Revision | `6dc912643133e5c7d3c305979d4052da9cb45153` |
| Tracking | `FND-SONAR-0030`; `AZ9cRyj3HhV2CayPTPzB`; `AZ9cRyj3HhV2CayPTPzC` |
| Grenze | Parent `ci/provisioning` und ein direkter Parent-Cache-Contract-Test; Framework, MRTS, Gitlinks, `.github`, SonarQube-Cloud-Einstellungen, Abhängigkeiten und `master` bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Analyse von `master` enthält zwei verbleibende
`python:S3776`-Maintainability-Zeilen in
`ci/provisioning/components/prepare-runtime-components.py`:
`prepare_apache_httpd()` und `prepare_nginx_runtime()` haben jeweils kognitive
Komplexität 16, obwohl 15 erlaubt ist. Das angefragte Verzeichnis hat null
Security-, null Reliability- und null Duplikatzeilen-Befunde.

## Akzeptanzkriterien

- Die beiden exakten Zeilen erhalten eine verhaltenserhaltende Source-
  Remediation ohne `NOSONAR`, Suppression, Exclusion, Regel-, Quality-Gate-
  oder Threshold-Änderung.
- Keyed Apache- und NGINX-Pläne verwenden weiter validiertes transaktionales
  Staging; unkeyed Pläne bleiben direkt.
- Bestehende Cache-, Provenance-, Containment-, Command-Construction-,
  Publication-, Record- und Failure-Semantik bleibt unverändert.
- Fokussierte Tests und anwendbare lokale Checks bestehen; Exact-Head-GitHub-
  Actions und SonarQube-Cloud-Analyse bleiben für `verified_pr` erforderlich.

## Implementierungsentscheidung und Begründung

`prepare_connector_with_optional_staging()` besitzt nun die bereits gemeinsame
Entscheidung: Ein keyed nichttransaktionaler Plan nimmt den bestehenden
`prepare_connector_transactionally()`-Pfad, während ein unkeyed oder bereits
gestagter Plan seinen Prepare-Callback direkt aufruft. Die öffentlichen Apache-
und NGINX-Einstiegspunkte delegieren an private Per-Plan-Implementierungen,
deren bisheriger Body und Kontrollfluss-Reihenfolge erhalten bleiben. Zwei
direkte Tests beweisen direkte/unkeyed und transaktionale/keyed Delegation;
bestehende Apache- und NGINX-Cache-Contract-Tests üben weiterhin tatsächliches
Staging und Publication aus.

## Security-Auswirkung

Der Source ist sicherheitsrelevant, weil er Cache-Pfade, Downloads, Provenance,
Publication und subprocess-nahe Daten verarbeitet. Die bewahrte Invariante
lautet: Keyed Connector-Pläne bleiben im bestehenden validierten Managed-Root-
Staging-/Publication-Control, während unkeyed Pläne direkt bleiben. Der
fokussierte Source-/Control-Review fand keine plausible diff-induzierte
Security-Regression und keinen reportierbaren Security-Befund. Er ist kein
vollständiger Repository-Security-Scan und kein Runtime-Build-Ergebnis.

## Geänderte Dateien

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- Dieses englische/deutsche Change-Record-Paar.

## Tests und tatsächliche Ergebnisse

| Befehl | Ergebnis |
| --- | --- |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/provisioning/components/prepare-runtime-components.py tests/test_runtime_component_cache_contract.py` | bestanden |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_runtime_component_cache_contract` | bestanden: 34 Tests |
| `git diff --check` | bestanden |
| Initiale Exact-Head-SonarQube-Cloud-Analyse für PR #226 | Quality Gate `OK` und null New-Code-Duplikation, aber fünf task-eigene `python:S3415`-Assertion-Order-Zeilen wurden im Follow-up korrigiert |
| Finale Exact-Head-Hosted-Runde von PR #226 für `c19defa183e133cfa64853e9bfe62569237c450d` | bestanden: SonarQube-Cloud-Quality-Gate `OK`, null New Issues, null New-Code-Duplikation und alle abgeschlossenen GitHub-Actions-Checks bestanden |

Der ausgewählte Interpreter ist `/root/git/ModSecurity-conector/.venv/bin/python`
(Python `3.14.4`) mit `PYTHONNOUSERSITE=1`,
`PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1` und
`PYTHONDONTWRITEBYTECODE=1`. Test-Temporary-State liegt in task-eigenem
externem Storage.

## Ausgeführte Befehle

Die Befehle und Ergebnisse in der vorstehenden Tabelle bilden den vollständigen
lokalen Ausführungsnachweis. Auch `make check-no-crs-source-normalization` und
`make check-bilingual-docs` wurden ausgeführt; ihre exakten blockierten
beziehungsweise Remediation-Zustände stehen unter **Nicht ausgeführte
Prüfungen mit Begründung** und im Task-Plan. Der initiale Record entstand vor
der Delivery; PR #226 wurde danach committed, gepusht und verifiziert. Weder
ein Build noch eine Dependency-Installation liefen, und es gab keinen Merge.

## Runtime-Evidence

Die bestehende Suite übt Apache-Keyed-Staging, NGINX-Rebuilds bei einem
marker-eigenen Partial-Root, Sichtbarkeit atomarer Publication, Ablehnung von
Managed-Root-Löschung, Digest-vor-Publication und die neuen direkten/unkeyed
sowie keyed/staged Delegation-Controls aus. Kein Third-Party-Download und kein
nativer Connector-Build lief.

## Nicht ausgeführte Prüfungen mit Begründung

- `make check-no-crs-source-normalization` wurde versucht, aber während der
  Collection blockiert: Der isolierte Parent-Worktree enthält absichtlich nicht
  die Framework-Submodule-Datei
  `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`.
  Framework zu initialisieren oder zu ändern liegt außerhalb dieses Parent-only
  Tasks.
- `make check-bilingual-docs` und `make check-doc-links` erreichten beide den
  neuen Change Record erfolgreich, werden jedoch von denselben absichtlich
  fehlenden Framework-Targets blockiert, auf die bereits vorhandene Repository-
  Dokumente verweisen. Kein task-eigener Dokumentationslink schlug fehl.
- `make check-runtime-path-policy` wurde mit dem ausgewählten Parent-
  Interpreter versucht und ist blockiert, weil sein Shell-Control dasselbe
  fehlende `modules/ModSecurity-test-Framework/ci/lib/common.sh` importiert;
  es übte keinen geänderten Runtime-Path-Control aus.
- Ein echter Runtime-Component-Provision/Build lief nicht, weil er Third-Party-
  Komponenten herunterlädt und kompiliert; das geht über diese strukturelle
  Remediation hinaus.
- Ruff und Pyright liefen nicht, weil die ausgewählte Parent-virtuelle Umgebung
  keines der beiden Tools enthält; kein Paket- oder Dependency-Contract änderte
  sich.
- Exact-Head-GitHub-Actions und SonarQube-Cloud-Analyse bestanden für den
  aktuellen Source-Head vor diesem reinen Record-Follow-up.

## Bekannte Einschränkungen

Die finale Hosted-Runde beweist den vorherigen PR-Head, kann aber nicht den
resultierenden `master`-Zustand beweisen. Der aktuelle Nutzer hat Parent-PR
#226 nun ausdrücklich für die Integration in `master` autorisiert ("bringe das
pr 226 in den master"). Das aktive Ruleset erlaubt die etablierte normale
`merge`-Methode, verlangt kein Approval, aber aufgelöste Review-Threads und
sechs benannte Checks. Dieser reine Record-Follow-up muss vor dem geschützten
Merge selbst eine frische Exact-Head-Verifikation abschließen; danach bleibt
die Resulting-`master`-Prüfung erforderlich.

## Verbleibende Risiken

Der weitere repositoryweite SonarQube-Cloud-Backlog ist außerhalb des Scopes.
Diese Source-Änderung autorisiert nicht selbstständig eine `master`-
Integration; die aktuelle Nutzerautorisierung ist auf PR #226 in Parent
`master` begrenzt und erteilt weder einen direkten Default-Branch-Write noch
eine Framework-/MRTS- oder Gitlink-Aktion.

## Finaler Diff- und Review-Status

Draft-PR #226 ist gegen `master` offen; sein zuletzt verifizierter Source-Head
ist `b08bc69278570a02af5c0367bffb2dea47d37d7c`. Er hat einen sauberen Merge-
Status, kein erforderliches Approval und keine Review-Threads. Alle
abgeschlossenen Checks und das SonarQube-Cloud-Quality-Gate bestanden für
diesen exakten Head. Dieser reine Record-Follow-up erfasst die aktuelle
Nutzerautorisierung, Parent-Ownership, keine Cross-Repository-Abhängigkeit und
normalen `merge` als ausgewählte erlaubte Methode. Seine frische Exact-Head-
CI-/Sonar-Runde ist vor dem Exact-Head-geschützten Merge erforderlich. Bei
dieser Record-Revision erfolgten kein Merge, Release, direkter `master`-Push,
Bypass oder Branch-Cleanup.
