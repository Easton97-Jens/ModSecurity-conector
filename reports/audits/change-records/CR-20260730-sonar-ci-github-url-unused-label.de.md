# Change Record: Parent-CI-Bereinigung der GitHub-URL-Validierung und Test-Bootstrap-Guard für SonarQube Cloud S1172/S9073

**Sprache:** [English](CR-20260730-sonar-ci-github-url-unused-label.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260730-sonar-ci-github-url-unused-label |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f |
| Tracking | Parent-SonarQube-Cloud-`python:S1172`-Code-Smell `AZ9cRyj3HhV2CayPTPyt` in `ci/provisioning/components/prepare-runtime-components.py:245` sowie PR-#198-Follow-up-`python:S9073`-Code-Smell `AZ-zgsKSuhGCH8wggCxz` in `tests/test_prepare_runtime_components.py:22`. |
| Grenze | Parent-CI-URL-Konfigurationsvalidierung und Dynamic-Import-Bootstrap des Testmoduls, direkte Parent-Tests, dieses englisch/deutsche Change-Record-Paar und die gepaarten Indizes. Framework, MRTS, Gitlinks, Connector-Source, SonarQube-Cloud-Konfiguration, Quality Gates, Exclusions, Suppressions und `master` bleiben unverändert. |

## Motivation und Problemstellung

SonarQube Cloud meldet, dass `label` von
`require_https_github_repo_url(url, label)` nicht benutzt wird. Der Helper
liegt an einer Source-URL-Validierungsgrenze; diese Änderung entfernt nur
diesen ungenutzten Signaturwert und sein einziges Caller-Argument, ohne das
bestehende Validierungsverhalten zu verändern.

Nach der anfänglichen exakten PR-#198-Analyse meldete SonarQube Cloud außerdem
den offenen MAJOR-Code-Smell `python:S9073` an der zusammengesetzten Dynamic-
Import-Assert-Anweisung des Testmoduls. Das PR-Quality-Gate war `OK`, aber das
task-eigene Issue wird nicht von der separaten akzeptierten, nur master-
bezogenen FND-SONAR-0001-Signatur abgedeckt. Der Test-Bootstrap benötigt daher
einen expliziten Importfehler-Guard, der unter Python-Optimierung wirksam bleibt.

## Akzeptanzkriterien

- Nur den ungenutzten Parameter `label` und sein direktes Caller-Argument entfernen.
- Die Validierung von `github_repo_path()` bewahren: exaktes HTTPS, exaktes
  `github.com`, keine Query oder Fragment und genau ein Owner/Repository-Paar.
- Das Blocked-Verhalten vor Cache-/Build-Setup für ungültige konfigurierte
  GitHub-URLs bewahren und direkte Canonical-Acceptance- und Rejection-Coverage ergänzen.
- Nur die zusammengesetzte Dynamic-Import-Assert-Anweisung durch einen
  expliziten `ImportError`-Guard für eine nicht verfügbare Modulspezifikation
  oder einen nicht verfügbaren Loader ersetzen.
- Gültige dynamische Modulerzeugung und genau-einmalige Ausführung in normalem
  Python und unter `Python -O` bewahren.
- Ein gleichwertiges englisch/deutsches Change-Record-Paar und gepaarte Indizes pflegen.
- Keinen Baseline-SonarQube-Cloud-Issue vor einer exakten PR-Head-Analyse als geschlossen behaupten.

## Implementierungsentscheidung und Begründung

`require_https_github_repo_url()` akzeptiert jetzt nur `url`; `label` wurde vom
Helper nicht gelesen, sein Rückgabewert vom einzigen Caller verworfen und es
kam in keiner Validierungsfehlermeldung vor. Der neue direkte Test bewahrt die
Canonicalisierung einer HTTPS-GitHub-URL mit `.git`-Suffix und verwirft über den
Konfigurations-Caller Nicht-HTTPS-, falsche Host-, Host-Port-, Query-,
Fragment-, unvollständige und überlange Repository-Formen.

Das Testmodul verwendet nun einen expliziten Guard
`if SPEC is None or SPEC.loader is None`, der vor der unveränderten
`module_from_spec()`-/`exec_module()`-Sequenz `ImportError` auslöst. Dies ist
eine reine Test-Bootstrap-Reparatur: Sie ändert weder den Produkt-Helper noch
die GitHub-URL-Validierungsgrenze.

## Geänderte Dateien

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Fokussierte Kommandos nutzen den ausgewählten Parent-`.venv`-Python mit
`PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`,
`PIP_DISABLE_PIP_VERSION_CHECK=1`, `PYTHONDONTWRITEBYTECODE=1` und
task-owned externen `TMPDIR`-/Bytecode-Pfaden:

- `rtk proxy -- <Parent .venv python> -m pip check`
- `rtk proxy -- <Parent .venv python> -m py_compile ci/provisioning/components/prepare-runtime-components.py tests/test_prepare_runtime_components.py`
- `rtk proxy -- <Parent .venv python> -m unittest -v tests.test_prepare_runtime_components.PrepareRuntimeComponentsTest.test_github_repo_url_config_preserves_canonical_and_rejection_policy tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_clean_managed_git_checkout_is_reused_across_target_preparations`
- `rtk proxy -- <Parent .venv python> -m unittest -v tests.test_prepare_runtime_components`
- `rtk proxy -- <Parent .venv python> -O -m unittest -v tests.test_prepare_runtime_components`
- `rtk proxy -- <Parent .venv python> -c <controlled invalid-SPEC import rejection>`
- `rtk proxy -- <Parent .venv python> -O -c <controlled invalid-SPEC import rejection>`
- `rtk proxy -- <Parent .venv python> -m unittest -v tests.test_bilingual_docs`
- `rtk proxy -- <Parent .venv python> -c <direct Change Record pair validation>`
- `rtk proxy -- make check-bilingual-docs`
- `rtk proxy -- make check-doc-links`
- `rtk proxy -- git diff --check`

## Tests und tatsächliche Ergebnisse

- Auswahl der Parent-Python-Umgebung und `pip check` bestanden; der Interpreter ist Python `3.14.4` in der Parent-Virtual-Environment.
- Python-Syntaxkompilierung für die geänderten Source- und Testdateien bestanden.
- Der neue URL-Validator-Contract-Test bestand und deckt gültige Canonicalisierung sowie sieben verworfene Konfigurationsformen ab.
- Der bestehende Managed-Checkout-Reuse-Control bestand mit einer kanonischen GitHub-URL und einem kontrollierten lokalen Clone.
- Das vollständige Modul `tests.test_prepare_runtime_components` bestand im
  lokalen Remediation-Worktree normal mit 29/29 Tests und unter `Python -O`
  ebenfalls mit 29/29 Tests, wenn der bestehende read-only Framework-Testroot
  bereitgestellt wurde; es wurde keine Framework-Initialisierung oder kein
  Fallback verwendet.
- Der direkte Change-Record-Paar-Vertrag bestand ohne Fehler, und
  `tests.test_bilingual_docs` bestand auf dem anfänglichen synchronisierten
  PR-Head mit 22 Tests.
- `make check-bilingual-docs` ist ausschließlich durch 20 vorhandene fehlende
  Framework-Gitlink-Linkziele `blocked_environment`; kein gemeldeter Fehler
  nennt dieses Paar oder seine Indizes. `make check-doc-links` ist durch die
  entsprechenden 16 vorhandenen fehlenden Framework-Gitlink-Linkziele blockiert.
- `git diff --check` bestand nach den Source-, Test- und Dokumentationsänderungen.
- Der explizite Guard-Invalid-SPEC-Control bestand in normalem Python und
  unter `Python -O`: Er monkeypatchte die Spec-Erzeugung auf `None` und
  beobachtete vor der Modulinitialisierung ausschließlich den exakten
  `ImportError`.

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet für die URL-Signaturänderung
`already_safe` und für den Test-Bootstrap-Guard
`not_security_relevant_maintainability_only`. Aus der Umgebung stammende GitHub-URLs bleiben kontrollierter
Input; `github_repo_path()` erzwingt weiterhin die
HTTPS-/Exact-Host-/Plain-Owner-Repository-Policy vor jedem Cache-, Build-, Git-
oder Network-Sink. Ungültige Konfigurationen lösen weiterhin `RuntimeError`
aus und folgen dem bestehenden Blocked-Pfad. Es wird kein Sicherheitsbefund als
behoben behauptet.

## Dokumentationsstatus

Dieser Record und sein deutsches Pendant beschreiben dieselbe Source-Grenze,
Tests, Einschränkungen und Delivery-Grenze. Die gepaarten Record-Index-Einträge
liefern die Traceability. Der direkte Paar-Vertrag und die bilinguale
Unit-Suite bestehen; vollständige Repository-Dokumentationsprüfungen sind nur
durch bestehende fehlende Framework-Gitlink-Ziele blockiert, nicht durch diesen
Record oder seine Indizes.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll- oder Produktions-Runtime-Verhalten
geändert oder behauptet. Die fokussierten Unit-Controls prüfen die
CI-Konfigurationsgrenze; sie sind keine Connector-Runtime-Evidence.

## Bekannte Einschränkungen

Dieser Kandidat bearbeitet eine offene Parent-`ci/`-SonarQube-Cloud-Zeile aus
der aktuellen 304-Item-CI-Inventur und einen PR-lokalen Test-Bootstrap-Code-
Smell. Beide Zeilen bleiben offen, bis SonarQube Cloud den finalen exakten
gelieferten PR-Head analysiert; das PR-lokale `python:S9073` blockiert bis
dahin die Merge-Betrachtung.

## Verbleibende Risiken

Eine versehentlich übersehene Call Site könnte zukünftige URL-Validierung
fehlschlagen lassen. Das aktuelle Parent-Call-Inventar fand einen Caller; der
direkte Konfigurationstest und der bestehende Managed-Checkout-Control üben
sowohl die Validierung als auch den nachgelagerten kanonischen URL-Pfad aus.
Diese Änderung trifft keine Aussage über nicht verwandte Sonar-Befunde oder
Scanner-Vulnerability-Leads.

## Nicht ausgeführte Prüfungen mit Begründung

- Das exakte lokale Remediation-Testmodul bestand nur mit explizit ausgewähltem
  bestehendem read-only Framework-Testroot; dem isolierten Worktree fehlen weiterhin unveränderte
  Framework-Linkziele für breitere Dokumentationskommandos. C11 initialisiert
  oder verändert diese Grenze nicht.
- Gehostete GitHub Actions, SonarQube-Cloud-Kandidaten-Head-Analyse, Commit,
  Push und Draft-PR-Erstellung sind zum Zeitpunkt der Record-Erstellung nicht
  erfolgt und werden nicht behauptet.
- Connector-Builds, Host-Konfigurationsprüfungen, Runtime-Smokes, Protokollmatrizen, Framework-Checks und MRTS-Checks sind nicht anwendbar, da keine Connector-/Runtime-Implementierung oder Cross-Repository-Inhalte geändert werden.

## Finaler Diff- und Review-Status

Die abgegrenzte Implementierung entfernt nur den ungenutzten Signaturparameter
und das passende Caller-Argument, ergänzt direkte URL-Policy-Preservation-
Coverage und ersetzt die zusammengesetzte Test-Bootstrap-Assert-Anweisung durch
einen expliziten `ImportError`-Guard. Delivery- und finale Exact-Head-Hosted-
Evidence werden absichtlich erst nach ihrem Eintreten erfasst; kein `master`-
Merge wird durch diesen Change Record autorisiert.
