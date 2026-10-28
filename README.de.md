# ModSecurity Connector

**Sprache:** [English](README.md) | Deutsch

libModSecurity mit Apache, NGINX, HAProxy, Envoy, Traefik oder lighttpd verbinden:
Dieses Repository stellt die Hostintegrationen, gemeinsame Runtime,
Konfigurationsbeispiele, Build-Steuerung und Werkzeuge zur Verhaltensprüfung
bereit. Die ModSecurity Engine wertet Regeln aus; der jeweilige Connector
liefert die Hostdaten und übersetzt eine Engine-Entscheidung in eine vom Host
unterstützte Aktion.

**Neu im Projekt?** Mit [Einstieg](docs/getting-started.de.md) beginnen und danach
unter [Beispiele](examples/README.de.md) einen Host wählen. **Bestehende Einrichtung
aktualisieren?** Vor der Wiederverwendung alter Konfigurationen
[Migration und aktuelles Verhalten](docs/migration.de.md) lesen: Connector-eigene
Request-/Response-Body-Größenoptionen wurden entfernt, und die
Standard-Testauswahl wurde geändert.

## Host und Profil wählen

Es gibt sechs Hostfamilien und zehn logische Connector-Profile. Ein Profil
bezeichnet eine bestimmte Integrationstopologie und garantiert nicht, dass
jedes Protokoll oder jeder späte Eingriff unterstützt wird.

| Hostfamilie | Logische Profile | Einstieg |
| --- | --- | --- |
| Apache | `apache` | [Guide](docs/connectors/apache.de.md) / [Beispiele](examples/apache/README.de.md) |
| NGINX | `nginx` | [Guide](docs/connectors/nginx.de.md) / [Beispiele](examples/nginx/README.de.md) |
| HAProxy | `haproxy-htx`, `haproxy-spoe-spop` | [Guide](docs/connectors/haproxy.de.md) / [Beispiele](examples/haproxy/README.de.md) |
| Envoy | `envoy-ext-proc`, `envoy-ext-authz` | [Guide](docs/connectors/envoy.de.md) / [Beispiele](examples/envoy/README.de.md) |
| Traefik | `traefik-native-uds`, `traefik-forwardauth` | [Guide](docs/connectors/traefik.de.md) / [Beispiele](examples/traefik/README.de.md) |
| lighttpd | `lighttpd-patched`, `lighttpd-stock` | [Guide](docs/connectors/lighttpd.de.md) / [Beispiele](examples/lighttpd/README.de.md) |

Direkte/native Integrationen und Autorisierungswege sind nicht austauschbar.
SPOE/SPOP, ext_authz und forwardAuth benötigen für Response-Phasen den
dokumentierten Response-Companion oder Observer. Dieser hebt die Grenzen für
Request-Stichproben oder gepufferte Requests des Autorisierungswegs nicht auf.
Patched-Native-lighttpd und sein Stock-Sidecar sind getrennte Lösungen und
keine Fallback-Modi.

Der [Connector-Index](docs/connectors/README.de.md) unterscheidet logische
Profil-IDs, Profilnamen der Root-Lifecycle-Targets und aufgezeichnete
Integrationsmodi. Die [Body-Inspection-Matrix](docs/body-inspection-review-matrix.de.md)
beschreibt die tatsächlichen Grenzen aller zehn Profile.

## Schnellstart

Git, Make und die im [Build-Guide](docs/build/README.de.md) beschriebenen
Voraussetzungen verwenden. Toolchain- und Framework-Revisionen folgen dem
eingecheckten [Vertrag für Versions-Pins](docs/reference/version-pins.de.md),
nicht der zufällig neuesten Version auf dem Rechner.

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
make check-active-inventory
make quick-check
```

Bei einem vorhandenen Clone ohne Submodule zuerst
`git submodule update --init --recursive` ausführen. `FRAMEWORK_ROOT` zeigt
normalerweise auf `modules/ModSecurity-test-Framework`; nur mit einem
vertrauenswürdigen passenden Checkout überschreiben.

`make check-active-inventory` prüft das gesamte ausgewählte Testinventar,
ohne Tests zu starten. `make quick-check` führt statische Prüfungen und
zugelassene funktionale Teilmengen aus. Keiner der Befehle qualifiziert jeden
Host und jedes Profil für den Betrieb. `make test` führt die aktive Auswahl
aus und benötigt deren tatsächliche Compiler-, SDK- und Hostvoraussetzungen.
Fehlende Voraussetzungen dürfen nicht als Erfolg dargestellt werden.

## Befehle nach Aufgabe

Befehle im Repository-Hauptverzeichnis ausführen. Das Root-`Makefile` ist die
Befehlsreferenz; die verlinkten Guides beschreiben Voraussetzungen und Ausgaben.

| Aufgabe | Befehl oder Guide | Aussage des Ergebnisses |
| --- | --- | --- |
| Checkout prüfen | `make quick-check` | Statische Verträge und ausgewählte funktionale Teilmengen |
| Testauswahl ohne Ausführung prüfen | `make check-active-inventory` | Zulässigkeit des vollständigen aktiven Inventars |
| Standard-Testauswahl ausführen | `make test` | Ergebnisse der tatsächlich ausgewählten und ausgeführten Fälle |
| Eine Integration bauen | `make build-nginx` | Build-Erfolg dieser Route, kein Traffic-Verhalten |
| Hostkonfiguration validieren | `make check-config-apache` | Laden der Konfiguration, kein P1–P4-Laufzeitnachweis |
| Dokumentationspaare und Links prüfen | `make check-bilingual-docs` / `make check-doc-links` | Konsistenz der Dokumentation |
| Einen aufgezeichneten Lauf einordnen | [Tests und Nachweise](docs/testing-and-evidence.de.md) | Exaktes Profil, Regeln, Run-ID, Artefakte und Einschränkungen |

Normale lokale und CI-Tests verwenden eine gemeinsame maßgebliche Auswahl:
[config/testing/active-cases.json](config/testing/active-cases.json). Die
Kerngrenze von 100 Fällen und die getrennt autorisierte geschützte
Offline-Python-Ausnahme werden getrennt gezählt; die Ausnahme ergänzt keine
Connector-E2E-Fälle. Für Fallzahlen das Inventar und dessen Prüfausgabe
verwenden, statt aus einem Befehlsnamen vollständige Abdeckung abzuleiten.

Full-Lifecycle-Kampagnen sind Spezialarbeit und nicht der automatische nächste
Schritt. Sie benötigen einen gesonderten aktuellen Auftrag und
`ON_DEMAND_TESTS=1`. Das Flag ist keine allgemeine Umgehung und eröffnet keine
abgeschlossene I12-Arbeit erneut. Geschützte NGINX-Hostprüfungen behalten ihren
separat kontrollierten Ausführungsweg für den exakten Commit.

## Body-Inspection und Phase 4

| Phase | An die Engine gelieferte Daten |
| --- | --- |
| P1 | Request-Header |
| P2 | Request-Body |
| P3 | Response-Header |
| P4 | Response-Body |

**Body-Inspection-Limits gehören zu libModSecurity.** Request-Policy mit
`SecRequestBodyLimit`, `SecRequestBodyNoFilesLimit` und
`SecRequestBodyLimitAction` konfigurieren; Response-Policy mit
`SecResponseBodyLimit` und `SecResponseBodyLimitAction`. Body-Zugriff und
Response-MIME-Auswahl bleiben ebenfalls Engine-Einstellungen. Ohne explizite
Engine-Direktiven gilt die native Engine-Semantik; der Connector darf keine
Ersatzstandards einfügen oder Eingaben auf einen selbst gewählten
Inspection-Präfix kürzen.

| Phase-4-Modus | Bedeutung | Bedeutet nicht |
| --- | --- | --- |
| `off` | Native Interventions-/Fehlerbehandlung ohne zusätzliche Safe-/Strict-Late-Action-Policy | Engine oder Response-Inspection sind deaktiviert |
| `safe` | Unterstützte vorsichtige Behandlung einer Entscheidung nach Beginn der Response-Ausgabe | Native Reject-Ergebnisse oder echte Verarbeitungsfehler dürfen ignoriert werden |
| `strict` | Unterstützte strikte späte Hostaktion des ausgewählten Profils | Jedes Profil kann eine bereits begonnene Response abbrechen |

`all` ist ein Beispiellayout und kein vierter Phase-4-Modus. Eine
Strict-Konfiguration kann bereits beim Start abgewiesen werden, wenn dem
Profil die benötigte Hostaktion fehlt. Modi wählen niemals ein
Body-Größenlimit oder eine Engine-Limitaktion.

Alte Einstellungen wie `request_body_limit`, `response_body_limit`,
`body_limit_action` und `modsecurity_phase4_body_limit` wurden entfernt und
werden nicht stillschweigend als Kompatibilitätsoptionen akzeptiert. Den
[Migrationsguide](docs/migration.de.md) und den maßgeblichen
[Body-Limit-Vertrag](docs/phase4-mode-budget.de.md) beachten.
Arbeitsbuffer, einzelne Frames/Nachrichten, Metadaten, Timeouts, Dateiprüfungen
und die dokumentierten Host-Autorisierungslimits bleiben getrennte
Sicherheitsgrenzen.

## Repository-Übersicht

| Pfad | Inhalt |
| --- | --- |
| `common/` | Connector-neutrale Runtime-Verträge und gemeinsame Unterstützung |
| `connectors/` | Hostspezifischer Source, Integration, Metadaten und Harnesses |
| `docs/` | Nutzeranleitungen, Architektur, Verträge, Betrieb und Referenzen |
| `examples/` | Anzupassende und zu validierende Host-/Profilkonfigurationen |
| `ci/` und `tests/` | Parent-Prüfungen, Steuerung und Regressionstests |
| `reports/` | Laufbezogene Berichte, aktuelle Zusammenfassungen und historische Aufzeichnungen |
| `licenses/` | Externe Herkunft, Source-Basen und aufbewahrte Upstream-Hinweise |
| `modules/ModSecurity-test-Framework/` | Unabhängiges Framework-Submodule mit wiederverwendbaren Fällen, Schemas, Runnern und Normalizern |

Generierte Builds, Cache, Runtime, Logs und Nachweise außerhalb des Checkouts
halten. Dokumentierte Pfade wie `BUILD_ROOT` und `EVIDENCE_ROOT` sowie nicht
geheime, dateisystemsichere Run-IDs verwenden. Credentials oder sensible
Traffic-Bodies gehören niemals in versionierte Beispiele oder Review-Artefakte.

## Ergebnisse, Sicherheit und Herkunft

Ein erfolgreicher Build, Konfigurationscheck, eine Capability-Deklaration, ein
Smoke-Test oder Scanner belegt nur seinen eigenen Umfang. Diese README
behauptet keine Produktionsreife, CRS-Vollständigkeit, vollständige HTTP/2-
oder HTTP/3-Abdeckung, vollständige Matrix oder Strict-Unterstützung aller
Profile. [Reports](reports/README.de.md) beschreiben aufgezeichnete Läufe;
[Betrieb und Sicherheit](docs/operations-and-security.de.md) behandelt
Deployment-Entscheidungen. Schwachstellen gemäß [SECURITY.de.md](SECURITY.de.md)
melden.

[licenses/](licenses/README.de.md) erklärt die Herkunft ausgewählten externen
Materials, seine aufgezeichnete Upstream-Basis und die Unterschiede lokaler
Anpassungen. Das Verzeichnis ist keine Lizenzdeklaration für das gesamte
Repository. Aufbewahrte Upstream-Hinweise begleiten weiterhin das betreffende
Material; eine lokale Änderung beseitigt dessen Upstream-Herkunft nicht.
Dateibezogene Herkunft steht in den passenden `ORIGIN.md`- und
`SOURCE_MAP.json`-Dateien. Auf diesem Stand gibt es keine Top-Level-`LICENSE`.

## Dokumentation

Der [Dokumentationsindex](docs/README.de.md) verlinkt aktuelle Konfigurations-
und Body-Inspection-Verträge, Compiler-Guides, aktive Tests, Versions-Pins,
CI-/Sonar-Analyse, Evidence-Abschlüsse und Betriebshinweise. Englisch und
Deutsch werden gemeinsam gepflegt. Generierte Referenzen müssen über ihre
Quelle bzw. ihren Generator geändert werden, nicht isoliert von Hand.
