**Sprache:** [English](pr27-issue-reduction.md) | Deutsch

# PR 27 Sonar-Issue-Inventar

Diese deutsche Begleitdatei fasst die lokalen Common-SDK-Korrekturen zusammen.
Die Änderungen betreffen connector-neutrale Common-SDK-Hilfen, C-Standard-Probes,
Ereignis-/JSONL-Trunkierungsverhalten, Header-/Pfad-/Konfigurationsvalidierung
und neue Common-Infrastruktur.

SonarCloud after-count: NOT VERIFIED.

Es wird keine Connector-Laufzeitintegration, keine Produktionsreife und keine
Connector-Fähigkeit behauptet.

## Abschluss des Common-SDK-Pakets

Ergänzt wurden lokale, ausschließlich common-bezogene Helfer für
Konfigurationsparser, Request-/Response-Validierung, Rule-Merge/Error/Event,
Test-Result-JSON, Connector-Manifeste, Runtime-Report-Skelette,
Origin-Governance, Build-Verträge, C++-Wrapper, Limits, Rule-ID-Extraktion,
Log-Sanitizing und Body-Snippet-Redaktion.

SonarCloud after-count: NOT VERIFIED.

## PR-27-Bereinigung für SonarCloud und Codex Review

SonarCloud-Issue-Abruf: lokal über die SonarCloud-Issues-API für Pull Request 27 am 2026-07-02 verifiziert.

Lokale Korrektur: Die offenen neuen SonarCloud-Hinweise wurden in den Common-SDK-Dateien durch explizitere Deklarationen, ausgeschriebene Kontrollflüsse, entfernte verschachtelte Bedingungsoperatoren, einen gruppierten Event-JSON-Formatter und Shell-Hilfsfunktionen mit lokalen Parameterzuweisungen adressiert. Diese Änderungen bleiben connector-neutral und ändern keine Connector-Laufzeitpfade.

SonarCloud after-count: NOT VERIFIED. Die lokalen Prüfungen lösen keine neue SonarCloud-Analyse aus.

## PR-27-Folgekorrektur für Codex-Review-P2-Hinweise

Die lokalen Folgekorrekturen bleiben ausschließlich im Common SDK und ändern keine Connector-Laufzeitpfade.

- `ALLOW`- und `LOG_ONLY`-Entscheidungen erzeugen keine Blockierungsereignisse mehr.
- Transaction-IDs aus Headern verwenden jetzt die begrenzte Header-Slice-Länge.
- Spezifische Entscheidungsaktionen wie Drop und Connection-Abort bleiben erhalten.
- Ruleset-Neuladen ersetzt das alte Ruleset erst nach erfolgreicher Erstellung.
- Artifact-Helfer lehnen terminale Parent-Directory-Segmente ab.
- Adapter-Verträge vergleichen deklarierte Phasen-Capabilities mit passenden Callbacks.
- Rule-Load-Events verwenden aufruferverwalteten Reason-Speicher.
- `transaction.h` stellt Decision-Deklarationen für Starter-Header wieder bereit.
- `MSCONNECTOR_ERROR_NONE` erzeugt kein Fehlerereignis.

GitHub review thread resolved state: NOT VERIFIED.
SonarCloud after-count: NOT VERIFIED.

## PR-27-Folgekorrektur für Starter-Kompatibilität aus Codex Review

Die lokalen Korrekturen bleiben ausschließlich im Common SDK und übernehmen das
Common SDK nicht in Connector-Laufzeiten.

- `common/src/transaction.c`: Kompatibilitäts-Konstruktoren für Decisions werden nun aus dem Transaction-Objekt gelinkt, das Starter-Builds bereits verwenden.
- `common/src/adapter_contract.c`: deklarierte Phasen-Capabilities verlangen weiterhin passende Adapter-Callbacks, ohne Nicht-Phasen-Capabilities zu übererzwingen.
- `common/include/msconnector/transaction.h`: Decision-Deklarationen bleiben für Header verfügbar, die nur `transaction.h` einbinden.
- `common/src/error.c`: NULL-Errors und `MSCONNECTOR_ERROR_NONE` erzeugen kein Internal-Error-Event.
- `common/src/headers.c`: begrenzte Header-Value-Slice-/Copy-Helfer wurden für Pointer-plus-Length-Werte ergänzt; Request-/Response-Content-Type-Slice-Helfer verwenden diese APIs.
- `common/src/rule_loader.c`: unvollständige Remote-Rule-Key/URL-Paare werden vor Inline- oder Datei-Backend-Aufrufen abgelehnt.
- `common/src/transaction_id.c`: Expression-Callback-Ausgaben werden vor der Validierung geleert und begrenzt geprüft; nicht terminierte volle Puffer werden sicher abgelehnt.

GitHub review thread resolved state: NOT VERIFIED.
SonarCloud after-count: NOT VERIFIED.

## Verbleibende Common-SDK-Sonar-Korrekturen

- `common/include/msconnector/transaction.h`: Include-Reihenfolge korrigiert, indem gemeinsame Phase-Deklarationen nach `common/include/msconnector/phase.h` verschoben wurden. `decision.h` bindet nun `phase.h` ein, und `transaction.h` bindet `decision.h` im oberen Include-Block ein, damit Starter-Header weiterhin `msconnector_decision`-Deklarationen sehen.
- `common/src/rule_event.c`: Pointer-to-const-Hinweis korrigiert, indem nur der alte deaktivierte Wrapper `msconnector_rule_load_event()` einen Parameter `const msconnector_event *` erhält; `msconnector_rule_load_event_ex()` behält den veränderbaren Event-Zeiger, weil die Funktion das Event befüllt.
- SonarCloud-Nachzählung: NOT VERIFIED.

## Aktuelle Codex-Review-Härtungen

- `common/src/json_escape.c`: JSON-Escaping schreibt nur noch vollständige Escape-Sequenzen und vermeidet teilweise `\`, `\n`- oder `\u00XX`-Fragmente bei abgeschnittenen Feldern.
- `common/src/modsecurity_engine.c`: Transaktions-Cleanup setzt `native_transaction` auch dann zurück, wenn kein Backend-Callback `free_transaction` vorhanden ist.
- `common/src/decision.c`: Blockierungs-Event-IDs werden aus der Entscheidungsphase gewählt, sodass Response-Phasen Response-Blocked-Metadaten verwenden.
- `common/src/rule_loader.c`: Remote-Regel-Key/URL-Paare werden vor Inline-/Datei-/Remote-Backend-Mutationen auf NULL und leere unvollständige Werte geprüft.
- `ci/common-harness.sh`: Under-Root-Prüfungen verwerfen Parent-Directory-Segmente, bevor ein Root-Präfix akzeptiert wird.
- `common/include/msconnector/request.hpp`: C++-Wrapper-Aliase für Starter-Kompatibilität wurden wiederhergestellt.
- `common/src/headers.c`, `common/src/request_helpers.c` und `common/src/response_helpers.c`: Begrenzte Slice-/Copy-Helfer bleiben der sichere Pfad; rohe Content-Type-Helfer geben keine begrenzten Slices als C-Strings mehr zurück.
- SonarCloud-Nachzählung: NOT VERIFIED.

## PR-29-Common-SDK-Review-Korrekturen

- `common/src/transaction_id.c`: Transaktions-ID-Validierung verwirft nun Nicht-ASCII-Bytes oberhalb des druckbaren ASCII-Bereichs und behält begrenzte Header-/Expression-Prüfung bei.
- `common/src/config.c`: Konfigurationsvalidierung behandelt NULL und leere Remote-Regel-Felder konsistent und verwirft unvollständige Key/URL-Paare vor dem Rule Loading.
- `common/src/late_intervention.c`: Strikter Late-Intervention-Abbruch greift nur, nachdem Header gesendet wurden oder der Response-Body gestartet ist; vor Ausgabebeginn bleibt ein sauberer Deny möglich.
- `common/src/transaction.c`: Kompatibilitäts-Konstruktoren leiten die Entscheidungsart aus dem Status ab, wenn die Intervention nicht disruptiv ist, sodass BLOCKED/ERROR nicht als ALLOW verbleibt.
- `common/src/http_status.c`: Nicht-blockierende Metadaten für HTTP `302 Found` wurden ergänzt, damit Redirect-Events korrekten Statustext haben.
- SonarCloud-Nachzählung: NOT VERIFIED.
