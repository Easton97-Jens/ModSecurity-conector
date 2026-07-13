# ModSecurity Connector

**Sprache:** [English](README.md) | Deutsch

Dieses Repository enthält connector-eigenen Source, ausgewählte
Host-Integrationsrouten, Lifecycle-Wrapper, Konfiguration und
Evidence-Consumer für libmodsecurity-basierte Server-Connectoren.
Wiederverwendbare Case-Kataloge, Schemas und Framework-Runner liegen im
Submodule <code>modules/ModSecurity-test-Framework</code>.

Das Repository dokumentiert sechs ausgewählte HTTP/1.1-Kernrouten. Ihr
Ergebnis ist laufabhängig: Source-Wiring, Builds, Capability-Deklarationen und
Config-Checks sind für sich allein keine Evidence-Ergebnisse.

## Ausgewählte Connector-Routen

| Connector | Ausgewähltes Full-Lifecycle-Profil | Aufgezeichneter Integrationsmodus | Einstiegspunkt |
|---|---|---|---|
| Apache | <code>native-httpd-module</code> | <code>native-httpd-module</code> | [Connector-Guide](docs/connectors/README.de.md) / [Source](connectors/apache/README.de.md) |
| NGINX | <code>native-nginx-http-module</code> | <code>native-nginx-http-module</code> | [Connector-Guide](docs/connectors/README.de.md) / [Source](connectors/nginx/README.de.md) |
| HAProxy | <code>native-htx-filter</code> | <code>native-htx-filter</code> | [Connector-Guide](docs/connectors/README.de.md) / [Source](connectors/haproxy/README.de.md) |
| Envoy | <code>ext_proc</code> | <code>ext_proc</code> | [Connector-Guide](docs/connectors/README.de.md) / [Source](connectors/envoy/README.de.md) |
| Traefik | <code>native-middleware</code> | <code>native-traefik-middleware</code> | [Connector-Guide](docs/connectors/README.de.md) / [Source](connectors/traefik/README.de.md) |
| lighttpd | <code>patched-native</code> | <code>patched-native-lighttpd</code> | [Connector-Guide](docs/connectors/README.de.md) / [Source](connectors/lighttpd/README.de.md) |

Der Profilwert ist die Identität des Root-Lifecycle-Targets. Der
aufgezeichnete Integrationsmodus ist der beschreibende Wert, der mit dem
effektiven Run-Profil geschrieben wird. Details, alternative
Compatibility-Begriffe und Grenzen stehen in der
[Connector-Dokumentation](docs/connectors/README.de.md).

## Architektur

~~~mermaid
flowchart LR
    Client[HTTP client] --> Host[Selected connector host]
    Host --> Adapter[Connector adapter or bridge]
    Adapter --> Common[Common runtime / libmodsecurity]
    Common --> Host
    Host --> Raw[Invocation-local raw artifacts]
    Raw --> Finalize[Normalize and finalize]
    Finalize --> Evidence[Run-scoped canonical evidence]
    Evidence --> Validate[Evidence validators and reports]
~~~

Der Host ist Apache, NGINX, HAProxy, Envoy, Traefik oder lighttpd. Die
ausgewählte Route bestimmt ihre Request-/Response-Sichtbarkeit und
Phasengrenze. Roh-Runtime-Ausgabe ist nicht automatisch kanonische Evidence;
Finalisierung und Validierung binden Artefakte an Connector, Profil, Rules und
Run-ID.

## Schnellstart

Initialisieren Sie das Framework-Submodule und prüfen Sie dann seinen Ort:

~~~sh
git submodule update --init --recursive
make check-framework
~~~

<code>FRAMEWORK_ROOT</code> verwendet standardmäßig
<code>modules/ModSecurity-test-Framework</code>. Setzen Sie ihn nur bei einem
vertrauenswürdigen vorhandenen Framework-Checkout, zum Beispiel:

~~~sh
make check-framework FRAMEWORK_ROOT="/srv/src/ModSecurity-test-Framework"
~~~

<code>/srv/src/ModSecurity-test-Framework</code> ist ein Beispiel für einen
<em>externen Source-Root</em>: einen vom Benutzer ausgewählten absoluten
Checkout außerhalb dieses Repositorys. Es ist kein literaler oder
entwicklerspezifischer Pfad. Eine fehlende Framework-Voraussetzung erzeugt
Exit-Code <code>77</code>.

Führen Sie den lokalen Struktur-/Dokumentationscheck aus:

~~~sh
make quick-check
~~~

Dieser validiert repository-orientierte Checks; er führt nicht jeden
Connector-Host aus und erzeugt keine Full-Lifecycle-Evidence.

## Build- und Testüberblick

| Ziel | Beginnen mit | Wichtige Grenze |
|---|---|---|
| Eine ausgewählte Route bauen | <code>make build-nginx</code> | Build-Erfolg ist keine Runtime-Evidence |
| Ausgewählte Konfiguration prüfen | <code>make check-config-nginx</code> | Config-Load ist keine Traffic-Ausführung |
| Einen fokussierten Smoke ausführen | <code>make runtime-smoke-nginx</code>, wo bereitgestellt | Ein Smoke ist keine Full-Lifecycle-Promotion |
| Einen ausgewählten Aggregate-Candidate-Run erzeugen | <code>NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-all-connectors</code> | Run-ID ist ein Beispiel für ein sicheres Token, kein Outcome-Claim |
| Finalisierte Evidence validieren | <code>NO_CRS_RUN_ID="six-core-20260712T120000Z" make check-six-connector-core-completion</code> | Read-only-Gate; Exit <code>0</code> ist auf diesen Gate-Vertrag begrenzt |

Die exakten Eingaben, Ausgaben, Target-Bedeutungen, Statuswerte, Exit-Codes und
Platzhalter stehen unter [Build](docs/build/README.de.md) und
[Tests und Nachweise](docs/testing-and-evidence.de.md).

## Evidence-Grenze

Evidence wird unter einem externen Runtime-/Evidence-Baum abgelegt,
normalerweise <code>EVIDENCE_ROOT/connector/run-id</code>. Die Namen
<code>connector</code> und <code>run-id</code> sind konzeptionelle
Komponenten, keine literalen Verzeichnisnamen: Connector ist einer der sechs
Namen der Tabelle und Run-ID ein dateisystemsicheres Token wie
<code>six-core-20260712T120000Z</code>.

Keine Aussage hier behauptet:

- Production Readiness oder Production Hardening;
- CRS-Verifikation oder CRS-Vollständigkeit;
- vollständige HTTP/2- oder HTTP/3-Verifikation;
- vollständige Matrix-Abdeckung; oder
- Strict-Verifikation für alle Connectoren.

Strict Late Intervention, erweiterte Transports, CRS-Verhalten und Extended
Matrices bleiben getrennte Evidence-gesteuerte Arbeit. Lesen Sie die aktuellen
[Testing-Reports](reports/README.de.md) und den
[Guide für Tests und Nachweise](docs/testing-and-evidence.de.md), bevor Sie einen Ergebnis-Claim
erheben.

## Dokumentation

- [Dokumentationsindex](docs/README.de.md)
- [Einstieg](docs/getting-started.de.md)
- [Konfiguration](docs/configuration.de.md)
- [Variablen](docs/reference/variables.de.md)
- [Glossar](docs/reference/glossary.de.md)
- [Build-Guide](docs/build/README.de.md)
- [Connector-Guide](docs/connectors/README.de.md)
- [Tests und Nachweise](docs/testing-and-evidence.de.md)
- [Nachvollziehbarkeit von Änderungen](docs/change-traceability.de.md)
- Dokumentationspflege: `AGENTS.md` ist eine optionale lokale Anweisungsdatei für
  Codex und gehört nicht zur versionierten Projektdokumentation. Für sie gibt es
  keine deutsche Begleitdatei.
- [Betrieb und Sicherheit](docs/operations-and-security.de.md)
- [Framework-Modul](modules/ModSecurity-test-Framework/README.de.md)

Repository-eigene English-/German-Dokumentation wird geprüft mit:

~~~sh
make check-bilingual-docs
~~~

Generierte Reports müssen über Generator/Source of Truth geändert werden,
nicht durch manuelle Bearbeitung.
