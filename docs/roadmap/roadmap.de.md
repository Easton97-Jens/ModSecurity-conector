# Roadmap

**Sprache:** [English](roadmap.md) | Deutsch

Status: aktueller evidenzbasierter Roadmap-Snapshot

In dieser Roadmap wird aufgezeichnet, was das Repository aktuell aus eingecheckten Daten nachweisen kann
Code, generierte Berichte, lokale Ergebniszusammenfassungen und Dokumentation. Generiert
Abdeckung, nur kartiertes Inventar, reine API-Smoke-Ergebnisse und Quellenherkunft
sind nützliche Evidence, aber sie allein fördern das Verhalten von Connectoren nicht.

## Aktueller Fokus

- Sorgen Sie dafür, dass Apache-, NGINX- und HAProxy-Evidence auf den realen Connector beschränkt bleiben
Weg:
HTTP-Client zum Serverprozess zum Connector-Modul zu libmodsecurity zu HTTP
Antwort.
- Den generierten Berichtsstatus an `TEST-COVERAGE-SUMMARY.md` anpassen,
`reports/testing/generated/canonical/full-runtime-matrix.generated.md`,
`reports/testing/generated/canonical/final-consistency-audit.generated.md` und
`reports/testing/README.md`.
- Behalten Sie die Unterscheidung zwischen standardmäßigen lokalen Connector-Zusammenfassungen und bei
force-all/full-matrix Evidence. Full-Matrix-Fehler bleiben sichtbar und
klassifiziert; Sie sind nicht PASS-sicher für Deckenanschlüsse.
- Lassen Sie `RESPONSE_BODY` nicht überprüft und nicht hochgestuft, bis sowohl Apache als auch
NGINX gibt stabiles HTTP 403 für denselben YAML-Fall zurück, der den Response Body blockiert.
– Behalten Sie die Zuordnung der RAW-Argumentsammlung bei, bis eine lokale Konfiguration erfolgt
Die ModSecurity v3-Quelle enthält PR #3564-Verhalten und beide Connectoren sind erfolgreich
echtes HTTP smoked für die gleichen YAML-Fälle.
- Behalten Sie Quellenangabe, Lizenz, origin/provenance-Metadaten und Adapter bei
Metadaten-Drift-Prüfungen, während die Apache-, NGINX- und HAProxy-Quelle erhalten bleibt
Adapterbesitz.

## Implementiert

- Monorepo-Layout mit repo-lokaler Apache-, NGINX- und HAProxy-Connector-Quelle
Bäume unter `connectors/apache/`, `connectors/nginx/` und
`connectors/haproxy/`.
- Platzhaltergerüste für `connectors/{envoy,lighttpd,traefik}/`.
- Connectorenneutrale C-First-Stiftleisten in `common/include/msconnector/` für
Direktiven, options/defaults, Regelladestatistiken, Anfrage, Antwort,
Transaktion, Intervention, Fähigkeit, origin/provenance, Protokollierung und
Statusdatenformen.
- Kleine connectorneutrale Hilfsimplementierungen in `common/src/` für Status,
Interventions-, Ursprungs- und Fähigkeitsmetadaten.
- Apache- und NGINX-Metadatendateien, `ORIGIN.md`-Dateien, `SOURCE_MAP.json`-Dateien,
zentrale Attributionskopien unter `licenses/` und Driftprüfungen
`ci/check-adapter-metadata-drift.sh`.
– Adaptereigene Apache-Build-Eingaben, APXS/Autotools-Dateien, Harness-Dateien usw
Produktivquelle unter `connectors/apache/src/`.
- Adaptereigenes NGINX-Modul `config`, Harness-Dateien und produktive Quelle
unter `connectors/nginx/src/`, einschließlich aufgezeichneter PR #377 Phase-4-Quelle
Herkunft für NGINX-Dateien.
– Gemeinsame Direktiven- und Optionsmetadaten, die von Apache und NGINX ohne Verschiebung verwendet werden
Server-hook/filter/runtime-Besitz in `common/`.
– Apache- und NGINX-Unterstützung für den in dokumentierten Direktivensatz
`docs/connectors/directive-parity.md`; Es bleiben nur NGINX-Phase-4-Steuerungen bestehen
connectorspezifisch.
– Regel-Ladestatistik-Metadaten in
`common/include/msconnector/rule_load_stats.h`; NGINX berichtet über seine
vorhandener Startup-Logpfad, während Apache die Zähler als intern speichert
Nur Konfigurationsmetadaten.
– Framework-gestützte öffentliche Ziele im Connector `Makefile`, einschließlich
`make lint`, `make summary`, `make case-matrix`, `make smoke-common`,
`make smoke-apache`, `make smoke-nginx` und `make smoke-all`.
- YAML-Fallkorpus und generierter Berichtsfluss im Besitz von
`modules/ModSecurity-test-Framework`, mit Connector-Evidence, der unten ausgegeben wird
`reports/testing/` und Root-Zusammenfassungskopie `TEST-COVERAGE-SUMMARY.md`.
– Aktuell generierte Abdeckungszusammenfassung für 140 YAML-Fälle, einschließlich 80 früherer erwarteter Fehler
Fälle, 10 nur zugeordnete Importinventareinträge, 11 Connector-Gap-Fälle,
13 Fälle von Runtimeunterschieden und 24 verbleibende `RESPONSE_BODY`-Fälle
nicht verifiziert.
- Runtimeergebnis-Metadaten abgestimmt auf `msconnector_status`,
`msconnector_origin` und `msconnector_intervention` unter Beibehaltung der
shell/Python-Harness unabhängig von C FFI.
- Reale Connector-Ergebnismetadaten für Apache, NGINX und HAProxy
Zusammenfassungen, einschließlich server/proxy-Binärdatei, Connector-Modul oder SPOA/SPOP
Integrationspfad, libmodsecurity-Pfad, Ursprung und verifizierte Variablenfamilien
wird nur aus der Übergabe von active/imported-Fällen abgeleitet.
- Aktuell generierte Standard-RuntimeEvidenceberichte Apache 54 PASS /
0 FEHLER / 0 BLOCKIERT, NGINX 60 PASS / 0 FEHLER / 0 BLOCKIERT und HAProxy
55 PASS / 0 FAIL / 0 BLOCKIERT. Hierbei handelt es sich lediglich um Evidence für Standardrauch; es ist
kein pauschaler Stabilitätsanspruch für alles erzwingende, ehemals erwartete Scheitern,
Nur zugeordnete, zukünftige oder blockierte Fälle.
- Aktuelle Force-All-RuntimeEvidenceberichte Apache 100 PASS / 27 FAIL /
0 BLOCKIERT, NGINX 95 PASS / 39 FAIL / 0 BLOCKIERT und HAProxy 104 PASS /
23 FAIL / 0 BLOCKED, mit ehemaligem erwarteten Fehler, Zukunft, Verbindungslücke,
runtime-difference und Response-Body-Pass-Through-Ergebnisse werden nicht hochgestuft.
- Aktuelle Full-Matrix-Evidenceberichte 3074 PASS / 782 FAIL / 0 BLOCKIERT. Der
Die abschließende Konsistenzprüfung empfiehlt keinen nächsten zur Runtime reparierbaren Connector-Cluster.
- Dokumentation zum Fähigkeitsmodell, Statusmodell, Adapterschnittstelle,
allgemeine Runtimegrenzen, Direktivenparität, Regelladestatistiken, Quelle
Namensnennung und license/origin-Richtlinie.

## Nächste Meilensteine

- Anschließend wird die dokumentierte YAML-Fallform in ein maschinenlesbares Schema umgewandelt
die gemeinsame YAML-Form und das Connector-spezifische Erweiterungsverhalten vereinbaren.
- Erweitern Sie die Unterstützung gemeinsam genutzter Geräte für externe Dateien, schema/DTD/XML-Geräte,
Dateigestützte Operatoren, binary/NUL-Nutzlastdarstellung und größere Antwort
Vorrichtungen.
- Halten Sie `reports/testing/case-matrix.md` und generierte Matrixberichte auf dem neuesten Stand
aus aktuellen Connector-Zusammenfassungen, ohne sie als eigenständige Runtime zu verwenden
nachweisen.
- Abgleichen der nachverfolgten generierten Runtimeberichte mit allen neu ausgeführten lokalen Berichten
Smoke-Ergebnisse vor der Aktualisierung des PASS/FAIL-Wortlauts in den Statusdokumenten.
– Fügen Sie eine klarere Connector-spezifische Konfigurationstestunterstützung für Fälle hinzu, in denen dies nicht möglich ist
ausgedrückt als einfache HTTP-Smokes, wie z. B. eine ungültige NGINX-Phase-4-Konfiguration.
- Stabile Audit-Log-Parser für abschnittsbezogene Prüfungen hinzufügen oder verfeinern; halten
flüchtige Felder aus erforderlichen Behauptungen.
– Fördern Sie die Nur-NGINX-TX-Bewertung und leiten Sie Fälle erst nach Apache auf „Common“ um
Gleichwertigkeit wird umgesetzt, getestet und dokumentiert.
- Fördern Sie mehrteilige filename/file-collection-Randgehäuse erst nach dem Anschluss
Runtimenachweise und native/semantic-Vergleich rechtfertigen eine Förderung.

## Später / Aufgeschoben

– Envoy, Lighttpd und Traefik bleiben zurückgestellt. Sie brauchen stabiles Common
Metadaten, stabiles Harness-Verhalten, ein ausgewählter Integrationsansatz und
Bevor Sie einen Kompatibilitätsanspruch geltend machen, sollten Sie sich eine Zusammenfassung der Connectoren aus der realen Welt anschauen.
- HAProxy verfügt über einen evidenzbasierten SPOA/SPOP-Runtimepfad mit Standard- und
Force-All-Smoke-Evidence, während größere Fähigkeitslücken weiterhin gemeldet werden und
nicht gefördert.
– Die Apache-Parität für NGINX-spezifische Phase-4-Anweisungen bleibt zurückgestellt.
- Gemeinsame Berichterstellung für Regelladestatistiken und deren Anzeige nach der Konfiguration durch Apache
Zähler bleiben zurückgestellt, bis die Aggregations- und Zusammenführungssemantik entworfen ist.
– Eine weitere Reduzierung der Quelle im Besitz des Apache/NGINX-Adapters bleibt aufgeschoben bis
Äquivalentes Verhalten existiert im gepflegten lokalen Code, die Namensnennung bleibt darunter
`licenses/`, `ORIGIN.md` und `SOURCE_MAP.json` sowie relevante reale Anwendungen
Smoke geht immer noch vorbei.
- Vollständiger CRS v2/v3-Kompatibilitätsvergleich, Leistungsbasislinien, elegant
Neustart-Lebensdauerprüfungen, vhost/UID Audit-Log-Szenarien, HTTP/2, Streaming,
und körperpuffernde Abdeckung bleiben spätere Arbeiten.
– Ein dediziertes `smoke-api`-Ziel für die konnektorfreie öffentliche C-API-Regression der Version 3
Kandidaten bleibt eine mögliche Ergänzung; Nur-API-Ergebnisse müssen getrennt bleiben
aus connectorfestem Material.

## Blockiert / Wartend

- Die `RESPONSE_BODY`-Blockierung wartet auf stabilem Apache und NGINX echtem HTTP 403
Verhalten für dasselbe YAML-Probe. PR #377-Quelle ist für NGINX aufgezeichnet, aber
Die Quellenaufnahme ist keine Response Bodyvalidierung.
– RAW-Argumentsammlungen warten auf lokale ModSecurity v3-Unterstützung
PR #3564 plus Weitergabe von Apache- und NGINX-Smokes aus der realen Welt.
- XML ​​schema/DTD-Validierung, Parser-Fehlerfälle, dateigestützte Operatoren,
fehlerhafte mehrteilige Körper, HTTP/2, Streaming und große body/response
Szenarien warten auf explizite Vorrichtungs- und Transportunterstützung.
– `v3_action_nolog_pass_no_audit` bleibt früherer erwarteter Fehler, da lokaler Apache/NGINX
Die Beobachtungen und das Prüfverhalten von GitHub Actions waren unterschiedlich.
- Zukünftige Connectoren warten auf einem ausgewählten Integrationspfad und einem echten Server
Harness, der die gleichen status/origin/intervention-Metadaten ausgeben kann.
- Neue Umgebungen können weiterhin blockiert werden, bis Quelldownloads, Toolchains usw.
Die libmodsecurity-Builds, Server-Builds und Connector-Modul-Builds sind abgeschlossen.

## Unbekannte / Designentscheidungen

– Ob das YAML-Schema ein JSON-Schema, ein benutzerdefinierter Validator oder beides sein soll.
– Wie viel Connector-spezifische YAML-Erweiterung sollte ansonsten zulässig sein
häufige Fälle.
– Wo soll die erste dauerhafte Common Runtime API-Grenze über Metadaten hinaus gezogen werden?
Helfer, ohne Apache-Hooks, NGINX-Filter, Body-Handling oder zu absorbieren
Transaktionsdauer zu früh.
- Wie man leere Antworten im Response Body, verspätete Interventionen usw. darstellt
Verhalten bereits gesendeter Header in einem stabilen Statusmodell.
– Ob die Apache-Response Bodyparität gemeinsames Verhalten verwenden soll, nur Apache
Richtlinien oder einem engeren dokumentierten Support-Level.
- HAProxy-Integrationspfad: SPOE-Dienst, Lua oder nativer Filter.
– Envoy-Integrationspfad: nativer C++-Filter, externe Verarbeitung, Lua oder Wasm.
- Lighttpd-Integrationspfad: natives Plugin oder `mod_magnet`.
- Traefik-Integrationspfad: plugin/middleware, Yaegi, Wasm oder ein anderer
dokumentierter Integrationsweg.

## Empfohlene nächste Aktionen

- Führen Sie `make lint`, `make summary` und `make case-matrix` aus, bevor Sie Änderungen vornehmen
Statusdokumente und notieren Sie dann die genauen Ergebnisse.
- Führen Sie `make smoke-common`, `make smoke-apache`, `make smoke-nginx` oder aus
`make smoke-all` nur, wenn erwartet wird, dass die Umgebung über die erforderlichen Abhängigkeiten verfügt
lokale Source-Build-Voraussetzungen; Zeichnen Sie PASS/FAIL/BLOCKED genau auf.
- Erstellte Berichte mit `make generate-test-matrix` aktualisieren und mit überprüfen
`make check-test-matrix` bei YAML-Fällen, Importstatus oder Connector
Zusammenfassungseingaben ändern sich.
- Behalten Sie die Blockierung des Response Bodys und RAW-ARGS in den blocked/waiting-on-Abschnitten bei, bis
Die lokale Quellenunterstützung und die beiden realen Connector-Smokes Evidencen dies.
- Behalten Sie die zukünftige Connector-Funktion als design-only/deferred bei, bis gemeinsame Metadaten und
Das Verhalten des Harnesss ist stabil genug, um das Kopieren von Apache/NGINX-Annahmen zu vermeiden.
- Halten Sie die Quellenangabe und Lizenzdateien bei jedem Connector synchronisiert
Die Quelle wird verschoben, reduziert oder aktualisiert.
