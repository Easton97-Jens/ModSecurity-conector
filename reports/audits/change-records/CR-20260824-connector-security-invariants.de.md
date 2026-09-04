# Change Record

**Sprache:** [English](CR-20260824-connector-security-invariants.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260824-connector-security-invariants |
| Datum (UTC) | 2026-08-24 |
| Basis-Revision | a6b4ced4876a19666f7c7203ed9e719674c69ec1 |
| Baseline der aktuellen uncommitted Erweiterung | 8d8907f605a36ed8139d891f03f028cafb06bc99 |
| Repository-Grenze | Nur Parent; Framework, MRTS, Gitlink, CI und Governance unverändert |
| Delivery-Autorität | Der aktuelle Benutzer hat Parent-Commit, Push und Draft-PR-Erstellung ausdrücklich autorisiert; kein Merge |

## Motivation und Problemstellung

Die angeforderte Prüfung umfasst zehn Connectorvarianten und ihre gemeinsamen
Common-, Engine-, Provisioning- und Runtime-Grenzen. Der Source-Review fand
drei Parent-eigene Hardening-Möglichkeiten mit konkreter Kontrolllücke:
Remote-Rule-Konfiguration konnte libmodsecurity-Remote-Laden ohne einheitliche
Trust-Policy erreichen; der nicht authentifizierte HTTP-Autorisierungshelfer
akzeptierte einen Wildcard-Listener, doppelte sicherheitsrelevante Header und
eine stille Listener-Adresssubstitution bei fehlendem oder zu großem `Host`;
und Common-Event-Ausgabe konnte unescapte Protocol-Metadaten serialisieren und
einen unsicheren finalen Event-Pfad öffnen.

Ein fokussierter zweiter Common-Re-Audit fand drei weitere unabhängig
behebbare Grenzen: Nur positive Ressourcenkonfiguration konnte Header-/Event-/
Body-Hard-Caps vor Allokationspfaden überschreiten; fehlerhafte UTF-8-Bytes
konnten ungültiges Event-JSONL erzeugen; und ein abgetrennter
Autorisierungsworker konnte nach Ablauf beider begrenzten Shutdown-Waits das
stackbesessene Service-Objekt überleben.

Der ausführbare direkte NGINX-Archivpfad liegt im separaten Framework-
Repository. Die aktuelle Autorisierung erlaubt nur Parent-Änderungen;
Framework-Write-/Test-Arbeit erfordert eine explizite Repository-Auswahl durch
den Benutzer. Der Pfad wird daher als blockierte Remediation-Abhängigkeit
berichtet und weder hier gepatcht noch als sicher extrahiert dargestellt.

## Akzeptanzkriterien

- Jeder geprüfte Parent-Remote-Rule-Einstiegspunkt lehnt vollständige und
  unvollständige Remote-Rule-Konfiguration vor einem netzwerkfähigen Sink ab.
- Apache, NGINX und Common Runtime behalten keinen produktiven
  `msc_rules_add_remote`-Pfad; alle Connector-Capability-Records beschreiben
  dieselbe Policy.
- Native Apache, HAProxy SPOE/SPOP und NGINX schlagen bei abgelehnter Engine-
  Operation, fehlender Authority/fehlendem Host oder Überschreitung des
  Request-Body-Budgets fail-closed fehl; keiner ersetzt Client-Authority still
  durch einen Listener-, Virtual-Server-, Server-Endpunkt- oder `localhost`-
  Wert.
- HAProxy HTX schlägt nach Setup-, Sequenz-, Header- oder Body-Append-Fehlern
  fail-closed fehl; der SPOP-Diagnoseparser hat endliche Reads,
  überlaufsichere Varints, begrenzte Strings und Header-Byte-Validierung.
- Envoy ext_proc akzeptiert nur numerische Loopback-Listener, hat endliche
  Connection-/Stream-Admission und lehnt Requests ohne `:authority` und ohne
  `Host` vor dem Engine-Mapping ab.
- Der Traefik-Native-UDS-Dienst besitzt weder eine unbeschränkte Worker-Queue
  noch einen Default-Lifetime-Shutdown: Er lässt höchstens 64 aktive Worker bei
  einem Backlog von 32 zu; ein positives explizites `--max-connections` bleibt
  eine kontrollierte One-shot-Testgrenze.
- Der nicht authentifizierte Common-HTTP-Autorisierungsendpunkt bleibt
  Loopback-only und lehnt doppelte, fehlende, leere oder zu große `Host`-
  Werte sowie konfigurierte Original-URI-Header vor dem Transaction-Mapping
  ab; er ersetzt den Hostnamen nie durch die Listener-Adresse.
- Event-Metadaten bleiben payloadfreies JSONL, sind escaped und NULL-sicher,
  und die POSIX-final Event-Datei ist no-follow, regulär und privat (`0600`).
- Die FNV-basierte Event-Kette ist nur als prozesslokale, nicht-kryptografische
  Korrelation dokumentiert; sie wird nicht als Tamper-Evidence beschrieben.
- Common-Header-/Event-Ressourceneinstellungen weisen Werte über ihren festen
  Obergrenzen ab; Request-, Response- und Phase-4-Body-Konfiguration weist
  Werte über 10485760 Byte (10 MiB) ab.
- Event-JSONL erhält valides UTF-8, encodiert fehlerhafte Bytes als `\\u00XX`
  und begrenzt jeden Event-Field-Scan; Request- oder Response-Body-Payloads
  werden nie ausgegeben.
- Ein abgetrennter Autorisierungsworker referenziert nie einen zerstörten
  Service/Runtime; Deferred-Shutdown übergibt das finale Cleanup sicher an den
  letzten Worker.
- Kein Workflow-, Branch-Protection-, Ruleset-, Required-Check- oder anderer
  Governance-Pfad wird geändert.

## Implementierungsentscheidung und Begründung

Für Remote Rules wurde Policy A gewählt: Remote-Laden ist einheitlich
deaktiviert. Die vorhandenen Common-, Apache- und NGINX-Quellpfade erzwingen
gemeinsam weder HTTPS, Origin-Allowlisting, Integritätsprüfung, Größen- und
Zeitgrenzen, atomare Aktivierung noch Credential-Isolation, die eine sichere
Remote-Loading-Policy benötigen würde. Konfigurationsvalidierung, Common
Loader, Common Runtime und beide Host-Directive-Handler schlagen nun vor einem
Fetch oder nativen Remote-API-Aufruf fail-closed fehl. Inline Rules und lokale
Rules-Dateien bleiben unterstützt.

Der Common-HTTP-Autorisierungsdienst besitzt keinen authentifizierten
Transportmodus. Sein Listener-Parser normalisiert deshalb `localhost` zu
`127.0.0.1` und lehnt Wildcards sowie andere Adressen ab. Außerdem weist er
doppelte `Host`- und profildefinierte Original-URI-Header zurück, bevor ein
ausgewählter Wert das Mapping beeinflussen kann. Ein fehlender, leerer oder zu
großer `Host` erhält nun vor dem Mapping eine 400-Antwort, statt still zur
Listener-Adresse zu werden. Das bestehende begrenzte Worker-Admission- und
Shutdown-Ownership-Modell bleibt erhalten; Shutdown liefert einen definierten
Fehler, statt Runtime-Objekte zu zerstören, die noch ein ununterbrechlicher
Worker hält.

Event-Protocol-Text wird mit dem gemeinsamen JSON-Escaper escaped. Der POSIX-
Event-Sink wird mit `O_NOFOLLOW` geöffnet, als reguläre Datei geprüft, mit
`fchmod(0600)` eingeschränkt und anschließend in einen Stream überführt.
Windows besitzt in dieser Implementierung keine äquivalente Reparse-Point-
Kontrolle und schlägt daher fail-closed fehl, statt einen konfigurierten
Event-Pfad zu öffnen. Die Änderung behauptet bewusst keine
prozessübergreifende Tamper-Resistenz.

Der Common-Content-Length-Parser weist nun jeden doppelten Wert zurück,
einschließlich identischer Duplikate. Das vermeidet die Abhängigkeit von
unterschiedlichen Host-Normalisierungsregeln an einer
Request-Smuggling-sensitiven Übersetzungsgrenze.

Ressourcenlimits sind nun sowohl in der Common-Ressourcenvalidierung als auch
in der Runtime-Konfigurationsvalidierung begrenzt. Vorhandene eingecheckte
Profile mit einem 10-MiB-Body-Limit bleiben gültig, während größere Request-,
Response- oder Phase-4-Budgets fehlschlagen, bevor Common-Buffering- oder
Allokationspfade sie konsumieren.

Event-Serialisierung verwendet nun einen längenbewussten JSON-Escaper an der
Event-Grenze. Valides UTF-8 bleibt erhalten; jedes fehlerhafte Byte wird zu
einem `\\u00XX`-JSON-Escape. Dies ist eine JSON-Sicherheits-Transformation,
keine Behauptung byteweiser Semantikerhaltung.

Für begrenzten Shutdown ist der Autorisierungsservice heapbesessen und enthält
eine begrenzte, vollständig besessene Kopie der Profilstruktur, ihrer
Textfelder und ihrer Original-URI-Headerliste. Laufen beide Waits ab, entlinkt
sich der letzte abgetrennte Worker und gibt Service/Runtime frei; kann
Mutex-Ownership nicht bewiesen werden, wird prozesslokaler State absichtlich
geleakt, statt ihn bei potentiell lebendem Zugriff freizugeben. Mapping-
Callbacks bleiben ausschließlich Code-Pointer.

## Aktuelle Erweiterung der nativen Connector-Grenzen

Der Follow-up-Review fand validierte Parent-eigene Lücken an nativen
Connector-Grenzen und nahm enge fail-closed Änderungen vor. Apache propagiert
native Engine-Fehler nun als Request-Fehler, akzeptiert nur exakten
libmodsecurity-Phasenerfolg (`== 1`), wendet vor dem Append das gemeinsame
Request-Body-Budget an und öffnet native Event-Dateien über einen no-follow-,
Regular-File- und privaten Descriptor-Vertrag. NGINX verlangt einen tatsächlich
vorhandenen nichtleeren Client-`Host`, propagiert Transaction-/Header-/Body-
Fehler, begrenzt In-Memory- und Temporary-File-Request-Bodies und weist die
native Phase-4-Event-Directive zurück, statt einen Pfad ohne gleichwertigen
sicheren Descriptor-Vertrag zu öffnen.

Der Apache-Request-Mapper weist nun ebenfalls fehlende oder leere empfangene
`Host`-Metadaten zurück, statt `r->hostname` einzusetzen. Der native
HAProxy-Mapper weist fehlenden oder leeren `Host` zurück, und das Binding
behandelt diesen Mapperfehler vor der Allokation einer libmodsecurity-
Transaktion als terminal. Der Legacy-CRS-Helper verlangt einen expliziten Host
und der SPOP-Notify-Handler trennt einen Request mit fehlenden Host-Metadaten
vor der Legacy- oder Produktionsverarbeitung.

HAProxy Binding akzeptiert ebenfalls nur exakten libmodsecurity-Phasenerfolg
(`== 1`) und erhält dabei den getrennten Regel-Lade-Rückgabevertrag. HAProxy
HTX zeichnet Header-Setup- und Response-Header-Engine-Fehler nun in einem
getrennten `fail_closed`-Zustand auf und gibt aus späteren Header- oder
Payload-Callbacks `-1` zurück; er behandelt eine fehlende Transaction nach
einem nicht deaktivierten Abort, fehlende Response-Header oder einen Append-
Fehler nicht mehr als Pass-through. Die SPOP-Diagnose-Runtime verwendet eine
monotone begrenzte Receive-Deadline, weist fehlerhafte oder überlaufende
Varints sowie nicht darstellbare Typed Strings zurück, validiert Header-Bytes
vor dem Transaction-Input und begrenzt Worker-/Konfigurationsoptionen, die
sonst nicht unterstützte Concurrent- oder Response-Body-Pfade erzeugen würden.

Envoy ext_proc weist nichtnumerische oder nicht-Loopback-Listener-
Konfiguration zurück, erzwingt 128 gleichzeitige Connections und 128
gleichzeitige RPC-Streams und weist Requests ohne `:authority` und `Host`
zurück. Die Traefik-Go-Middleware wählt bei ausgelassenem `engineMode` `uds`
und weist jeden anderen Modus einschließlich `passthrough` zurück, bevor ein
Allow-all-Engine-Pfad ausgewählt werden könnte. Die native C-UDS-Engine
begrenzt lebende abgetrennte Worker vor der Allokation auf 64 und
schließt überzählige Sockets, statt sie zu queueen. Der historische Wert Null
bleibt der Persistent-Service-Sentinel; positives `--max-connections` bleibt
auf kontrollierte One-shot-Läufe beschränkt.
Wenn ein nichtstandardmäßiger Header-Map-`Host` vorhanden ist, muss er
Singleton, Control-free und exakt gleich `request.Host` sein; eine Abweichung
oder ein Header-Splitting-Wert wird zurückgewiesen, bevor die Engine eine der
beiden Repräsentationen sieht.

Ein unabhängiger Final-Review fand eine Zwischenimplementierung, die den
Default-Null-Sentinel in eine Lebenszeitquote von 256 Connections änderte.
Weil die Go-Middleware pro Request eine UDS-Connection öffnet, war dies eine
bestätigte lokale Availability-/DoS-Regression. Der finale Code entfernt die
Default-Quote, behält aber Active-Worker- und Backlog-Grenzen bei. Lokale
258-Connection- und 64-Active-Worker-Saturation-/Recovery-Tests üben das
reparierte Verhalten aus.

## Finale Boundary-Abstimmung vom 2026-08-25

Der letzte Boundary-Pass ergänzt vier evidenzgestützte Records.
`FND-PARENT-0912` macht das Ergebnis des HAProxy-Mappers zur Voraussetzung für
den Engine-Eintritt: Ungültige Syntax, Header-Budgets, Authority-Kardinalität,
doppeltes Content-Length und Content-Length-/Transfer-Encoding-Mehrdeutigkeit
scheitern nun vor Raw-Request- oder Response-Headersinks. `FND-PARENT-0913`
macht den SPOP-Notification-Verbrauch exakt, validiert begrenzte
Header-/Varint-Eingaben und gibt dem Legacy-State-null-Receive-Pfad eine
2.000-ms-Deadline. `FND-PARENT-0914` begrenzt `max-transactions` auf
`1..65536`, setzt 4096 als Default und beweist die Cache-Allokationsgröße vor
`calloc`.

`FND-PARENT-0915` ist ein bestätigter Common-Concurrency-Defekt, nicht nur ein
statischer Kandidat: Pre-Fix-ThreadSanitizer beobachtete, wie der
SIGTERM-/SIGINT-Handler `authorization_stop` schrieb, während ein Detached
Worker es über seine I/O-Helfer las. Worker erben nun beim Erzeugen eine
blockierte SIGTERM-/SIGINT-Maske und besitzen keinen erreichbaren Lesezugriff
auf dieses Flag; Deadline- und Socket-Shutdown-Cancellation bleiben erhalten.
Der reparierte normale Timeout-/Admission-Smoke, das Common-Memory-Safety-
Target, der sechsteilige Authorization-Contract und derselbe TSan-Smoke
bestanden alle mit Exit-Code 0 und ohne TSan-Warnung. Dies ersetzt die frühere
Klassifikation des vollständigen Timeout-TSan als nicht schlüssig.

Das externe payload-sichere Evidenzmanifest der Aufgabe liegt unter
`/var/tmp/codex/ModSecurity-conector/runs/20260825T005347Z-connector-security-final-validation/manifest.json`.
Seine aktuelle fokussierte Python-Suite verzeichnet 103 bestandene Tests; der
später angepasste Common-Authorization-Contract bestand 6/6. Der eigenständige
SPOP-ASan/UBSan/Leak-Harness, HAProxy-C17-/Overlay-Controls, Apache-C17-Lint
und Traefik-Go-Race-, vet- und Formatchecks bestanden als separat aufbewahrte
fokussierte Evidenz.

`FND-CROSS-0011` bleibt blockiert und wird nicht als behoben dargestellt: Der
separat governte Framework-NGINX-Provisioner ruft direkt `tar -xf` auf und
umgeht den Shared Helper. Der direkte Pfad besitzt noch nicht den verlangten
begrenzten Member-/Pfad-/Link-/Typ-/Count-/Größen-/Target-Root-/Overwrite-
Preflight oder isolierte positive/negative Archivkontrollen. Es wurde kein
Archiv konstruiert oder extrahiert, weil der Benutzer das Framework-Repository
nicht explizit für Write-/Test-Arbeit ausgewählt hat.

## Update nach der Boundary-Abstimmung — 2026-08-25

Der letzte Parent-only-Source-to-Sink-Pass ergänzt sieben fixe, aber nicht als
Host-Runtime verifizierte Records. `FND-PARENT-0916` gibt dem öffentlichen
HAProxy-Binding und dem HTX-Borrowed-Payload-Pfad kumulative Request-/Response-
Byte-Budgets mit Subtraktionsform-Overflow-Checks vor dem libmodsecurity-
Body-Sink. `FND-PARENT-0917` weist ungültige Headernamen, Control Characters,
fehlerhaftes UTF-8 und zu große Gesamtheader im Envoy ext_proc vor dem rohen
CGo-Headersink zurück; die fail-closed-Regel ohne Authority bleibt erhalten.
`FND-PARENT-0918` weist response-tragende SPOP-Argumente in einer
`check-request`-Notification zurück, sodass ein Peer die Request-Verarbeitung
nicht als Response-Verarbeitung reklassifizieren kann.

`FND-PARENT-0919` lässt den optionalen Envoy-JSONL-Observer jeden absoluten
Vorfahren mit No-Follow-Deskriptoren durchlaufen und unsicheren finalen Typ,
Owner oder Mode vor jeder Mutation zurückweisen. `FND-PARENT-0920` wendet den
entsprechenden descriptor-backed Vorfahren-/Owner-/Typ-/Private-Mode-Vertrag
auf die Common-Runtime-Event-Datei an. `FND-PARENT-0921` lässt beide
kompilierten Apache-Connection-Phase-Hooks jeden Rückgabewert ungleich `1` vor
der normalen Request-Verarbeitung als internen Fehler behandeln.
`FND-PARENT-0922` wendet denselben sicheren Vorfahrenvertrag auf die native
Apache-Event-Datei an. Diese Records behaupten keinen Remote-Exploit, wenn die
Evidenz nur eine lokale Parser- oder Descriptor-Grenze belegt.

Der aktuelle Task-Worktree bestand die fokussierte 118-Test-Contract-Suite,
Apache C17, Common Memory Safety, den Common-Autorisierungs-
Timeout-/Admission-Smoke, Envoy-ext_proc- und Traefik-Native-Paket-Race-Tests
sowie Vet-/Formatchecks und den HAProxy-HTX-Overlay-Contract. Die
Validierungsquittung liegt unter
`/var/tmp/codex/ModSecurity-conector/runs/20260825T014358Z-final-focused-contract-rerun/evidence/validation-summary.md`
(SHA-256 `52ac0fecea6bf7e5e5657ba6cb8cf00bce34995e918c3c271cf76b0c887bc2c3`).
Das exakte HAProxy-C17-Target bleibt vor der Compilation durch
`nginx_pinned_provenance_ref_mismatch` blockiert; die Legacy-Common-Helper-
und SDK-Contracts bleiben an bestehenden CI-eigenen Erwartungen fehlgeschlagen
und wurden nicht geändert. Diese Evidenz ersetzt nicht die nicht verfügbare
native Zehn-Host-, HTTP/2/HTTP/3-, Reload-, Leak- oder vollständige
Sanitizer-Matrix.

## Finaler fokussierter Validierungsnachtrag — 2026-08-25

Die finale fokussierte Prüfung führt `FND-PARENT-0923` bis `FND-PARENT-0925`
als im Parent-Source- und Testbereich behoben, aber nicht als Host-Runtime-
verifiziert. Envoy ext_proc validiert den finalen Redirect-`location`-Wert
nun nochmals am Response-Header-Sink und weist ungültiges UTF-8, Controls,
Whitespace, CR/LF, NUL sowie überlange Werte vor der Header-Ausgabe zurück.
HAProxy SPOP erhält bei einer doppelten Request-ID die aktive Transaktion; die
Duplikatnachricht wird zurückgewiesen und kann die ursprüngliche Transaktion
weder ersetzen noch abschließen. Der Envoy-Phase-4-Harness verfolgt nun
akzeptierte Handler-Threads bis zu ihrem Abschluss vor dem Abbau des
temporären Roots und bewahrt den standardmäßigen HTTPS-Servertyp samt
TLS-Fixture-Semantik.

Die final beobachteten Validierungen waren: Envoy-Transport `19/19`; Envoy-Go
`-race`, `vet` und `gofmt`; SPOP-Reliability `14/14`; die fokussierte Parent-
Suite `104/104`; der HAProxy-HTX-Overlay-Contract; sowie `git diff --check`.
Dies sind lokale Source-, Harness- und Package-Checks. Die vollständige
Zehn-Host-Matrix, HTTP/2/HTTP/3, Reload, Leak- und vollständige
Sanitizer-Abdeckung bleiben unausgeführt; der Framework-NGINX-Archivpfad
bleibt unter `FND-CROSS-0011` blockiert. Kein Commit, Push, Pull Request oder
anderer Delivery-Schritt ist durch diesen Record autorisiert.

## Geänderte Dateien

- `common/src/config.c`, `common/src/rule_loader.c`, `common/src/rule_merge.c`,
  `common/src/directive_spec.c` und `common/runtime/msconnector_runtime.c` —
  gemeinsame Remote-Rule-Ablehnung, Runtime-Enforcement und sicheres
  Event-Öffnen.
- `common/src/headers.c` und `fuzz/common_http_headers_fuzz.c` — fail-closed
  Duplicate-Content-Length-Parsing und seine begrenzte Fuzzer-Kontrolle.
- `connectors/apache/src/msc_config.c` und
  `connectors/nginx/src/ngx_http_modsecurity_module.c` — direkte Host-
  Directive-Ablehnung vor nativer Remote-Konvertierung.
- `common/runtime/http_authorization_service.c` — Loopback-only-Listener,
  fail-closed-Validierung für doppelte/fehlende/leere/zu große `Host`-Werte vor
  dem Mapping, signal-sicheres Send und begrenztes Shutdown-Verhalten;
  heapbesessenes Deferred-Cleanup, ein begrenztes, vollständig besessenes
  Profil für einen ununterbrechlichen abgetrennten Worker sowie
  Serving-Thread-only-Shutdown-Flag-Ownership mit Worker-Signal-Masking.
- `common/src/event.c`, `common/include/msconnector/event.h` und
  `common/include/msconnector/integrity_event.h` — escaped/NULL-sichere Event-
  Metadaten, sichere Korrelationssemantik und Event-Sink-Invariante.
- `common/src/json_escape.c` und `common/include/msconnector/json_escape.h` —
  längenbewusste Erhaltung von validem UTF-8 und JSON-Encoding fehlerhafter
  Bytes.
- `common/include/msconnector/limits.h`, `common/src/resource_limits.c` und
  `common/src/config.c` — endliche Header-/Event-Limits plus eine harte
  10-MiB-Konfigurationsobergrenze für Request-, Response- und Phase-4-Bodies.
- `connectors/{apache,nginx}/README.md` und `.de.md` — Remote-Rule-Verhalten.
- `connectors/{apache,nginx,envoy,haproxy,lighttpd,traefik}/capabilities.json`
  — eine konsistente Remote-Rule-Capability-Aussage.
- `tests/test_remote_rules_disabled.py`,
  `tests/test_http_authorization_service_security_contract.py` und
  `tests/test_event_runtime_security_contract.py` — fokussierte Regression-
  Contracts.
- `tests/event_json_utf8_smoke.c`, `tests/test_resource_limits_hard_caps.c`
  und `tests/http_authorization_service_detached_worker_smoke.c` — fokussierte
  Controls für fehlerhaftes UTF-8, Caps, Missing-Host-Ablehnung vor Mapper-
  Eintritt und den Deferred-Worker-Lifecycle.
- `examples/common/common-connector-configuration.{md,de.md}`,
  `docs/{configuration,architecture}.{md,de.md}` sowie die Apache-/NGINX-
  README-Paare — dokumentierte endliche Limits, Phase-4-
  Konfigurationsobergrenze und die technisch durchgesetzte Remote-Rule-
  Ablehnungsrichtlinie.
- `connectors/apache/src/mod_security3.c`, `msc_filters.c` und
  `msc_apache_mapper.c` — fail-closed Engine-Return-Propagation einschließlich
  exaktem Connection- und Request-Phasenerfolg, begrenzter nativer Request-
  Body-Aufnahme, descriptor-backed vorfahrensicherem nativen Event-Öffnen und
  verpflichtendem Mapping des empfangenen Host.
- `connectors/nginx/src/ngx_http_modsecurity_{access,common,mapper,module}.c`
  und NGINX-README-/Capability-Records — verpflichtender Client-Host,
  Fehler-/Body-Limit-Propagation und fail-closed natives Phase-4-Event-
  Logging.
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`,
  `connectors/haproxy/src/haproxy_modsecurity_mapper.c`,
  `connectors/haproxy/src/haproxy_modsecurity_binding.c` und
  `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — fail-closed
  HTX-Setup-/Fehler-/Sequenzbehandlung einschließlich nicht abbildbarer
  disruptiver Entscheidungen und Request-EOS-Fehler, kumulativer begrenzter
  Borrowed-Payload-Accounting, exakter nativer
  Phasenerfolg, verpflichtende Authority vor der Transaktionsallokation,
  fail-closed Request-/Response-Mapper-Ergebnisse mit begrenztem/validiertem
  Header-Framing sowie begrenztes SPOP-Frame-/Header-/Liveness- und
  Transaktionscache-Parsing/-Allokation plus Notification-Phasenkonsistenz.
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go` und
  `internal/processor/{config,jsonl,processor}.go` — numerische Loopback-
  Konfiguration, endliche gRPC-Admission, Authority-/Header-Validierung und
  descriptor-backed private JSONL-Ausgabe.
- `connectors/envoy/ext_proc/internal/processor/{processor.go,processor_test.go}`
  — finale `location`-Validierung am Response-Header-Sink sowie Regressionen
  für ungültiges UTF-8, Controls, Whitespace und Größenüberschreitung.
- `connectors/envoy/harness/envoy_smoke_helper.py` und
  `tests/test_envoy_transport_hardening_contract.py` — Tracking akzeptierter
  Handler-Lebenszyklen bis zum deterministischen Phase-4-Cleanup bei Erhalt
  von HTTPS-Fixture-Typ und TLS-Verhalten.
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` und
  `tests/test_sonar_reliability_contract.py` — Zurückweisung doppelter
  SPOP-Request-IDs bei Erhalt der aktiven Transaktion und zugehöriger
  Regressionstest.
- `connectors/traefik/native_middleware/`,
  `connectors/traefik/src/traefik_engine_service.c` und zugehörige Traefik-
  Konfigurations-/README-/ORIGIN-Dateien — sicherer UDS-Default, endliche aktive
  Admission, kein Default-Lifetime-Shutdown, Authority-Validierung und
  Header-Map-Übereinstimmung vor der Engine-Erzeugung und portable
  Peer-Identity-Einschränkung.
- `common/src/generic_mapper.c` — erhält einen fehlenden Client-Hostname,
  statt einen Server-Endpunkt still als Request-Authority einzusetzen.
- `tests/test_{apache_connection_phase_contract,apache_native_security_contract,haproxy_binding_phase_contract,haproxy_header_validation_contract,haproxy_htx_filter_security_contract,native_host_fallback_contract,nginx_native_security_contract}.py`,
  Envoy-ext_proc-Go-Tests, Traefik-Go-/Native-Tests und bestehende fokussierte
  Common-/Apache-/SPOP-Contracts — task-eigene Regressionen für diese Grenzen,
  einschließlich Missing-Host-, Header-Framing-, Worker-Signal-Ownership- und
  HTX-Fail-Closed-Fällen.
- Dieses englisch/deutsche Change-Record-Paar.

Kein Framework-Source, MRTS-Source, Gitlink, Dependency, erzeugtes Runtime-
Artefakt oder CI/Governance-Datei ist Teil dieser Änderung.

## Ausgeführte Befehle

Der Platzhalter `<external-task-root>` bezeichnet das task-eigene Verzeichnis
unter `/var/tmp/codex/ModSecurity-conector/`; es liegt außerhalb des Checkouts.

### PASS

~~~text
rtk proxy python3 -B -m unittest -v tests.test_remote_rules_disabled tests.test_http_authorization_service_security_contract tests.test_event_runtime_security_contract
rtk proxy env BUILD_ROOT=<external-task-root>/http-timeout make check-http-authorization-service-timeout
rtk proxy env CC=clang ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror -fsanitize=address -fno-omit-frame-pointer' BUILD_ROOT=<external-task-root>/http-asan make check-http-authorization-service-timeout
rtk proxy env CC=clang UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror -fsanitize=undefined -fno-omit-frame-pointer' BUILD_ROOT=<external-task-root>/http-ubsan make check-http-authorization-service-timeout
rtk proxy env BUILD_ROOT=<external-task-root>/memory make check-common-memory-safety
rtk proxy env BUILD_ROOT=<external-task-root>/fuzz make check-common-http-header-fuzz
rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include -Icommon/runtime -fsyntax-only common/src/headers.c common/src/rule_merge.c common/src/event.c common/runtime/msconnector_runtime.c
rtk proxy make check-common-security-contract check-common-flow-integrity check-directive-parity
rtk proxy sh -c 'cc -std=c17 -Wall -Wextra -Werror -I. -Icommon/include tests/test_resource_limits_hard_caps.c common/src/resource_limits.c common/src/limits.c common/src/config.c common/src/body_policy.c common/src/block_statuses.c common/src/http_status.c -o <external-task-root>/resource-limits-hard-caps && <external-task-root>/resource-limits-hard-caps'
rtk proxy sh -c 'clang -std=c17 -Wall -Wextra -Werror -fsanitize=address,undefined -fno-omit-frame-pointer -I. -Icommon/include tests/test_resource_limits_hard_caps.c common/src/resource_limits.c common/src/limits.c common/src/config.c common/src/body_policy.c common/src/block_statuses.c common/src/http_status.c -o <external-task-root>/resource-limits-hard-caps-asan-ubsan && ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 <external-task-root>/resource-limits-hard-caps-asan-ubsan'
rtk proxy sh -c 'cc -std=c17 -Wall -Wextra -Werror -I. -Icommon/include tests/event_json_utf8_smoke.c common/src/*.c -o <external-task-root>/event-json-utf8-smoke && <external-task-root>/event-json-utf8-smoke | python3 -c "import json,sys; [json.loads(line) for line in sys.stdin if line.strip()]"'
rtk proxy sh -c 'clang -std=c17 -Wall -Wextra -Werror -pthread -fsanitize=thread -fno-omit-frame-pointer -I. -Icommon/include -Icommon/runtime tests/http_authorization_service_detached_worker_smoke.c common/runtime/http_authorization_service.c common/src/*.c -o <external-task-root>/http-auth-detached-worker-tsan && TSAN_OPTIONS=halt_on_error=1 <external-task-root>/http-auth-detached-worker-tsan'
~~~

Die fokussierte Python-Suite bestand 11 Tests. Der Loopback-
Timeout-/Admission-Smoke bestand normal, mit ASan samt Leak-Detection und mit
UBSan. Das Memory-Safety-Target bestand seinen normalen und optionalen
ASan/UBSan-Smoke. Der begrenzte libFuzzer-Lauf absolvierte 533086 Ausführungen
in 16 Sekunden ohne AddressSanitizer- oder UndefinedBehaviorSanitizer-
Diagnose. Der C17-Syntaxcheck und die aufgeführten Common-Contracts bestanden.
Der aktuelle Dokumentationslink-Check ist wegen des nicht verfügbaren/nicht
initialisierten Framework-Submoduls (17 Framework-Targets) blockiert; eine
manuelle Prüfung fand kein fehlendes Ziel in den geänderten Parent-Dokumenten.

Der zweite Re-Audit ergänzte einen normalen und ASan/UBSan-Hard-Cap-Smoke,
einen normalen und ASan/UBSan-Smoke für fehlerhaftes-UTF-8-JSONL mit strengem
Python-JSON-Parsing sowie einen kontrollierten Detached-Worker-Smoke. Der
Detached-Worker-Control bestand normal, mit ASan/UBSan samt Leak-Detection und
mit TSan ohne Diagnose. Sein TSan-Ergebnis ist getrennt vom bestehenden TSan-
Lauf des vollständigen HTTP-Timeout-Smokes, der nicht schlüssig bleibt. Ein
weiterer Header-Fuzzer-Lauf absolvierte 516409 Ausführungen in 16 Sekunden ohne
Sanitizer-/Crash-Diagnose; beide Fuzzerzählwerte bleiben als getrennte
historische lokale Läufe erhalten. Der Detached-Worker-Smoke gibt zudem
caller-besessenen Profiltext und die Original-Headerliste nach Rückkehr des
Service-Entrypoints frei, bevor er den blockierten Worker freigibt.

Der nachgezogene Host-Control bestand den Python-Autorisierungsvertrag mit
fünf Tests, einen strengen C17-Syntaxcheck und einen echten lokalen Loopback-
Smoke. Sowohl ein fehlender `Host` als auch ein 1024 Byte langer Host-Wert (die
feste Hostname-Puffergrenze) erhielten HTTP 400, bevor das Mapper-Flag des
Smokes oder das Fake-Runtime-Transaktionsflag gesetzt wurde; anschließend
erreichte ein Request mit gültigem `Host` weiterhin den absichtlich blockierten
Worker. Derselbe Smoke bestand mit ASan/UBSan samt Leak-Detection und mit TSan
ohne Diagnose. Der bestehende Timeout-/Admission-/Cancel-/Parallel-Smoke
bestand nach der Implementierungsänderung erneut.

### Aktueller nativer Boundary-PASS

~~~text
rtk proxy python3 -B -m unittest -v tests.test_remote_rules_disabled tests.test_http_authorization_service_security_contract tests.test_event_runtime_security_contract tests.test_haproxy_htx_filter_security_contract tests.test_haproxy_binding_phase_contract tests.test_sonar_reliability_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_traefik_native_local_plugin tests.test_apache_native_security_contract tests.test_generic_mapper_host_fallback_contract tests.test_native_host_fallback_contract
rtk proxy make -C connectors/haproxy check-htx-overlay
rtk proxy env APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/apache-c17-native-host-final make check-apache-c17-lint
rtk proxy make check-common-security-contract check-common-flow-integrity check-directive-parity
rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include -fsyntax-only common/src/generic_mapper.c
rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include -Iconnectors/haproxy/src -fsyntax-only connectors/haproxy/src/haproxy_modsecurity_mapper.c
rtk proxy env GOTOOLCHAIN=local go test -mod=readonly -run 'TestMiddlewareRejects(Invalid|Missing)AuthorityBeforeEngine' -count=1  # Traefik middleware
rtk proxy env GOTOOLCHAIN=local go test -mod=readonly -run 'TestMiddleware(RejectsConflictingHostHeaderBeforeEngine|RejectsInvalidHostHeaderBeforeEngine|AcceptsMatchingHostHeaderWithoutAuthorityDuplicate)' -count=1  # Traefik middleware
rtk proxy env GOTOOLCHAIN=local go test -race -mod=readonly ./...  # Traefik middleware
rtk proxy env GOTOOLCHAIN=local go vet ./...  # Traefik middleware
~~~

Der aktuelle fokussierte Python-Befehl bestand 96 Tests. Apache C17, der
HAProxy-Exact-Success-Binding-Contract und der HAProxy-HTX-Overlay-Contract
bestanden. Der gezielte Authority-Regressionstest der Traefik-Middleware,
`go test -race` und `go vet` bestanden. Die Common-Security-/Flow-/Directive-
Contracts sowie der strenge Common-Mapper-Syntaxcheck bestanden. Frühere
107-Test-, Envoy-, Memory-, Timeout- und Fuzzer-Runs bleiben separat
aufbewahrte historische Evidenz für ihren damaligen Scope.

Die aktuellen HTX-Source-Contracts zeigen, dass eine nicht unterstützte
disruptive Action oder ein Status sowie ein Fehler bei der Request-Body-
Finalisierung nun `fail_closed` setzen, die Transaktion abbrechen und einen
Fehler zurückgeben, statt in den Disabled-Passthrough zu wechseln. Die
Traefik-Middleware weist fehlenden oder fehlerhaften `request.Host` vor
`engine.Open` zurück; ihr legitimer Control mit gültiger Authority bleibt
akzeptiert. Der Common-Mapper verwandelt einen fehlenden Client-Hostname nicht
mehr in einen Server-Endpunkt. Dies sind Source-Contract- und lokale Paket-
Ergebnisse, kein Host-Fault-Injection-Nachweis.

Der Traefik-Header-Adapter weist nun auch einen Singleton `Header["Host"]`
zurück, der mit `request.Host` kollidiert oder Control Characters enthält,
bevor die Engine geöffnet wird; ein passender Singleton-Host bleibt ein
One-Entry-Normal-Control. Der fokussierte Drei-Fall-Go-Test, Paket-Race-Test,
vet und Formatcheck bestanden. Dies ist lokaler Adapternachweis, kein echter
Traefik-Host-Erreichbarkeitstest.

Der zusätzliche Native-Authority-Contract beweist, dass Apache fehlende oder
leere empfangene Host-Metadaten zurückweist; HAProxy sie zurückweist und vor
der Transaktionsallokation abbricht; der CRS-Helper einen expliziten Host
verlangt; und SPOP die Missing-Host-Nachricht vor der Request-Verarbeitung
trennt. Der positive CRS-Selftest verwendet weiterhin explizites synthetisches
`localhost`; es ist kein Runtime-Fallback mehr.

Der isolierte Traefik-Engine-Service-Build sowie der Protokoll-/Cleanup-
Runtime-Check bestanden normal, unter ASan/UBSan mit Leak-Detection und unter
TSan ohne Diagnose. Unabhängige lokale Clients prüften 258 sequenzielle
Connections ohne Default-Lifetime-Shutdown sowie das Schließen der 65.
gleichzeitigen Connection am 64-Worker-Cap mit anschließender erfolgreicher
Recovery.

### Erwartete Source-Abwesenheit

~~~text
rtk proxy rg -n 'msc_rules_add_remote|rule_backend\.add_remote' common connectors/apache connectors/nginx
~~~

Dieser Befehl endete mit `1`, dem erwarteten `rg`-No-Match-Ergebnis: In den
abgegrenzten Pfaden blieb kein produktiver Source-Sink zurück.

### Fehlgeschlagen / nicht schlüssig

~~~text
rtk proxy env BUILD_ROOT=<external-task-root>/helpers make check-common-helpers
rtk proxy env CC=clang TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror -fsanitize=thread -fno-omit-frame-pointer' BUILD_ROOT=<external-task-root>/http-tsan make check-http-authorization-service-timeout
rtk proxy timeout 30s .venv/bin/python ci/checks/documentation/check-bilingual-docs.py
rtk proxy make -C connectors/traefik test-engine-service
rtk proxy <HAProxy full binding self-test>
rtk proxy make check-haproxy-c17-lint
~~~

`check-common-helpers` kompilierte, scheiterte dann jedoch an seiner
bestehenden Assertion, dass ein vollständiges Remote-Rule-Paar validiert. Seine
Testimplementierung liegt unter `ci/`, das die aktuelle Anfrage ausdrücklich
ausschließt; keine Policy und kein Test wurden abgeschwächt. Die älteren
TSan-Wrapper-Versuche in diesem historischen Abschnitt besaßen keinen
terminalen Status und bleiben nicht schlüssig. Für die tatsächliche
Signal-/Worker-Grenze werden sie durch die spätere kontrollierte Pre-Fix-
Race-Bestätigung und den sauberen Post-Fix-TSan-Smoke der finalen Abstimmung
ersetzt. Auch der Bilingual-Checker lieferte innerhalb von 30 Sekunden über
den Command-Wrapper keinen terminalen Exit-Status oder Abschlussmarker;
erforderliche Change-Record-Überschriften und English/German-Parität wurden
manuell geprüft, das automatisierte Ergebnis ist aber nicht schlüssig statt
bestanden.

Das kombinierte Traefik-Target `test-engine-service` baut erfolgreich, aber
sein unveränderter Socket-Ownership-Selftest endet nach dem bestandenen
Protocol-Selftest mit einem Nonzero-Status. Direkte Runtime-Protokoll-/Cleanup-
Checks bestehen in normalen, ASan/UBSan- und TSan-Builds. `strace` ist in
dieser Umgebung nicht verfügbar; der unveränderte Selftest-Fehler bleibt daher
eine offene Validierungslücke und ist keine Evidence dafür, dass die
Socket-Ownership-Kontrolle unsicher ist.

Der optionale vollständige HAProxy-Binding-Selftest ist vor der Binding-
Compilation blockiert: Sein Probe referenziert das nicht verfügbare Symbol
`msc_get_rules_messages_rule_ids`. Die fokussierten Source-Contract- und HTX-
Overlay-Controls bestehen, aber dieser Blocker wird nicht als Host-Runtime-
Validierung dargestellt.

Das HAProxy-C17-Lint-Ziel bleibt ebenfalls vor der HAProxy-Compilation
blockiert: `prepare-runtime-components` meldet
`nginx_pinned_provenance_ref_mismatch` und stellt die erforderlichen Host-
Header/-Quellen nicht bereit. Dies ist eine externe Provisioning-Voraussetzung,
kein PASS-Ergebnis und keine Evidenz für einen Source-Fehler.

## Security-Auswirkung

Die ausgelieferten Parent-Kontrollen schließen Configuration-zu-Sink-Remote-
Rule-Laden, blockieren nicht authentifizierte öffentliche HTTP-
Autorisierungsbindungen, entfernen mehrdeutige Duplicate-Security-Header- und
Content-Length-Pfade, weisen stille Authorization-Host-Fallbacks zurück und
schützen finale Event-Datei sowie JSONL-Grenze. Bestehende
Request-/Header-/Body-Limits, Phase-Validierung, payloadfreies Event-JSONL,
lokale Rules und deterministisches Cleanup werden nicht gelockert.

Die aktuelle Erweiterung weist außerdem in HTX nicht durchsetzbare disruptive
Ergebnisse und Request-Body-Finalisierungsfehler zurück, statt sie als reine
Beobachtung zu behandeln, verlangt für Traefik Native eine Authority vor der
Engine-Allokation und verhindert, dass der gemeinsame Generic-Mapper einen
Server-Endpunkt als fehlenden Client-Host verwendet.

Dies ist Hardening auf Basis von Source-to-Sink-Evidence. Es ist keine
Behauptung, dass ein Remote-Deployment erreichbar war oder jedes HAProxy-,
HTTP/2-, HTTP/3-, UDS- oder host-spezifische Runtime-Verhalten dynamisch als
sicher bewiesen wurde.

## Runtime-Evidence

Der HTTP-Smoke verwendet lokale Loopback-Listener und eine fokussierte Fake-
Runtime. Er belegt begrenzte Admission-, Cancel-, Timeout-, Recovery- und
Shutdown-Pfade des gemeinsamen HTTP-Helfers. Der begrenzte Fuzzer deckt den
Common-HTTP-Header-Parser ab. Die aktuelle Erweiterung startet außerdem nur
einen isolierten nativen Traefik-UDS-Engine-Service mit lokalen gecachten
libmodsecurity-Artefakten; dies ist kein Traefik-Host-Runtime-Test. Kein
nativer Apache-, NGINX-, HAProxy-, Envoy-, Traefik-Host- oder lighttpd-
Hostprozess wurde gestartet, und es erfolgte kein externes Netzwerk oder
Dependency-Download.

## Bekannte Einschränkungen

- Der direkte NGINX-`tar`-Aufruf und der transitive gemeinsame Archivhelfer
  sind Framework-owned. Ihre fehlende Evidence für alle angeforderten Member-
  Count-, Byte-Size-, Link-, Device- und Traversal-Kontrollen bleibt außerhalb
  der Parent-only-Änderung.
- Envoy-ext_proc-Admission ist nun endlich und race-getestet, aber ein einzelnes
  zugelassenes `Recv` besitzt weiterhin keine unabhängige Application-Level-
  Idle-Deadline; die Limits begrenzen die Ressourcenadmission, beweisen aber
  nicht jeden Stalled-Client-Recovery-Pfad.
- Für vollständige native Host-, HTTP/2/HTTP/3-, Reload-,
  Cross-Connector-Parallel-, Leak- und ThreadSanitizer-Matrizen gibt es in
  diesem Checkout kein sicheres verfügbares Target.
- Es steht keine laufende HAProxy-Host-Fixture zur Verfügung, um eine nicht
  unterstützte disruptive Entscheidung oder einen Request-EOS-Fehler zu
  injizieren und nachzuweisen, dass das Backend nicht erreicht wird; der
  aufbewahrte HTX-Nachweis besteht daher aus Source-Contract plus Overlay-
  Validierung.
- Die native HAProxy-C17-Compilation ist vor der Compilation durch den
  gepinnten Provisioning-Provenance-Mismatch blockiert; der geänderte
  Standalone-Mapper kompiliert, aber ein vollständiger Host-Build und ein
  Missing-Host-Request wurden nicht ausgeführt.
- Es wurde keine Live-Traefik-UDS- oder lighttpd/Envoy-Generic-Mapper-
  Hostmatrix für eine bewusst fehlende Authority ausgeführt. Der Traefik-
  Pakettest beweist die Ablehnung vor dem Öffnen der Engine; andere Generic-
  Consumer behalten ihre expliziten lokalen Verträge.
- Der kontrollierte Deferred-Worker-Test verwendet eine Fake-Runtime und
  beweist weder einen echten libmodsecurity-Hang noch Host-Supervisor-
  Reload-Verhalten.
- Der UTF-8-Smoke deckt fehlerhaftes und valides UTF-8, eingebettetes NUL im
  begrenzten Escaper und repräsentative URI-/Protocol-Felder ab. Er ist keine
  vollständige native Host-Field-Matrix oder ein Beweis maximaler Escape-
  Expansion.
- Die Operator-seitige Traefik-ORIGIN- und Connector-Dokumentation beschreibt
  nun, dass in der Produktion ausschließlich UDS akzeptiert wird; die frühere
  Source-only-Formulierung zu `passthrough` wurde ohne Änderung von CI-eigenen
  Generatoren oder Workflow-Dateien entfernt.

## Verbleibende Risiken

Operatoren mit Remote Rules müssen auf Inline- oder lokale File-Rules
migrieren; eine Konfiguration mit einem der beiden Remote-Rule-Felder schlägt
deterministisch fehl, statt einen Fallback zu verwenden. Ein künftiges sicheres
Remote-Loading-Feature benötigt ein getrennt geprüftes HTTPS-/Origin-/
Integrity-/Timeout-/Size-/Atomic-Activation-Design.

NGINX-Temporary-Body-File-Type-/No-Follow-Enforcement unter einem feindlich
kontrollierten NGINX-Temporary-Pfad, Envoy-ext_proc-Stalled-Admission-Streams,
Traefik-Native-UDS-Peer-Identity und host-spezifisches Lifecycle-Verhalten
bleiben plausible Kandidaten bis native, isolierte Runtime-Evidence vorliegt.
Kein bestätigter High- oder Critical-Impact-Befund wird still als erledigt
behandelt: Das separate `FND-PARENT-0222` (P0/high) bleibt ein
Release-Blocker mit Source-Level-Korrektur, aber ohne echten
NGINX/libmodsecurity-Host-Proof. Es ist nicht Teil der staged Delivery dieses
Common-Follow-ups.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Framework-Archivtest und keine Framework-Source-Änderung wurden
ausgeführt, weil die aktuelle Autorisierung nur Parent-Änderungen erlaubt und
Framework-Write-/Test-Arbeit weiterhin eine explizite Repository-Auswahl
erfordert. Keine native Hostmatrix, kein externer Remote-Fetch, keine
Dependency-Installation und keine Hosted-CI-/Governance-Operation wurden
ausgeführt. Fokussierte lokale Targets verwenden Repository-Skripte unter
`ci/`, aber keine dieser Dateien wurde geändert. Die Legacy-`ci/`-Helper-
Assertion wird als fehlgeschlagen berichtet, nicht geändert. `check-doc-links`
ist wegen des nicht verfügbaren Framework-Submoduls blockiert und wird nicht
als bestandene Prüfung gezählt.

## Finaler Diff- und Review-Status

Der anfängliche scoped Parent-Commit ist
`4fa010412bfc7510da4ca787d9d923b9e8cad018`; der Delivery-Status-
Dokumentationscommit ist `7367187de072a86cfb5314740f8e47870c530e39`. Das hier
beschriebene Common-Re-Audit-Follow-up ist lokal als
`16a4a06fbf1e1ed20171bc29d31ce3e8476aa3db` committed, gefolgt vom engen Host-
Fallback-Fix `1de8071aa92cc72cadcc90a0e49f39e27e9ceba6`. Sein unabhängiger,
versiegelter Security-Diff-Review meldet im Bereich
`6c75b136..1de8071aa92cc72cadcc90a0e49f39e27e9ceba6` null berichtsfähige
Befunde; die partielle Coverage ist ausdrücklich auf die nicht verfügbare
native Hostmatrix begrenzt. `CAND-AUTH-HOST-001` ist als lokaler Record
`FND-PARENT-0900` erledigt: fehlende, leere oder übergroße Host-Werte wählen
nicht mehr die Listener-Adresse, und der verstärkte lokale Smoke beobachtet die
Ablehnung fehlender und grenzgroßer Host-Werte vor Mapper- oder Fake-Runtime-
Eintritt. Die aktuelle Native-Boundary-Erweiterung einschließlich
`FND-PARENT-0912` bis `FND-PARENT-0922` bleibt bis zu einem frischen finalen
Scoped-Security-Diff-Review uncommitted; keine ältere Null-Befund-Aussage wird
darauf fortgeschrieben. `FND-CROSS-0011` erfasst den separat governten,
blockierten Framework-NGINX-Archivpfad. Die generierte Traefik-Default-
Dokumentationsdrift wird separat verfolgt, weil ihr Generator im
ausgeschlossenen CI-Scope liegt. Remote-Veröffentlichung, Commit und
PR-Erstellung warten auf eine aktuelle explizite Autorisierung des Benutzers.
Es würden ausschließlich exakt task-eigene Parent-Dateien gestaged.
Kein Merge ist autorisiert oder behauptet.

## Endpoint- und NGINX-Post-Fix-Abgleich — 2026-08-25

`FND-PARENT-0926` und `FND-PARENT-0927` sind lokale Parent-Findings mit dem
Status `fixed`, jedoch nicht als Host-Runtime verifiziert oder geschlossen. Der
erste entfernt die Common/HAProxy-Praxis, fehlende Endpoint-Metadaten vor der
ModSecurity-Connection-Phase zu erfinden. Common verlangt nun begrenzte
Client- und Server-Endpoints; der HAProxy-HTX-Filter leitet sie aus dem
aktiven Frontend-Stream ab oder schlägt fail-closed fehl und bewahrt einen
gültigen UNIX-Endpoint, statt ihn durch eine erfundene IP oder einen nominalen
Port zu ersetzen. Der zweite lässt einen NGINX-Common-Mapper-Fehler mit
`NGX_HTTP_BAD_REQUEST` zurückkehren, bevor Hostname-, Connection-, URI- oder
rohe Request-Header-Verarbeitung stattfindet.

Der fokussierte Post-Fix-Befehl für HTX-, Endpoint-, HAProxy-Header- und
NGINX-Contracts bestand 31 Tests. `make -C connectors/haproxy
check-htx-overlay` und `git diff --check` bestanden ebenfalls. Ein isolierter
HAProxy-3.2.22-Overlay-Build kompilierte und linkte den finalen
Endpoint-Capture-Source. `make check-nginx-c17` war vor der Compilation
blockiert, weil die erforderlichen NGINX-Headers/-Sources nicht verfügbar
sind; dies wird nicht als bestandener nativer NGINX-Build erfasst.

Die gemeinsame Remote-Rule-Policy bleibt die deterministische Policy A:
nichtleere `rules_remote_key` oder `rules_remote_url` werden vor einem Fetch
abgewiesen. Event-Korrelation bleibt als prozesslokale, nicht kryptographische
Korrelation dokumentiert, nicht als manipulationssicherer Audit-Mechanismus.
Die Framework-ownede direkte NGINX-Archivextraktion bleibt außerhalb des
Scopes; daher wurde kein Archiv erstellt oder extrahiert und keine
Member-Validierung behauptet.

Ein frischer lokaler Post-Fix-Security-Diff-Review des resultierenden Content-
Snapshots meldete null verbleibende berichtsfähige Findings bei partieller
Abdeckung. Die kanonischen lokalen Scan-Artefakte sind Task-Completion-
Evidence statt einer versionierten Record-Abhängigkeit, sodass dieser Change
Record keinen selbstreferenziellen Snapshot-Loop erzeugt. Die unvollständige
aktuelle Host-/Protocol-/Reload-/Sanitizer-/Leak-Matrix, der Stock-lighttpd-
Build und zurückgestellte Source-Kandidaten bleiben Einschränkungen. Durch
diesen Abgleich wurden keine Workflow-, Governance-, Framework-, MRTS-,
Commit-, Push-, Pull-Request- oder Merge-Aktionen ausgeführt.

## Finaler Boundary-Abgleich — 2026-08-25

Der finale Parent-only-Pass ergänzte vier enge, evidenzbasierte Reparaturen.
HAProxy SPOP weist nun nicht terminierte/überbreite Varints und Typed-
`uint32`-Verengung ab (`FND-PARENT-0932`). Traefik Native UDS weist fehlerhafte
HTTP-Feldnamen und Control-Byte-Werte vor dem Common-Mapping ab
(`FND-PARENT-0934`). Envoy ext_proc serialisiert JSONL-Dateistatus von
`Record`/`Close` und weist Millisekunden-Timeouts ab, die nicht in
`time.Duration` passen (`FND-PARENT-0935` und `FND-PARENT-0936`). NGINX-native
Request- und Response-Headersenken verwenden nun die vorhandenen gemeinsamen
Limits für Anzahl, Namen, Werte und aggregierte Bytes vor libmodsecurity
(`FND-PARENT-0937`). Dies sind lokale `fixed` Findings, keine Behauptungen über
einen Delivery-Head oder eine Native-Host-Verifikation.

Die fokussierte Validierung bestand: die vollständige ext_proc-Go-Race-Suite
und `go vet`; die Native-Traefik-Paket-Race-Suite und `go vet`; C17
`-Wall -Wextra -Werror`-Syntaxvalidierung für den UDS-Service; NGINX-
Header-Contracts (10 Tests); die kombinierte lokale 137-Test-
Security-Regression; die Common-Security-/Flow-/Adapter-/Directive-Contracts;
und `make -C connectors/haproxy check-htx-overlay`. `git diff --check`
bestand. Native NGINX-Kompilierung bleibt durch fehlende Header/Source blockiert,
und der vollständig gelinkte Traefik-UDS-Selftest durch ungelöste lokale
`libxml2`-Symbole; keines davon wird als bestandener Native-Host-Test gezählt.

Der finale Source-Review erfasst außerdem `FND-PARENT-0938` als `deferred`
Kandidaten, nicht als bestätigte Schwachstelle: Sendet ein HAProxy-Upstream
finale Response-Header vor Request-EOS, enthält der Source einen möglichen Pfad,
der später die normale Response-Phase-3/4-Inspektion deaktiviert. Payload-vor-
Header- und disruptive Request-Body-Zweige sind fail-closed. Ein gepinntes
HAProxy-3.2.22-Fixture für Partial-Request/Early-Response muss Callback- und
Forwarding-Reihenfolge belegen, bevor Remediation oder Bypass behauptet werden.

Remote Rules bleiben die einheitliche Policy A: nichtleere Remote-Felder werden
vor einem Fetch abgewiesen; daher wird keine Origin-, Secret-Weiterleitungs-,
Partial-Download- oder Atomic-Activation-Behauptung gemacht. Der Event-Hash
bleibt nur als lokale, nicht kryptographische Korrelation dokumentiert. Die
Framework-ownede direkte NGINX-Archivextraktion bleibt außerhalb dieser
Parent-only-Autorität; kein Archiv wurde erzeugt oder extrahiert und keine
Member-Validierung behauptet. CI-/Governance-Dateien bleiben unverändert.
Vollständige aktuelle H1/H2/H3-, Reload-, Leak-, Sanitizer-, Stock-lighttpd-
und Zehn-Host-Runtime-Evidenz bleibt unvollständig.

## Aktuelle Revalidierung der Native-Traefik-UDS-Deadline — 2026-08-25

`FND-PARENT-0242` ist im aktuellen Task-Worktree behoben und nicht nur in
historischer, ungemergter Evidenz. Die Native-Traefik-UDS-Antwortframe-Senke
nutzt eine einzelne monotone Deadline, begrenztes `poll(POLLOUT)` und
nichtblockierende Writes; der Ablauf beendet nur den nicht lesenden Peer und
gibt dessen Worker-Slot frei. Die versionierte, begrenzte Regression hält 64
nicht lesende UDS-Peers und belegt danach, dass ein nachfolgender lesender Peer
nach Ablauf der Deadline fertig wird. Der C17-Syntaxcheck, der Shell-Check,
die 133-Test-Parent-Vertragssuite, das native Service-Target und dasselbe
native Service-Target mit Clang ASan/UBSan samt Leak-Erkennung bestanden. Dies
sind lokale Connector-/Service-Kontrollen, kein Traefik-Hostruntime-,
ThreadSanitizer- oder unabhängiger File-Descriptor-Leak-Nachweis.

Die Dokumentation wurde auf die Source-Policy abgeglichen: Native NGINX-
`modsecurity_phase4_log` ist registriert, schlägt aber fail-closed fehl, weil
es den Common-Event-Dateideskriptorvertrag nicht erfüllen kann; aktive Beispiele
und das Smoke-Template stellen es nicht länger als nutzbar dar. Apache-/NGINX-/
lighttpd-Referenzen beschreiben nun die einheitliche Remote-Rule-Policy A, bei
der nichtleere Remote-Felder vor Loader- oder Netzwerkaktionen abgewiesen
werden. Die Native-Traefik-Dokumentation nennt jetzt `uds` als einzigen
akzeptierten Default/Modus. `git diff --check` sowie die fokussierten
NGINX-/Traefik-Verträge bestanden nach diesem Abgleich.

Die vollständige Zehn-Connector-Host-/Protokoll-/Reload-/Concurrency-Matrix
bleibt wegen der fehlenden Framework-Runtime und Host-Voraussetzungen blockiert.
Insbesondere wurde der Framework-ownede direkte NGINX-Archivextraktionspfad
(`FND-CROSS-0011`) weder geändert noch ausgeführt; der zurückgestellte HTX-
Early-Response-Kandidat (`FND-PARENT-0938`) bleibt weder bestätigt noch
behoben. Diese lokale Revalidierung ändert keine Delivery-Autorisierung und
führt keine Delivery-Aktion aus.

## Aktuelles lokales Verifikationsergebnis — 2026-08-25

Die Go-Pakete von Envoy ext_proc und Traefik Native bestanden `go test -race`
und `go vet` mit vom Netzwerk deaktivierter Modulauflösung. Der Common-
Memory-Safety-Smoke bestand, ebenso der Common-HTTP-Autorisierungs-
Timeout-/Admission-Smoke mit Clang ASan/UBSan samt Leak-Erkennung und Clang
TSan. Seine absichtlichen Controls für Fehlformat, Timeout, Überlast,
abrupten Disconnect und blockierten Peer gaben erwartete Fail-closed-Meldungen
ohne Sanitizer-Diagnostik aus.

`check-common-security-contract`, `check-common-flow-integrity`,
`check-adapter-contracts` und `check-directive-parity` bestanden. Der separate
`check-common-sdk-contract` bleibt fehlgeschlagen, weil seine bestehende
statische Policy das server-spezifische Token `envoy` in
`common/include/msconnector/limits.h` ohne Nicht-Integrations-Kontext ablehnt.
Dieser Checker/diese Policy wird im Parent-Connector-Härtungsscope nicht
geändert; der Fehler wird dokumentiert statt maskiert.

## NGINX-Phase-4-Content-Type-Konfigurationsgrenze — 2026-08-25

`FND-PARENT-0940` ist ein lokaler `fixed`-Security-Hardening-Record. Der
native `modsecurity_phase4_content_types_file`-Loader vertraute zuvor einer
pathname-`stat()`-Größe vor der Allokation und öffnete den Pfad erst danach. Er
öffnet jetzt mit `NGX_FILE_NONBLOCK`, prüft den geöffneten Deskriptor mit
`ngx_fd_info`, verlangt eine reguläre Datei, erzwingt vor der Pool-Allokation
ein 64-KiB-Limit und weist einen verkürzten Read ab. Dies schließt den
source-seitigen unbeschränkten Allokations- und nichtregulären-Datei-Read-Pfad;
es wird keine Remote-Request-Schwachstelle behauptet.

Die fokussierte NGINX-Contract-/Konfigurationssuite bestand 9 Tests, und das
geänderte Modul kompilierte mit den konfigurierten NGINX-1.31.4-Host-Headers
und `-Werror`. Dies ersetzt nur die frühere Aussage „Headers/Source nicht
verfügbar“ für diese isolierte C-Kompilierung. Eine `nginx -t`-Fixture im
exakten Worktree für begrenzte reguläre Datei, FIFO, Verzeichnis, übergroße
Datei und parallelen Ersatz war nicht verfügbar; das Finding bleibt daher
`fixed`, nicht `verified` oder geschlossen. Es wurden keine CI-/Governance-,
Framework-, MRTS-, Commit-, Push-, Pull-Request- oder Merge-Aktionen ausgeführt.

Ein plattformübergreifender Source-Review ergänzte einen expliziten Win32-
Fail-closed-Zweig: Win32-NGINX stellt weder die hier benötigte POSIX-Regular-
File-Unterscheidung noch ein nichtblockierendes Dateiöffnungsflag bereit; diese
optionale lokale Dateidirektive wird dort daher abgewiesen, statt einen
schwächeren Special-File-Vertrag vorzutäuschen. Die POSIX-Kompilierung und der
statische Contract bleiben die tatsächlich ausgeführte Evidenz; es wird kein
Win32-Build-/Runtime-Nachweis behauptet.
## Envoy-ext_proc-prozessweite Aktivstream-Eingrenzung — 2026-08-25

`FND-PARENT-0943` erfasst eine lokale `fixed`-, nicht `verified`-Envoy-ext_proc-
Remediation. Die aufbewahrte historische Vier-Stream-Idle-Beobachtung belegte
Ressourcenretention über `engine_timeout_ms=150` hinaus; der Source-Review
bestätigte, dass `grpc.MaxConcurrentStreams(128)` pro Transport gilt. Der Dienst
erwirbt jetzt einen nichtblockierenden prozessweiten Slot vor
`streamState`-Konstruktion oder `TransactionOpener.Open`, liefert bei Sättigung
gRPC-`ResourceExhausted` und deferiert für jeden zugelassenen Normal-, EOF-,
Cancel- oder Processor-Error-Exit genau eine Freigabe. Die gRPC-Transport-
Einstellung verwendet denselben `DefaultMaxActiveStreams`-Konstantenwert.

Der aktuelle Task-Worktree bestand `go test -count=1 ./...`, `go test -count=1
-race ./...`, `go vet ./...` sowie die 19-Test-Auswahl
`tests.test_envoy_transport_hardening_contract`; der aufbewahrte payload-freie
Nachweis ist
`.codex/runs/20260825T122012Z-envoy-active-stream-capacity/evidence/validation.md`
mit SHA-256
`b246d933156ce602f928b5f81fc0078ffe2c28e586db72aafaaac72951197bd2`.
Die Capacity-one-Regression belegt, dass ein überzähliger Stream vor dem
Öffnen einer zweiten Transaktion abgewiesen wird und ein legitimer Stream nach
EOF wieder zugelassen wird.

Die Gesamtgrenze wird bewusst nicht als Idle-Deadline dokumentiert: Ein
zugelassener gültiger Stream kann weiter auf eine Envoy-Nachricht, EOF oder
Kontext-Cancel warten. Es werden kein verlinkter Common-/libmodsecurity- und
realer-Envoy-Multi-Transport-Sättigungs-, Reload-under-load-, Leak/Descriptor-,
exakter Delivery-Head-, Commit-, Push-, Pull-Request- oder Merge-Ergebnis
behauptet.

## Gemeinsame private Event-Dateideskriptor-Parität für Common und Apache — 2026-08-25

`FND-PARENT-0223` bleibt lokal `fixed`. Seine zuvor äquivalenten Common-
Runtime- und Apache-Pfadläufe sind jetzt eine Common-API:
`msconnector_open_private_event_file`. Auf unterstützten POSIX-Zielen durchläuft
sie jede konfigurierte Komponente mit `openat` und
`O_DIRECTORY|O_NOFOLLOW`, öffnet den finalen Sink mit
`O_NOFOLLOW|O_APPEND|O_CREAT|O_NONBLOCK`, weist ein nichtreguläres oder einem
anderen User gehörendes finales Objekt sowie ein gruppen-/welt-schreibbares
finales Parent-Verzeichnis ab, repariert eine akzeptierte vorhandene Datei auf
`0600` und erhält Close-on-Exec, wenn `O_CLOEXEC` fehlt. Common Runtime wandelt
den geprüften Descriptor in sein `FILE *` um; Apache übergibt ihn erst nach der
Common-Prüfung an APR.

Die begrenzte synthetische Regression bestand eine private reguläre Datei,
Modusreparatur einer vorhandenen Datei, Close-on-Exec, finale und Zwischen-
Symlinks, FIFO, Verzeichnis, Traversal und ein gruppenschreibbares Parent-
Verzeichnis im Normalmodus sowie unter Clang ASan/UBSan mit Leak-Erkennung.
Fokussierte Common-/Apache-/NGINX-Source-Contracts (16 Tests), C17-Syntaxchecks
für Common Runtime/Apache, der UTF-8-JSONL-Smoke und `git diff --check`
bestanden. Die native NGINX-Phase4-Dateidirektive bleibt vor der
Deskriptorerstellung deaktiviert: Ein Vorschlag zu ihrer Reaktivierung wurde
nicht umgesetzt, weil ihr geerbter Descriptor-/Reload-Lebenszyklus eine
separat autorisierungspflichtige Verhaltensänderung ist. Es werden keine
NGINX-Hostruntime, Apache-Hostruntime, Windows-Build, CI-/Governance-Datei,
Framework-/MRTS-Datei oder Delivery-Aktion behauptet.

## Delivery-Vorbereitung — 2026-08-25

Der aktuelle Benutzer hat für diesen bestehenden task-eigenen Branch
ausdrücklich einen Parent-Commit, Push und einen Draft-PR autorisiert. Die
Aufgabe autorisiert keinen Merge, keinen Default-Branch-Push, kein
History-Rewrite, keine Framework-/MRTS-Änderung, kein Gitlink-Update und keine
CI-/Governance-Änderung. Der Branch und jeder PR-Head bleiben an das
verifizierte `origin`-Ziel, den exakten SHA-Readback und die regulären
GitHub-Checks gebunden. Tatsächliche PR-Nummer, URL, Branch-SHA, Check-Status
und Review-Status werden erst nach Beobachtung im PR und in der
Task-Delivery-Evidenz erfasst; dieser Change Record behauptet sie nicht vorab.

## PR-#345-Sonar- und Workflow-Remediation — 2026-09-03

Der Task-Branch wurde vor dieser Remediation mit dem damaligen aktuellen
`origin/master` forward-gemergt; er erhält diese Master-Integration und
schreibt keine Historie um. Diese Erweiterung behebt aktuelle task-eigene
Sonar- und Workflow-Rückmeldungen ausschließlich durch Source-, Test- und
Dokumentationsänderungen. Sie verändert weder `.github/workflows`,
Branch-Protection, Rulesets, Required Checks, Sonar-Regeln, Quality-Gate-
Konfiguration, Exclusions, Suppressions noch Coverage-Schwellen.

Zwei unabhängig reproduzierte HAProxy-SPOE/SPOP-Pfade sind korrigiert.
Erstens werden legitime typisierte IPv4-/IPv6-`src`-/`dst`-Metadaten vor dem
Common-Mapping begrenzt, typgeprüft und kanonisch formatiert; nicht
unterstützte, verkürzte und nachlaufende Formen bleiben abgewiesen. Zweitens
sind fehlende erforderliche Endpunkte jetzt ein synchroner Zulassungsfehler
vor Owner-Task-Allokation oder Queueing. Er liefert daher bei
`fail-mode=open` und `closed` ein disruptives `deny`/503- und
`blocked=true`-ACK; die entsprechende Worker-Prüfung bleibt als Defense in
Depth erhalten. Es wurde kein Loopback-, Host- oder Endpoint-Fallback ergänzt.
Diese Befunde sind als FND-PARENT-1020 und FND-PARENT-1021 getrennt statt als
doppelte Findings erfasst.

Der Common-Remote-Rule-Helper prüft nun die bestehende einheitliche Policy A
korrekt: Jede nichtleere Remote-Konfiguration wird vor Mutation oder einem
netzwerkfähigen Sink abgewiesen. Änderungen an Common-Event-JSONL/Event-Datei,
Apache, NGINX, HAProxy-Binding/Mapper/HTX, Envoy ext_proc und Traefik Native
reduzieren Sonar-Komplexität oder Duplikate, ohne ihre Sicherheitsverträge zu
verändern. Refactor-sensitive HAProxy- und HTTP-Worker-Vertragstests wurden
erst nach Source-to-Sink-Review, der Mapper-, FIN-, Host-, Allokations-, Body-
und Fail-Closed-Reihenfolgen bestätigte, auf die neuen Helfergrenzen verlegt.
Das doppelte deutsche Traefik-Native-README wurde entfernt; sein Inhalt bleibt
mit dem englischen README abgestimmt.

Lokale Validierung bestanden: Common-C17-Helper, Security-/Flow-/Adapter- und
HTTP-Timeout-/Admission-/Cancel-Checks; der Detached-Worker-C17-,
ASan/UBSan-mit-Leak-Erkennung- und TSan-Smoke; Private-Event-C17-,
ASan/UBSan-, GCC-Analyzer- und Valgrind-Checks; Apache-C17;
Apache-/NGINX-/HTX- und HAProxy-Verträge; der HAProxy-SPOP-Protokoll-Self-Test;
sowie Envoy-ext_proc- und Traefik-Native-Format-, Vet-, Test- und Go-Race-
Checks. Die exakte gehostete HAProxy-CRS/no-MRTS-Kontrolle, der native
NGINX-Hostbuild/-Runtime und die vollständige H1/H2/H3-/Reload-Matrix bleiben
wegen nicht verfügbarer Framework-/Host-Artefakte blockiert und werden nicht
als bestanden dargestellt. Das Ergebnis der exakten PR-SHA-GitHub-Actions und
von SonarQube Cloud wird erst nach Delivery separat verifiziert; dieser Record
behauptet es nicht vorab.
