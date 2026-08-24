# Change Record

**Sprache:** [English](CR-20260824-connector-security-invariants.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260824-connector-security-invariants |
| Datum (UTC) | 2026-08-24 |
| Basis-Revision | a6b4ced4876a19666f7c7203ed9e719674c69ec1 |
| Repository-Grenze | Nur Parent; Framework, MRTS, Gitlink, CI und Governance unverändert |
| Delivery-Autorität | Nur lokaler Parent-Commit; Remote-Push und Draft-PR warten auf neue explizite Autorisierung des aktuellen Benutzers; kein Merge |

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
Repository. Der aktuelle Benutzer begrenzte die Implementierung auf Parent-
Fixes, daher wird dieser Pfad als Out-of-Scope-Remediation-Abhängigkeit
berichtet und weder hier gepatcht noch als sicher extrahiert dargestellt.

## Akzeptanzkriterien

- Jeder geprüfte Parent-Remote-Rule-Einstiegspunkt lehnt vollständige und
  unvollständige Remote-Rule-Konfiguration vor einem netzwerkfähigen Sink ab.
- Apache, NGINX und Common Runtime behalten keinen produktiven
  `msc_rules_add_remote`-Pfad; alle Connector-Capability-Records beschreiben
  dieselbe Policy.
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
  heapbesessenes Deferred-Cleanup und ein begrenztes, vollständig besessenes
  Profil für einen ununterbrechlichen abgetrennten Worker.
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
- `examples/common/common-connector-configuration.{md,de.md}` sowie die
  Apache-/NGINX-README-Paare — dokumentierte endliche Limits und Phase-4-
  Konfigurationsobergrenze.
- Dieses englisch/deutsche Change-Record-Paar und die gepaarten Archivindex-
  Einträge.

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
rtk proxy env BUILD_ROOT=<external-task-root>/docs make check-doc-links
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
Diagnose. Der C17-Syntaxcheck, die aufgeführten Common-Contracts und
Repository-Path-/Dokumentationslink-Checks bestanden.

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
~~~

`check-common-helpers` kompilierte, scheiterte dann jedoch an seiner
bestehenden Assertion, dass ein vollständiges Remote-Rule-Paar validiert. Seine
Testimplementierung liegt unter `ci/`, das die aktuelle Anfrage ausdrücklich
ausschließt; keine Policy und kein Test wurden abgeschwächt. Das TSan-Binary
wurde gebaut und übte Loopback-Fälle aus, aber der Command-Wrapper lieferte in
zwei Versuchen keinen terminalen Exit-Status oder Abschlussmarker. Es ist nicht
schlüssig, nicht bestanden. Auch der Bilingual-Checker lieferte innerhalb von
30 Sekunden über den Command-Wrapper keinen terminalen Exit-Status oder
Abschlussmarker; erforderliche Change-Record-Überschriften und English/German-
Parität wurden manuell geprüft, das automatisierte Ergebnis ist aber nicht
schlüssig statt bestanden.

## Security-Auswirkung

Die ausgelieferten Parent-Kontrollen schließen Configuration-zu-Sink-Remote-
Rule-Laden, blockieren nicht authentifizierte öffentliche HTTP-
Autorisierungsbindungen, entfernen mehrdeutige Duplicate-Security-Header- und
Content-Length-Pfade, weisen stille Authorization-Host-Fallbacks zurück und
schützen finale Event-Datei sowie JSONL-Grenze. Bestehende
Request-/Header-/Body-Limits, Phase-Validierung, payloadfreies Event-JSONL,
lokale Rules und deterministisches Cleanup werden nicht gelockert.

Dies ist Hardening auf Basis von Source-to-Sink-Evidence. Es ist keine
Behauptung, dass ein Remote-Deployment erreichbar war oder jedes HAProxy-,
HTTP/2-, HTTP/3-, UDS- oder host-spezifische Runtime-Verhalten dynamisch als
sicher bewiesen wurde.

## Runtime-Evidence

Der HTTP-Smoke verwendet lokale Loopback-Listener und eine fokussierte Fake-
Runtime. Er belegt begrenzte Admission-, Cancel-, Timeout-, Recovery- und
Shutdown-Pfade des gemeinsamen HTTP-Helfers. Der begrenzte Fuzzer deckt den
Common-HTTP-Header-Parser ab. Kein nativer Apache-, NGINX-, HAProxy-, Envoy-,
Traefik- oder lighttpd-Hostprozess wurde gestartet, und es erfolgte kein
externes Netzwerk oder Dependency-Download.

## Bekannte Einschränkungen

- Der direkte NGINX-`tar`-Aufruf und der transitive gemeinsame Archivhelfer
  sind Framework-owned. Ihre fehlende Evidence für alle angeforderten Member-
  Count-, Byte-Size-, Link-, Device- und Traversal-Kontrollen bleibt außerhalb
  der Parent-only-Änderung.
- Eine gleichzeitig geänderte Envoy-ext_proc-Idle-Timeout-/Admission-
  Implementierung bleibt unstaged. Ihr fokussierter Go-Race-Lauf scheitert an
  `TestStreamIdleTimeoutCleansUpAndAllowsFollowUpStream`; sie wird dieser
  Änderung weder zugeschrieben noch von ihr ausgeliefert.
- Für vollständige native Host-, HTTP/2/HTTP/3-, Reload-,
  Cross-Connector-Parallel-, Leak- und ThreadSanitizer-Matrizen gibt es in
  diesem Checkout kein sicheres verfügbares Target.
- Der kontrollierte Deferred-Worker-Test verwendet eine Fake-Runtime und
  beweist weder einen echten libmodsecurity-Hang noch Host-Supervisor-
  Reload-Verhalten.
- Der UTF-8-Smoke deckt fehlerhaftes und valides UTF-8, eingebettetes NUL im
  begrenzten Escaper und repräsentative URI-/Protocol-Felder ab. Er ist keine
  vollständige native Host-Field-Matrix oder ein Beweis maximaler Escape-
  Expansion.

## Verbleibende Risiken

Operatoren mit Remote Rules müssen auf Inline- oder lokale File-Rules
migrieren; eine Konfiguration mit einem der beiden Remote-Rule-Felder schlägt
deterministisch fehl, statt einen Fallback zu verwenden. Ein künftiges sicheres
Remote-Loading-Feature benötigt ein getrennt geprüftes HTTPS-/Origin-/
Integrity-/Timeout-/Size-/Atomic-Activation-Design.

HAProxy-HTX-Late-Response-Inspection, SPOP-Framing-/Cache-/Timeout-Verhalten,
Traefik-Native-UDS-Peer-Identity und host-spezifisches Lifecycle-Verhalten
bleiben plausible Kandidaten bis native, isolierte Runtime-Evidence vorliegt.
Kein bestätigter High- oder Critical-Impact-Befund wird still als erledigt
behandelt: Das separate `FND-PARENT-0222`-NGINX-P0/High-P2/P3-Finding bleibt
ein Release-Blocker mit Source-Level-Korrektur, aber ohne echten
NGINX/libmodsecurity-Host-Proof. Es ist nicht Teil der staged Delivery dieses
Common-Follow-ups.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Framework-Archivtest und keine Framework-Source-Änderung wurden
ausgeführt, weil der Benutzer die Implementierung ausdrücklich auf Parent
begrenzt hat. Keine native Hostmatrix, kein externer Remote-Fetch, keine
Dependency-Installation und keine Hosted-CI-/Governance-Operation wurden
ausgeführt. Fokussierte lokale Targets verwenden Repository-Skripte unter
`ci/`, aber keine dieser Dateien wurde geändert. Die Legacy-`ci/`-Helper-
Assertion wird als fehlgeschlagen berichtet, nicht geändert.

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
Eintritt. Remote-Veröffentlichung und Draft-PR-Erstellung warten auf eine neue
explizite Autorisierung des aktuellen Benutzers. Der aktive Checkout enthält
zudem unabhängige und gemischte gleichzeitige Edits; sie sind vom Staging
ausgeschlossen. Kein Merge ist autorisiert oder behauptet.
