# Connector-Dokumentation

**Sprache:** [English](README.md) | Deutsch

Dieser Bereich navigiert die sechs ausgewählten Connector-Routen. „P1“, „P2“,
„P3“ und „P4“ bedeuten die ModSecurity-Phasen Request Header, Request Body,
Response Header und Response Body. Der tatsächliche Case-Status einer Route ist
laufabhängig und stammt aus ihrer Evidence; Source-Präsenz, Capability-Manifest
oder Build erheben nicht selbst einen PASS-Claim.

Die ausgewählte HTTP/1.1-Kern-Dokumentation behauptet weder Production
Readiness noch CRS-Verifikation, vollständige HTTP/2- oder HTTP/3-Verifikation,
vollständige Matrix oder Strict-Verhalten für alle Connectoren.

## Connector-Karte

| Connector | Ausgewähltes Full-Lifecycle-Profil | Aufgezeichneter Integrationsmodus | Connector-Einstiegspunkt | P1–P4-Scope und Grenze |
|---|---|---|---|---|
| Apache | <code>native-httpd-module</code> | <code>native-httpd-module</code> | [Guide](apache.de.md) / [Quelle](../../connectors/apache/README.de.md) | Native Modulroute; P1–P4-Beobachtungen bleiben Run-/Evidence-abhängig und Response-Body-Verarbeitung kann bei EOS finalisieren |
| NGINX | <code>native-nginx-http-module</code> | <code>native-nginx-http-module</code> | [Guide](nginx.de.md) / [Quelle](../../connectors/nginx/README.de.md) | Native HTTP-Modulroute; P1–P4 benötigen ausgewählten Host-Run und Artefakte |
| HAProxy | <code>native-htx-filter</code> | <code>native-htx-filter</code> | [Guide](haproxy.de.md) / [Quelle](../../connectors/haproxy/README.de.md) | Native HTX-Filterroute; Body-Slices werden inkrementell weitergereicht und Phase 4 endet bei HTX-EOS |
| Envoy | <code>ext_proc</code> | <code>ext_proc</code> | [Guide](envoy.de.md) / [Quelle](../../connectors/envoy/README.de.md) | Streamed External-Processing-Route; Strict-Post-Commit-Reset bleibt eine getrennte Evidence-gesteuerte Frage |
| Traefik | <code>native-middleware</code> | <code>native-traefik-middleware</code> | [Guide](traefik.de.md) / [Quelle](../../connectors/traefik/README.de.md) | Native Middleware mit lokalem UDS-Service; Strict-Reset bleibt getrennt, bis Host-Evidence ihn nachweist |
| lighttpd | <code>patched-native</code> | <code>patched-native-lighttpd</code> | [Guide](lighttpd.de.md) / [Quelle](../../connectors/lighttpd/README.de.md) | Gepatchte Native-Host-/Modulroute; Entity-Body-Ranges werden vor Transfer-Framing verarbeitet und Phase 4 endet bei Entity-EOS |

Der Profilwert ist die interne Target-Identität, die der Root-Lifecycle-Runner
prüft. Der aufgezeichnete Integrationsmodus ist der beschreibende Wert, der in
run-lokale effektive Capability-Information geschrieben wird. Tauschen Sie die
Namen nicht aus und setzen Sie sie nicht manuell, um eine Compatibility-Route
umzuklassifizieren.

## Integrationsmodi

| Modus | Host und Rolle | Request-/Response-Sichtbarkeit | Kernroute oder Compatibility-Begriff | Bekannte Grenze |
|---|---|---|---|---|
| <code>native-httpd-module</code> | Apache-Modul, von httpd geladen | Host-Request-/Response-Hooks und Filter | Ausgewählte Apache-Kernroute | Response-Body-Entscheidungen können bei EOS finalisieren; Evidence muss das tatsächliche Ergebnis zeigen |
| <code>native-nginx-http-module</code> | NGINX-HTTP-Modul | NGINX-Request-/Response-Verarbeitung | Ausgewählte NGINX-Kernroute | Host-Konfiguration, Worker-Berechtigungen und Runtime-Artefakte bleiben profil-spezifisch |
| <code>native-htx-filter</code> | Nativer HAProxy-HTX-Filter | HTX-Request-/Response-Repräsentation | Ausgewählte HAProxy-Kernroute | HTX-/EOS-Semantik ist kein Claim vollständiger Transport- oder Protocol-Abdeckung |
| <code>ext_proc</code> | Envoy External-Processing-Bridge | Streamed Host-/Processor-Austausch | Ausgewählte Envoy-Kernroute | Ein Processor-/gRPC-Event ist nicht automatisch ein Nachweis eines client-sichtbaren Strict-Resets |
| <code>native-traefik-middleware</code> | Native Traefik-Middleware mit lokalem UDS-Service | Middleware-Request-/Response-Pfad durch lokale Engine | Aufgezeichneter ausgewählter Traefik-Modus | UDS-Lokalität und Source-Wiring beweisen nicht selbst Strict-Transport-Verhalten |
| <code>patched-native-lighttpd</code> | Gepatchter nativer lighttpd-Core plus Modul | HTTP/1-Entity-Body-Ranges vor Transfer-Framing | Aufgezeichneter ausgewählter lighttpd-Modus | Patch-/Build-Existenz und EOS-Wiring benötigen Run-Artefakte für eine Ergebnisaussage |
| <code>ext_authz</code> | Envoy-Service für externe Autorisierung | Normalerweise Pre-Upstream-Authorization-Sicht | Compatibility-/alternativer Begriff | Beobachtet die spätere Upstream-Response nicht wie ext_proc |
| <code>forwardAuth</code> | Traefik-Forward-Auth-Integration | Authorization-Request-/Response-Entscheidung | Compatibility-/alternativer Begriff | Nicht als Native-Middleware-Evidence umbenennen |
| <code>spoe-spop-agent</code> | HAProxy-Agent-/Protocol-Vokabular | Agent-vermittelter Request-/Response-Pfad | Compatibility-/alternativer Begriff | Nicht mit der ausgewählten nativen HTX-Filter-Identität gleichsetzen |

<code>EOS</code> bedeutet End of Stream, <code>HTX</code> ist die interne
HTTP-Transaction-Repräsentation von HAProxy und <code>UDS</code> ein Unix
Domain Socket. Vollständige Definitionen stehen im
[Glossar](../reference/glossary.de.md).

## Target-Karte

| Aufgabe | Target | Wichtige Eingabe | Ausgabe / Einschränkung |
|---|---|---|---|
| Einen Connector bauen | <code>make build-<connector></code> | Sicherer <code>BUILD_ROOT</code>; Host-Voraussetzungen | Nur Build-Ausgabe; keine Runtime-Aussage |
| Eine Konfiguration prüfen | <code>make check-config-<connector></code> | Vorbereiteter ausgewählter Host/Config | Config-Load-Diagnostik; kein Traffic |
| Einen minimalen Smoke ausführen | <code>make runtime-smoke-<connector></code>, wo bereitgestellt | Vorbereiteter Host und sichere Runtime-Pfade | Fokussierte Runtime-Ausgabe; keine Full-Lifecycle-Evidence |
| Die ausgewählte No-CRS-Baseline ausführen | <code>make no-crs-baseline-<connector></code> | <code>NO_CRS_RULES_FILE</code>, sichere Pfade | Capability-ausgewählte Candidate-Evidence |
| Einen Full Lifecycle ausführen | <code>make full-lifecycle-<connector></code> | Target-gemanagte Profil-Identität; <code>NO_CRS_RUN_ID</code> empfohlen | Candidate-Full-Lifecycle-Artefakte |
| Einen Connector-Run validieren | <code>make evidence-check-<connector></code> | <code>NO_CRS_RUN_ID</code> oder letzte Run-ID, <code>EVIDENCE_ROOT</code> | Read-only-Evidence-Validierung |

Der Platzhalter <code>&lt;connector&gt;</code> erlaubt
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code> und <code>lighttpd</code>. Beispiel:

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-nginx
~~~

<code>NO_CRS_RUN_ID</code> ist eine sichere Kennung für einen Evidence-Satz.
Sie ist für explizite Evidence-Gates erforderlich, hat keinen festen
Root-Default und darf weder Secrets, persönliche Daten, Schrägstriche noch
Traversal-Segmente enthalten. Das Beispiel behauptet nicht das Ergebnis des
Kommandos; prüfen Sie die erzeugten Artefakte und das Validierungsergebnis.
Siehe [Konfigurationsvariablen](../reference/variables.de.md#no-crs-und-evidence-variablen).

## Konfigurationsvariablen und Platzhalter

Die zentrale [Variablenreferenz](../reference/variables.de.md) dokumentiert
Format, Default, Setter, Scope, Auswirkung und Sicherheit für Root-Variablen
und direkte Harness-Controls. Die kompakten connector-spezifischen Gruppen sind:

| Connector | Typische direkte Variablen | Vor Verwendung prüfen |
|---|---|---|
| Apache | <code>APACHE_HTTPD</code>, <code>APXS</code>/<code>APXS_BIN</code>, <code>APACHE_MODULE</code>, <code>HTTPD_PREFIX</code>, <code>PORT</code> | Vertrauenswürdige Host-/Modul-Pfade und einen Loopback-Port |
| NGINX | <code>NGINX_BINARY</code>, <code>NGINX_MODULE</code>, <code>NGINX_PREFIX</code>, <code>NGINX_HARNESS_PARENT</code>, <code>NGINX_WORKER_USER</code> | Modul-/Binary-Kompatibilität und Worker-Zugriff auf Runtime-Pfade |
| HAProxy | <code>HAPROXY_BIN</code>, <code>SPOA_RUNTIME_BIN</code>, <code>HAPROXY_HTX_CANONICAL_RULES_FILE</code>, Port-Offsets | Vertrauenswürdige Host-/Agent-Binaries und konfliktfreie Loopback-Ports |
| Envoy | <code>ENVOY_BIN</code>, <code>EXT_PROC_BIN</code>, <code>ENVOY_CONFIG</code>, <code>EXT_PROC_PORT</code> | Generierte Config außerhalb des Checkouts und gültige lokale Ports |
| Traefik | <code>TRAEFIK_BIN</code>, <code>TRAEFIK_NATIVE_RUNTIME_ROOT</code>, <code>TRAEFIK_ENGINE_SOCKET_PARENT</code>, <code>TRAEFIK_CONNECTOR_CONFIG</code>, <code>TRAEFIK_CONNECTOR_LISTEN</code> | Vertrauenswürdiges Binary, privater Runtime-/Socket-Elternpfad, Loopback-Listen-Adressen |
| lighttpd | <code>LIGHTTPD_BIN</code>, <code>LIGHTTPD_PATCHED_ROOT</code>, <code>LIGHTTPD_CONNECTOR_MODULE</code>, <code>LIGHTTPD_SMOKE_PORT</code> | Passender gepatchter Host/Modul, absolute externe Pfade, gültiger Loopback-Port |

Namen in dieser Tabelle versprechen nicht, dass jeder direkte Override für CI
oder kanonische Evidence geeignet ist. Die Root-Targets setzen kompatible
invocation-lokale Werte und sind vorzuziehen.

## Status- und Evidence-Grenze

Verwenden Sie <code>PASS</code>, <code>FAIL</code>, <code>BLOCKED</code>,
<code>NOT EXECUTED</code>, <code>NOT APPLICABLE</code> und
<code>UNSUPPORTED</code> genau wie unter
[Tests und Nachweise](../testing-and-evidence.de.md) definiert. Eine Capability kann
<code>implemented_not_asserted</code> sein, ohne dass ein konkreter
kanonischer Lauf bestanden hat. Umgekehrt wird ein Evidence-Run gegen sein
ausgewähltes Profil, Rules, Case-Anforderungen und Artefakte ausgewertet; er
zertifiziert keine nicht ausgewählten Protocols oder Compatibility-Pfade.

Lesen Sie [Tests und Nachweise](../testing-and-evidence.de.md), bevor Sie ein Connector-
Ergebnis in Report oder Claim verwenden.

## Neuer- und Future-Connector-Vertrag

Ein neuer Connector deklariert zuerst Origin, Fähigkeiten,
Konfigurations-Mapping, Request-/Response-Mapping, Decision-/Event-Mapping und
Artefaktlayout. Er behält Host-API-Typen, Hooks, Filter, Protocol-Framing,
Build-Kleber und Objektlebensdauer im Connector-Tree. Er darf Common-
Request-/Response-/Config-Verträge und den Generic Mapper nur verwenden, wenn
die Hostdaten in diese Verträge passen; Body-Payloads werden über diesen Pfad
nie protokolliert.

| Anforderung | Vor einem Laufzeitclaim |
| --- | --- |
| Konfiguration | Hostsyntax registrieren und hostspezifische Parser-Typen lokal halten |
| Mapping | Gemappten Request-/Response-Output gegen Common-Verträge validieren |
| Provenienz | Origin-Metadaten, Capability-Manifest und ausgewählten Modus pflegen |
| Tests | Reales Host-Harness und payload-sichere Laufartefakte bereitstellen |
| Status | Starterpfade bis zu passender Laufzeit-Evidence nicht verifiziert halten |

Zukünftige Hostarbeit folgt derselben Selected-Route-Regel wie die sechs
aktuellen Connectoren. Ein Source-Scaffold, Generic Mapper, kompatible API oder
Buildsmoke etabliert keinen Real-World-Connector-Pfad.

## Evidence-Vertrag für neue Connectoren

Ein neuer Connector hält Host-Hooks, Parserregistrierungen, Body-/Response-
Verarbeitung, Protocol-Framing, Build-Glue, Objektlebensdauer und
host-spezifische Diagnostik in seinem Connector-Baum. Sein Repository-Guide ist
die kanonische leserorientierte Erklärung; code-nahe Dateien zeichnen
Provenienz und lokale Ausführungsdetails auf. Keinen connector-lokalen
Testbaum erstellen: wiederverwendbare ausführbare Cases, Schemata und Runner
bleiben Framework-eigen.

| Erforderliches Artefakt | Mindestens aufgezeichneter Inhalt | Grenze |
| --- | --- | --- |
| <code>README.*</code> | Ausgewählte Route, lokale Build-/Harness-Entry-Points und explizite Grenzen | Source- oder Konfigurationspräsenz ist keine Runtime-Evidence |
| <code>TODO.md</code> | Offene Integrations-, Coverage- und Promotion-Arbeit | Ein abgehakter Punkt ist kein Result-Datensatz |
| <code>ORIGIN.md</code> und Source-Map | Upstream-Wahl, Lizenz, importierte Dateien, lokale Änderungen und Pins | Source-, Lizenz-, Versions- oder API-Fakten niemals erfinden |
| <code>metadata.*</code> und Build-Glue | Connector-Identität, eigene Build-Inputs, Pfade und Prerequisite-Verhalten | Ein Compile-/Link-Check ist kein Hostverkehr |
| Harness und lokale Konfiguration | Exakte ausgewählte Host-/Profile-Inputs und payload-sicherer Ausgabeort | Ein Start-/Config-Check ist kein Lifecycle-Ergebnis |
| Framework-Case-/Catalog-Referenzen | Case-Scope, Ruleset-Variante, Runner und Result-/Evidence-IDs | Framework-Tests nicht nach <code>connectors/&lt;name&gt;/tests</code> kopieren |

## Evidence- und Promotion-Bedingungen

Vor einem eingegrenzten Claim Befehl, Exit-Verhalten, Connector-Scope,
ausgewähltes Profil, Ruleset, Run-ID, effektive nicht geheime Konfiguration,
Result-/Event-Artefakte und PASS/FAIL/BLOCKED/NOT EXECUTED aufzeichnen. No-CRS-
und With-CRS-Varianten bleiben getrennt: Eine ersetzt niemals die andere. Die
Mindestprüfungsmatrix umfasst P1, P2, P3, P4, Response-Body-Verhalten,
Negative-/Pass-Through-Verhalten, Audit-/Log-Beobachtungen,
Konfigurations-/Startup-Verhalten und verbleibende blockierende oder fehlerhafte
Zeilen.

| Scope-Label | Mindestens aufgezeichnete Grundlage | Unzureichende Grundlage |
| --- | --- | --- |
| <code>template</code> oder <code>scaffolded</code> | Nur Struktur- und Dokumentationsanforderungen | Abgeleitetes Hostverhalten |
| <code>adapter-owned</code> | Eigene Source-/Build-Metadaten plus Provenienz | Vermuteter Upstream oder kopierte Kompatibilitätsbeschreibung |
| <code>runtime-smoke-verified</code> | Aktueller ausgewählter Host-Smoke mit Befehl und Result-Artefakten | Statischer Source, generierter Report oder reiner Prozessstart |
| <code>crs-verified</code> | Aktueller ausgewählter With-CRS-Lauf, effektives CRS-Input und Result-Artefakte | Ein No-CRS-Ergebnis |
| <code>partial</code> | Wahrheitsgemäß begrenzte Struktur oder ausgewählte Evidence | Claim vollständiger Phasen-, Protocol- oder Matrix-Coverage |
| Mehr als <code>partial</code> | Geprüfte Matrix und Evidence für jede beanspruchte Fähigkeit; Lücken bleiben explizit | Pass-Through-/Log-Only-Ausgabe als Response-Body-Blocking-Beweis |

Framework-Cases liegen unter
<code>modules/ModSecurity-test-Framework/tests/cases/</code>, optionale
connector-spezifische Cases unter
<code>modules/ModSecurity-test-Framework/tests/cases/connector-specific/&lt;connector&gt;/</code>
und Framework-Runner unter
<code>modules/ModSecurity-test-Framework/tests/runners/</code>. Nur Targets
zitieren, die im Parent-Makefile existieren, und vor der Ergebnisauswertung den
[Test-/Evidence-Guide](../testing-and-evidence.de.md) lesen.
