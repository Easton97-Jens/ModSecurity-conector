# Change Record: Endpunktmetadaten des lighttpd-Stock-Sidecars

**Sprache:** [English](CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change ID | CR-20260916-lighttpd-stock-sidecar-endpoint-metadata |
| Datum (UTC) | 2026-09-16 |
| Basisrevision | `e475baabf0787cbc804f176ae998b62156892825` |
| Benutzerautorisierung | „erstelle ein eigenen worktree und ein pr dann“ |
| Delivery-Status | Ein task-owned Parent-Worktree und ein Draft PR sind autorisiert. Kein Merge, Auto-Merge, direkter `master`-Schreibvorgang, Framework-/MRTS-/Gitlink-Change oder Branch-Löschung ist autorisiert. |

## Motivation und Problembeschreibung

Der zurückbehaltene General-State-Lauf `20260913T142629Z-e475baa` meldete 14/33
lighttpd-Stock-Sidecar-Loopback-Fehler und einen fehlgeschlagenen ersten
Real-Host-Allow-Fall. Auf der aktuellen Basis lieferte der unveränderte
gezielte Allow-Control `502`, obwohl `200` erwartet wurde.
`sidecar_exchange_request` erzeugte `msconnector_request` ohne
`request.client` oder `request.server`, während Common
`validate_request_input` begrenzte nichtleere Endpunktadressen verlangt.

## Akzeptanzkriterien

- Eine gültige akzeptierte Loopback-TCP-Anfrage übergibt Common tatsächliche
  Client-/Server-Endpunktmetadaten und kann den normalen Allow-Pfad erreichen.
- Ein Phase-1-Block liefert weiterhin `451`, gibt den Upstream nicht frei und
  sein Event meldet `client_ip` `127.0.0.1`.
- Ungültige Endpunkt-Lookups, Address-Konvertierung, Familie oder Port null
  schlagen vor Transaktionsbeginn und Upstream-Kontakt fail-closed fehl.
- Der socket-freie `runtime_begin_smoke` besitzt gültige explizite
  Testmetadaten.
- C17/Werror-Builds mit `cc` und `clang` gelingen.

## Implementierungsentscheidung und Security-Auswirkung

`sidecar_capture_request_endpoints` bezieht beide Endpunkte ausschließlich mit
`getpeername()` und `getsockname()` vom akzeptierten Client-Socket. Es lehnt
Syscall-Fehler, unerwartete sockaddr-Größen/-Familien, Konvertierungsfehler und
Ports null ab. Konvertierte Werte liegen bis zum Transaktions-Cleanup im
`sidecar_exchange_state`, sodass keine geliehenen Stack-Pointer verwendet
werden. Es gibt keinen `Host`-Header- oder fabrizierten Produktions-Fallback.

Der Listener bleibt auf literales IPv4-Loopback begrenzt. Eine fehlgeschlagene
Erfassung kann weder eine Common-Transaktion starten noch den Upstream
kontaktieren; der bestehende Connector-Fehlerpfad schlägt fail-closed fehl.
`runtime_begin_smoke` ist nicht socket-basiert, daher bleiben seine expliziten
Loopback-Werte auf synthetischen Testinput begrenzt.

## Geänderte Dateien

- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/lighttpd/stock_sidecar/runtime_begin_smoke.c`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.md`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Check | Ergebnis | Beobachtetes Ergebnis |
| --- | --- | --- |
| Stock-Sidecar-C17/Werror-Build mit `CC=cc` | bestanden | Build mit externem Task-Root und verifizierter ModSecurity-Bibliothekskopie abgeschlossen. |
| Stock-Sidecar-C17/Werror-Build mit `CC=clang` | bestanden | Unabhängiger Clang-Build abgeschlossen. |
| Gezielte Allow-, Endpoint-Metadata- und Runtime-Identity-Tests | bestanden | 3 benannte Tests im finalen Task-Worktree bestanden. |
| Vollständiges Modul `connectors/lighttpd/tests/test_stock_sidecar_contract.py` | fehlgeschlagen | 33 von 34 Tests bestanden; der Immediate-Client-Reset-Event-Fall blieb leer. |
| `git diff --check` vor dem Delivery-Setup | bestanden | Keine Whitespace-Fehler im Produkt-Diff. |

## Runtime-Evidenz

Die gezielten TCP-Sidecar-Tests übten eine echte akzeptierte Loopback-Verbindung
aus. Der neue Phase-1-Block-Test beobachtet `client_ip` `127.0.0.1`, Status
`451` und keine Upstream-Freigabe. Der ursprüngliche gezielte Allow wechselte
nach der Reparatur vom reproduzierten Fehler `502` zu `200`.

## Nicht ausgeführte Checks und Begründung

Kein reales Stock-lighttpd-Backend, keine vollständige Connector-Matrix, kein
hosted PR-Check, keine SonarQube-Cloud-Analyse, kein Review-Readback und kein
Resulting-Master-Workflow können derzeit behauptet werden. Der repositoryweite
Aufruf `make check-bilingual-docs` wurde nach 80 Sekunden ohne Ergebnis
unterbrochen und ist deshalb nicht als bestanden dokumentiert. Der Immediate-
Reset-Test bleibt unverändert, weil eine Änderung ohne nachgewiesenen
Synchronisationsvertrag einen Delivery-Lifecycle-Defekt maskieren könnte.

## Bekannte Einschränkungen und Follow-up

Das vollständige Modul hat einen fehlschlagenden Immediate-Reset-Test ohne
Event-Record nach dem Client-Reset. Das reale Stock-lighttpd-Backend und die
vollständige Matrix wurden nicht erneut ausgeführt. `FND-PARENT-1091` ist lokal
`fixed`, nicht `verified`; sein Release- und Candidate-Integration-Blocker-
Status bleibt, bis vollständiger Contract, Real-Backend und ursprüngliche
Reproduktions-/Control-Evidenz am exakten PR-Head bestehen.

## Finaler Diff und Delivery-Status

Dieser Record ist Teil des task-owned Branches. Er enthält nur lokale Evidenz,
die vor dem Draft PR verfügbar ist. Nach dem Push müssen lokaler HEAD,
Remote-Branch-SHA und PR-Head-SHA exakt verglichen werden. Erforderliche
GitHub-Checks, SonarQube, Review-/Conversation-Status und ein späterer Merge
sind ausstehend und werden von diesem Record nicht behauptet.
