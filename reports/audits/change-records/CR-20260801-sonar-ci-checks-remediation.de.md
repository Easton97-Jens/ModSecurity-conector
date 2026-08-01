# Änderungsnachweis: Parent-CI-Checks-SonarQube-Cloud-Bereinigung

**Sprache:** [English](CR-20260801-sonar-ci-checks-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-ci-checks-remediation` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `3ff87de53df34cecbc9c6489c858e64bdf3fd198` |
| Tracking | Aktuelles SonarQube-Cloud-Komponenten-Inventar für Parent `ci/checks`: 6 Security-Befunde, 2 Security-Hotspots, 32 Maintainability-Befunde und 0,0 % duplizierte Zeilen. |
| Grenze | Parent-`ci/checks`, ein fokussierter Parent-Test und dieses deutsch/englische Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, Workflows, Scanner-Einstellungen, Suppressions und `master` bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle `ci/checks`-Komponente enthält Security-Befunde für die
Eingrenzung von Report-Schreibpfaden und feste Policy-Pfade, Security-Hotspots
für statische URL-Policy-Beispiele sowie Maintainability-Befunde für lange
Checker, wiederholte Literal-Owner, reguläre Ausdrücke und die Verteilung von
Konfigurationsmetadaten. Die Bereinigung muss die fail-closed-Policy-Verträge
aller Checker bewahren und die konkreten Source-Ursachen ohne SonarQube-Cloud-
Einstellung, Suppression, Exclusion oder Quality-Gate-Workaround entfernen.

## Akzeptanzkriterien

- Jeder aktuelle `ci/checks`-Source-Befund erhält in dieser Änderung eine
  Source-Level-Behebung; Scanner-Regeln, Exclusions, Suppressions und das
  Quality Gate bleiben unverändert.
- Bilinguale Dokumentation, Generated Reports, Konfigurationsreferenz,
  Lifecycle-, HAProxy-HTX-, Runtime-Path- und Common-Adoption-Checks bewahren
  ihre bisherigen erfolgreichen Kontrollen.
- Generierte Test-Matrix-Reports werden nur aktualisiert, wenn sie reguläre,
  keine Symlink-Dateien unterhalb der ausgecheckten Parent-Root sind.
- Der exakte PR-Head erhält frische GitHub-Actions- und SonarQube-Cloud-
  Evidence vor jeder Merge-Entscheidung.

## Implementierungsentscheidung und Begründung

Kleine zweckgebundene Hilfen besitzen jetzt Report-Pfad-Trust-Checks,
Dokument-/Lifecycle-Teilprüfungen, Scanner-Result-Parsing, HAProxy-HTX-
Verträge und die Darstellung der Konfigurationsreferenz. Die großen Envoy- und
Traefik-YAML-Metadaten-Dispatcher verwenden explizites Path-Matching statt
verschachtelter Bedingungsketten; ihre Ausgabe bleibt gegen das eingecheckte
Inventar und die bilingualen Referenzen geprüft.

Die statische URL-Testpolicy wird aus benannten Scheme- und Host-Komponenten
gebildet. Damit weist der Checker unsichere Repository-Referenzen weiter ab,
ohne einen fest codierten unsicheren URL-Sink zu behalten. Gemeinsame feste
Roots und wiederholte Markdown-Muster haben einen privaten Owner. Der neue
Regressionstest deckt den regulären In-Tree-Report-Control sowie die
Abweisung von Symlink- und Outside-Root-Schreibzielen ab.

### Follow-up der Draft-PR-Analyse

Die erste Draft-PR-Analyse meldete sieben verbleibende New-Code-Source-Issues.
Dieses Follow-up gibt dem FTW-Repository-Namen einen Owner, zerlegt zwei noch
zu komplexe Checks in zweckgebundene Helfer, ersetzt die drei beanstandeten
Backtracking-Patterns durch begrenztes zeilenorientiertes Parsing oder einen
kleinen Key-Parser und trennt die zusammengesetzte Import-Assertion des
Testmoduls.

## Geänderte Dateien

- `ci/checks/analysis/clang_analysis_baseline.py`
- `ci/checks/connectors/all/check-remaining-connectors-common-adoption.py`
- `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`
- `ci/checks/documentation/check-bilingual-docs.py`
- `ci/checks/documentation/check-connector-config-reference.py`
- `ci/checks/documentation/check-generated-report-layout.py`
- `ci/checks/documentation/check-no-crs-doc-consistency.py`
- `ci/checks/documentation/connector_config_reference.py`
- `ci/checks/documentation/ensure-test-matrix-language-switches.py`
- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `ci/checks/evidence/check-six-connector-core-completion.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_ensure_test_matrix_language_switches.py`
- `reports/audits/change-records/README.md`, das deutsche Gegenstück und
  dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `python -m unittest tests.test_bilingual_docs tests.test_runtime_path_policy tests.test_clang_analysis_baseline tests.test_full_lifecycle_evidence tests.test_full_lifecycle_gate_wiring tests.test_connector_config_reference tests.test_ensure_test_matrix_language_switches` | bestanden: 60 Tests. |
| `python -m unittest tests.test_generated_report_evidence_integrity` | bestanden: 76 Tests; der eingebettete Generated-Report-Layout-Check bestand. |
| `python ci/checks/documentation/check-bilingual-docs.py` | bestanden: `bilingual docs ok`. |
| `python ci/checks/documentation/check-connector-config-reference.py` | bestanden für Apache-, NGINX-, HAProxy-, Envoy-, Traefik-, lighttpd-, Common-Runtime- und Engine-Inventare. |
| `python ci/checks/documentation/check-no-crs-doc-consistency.py` | bestanden. |
| `python ci/checks/connectors/all/check-remaining-connectors-common-adoption.py` | bestanden für alle Connectoren. |
| `python ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | bestanden: alle 26 statischen Verträge. |
| `python ci/checks/security/check-runtime-path-policy.py` | bestanden; die erwarteten negativen Self-Checks wiesen unsichere Roots ab. |
| Follow-up-Fokussuite für Konfigurationsreferenz-, Lifecycle-, Generated-Report-, Path-Update- und bilinguale Controls | bestanden: 121 Tests. |
| `git diff --check` | vor dem Hinzufügen des Change Records bestanden; wird nach allen Dokumentationsänderungen und vor der Auslieferung erneut ausgeführt. |

## Security-Auswirkung

Der Report-Sprach-Updater weist einen symbolischen Link, eine nicht reguläre
Datei oder einen aufgelösten Pfad außerhalb des Checkouts zurück, bevor er ihn
liest oder schreibt. Runtime-Path-Policy-Roots bleiben durch die gemeinsame
vertrauenswürdige Hilfe bestimmt. URL-Checks, Artefaktvalidierung und alle
bestehenden fail-closed-Policy-Pfade bleiben aktiv; die Änderung erweitert
weder Netzwerk-, Dateisystem-, Credential- noch CI-Autorität.

## Runtime-Evidence

Nicht anwendbar. Dies sind statische Parent-CI-Check- und Dokumentations-
Generator-Änderungen. Der HAProxy-HTX-Static-Contract sowie die In-Tree-,
Symlink- und Outside-Path-Tests sind Control-Evidence, keine Connector-
Runtime-Behauptung.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Builds und Runtime-Matrizen wurden nicht ausgeführt,
  weil sich weder Connector-Produktsource noch Runtime-Verhalten änderte.
- Framework- und MRTS-Prüfungen wurden nicht ausgeführt, weil weder eines der
  Repositories noch einer der Gitlinks im Scope liegt.
- Frische SHA-gebundene GitHub Actions, Review-Status und SonarQube Cloud sind
  noch ausstehende Delivery-Evidence für den Draft-PR
  [#212](https://github.com/Easton97-Jens/ModSecurity-conector/pull/212).

## Bekannte Einschränkungen

Der Task-Branch wurde vor der Erstellung des Draft-PR
[#212](https://github.com/Easton97-Jens/ModSecurity-conector/pull/212) auf
den aktuellen `origin/master` rebasiert. Die Source-Level-Bereinigung ist
extern erst geschlossen, wenn eine SonarQube-Cloud-Analyse für den finalen
PR-Head die Abwesenheit der genannten Komponentenbefunde sowie keine neuen
Issues und keine New-Code-Duplizierung bestätigt.

## Verbleibende Risiken

Die strukturellen Refactorings bewahren die Checker-Ausgaben durch die
fokussierten Suiten. Ein nicht ausgeübter ungewöhnlicher YAML-Pfad oder ein
fehlerhaftes Report-Layout könnte jedoch noch eine Abweichung in der
Diagnosereihenfolge zeigen. Die finalen SHA-gebundenen Hosted- und
SonarQube-Cloud-Prüfungen sind erforderlich, um diese Integrationsklasse zu
erkennen. Die negativen Path-Update-Tests mindern die sicherheitsrelevante
Schreibgrenze; dieser Record enthält weder rohe Report-Inhalte noch Credentials.

## Finaler Diff- und Review-Status

Zum Zeitpunkt dieses Records bleibt der Kandidat auf Parent-`ci/checks`, den
fokussierten Test und Traceability-Dokumentation begrenzt. Es gibt keine
Framework-/MRTS-/Gitlink-, Workflow-, Dependency-, Scanner-Konfigurations-,
Suppression- oder `master`-Änderung. Die genannten lokalen Controls bestanden;
finaler Scoped-Review, Commit und Push für Draft-PR
[#212](https://github.com/Easton97-Jens/ModSecurity-conector/pull/212) sind
abgeschlossen, die SHA-gebundene Hosted-Verifikation steht noch aus. Dieser
Record autorisiert keinen Merge.
