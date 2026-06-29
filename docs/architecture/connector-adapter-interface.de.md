# Connector-Adapter-Schnittstelle

**Sprache:** [English](connector-adapter-interface.md) | Deutsch

Dieses Dokument ist der stabile Vertrag für zukünftige Connectorbäume. Das ist es nicht
ein Webserver-Implementierungsplan.

## Connector-neutrale Verantwortlichkeiten

Der Shared Runner besitzt die YAML-Lade- und capability/status-Validierungsregel
Materialisierung, Request der body/header-Generierung, erwartete HTTP-Statusprüfungen,
Stabile Audit-Log-Prüfungen und zusammenfassende JSON-Generierung.

Connector-Code besitzt nur serverspezifische build/runtime-Mechaniken: Modul
Laden, Serverkonfiguration, Requestsversand, Protokollerfassung und Bereinigung.

## Erforderliche Haken

| Haken | Verantwortung |
| --- | --- |
| `prepare()` | Überprüfen Sie die Voraussetzungen und erstellen Sie generierte Verzeichnisse unter `BUILD_ROOT` |
| `start()` | Starten Sie den echten Serverprozess mit geladenem Connector-Modul |
| `stop()` | Stoppen Sie den Serverprozess, ohne veraltete Listener zu hinterlassen |
| `reload()` | Laden Sie die Konfiguration dort neu, wo der Connector sie unterstützt. Andernfalls wird das Dokument nicht unterstützt |
| `apply_rules()` | Installieren Sie generierte ModSecurity-Regeln für einen Fall |
| `materialize_case()` | Wandeln Sie gemeinsam genutzte YAML-Artefakte in konnektorspezifische Konfigurationsdateien um |
| `send_request()` | Senden Sie die echte HTTP-Anfrage aus dem YAML-Fall |
| `collect_logs()` | Kopieren oder referenzieren Sie Server-, Connector-, Audit- und Zugriffsprotokolle |
| `summarize_results()` | Schreiben Sie die Ergebnisse des Connectors JSON/text mithilfe eines gemeinsamen Schemas |
| `cleanup()` | Entfernen oder isolieren Sie den Runtimestatus unter `BUILD_ROOT` |

## Freigegebene Metadatenmodelle

Zukünftige Adapter sollten dieselben Nur-Anhänge-Metadaten melden, die vom aktuellen verwendet werden
Apache- und NGINX-Kabelbäume:

- `msconnector_status`: neutrales Betriebsergebnis (`ok`, `error`, `blocked`,
`unsupported`), zugeordnet vom Runtimerauchstatus.
- `msconnector_origin`: Quell-Repository, revision/version, Lizenz und
importierte Pfadmetadaten für das zu testende Connector-Modul.
- `msconnector_intervention`: Störflag, HTTP-Interventionsstatus, wenn
störende und optionale Protokollmeldung.

Die aktuellen shell/Python-Kabelbäume serialisieren diese Formen als JSON. Das tun sie nicht
Instanziieren Sie die C-Strukturen über FFI.

Phase 3 fügt kleine Common-C-Hilfsimplementierungen für diese Formen hinzu. Vorhanden
Apache- und NGINX-Kabelbäume verwenden weiterhin Python/Shell und spiegeln das Schema durch
`modules/ModSecurity-test-Framework/tests/runners/msconnector_models.py`.

## Grenzregeln

- `common/` und `docs/imports/common/` bleiben connectorneutral.
- `connectors/<name>/` enthält serverspezifische build/runtime-Logik.
– Generierte Konfigurationen, Protokolle, Downloads und Binärdateien bleiben unter `BUILD_ROOT`.
- Der direkte Erfolg der libmodsecurity-API zählt nie als Connector-Erfolg.

Zukünftige Envoy-, Lighttpd- und Traefik-Adapter müssen dasselbe Evidencen
`real-world-connector-path`-Semantik, bevor ein häufiger Fall als PASS gewertet wird.
HAProxy verfügt bereits über einen evidenzbasierten SPOA/SPOP-Runtimepfad; breiteres HAProxy
Fähigkeitslücken bleiben im Berichtsbesitz, bis RuntimeEvidence die Heraufstufung unterstützen.
