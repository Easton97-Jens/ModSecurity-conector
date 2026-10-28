# Konfiguration

**Sprache:** [English](configuration.md) | Deutsch

## Mit der zu ändernden Ebene beginnen

Eine Hostkonfiguration bindet den Connector an Traffic an. Einstellungen der
Common Runtime konfigurieren gemeinsame Verarbeitung, wenn die gewählte
Integration eine Runtime-Datei verwendet. ModSecurity-Regeln konfigurieren
Engine-Inspection und Regelauswertung. Eine Einstellung auf einer Ebene ändert
nicht automatisch eine andere Ebene.

| Ebene | Zweck | Maßgebliches Detail |
| --- | --- | --- |
| Host oder Connector | Registriert und konfiguriert eine ausgewählte Hostintegration | Passender Connector-Guide und vollständige Beispielreferenz |
| Common Runtime | Parst die gewählte lokale Key/Value-Servicekonfiguration, wenn die Route sie verwendet | [Common-Runtime-Referenz](../examples/common/common-connector-configuration.de.md) |
| ModSecurity Engine | Lädt und wertet <code>Sec*</code>-Regeln aus | [Engine-Direktivenreferenz](../examples/common/modsecurity-directives.de.md) |

Für eine erste Einrichtung ein passendes [Beispiel](../examples/README.de.md)
wählen und dessen hostspezifische Anpassungs- und Validierungshinweise lesen.
Bei bestehenden Einrichtungen vor dem Kopieren alter Optionen
[Migration](migration.de.md) lesen.

## Body-Inspection gehört zur Engine

Request-Limits und -Aktionen verwenden `SecRequestBodyLimit`,
`SecRequestBodyNoFilesLimit` und `SecRequestBodyLimitAction`. Response-Limits
und -Aktionen verwenden `SecResponseBodyLimit` und `SecResponseBodyLimitAction`.
Der Zugriff bleibt über `SecRequestBodyAccess` und `SecResponseBodyAccess`
gesteuert; die Response-MIME-Auswahl bleibt bei `SecResponseBodyMimeType` und
`SecResponseBodyMimeTypesClear`.

Kumulative Connector-Einstellungen einschließlich `request_body_limit`,
`response_body_limit`, `body_limit_action` und
`modsecurity_phase4_body_limit` wurden entfernt. Sie sind weder
Kompatibilitätsaliase noch Ersatzwerte für Hostkapazität. Der Connector darf
keine Engine-Limitstandards liefern, aus Regeltext ableiten,
Reject/ProcessPartial wählen oder einen Body auf einen eigenen
Inspection-Präfix kürzen. Ohne explizite Direktiven bleibt die native
Engine-Semantik erhalten.

Limits einzelner Frames/Nachrichten, begrenzter Arbeitsspeicher,
Metadatenlimits, Timeouts, Dateivalidierung und tatsächliche
Autorisierungs-Hostgrenzen bleiben unabhängig davon bestehen. Der
[Body-Limit-Vertrag](phase4-mode-budget.de.md) und die
[Matrix der zehn Profile](body-inspection-review-matrix.de.md) erklären diese
Grenzen.

## Konfigurationsprinzipien

Ein Profil nur mit dem Connector und der Hostsyntax verwenden, für die es
geschrieben wurde. Build-, Cache-, Runtime-, Log- und Evidence-Ausgaben bleiben
außerhalb des Checkouts. Secrets über einen externen Secret-Mechanismus
bereitstellen; sie gehören nicht in eingecheckte Beispiele, Regeln, für Reviews
vorgesehene Befehlszeilen oder generierte Nachweise.

`SecRuleEngine`, Enable/Disable-Schalter des Hostconnectors,
Body-Zugriffskontrollen und Phase-4-Modi sind getrennte Einstellungen. Ein
aktiver Connector kann ein Regelwerk mit `SecRuleEngine Off` laden.
`DetectionOnly` wertet aus und protokolliert ohne disruptive Regelaktionen;
die native Engine-Limitsemantik bleibt erhalten.

## Profile und spätes Verhalten

Die Phase-4-Policy steuert unterstützte Behandlung einer
Response-Phase-Entscheidung, nicht MIME-Auswahl, Body-Größe oder
Engine-Limitaktion. Sie kann bereits an den Client gesendete Bytes nicht
zurücknehmen.

| Profil | Zweck | Grenze |
| --- | --- | --- |
| Off | Keine zusätzliche Safe-/Strict-Late-Action-Policy; gewählte Host-/Service-Struktur bleibt aktiv | Native Inspection sowie Interventions-/Fehlerbehandlung bleiben wie konfiguriert aktiv |
| Safe | Ausgewählte P1–P4-Referenz mit vorsichtiger später Behandlung | Erlaubt nicht, native Reject-Ergebnisse oder echte Fehler zu ignorieren |
| Strict | Fordert die unterstützte strikte Hostaktion des gewählten Profils an | Nicht unterstützte Aktionen können beim Start abgewiesen werden; kein universeller Late-Abort-Nachweis |
| DetectionOnly | Engine-Regeln werden ausgewertet und protokolliert | Disruptive Regelaktionen werden nicht angewendet |
| Disabled | Engine oder Hostintegration sind wie dokumentiert deaktiviert | Testet nicht den aktivierten Connectorpfad |

`all` ist das vollständige Beispiellayout und kein vierter Phase-4-Modus. Ein
Layout mit `strict` ist nicht automatisch auf jedem Host zulässig. Gemeinsame
Phase-4-Source-Standards verwenden `off`; ein expliziter Beispielwert ist kein
Source-Standard.

Eingecheckte Profildateien und generierte Referenzen sind die maßgeblichen
Quellen für Syntax, Standards, Kontexte, Vererbung, Platzhalter und Validierung.

## Vollständige Connector-Referenzen

| Connector | Vollständige Direktiven-/Konfigurationsreferenz |
| --- | --- |
| Apache | [Apache](../examples/apache/configuration-reference.de.md) |
| NGINX | [NGINX](../examples/nginx/configuration-reference.de.md) |
| HAProxy | [HAProxy](../examples/haproxy/configuration-reference.de.md) |
| Envoy | [Envoy](../examples/envoy/configuration-reference.de.md) |
| Traefik | [Traefik](../examples/traefik/configuration-reference.de.md) |
| lighttpd | [lighttpd](../examples/lighttpd/configuration-reference.de.md) |

Kompatibilitätseinträge sind in diesen Referenzen bewusst gekennzeichnet. Sie
ändern weder den gewählten Integrationsmodus noch begründen sie Unterstützung
eines anderen Pfads. Ein Response-Companion entfernt keine Request-Buffer-
oder Protokoll-Stichprobengrenzen seines Autorisierungs-Hosts.

## Variablen, Platzhalter und Validierung

[Variablen](reference/variables.de.md) definiert Format, Standards, Setzer,
Geltungsbereich, Auswirkungen, Beispiele und Sicherheitshinweise für
Repository-/Harness-Variablen. [Versions-Pins](reference/version-pins.de.md)
erklärt die Zuständigkeit für Toolchains und Revisionen. Diese Inputs sind
keine beliebigen Hostdirektiven.

Ausgewählte Hostkonfiguration mit dem dokumentierten nativen Checker oder mit
`make check-config-<connector>` validieren, soweit das Root-Target existiert.
Den Platzhalter durch das tatsächliche Hostfamilien-Target ersetzen, etwa
`make check-config-nginx`. Erfolgreiches Laden führt weder Traffic aus noch
wertet es ein Laufzeitergebnis auf. Siehe [Tests und Nachweise](testing-and-evidence.de.md).

## Direktivenparität und Kompatibilität

Gleiche Namen bedeuten nicht identische Hostsyntax, Kontexte, Vererbung oder
Auswertung. Apache-Ausdrücke sind keine NGINX-Direktiven.
Common-Runtime-Schlüssel dürfen nicht als unregistrierte Hostdirektiven
dargestellt werden.

| Oberfläche | Apache | NGINX | Grenze |
| --- | --- | --- | --- |
| <code>modsecurity</code>, Rules, Rules-Datei | Registrierte Hostdirektiven | Registrierte Hostdirektiven | Lokales Laden von Regeln bleibt Connector-Aufgabe |
| <code>modsecurity_rules_remote</code> | Registriert, aber von gemeinsamer Security-Policy abgewiesen | Registriert, aber von gemeinsamer Security-Policy abgewiesen | Ablehnung vor Fetch oder nativem Remote-API-Aufruf |
| <code>modsecurity_transaction_id</code> | Statische String-Semantik | Request-bezogene Complex-Value-Semantik | Gleicher Name bedeutet nicht gleiche Auswertung |
| <code>modsecurity_transaction_id_expr</code> | Registrierte Apache-Ausdrucksdirektive | Nicht registriert | Apache-Ausdruckssyntax nicht nach NGINX kopieren |
| Phase-4-Modus und Event-Logging | Hostspezifische registrierte Controls | Hostspezifische registrierte Controls | Entfernte Connector-Body-Größendirektiven werden durch gemeinsame Metadaten nicht wiedereingeführt |
| HAProxy-Konfiguration | Getrennte native HTX-Hostkonfiguration | Nicht anwendbar | SPOE/SPOP bleibt eine getrennte Stichproben-/Companion-Oberfläche |

Gemeinsame Metadaten bleiben connector-neutral. Hostregistrierung,
Vererbungsverhalten, Lebensdauer, Hooks, Filter und tatsächliche
Laufzeitaktionen bleiben Connector-Aufgaben.

## Weitere Referenzen

- [Architektur](architecture.de.md)
- [Connector-Guides](connectors/README.de.md)
- [Gemeinsame Regelbeispiele](../examples/common/rule-examples.de.md)
- [Glossar](reference/glossary.de.md)
- [Migration](migration.de.md)
