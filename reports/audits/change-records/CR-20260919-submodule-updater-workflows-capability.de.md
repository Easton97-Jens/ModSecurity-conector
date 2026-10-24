# Change Record

**Sprache:** [English](CR-20260919-submodule-updater-workflows-capability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260919-submodule-updater-workflows-capability |
| Datum (UTC) | 2026-09-19 |
| Basis-Revision | 1bc48cd23abc3178e302108b62f68c74434b80e6 |

## Motivation und Problemstellung

GitHub-Actions-Lauf [35454150502](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35454150502)
hat einen Framework-Kandidaten validiert und scheiterte anschließend, als sein
Publisher die freigegebene statische Parent-Projektion pushte. Die Remote-Seite
lehnte `.github/workflows/test-connectors-with-crs-no-mrts.yml` ab, weil der
Publisher das ambient `github.token` verwendete, das in dieser
Repository-Konfiguration keine Workflow-Dateien aktualisieren darf.

Diese Workflow-Projektion ist erforderlich: Sie aktualisiert die geschlossenen
statischen CRS/no-MRTS-SHA-Konsumenten und ihr Test-Fixture, nachdem der
aktuelle Parent-Zustand verifiziert wurde. Ihre Entfernung würde diese
Konsumenten veralten lassen statt die Veröffentlichung zu reparieren.

## Akzeptanzkriterien

- Der Publisher besitzt keine ambient Schreibberechtigung und verwendet nur
  einen kurzlebigen, repositorybegrenzten App-Token mit genau den für seinen
  freigegebenen Wartungscommit erforderlichen Schreib-Scope `contents`,
  `pull-requests` und `workflows`.
- Resolver-, Validator- und Outcome-Jobs bleiben frei vom App-Credential und
  von Secrets.
- Die geschlossene CRS/no-MRTS-Workflow- und Test-Fixture-Projektion, ihre
  Vor- und Nachprojektionsvalidierung sowie die Ablehnung unerwarteter Pfade
  bleiben erhalten.
- Ein Fallback auf `github.token`, ein unabhängiger App-Scope, ein anderes
  Ziel-Repository oder wiederhergestellte ambient Schreibberechtigungen lassen
  den statischen Vertrag fehlschlagen.
- Fokussierte und repositoryeigene CI-Sicherheitsprüfungen bestehen lokal;
  Exact-Head-Hosted-Evidenz wird erst nach ihrer Beobachtung festgehalten.

## Implementierungsentscheidung und Begründung

`create-submodule-update-pr` besitzt nun nur `contents: read` als ambient
Job-Berechtigung. Nach dem bestehenden Trusted-Default-Branch- und erfolgreichen
Validator-Gate prüft er die bereits konfigurierten `WORKFLOW_UPDATER`-App-Eingaben
und prägt genau einen Token über die gepinnte Aktion
`actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1`.
Der Token ist auf das aktuelle Repository begrenzt und fordert exakt
`permission-contents: write`, `permission-pull-requests: write` und
`permission-workflows: write`. Nur der Publisher übergibt diesen Output als
`GH_TOKEN` an seinen bestehenden GitHub-CLI- und Git-Veröffentlichungspfad.

Die bestehende App-Konfiguration wurde nicht angelegt, rotiert, eingesehen oder
erweitert. Der historische erfolgreiche Lauf
[32544278902](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/32544278902)
hat diesen begrenzten Token bereits geprägt und Änderungen an Workflow-Dateien
veröffentlicht. Die Reparatur verwendet dieses etablierte Muster erneut, statt
dem `GITHUB_TOKEN` eine breite Workflow-Schreibberechtigung zu geben.

## Security-Auswirkung

Diese Änderung betrifft eine CI-Supply-Chain- und Veröffentlichungsgrenze. Das
schreibfähige Credential bleibt auf den Publisher begrenzt, der nur nach den
bestehenden Trusted-Resolver-/Validator-Gates erreichbar ist. Der App-Token ist
auf ein Repository und seine drei deklarierten Fähigkeiten begrenzt; Resolver,
Validator, Outcome oder Pull-Request-Code können ihn nicht erhalten. Die
registrierte Workflow-Projektion bleibt ein geschlossener, vor und nach der
Synchronisierung geprüfter Zielpfad.

Es ändern sich keine Framework- oder MRTS-Source, kein Gitlink, keine
NGINX-Ownership-Grenze, keine App-Installation, Repository-Einstellung,
Credential-Wert, Token-Secret, Quality Gate oder Branch-Protection-Regel.

Ein frischer unabhängiger Post-Patch-Security-Review fand keinen
berichtspflichtigen Bypass oder Regression in dieser Source-Grenze. Er
bestätigte den geschützten Trigger/das Gate, die Publisher-only-Credential-
Exposition, das Fehlen eines Secret-Printing-Pfads, die geschlossene Projektion
und die Vor-/Nachprojektions-Pfad-Gates. Er startete keinen Hosted-Workflow und
behauptet daher keine Live-App-Token-Enforcement.

## Geänderte Dateien

- `.github/workflows/update-submodules.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260919-submodule-updater-workflows-capability.md`
- `reports/audits/change-records/CR-20260919-submodule-updater-workflows-capability.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

- `python -m unittest -v
  tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_update_submodules_separates_validation_from_publishing
  tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_job_write_permissions_are_exactly_allowlisted`
- `python -m unittest -q tests.test_update_framework_versions`
- `python -m unittest -q tests.test_verify_framework_candidate_contract`
- `python -m unittest -q tests.test_ci_security_workflows`
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract`

Alle Befehle nutzten den ausgewählten Parent-Virtualenv-Interpreter mit
deaktivierten User-Site-Packages und ohne Installation oder Änderung von
Abhängigkeiten.

## Tests und tatsächliche Ergebnisse

- Fokussierte Publisher- und Schreibberechtigungs-Verträge aus
  `tests.test_ci_security_workflows`: bestanden (2 Tests).
- `tests.test_update_framework_versions`: bestanden (21 Tests).
- `tests.test_verify_framework_candidate_contract`: bestanden (27 Tests).
- `tests.test_ci_security_workflows`: bestanden (30 Tests).
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract`: bestanden (155 Tests, 5 erwartete
  Namespace-/Identity-Integrations-Skips).
- `git diff --check`: bestanden.

Erwartete Diagnosen aus Negativtests sind fail-closed Kontrollfälle und keine
Testfehler.

## Runtime-Evidence

Der ursprüngliche Hosted-Fehler ist Lauf
[35454150502](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35454150502),
Publisher-Job
[105926592805](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35454150502/job/105926592805).
Er erreichte die erforderliche Projektion und wurde spezifisch wegen fehlender
Workflow-Datei-Fähigkeit abgelehnt.

Zu diesem Aufzeichnungszeitpunkt wird kein aktueller Task-Hosted-Lauf, Push,
Pull Request oder Merge behauptet. Lokale Verträge können nicht beweisen, dass
die Live-App-Installation nach dem historischen erfolgreichen Lauf unverändert
ist; jedes Exact-Head-Hosted-Ergebnis muss separat beobachtet werden.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurde kein Workflow-Dispatch oder Rerun durchgeführt: Das Starten eines
GitHub-hosted Laufs ist eine externe Aktion außerhalb dieses
Source-Change-Records. Keine Runtime-Connector-Matrix ist anwendbar, weil sich
kein Connector- oder Runtime-Verhalten geändert hat.

`make check-bilingual-docs` und `make check-doc-links` wurden ausgeführt, sind
in diesem isolierten Worktree aber durch bestehende Repository-Links in das
absichtlich nicht initialisierte Submodule
`modules/ModSecurity-test-Framework` blockiert. Nachdem die anfänglichen
Pflichtüberschriften des Records korrigiert waren, meldete der
Bilingual-Checker keinen Task-Record-Fehler; jede verbleibende Meldung nannte
nur diese fehlenden Framework-Ziele. Das Initialisieren oder Ändern dieses
separaten Repositorys liegt außerhalb des Scopes.

## Bekannte Einschränkungen

Lokale Tests können die GitHub-App-Token-Prägung, die Remote-Autorisierung für
Workflow-Dateien, Branch Protection, Scheduler-Verhalten oder einen echten
zukünftigen Framework-Kandidaten nicht ausführen. Sie beweisen stattdessen die
Source-seitigen Least-Privilege- und Closed-Projection-Verträge.

## Verbleibende Risiken

Wenn die bestehende App-Installation entfernt oder ihre `Workflows`-Berechtigung
entzogen wird, scheitert der Publisher beim Token-Minting oder bei der
Veröffentlichung fail closed, statt auf `github.token` zurückzufallen. Eine
spätere Änderung am Publisher muss das Credential auf sein Trusted-Gate
begrenzen und die exakten statischen Tests erhalten.

## Finaler Diff- und Review-Status

Lokale Implementierung, fokussierte Security-Contract-Validierung,
Bilingual-Record-Struktur, eingegrenzter Diff-Review und der frische
unabhängige Security-Review sind abgeschlossen. Das Source-seitige Finding ist
behoben; autorisierte Exact-Head-PR-Delivery, Hosted-Checks, SonarQube-Cloud-
Evidenz und Live-App-Token-Enforcement stehen noch aus. Kein Merge ist
autorisiert oder behauptet.
