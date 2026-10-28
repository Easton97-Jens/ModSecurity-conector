# Connector-Beispiele

**Sprache:** [English](README.md) | Deutsch

Diese Beispiele zeigen die Konfiguration der sechs Hostfamilien und zehn
logischen Connector-Lösungen des Repositorys. Zuerst Host und Topologie wählen,
danach die Konfiguration anpassen. Beispiele sind Lehr-/Referenzmaterial,
keine Produktions-Deployment-Manifeste und keine Laufzeitnachweise.

Eine ältere Konfiguration aktualisieren? [Migration](../docs/migration.de.md)
lesen. Connector-eigene kumulative Request-/Response-Limits wurden entfernt.
Ein Wert aus einem älteren Beispiel wird vom aktuellen Source nicht
automatisch akzeptiert.

## Host wählen

| Hostfamilie | Beispiel-Guide | Logische Profile |
| --- | --- | --- |
| Apache | [Apache](apache/README.de.md) | `apache` |
| NGINX | [NGINX](nginx/README.de.md) | `nginx` |
| HAProxy | [HAProxy](haproxy/README.de.md) | `haproxy-htx`, `haproxy-spoe-spop` |
| Envoy | [Envoy](envoy/README.de.md) | `envoy-ext-proc`, `envoy-ext-authz` |
| Traefik | [Traefik](traefik/README.de.md) | `traefik-native-uds`, `traefik-forwardauth` |
| lighttpd | [lighttpd](lighttpd/README.de.md) | `lighttpd-patched`, `lighttpd-stock` |

Natives Streaming, ein Autorisierungsweg mit Response-Companion und ein
Traffic-führender Sidecar sind unterschiedliche Topologien. Sie unterscheiden
sich bei Request-Body-Sichtbarkeit, Hostvoraussetzungen und späten Aktionen.
Die [Body-Inspection-Matrix der zehn Profile](../docs/body-inspection-review-matrix.de.md)
erklärt diese Grenzen. Ein Response-Observer macht die gepufferte
Request-Autorisierung seines Hosts nicht inkrementell.

## Konfigurationslayout wählen

| Layout | Verwendung | Grenze |
| --- | --- | --- |
| `off` | Native Interventions-/Fehlerbehandlung ohne zusätzliche Safe-/Strict-Late-Action-Policy | Deaktiviert nicht die konfigurierte Engine-Inspection |
| `safe` | Nützliche Einstiegsreferenz für die ausgewählte P1–P4-Konfiguration | Vorsichtige späte Behandlung ignoriert weder native Reject-Ergebnisse noch echte Fehler |
| `strict` | Unterstützte strikte späte Aktion des ausgewählten Profils | Kann beim Start abgewiesen werden, wenn die erforderliche Hostaktion fehlt |
| `all` | Vollständige quellenbasierte Konfigurationsreferenz | Kein vierter Phase-4-Modus und keine Garantie für Laufzeitzulassung |

Das `all`-Layout verwendet einen echten Phase-4-Wert wie `strict` und erzeugt keinen nicht unterstützten P4-Modus `all`.
Eine eingecheckte Strict-Datei beweist keinen client-sichtbaren
Post-Commit-Abbruch. Werte, die nicht gemeinsam aktiv sein dürfen oder
betreiberspezifische Credentials benötigen, bleiben mit ihrer Auswahlgrenze
inaktiv. Nicht jede kommentierte Option einschalten.

`SecRuleEngine DetectionOnly`, `SecRuleEngine Off`, ein deaktivierter
Connector und Phase-4-`off` wirken auf unterschiedlichen Ebenen. Vor der
Auswahl den Host-Guide und die [Regelbeispiele](common/rule-examples.de.md)
lesen.

## Zehn logische Lösungen

| Logische Connectorlösung | Off | Safe | Strict | All |
| --- | --- | --- | --- | --- |
| Apache | [off](apache/off/httpd.conf) | [safe](apache/safe/httpd.conf) | [strict](apache/strict/httpd.conf) | [all](apache/all/httpd.conf) |
| NGINX | [off](nginx/off/nginx.conf) | [safe](nginx/safe/nginx.conf) | [strict](nginx/strict/nginx.conf) | [all](nginx/all/nginx.conf) |
| HAProxy HTX | [off](haproxy/off/haproxy-htx.cfg) | [safe](haproxy/safe/haproxy-htx.cfg) | [strict](haproxy/strict/haproxy-htx.cfg) | [all](haproxy/all/haproxy-htx.cfg) |
| HAProxy SPOE/SPOP | [off](haproxy/spoe-spop/off/) | [safe](haproxy/spoe-spop/safe/) | [strict](haproxy/spoe-spop/strict/) | [all](haproxy/spoe-spop/all/) |
| Envoy ext_proc | [off](envoy/ext-proc/off/) | [safe](envoy/ext-proc/safe/) | [strict](envoy/ext-proc/strict/) | [all](envoy/ext-proc/all/) |
| Envoy ext_authz | [off](envoy/ext-authz/off/) | [safe](envoy/ext-authz/safe/) | [strict](envoy/ext-authz/strict/) | [all](envoy/ext-authz/all/) |
| Traefik Native UDS | [off](traefik/native-uds/off/) | [safe](traefik/native-uds/safe/) | [strict](traefik/native-uds/strict/) | [all](traefik/native-uds/all/) |
| Traefik forwardAuth | [off](traefik/forwardauth/off/) | [safe](traefik/forwardauth/safe/) | [strict](traefik/forwardauth/strict/) | [all](traefik/forwardauth/all/) |
| lighttpd Patched | [off](lighttpd/patched/off/) | [safe](lighttpd/patched/safe/) | [strict](lighttpd/patched/strict/) | [all](lighttpd/patched/all/) |
| lighttpd Stock | [off](lighttpd/stock/off/) | [safe](lighttpd/stock/safe/) | [strict](lighttpd/stock/strict/) | [all](lighttpd/stock/all/) |

Links sind relativ zu diesem `examples/`-Verzeichnis. Pfade innerhalb einer
Hostkonfiguration, etwa `/etc/modsecurity/no-crs-baseline.conf`, sind
Installationsbeispiele und müssen meist an den Zielrechner angepasst werden.

## Kompatibilitäts- und Companion-Grenzen

Die vollständigen Bundles oben und das aufbewahrte eigenständige
Kompatibilitätsmaterial sind nicht dasselbe. Den passenden Hostabschnitt lesen:

- [HAProxy-SPOE/SPOP-Kompatibilitätsmaterial](haproxy/README.de.md#spoespop-kompatibilitätsmaterial)
- [Envoy-ext_authz-Kompatibilität](envoy/README.de.md#ext_authz-kompatibilität)
- [Traefik-forwardAuth-Kompatibilität](traefik/README.de.md#forwardauth-kompatibilität)
- [lighttpd-Sidecar-Kompatibilität](lighttpd/README.de.md#sidecar-kompatibilität)

Ein Request-only-Service begründet ohne seinen erforderlichen Companion keine
P3/P4-Inspection. Die alte host-only Sidecar-Illustration ist nicht die
Traffic-führende Stock-lighttpd-Lösung. Nachweise einer Route qualifizieren
keine andere Route.

## Body-Inspection und Sicherheit

P1/P2 bedeuten Request-Header/-Body; P3/P4 bedeuten Response-Header/-Body.
libModSecurity besitzt Inspection-Limits und -Aktionen für Request- und
Response-Bodies. Die beabsichtigten nativen Engine-Direktiven in der Regeldatei
konfigurieren, einschließlich `SecRequestBodyLimit`,
`SecRequestBodyNoFilesLimit`, `SecRequestBodyLimitAction`,
`SecResponseBodyLimit` und `SecResponseBodyLimitAction`, soweit die eigene
Policy sie benötigt. Zugriff und MIME-Auswahl bleiben ebenfalls
Engine-Einstellungen.

Entfernte Common-/Native-Body-Größenoptionen nicht als zusätzliche
Sicherheitsschicht eintragen. Sie führen zu Konfigurationsfehlern; der
Connector darf weder Standards einfügen noch still einen eigenen
Inspection-Präfix auswählen. Die vollständige
[Liste entfernter Optionen](../docs/migration.de.md) und den
[Body-Limit-Vertrag](../docs/phase4-mode-budget.de.md) beachten.

Einzelne Frames/Nachrichten, Arbeitsbuffer, Header-/Event-Metadaten, Timeouts,
Dateivalidierung und dokumentierte Host-Autorisierungsgrenzen bleiben
unabhängige Controls. Deren Entfernung nicht mit dem Entfernen
Connector-eigener Inspection-Größenpolicy verwechseln. Safe-Absicht,
First-byte-before-EOS und No-full-buffer-Eigenschaften benötigen passende
Hostnachweise; statische Dateien allein belegen sie nicht.

## Anzupassende Werte

| Wert | Warum er variiert | Beispiel und Vorsicht |
| --- | --- | --- |
| Host-/Modulpfad | Installation und Modul-ABI unterscheiden sich | Zum ausgewählten Host passendes Modul verwenden; installierte Konfiguration nicht blind überschreiben |
| Regeldateipfad | Der Service muss geprüfte Engine-Regeln lesen können | `/etc/modsecurity/no-crs-baseline.conf` ist ein Installationsbeispiel und kein universeller Standard |
| Listener/Upstream | Lokale Anwendungen und Routen unterscheiden sich | `127.0.0.1:8080` / `127.0.0.1:8081`; öffentliche Exposition ist eine getrennte Entscheidung |
| Runtime-/Socketpfad | Services brauchen private beschreibbare Orte | Geschütztes Runtime-Verzeichnis außerhalb des Checkouts verwenden |
| Log-/Eventziel | Rechte und Aufbewahrung sind deployment-spezifisch | Metadatenlogs schützen und rotieren; niemals Secrets oder Traffic-Bodies für Reviews ergänzen |

Credentials, Private Keys, Cookies und Authorization-Werte über den sicheren
Konfigurationsmechanismus des Hosts bereitstellen. Sie weder committen noch
in Run-IDs oder Review-Nachweise aufnehmen.

## Typischer Ablauf

1. Hostfamilie und logisches Profil wählen und deren Voraussetzungen lesen.
2. Zum Lernen mit der passenden `safe`-Referenz beginnen oder bewusst eine
   andere Policy wählen. Vor `strict`- oder `all`-Dateien Strict-Zulassung prüfen.
3. Pfade, Adressen, Regeln, Rechte und private Endpunkte anpassen.
4. Den dokumentierten nativen Hostchecker oder das Root-Konfigurationstarget ausführen.
5. Root-Build-/Start-Targets nur mit ihren Voraussetzungen verwenden. Normale
   Tests über das aktive Inventar wählen; nicht jeden alten Test als Standard ansehen.
6. Für Laufzeitaussagen gesondert autorisierte Profil-/Run-Nachweise verwenden
   und deren Artefakte validieren. Große Kampagnen sind kein automatischer Beispielschritt.

Ein erfolgreicher Syntax-/Konfigurationscheck belegt nur Parsing/Laden. Er
beweist keine Produktionsreife, CRS-Vollständigkeit, vollständige
Protokollabdeckung, sämtliche P1–P4-Ergebnisse oder Strict-Late-Verhalten.

## Regeln und Phasen-IDs

Die No-CRS-Baseline verwendet folgende Repository-Testprofil-IDs. Sie sind
keine OWASP-Core-Rule-Set-IDs; lokale Host-Illustrationsregeln können andere
IDs besitzen.

| Regel-ID | Phase | Bedeutung |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung innerhalb der gewählten Host-/Policy-Grenze |

Jeder Host-Guide nennt die Regelquelle und den Umfang seines Beispiels. Keine
veränderliche Framework-Regeldatei in ein Beispiel kopieren und anschließend
als feste Baseline behandeln.

## Detaillierte Referenzen

| Referenz | Umfang |
| --- | --- |
| [Common Runtime](common/common-connector-configuration.de.md) | Aktuelle quellenbasierte `key=value`-Parseroberfläche |
| [ModSecurity-Direktiven](common/modsecurity-directives.de.md) | Engine-Direktiven der eingecheckten Beispiele |
| [Regelbeispiele](common/rule-examples.de.md) | Enforcement, DetectionOnly und Engine Off |
| [Apache](apache/configuration-reference.de.md) | Registrierte Hostdirektiven und Beispielfelder |
| [NGINX](nginx/configuration-reference.de.md) | Registrierte Hostdirektiven, Kontexte und Beispielfelder |
| [HAProxy](haproxy/configuration-reference.de.md) | Native HTX- und getrennt markierte SPOE/SPOP-Konfiguration |
| [Envoy](envoy/configuration-reference.de.md) | Prozessor-, Service- und Hostkonfiguration |
| [Traefik](traefik/configuration-reference.de.md) | Native UDS- und getrennt markierte forwardAuth-Konfiguration |
| [lighttpd](lighttpd/configuration-reference.de.md) | Patched-Native- und Stock-Sidecar-Konfiguration |

Diese Detailreferenzen sind generiert. Änderungen über ihren Generator
vornehmen, statt Ausgaben isoliert zu bearbeiten. Für Konzepte
[Konfiguration](../docs/configuration.de.md), für Befehle
[Einstieg](../docs/getting-started.de.md) und für Ergebnisse
[Tests und Nachweise](../docs/testing-and-evidence.de.md) lesen.
