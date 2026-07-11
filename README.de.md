# ModSecurity Connector

**Sprache:** [English](README.md) | Deutsch

Dieses Repository enthält connector-fokussierten Code und Integrationsgerüste
für Server-Connectoren auf Basis von libmodsecurity v3. Das wiederverwendbare
Test-Framework liegt im Modul `modules/ModSecurity-test-Framework`; dieses
Repository enthält die Connector-Quellbäume, Connector-Metadaten,
Harness-Integration und generierte Connector-Evidence.

## Dokumentationsindex

GitHub zeigt weiterhin alle Dateien im Repository-Baum; diese Links halten Sie
in der gewählten Dokumentationssprache.

### Compile- / Operator-Guides

- [Apache](./COMPILE_APACHE.de.md)
- [NGINX](./COMPILE_NGINX.de.md)
- [HAProxy](./COMPILE_HAPROXY.de.md)
- [Envoy](./COMPILE_ENVOY.de.md)
- [Traefik](./COMPILE_TRAEFIK.de.md)
- [Lighttpd](./COMPILE_LIGHTTPD.de.md)
- [Open Connectors](./COMPILE_OPEN_CONNECTORS.de.md)

### Beispiel-Konfigurations-READMEs

- [Apache-Beispiele](./examples/apache/README.de.md)
- [NGINX-Beispiele](./examples/nginx/README.de.md)
- [HAProxy-Beispiele](./examples/haproxy/README.de.md)
- [Envoy-Beispiele](./examples/envoy/README.de.md)
- [Traefik-Beispiele](./examples/traefik/README.de.md)
- [Lighttpd-Beispiele](./examples/lighttpd/README.de.md)

## Connector-Architektur

Das Repository ist in eine connector-neutrale C-Schicht und adaptereigene
Connector-Bäume aufgeteilt:

- `common/include/msconnector/` definiert gemeinsame Datenformen für
  Direktiven, Optionen/Defaults, Rule-Load-Statistiken, Requests, Responses,
  Transactions, Interventions, Capabilities, Herkunft, Logging und Status.
- `common/src/` enthält kleine connector-neutrale Hilfsimplementierungen.
- `connectors/apache/` enthält den Apache-Connector-Adapter,
  Autotools/APXS-Build-Eingaben, Harness-Dateien, Metadaten und produktiven
  Quellcode unter `connectors/apache/src/`.
- `connectors/nginx/` enthält den NGINX-Connector-Adapter, die Modul-`config`,
  Harness-Dateien, Metadaten und produktiven Quellcode unter
  `connectors/nginx/src/`.
- `connectors/haproxy/` enthält einen produktiven SPOA/SPOP-Runtime-Pfad,
  Beispiele, Harness-Dateien, Metadaten und produktiven Quellcode unter
  `connectors/haproxy/src/`.
- `connectors/{envoy,lighttpd}/` sind Gerüste für zukünftige Connectoren mit
  Dokumentation und TODOs; `connectors/traefik/` ergänzt einen Starter für
  einen lokalen Decision-Service ohne Runtime-Verifikation.

Connector-Quellcode ist repository-lokal. Apache- und NGINX-Connector-
Repositories werden nicht als Runtime-Defaults abgerufen.

## Unterstützte Connectoren

| Connector | Status | Primärer Pfad |
| --- | --- | --- |
| Apache | adaptereigener Quellbaum mit Real-World-Smoke-Harness; evidence-begrenzt, nicht pauschal stabil | `connectors/apache/` |
| NGINX | adaptereigener Quellbaum mit Real-World-Smoke-Harness; evidence-begrenzt, nicht pauschal stabil | `connectors/nginx/` |
| HAProxy | produktive SPOA/SPOP-Runtime mit Live-HAProxy-Smoke-Evidence; evidence-begrenzt und partiell | `connectors/haproxy/` |
| Envoy | zurückgestelltes Platzhalter-Gerüst | `connectors/envoy/` |
| Lighttpd | zurückgestelltes Platzhalter-Gerüst | `connectors/lighttpd/` |
| Traefik | Starter für lokalen Decision-Service; Runtime nicht verifiziert | `connectors/traefik/` |

Pass-Claims für Apache, NGINX und HAProxy müssen an ein konkretes Smoke-Ergebnis
gebunden sein. Die aktuelle generierte Default-Runtime-Evidence ist Apache
`54/54 PASS`, NGINX `60/60 PASS` und HAProxy `55/55 PASS`. Force-all-Runtime-
Evidence bleibt getrennt: Apache `133 attempted / 100 PASS / 27 FAIL /
0 BLOCKED / 6 NOT_EXECUTABLE`, NGINX `140 attempted / 95 PASS / 39 FAIL /
0 BLOCKED / 6 NOT_EXECUTABLE` und HAProxy `133 attempted / 104 PASS / 23 FAIL /
0 BLOCKED / 6 NOT_EXECUTABLE`. API-only-Smokes sind kein Connector-Nachweis.

## Merge Readiness / Aktueller Status

Aktuelle Merge-Readiness-Evidence für PR #13:

- SonarCloud Quality Gate: `OK`
- SonarCloud-Ratings: Reliability `A`, Security `A`
- SonarCloud Bugs/Vulnerabilities: `0`
- SonarCloud Security Hotspots: `0 open / 100% reviewed`
- Full-Matrix: `3074 PASS / 782 FAIL / 0 BLOCKED`
- Final consistency audit: `recommended_next_fix_cluster: none`
- Aktive runtime-fixable Cluster: keine
- Reports wurden über die Make-/Generator-Targets aktualisiert
- Framework- und MRTS-Submodule: clean

Die 782 Full-Matrix-Fehlschläge werden nicht ignoriert und nicht manuell
umgeschaltet. Sie bleiben in den generierten Work Queues und Analyse-Reports
als semantische Unterschiede, Capability-Gaps, reine Report-Fälle oder
`not_next`-Bereiche klassifiziert, die nicht durch Änderungen an Expected-
Status oder PASS/FAIL-Werten gelöst werden sollen. Die kanonischen
Merge-Readiness-Reports sind:

- [Full runtime matrix](reports/testing/generated/canonical/full-runtime-matrix.generated.de.md)
- [Final consistency audit](reports/testing/generated/canonical/final-consistency-audit.generated.de.md)
- [Next fix plan](reports/testing/generated/canonical/next-fix-plan.generated.de.md)
- [Remaining failure analysis](reports/testing/generated/canonical/remaining-failure-analysis.generated.de.md)
- [Testing report index](reports/testing/README.de.md)

## Connector-Feature-Status

Die Apache- und NGINX-Connectoren teilen connector-neutrale Metadaten in
`common/`, behalten das Server-Runtime-Verhalten aber in ihren adaptereigenen
Bäumen. Die folgenden Tabellen beschreiben nur den aktuell implementierten
Stand.

### Gemeinsame Features

| Feature | Apache | NGINX | Hinweise |
| --- | --- | --- | --- |
| <code>modsecurity on&#124;off</code> | Unterstützt | Unterstützt | Gemeinsamer Direktivenname aus `common/include/msconnector/directives.h`; serverspezifische Direktivenregistrierung bleibt adaptereigen. |
| Inline-Regeln | Unterstützt | Unterstützt | `modsecurity_rules`; Regel-Loading und Fehlerpfade bleiben connector-spezifisch. |
| Regeldatei | Unterstützt | Unterstützt | `modsecurity_rules_file`; Werte zählen nach erfolgreichem Laden in die Rule-Load-Metadaten ein. |
| Remote-Regeln | Unterstützt | Unterstützt | `modsecurity_rules_remote`; Remote-Loading bleibt connector-spezifisch. |
| Transaction ID | Unterstützt | Unterstützt | Apache akzeptiert einen statischen String oder eine separate Apache-Expression-Direktive; NGINX akzeptiert einen NGINX Complex Value. |
| Error-Log-Weiterleitungsrichtlinie | Unterstützt | Unterstützt | <code>modsecurity_use_error_log on&#124;off</code>; Default ist on. Audit-Logs, Interventions und Request-/Response-Verarbeitung bleiben unverändert. |
| Rule-Load-Stats-Metadaten | Unterstützt | Unterstützt | Gemeinsame Datenform in `common/include/msconnector/rule_load_stats.h`; nur Metadaten. |
| Gemeinsame Direktiven-Metadaten | Verwendet | Verwendet | Gemeinsame Konstanten für Direktiven-Namen werden von beiden Connectoren verwendet. |
| Gemeinsame Options-Metadaten | Partiell | Partiell | Apache und NGINX verwenden gemeinsame Defaults für Aktivierung, Error-Log-Weiterleitung und begrenzte Phase-4-Optionen, wo implementiert. |

### Apache

Der Apache-Connector ist ein adaptereigenes Apache-Modul unter
`connectors/apache/`. Er unterstützt derzeit:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` behält die vorhandene Static-String-Semantik.
`modsecurity_transaction_id_expr` ist eine opt-in Apache-String-Expression, zum
Beispiel `%{REQUEST_URI}`, die pro Request ausgewertet wird. Statische und
Expression-basierte Transaction IDs schließen sich im selben Apache-Kontext
gegenseitig aus; normale Child-Context-Overrides gelten beim Config-Merge. Wenn
keine der beiden Direktiven gesetzt ist, wenn die Expression zu einem leeren
Wert auswertet oder fehlschlägt, behält Apache den vorhandenen `UNIQUE_ID`-
Fallback und erstellt danach eine Transaction ohne explizite ID, falls kein
brauchbarer `UNIQUE_ID`-Wert verfügbar ist.

`modsecurity_use_error_log off` unterdrückt nur die Apache-Error-Log-Weiterleitung
aus dem libmodsecurity-Log-Callback. Audit-Logging, Interventions, Hooks,
Filter, Buckets, Transaction-Ownership sowie Request- und Response-Verarbeitung
werden nicht geändert.

Apache verfolgt Rule-Load-Statistiken intern in `msc_conf_t`. Der Connector
meldet diese Statistiken derzeit nicht im Post-Config-Log. Apache-Unterstützung
für begrenzte Phase 4 ist evidence-begrenzt und promoted kein vollständiges
RESPONSE_BODY-Verhalten.

### NGINX

Der NGINX-Connector ist ein adaptereigenes dynamisches NGINX-Modul unter
`connectors/nginx/`. Er unterstützt derzeit:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

`modsecurity_transaction_id` verwendet einen NGINX Complex Value und kann pro
Request NGINX-Variablen auswerten. NGINX gibt Rule-Load-Statistiken über den
gemeinsamen Rule-Load-Stats-Helper in seinem bestehenden Startup-Log aus, ohne
Log-Text, Format, Level oder Reihenfolge zu ändern.

Die Phase-4-Direktiven sind begrenzte Runtime-Controls. Sie sind kein
gemeinsamer Promotion-Vertrag und promoten kein vollständiges RESPONSE_BODY-
Verhalten.

### HAProxy

Der HAProxy-Connector verwendet einen produktiven SPOA/SPOP-Pfad unter
`connectors/haproxy/`. Er unterstützt derzeit:

- `haproxy-modsecurity-spoa`
- HAProxy-SPOE/SPOP-Integration
- libmodsecurity-Regelladen und Decision-Verarbeitung
- `decision.jsonl` als Runtime-Decision-Evidence
- Audit-Log-Plumbing
- Request-Phasen 1/2
- implementierte Phase-3-Response-Header-Evidence
- nur Response-Header-Verarbeitung; das frühere Response-Body-Phase-4-Sample ist deaktiviert

HAProxy wird über HAProxy-, SPOE- und SPOA-Agent-Konfigurationsdateien
konfiguriert, nicht über Apache-/NGINX-artige `modsecurity_*`-Direktiven. Es
gibt keinen synthetischen Matrix-Writer; generierte HAProxy-Reports verwenden
Live-Runtime-Zusammenfassungen und den Runtime-Validation-Snapshot.

Phase 4 / RESPONSE_BODY ist im gewählten SPOE/SPOP-Pfad
`not_implemented`: Das frühere `wait-for-body`-Sample ist deaktiviert und
keine Runtime-Evidence.

### Bekannte Unterschiede und zurückgestellte Bereiche

| Bereich | Aktueller Stand |
| --- | --- |
| Transaction-ID-Mapping | Apache unterstützt statische Strings plus opt-in Apache-String-Expressions über `modsecurity_transaction_id_expr`; NGINX unterstützt Complex Values über `modsecurity_transaction_id`. |
| Phase-4-Direktiven | Apache und NGINX implementieren begrenzte Phase-4-Controls; vollständiges RESPONSE_BODY-Verhalten bleibt nicht promoted. |
| HAProxy-Direktivenmodell | HAProxy verwendet HAProxy-Konfiguration, SPOE-Konfiguration und `haproxy-modsecurity-spoa`-Agent-Konfiguration statt `modsecurity_*`-Serverdirektiven. |
| RESPONSE_BODY-Verhalten | Apache-/NGINX-Source-Pfade bleiben evidence-begrenzt; HAProxy Phase 4 ist im gewählten SPOE/SPOP-Pfad `not_implemented`, weil das frühere `wait-for-body`-Sample deaktiviert ist. |
| Apache-Bucket-/Filter-/Intervention-Pfade | In dieser Common-Metadata-Arbeit bewusst nicht refaktoriert. |
| Common Layer | Enthält nur connector-neutrale Metadaten und Datenformen; besitzt keine Apache- oder NGINX-Runtime-APIs. |
| Rule-Load-Stats-Reporting | NGINX berichtet über sein bestehendes Startup-Log; Apache behält Stats als interne Metadaten, bis Anzeigeaggregation und Merge-Semantik explizit designt sind. |

## Connector-Metadaten

Adapter-Metadaten gehören dem jeweiligen Connector:

- `connectors/apache/metadata.c`
- `connectors/nginx/metadata.c`
- `connectors/*/ORIGIN.md`
- `licenses/*/ORIGIN.md`
- `config/testing/import-status.json`

Die Metadata-Drift-Checks vergleichen die Source-Attribution der Connectoren
mit Connector- und Framework-Dokumentation, ohne Connector-Runtime-Code zu
verlinken.

## Build- und Runtime-Integration

Die öffentlichen Connector-Target-Namen bleiben unverändert und delegieren bei
Bedarf an das Framework-Modul:

```sh
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
make summary
make case-matrix
make runtime-matrix-all
make smoke-common
make smoke-apache
make smoke-nginx
make smoke-haproxy
make smoke-all
make runtime-matrix-haproxy
```

CRS-Varianten sind über das Framework-Modul verfügbar:

```sh
make test-no-crs
make test-with-crs
make test
```

`test-no-crs` lädt nur die generierten lokalen YAML-Case-Regeln. `test-with-crs`
holt/bereitet OWASP CRS über den zentralen Pin in
`modules/ModSecurity-test-Framework/ci/common.sh` vor und lädt CRS vor den
lokalen Case-Regeln. `test` führt beide Varianten aus.

## MRTS-Tests

MRTS ist im Framework als erforderliches Framework-Submodul integriert. Das
Connector-Repository kopiert keine MRTS-Generatorlogik; diese Targets delegieren
an `FRAMEWORK_ROOT`.

Initialisieren Sie Connector-Submodule rekursiv, damit das verschachtelte
Framework-MRTS-Submodul verfügbar ist:

```sh
git submodule update --init --recursive
```

Die delegierten Targets verwenden standardmäßig
`modules/ModSecurity-test-Framework/tools/MRTS`. Sie können weiterhin auf einen
separaten Checkout zeigen:

```sh
MRTS_ROOT=/path/to/MRTS make mrts-generate
```

Delegierte Targets:

```sh
make mrts-generate
make test-no-mrts
make test-with-mrts
make test-with-mrts-feature-demo
make test-mrts-matrix
make mrts-ftw
```

Das Framework liest Upstream-MRTS-Eingaben direkt aus `$MRTS_ROOT`, schreibt
generierte Regeln, go-ftw YAML, Framework-Cases und `mrts.load` unter
`$MRTS_BUILD_ROOT` und verwendet `upstream-config-tests` als standardmäßig
ausführbaren MRTS-Korpus. Feature-Demo-Tests werden als optionale/Demo-Coverage
berichtet und können nur über das explizite Opt-in-Target oder
`MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` versucht werden. Golden References
unter dem MRTS-Submodul sind nur Drift-/Report-Eingaben und niemals Runtime-
Eingaben.

Native MRTS-Infrastruktur-Evidence ist von Connector-Smoke-Evidence getrennt:

```sh
make mrts-upstream-infra-check
make mrts-native-apache-full
make mrts-native-nginx-pr24-full
make mrts-native-full-run
```

Native Outputs werden unter `$MRTS_NATIVE_ROOT` bereitgestellt und als separate
native Infrastruktur-Evidence berichtet:

- Apache native: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Diese nativen MRTS-Reports sind von Connector-Full-Matrix-Evidence getrennt.
Fehlende lokale Abhängigkeiten wie `go-ftw`, `albedo`, `apachectl`, `nginx` oder
das NGINX-ModSecurity-Modul werden als `BLOCKED` berichtet; global wird nichts
installiert.

Runtime-Tool-Source-URLs, erwartete Release-Refs, Binary-Defaults und
Kandidatenlisten sind in `modules/ModSecurity-test-Framework/ci/common.sh`
zentralisiert. Runtime-Vorbereitungs- und Proof-Skripte laden diese Framework-
Umgebung und lesen Werte wie `GO_FTW_SOURCE_URL`, `ALBEDO_SOURCE_URL` und
`EXPAT_SOURCE_URL` daraus. Lokale Overrides können vor dem Aufruf der Make-
Targets über Umgebungsvariablen gesetzt werden.

MRTS-/CRS-Ergebnispfade sind nach Variante getrennt:

```text
$BUILD_ROOT/results/no-crs/no-mrts
$BUILD_ROOT/results/no-crs/with-mrts
$BUILD_ROOT/results/with-crs/no-mrts
$BUILD_ROOT/results/with-crs/with-mrts
```

Source-Build-Variablen bleiben konfigurierbar:

```sh
VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified
BUILD_ROOT=$VERIFIED_RUN_ROOT/build
SOURCE_ROOT=$VERIFIED_RUN_ROOT/src
MODSECURITY_GIT_REF=v3/master
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3
```

`BUILD_ROOT` ist ein lokaler Build-/Output-Ort, kein Cache-Vertrag. Vollständige
Runtime-Validierung ist lokal und evidence-basiert; `make smoke-all` ist nur
dann maßgeblich, wenn es tatsächlich erfolgreich ausgeführt wurde.

Verified-Run- und Report-Refresh-Workflows verwenden standardmäßig
`${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified`, mit
`NGINX_HARNESS_PARENT` unterhalb dieses Roots, damit Worker-Prozesse den
generierten Docroot durchlaufen können. Siehe
[Verified Run Environment](docs/testing/verified-run-environment.de.md) für den
Runtime-Pfad-Vertrag, den NGINX-Docroot-Preflight und Regeln für generierte
Artefakte.

GitHub-Actions-Artefakte werden vom Root-Workflow
[cleanup-artifacts](./.github/workflows/cleanup-artifacts.yml) per manueller
Ausführung und nächtlichem Zeitplan bereinigt. Das vendored Framework-Modul hat
denselben Cleanup-Workflow, wenn es als eigenes GitHub-Repository läuft. In
beiden Repositories behält Cleanup nur das neueste Artefakt je logischer
Artefaktgruppe und höchstens die neuesten 20 Artefakte insgesamt.
Upload-Workflows bereinigen ihre passende logische Gruppe vor dem Upload.
Report- und Log-Artefakte sind Best-Effort-Diagnostik mit einem Tag Retention.

GitHub-Actions-Workflow-Versionen werden getrennt von Build- und Testlogik
gepflegt. Dependabot prüft Root-GitHub-Actions wöchentlich. Der Workflow
[check-actions-versions](./.github/workflows/check-actions-versions.yml)
meldet veraltete `uses:`-Einträge, während
[update-actions-versions](./.github/workflows/update-actions-versions.yml)
Workflow-Action-Refs auf `automation/update-github-actions-versions`
aktualisiert und einen Pull Request öffnet, statt direkt auf den Default-Branch
zu pushen. Der Updater scannt sowohl die Root-Workflows als auch
`modules/ModSecurity-test-Framework`; weil das Framework ein Submodul ist,
werden Modul-Workflow-Änderungen nur berichtet, sofern `SUBMODULE_UPDATE_TOKEN`
nicht verfügbar ist, um den separaten Modul-Branch/PR zu erstellen und den
Submodul-Pointer zu aktualisieren. SHA-pinned, lokale, Docker- und dynamische
`uses:`-Einträge werden nicht automatisch geändert. Reports werden in die Step
Summary geschrieben und als Best-Effort-Artefakt für einen Tag hochgeladen.

## Framework-Modul-Integration

Initialisieren Sie das Framework-Modul, bevor Sie framework-gestützte Targets
ausführen:

```sh
git submodule update --init --recursive
```

Der Standard-Modulpfad ist:

```sh
modules/ModSecurity-test-Framework
```

Überschreiben Sie ihn, wenn Sie einen separaten Checkout verwenden:

```sh
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make runtime-matrix-all
```

Das Framework besitzt YAML-Cases, Runner, Normalizer, Runtime-Matrix-Logik,
Coverage-Generierung, v3-API-Smoke-Helfer und wiederverwendbare
Testdokumentation. Connector-spezifische generierte Evidence wird in diesem
Repository unter `reports/testing/` geschrieben. Die Root-Coverage-
Zusammenfassung gehört dem Framework unter
`modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`; das Parent-
Repository pflegt keine separate Coverage-Summary-Quelle der Wahrheit.

## Report Refresh

Generierte Reports müssen über ihre Generatoren aktualisiert werden, nicht per
Hand. Das Connector-Refresh-Target aktualisiert den connector-eigenen
Reportkatalog, einschließlich Full Runtime Matrix, Work Queues,
Remaining-Failure-Analysis, Capability-/Gap-Reports und Final Consistency
Audit:

```sh
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make refresh-all-reports
```

Das Framework-Refresh-Target aktualisiert framework-eigene generierte
Dokumentation:

```sh
make -C modules/ModSecurity-test-Framework refresh-framework-reports
```

Vor dem Merge sollten die Lint- und Quick-Checks in beiden Repositories erneut
ausgeführt werden; danach ist zu prüfen, dass das generierte Report-Manifest
und der Final Consistency Audit mit dem aktuellen Branch-Stand übereinstimmen.
Runtime-Caches, generierte MRTS-Regeln, FTW YAML, Load-Dateien und temporäre
Job-Ausgaben sind lokale Artefakte und dürfen nicht committed werden.

## Dokumentationslinks

- Build-/Prepare-Dokumente: [Compile Apache](./COMPILE_APACHE.de.md),
  [Compile HAProxy](./COMPILE_HAPROXY.de.md),
  [Compile NGINX](./COMPILE_NGINX.de.md),
  [Prepare Envoy](./COMPILE_ENVOY.de.md),
  [Prepare Traefik](./COMPILE_TRAEFIK.de.md),
  [Compile Lighttpd](./COMPILE_LIGHTTPD.de.md),
  [Open Connectors](./COMPILE_OPEN_CONNECTORS.de.md)
- Beispiel-Konfigurationen: [Apache-Beispiele](./examples/apache/README.de.md), [NGINX-Beispiele](./examples/nginx/README.de.md), [HAProxy-Beispiele](./examples/haproxy/README.de.md)
- Gemeinsame Connector-Feature-Dokumente: [Shared Features](./SHARED_FEATURES.md)
- Roadmap: [docs/roadmap/roadmap.de.md](docs/roadmap/roadmap.de.md)
- Architektur-Dokumente: [docs/architecture/](./docs/architecture/)
- Capability Model: [docs/architecture/capability-model.de.md](docs/architecture/capability-model.de.md)
- Status Model: [docs/architecture/status-model.de.md](docs/architecture/status-model.de.md)
- Connector Adapter Interface: [docs/architecture/connector-adapter-interface.de.md](docs/architecture/connector-adapter-interface.de.md)
- Connector-Dokumente: [docs/connectors/](./docs/connectors/)
- Rule-Load-Stats: [docs/connectors/rule-load-stats.de.md](docs/connectors/rule-load-stats.de.md)
- YAML-Schema-Hinweise: [modules/ModSecurity-test-Framework/docs/imports/common/schema.de.md](modules/ModSecurity-test-Framework/docs/imports/common/schema.de.md)
- Gemeinsame Fixtures: [modules/ModSecurity-test-Framework/docs/imports/common/fixtures.de.md](modules/ModSecurity-test-Framework/docs/imports/common/fixtures.de.md)
- Smoke-Target-Semantik: [modules/ModSecurity-test-Framework/docs/testing/fast-checks.de.md](modules/ModSecurity-test-Framework/docs/testing/fast-checks.de.md)
- Testing-Report-Index: [reports/testing/README.de.md](reports/testing/README.de.md)
- Real-World-Connector-Validation: [reports/testing/real-world-connector-validation.de.md](reports/testing/real-world-connector-validation.de.md)
- HAProxy-PoC-Evidence: [reports/testing/haproxy-poc.de.md](reports/testing/haproxy-poc.de.md)
- Full Runtime Matrix: [reports/testing/generated/canonical/full-runtime-matrix.generated.de.md](reports/testing/generated/canonical/full-runtime-matrix.generated.de.md)
- Final Consistency Audit: [reports/testing/generated/canonical/final-consistency-audit.generated.de.md](reports/testing/generated/canonical/final-consistency-audit.generated.de.md)
- Next Fix Plan: [reports/testing/generated/canonical/next-fix-plan.generated.de.md](reports/testing/generated/canonical/next-fix-plan.generated.de.md)
- Remaining Failure Analysis: [reports/testing/generated/canonical/remaining-failure-analysis.generated.de.md](reports/testing/generated/canonical/remaining-failure-analysis.generated.de.md)
- Case-Matrix-Reports: [reports/testing/case-matrix.de.md](reports/testing/case-matrix.de.md), [reports/testing/generated/coverage/case-matrix.generated.de.md](reports/testing/generated/coverage/case-matrix.generated.de.md)
- PR-/Source-Evidence: [reports/testing/evidence/pr-evidence-summary.de.md](reports/testing/evidence/pr-evidence-summary.de.md), [reports/testing/evidence/raw-args-pr3564.de.md](reports/testing/evidence/raw-args-pr3564.de.md)
- Lizenz- und Herkunftsindex: [docs/licensing/license-and-origin.de.md](docs/licensing/license-and-origin.de.md)
- Framework-Dokumente: `modules/ModSecurity-test-Framework/README.md`
- Connector-Test-Evidence: `reports/testing/`
- Framework-eigene Coverage-Zusammenfassung: `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

## Lokale Entwicklung

Typisches lokales Setup:

```sh
git submodule update --init --recursive
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
```

Runtime- und Coverage-Evidence darf nicht allein aus generierten Metadaten
abgeleitet werden. XFAIL-, pending-, future-, connector-gap- und
runtime-difference-Cases bleiben Evidence-Klassen, bis sie explizit durch
dokumentierten Runtime-Nachweis promoted werden. Phase 4 / RESPONSE_BODY ist
im gewählten HAProxy-SPOE/SPOP-Pfad `not_implemented`; das deaktivierte
`wait-for-body`-Sample ist keine Runtime-Evidence.
