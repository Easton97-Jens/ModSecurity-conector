# Migration und aktuelles Verhalten

**Sprache:** [English](migration.md) | Deutsch

Diesen Guide bei der Aktualisierung eines vorhandenen Checkouts oder einer
Konfiguration verwenden. Er erklärt Änderungen seit der früheren
Dokumentationsüberarbeitung und verlinkt die aktuellen Source-Verträge. Er
ändert keine Laufzeitstandards, wählt kein Regelwerk und behauptet keine
Validierung einer bestehenden Installation.

## Vor der Aktualisierung

Eingesetzte Connector-/Hostversionen und die tatsächlich verwendete
Konfiguration festhalten. Checkout und aufgezeichnete Submodule gemeinsam
aktualisieren. [Versions-Pins](reference/version-pins.de.md) lesen und das
passende aktuelle [Hostbeispiel](../examples/README.de.md) mit der eigenen
Konfiguration vergleichen. Service-Identitäten, private Endpunkte,
Regelzuständigkeit und Logberechtigungen erhalten.

Ein logisches Profil ist eine Topologie und nicht nur ein Hostname. Ein
Autorisierungs-/Companion-Profil nicht durch natives Streaming ersetzen und
das gleichzeitig als reine Konfigurationsaktualisierung beschreiben.

## Body-Limits gehören jetzt zur Engine

Die frühere Übergangserklärung, Connector-Response-Limits blieben als
Kompatibilitäts- oder Kapazitätswerte akzeptiert, ist nicht mehr der aktuelle
Vertrag. Die unten genannten Connector-eigenen kumulativen Request- und
Response-Optionen wurden entfernt. Unbekannte/entfernte Optionen führen zu
Konfigurationsfehlern, statt ignoriert zu werden. Es gibt keine umbenannte
kumulative Connector-Größenoption als Ersatz.

| Ebene oder Integration | Entfernte Einstellungen | Aktuelle Policy-Zuständigkeit |
| --- | --- | --- |
| Common Runtime | `request_body_limit`, `response_body_limit`, `body_limit_action` | Native Engine-Regelkonfiguration |
| Native Connector-Direktiven | `modsecurity_request_body_limit`, `modsecurity_body_limit_action`, `modsecurity_response_body_limit`, `modsecurity_phase4_body_limit` | Native Engine-Regelkonfiguration |
| HAProxy-Filteroptionen | `request-body-limit`, `response-body-limit` | Native Engine-Regelkonfiguration |
| Envoy-Serviceoptionen | `max_request_body_bytes`, `max_response_body_bytes` | Native Engine-Regelkonfiguration |
| Traefik-Native-Middleware-Option | `maxRequestBodyBytes` | Native Engine-Regelkonfiguration |

Für Request-Inspection `SecRequestBodyAccess`, `SecRequestBodyLimit`,
`SecRequestBodyNoFilesLimit` und `SecRequestBodyLimitAction` prüfen. Für
Response-Inspection `SecResponseBodyAccess`, `SecResponseBodyMimeType`,
`SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit` und
`SecResponseBodyLimitAction` prüfen.

Ein altes Connector-Limit nicht mechanisch in einen neuen Engine-Wert
übersetzen, sondern die beabsichtigte Anwendungspolicy prüfen. Der Connector
darf keine Werte aus Regeltext ableiten, Standards einfügen,
Reject/ProcessPartial auswählen oder Bodies auf einen eigenen
Inspection-Präfix kürzen. Ohne explizite Direktiven bleibt die native
libModSecurity-Semantik bestehen. Auch `DetectionOnly` behält tatsächliche
Engine-Semantik. Maßgebliche Details stehen unter
[Body-Limit-Zuständigkeit](phase4-mode-budget.de.md).

## Phase-4-Modi sind keine Größenrichtlinien

`off`, `safe` und `strict` wählen unterstützte späte Interventionsbehandlung.
Sie wählen keine MIME-Typen, kein Byte-Budget und keine Engine-Limitaktion.

`off` schaltet weder Engine noch Response-Inspection ab. `safe` erlaubt nicht,
native Reject-Ergebnisse, Transportfehler oder Verarbeitungsfehler zu
ignorieren. `strict` benötigt eine unterstützte Hostaktion des gewählten
Profils und kann bereits beim Start abgewiesen werden. Bereits gesendeter
Status, Header und Bytes lassen sich nicht zurücknehmen. Das Beispiellayout
`all` ist kein vierter Phasenmodus.

Der gemeinsame Source-Standard für Phase 4 ist `off`, definiert durch
`MSCONNECTOR_DEFAULT_PHASE4_MODE` in `common/include/msconnector/options.h`.
Ein Beispiel mit explizitem `safe` oder `strict` ändert diesen Source-Standard
nicht. Für Kontext und Vererbung die generierten Hostreferenzen verwenden.

## Verbleibende Sicherheitsgrenzen

Das Entfernen kumulativer Connector-Inspection-Limits entfernt weder begrenzten
Arbeitsspeicher noch Validierung. Grenzen einzelner Chunks/Frames/Nachrichten,
Header-/Event-Metadatenlimits, Korrelationslimits, Timeouts, Deskriptor- und
Dateibereichsvalidierung, geprüfte Lesezugriffe, Pointerprüfungen und
Überlaufschutz bleiben erhalten. Ein wiederverwendbarer Arbeitsbuffer ist keine
Grenze für die gesamte Body-Größe.

Autorisierungswege besitzen weiterhin echte Host- oder Protokollgrenzen:

| Profilgrenze | Verbleibende Einschränkung |
| --- | --- |
| Envoy ext_authz | Host-`max_request_bytes` begrenzt den an die Autorisierung gelieferten Request-Body; der Response-Observer macht Requests nicht inkrementell |
| Traefik forwardAuth | Host-`maxBodySize` puffert und begrenzt den weitergereichten Request-Body |
| Zusammengesetzte Traefik-Autorisierungsresponse | Host-`maxResponseBodySize` begrenzt die Autorisierungsresponse, nicht die Response der Upstream-Anwendung |
| HAProxy SPOE/SPOP | Eine begrenzte Nachricht trägt eine Request-Stichprobe; eine unvollständige Stichprobe beweist keine vollständige P2-Inspection |

Diese Hosteinstellungen nicht entfernen, nur weil eine ähnlich benannte
Connector-Option entfernt wurde. Native Streaming-Profile sind getrennte
Wege. Die [Matrix der zehn Profile](body-inspection-review-matrix.de.md) und
den passenden Host-Guide zu unvollständigen Stichproben,
Framing-Einschränkungen und nicht nachgewiesenem Verhalten lesen.

## Testauswahl ist zentralisiert

Normale lokale, CI- und geplante funktionale Prüfungen verwenden
[config/testing/active-cases.json](../config/testing/active-cases.json).
Der 100-Fälle-Kern und die getrennt autorisierte geschützte
Offline-Python-Ausnahme werden getrennt gezählt. Zusätzliche Offline-Fälle
bedeuten keine zusätzliche Connector-E2E-Auswahl.

```sh
make check-active-inventory
make quick-check
```

Die Zulassungsprüfung validiert das gesamte Inventar ohne Teststart.
`make test` führt die zugelassene Auswahl mit ihren tatsächlichen
Voraussetzungen aus. Unbekannte/leere Auswahl und geänderte Quellbindungen
sind Fehler und kein Anlass, die Auswahl zu kürzen oder Prüfungen zu umgehen.
Standardaliase und Filter bleiben Teilmengen und keine vollständigen
Profilnachweise.

Archivierte Prüfsuiten sind keine automatischen Standards. Spezialausführung
benötigt einen gesonderten aktuellen Auftrag und die dokumentierte explizite
Auswahl `ON_DEMAND_TESTS=1`. Weder dieser Guide noch das Flag autorisiert neue
I12-Aufzeichnungen. [Tests und Nachweise](testing-and-evidence.de.md),
[Test-Einstiegspunkte](../tests/README.de.md) und die dokumentierten Abschlüsse
unterscheiden aktuelle Auswahl und historische Abdeckung.

## Toolchains, generierte Dateien und externe Herkunft

`ci/tooling/project-versions.lock.json` besitzt die normale Auswahl von
Projekt-Toolchains und Framework-/MRTS-Revisionen. `.python-version` und
`.go-version` sind generierte Ansichten. Security-Tool-/Action-Pins und
Identitäten geschützter Broker behalten ihre getrennten geprüften Verträge.
Keine Ansicht isoliert ändern und keine veränderliche Quelle einsetzen, nur
damit ein lokaler Befehl besteht.

Generierte Compiler-Guides, `examples/common/`, Host-Konfigurationsreferenzen
und generierte Reports müssen über ihren Generator-/Source-Vertrag
aktualisiert werden. Manuelle Formulierungsverbesserungen gehören in gepflegte
Guides, sofern nicht bewusst auch der Generator angepasst und neu ausgeführt
wird.

Der [Bereich licenses](../licenses/README.de.md) bleibt ein
Herkunfts-/Referenzbereich: Upstream-Projekt, aufgezeichnete Revisions- und
Lizenzbasis, aufbewahrte Hinweise und lokale Unterschiede. Er lizenziert
übernommenes Material nicht neu und erklärt keine einheitliche Lizenz für das
gesamte Repository.

## Migrierte Einrichtung validieren

Zuerst die gewählte Hostkonfiguration mit ihrem dokumentierten Checker oder
Root-`check-config`-Target validieren. Anschließend nur die beabsichtigten
zugelassenen Tests ausführen. Für jede Laufzeitaussage Revision, logisches
Profil, Regeln, Run-ID, Artefakte und verbleibende Grenzen festhalten. Ein
bestandener Parser-, Build-, Dokumentations- oder Scannercheck qualifiziert
kein Deployment.

Bei Dokumentationsänderungen `make check-bilingual-docs` und
`make check-doc-links` verwenden. Für Betriebsrisiken und sensible Daten
[Betrieb und Sicherheit](operations-and-security.de.md) lesen.
