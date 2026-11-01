# Dokumentation

**Sprache:** [English](README.md) | Deutsch

Mit der Aufgabe beginnen, die erledigt werden soll. Die Einstiegsanleitungen
erklären das Projekt schrittweise; die verlinkten technischen Referenzen
enthalten weiterhin genaue Syntax, Voraussetzungen, Zuständigkeiten und Grenzen.

Das Repository besitzt sechs Hostfamilien und zehn logische Connector-Profile.
Seine ausgewählten Kernrouten sind auf HTTP/1.1 ausgerichtet. Ein Build oder
Konfigurationscheck belegt weder Produktionsreife noch vollständige
Protokollabdeckung.

## Erste Schritte

| Schritt | Lesen | Ergebnis |
| --- | --- | --- |
| 1 | [Einstieg](getting-started.de.md) | Checkout initialisieren, Voraussetzungen vorbereiten und erste Checks ausführen |
| 2 | [Beispiele](../examples/README.de.md) | Host, logisches Profil und Konfigurationslayout wählen |
| 3 | [Konfiguration](configuration.de.md) | Hostintegration, Common Runtime und Engine-Regeln auseinanderhalten |
| 4 | [Build](build/README.de.md) | Ausgewählte Integration bauen und validieren |
| 5 | [Tests und Nachweise](testing-and-evidence.de.md) | Aktive Testauswahl und Aussagekraft der Ergebnisse verstehen |

Eine bestehende Installation aktualisieren? Zuerst [Migration](migration.de.md)
lesen. Aus dem aktuellen Source entfernte Connector-Größenoptionen für Requests
und Responses sind keine Kompatibilitätsaliase. Sie dürfen nicht aus alten
READMEs oder Reports zurückkopiert werden.

## Dokumentation nach Aufgabe finden

| Ich möchte… | Einstieg | Details |
| --- | --- | --- |
| den Datenfluss verstehen | [Architektur](architecture.de.md) | [Repository-Konzept](repository-concept.de.md) |
| die Integrationstopologie wählen | [Connector-Index](connectors/README.de.md) | [Beispiele](../examples/README.de.md) |
| Regeln und Body-Inspection konfigurieren | [Konfiguration](configuration.de.md) | [Body-Limit-Zuständigkeit und Phase-4-Modus](phase4-mode-budget.de.md) |
| Grenzen der Body-Verarbeitung vergleichen | [Body-Inspection-Matrix der zehn Profile](body-inspection-review-matrix.de.md) | Passender Connector-Guide |
| eine ältere Konfiguration aktualisieren | [Migration](migration.de.md) | Aktuelle generierte Konfigurationsreferenzen in den Hostbeispielen |
| einen Host vorbereiten oder bauen | [Build](build/README.de.md) | [Compiler-Guides](build/compilers/README.de.md) |
| Variablen oder Toolchains wählen | [Variablen](reference/variables.de.md) | [Versions-Pins](reference/version-pins.de.md) |
| Standardtests ausführen | [Tests und Nachweise](testing-and-evidence.de.md) | [Test-Einstiegspunkte](../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_tests/README.de.md) |
| einen Laufzeitbericht einordnen | [Reports](../reports/README.de.md) | Profil, Regeln, Revision, Run-ID, Artefakte und verbleibende Grenzen |
| sicher betreiben | [Betrieb und Sicherheit](operations-and-security.de.md) | [Schwachstellen melden](../SECURITY.de.md) |
| CI und Scanner verstehen | [CI-Sicherheitswerkzeuge](security/ci-security-tooling.de.md) | [CI-Einstiegspunkte](../ci/README.de.md) |
| statische Analyse konfigurieren | [SonarQube-Cloud-Analyse](sonarqube-analysis.de.md) | Analyseumfang und Nachweise der exakten Revision |
| privilegierte NGINX-Prüfungen verstehen | [Vertrauenswürdiger NGINX-Root-Broker](security/trusted-nginx-root-broker.de.md) | Geschützte Ausführung bleibt von normalen PR-Checks getrennt |
| einen Begriff nachschlagen | [Glossar](reference/glossary.de.md) | Technische Bezeichner bleiben im Source suchbar |
| das Projekt ändern | [Nachvollziehbarkeit](change-traceability.de.md) | [Change Records](../reports/audits/change-records/README.de.md) |
| externe Herkunft prüfen | [Herkunfts- und Lizenzreferenzen](../licenses/README.de.md) | Connector-Dateien `ORIGIN.md` und `SOURCE_MAP.json` |

## Connector-Guides

| Hostfamilie | Ausgewählter Kernintegrationsmodus | Guide |
| --- | --- | --- |
| Apache | `native-httpd-module` | [Apache](connectors/apache.de.md) |
| NGINX | `native-nginx-http-module` | [NGINX](connectors/nginx.de.md) |
| HAProxy | `native-htx-filter` | [HAProxy](connectors/haproxy.de.md) |
| Envoy | `ext_proc` | [Envoy](connectors/envoy.de.md) |
| Traefik | `native-traefik-middleware` | [Traefik](connectors/traefik.de.md) |
| lighttpd | `patched-native-lighttpd` | [lighttpd](connectors/lighttpd.de.md) |

Diese Tabelle nennt Kernrouten der Hostfamilien, nicht das gesamte Inventar
logischer Profile. Der [Connector-Index](connectors/README.de.md) behandelt
zusätzlich SPOE/SPOP, ext_authz, forwardAuth und Stock lighttpd. Source und
`capabilities.json` eines Profils beschreiben Implementierungsstand und sind
kein `PASS`-Ergebnis. Ein Profil liefert niemals Laufzeitnachweise für ein
anderes Profil derselben Hostfamilie.

## Beispiele, Tests und Nachweise

Der [Beispielindex](../examples/README.de.md) verlinkt alle zehn logischen
Lösungen mit ihren `off`-, `safe`-, `strict`- und `all`-Layouts. Vor Änderungen
an Modulpfaden, Regeldateien, Listenern, Upstreams, Sockets oder Logzielen den
passenden Host-Guide lesen. Beispiele sind Konfigurationsreferenzen und keine
fertigen sicheren Deployments. Ein `all`-Layout kann einen Strict-Modus wählen,
den das betreffende Hostprofil nicht zulässt.

Die normale funktionale Auswahl gehört zu
[config/testing/active-cases.json](../modules/ModSecurity-test-Framework/connector_suite/config/testing/active-cases.json).
`make check-active-inventory` prüft die gesamte Auswahl ohne Ausführung;
`make test` führt die aktive Auswahl mit ihren tatsächlichen Voraussetzungen
aus. `make quick-check` enthält statische Checks und zugelassene funktionale
Teilmengen. Kerngrenze und separat autorisierte Offline-Python-Ausnahme dürfen
nicht mit vollständiger Connector-E2E-Abdeckung verwechselt werden.

Ein `minimal_runtime_smoke` ist bewusst eng begrenzt. Builds, Source-Prüfungen,
Konfigurationschecks, Inventare, Scanner und vollständige Hostläufe bleiben
unterschiedliche Nachweisarten. Vor der Interpretation eines Ergebnisses
[Tests und Nachweise](testing-and-evidence.de.md) lesen. Historische Nachweise
sowie der [Abschluss zu PR #382](pr-382-merge-readiness.de.md) oder der
[I12-Abschluss zu PR #410](pr-410-i12-closeout-20261024.de.md) beschreiben ihren
aufgezeichneten Umfang; sie autorisieren keine weitere Kampagne und
zertifizieren nicht jedes aktuelle Profil.

## Zuständigkeit für Dokumentation

Parent besitzt die Connector-Produktintegration und ihre Dokumentation. Das
[Framework-Submodule](../modules/ModSecurity-test-Framework/README.de.md) besitzt
wiederverwendbare Testfälle, Schemas, Runner und Normalizer. Der
[Common-Source-Guide](../common/README.de.md) erklärt die Zuständigkeit für
gemeinsame Implementierung.

Englische und deutsche Begleitdateien müssen technisch gleichwertig bleiben.
Mit `make check-bilingual-docs` prüfen und Links mit `make check-doc-links`
validieren. Compiler-Guides, `examples/common/`, Host-Konfigurationsreferenzen
und andere generierte Ausgaben folgen ihrem Generator-/Source-Vertrag. Neue
Erklärungen gehören in gepflegte Guides oder in den Generator, nicht in
isoliert geänderte Ausgabedateien.
