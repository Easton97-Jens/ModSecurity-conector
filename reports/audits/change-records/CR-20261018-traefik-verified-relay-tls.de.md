# Change Record: CR-20261018-traefik-verified-relay-tls

**Sprache:** [English](CR-20261018-traefik-verified-relay-tls.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-traefik-verified-relay-tls |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `a29019558678222b88913be0e202db3c9d14323a` |


## Motivation und Problemstellung

Die an a29019558678222b88913be0e202db3c9d14323a gebundene Sonar-Analyse meldet S5332 am synthetischen Authorization-Relay. Der Klartext-Listener wird durch verifiziertes TLS ersetzt; der Befund wird weder unterdrückt noch akzeptiert.

## Akzeptanzkriterien

TLS mit frischer privater Runtime-CA und IP-SAN-Zertifikat für 127.0.0.1 bereitstellen. CA-Vertrauen und Hostnamenprüfung verlangen; Klartext, falsche CA und falschen SAN vor Engine-Zugriff ablehnen. Authorization-Response-Kapazität 32768 sowie Request-/Sample-Verhalten erhalten. Private Schlüssel bleiben außerhalb von Git und veröffentlichten Artefakten.

## Implementierungsentscheidung und Begründung

Python 3.14 HTTPSServer verwendet mindestens TLS 1.2 und HTTP/1.1-ALPN. Vorhandenes OpenSSL erzeugt synthetische Zertifikate mit einem Tag Gültigkeit. Der private CA-Schlüssel wird nach Signierung gelöscht, der Leaf-Schlüssel verbleibt ausschließlich im privaten Taskverzeichnis. HTTPS, tls.ca und insecureSkipVerify: false werden vor YAML-Prüfung und Hoststart konfiguriert. Der gepinnte Traefik-Vertrag verwendet ClientTLS.ca. Quellen: [Python HTTPSServer](https://docs.python.org/3.14/library/http.server.html), [gepinntes Traefik ClientTLS](https://github.com/traefik/traefik/blob/fc92cc118a0557a029c7019d5ee06665127b0f13/pkg/types/tls.go), [gepinntes forwardAuth](https://github.com/traefik/traefik/blob/fc92cc118a0557a029c7019d5ee06665127b0f13/pkg/middlewares/auth/forward.go).

## Geänderte Dateien

Traefik-spezifisch: i12_auth/auth_proxy.py bindet HTTPS; i12_auth/tls_fixture.py erzeugt begrenztes privates Zertifikatsmaterial und konfiguriert Vertrauen; i12_auth/prepare.py staged den Helper und erfasst nur öffentliche Zertifikatshashes. tests/test_traefik_i12_tls.py und tests/test_traefik_i12_quality_controls.py prüfen echte TLS-Verbindungen und Ablehnungsgrenzen. Dieser zweisprachige Change Record dokumentiert das Ergebnis.

## Ausgeführte Befehle

Alle lokalen Befehle verwenden RTK und die Parent-Virtualenv. Die fokussierte TLS-/Quality-/Authorization-Suite bestand vor der letzten Ergänzung öffentlicher Zertifikatshashes 30 Tests. Die abschließende gemeinsame TLS-/Quality-/Auth-/Source-Export-/Native-Measurement-/Ledger-Suite bestand 58 Tests in 17,594 Sekunden; 42 zweisprachige Dokumentations- und Change-Record-Tests bestanden. AST-Syntax aller fünf Python-Dateien und git diff --check bestanden. Exakte Befehle, Exitcodes und Quellhashes liegen extern unter relay-tls/final.json.

## Security-Auswirkung

Zertifikatsketten- und IP-Hostnamenprüfung bleiben aktiv. Keine Verifikationsumgehung, Paketinstallation, Befundstatusänderung oder Abschwächung von Quality Gates. Der Generator lehnt wiederverwendete, verlinkte, schreibbare oder fremde Pfade ab. Das Relay verweigert freigegebene oder verlinkte Schlüssel. CA-Schlüssel werden nach Signierung gelöscht. Der verbleibende server.key darf weder veröffentlicht noch committed werden; öffentliche Receipts enthalten ausschließlich Zertifikatshashes.

## Runtime-Evidence

Echte lokale TLS-Sockets belegen verifizierte Sample-Weiterleitung, Ablehnung von Klartext/falscher oder fehlender CA/falschem SAN vor dem Engine-Stub und gesunden TLS-Nachbarverkehr danach. Testserver werden beendet und private temporäre Verzeichnisse entfernt. Dies belegt synthetische Relay-Kontrollen, keinen Traefik-Host-Lifecycle. Vorhandene a290- und Acceptance-Captures bleiben unverändert versiegelt.

## Bekannte Einschränkungen

Der native Authorization-Upstream behält seinen bisherigen privaten Loopback-HTTP-Transport. Diese Änderung betrifft den durch S5332 gemeldeten HTTPS-Listener. Tatsächliche Traefik-CA-Nutzung und Runtime-Cleanup benötigen einen frischen separat verantworteten Hostcapture; alte Captures dürfen nicht umetikettiert werden.

## Verbleibende Risiken

Synthetische Zertifikate mit einem Tag Gültigkeit müssen unmittelbar vor jedem neuen Capture entstehen. Private Runtime-Leaf-Schlüssel bleiben von Veröffentlichung ausgeschlossen. Erst eine frische exakt headgebundene Hosted-Analyse kann die Auflösung von S5332 belegen.

## Nicht ausgeführte Prüfungen mit Begründung

Diese begrenzte Fixture-Aufgabe startet keinen echten Traefik-Host, führt kein Go/Race/Vet aus und verändert weder Git- noch Sonar-Zustand. Parent verantwortet Integration, frische Hostausführung und Hosted-Checks. Echte TLS-Server und Zertifikatsablehnungen werden lokal ausgeführt.

## Finaler Diff- und Review-Status

Der begrenzte Diff erhält maxResponseBodySize=32768 und bestehende Sample-/Transportsemantik. Keine Produktänderung, keine Änderung an Acceptance-Producern oder versiegelten Captures. 58 Regressionstests, 42 Dokumentationstests, fünf Syntaxprüfungen und die Whitespace-Prüfung bestanden; Hosted- und Host-Abnahme stehen noch aus.
