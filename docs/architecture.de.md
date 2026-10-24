# Architektur

**Sprache:** [English](architecture.md) | Deutsch

## Geltungsbereich

Dies ist die aktuelle maßgebliche Architekturreferenz des Connector-Repositorys.
Sie beschreibt die ausgewählten Hostpfade und ihre gemeinsamen Grenzen. Der
[gemeinsame Transaktions- und Phasenvertrag](../common/docs/transaction-phase-contract.de.md)
ordnet alle zehn logischen Connectorlösungen zu, ohne einen Quellpfad zu einem
Laufzeitnachweis zu befördern. Sie behauptet keine Produktionsreife, keine Produktionshärtung, keine
CRS-Verifikation, keine vollständige HTTP/2- oder HTTP/3-Abdeckung, keine
vollständige Matrix und kein Strict-Verhalten für alle Connectoren.

## Repository-Verantwortung

| Ebene | Besitzt | Besitzt nicht |
| --- | --- | --- |
| <code>common/</code> | Connector-neutrale C-first-Typen, Parser, Limits, Eventformen und Hilfsimplementierungen | Host-SDK-Objekte, Hooks, Filter, Host-Konfigurationsregistrierung oder Transaktionslebensdauer |
| <code>connectors/&lt;name&gt;/</code> | Hostintegration, Quellattribution, Build-Kleber, Hostkonfiguration, Request-/Response-Mapping und hostspezifische Tests | Einen zweiten generischen Common-Runtime-Vertrag |
| Framework-Submodul | Wiederverwendbare Cases, Schemata, Katalogauswahl, Normalisierung und Framework-eigene Runner | Connector-Quellcode, Hostintegration oder einen Connector-PASS ohne Laufzeitnachweis |
| Laufzeitnachweis | Ergebnisse, Events, effektive Konfiguration und Provenienz eines ausgewählten Laufs | Eine allgemeine Zusicherung außerhalb dieses Profils, Regelwerks und der Run-ID |

Eingecheckte Quellen und Buildskripte definieren Implementierungsdetails. Dieses
Dokument hält die beabsichtigte Ownership- und Sicherheitsgrenze fest.

## Navigation nach Hostfamilie und logische Profile

Die folgenden sechs Zeilen navigieren Hostfamilien; sie behaupten nicht, dass
jede Familie nur ein logisches Profil besitzt. Der gemeinsame Transaktions- und
Phasenvertrag definiert die zehn logischen Profilidentitäten und hält
Companion-/Composite-Profile von direkten Hostrouten getrennt.

| Hostintegration | Aktueller Kernpfad der Hostfamilie | Grenze für Response-Body |
| --- | --- | --- |
| Apache | Natives HTTPD-Modul | EOS-only-All-Response-Output-Gate; normalisierte Brigades werden bis zum ersten EOS vor Release zurückgehalten |
| NGINX | Natives HTTP-Modul | Response-Filter und Request-/Subrequest-End-of-Stream |
| HAProxy | Nativer HTX-Filter | HTX-End-of-Stream |
| Envoy | Gestreamter <code>ext_proc</code>-Dienst | Stream-Abschluss im ausgewählten Service-Protokoll |
| Traefik | Native Middleware mit lokalem UDS-Engine-Service | ResponseWriter-Commit-Grenze |
| lighttpd | Kanonische logische Stock-Route <code>stock-lighttpd-sidecar</code>; separate gepatchte Native-Route <code>patched-native-lighttpd</code> | Das Stock-Sidecar besitzt begrenztes HTTP/1.1 P1--P4; die gepatchte Route besitzt Semantik für dekodiertes Entity-Body-EOS |

Jeder Connector-Guide dokumentiert seinen hostspezifischen Pfad, Lifecycle,
Buildpfad, Grenzen, Kompatibilitätspfade, Betrieb und Validierung:
[Apache](connectors/apache.de.md), [NGINX](connectors/nginx.de.md),
[HAProxy](connectors/haproxy.de.md), [Envoy](connectors/envoy.de.md),
[Traefik](connectors/traefik.de.md) und [lighttpd](connectors/lighttpd.de.md).

## Transaktionslebenszyklus

| Phase | Neutrale Operation | Verantwortung des Hosts | Nachweisgrenze |
| --- | --- | --- | --- |
| P1 | Request-Header-Verarbeitung nach Connection-/URI-Voraussetzungen | Request-Metadaten mappen und einen zulässigen Eingriff vor Commit anwenden | Connection und URI sind Voraussetzungen, nicht P1 selbst |
| P2 | Request-Body anhängen und abschließen | Nur wie vom ausgewählten Hostpfad erlaubt streamen oder puffern; einmal bei Request-EOS abschließen | Body-Unterstützung ist profilspezifisch |
| P3 | Response-Header-Verarbeitung | Ursprungsstatus erhalten und feststellen, ob Header noch veränderbar sind | Ein P3-Ergebnis belegt kein P4-Verhalten |
| P4 | Response-Body anhängen und abschließen | Begrenzte Chunks verarbeiten, die ausgewählte Host-Release-Grenze einhalten und späten Eingriff sicher auflösen; Apache hält alle normalisierten Outputs bis zum ersten EOS vor Release zurück | Aktion nach Commit bleibt host- und nachweisabhängig |
| Logging | Transaktionslogging und Cleanup | Payload-sichere Metadaten ausgeben und Host-/Engine-Zustand genau einmal freigeben | Logs sind laufbezogene Nachweise, keine Laufzeitgarantie |

Die Engine-seitige öffentliche Reihenfolge basiert auf libmodsecurity-v3-Aufrufen
für Verbindung, URI, Request-Header/-Body, Response-Header/-Body, Eingriff,
Logging und Cleanup. Ein Connector darf eine Phase nicht nur wegen eines
neutralen Typs oder Quellzweigs als unterstützt bewerben.

Der [gemeinsame Transaktions- und Phasenvertrag](../common/docs/transaction-phase-contract.de.md)
ist die maßgebliche Common-Zuordnung für P1--P4, begrenzten Zustand,
Entscheidungen, Response-Companions und die zehn Lösungsidentitäten. Dieser
Architekturleitfaden unterscheidet weiterhin Quellkonfiguration von beobachtetem
Hostverhalten.
Seine dauerhafte Entscheidungsbegründung ist
[ADR-003](decisions/ADR-003-shared-p1-p4-lifecycle-semantics.de.md).

## Common-Grenze und C-first-Vertrag

Die Common-Schicht ist absichtlich C-first. Ihre öffentlichen Header modellieren
Request, Response, Transaktion, Eingriff, Status, Fähigkeit, Origin, Logging,
Limits und Konfiguration ohne Apache-, NGINX-, HAProxy-, Envoy-, Traefik- oder
lighttpd-SDK-Header. Dünne C++-Wrapper begründen kein zweites Ownership-Modell
und dürfen keine Host-ABI-Grenze überschreiten.

Common darf neutrale Eingaben validieren, Konfiguration normalisieren,
Eventdaten redigieren und begrenzte Metadaten schreiben. Es darf keinen
Connector-eigenen vollständigen Response-Body nur zur Regelauswertung halten,
kein Hostobjekt besitzen, keine hostspezifische späte Response-Aktion
entscheiden und keine Server-/Proxy-Integration einbetten.

## Ownership, Limits und sicheres spätes Verhalten

Request- und Response-Puffer bleiben Eigentum des Hostadapters. Common erhält
nur validierte Ansichten oder begrenzte Kopien, wenn seine API sie ausdrücklich
benötigt. Header, Body-Bereiche, Transaktions-IDs, Eingriffsdaten und
Event-Metadaten benötigen an jeder Adaptergrenze eine dokumentierte Lebensdauer.

Das ausgewählte Safe-P4-Verhalten ist konservativ: Eine Bedingung nach Commit
wird als begrenzte, payload-sichere Beobachtung aufgezeichnet, sofern der
ausgewählte Hostpfad und Laufzeitnachweis keine client-sichtbare Aktion
belegen. Ein Dokumentationslabel wie <code>strict</code> ist kein Nachweis für
einen Abbruch oder HTTP-Fehler. Apache ist eine beabsichtigte Pre-Commit-
Ausnahme: Sein P4-All-Response-Gate hält ursprüngliche Ausgabe bis zum ersten
EOS zurück, sodass ein normaler Deny diese Ausgabe verwirft und seinen
terminalen Fehler vor Release sendet. Apache-Safe-/Strict-Late-Verhalten gilt
nur für einen unabhängig als bereits committed nachgewiesenen Pfad.

## Fähigkeits-, Status- und Nachweismodell

Fähigkeiten beschreiben eine Host-/Profileigenschaft; sie sind keine
Ergebnisdatensätze. Das Statusvokabular unterscheidet implementiert,
nicht unterstützt, blockiert, nicht ausgeführt und beobachtete Ergebniszustände.
Ein Source-Build, Konfigurationsladen oder eine generierte Matrix kann kein
nicht ausgeführtes Hostverhalten befördern.

Kanonische Nachweise binden ein Ergebnis an Connector, ausgewähltes Profil,
Regelinput, Run-ID, effektive Konfiguration und erforderliches Artefaktschema.
Ergebnis-/Eventdatensätze bleiben payload-sicher: Request-Bodies, Response-
Bodies, Zugangsdaten, Cookies oder Authorization-Werte werden nicht nur zur
Phasendokumentation gespeichert.

## Rule-Load-Metadaten

Die Common-Rule-Load-Struktur zeichnet nur erfolgreiche Inline- und lokale
Datei-Regelzugänge auf. Sie zählt Regeln statt Direktivenaufrufe oder
Dateianzahl. Remote-Regelinputs werden vor dem Loader, einem Netzwerkauruf oder
einem nativen Remote-Rule-API-Aufruf abgelehnt; sie besitzen keinen Zähler für
erfolgreiche Loads und keine exponierten Metadaten. Fehlgeschlagene Ladevorgänge
behalten ihren bestehenden Fehlerpfad und erhöhen keinen Zähler. Die Metadaten beeinflussen weder RulesSet-Ownership,
Merge-Verhalten, Request-/Response-Verarbeitung, Body-Handling, Interventionen
noch Phasenverhalten.

| Feld | Bedeutung | Aktuelle Sichtbarkeit |
| --- | --- | --- |
| <code>inline_rules</code> | Aus Inline-Regelcontent geladene Regeln | Connector-Konfigurationsmetadaten |
| <code>file_rules</code> | Aus Regelfiles geladene Regeln | NGINX-Startup-Logging; Apache-interne Metadaten |

Common hat keine Reporting-API für diese Werte. Ein geteilter Report oder eine
Apache-Post-Config-Anzeige bleibt getrennte Arbeit und kann nicht aus einem
Zähler abgeleitet werden.

## Sicherheitsdatenfluss-Vertrag

Common-Integrity-Helfer sind ausdrücklich <code>non_crypto</code>; sie sind
keine kryptographische oder manipulationssichere Garantie. CI- und fokussierte
Smoke-Prüfungen verifizieren nur die dokumentierte Source-/Contract-Grenze.
Event- und Decision-Serialisierung bleibt payload-frei, begrenzt und
connector-neutral; Hostintegrationen bleiben für ihr eigenes Request-/Response-
und Transportverhalten verantwortlich.

## Konfigurations- und Buildgrenzen

Host-/Connector-Konfiguration, Common-Runtime-Key/Value-Konfiguration und
ModSecurity-Engine-<code>Sec*</code>-Direktiven sind getrennte Ebenen. Den
repositoryweiten Überblick liefert [Konfiguration](configuration.de.md); die
vollständigen Connector-Direktivenreferenzen bleiben unter
<code>examples/&lt;connector&gt;/</code>.

Builds werden außerhalb des Checkouts materialisiert und bleiben von
Konfigurationsladen, Hoststart, Verkehrsausführung und Evidence-Promotion
getrennt. Die aktuellen Compiler-/Build-Einstiege stehen in der
[Build-Dokumentation](build/README.de.md).

## Historischer Kontext

Frühere Extraktionspläne, Refactor-Reviews, Migrationspläne und thematische
Common-Notizen wurden hier zusammengeführt. Die Git-Historie bewahrt ihre
detaillierte Chronologie. Die aktuelle Regel bleibt unverändert: Connector-
neutraler Code wird nur verschoben, wenn Ownership, Quellattribution,
Buildverhalten und Hostnachweis explizit und prüfbar bleiben.

## Verwandte Referenzen

- [Zielkonzept für das Produkt-Monorepo](repository-concept.de.md)
- [Konfigurations- und Laufzeit-Hinweise](configuration.de.md)
- [Tests und Nachweise](testing-and-evidence.de.md)
- [Betrieb und Sicherheit](operations-and-security.de.md)
- [Variablen](reference/variables.de.md) und [Glossar](reference/glossary.de.md)
- [Common-Quellbaum-Guide](../common/README.de.md)
