# Dokumentationsindex

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis ist der Dokumentations-Einstiegspunkt für das
Connector-Repository. Es beschreibt die aktuelle HTTP/1.1-Kern-Lifecycle-
Arbeit für sechs Connectoren, ohne Production Readiness, CRS-Verifikation,
HTTP/2-Verifikation, HTTP/3-Verifikation, vollständige Matrix oder
Strict-Verhalten für alle Connectoren zu behaupten.

## Hier beginnen

| Bereich | Lesen Sie dies für | Source of Truth |
|---|---|---|
| [Konfiguration](configuration/variables.de.md) | Variablen, Pfadrollen, Platzhalter, Target-Eingaben, IDs, Status oder Integrationsmodi | Root-Makefile und Runtime-Wrapper |
| [Glossar](reference/glossary.de.md) | Definition von EOS, HTX, ext_proc, APXS, UDS, Evidence oder einem anderen Repository-Begriff | Diese Referenz plus lokale Erklärungen |
| [Build](build/README.de.md) | Build-Familien, Toolchain-Voraussetzungen, Caches und sichere Build-Pfade | Root- und Connector-Makefiles |
| [Connectoren](connectors/README.de.md) | Ausgewählte Host-Route und Dokumentationseinstieg für einen Connector | Connector-Metadaten, Capabilities und Harnesses |
| [Testing](testing/README.de.md) | Target-Auswahl, Status, Case-IDs und Testgrenzen | Root-Targets und Framework-Case-Katalog |
| [Evidence](evidence/README.de.md) | Artefaktlayout, Validierung, Promotion, Privacy und Run-IDs | Runtime-Lifecycle-Wrapper und Framework-Schemas |
| [Architektur](architecture/README.de.md) | Common-Layer, Connector-Grenzen und Architekturentscheidungen | Eingecheckte Architektur-Dokumente |
| [Entwicklung](development/documentation-style-guide.de.md) | Wie Dokumentation sicher geschrieben oder geprüft wird | Dieser Stil-Leitfaden |
| [Reports](../reports/testing/README.de.md) | Aktuelle generierte und manuell gepflegte Test-/Report-Einstiegspunkte | Report-Generatoren und Report-Metadaten |
| [Framework-Modul](../modules/ModSecurity-test-Framework/README.de.md) | Framework-eigener Katalog, Schemas, Runner und CI-Dokumentation | Framework-Repository |

Alle relativen Pfade dieser Tabelle beginnen am Repository-Root oder diesem
<code>docs/</code>-Verzeichnis, wie der Link es ausweist. Generierte Reports
bleiben unter <code>reports/</code>; eine als generated markierte Datei darf
nicht manuell verändert werden.

## Navigation nach Aufgabe

### Einen lokalen Strukturcheck ausführen

Verwenden Sie nach Änderungen an repository-eigener Dokumentation:

~~~sh
make check-bilingual-docs
~~~

Das Target prüft English-/German-Begleitdateien und lokale Links. Es führt
nicht alle Connectoren aus und erzeugt keine Runtime-Evidence. Siehe
[Testing](testing/README.de.md) für Status- und Exit-Code-Bedeutungen.

### Eine ausgewählte Connector-Route vorbereiten oder ausführen

Beginnen Sie mit [Build](build/README.de.md) und dem passenden Eintrag unter
[Connectoren](connectors/README.de.md). Der Platzhalter
<code>&lt;connector&gt;</code> akzeptiert nur <code>apache</code>,
<code>nginx</code>, <code>haproxy</code>, <code>envoy</code>,
<code>traefik</code> oder <code>lighttpd</code>; zum Beispiel:

~~~sh
make build-nginx
~~~

Dies baut eine ausgewählte Route. Es beweist nicht selbst Runtime-Verhalten
und promotet keine Capability.

### Mit kanonischer Evidence arbeiten

Wählen Sie eine sichere Run-ID und ein Evidence-Verzeichnis wie unter
[Konfiguration](configuration/variables.de.md#no-crs-und-evidence-variablen)
beschrieben. Verwenden Sie anschließend die exakte Target-Familie aus
[Evidence](evidence/README.de.md). Eine Run-ID ist ein dateisystemsicheres
Token wie <code>six-core-20260712T120000Z</code>; sie darf weder Secrets noch
persönliche Daten enthalten.

## Dokumentations-Ownership

- Repository-eigene Erklärungen, Navigation und aktuelle Guides gehören nach
  <code>docs/</code>, in Connector-Verzeichnisse oder Reports, je nach Zweck.
- Das Framework besitzt wiederverwendbare Case-Schemas, Katalogmechanik und
  Framework-Runner in <code>modules/ModSecurity-test-Framework/</code>.
- Generiertes Material gehört an den vom Generator definierten Ort. Ändern Sie
  Generator/Source of Truth, bewahren Sie Provenance und regenerieren Sie.
- Historische Reports bewahren ihre ursprünglichen Fakten und sollen als
  historisch gekennzeichnet statt als aktueller Stand umgeschrieben werden.
- Die [historische Dokumentation](archive/README.de.md) enthält bewahrte
  Repository-Inventare und Issue-Snapshots, die keine aktuelle Anleitung sind.

## Aktuelle Connector-Statusquellen

Die sechs ausgewählten Connector-Namen sind Apache, NGINX, HAProxy, Envoy,
Traefik und lighttpd. Die eingecheckte Bereichsdeklaration jedes Connectors
liegt unter `connectors/<connector>/capabilities.json`; der jeweilige
Connector-Guide erläutert Host-Route und Evidenzgrenze. Ein Status
`minimal_runtime_smoke` bezeichnet nur einen engen, connector-spezifischen
Runtime-Pfad. Er ersetzt weder ein kanonisches Aggregatresultat noch nicht
ausgeführte Katalogfälle.

## Bilinguale Policy

Jedes repository-eigene englische Dokument unter <code>docs/</code> besitzt
eine <code>.de.md</code>-Begleitdatei mit denselben technischen Namen,
Defaults, Pfaden, IDs, Status und Targets. Lesen Sie den
[Dokumentationsstil-Leitfaden](development/documentation-style-guide.de.md),
bevor Sie Variable, Platzhalter, Kommando-Beispiel oder Evidence-Claim
hinzufügen.
