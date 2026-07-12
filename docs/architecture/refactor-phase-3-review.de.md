# Refactor-Phase-3-Überprüfung

**Sprache:** [English](refactor-phase-3-review.md) | Deutsch

Status: umgesetzt

## Extrahiert

In Phase 3 wurde nur die connectorneutrale Hilfslogik extrahiert:

| Bereich | Gemeinsamer Helfer | Grund |
| --- | --- | --- |
| Statusmetadaten | `common/src/status.c` | Ordnet Runtimeergebniswörter `msconnector_status`-Namen zu |
| Interventionsmetadaten | `common/src/intervention.c` | Erstellt die neutrale Interventionsdatenform |
| Ursprungsmetadaten | `common/src/origin.c` | Stellt die Herkunft ohne Connector-Besitz dar |
| Fähigkeitsbeschreibungen | `common/src/capabilities.c` | Benennt und erstellt konnektorneutrale Fähigkeitsflags |

Die Python-Harness-Ebene spiegelt diese Konzepte wider
`modules/ModSecurity-test-Framework/tests/runners/msconnector_models.py`; Es werden weder FFI, `ctypes` noch ein C verwendet
Bridge-Binärdatei.

## Aufgeschoben

Die folgenden Kandidaten bleiben connectorspezifisch:

- Apache-Hook-Registrierung und Filter.
- Apache bucket/error-Helfer, einschließlich `send_error_bucket()`.
- NGINX-Modulregistrierung und body/header-Filter.
- NGINX-Requestszeichenfolgenkonvertierung, PCRE-Pool-Helfer und Protokollrückruf.
- Serverspezifisches Konfigurations-Parsing.
- Request/response Körperbesitz und Pufferung.
- Lebensdauer der libmodsecurity-Transaktion.
- `RESPONSE_BODY`-Blockierungsverhalten.

Phase 5 bestätigte, dass es sich hierbei nicht um sichere Kandidaten für den zweiten Austausch handelt.
Selbst wenn ein Helfer klein ist, ist er in die Konfiguration request/response eingebettet.
Lebenszyklus, Audit oder Apache-Bucket-Verhalten. Zukünftige Arbeiten sollten zunächst vorgestellt werden
Repo-eigener Adaptercode um ein enges Verhalten herum, dann Evidencen Sie die Äquivalenz mit
reale Apache- und NGINX-Smoke-Läufe.

## Risiken

- C- und Python-Metadatennamen können abweichen. `ci/checks/common/check-common-helpers.sh`,
`make lint` und zusammenfassende Schemaprüfungen sind die aktuellen Leitplanken.
– Ein zukünftiger Connector benötigt möglicherweise zusätzliche Funktionsnamen. Das sollten die sein
Nur anhängen hinzugefügt und im Python-Modell gespiegelt.
- Die allgemeinen Helfer sind noch kein Produkt-Connector-Code. Jede Produktionsverwendung muss
mit separatem Smoke-Nachweis eingeführt werden.
– In Phase 6 wurden Adapter-eigene Metadatenskelette außerhalb von `common/` hinzugefügt. Diese Dateien
nennen möglicherweise Apache oder NGINX als Komponenten, vermeiden aber dennoch Server-Header.
libmodsecurity-Besitz und produktive Runtimepfade.
– Phase 9 macht den NGINX-Quelladapter zum Eigentum des Adapters, aber das bleibt außerhalb von Common.
Die NGINX-Modulquellen besitzen weiterhin NGINX-spezifische Hooks, Filter usw
Transaktionsintegration; Common übernimmt diese Pfade nicht.
