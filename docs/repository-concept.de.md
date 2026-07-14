# Repository-Konzept

**Sprache:** [English](repository-concept.md) | Deutsch

## Verbindlichkeit, Geltungsbereich und Claim-Disziplin

Dieses Dokument ist das verbindliche Zielkonzept für das Produkt-Monorepo. Es
definiert, wie die sechs Connector-Produkte, der gemeinsame Produktvertrag und
das unabhängige Test-Framework zusammengehören. Es ergänzt, ersetzt aber nicht,
die aktuelle [Architektur](architecture.de.md), die Connector-Guides,
Konfigurationsreferenzen und Evidence-Berichte. Wenn diese Quellen einander
widersprechen, sind relevanter Code, Tests, aktuelle Evidence und angenommene
Entscheidungen abzugleichen; der Widerspruch ist sichtbar zu machen statt
stillschweigend einen Claim zu wählen.

Das Konzept umfasst Apache, NGINX, HAProxy, Envoy, Traefik und lighttpd. Es ist
kein Claim über Production Readiness, Production Hardening, CRS-Vollständigkeit,
vollständiges HTTP/2/HTTP/3, vollständige Matrix oder Strict-Post-Commit-
Enforcement.

### Claim-Labels

Die folgenden Labels sind in diesem Dokument und in künftigen Entscheidungen
zu verwenden. Ein Label beschreibt die Stärke und den Scope der zitierten
Repository-Evidence; es erweitert niemals einen Claim über diese Evidence
hinaus.

| Label | Bedeutung | Verbotene Folgerung |
| --- | --- | --- |
| `verified` | Direkt durch untersuchtes Source-/Contract-Material oder durch einen ausdrücklich abgegrenzten kanonischen Evidence-Record mit Profil und Run-ID belegt. | Production Readiness oder Abdeckung außerhalb des zitierten Scopes. |
| `documented_not_runtime_verified` | Durch Prosa, Konfiguration, Metadaten oder einen generierten/informativen Record dokumentiert, ohne passende aktuelle Runtime-Evidence für das genannte Verhalten. | Eine Capability-Deklaration, einen Build oder ein Konfigurationsladen als PASS behandeln. |
| `compatibility_only` | Beibehaltener alternativer oder historischer Pfad, dessen Semantik und Evidence den ausgewählten Pfad nicht ersetzen. | Ihn als P1--P4-Evidence des ausgewählten Pfads umetikettieren. |
| `unknown` | Das untersuchte Repository-Material belegt den Fakt oder den aktuellen Promotion-Status nicht. | Hostverhalten, Ownership oder Readiness erraten. |
| `out_of_scope` | Bewusst außerhalb des ausgewählten Sechs-Connector-HTTP/1.1-Kerns oder dieser Dokumentationsänderung. | Ihn ohne getrennte Arbeit als unsupported, implementiert oder verified bezeichnen. |

### Quellenhierarchie und Evidence-Grenze

| Quellenklasse | Verbindlichkeit für dieses Konzept | Aktueller Status |
| --- | --- | --- |
| Produkt-Source, eingecheckte Contracts und fokussierte Tests | Implementierungs-Ownership, Lifecycle-Invarianten und Build-/Contract-Verhalten. | `verified` für den zitierten Source-Contract; für sich kein Runtime-Nachweis. |
| Aktuelle Architektur und Connector-Guides | Aktueller ausgewählter Pfad und dokumentierte Grenze. | `verified` als Dokumentationsstruktur; Runtime-Claims benötigen weiterhin Run-Evidence. |
| `reports/current/core-completion.md` und `reports/current/readiness.md` | Abgegrenzte Selected-Core-Berichtsaussage für Run `six-connectors-core-final-20260712T164725Z-e16e7f1`. | Hier `documented_not_runtime_verified`, weil rohe kanonische Artefakte nicht unabhängig revalidiert wurden; niemals ein Production-Claim. |
| `connectors/*/capabilities.json` und generierte Capability-Kataloge | Capability- und Source-Grenzen-Deklarationen. | `documented_not_runtime_verified`; allein niemals Runtime-Promotion. |
| `reports/testing/generated/` | Generatorverwaltete Berichtssnapshots. | `unknown` für aktuelle Promotion, wenn Report-Freshness `stale`, `skipped` oder `skipped_stale_input` meldet. |
| `.codex/context/` und lokales `AGENTS.md` | Lokale Arbeitsunterstützung und Codex-Anweisungen. | Als versionierte Produktquelle `out_of_scope`; sie ersetzen dieses Konzept nicht. |

## Produktvision und ausdrückliche Nichtziele

Das Repository ist ein Produkt-Monorepo für libmodsecurity-basierte
Connector-Produkte. Es löst das gemeinsame Produktproblem, einen gemeinsamen
ModSecurity-Transaktionsvertrag auf sechs verschiedene HTTP-Server- oder
Proxy-Host-APIs anzuwenden und dabei hostspezifische Hooks, Filter, Services,
Middleware, Konfiguration, Build, Packaging, Installation und
client-sichtbare Aktionen beim zuständigen Adapter zu halten.

libmodsecurity stellt Rule Engine und transaktionsnahe Operationen bereit. Es
stellt für dieses Repository kein Apache-Modul, NGINX-Modul, HAProxy-Filter,
Envoy-External-Processor, Traefik-Middleware oder lighttpd-Modul bereit. Die
Connector- und `common/`-Schichten mappen begrenzte Hostdaten auf die Engine und
mappen eine Engine-Interventionsanforderung zurück auf eine Hostaktion.

Das Framework-Submodul ist ein unabhängiges Repository für wiederverwendbare
Tests. Es besitzt wiederverwendbare Cases, Runner, Normalizer, Katalogauswahl,
Schemas und Report-Generierung. Der Parent besitzt das eigentliche
Connector-Produkt, seinen hostspezifischen Ausführungsseam und die kanonischen
Host-Artefakte, die ein Framework-Workflow normalisieren und validieren kann.

Dieses Repository ist keine zweite allgemeine Testplattform, kein Ersatz für
libmodsecurity, keine universelle Host-ABI, kein Ablageort für generierte
Runtime-Ausgabe und keine Garantie, dass jeder Host, jedes Protokoll, jedes
Regelwerk, jede Konfiguration oder jeder Late-Intervention-Modus in Production
unterstützt wird.

## Monorepo-Grenze und Änderungsrouting

Die Grenze ist absichtlich einfach:

```text
Parent repository:
How is the product built and attached to the selected host?

Framework repository:
How is the product checked for correct, secure, and consistent behavior?
```

| Grenze | Owner und Inhalte | Besitzt nicht | Änderungsziel |
| --- | --- | --- | --- |
| Parent-Repository | Produktiver Connector-Source, `common/`, Buildsysteme, Connector-Konfiguration, Packaging-/Installationsmaterial, Connector-Dokumentation, Produkt-Contracts, hostspezifische Harness-Seams und Artefaktproduzenten. | Einen zweiten wiederverwendbaren Case-Katalog, generischen Normalizer oder allgemeine Testplattform. | Dieses Repository. |
| `modules/ModSecurity-test-Framework` | Wiederverwendbare Testfälle, Regelkataloge, Runner und wiederverwendbare Harness-Logik, Schemas, Normalizer, connectorübergreifender Vergleich, wiederverwendbare Smoke-/Integration-Logik und kanonische Testreport-Generierung. | Connector-Implementierung, Host-Hook-Code, Host-Build-Konfiguration oder eine Connector-Promotion-Entscheidung. | Das Framework-Repository und sein eigener Change Record. |
| Externe Host- und ModSecurity-Quellen | Gepinnte oder ausgewählte Upstream-Host-/Engine-Inputs, Lizenzen, Provenance und externe Runtime-Abhängigkeiten. | Parent-Produkt-Source-Ownership, sofern nicht mit expliziter Attribution importiert. | Der relevante externe Source-Prozess und Parent-Provenance-Records. |
| Externe Build-, Cache-, Runtime-, Log- und Evidence-Roots | Invocation-lokale Ausgaben, ausgewählt durch dokumentierte Variablen wie `BUILD_ROOT`, `EVIDENCE_ROOT` und `VERIFIED_RUN_ROOT`. | Versionierter Source, Secrets oder dauerhafte Produktdokumentation. | Außerhalb beider Checkouts. |
| Generierte Reports und Inventare | Generator-eigene Ausgabe unter Pfaden wie `reports/testing/generated/`. | Manuelle Korrekturen oder neue Runtime-Ergebnisse. | Ihr Generator-/Source-Contract, niemals eine Handeingabe. |
| Manuell gepflegte Dokumentation und Change Records | Bilinguale Produktanleitung, Entscheidungen, aktuelle Report-Zusammenfassungen und Traceability. | Rohe Payloads, Secrets oder einen Ersatz für generierte Evidence. | Dieses Repository mit englisch-deutschen Begleitfassungen. |

Eine connector-neutrale Produktregel gehört nur dann nach `common/`, wenn sie
ohne Host-SDK kompiliert und funktioniert. Eine Host-API-Aktion,
Hostobjektlebensdauer, Host-Config-Parser, Build-/Packaging-Verhalten oder ein
hostspezifischer Runtime-Seam gehört nach `connectors/<name>/`.
Wiederverwendbare Cases, Normalizer, Runner oder Schemas gehören in das
Framework. Ein kleiner Parent-Test bleibt im Parent, wenn er Parent-Build-,
Konfigurations-, Artefakt-, Path-, Security- oder Adapter-Seam-Verhalten
schützt; ein Framework-Katalog-Case darf nicht in den Parent kopiert werden.

## Komponenten- und Abhängigkeitsmodell

Das Ziel ist ein gemeinsamer Produktvertrag mit hostspezifischen Adaptern,
nicht sechs unabhängige Produkte mit demselben Namen.

```text
                         +-------------------------------+
                         | common/                       |
                         | neutral types, lifecycle,      |
                         | limits, decisions, redaction   |
                         +---------------+---------------+
                                         ^
                                         |
        +----------------+---------------+---------------+----------------+
        |                |               |               |                |
 connectors/apache  connectors/nginx  connectors/haproxy connectors/envoy ...
        |                |               |               |                |
        +----------------+---------------+---------------+----------------+
                                         |
                              selected host API / service

 Parent build, configuration, and host-specific artifact producers
                                         |
                                         v
 Framework cases, normalization, validation, and generated reports
```

| Komponente | Verantwortung | Zulässige Abhängigkeiten | Verbotene Kopplung |
| --- | --- | --- | --- |
| `common/` | Host-neutrale C-first-Contracts, Runtime-Unterstützung, Lifecycle-Phasen, Limits, Decision-/Event-Shapes, Logging/Redaction und Mapper-Contracts. | libmodsecurity-nahe neutrale Implementierung und Standard-C-Funktionen. | Host-SDK-Objekte, Host-Hooks, Filter-Registrierung, Server-ABI, Host-Buffer-Ownership oder hostspezifische Late-Action. |
| `connectors/apache/` | Apache-Modul, APR-/Request-Pool-Handling, Hooks/Filter, Apache-Konfiguration, APXS-Build, Packaging-/Installationsinputs und Apache-Seam. | `common/`, libmodsecurity, Apache-/APR-APIs, Parent-Build/-Konfiguration. | Annahmen über NGINX-/HAProxy-/Envoy-/Traefik-/lighttpd-APIs oder einen duplizierten Shared Contract. |
| `connectors/nginx/` | NGINX-HTTP-Modul, Request-/Location-Konfiguration, Filter-/Access-Wiring, NGINX-Pools, Build- und Installationsinputs. | `common/`, libmodsecurity, NGINX-APIs, Parent-Build/-Konfiguration. | Apache-Ausdruckssemantik, andere Host-SDKs oder gehaltene Host-Buffer in Common. |
| `connectors/haproxy/` | Native HTX-Overlay/-Filter, HAProxy-Mapping, Konfiguration, Build-/Harness-Seam und getrenntes historisches SPOP-Material. | `common/`, libmodsecurity, HAProxy-HTX-APIs, Parent-Build/-Konfiguration. | `spoe-spop-agent` als nativen HTX-Produktpfad behandeln. |
| `connectors/envoy/` | Envoy-`ext_proc`-Service, Protocol-Mapping, generiertes Host-Konfigurationsmaterial, Build-/Harness-Seam und `ext_authz`-Compatibility-Material. | `common/`, libmodsecurity, Envoy-/gRPC-/Go-Interfaces, Parent-Build/-Konfiguration. | `ext_authz` als Response-Phasen-Evidence für `ext_proc` behandeln. |
| `connectors/traefik/` | Native Middleware, lokale UDS-Engine-Service-Client-/Server-Grenze, Traefik-Konfigurations-/Build-Seam und `forwardAuth`-Compatibility-Material. | `common/`, libmodsecurity, Go- und Traefik-Plugin-Interfaces, Parent-Build/-Konfiguration. | `forwardAuth` als Response-Phasen-Evidence für native Middleware behandeln. |
| `connectors/lighttpd/` | Gepatchtes natives lighttpd-Modul, Mapper- und gepatchte-Host-Grenze, Konfigurations-/Build-Seam und getrenntes Stock-/Sidecar-Compatibility-Material. | `common/`, libmodsecurity, ausgewählte lighttpd-APIs, Parent-Build/-Konfiguration. | Stock-/Sidecar-Verhalten als `patched-native`-Evidence behandeln. |
| `ci/` | Parent-Orchestrierung, sichere Path-Checks, Source-/Contract-Checks, Lifecycle-Stage-Invocation, Artefaktproduzenten und Report-Consumer. | Parent-Code, Root-Makefile und ausdrücklich delegierte Framework-Tools. | Wiederverwendbare Katalog-/Normalizer-Rolle des Frameworks ersetzen oder Host-Produktlogik einbetten, die in einen Connector gehört. |
| `config/` | Versionierte deklarative Test-/Konfigurationsinputs und Import-Status. | Parent-Dokumentation und Checker. | Runtime-Secrets, generierte Evidence oder Host-Implementierung. |
| `tests/` | Fokussierte Parent-Produkt-Contract-, Path-/Security-, Artefakt- und Adapter-Seam-Tests. | Parent-`ci/`, Root-Makefile und deklarierte Framework-Fixtures, wenn nötig. | Einen zweiten wiederverwendbaren Case-Korpus oder kanonisches Host-Runtime-Ergebnis. |
| `reports/` | Aktuelle manuell gepflegte Reports, Change Records, generierte Report-Orte und quellenbasierte Inventare. | Source-Contracts und Framework-Generatoren. | Manuelle Änderung generierter Ausgaben oder Speicherung roher Payloads/Secrets. |
| Framework-Submodul | Wiederverwendbare Tests, Kataloge, Normalizer, Schemas, Runner und Report-Generierung. | Deklarierte Connector-Inputs und Artefakt-Contracts. | Parent-Connector-Source oder hostspezifische Produkt-Build-Ownership. |

## Connector-Vertrag und fertiges Produkt

Jedes Verzeichnis `connectors/<name>/` ist der hostspezifische Produktadapter.
Es muss gemeinsame Regeln adaptieren; es darf gemeinsame Lifecycle-, Limit-,
Decision-, Logging-/Redaction-, Error- oder Ownership-Semantik nicht
unabhängig neu erfinden. Source, Build, Konfiguration, Packaging, Installation,
Dokumentation und ein Framework-naher Ausführungsseam definieren gemeinsam das
Produkt für diesen Host.

| Anforderung an das fertige Produkt | Erforderliche Bedeutung | Evidence-Grenze |
| --- | --- | --- |
| Reproduzierbarer Build | Ein dokumentiertes Target kann den ausgewählten Connector mit seinen deklarierten Inputs bauen. | Ein Build ist kein Host-Traffic-Nachweis. |
| Dokumentierte Abhängigkeiten | Host, libmodsecurity, Toolchain und externe Roots sind ohne Secret- oder Workstation-Annahmen benannt. | Discovery ist kein Runtime-Ergebnis. |
| Dokumentierte Installation und Packaging | Der hostspezifische Load-/Installationspfad ist explizit. | Installationstext ist kein Installed-Host-Claim. |
| Versionierte Konfiguration | Ausgewählte Host- und Common-/Engine-Inputs sind versioniert und referenziert. | Eine Konfigurationsdatei ist kein Capability-Ergebnis. |
| Vollständige Host-Anbindung | Die ausgewählte Hostintegration besitzt Hooks, Filter/Service/Middleware, Mapper und Action-Pfad. | Source-Präsenz ist kein Lifecycle-PASS. |
| P1--P4-Lifecycle im unterstützten Scope | Der Host mappt nur den dokumentierten Phasen-Scope und EOS-/Commit-Grenzen. | Der Scope schließt nicht ausgewählte Protocol-/Strict-Verhalten aus. |
| Ownership und Cleanup | Resource-Owner, geliehene Daten, Error-Pfade und One-Time-Finish-/Destroy-Regeln sind dokumentiert. | Eine statische Regel ist keine Resilience-Evidence. |
| Definierte Intervention und Errors | Angeforderte Engine-Action und tatsächliche Host-Action-/Error-Abbildung sind unterscheidbar. | Eine Engine-Decision beweist keine client-sichtbare Action. |
| Englische und deutsche Dokumentation | Lesergerichtete Produktanleitung besitzt vollständige Begleitfassungen. | Strukturelle Parität allein beweist kein semantisches Verhalten. |
| Framework-Integration | Der Connector liefert einen Adapter-Seam und vom Framework konsumierbare Artefakte. | Ein Framework-Starter oder generierter Report ist keine Host-Promotion. |
| Test- und Evidence-Pfad | Build-/Konfigurations-/Smoke-/Lifecycle-/Evidence-Targets und Ergebnisgrenzen sind dokumentiert. | Eine Ebene promotet keine andere. |
| Kein nicht gestützter Readiness-Claim | Bekannte Evidence-Grenzen und `NOT EXECUTED`-Arbeit bleiben sichtbar. | Kein Connector wird durch Deklaration production ready. |

## Tatsächlicher Datenfluss und Lifecycle

Dies ist die gemeinsame tatsächliche Form, die durch Common Runtime,
Connector-Guides und den Selected-Run-Contract belegt ist. Ein Host kann Hook,
Filter, Service oder Middleware verwenden, darf aber die Ownership- und
Phasenregeln nicht umgehen.

```text
Client
  -> selected Host or Proxy
  -> Connector hook, filter, service, or middleware
  -> Host mapper
  -> Common Runtime and/or libmodsecurity
  -> requested decision and host intervention or forwarding
  -> logging and cleanup
  -> invocation-local raw evidence
  -> Framework normalization
  -> validation and reports
```

Die Common Runtime besitzt Engine, Rules, Konfigurationsstrings und interne
Transaction-Metadaten. Sie leiht einen gemappten Request/Response oder
Body-Chunk nur für den entsprechenden Aufruf. Der Host besitzt seine Objekte,
Buffer, Wire-Semantik und Commit-Semantik der Response.

| Schritt | Konsumierte Daten und Commit-Grenze | One-Time-Regel | Ergebnisgrenze |
| --- | --- | --- | --- |
| P1 | Connection-Metadaten, URI und Request-Header vor einer zulässigen Request-Action. | Connection/URI/Header genau einmal pro Transaction verarbeiten; keinen abgeschlossenen Request-Kontext wiederverwenden. | Eine Pre-Request-Decision kann nur vor dem Commit der relevanten Response durch den Host actionierbar sein. |
| P2 | Begrenzte Request-Body-Chunks; die Phase endet bei ausgewähltem Request-EOS. | Chunks dürfen sich wiederholen; `finish_request_body` erfolgt genau einmal, danach kein Append. | Ein ausgewähltes P2-Ergebnis beweist kein allgemeines Host-Streaming- oder Forwarding-Verhalten. |
| P3 | Response-Status und -Header vor oder an der Header-Commit-Grenze des Hosts. | Response-Header genau einmal vor P4 verarbeiten. | Eine angeforderte Action ist nur client-sichtbar, wenn der Host die Response noch ändern kann. |
| P4 | Begrenzte Response-Body-Chunks nach P3; die Phase endet bei ausgewähltem Response-EOS. | Chunks dürfen sich wiederholen; `finish_response_body` oder unobserved completion erfolgt genau einmal, danach kein Append. | Action nach Commit ist hostspezifisch; Safe zeichnet ein konservatives tatsächliches Ergebnis auf statt eine committed Response umzuschreiben. |
| Logging und Cleanup | Finaler Transaction-State, begrenzte Metadaten, tatsächliche Host-Action und Artefakt-Provenance. | `finish` friert den Common-Flow ein; destroy ist an der Ownership-Grenze idempotent. | Logs/Events sind payload-sichere begrenzte Artefakte, keine allgemeine Runtime-Garantie. |

| Hostunterschied | Ausgewähltes dokumentiertes Verhalten | Status |
| --- | --- | --- |
| Apache | Request-/Output-Filter leihen APR-Buckets; P2/P4 enden bei EOS; Response-Decisions hängen vom Output-Commit ab. | `verified` Source-Contract; Selected-Core-Evidence ist abgegrenzt. |
| NGINX | Der Host liefert den Request-Body zunächst vollständig; der Connector iteriert ihn, daher ist P2 kein End-to-End-Request-Streaming. Response-Chains nutzen Filter-/EOS-Handling. | `verified` Source-Contract; kein Request-Streaming behaupten. |
| HAProxy | Native HTX leitet aktuelle Blocks weiter und finalisiert am HTTP-Ende; Native HTX und SPOP sind getrennt. | `verified` Source-Contract. |
| Envoy | `ext_proc` mappt einen gestreamten gRPC-Austausch; Request-/Response-EOS oder Trailer schließen die relevante Phase. | `verified` Source-Contract; `ext_authz` ist `compatibility_only`. |
| Traefik | Native Middleware und ihr lokaler UDS-Engine-Service halten eine Transaction pro Request; ResponseWriter-Commit begrenzt späte Action. | `verified` Source-Contract; `forwardAuth` ist `compatibility_only`. |
| lighttpd | Gepatchte native Hooks erhalten geliehene Identity-Entity-Ranges und ein EOS; Short Writes oder nicht ausgewählte Modi dürfen keine doppelte Ingestion verursachen. | `verified` Source-Contract für den ausgewählten Patch; breite Fault Tolerance ist `out_of_scope`. |

Für den aufgezeichneten Selected Core sagt `reports/current/core-completion.md`,
dass P1, P2, P3, P4-Rule-Evaluation, Safe-Late-Action, erstes Byte vor
Upstream-EOS, kein connector-eigener vollständiger Response-Buffer und Cleanup
für Run `six-connectors-core-final-20260712T164725Z-e16e7f1` bestanden haben.
Das ist hier ein `documented_not_runtime_verified`-Report-Claim, weil diese
Aufgabe rohe kanonische Artefakte nicht unabhängig revalidiert hat. Er bleibt
auf die genannten HTTP/1.1-Core-Pfade und Cases begrenzt. Er behauptet keine
P4-Decisions pro Chunk, kein HTTP/2/HTTP/3, kein CRS, keinen vollständigen
Katalog, kein Strict-Post-Commit-Enforcement und keine Production Readiness.

## Ownership- und Cleanup-Invarianten

Ownership ist ein Produktvertrag. Ein Connector muss jede Resource auf
Success, terminaler Intervention, Parser-Fehler, Host-Cancellation und
Startup-Fehler freigeben, ohne einen Host-Pointer über seinen gültigen Callback
hinaus zu behalten.

| Resource | Owner | Borrower oder Consumer | Erforderliche Cleanup-Invariante |
| --- | --- | --- | --- |
| Host-Request-/Response-Objekt | Ausgewählter Host | Connector-Mapper und Common-Call-Grenze | Hostobjekt niemals in `common/` behalten; durch den Host-Lifecycle freigeben. |
| Apache-APR-Pools, Request-Kontext und Brigades | Apache/Request-Pool | Apache-Adapter während Hook-/Filter-Ausführung | Request-lokalen State im Request-Pool allokieren; Redirect-Daten in diesen Pool kopieren; Transaction beim Request-Cleanup freigeben. |
| NGINX-Request-Pool, Location-Konfiguration und Chains | NGINX | NGINX-Adapter und Common-Call-Grenze | Request-Kontext/Redirect-Kopie in `r->pool` halten; Chain-Buffer-Pointer nach Filter-Call nicht behalten; Transaction mit Request-Pool-Cleanup bereinigen. |
| HAProxy-HTX-Blocks und Filter-Kontext | HAProxy besitzt HTX; Filter besitzt eigenen Kontext/Snapshots | HTX-Adapter und Common-Call-Grenze | Nur aktuelle HTX-Daten leihen; Transaction und begrenzte Snapshots bei Detach, Reset, Reply und Error freigeben. |
| ModSecurity-/Common-Transaction | Common-Runtime-Transaction-Objekt und native Engine-Transaction | Connector ruft Phase-APIs auf | Erst nach erforderlichem EOS-State finishen, dann genau einmal destroyen; native Transaction auch auf Error-Pfad bereinigen. |
| Engine/Runtime, Rules und Runtime-Konfigurationsstrings | `common/` Runtime | Connector-Setup/-Shutdown | Einmal für den konfigurierten Owner-Scope erstellen; Event-Datei, Engine, Rules und kopierte Konfiguration beim Runtime-Destroy schließen. |
| Intervention und Redirect-URL | Host-Adapter besitzt Host-Materialisierung; Common-Decision trägt nur begrenzte Daten | Host-Action-Mapper | Redirect/Location vor Nutzung in die Host-Request-Lebensdauer kopieren; keine Caller-eigenen URL-Pointer behalten. |
| Request-/Response-Body-Buffer | Host | Common-Append-Call | Begrenzte Views/Kopien nur für den Call übergeben; Zähler und Trunkierung verfolgen, niemals einen connector-eigenen Cross-Callback-Full-Response-Buffer. |
| Go-Request-State und CGo-Slices | Envoy-/Traefik-Service oder Middleware-Request-Scope | Common-/libmodsecurity-Bridge | Transiente Go-Slice-Daten bei Bedarf für einen CGo-Call kopieren; Stream-/Request-Map-State entfernen und Transaction bei EOF, Error oder normaler Completion finishen/destroyen. |
| UDS-Listener, Connection und Service-Session | Traefik-Native-Service-Prozess | Middleware und Protocol pro Request | Socket-Berechtigungen und Lokalität beschränken; Connection/Session und serverseitige Transaction bei normalem Finish, Client-EOF, Protocol-Error oder Startup-Fehler schließen. |
| Raw Evidence und Logs | Invocation-ausgewählter externer Evidence-/Log-Root | Parent-Producer und Framework-Consumer | Payload-frei, nach Connector/Profil/Run-ID begrenzt halten, Secrets redigieren und keine Runtime-Ausgabe committen. |

Die Common-API weist Body-Append nach Finalisierung, Response-Body-Arbeit vor
Response-Headers, doppelte Host-Action-Aufzeichnung und Transaction-Finish mit
unfertiger ausgewählter Streaming-/EOS-Phase zurück. Das sind `verified`
Source-Invarianten. Ein Connector muss sie auch dann erhalten, wenn sein
Host-Callback-Modell abweicht.

## Connector-Profil-Crosswalk

Ausgewählter Pfad, Compatibility-Begriff und seine Evidence stehen absichtlich
in getrennten Spalten. Aus einem alternativen Profil oder einem stale
Capability-Manifest darf kein Selected-Route-Support abgeleitet werden.

| Connector | Ausgewählter Produktpfad | Compatibility-Pfad | Hostintegration und Engine-Grenze | Unterstützter ausgewählter Phasen-Scope | Runtime-/Evidence-Status | Bekannte Grenze | Build-, Check-, Smoke- und Lifecycle-Targets |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | `native-httpd-module` | Kein separater benannter Alternativpfad ist ausgewählt; Legacy-Directive-Erwartungen sind kein ausgewählter Pfad. | Natives httpd-Modul mit Common-/libmodsecurity-Mapping. | P1--P4, EOS-basiertes P2/P4. | Aktueller Report sagt `PASS`; hier `documented_not_runtime_verified`, ebenso Capability-Deklarationen. | Safe nach Commit ist konservativ; Strict-client-sichtbares Verhalten wird nicht breit behauptet. | `build-apache`, `check-config-apache`, `start-smoke-apache`, `runtime-smoke-apache`, `full-lifecycle-apache`, `evidence-check-apache` |
| NGINX | `native-nginx-http-module` | Kein separater benannter Alternativpfad ist ausgewählt; Apache-Syntax ist nicht kompatibel. | Natives NGINX-HTTP-Modul mit Common-/libmodsecurity-Mapping. | P1--P4; Host-vorbereiteter P2-Body und Filter-/EOS-P4. | Aktueller Report sagt `PASS`; hier `documented_not_runtime_verified`, ebenso Capability-Deklarationen. | Request-Body wird vom ausgewählten Adapter nicht End-to-End gestreamt; Strict-/Protocol-Claims bleiben getrennt. | `build-nginx`, `check-config-nginx`, `start-smoke-nginx`, `runtime-smoke-nginx`, `full-lifecycle-nginx`, `evidence-check-nginx` |
| HAProxy | `native-htx-filter` | `spoe-spop-agent` ist `compatibility_only`. | Nativer HTX-Filter und Common-/libmodsecurity-Mapping. | P1--P4 auf HTX-/EOS-Selected-Core. | Aktueller Report sagt `PASS`; hier `documented_not_runtime_verified`; Manifest-Mode-Divergenz ist ebenfalls `documented_not_runtime_verified`. | Safe P4 ist `log_only`; Strict-Post-Commit-Action ist im Selected Guide `not_attempted`. | `build-haproxy`, `check-config-haproxy`, `start-smoke-haproxy`, `runtime-smoke-haproxy`, `full-lifecycle-haproxy-htx`, `evidence-check-haproxy` |
| Envoy | `ext_proc` | `ext_authz` / `http-ext-authz-service` ist `compatibility_only`. | Gestreamter Envoy-External-Processor-Service mappt gRPC-Messages auf Common/libmodsecurity. | P1--P4 über ausgewählte Stream-/EOS-Grenze. | Aktueller Report sagt `PASS`; hier `documented_not_runtime_verified`; Manifest-Mode-Divergenz und generierter Capability-Status sind ebenfalls so gelabelt. | Strict Reset/Cancellation wird nicht allein durch eine Service-Decision etabliert. | `build-envoy`, `check-config-envoy`, `start-smoke-envoy`, `runtime-smoke-envoy`, `full-lifecycle-envoy-ext-proc`, `evidence-check-envoy` |
| Traefik | `native-middleware` / `native-traefik-middleware` | `forwardAuth` / `http-forwardauth-service` ist `compatibility_only`. | Native Go-Middleware kommuniziert mit einem privaten UDS-Common-/libmodsecurity-Engine-Service. | P1--P4 mit ResponseWriter-/EOS-Grenze. | Aktueller Report sagt `PASS`; hier `documented_not_runtime_verified`; Manifest-Mode-Divergenz und generierter Capability-Status sind ebenfalls so gelabelt. | Safe P4 ist `log_only`; nativer Strict-Abort bleibt getrennte Evidence-Arbeit. | `build-traefik`, `check-config-traefik`, `start-smoke-traefik`, `runtime-smoke-traefik`, `full-lifecycle-traefik-native`, `evidence-check-traefik` |
| lighttpd | `patched-native` / `patched-native-lighttpd` | Stock-native-, Sidecar- und Legacy-Bridge-Material ist `compatibility_only`. | Versionsgebundenes gepatchtes lighttpd-Modul mappt ausgewählte geliehene Entity-Ranges auf Common/libmodsecurity. | P1--P4 für ausgewählte HTTP/1-Identity-Entity-Ranges und EOS. | Aktueller Report sagt `PASS`; hier `documented_not_runtime_verified`; Manifest-Mode-Divergenz und generierter Capability-Status sind ebenfalls so gelabelt. | Compression, HTTP/2, nicht ausgewähltes Buffering und Strict-Client-Abort sind `out_of_scope`. | `build-lighttpd`, `check-config-lighttpd`, `start-smoke-lighttpd`, `runtime-smoke-lighttpd`, `full-lifecycle-lighttpd-patched`, `evidence-check-lighttpd` |

Das Root-Makefile behält Aliase wie `full-lifecycle-haproxy`,
`full-lifecycle-envoy`, `full-lifecycle-traefik` und
`full-lifecycle-lighttpd` für ihre ausgewählten Targets. Für Evidence und
Dokumentation ist die explizite Target-Identität zu verwenden, damit eine
Compatibility-Ausführung nicht als Full Lifecycle fehlklassifiziert wird.

## Konfigurationsvertrag und sicherheitsrelevante Defaults

Konfiguration hat getrennte Host-/Connector-, Common-Runtime- und
ModSecurity-Engine-Layer. Ein Wert auf einem Layer konfiguriert keinen anderen
implizit.

| Konfigurationsort oder Input | Owner | Zweck | Status und Grenze |
| --- | --- | --- | --- |
| `connectors/<name>/`, `examples/<name>/` und versionierte Profildateien | Parent-Connector | Hostsyntax, hostspezifische Service-/Middleware-/Filter-Konfiguration, Installations-/Build-Inputs und ausgewählte Profile. | Als versionierte Konfiguration `verified`; ein Load beweist keinen Traffic. |
| `common/runtime/msconnector_runtime.c` und `examples/common/` | Parent-`common/` | Neutrale `key=value`-Runtime-Konfiguration, Limits, Event-Pfad und Engine-Rule-Source. | `verified` Parser-/Source-Contract; ein Key ist keine Host-Directive. |
| `common/rules/` und Connector-Rule-/Konfigurationsinputs | Parent-Connector-Produkt | Targeted Rules und produkt-eigene ausgewählte Inputs. | Bis zur Nutzung durch passende abgegrenzte Evidence `documented_not_runtime_verified`. |
| `modules/ModSecurity-test-Framework/tests/` und Framework-Variablen | Framework | Wiederverwendbare Cases, Rules, Schemas, Katalogauswahl, Runner-Defaults und Normalisierung. | Framework-eigene Testinputs; der Parent zeichnet die hostspezifische effektive Konfiguration auf. |
| `BUILD_ROOT`, `EVIDENCE_ROOT`, `VERIFIED_RUN_ROOT`, Ports, Binary-Pfade und UDS-Pfade | Invocation-/CI-Operator | Externer Build-/Cache-/Runtime-/Log-/Evidence-Ort und Host-Launch-Werte. | Lokale/Runtim-Werte; niemals versionierte Secrets oder Capability-Nachweis. |
| Secrets, Credentials, Cookies, Tokens und private Schlüssel | Externer Secret-Mechanismus | Runtime-Authentisierung oder privater Deployment-Input, wenn nötig. | Für versionierte Beispiele, Reports und dieses Konzept `out_of_scope`. |

| Kontrolle | Quellenbasierter Default oder ausgewählter Wert | Security-Wirkung und Klassifikation |
| --- | --- | --- |
| `enabled` | Common-Runtime-Default `off`. | Bezogen auf Common-Enforcement fail-open, bis er explizit aktiviert wird; keine repositoryweite Host-Failure-Policy. |
| `request_body_limit`, `response_body_limit`, Header-Limits und `max_event_json_bytes` | Common-Runtime-Defaults begrenzen Body-/Header-/Event-Input. | Begrenzen Ressourcen und Metadatenexposition; ein höherer Wert beweist kein sicheres Buffering. |
| `body_limit_action` | Common-Runtime-Default `reject`. | Weist einen Chunk über dem Limit vor der Engine-Eingabe ab; die daraus folgende Host-Response bleibt connectorspezifisch. |
| `default_block_status` und `default_error_status` | Common-Runtime-Defaults `403` und `500`. | Definieren Fallback-Statuswerte, wo ein Host sie mappt; beweisen keine einheitliche fail-closed Response. |
| `response_body_mode` und `phase4_mode` | Common-Runtime-Defaults `none` und `safe`. | Standardmäßig wird kein P4-Input verarbeitet; Safe-Late-Verhalten ist konservativ und kann nach Commit `log_only` sein, keine universelle fail-open-/fail-closed-Policy. |
| Envoy `failure_mode_allow` | Ausgewählte `ext_proc`-Templates setzen `failure_mode_allow: false`. | Ausgewählte Konfiguration dokumentiert fail-closed Processor-Erreichbarkeit; keine Evidence für jedes Envoy-Deployment. |
| `rules_remote_url` und externe Downloads | Optionale Rule-/Source-Inputs. | Als externe Trust-Grenze behandeln: deklarierte Origin, Pin/Checksumme soweit vorhanden und kein stiller Fallback erforderlich. |

Die dokumentierten Selected-Core-Reports beschreiben Safe P4 als angefordertes
`deny`, tatsächliches `log_only`, sichtbares HTTP 200 und keinen
Connection-Abort nach einer committed Response. Das ist eine abgegrenzte
Late-Intervention-Beobachtung, kein globaler Availability- oder Security-
Default.

## Test-, Evidence- und Report-Modell

| Ebene | Was sie belegen kann | Was sie nicht belegen kann |
| --- | --- | --- |
| Syntax-Check | Die geprüfte Datei parst unter dem benannten Tool. | Produktverhalten, Host-Traffic oder Security. |
| Contract-Test | Den expliziten Source-, Schema-, Path-, Privacy- oder Wiring-Contract. | Eine echte Host-Ausführung. |
| Unit-Test | Ein fokussiertes Funktions- oder Komponentenverhalten mit testgesteuerten Inputs. | Einen Host-Lifecycle oder ein Production-Ergebnis. |
| Build | Der ausgewählte Source-/Build-Schritt schließt ab. | Konfigurationsladen oder Traffic-Verhalten. |
| Konfigurationscheck | Ausgewählte Konfiguration parst oder lädt. | Request-/Response-Verhalten oder Rule-Coverage. |
| Smoke-Test | Die enge Host-/Service-Übung, die sein Target benennt. | Full Lifecycle, Katalogvollständigkeit oder Promotion. |
| Runtime-Test | Seine ausdrücklich aufgezeichnete Hostbeobachtung. | Andere Profile, Protocols oder nicht aufgezeichnete Capabilities. |
| Full-Lifecycle-Test | Das ausgewählte Profil und erforderliche Artefaktproduktion. | Production Readiness, vollständige Matrix, CRS oder alle Protocols. |
| Kanonische Evidence | Ein run-scoped Ergebnis, gebunden an Connector, ausgewähltes Profil, Rules, Konfiguration, Run-ID und erforderliche Artefakte. | Einen neuen Run oder breiteren Produkt-Claim. |
| Generierter Report | Die Darstellung seiner deklarierten Inputs durch einen Generator. | Aktuelle Wahrheit, wenn seine Inputs stale oder fehlend sind. |
| Production-Release-Entscheidung | Eine getrennt reviewte Betriebsentscheidung. | Automatische Folge einer vorigen Ebene. |

Das getrackte Parent-Testinventar bei Basisrevision wird unten klassifiziert.
Die Klassifikation ist ein Placement-Review, keine Move-Anforderung; durch
diese Konzeptänderung werden keine Tests verschoben.

| Klassifikation | Getrackte Parent-Tests | Begründung und Folgeaufgabe |
| --- | --- | --- |
| `repository_governance` | `test_bilingual_docs.py`, `test_compiler_guides.py`, `test_make_runtime_defaults.py`, `test_runtime_path_policy.py`, `test_update_github_actions_versions.py` | Schützen Parent-Dokumentation, Tooling, Paths und Workflow-Contracts; im Parent behalten. |
| `parent_product_contract` | `test_c_cpp_diagnostics.py`, `test_connector_capabilities.py`, `test_full_lifecycle_profiles.py`, `test_no_crs_selected_runner_wiring.py`, `test_six_connector_core_completion.py` | Schützen Root-Lifecycle-Auswahl, Capability-, Compiler- und Parent-Orchestrierungs-Contracts; im Parent behalten. |
| `connector_local_seam` | `test_envoy_transport_hardening_contract.py`, `test_nginx_phase4_runner_wiring.py`, `test_nginx_protocol_harness_contract.py`, `test_response_header_backend.py`, `test_traefik_native_local_plugin.py`, `test_traefik_transport_hardening_contract.py` | Prüfen einen Host-/Produkt-Integrationsseam; beim Parent-Adapter halten, bis ein bewusster Framework-Interface existiert. |
| `framework_candidate` | `test_collect_no_crs_source.py`, `test_engine_lifecycle_artifacts.py`, `test_full_lifecycle_evidence.py`, `test_resolve_runtime_paths.py`, `test_runtime_env_snapshot_contract.py`, `test_transport_lifecycle_artifacts.py` | Schützen generische Normalisierung, Artefakte oder Runner-Isolation, kodieren aber auch Parent-Profile. Wiederverwendbare Interface-Logik nur durch eine bewusste Framework-Änderung abspalten. |
| `unclear` | `test_prepare_runtime_components.py`, `test_runtime_component_cache_contract.py`, `test_runtime_component_cache_identity.py` | Component-Preparation-/Cache-Policy umspannt Parent-Produkt und Framework-Provisioning. Dauerhaften Owner vor einem Move reviewen. |

Alle diese Root-Tests sind für Runtime-Zwecke `documented_not_runtime_verified`:
Sie sind Unit-/Contract-Tests und wurden für diese Dokumentationsänderung nicht
ausgeführt. Aktuelle generierte Reports müssen nach Freshness interpretiert
werden. Die generierte `report-freshness.generated.md` benennt den älteren Run
`2026-06-16T19-12-00Z-614c8049` und markiert viele Reports als `stale`,
`skipped` oder `skipped_stale_input`. Daher sind diese Snapshots für aktuelle
Promotion `unknown`. Sie überschreiben und verifizieren auch nicht unabhängig
den abgegrenzten aktuellen Core-Report; erst nach gültigen Inputs über ihre
Generatoren refreshen, niemals hand editieren.

## Security-Modell

| Grenze | Erforderliche Regel |
| --- | --- |
| Untrusted HTTP-Daten | Request-/Response-Method, URI, Header, Body-Ranges, Status und Protocol-Metadaten als untrusted behandeln; begrenzte neutrale Mappings vor Common-/Runtime-Nutzung validieren. |
| Limits und Buffering | Dokumentierte Header-/Body-/Event-Limits durchsetzen und keinen connector-eigenen vollständigen Response-Buffer über Callbacks hinweg halten. |
| Paths und Symlinks | Sichere externe Roots verwenden; Artefakt-/Config-Pfade validieren und Runtime-/Generated-Ausgabe nicht aus dem ausgewählten Root entweichen lassen. |
| Downloads und Provenance | Explizite Workflows, deklarierte Source/Pins/Checksummen soweit bereitgestellt und keinen stillen System-Binary- oder Network-Fallback verwenden. |
| Intervention-Ownership | Angeforderte Engine-Decision von bestätigter Host-Action trennen; Redirect-Daten in den Host-Owner kopieren; nach Commit kein client-sichtbares Ergebnis erfinden. |
| UDS und Services | Traefik-artige lokale Sockets privat, berechtigungsbeschränkt, begrenzt und auf allen Connection-Outcomes bereinigt halten. |
| TLS-Redirects und Header | Host-Validierung anwenden, bevor Redirect-/Location-Output gesetzt wird; Redirect-Tokens oder untrusted Header-Werte nicht ohne Sanitization loggen. |
| Logging und Redaction | Events/Results payload-frei und begrenzt halten; Bodies, Cookies, Authorization, Credentials, private Schlüssel und geheime Konfiguration auslassen. |
| CI und Workflows | Actions pinnen und Repository-Paths/-Contracts validieren; CI-Erfolg ist kein Host-Runtime-Security-Claim. |
| Failure-Policy | Eine hostspezifische fail-open-/fail-closed-Entscheidung dokumentieren; keine aus Common-Defaults oder Safe-P4-Verhalten ableiten. |

Dieses Konzept promotet kein bestätigtes Security-Finding. Unbestätigte
Scanner-Kandidaten oder historische Notizen bleiben unbestätigt, bis eine
Source-to-Sink-Analyse und der passende Evidence-Record sie validieren.

## Erweiterungsregeln für Feature oder neuen Connector

Für einen neuen Connector oder ein wesentliches connectorübergreifendes Feature
ist diese Reihenfolge einzuhalten:

1. Das Host-Integrationsmodell beschreiben und die Architekturgrenze festlegen.
2. Ausgewählte Lifecycle-Phasen, Commit-Grenze und explizite Ausschlüsse deklarieren.
3. `common/`-Contracts für neutralen Lifecycle, Limits, Decisions, Logging und Errors wiederverwenden.
4. Hostspezifische Mapper, Hooks/Filter/Services/Middleware und Actions in `connectors/<name>/` implementieren.
5. Ownership, geliehene Daten, Intervention-/Redirect-Lebensdauer und Cleanup auf Success- und Error-Pfaden dokumentieren.
6. Reproduzierbaren Build, Packaging/Installation und versionierte Konfiguration bereitstellen.
7. Parent-Produkt-Contract-Tests und einen hostspezifischen Seam nur für echtes Hostverhalten ergänzen.
8. Framework-Adapter erstellen oder anpassen; Framework-Cases, Schemas, Runner und Normalizer wiederverwenden.
9. Trust Boundaries, Limits, Redaction, Downloads, UDS-/Transport-Berechtigungen und Failure-Policy analysieren.
10. Vollständige englische und deutsche Produkt-, Connector-, Konfigurations-, Lifecycle- und Limitation-Dokumentation ergänzen.
11. Erforderliche Source-/Contract-/Konfigurationschecks ausführen und bei einem Runtime-Claim abgegrenzte Runtime-Evidence erzeugen.
12. Reports über ihren Generator erzeugen und frische kanonische Artefakte von stale Snapshots unterscheiden.
13. Change Record und jeden betroffenen ADR aktualisieren und beide mit finalem Diff und tatsächlichen Checks abgleichen.

## Aktuelle Abweichungen vom Zielkonzept

| Bereich | Gewünschter Zustand | Aktueller beobachteter Zustand | Abweichung | Empfohlene Folgeaufgabe | Priorität | Repository |
| --- | --- | --- | --- | --- | --- | --- |
| Verbindliches Zielkonzept | Eine explizite Produkt-Monorepo-Zielquelle. | Die aktuelle Architektur ist current-state-orientiert; ein Zielkonzept gab es nicht. | Durch dieses Dokument adressiert, vorbehaltlich Review/Annahme. | Dieses Konzept aktuell halten und künftige ADRs verlinken. | High | Parent |
| ADR-Prozess | Kleiner versionierter ADR-Prozess für dauerhafte connectorübergreifende Entscheidungen. | Es wurde kein ADR-Verzeichnis/-Prozess gefunden. | Durch `docs/decisions/README.md` adressiert; keine rückwirkenden ADRs werden angelegt. | `ADR-001` bis `ADR-005` nur annehmen, wenn jede Entscheidung bereit ist. | Medium | Parent |
| Capability-Integrationsmodi | Ausgewähltes Profil und Capability-Metadaten stimmen überein. | HAProxy-, Envoy-, Traefik- und lighttpd-Manifeste benennen Legacy-/Alternativmodi, während aktuelle Route-Dokumentation ausgewählte native Routen benennt. | `documented_not_runtime_verified` Metadaten-Divergenz. | Metadaten/Manifeste und Generatoren in einer getrennten reviewten Änderung angleichen. | High | Parent |
| Runtime-Report-Provenance | Ein aktueller profilpassender kanonischer Artefaktsatz stützt jedes Runtime-Label. | Aktuelle Reports zitieren `PASS` für `six-connectors-core-final-20260712T164725Z-e16e7f1`, rohe Artefakte wurden in dieser Aufgabe aber nicht unabhängig revalidiert. | Ihr Ergebnis ist hier `documented_not_runtime_verified`. | Rohe kanonische Artefakte auffinden/revalidieren, bevor ein aktueller Runtime-Status promotet wird. | High | Parent + Framework |
| Generated-Report-Freshness | Aktuelle Reports leiten sich aus frischen Inputs für geprüfte Revisionen ab. | Viele generierte Reports zitieren den älteren Input `2026-06-16T19-12-00Z-614c8049` und sind `stale` oder skipped. | Sie sind für aktuelle Promotion `unknown`. | Mit gültigen Inputs über den Generator reproduzieren/refreshen; nicht hand editieren. | High | Parent + Framework |
| Common-Design-Notiz | Aktuelle Designnotizen beschreiben ausgewählte Produktpfade. | `common/docs/design.md` ist als `scaffolded` markiert und behält historisches Sidecar-/Open-Connector-Material. | Sie widerspricht aktueller Route-Dokumentation, wenn sie als aktuelle Architektur gelesen wird. | Historische Abschnitte in einer getrennten bilingualen Dokumentationsaufgabe abgleichen oder archivieren. | Medium | Parent |
| Testgrenze | Generische Testlogik liegt im Framework; Parent behält Produkt-Contracts und Host-Seams. | Root-Test-README beschreibt die Regel, aber generische Normalisierungs-/Evidence-Logik und Framework-nahe Tests bleiben im Parent, während das Framework auch hostspezifisches Provisioning/Runner enthält. | `framework_candidate`- und `unclear`-Placement-Split; kein automatischer Move ist begründet. | Stabilen Framework-Interface etablieren, dann wiederverwendbare Logik abspalten und Connector-Profile/Host-Seams im Parent halten. | Medium | Parent + Framework |
| Generator-/Output-Ownership | Framework-eigene Reports besitzen einen deklarierten Generator und Output-Owner. | Framework-Generierung schreibt Coverage-/Runtime-Output unter Parent-`reports/testing/generated/`; ein Parent-Language-Switch-Postprocessor beteiligt sich ebenfalls. | Generator-/Output-Ownership ist geteilt und benötigt explizite Governance. | Finalen Ownership-Contract in einem ADR festhalten und manuelle Generated-File-Änderungen vermeiden. | Medium | Parent + Framework |
| Connector-Selbstständigkeit | Jeder Connector kann mit `common/` ein dokumentiert baubares/installierbares Produkt bilden. | Root-Targets und Connector-Material existieren, aber Packaging-/Installationsvollständigkeit ist nicht einheitlich durch einen aktuellen Evidence-Record belegt. | `documented_not_runtime_verified`. | Build-/Packaging-/Installationsvertrag jedes Connectors auditieren und abgegrenzte Ergebnisse aufzeichnen. | Medium | Parent |
| Einheitliche beobachtbare Contracts | Geteilte Phasen-, Limit-, Intervention-, Logging-, Cleanup-, Konfigurations- und Evidence-Bedeutung über Hosts hinweg. | Hostimplementierungen unterscheiden sich zwangsläufig; Selected Core ist abgegrenzt und Strict-/Protocol-Coverage unvollständig. | Unterschiede sind nur explizit zulässig; breitere Gleichwertigkeit ist `out_of_scope`. | Targeted Evidence-/ADR-Arbeit für Strict-Verhalten und Protocol-Scopes ergänzen. | Medium | Parent + Framework |

## Definitionen und bekannte Grenzen

| Begriff | Verbindliche Definition |
| --- | --- |
| supported | Eine Fähigkeit ist nur für den genannten Connector, das ausgewählte Profil, den dokumentierten Scope und die erforderliche Evidence-Stufe supported; niemals allein aus Source-Präsenz abgeleitet. |
| selected profile | Die explizite Profil-/Target-Identität des Root-Lifecycle-Contracts für einen Connector, etwa `ext_proc` oder `native-htx-filter`. |
| compatibility path | Ein getrennt beibehaltener alternativer, Legacy-, Beispiel- oder Migrationspfad, der ein ausgewähltes Profil nicht ersetzt. |
| experimental | Ein ausdrücklich als nicht stabil gelabelter Scope mit eigener Evidence und Limitationen; dieses Dokument labelt keinen Selected-Core-Pfad stillschweigend als experimental. |
| runtime verified | Ein run-scoped Claim, gestützt durch erforderliche kanonische Host-Artefakte, ausgewähltes Profil, effektive Konfiguration, Rule-Input und Result-/Event-Validierung. |
| not executed | Ein bewusst nicht ausgeführter Status; weder PASS noch FAIL oder unsupported. |
| blocked | Eine deklarierte Voraussetzung fehlt, ist unsicher oder absichtlich nicht verfügbar; kein negatives Capability-Ergebnis. |
| unknown | Die Repository-Evidence belegt Fakt, Verhalten, Freshness oder Promotion-Status nicht. |
| production ready | Eine getrennte Release-/Betriebsentscheidung mit eigener Evidence und Risk Acceptance; kein Selected-Core-PASS bedeutet dies automatisch. |
| generated evidence | Ausgabe eines deklarierten Generators aus identifizierten Inputs; gültig nur innerhalb ihres Freshness-/Provenance-Contracts und niemals hand editiert. |
| manually maintained documentation | Versionierte lesergerichtete Prosa oder Change Record, bei Bedarf bilingual gepflegt, und kein Ersatz für rohe oder generierte Runtime-Artefakte. |

Bekannte Grenzen sind auf Repository-Evidence beschränkt: Die ausgewählte
Evidence ist ein HTTP/1.1-Compact-Core; erweiterte Kataloge sind
`NOT EXECUTED`; Generated-Report-Freshness ist uneinheitlich; Strict-
Post-Commit-Enforcement, CRS, vollständiges HTTP/2/3, Compression/nicht
ausgewählte Buffer, vollständige Matrixabdeckung, Long-Running-Resilience und
Production Readiness sind `out_of_scope`, soweit keine getrennte Evidence etwas
anderes sagt. Capability-/Compatibility-Deklarationen dürfen diese Grenzen
nicht umgehen.

## Entscheidungsprozess und verwandte Referenzen

Für dauerhafte Entscheidungen die bilinguale [ADR-Anleitung](decisions/README.de.md)
verwenden; die empfohlenen ersten Entscheidungen betreffen Parent-/Framework-
Grenze, host-neutrales `common/`, geteilte P1--P4-Semantik,
Connector-Selbstständigkeit und Parent-gegenüber-Framework-Tests. Keinen großen
historischen ADR-Satz ohne fokussierte Entscheidungsaufgabe nachtragen.

Dieses Dokument vor einer wesentlichen Architektur-, Lifecycle-, Connector-,
Testgrenzen- oder Security-Änderung lesen. Danach die aktuelle
[Architektur](architecture.de.md), [Konfiguration](configuration.de.md),
[Tests und Evidence](testing-and-evidence.de.md),
[Betrieb und Sicherheit](operations-and-security.de.md), passenden
Connector-Guide, aktuellen Report und zugehörigen Change Record lesen. Der
lokale Codex-Kontext ist nur Arbeitsunterstützung; dieses versionierte Konzept
ist die Zielzustandsquelle des Produkts.
