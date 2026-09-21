# Dokumentation

**Sprache:** [English](README.md) | Deutsch

Dies ist die zentrale Navigation für die Dokumentation des ModSecurity
Connectors. Wenn Sie neu im Projekt sind, beginnen Sie mit **Einstieg** und
wählen danach den Connector und das Beispiel für Ihren Host. Detaillierte
Referenzen bleiben erhalten, wenn exakte Variablen, Build-Verträge,
Evidence-Semantik oder Security-Grenzen benötigt werden.

Das Repository deckt aktuell sechs Hostfamilien und zehn logische
Connector-Profile ab. Die ausgewählte Kerndokumentation ist auf HTTP/1.1
ausgerichtet. Source-Code, ein erfolgreicher Build, ein Konfigurationscheck
oder eine Beispieldatei sind für sich allein kein Nachweis für Production
Readiness oder ein verifiziertes Runtime-Ergebnis.

## Neu im Projekt?

| Schritt | Lesen | Ergebnis |
| --- | --- | --- |
| 1 | [Einstieg](getting-started.de.md) | Klonen, Framework initialisieren, erste Checks ausführen und Host/Profil wählen. |
| 2 | [Beispiele](../examples/README.de.md) | Eine `off`-, `safe`-, `strict`- oder `all`-Konfiguration für die ausgewählte logische Lösung wählen. |
| 3 | [Connector-Index](connectors/README.de.md) | Ausgewählte Route, alternative logische Profile und hostspezifische Grenzen verstehen. |
| 4 | [Konfiguration](configuration.de.md) | Verstehen, welche Einstellungen zum Host, Connector/Common Runtime oder zur ModSecurity Engine gehören. |
| 5 | [Build](build/README.de.md) | Die ausgewählte Hostintegration vorbereiten und bauen, ohne Build-Erfolg mit Runtime-Nachweis zu verwechseln. |

## Dokumentation nach Aufgabe finden

| Ich möchte… | Hier beginnen | Danach lesen |
| --- | --- | --- |
| das Repository verstehen | [Architektur](architecture.de.md) | [Repository-Konzept](repository-concept.de.md) |
| einen Connector konfigurieren | [Konfiguration](configuration.de.md) | [Beispiele](../examples/README.de.md) |
| Connector/Profil auswählen | [Connector-Index](connectors/README.de.md) | den passenden Connector-Guide |
| einen Connector bauen | [Build](build/README.de.md) | [Compiler-Guides](build/compilers/README.de.md) |
| Phase 1–4 verstehen | [Architektur](architecture.de.md) | [Phase-4-Modus und Budget](phase4-mode-budget.de.md) |
| Tests ausführen oder Ergebnisse deuten | [Tests und Nachweise](testing-and-evidence.de.md) | [Reports](../reports/README.de.md) |
| Variablen verstehen | [Variablen](reference/variables.de.md) | [Glossar](reference/glossary.de.md) |
| sicher betreiben oder deployen | [Betrieb und Sicherheit](operations-and-security.de.md) | [SECURITY.de.md](../SECURITY.de.md) |
| CI-Security verstehen | [CI-Sicherheitswerkzeuge](security/ci-security-tooling.de.md) | [Vertrauenswürdiger NGINX-Root-Broker](security/trusted-nginx-root-broker.de.md) |
| Projektdokumentation ändern | [Nachvollziehbarkeit](change-traceability.de.md) | [Change-Record-Archiv](../reports/audits/change-records/README.de.md) |

## Connector-Guides

| Hostfamilie | Ausgewählte Core-Route | Guide |
| --- | --- | --- |
| Apache | `native-httpd-module` | [Apache](connectors/apache.de.md) |
| NGINX | `native-nginx-http-module` | [NGINX](connectors/nginx.de.md) |
| HAProxy | `native-htx-filter` | [HAProxy](connectors/haproxy.de.md) |
| Envoy | `ext_proc` | [Envoy](connectors/envoy.de.md) |
| Traefik | `native-traefik-middleware` | [Traefik](connectors/traefik.de.md) |
| lighttpd | `patched-native-lighttpd` | [lighttpd](connectors/lighttpd.de.md) |

Einige Hostfamilien besitzen mehr als eine logische Lösung. Jedes logische
Profil ist ein eigener Evidence-Scope; ein Profil beweist kein anderes Profil
derselben Hostfamilie.

Die `capabilities.json` jedes Connectors beschreibt den deklarierten
Implementierungsstatus und ist kein PASS-Ergebnis. Ebenso bezeichnet
`minimal_runtime_smoke` bewusst nur eine enge Runtime-Ebene und darf nicht als
Full-Lifecycle- oder Production-Readiness-Evidence interpretiert werden.

## Beispiele gehören zum Lernpfad

Der [Beispielindex](../examples/README.de.md) ist der praktische Begleiter
dieser Dokumentation. Er ordnet alle zehn logischen Lösungen ihren
eingecheckten `off`-, `safe`-, `strict`- und `all`-Layouts zu und
erklärt, welche Pfade, Ports, Rules-Dateien, Sockets und Logziele vor der
Verwendung angepasst werden müssen.

Beispiele sind **Konfigurationsreferenzen**, keine Deployment-Manifeste.
Validieren Sie immer die materialisierte Hostkonfiguration und lesen Sie die
passenden Connector-Einschränkungen, bevor Traffic gesendet wird.

## Referenz und Pflege

- [Variablen](reference/variables.de.md) ist die vollständige Variablen-/Platzhalterreferenz.
- [Glossar](reference/glossary.de.md) definiert repository-spezifische Begriffe.
- [Phase-4-Modus und Budget](phase4-mode-budget.de.md) definiert den aktuellen `off`-/`safe`-/`strict`-Vertrag.
- [Reports](../reports/README.de.md) ist der Einstieg für aktuelles und historisches Evidence-/Report-Material.
- [Common-Source-Tree-Guide](../common/README.de.md) erklärt connector-neutrale Code-Ownership.
- [Framework-Modul](../modules/ModSecurity-test-Framework/README.de.md) besitzt wiederverwendbare Testfälle, Schemas, Runner und Normalizer.

Englische und deutsche Repository-Dokumentation müssen inhaltlich gleichwertig
bleiben. Generierte Dokumentation wird über ihren Generator-/Source-Vertrag
gepflegt und nicht isoliert manuell editiert.
