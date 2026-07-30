# Change Record: Parent-CI-NGINX-HTTP-500-Literal-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-ci-nginx-http500-literal-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-nginx-http500-literal-deduplication` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `fda62539b6f0a710865707e3003b73ed4469f20e` |
| Bewertete Source-Revision | Lokaler Task-Patch gegen die genannte Basis-Revision. |
| Grenze | Nur die unten genannte Parent-`ci`-Source, ein direkter Parent-Test, dieses EN/DE-Paar und gepaarte Indizes. Keine `.github`-, `scripts`-, Framework-, MRTS-, Gitlink-, Scanner-Konfigurations-, Quality-Gate-, Exclusion-, Suppression- oder Default-Branch-Aktion. |
| SonarQube-Cloud-Verknüpfung | Zielt auf die aktuellen `python:S1192`-Literalbefunde `AZ7PU4lam6NRVhQ0A9r2` und `AZ7PU4lam6NRVhQ0A9r3` für `"htdocs/index.html"` und `"Permission denied"`; keine Scanner-Kontrolle und kein Issue-Status wird geändert. |

## Motivation und Problemstellung

Der NGINX-MRTS-HTTP-500-Clusterreport verwendete dieselben zwei festen
Error-Log-Literale in Error-Classification, Representative-Excerpt-Auswahl,
einem Permission-Probe-Pfad und Report-Evidence-Text. SonarQube Cloud meldet
die wiederholten Source-Literale als `python:S1192`; diese Verwendungen liegen
neben Classification- und Evidence-Path-Verhalten, das unverändert bleiben
muss.

## Implementierungsentscheidung und Begründung

`DOCROOT_INDEX_PATH` besitzt den festen relativen Pfad `htdocs/index.html` und
`PERMISSION_DENIED_TEXT` besitzt das exakte case-sensitive NGINX-Log-Token.
Alle ausgewählten Verbraucher verwenden diese Konstanten, ohne Bedingungen,
Reihenfolge oder Output-Text zu verändern.

`ERROR_PERMISSION_DENIED` bleibt bewusst getrennt: Es ist eine lower-case
Diagnosephrase mit anderer Semantik als der case-sensitive Log-Marker. Der
Refaktor verändert weder die Verified-Run-ID-Validierung noch Evidence-Input-
Auswahl, Safe-Root-Setup, Output-Writes oder das bestehende Permission-Probe-
Stat-Verhalten.

## Akzeptanzkriterien

- Index-Datei-, Directory-, Critical- und Generic-Failure-Classifications
  behalten ihre bisherige Priorität und exakten Literale.
- Representative Excerpts behalten Final-Run-Date-Filter, Auswahlreihenfolge
  und 600-Zeichen-Kürzung.
- `Path / DOCROOT_INDEX_PATH` bleibt im Permission Probe dasselbe relative
  Ziel `htdocs`/`index.html`.
- Der exakte künftige PR-Head muss null neue SonarQube-Cloud-Issues und `0.0%`
  New-Code-Duplizierung ohne Änderung von Scanner-Policy oder Controls zeigen.

## Geänderte Dateien

- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `tests/test_nginx_mrts_http500_cluster_analysis.py`
- dieses englisch/deutsche Change-Record-Paar und seine Indizes

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| Fokussierte NGINX-HTTP-500-Cluster-Analysis-Testsuite | bestanden: 3 Tests für Classification-Priorität, Ordinary-File-Negativ-Control, Final-Run-Date-Filter, Excerpt-Kürzung und Permission-Probe-Pfadkomponenten. |
| Selected-File-`py_compile` mit task-eigenem Bytecode-Cache | bestanden. |
| `git diff --check` | bestanden. |
| Unabhängige finale Source- und Test-Security-Diff-Reviews | bestanden: kein plausibler diff-eingeführter Sicherheitskandidat. |
| `make check-bilingual-docs` | `blocked_external_dependency`: Der Checker meldete nur bestehende fehlende Framework-Submodul-Link-Targets und keinen Fehler im geänderten Change Record oder Index. |

## Security-Auswirkung

Der Generator erhält CI-Evidence-Zeilen und Error-Log-Pfade und schreibt dann
generierte Evidence-Reports über bestehende Safe-Root-Controls. Die Konstanten
sind source-authored feste Daten, keine externen Eingaben. Der bestehende
`validate_verified_run_id()`-Check, das `add_safe_roots()`-Setup und die
`write_text_file()`-Output-Path-Control bleiben unverändert. Es entsteht kein
neuer Filesystem-, Netzwerk-, Subprocess-, Deserialisierungs- oder
Autorisierungspfad.

## Runtime-Evidence

Keine Connector-Runtime, keine NGINX-/MRTS-Ausführung, keine netzwerkgestützte
Vorbereitung und kein Report-Generator-`main()` liefen. Der fokussierte Test
verwendet ein privates temporäres Dateisystem und schreibt keine Repository-
Reports. Hosted-GitHub-Actions, SonarQube Cloud, Review, Freigabe, Merge und
Master-Verifikation sind noch nicht beobachtet oder beansprucht.

## Bekannte Einschränkungen

Der isolierte Worktree enthält nicht die Framework-Submodul-Targets, die
bestehende Repository-Dokumentation referenziert; deshalb kann der
repositoryweite Dokumentationscheck extern blockiert sein. Dieses Record
beansprucht nicht, dass der breitere Parent-`ci`-Backlog erschöpft ist.

## Verbleibende Risiken

Der Report-Generator behält seine bestehenden Annahmen über Evidence-Zeilen-
und Case-Metadata-Provenance. Diese Literal-only-Änderung belegt weder ein
vollständiges Connector-Runtime-, Hosted-Quality-Gate- noch Resulting-Master-
Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine Connector-Runtime, kein Report-Generator-`main()` und keine
  netzwerkgestützte Vorbereitung liefen, weil der Refaktor feste
  Source-Literale besitzt und der fokussierte Test das betroffene Verhalten
  ohne generierte Runtime-Evidence übt.
- Hosted-GitHub-Actions, SonarQube Cloud, Review, Freigabe, Merge und
  Master-Checks sind für den exakten aktuellen PR-Head noch nicht
  abgeschlossen.

## Delivery-Status

Der initiale Source-und-Traceability-Commit
`1bec752c45176f131a3eaf1d5f5ce854c28f9bae` wurde auf
`agent/parent-ci-nginx-mrts-http500-literals-20260729` gepusht, und Draft PR
[#187](https://github.com/Easton97-Jens/ModSecurity-conector/pull/187) wurde
gegen `master` eröffnet. Bei der initialen PR-Erstellung stimmten lokaler,
Remote- und PR-Head auf diesen Commit überein. Dieser Delivery-Metadaten-
Follow-up ändert nur Dokumentation; deshalb muss der exakte finale PR-Head
weiterhin frische Hosted-Checks und SonarQube-Cloud-Resultate erhalten. Keine
direkte Master-Änderung oder kein Merge ist autorisiert oder impliziert.

## Finaler Diff- und Review-Status

Der lokale Source-/Test-Diff bestand fokussierte Tests, ausgewählte
Kompilierung, Whitespace-Validierung und unabhängige Source-/Test-Security-
Diff-Reviews ohne plausiblen diff-eingeführten Kandidaten. Draft PR #187
existiert, aber die finale Exact-PR-Head-Hosted-Verifikation steht aus.
