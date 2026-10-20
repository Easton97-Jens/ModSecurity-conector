# Change Record: CR-20261020-traefik-trusted-provenance

**Sprache:** [English](CR-20261020-traefik-trusted-provenance.md) | Deutsch

Produktänderung für #382; die Host-Abnahme bleibt bei #413.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261020-traefik-trusted-provenance |
| Datum (UTC) | 2026-10-20 |
| Basis-Revision | `c5012b70c78ae2629eeede6603f591dfb002dd9a` |

## Motivation und Problemstellung

Traefiks C-Autorisierungsroute konnte vor P1 keine vertrauenswürdige Downstream-Provenienz für Run, Fall und Verbindung anhängen. HTTP-Forwarding-Felder und der Autorisierungs-Loopback-Socket belegen keine physische Client-Wiederverwendung.

## Akzeptanzkriterien

Begrenzte vertrauenswürdige IDs vor P1 kopieren; alte Aufrufer erhalten; gefälschte, doppelte, abgelaufene und mehrdeutige Bindungen ablehnen; Autorisierungsantworten privat binden; EOS und Cleanup aus Runtime-Zustand ableiten; native, private Socket-, Go/Race/Vet- und Security-Grenzen prüfen.

## Implementierungsentscheidung und Begründung

Additive Common-Begin- und Autorisierungs-Entry-APIs erhalten Signaturen und Profil-Layout. Der optionale Traefik-MTP1-Listener verwendet einen separaten privaten benachbarten Socket, gleiche UID/GID zur Authentisierung, 128 feste Slots, fünf Sekunden gültige Leases und zufällige Einmal-Capabilities. Metadaten werden vor nativem P1 kopiert; Antwortstatus/Companion-Handle des Dienstes werden über dieselbe Sitzung bestätigt. Der äußere Observer verbraucht diese Bestätigung vor dem Commit. Das MRC1-Wire-Protokoll und die gewöhnlichen/standardmäßigen Aufrufpfade, gemeinsamer Envoy-Connector-Code, Generatoren und Matrizen bleiben unverändert; die Common-Registry erhält eine additive API für vertrauensgebundene Bestätigung. Vertrauenswürdige Allow-Phasendatensätze erfinden keine Regelintervention. Cleanup reserviert seine Sequenz vor Flow-Unveränderlichkeit und schreibt erst nach nativem Free und Vertrags-Cleanup; Sink-Fehler werden nicht als erfolgreicher geprüfter Cleanup behandelt.

## Geänderte Dateien

`common/runtime/msconnector_runtime.{c,h}`, `common/runtime/http_authorization_service.{c,h}`; Traefik `src/traefik_provenance.{c,h}`, `src/traefik_forwardauth_service_main.c`, `build/build-connector.sh`, `response_observer/observer.go`, `response_observer/provenance{,_test}.go`, `response_observer/README{,.de}.md`; `ci/checks/common/check-http-authorization-service-timeout.sh`, `ci/checks/common/http_authorization_service_timeout_smoke.c`; `tests/http_authorization_service_{detached_worker,peer_close,trusted_binding}_smoke.c`, `tests/test_http_authorization_service_worker_contract.py`, `tests/test_i10_service_callers.py`, `tests/test_runtime_event_sink_failures.py`, `tests/test_runtime_trusted_provenance.py`, `tests/test_traefik_trusted_provenance.py`, `tests/test_engine_response_limits.py`, `tests/transaction_phase_runtime_companion_test.c` und dieses Change-Record-Paar.

## Ausgeführte Befehle

Alle Shell-Befehle liefen über RTK. Initiale Prüfung vor der Preclaim-Korrektur: Der Traefik-Repository-Build bestand mit `MODSECURITY_INCLUDE_DIR=/usr/include`, `MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu` und externem Task-Buildverzeichnis. Observer `go test -count=1 -v ./...` und `go test -race -count=1 -v ./...` bestanden jeweils 42 Tests; `go vet ./...` bestand. Go-Prüfungen verwendeten explizit den isolierten Go-1.27.2-GOROOT und speicherten `go env GOROOT GOVERSION`. Die initiale kombinierte Common/Auth/Native/Private-Socket-Suite bestand 100 Tests mit vier Skips (drei bestehende Skips und der durch die Traversal-Grenze des eingeschränkten Testroots blockierte Fremd-UID-Test). Dieselbe Fremd-UID/GID-Kontrolle bestand separat außerhalb der Sandbox mit durchsuchbarem externem Testroot. Common-SDK-/Security-Verträge und Change-Record-Struktur bestanden. Repository-Sprachpaare und Links aller vier geänderten Dokumentationsdateien bestanden; die vollständige Bilingual-/Link-Prüfung traf 22 bereits fehlende Framework-Submodule-Linkziele.

Nach der Preclaim-Korrektur bestanden 28 fokussierte Python-/Native-Tests mit einem Sandbox-UID-Skip; dieselbe UID/GID-Kontrolle bestand separat außerhalb der Sandbox. Echte verzögerte MTP1/Common-Claim-Positivkontrolle und kompilierte Negativkontrolle ohne Ablauf-Update bestanden. Isoliertes Go 1.27.2 Test/Race/Vet, strikte C17-Syntaxprüfung, Common-Security-Vertrag und `git diff --check` bestanden. Die Repository-weite Bilingual-Prüfung meldet weiterhin ausschließlich dieselben 22 fehlenden Framework-Submodule-Ziele. Eine abschließende enge Replay-Testkorrektur akzeptiert Reset/Broken-Pipe beim Senden oder Empfangen auf dem bereits geschlossenen Peer; die fokussierte Replay-Kontrolle bestand nach dieser Korrektur.

## Security-Auswirkung

Nur die private authentisierte Lease liefert Provenienz. Client-Capabilities werden vor der Reservierung verworfen; der Dienst entfernt den internen Token nach erfolgreichem Claim aus nativen P1-Headern. Die Bereitstellung erfordert äußerer Observer → eingebautes ForwardAuth → innerer Observer mit `confirmProvenance: true` → Backend. Die explizite `authRequestHeaders`-Liste enthält den privaten Token. Die innere Instanz verlangt den paketprivaten äußeren Request-Kontext, bestätigt einmal vor dem Backend und entfernt beide privaten Header/Trailer. Gleiche Unix-IDs bilden eine Vertrauensdomäne, keine Binärattestierung. Bestehende Authentisierung und Validierung bleiben wirksam.

## Runtime-Evidence

Tests verwenden physische Unix-Sockets, echtes libModSecurity-P1-Deny, Allow mit Companion-P3/P4, Abbruch vor Request-EOS sowie tatsächliche Common-Serialisierung, Cleanup und Sink-Fehler. Eine kompilierte Negativkontrolle ohne Kopie reproduziert die Provenienzlücke. Kontrollen erfassen Kapazitätssättigung ohne Nachbarverdrängung, echte Fremd-UID/GID-Ablehnung, Fake-Go-Transport-Reihenfolge bei Backend-Wartezeit über fünf Sekunden, fehlende/doppelte innere Bestätigung, typisierten Abbruch bei Panic/Cancel/Return vor Headern und ein physisches payloadfreies Cleanup-Fehlerlog. Separat belegen echte Common-/Native-Handles und eine physische MTP1-Abfrage initialen Fünf-Sekunden-Ablauf sowie einen nach Bestätigung nach 5,1 Sekunden noch gültigen Handle. Eine kompilierte Kontrolle ohne Ablauf-Update reproduziert den späten Claim-Fehler. Die Shutdown-Bestätigungsablehnung verwendet einen echten unbeanspruchten Handle mit einer ausdrücklich synthetischen reinen Metadaten-Blocker-Lease. Diese Ebenen qualifizieren keine Traefik-Host-Keepalive-ID und belegen keine Downstream-Clientzustellung.

## Bekannte Einschränkungen

Dem Observer fehlt ein zuverlässiger Schließhook für lebende Verbindungen. Sein instanzlokaler HMAC-Tupeltoken ist Korrelation; `connection_reused` bleibt false. Physische Belege für denselben lebenden Socket bleiben erforderlich. Runtime-Body-Finish-Zustand, niemals TCP-EOF, liefert `eos_seen`. `maxResponseBodySize=32768` bleibt Kapazität der Autorisierungsantwort. Die innere Bestätigung cached die Attestation vor Backend-Wartezeit. MRC1-Claim erfolgt normal beim ersten Response-Header; früheres Verlassen beansprucht nur für sofortigen typisierten Abbruch mit eigenem begrenzten Kontext. Fehlgeschlagener Cleanup bleibt erhalten und geloggt; bestehender begrenzter Companion-Ablauf bleibt Fallback.

## Verbleibende Risiken

Der optionale Modus hängt von dokumentierter Middleware-Reihenfolge und innerer Bestätigung ab. Autorisierung/Bestätigung über die feste Fünf-Sekunden-Reservierungslease hinaus schlägt fail-closed fehl. Normales MRC1-Preclaim läuft weiterhin nach fünf Sekunden ab. Die peer-authentisierte innere MTP1-Abfrage bestätigt ihren unbenutzten, noch gültigen Handle genau einmal unter Registry-Lock vor seiner Ausgabe: Der Ablauf wird auf den ursprünglichen Handoff plus konfigurierte TTL (Traefik 30 Sekunden) gesetzt und gewährt nur die verbleibende Laufzeit. Deny/leere, abgelaufene, wiederholte, beanspruchte, verwendete, fremde und Shutdown-Einträge lassen sich nicht verlängern; Callback-Fehler sperren den Backend-Eintritt. Der Go-Test mit langsamem Backend belegt nur Fake-Transport-Reihenfolge; ein physischer MTP1/Common-Registry-Test prüft reguläres Scheitern und bestätigten Erfolg nach 5,1 Sekunden. Complete läuft ausschließlich nach erfolgreichem privatem Claim, einschließlich eines anschließenden Runtime-Begin-Fehlers. Unabhängiges finales Review und Traefik-Host-Retakes bleiben erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Für diesen uncommitteten Diff werden keine vollständige Traefik-Host-Abnahme, CI- oder Sonar-Ergebnisse behauptet. #413 übernimmt Host-Retakes und ID-Qualifizierung nach Produktreview. Repository-weites Bilingual-/Link-PASS ist durch das nicht initialisierte Framework-Submodule blockiert; kein Framework-Inhalt oder gemeinsamer Generator wurde zum Verdecken verändert. Geänderte Dateilinks und Repository-Sprachpaare wurden unabhängig geprüft.

## Finaler Diff- und Review-Status

Uncommitteter Diff auf Basis `c5012b70c78ae2629eeede6603f591dfb002dd9a`; unabhängige Security- und Lifecycle-Reviews fanden keinen Blocker. `git diff --check` bestand. Dieser Worker hat weder committet noch gepusht oder gemergt. Host-Retakes und Repository-weite Dokumentationsvoraussetzungen bleiben ausdrücklich offen.
