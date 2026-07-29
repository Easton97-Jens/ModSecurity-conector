# Change Record: Parent-CI-Apache-Config-Reference-Condition-Remediation

**Sprache:** [English](CR-20260729-sonar-ci-apache-config-reference-condition.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-apache-config-reference-condition` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` |
| Bewertete Source-Revision | Lokaler Task-Patch gegen die genannte Basis-Revision |
| Grenze | Ausschließlich Parent `ci/checks/documentation/connector_config_reference.py`, sein direkter Parent-Regressionstest, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine `scripts/`, kein Framework, kein MRTS, kein Gitlink, kein generierter Configuration-Reference-Output, keine SonarQube-Cloud-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression, keine Default-Branch- oder Merge-Aktion sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Behebt die aktuelle `python:S3358`-verschachtelte Bedingung beim Apache-Directive-Example-File-Selector. Keine Scanner-Kontrolle wird geändert. |

## Motivation und Problemstellung

Das Parent-CI-Configuration-Reference-Inventar wählte die Apache-Example-File
über eine verschachtelte Bedingung. SonarQube Cloud meldet dieses Konstrukt
unter `python:S3358`. Obwohl die drei Ergebnisse einfach sind, gehören sie zur
source-backed Configuration Reference: Eine Verschiebung ihrer Partition könnte
eine Directive auf ein falsches Konfigurationsbeispiel zeigen lassen, ohne ihre
Parser-Registrierung zu ändern.

Das erforderliche Verhalten hat drei exakte Fälle: eine Source-File-Directive,
drei Minimal-Configuration-Directives und alle verbleibenden registrierten
Apache-Directives mit dem Safe-Configuration-Example.

## Akzeptanzkriterien

- Die verschachtelte Bedingung wird durch einen expliziten Safe-Default und
  zwei klar benannte Ausnahme-Branches ersetzt.
- `modsecurity_phase4_content_types_file` referenziert weiterhin
  `connectors/apache/src/msc_config.c`.
- Nur `modsecurity`, `modsecurity_rules_file` und
  `modsecurity_use_error_log` referenzieren `examples/apache/minimal/httpd.conf`.
- Jede andere extrahierte Apache-Directive referenziert weiterhin
  `examples/apache/safe/httpd.conf`.
- Der fokussierte Test, nicht schreibende Generator-/Checker-Controls, Syntax,
  Whitespace, bilinguale Dokumentation, Security-Review und ein exakter
  Draft-PR-Head liefern die aufgezeichnete Evidence. Hosted SonarQube Cloud
  muss null neue Issues, null neue Duplikatzeilen und `0.0%` New-Code-
  Duplizierung ohne Abschwächung von Scanner-Kontrollen zeigen.

## Implementierungsentscheidung und Begründung

Der Selector startet nun beim Safe-Apache-Example und überschreibt ihn nur für
die Source-File-Directive und das explizite Minimal-Example-Directive-Set.
Dies ist klarer als eine Bedingung in eine andere zu verschachteln und behält
gleichzeitig für alle registrierten Directives dieselbe Priorität und dieselben
Output-Bytes bei.

Der fokussierte Regressionstest leitet seine Zuordnung von `extract_apache()`
ab und prüft alle drei Partitionen. Er verhindert, dass eine künftige
Directive-Ergänzung stillschweigend eine unerwartete Example-File-Kategorie
erbt.

## Geänderte Dateien

- `ci/checks/documentation/connector_config_reference.py`
- `tests/test_connector_config_reference.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-apache-config-reference-condition.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-apache-config-reference-condition.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> <repository-venv-python> -m unittest -v tests.test_connector_config_reference` | bestanden: 1 fokussierter Mapping-Test. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make check-connector-config-reference` | bestanden: Der nicht schreibende Generator meldete 21 aktuelle generierte Dateien; der Reference-Checker meldete `apache=14, nginx=18, haproxy=41, envoy=141, traefik=71, lighttpd=19, common=25, engine=12`. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> <repository-venv-python> -m py_compile ci/checks/documentation/connector_config_reference.py tests/test_connector_config_reference.py` | bestanden. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> find ci/checks/documentation -type f -name '*.py' -exec <repository-venv-python> -P -m py_compile {} +` | bestanden: der vollständige ausgewählte `ci/checks/documentation/`-Python-Syntax-Scope. |
| `git -C <task-worktree> diff --check` | für den aktuell getrackten Source- und Index-Patch bestanden. Der finale Staged-All-File-Whitespace-Check bleibt für den ungetrackten Regressionstest und das Change-Record-Paar erforderlich. |
| `git -C <task-worktree> diff --cached --check` | für die exakten sechs task-eigenen gestageten Source-, Test-, Change-Record- und Index-Dateien bestanden. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make check-bilingual-docs` | `blocked_external_dependency`: Kein Fehler benennt dieses Change-Record-Paar; jeder gemeldete fehlende Link ist ein bestehendes Target unter dem absichtlich fehlenden Framework-Submodul. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make check-doc-links` | `blocked_external_dependency`: Jedes gemeldete Target ist eine bestehende Referenz unter dem absichtlich fehlenden Framework-Submodul; kein neues Change-Record-Target wird gemeldet. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make lint` | `blocked_external_dependency`: Parent-Shell-Syntax und CI-Python-Kompilierung liefen, danach konnte ein bestehender No-CRS-Check das absichtlich fehlende Framework `ci/checks/catalog/no_crs_baseline.py` nicht importieren. |
| Unabhängiger scoped Security-/Diff-Review | bestanden: kein plausibler reportbarer diff-induzierter Security-Kandidat; der Review verfolgte die vollständige Source-/Minimal-/Safe-Zuordnung, unmittelbare Renderer-/Checker-Consumer und den direkten Regressionstest. |

## Security-Auswirkung

Der geänderte Code liest repository-eigene Apache-Registrierungsdaten und
weist einen Documentation-Example-Pfad zu; er öffnet keine Datei und ändert
weder Parser, Kommando, Netzwerk, Credential noch einen Runtime-Request-Pfad.
Die relevante Invariante lautet, dass jede registrierte Apache-Directive ihre
exakte Source-/Minimal-/Safe-Example-File-Kategorie behält. Der fokussierte
Test übt die Ausnahme-Kategorien und die komplementäre Safe-Default-Kategorie
aus.

Der fokussierte Security-Preflight und der unabhängige finale scoped Source-/
Test-Diff-Review fanden kein plausibles reportbares Problem. Diese Maintenance-
Remediation beansprucht keinen Runtime-Security-Fix.

## Runtime-Evidence

Es wird keine Connector-Runtime, kein Netzwerk-Host und kein schreibender
Configuration-Reference-Generator-Lauf beansprucht. Der nicht schreibende
Generator-/Checker validiert das Repository-Inventar und der direkte Unit-Test
validiert die vollständige Apache-Mapping-Partition. Dies ist ausschließlich
Source-Level-Evidence.

## Bekannte Einschränkungen

Der Task-Worktree enthält absichtlich kein populiertes Framework-Submodul,
weshalb breite Targets, die Framework-Checks importieren, lokal nicht
vollständig laufen können. Dies betrifft weder den fokussierten Parent-Mapping-
Test noch die nicht schreibenden Configuration-Reference-Controls, begrenzt
aber die lokale Broad-Lint-Evidence.

## Verbleibende Risiken

Die expliziten Source-Branches bewahren die ausgewählte Output-Zuordnung lokal,
doch das finale Ergebnis ist noch nicht auf einem exakten Hosted-Draft-PR-Head
verifiziert. Jedes Verhalten außerhalb dieses Parent-CI-Extractors,
einschließlich generiertem Output und Connector-Runtime-Konfigurationsparsing,
bleibt unverändert und wird durch diesen Record nicht beansprucht.

## Nicht ausgeführte Prüfungen mit Begründung

- Die breite Connector-Runtime-Suite und `make test` führen Framework-eigene
  Provisioning- und Runtime-Pfade aus, die in diesem absichtlich nicht
  populierten Worktree nicht verfügbar und außerhalb des Scopes dieses nicht
  schreibenden CI-Selectors sind.
- Die vollständige Connector-Runtime-Matrix, schreibende Generated-Output-
Läufe und Netzwerk-Host-Checks sind für diesen nicht schreibenden CI-
Inventory-Selector außerhalb des Scopes.
- Hosted GitHub Actions, SonarQube-Cloud-PR-Analyse, Review, Freigabe, Merge
  und Master-Verifikation sind für den finalen Change-Record-Follow-up-Head
  noch nicht beobachtet und werden nicht lokal hergeleitet.

## Finaler Diff- und Review-Status

Der Source-Patch, der fokussierte direkte Mapping-Test, die ausgewählte Syntax-
Kompilierung, der Whitespace-Check für den getrackten Patch und die nativen
nicht schreibenden Configuration-Reference-Controls bestanden. Der finale
Staged-All-File-Whitespace-Check bestand für den vollständigen task-eigenen
Sechs-Dateien-Diff. Die beiden breiten Dokumentations-Targets und das breite
Lint-Target sind nur durch das absichtlich fehlende Framework-Submodul blockiert
und enthalten keinen Fehler für dieses Record-Paar. Die finale Security-Review
fand keinen plausiblen reportbaren diff-induzierten Kandidaten. Exact-Head-
Hosted- und SonarQube-Cloud-Evidence wird erst nach ihrer Beobachtung ergänzt.
Dieser initiale Record beansprucht keinen Commit, Push, Pull Request, Hosted-
Check, Review, Freigabe, Merge oder `master`-Änderung im initialen Source-
Record.

Delivery-Update: [Draft PR #191](https://github.com/Easton97-Jens/ModSecurity-conector/pull/191)
wurde am `2026-07-29T23:51:01Z` gegen `master` vom Branch
`agent/parent-ci-apache-config-reference-condition-20260729` geöffnet. Bei
Erstellung lösten lokaler Branch, Remote-Branch und PR-Head jeweils zu
`6ccdcbd096dd9a865cfdf8e23ce712606b919a51` auf. Dieses Update zeichnet nur den
beobachteten Draft-PR-Fakt auf; es beansprucht keinen Hosted-Check, kein
SonarQube-Cloud-Ergebnis, kein Review, keine Freigabe, keinen Merge und keine
`master`-Änderung. Nach dem Push dieses Delivery-Follow-ups ist eine frische
Exact-Head-Verifikation erforderlich.
