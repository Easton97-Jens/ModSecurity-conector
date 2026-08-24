# Change Record

**Sprache:** [English](CR-20260824-connector-security-invariants.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260824-connector-security-invariants |
| Datum (UTC) | 2026-08-24 |
| Basis-Revision | a6b4ced4876a19666f7c7203ed9e719674c69ec1 |
| Repository-Grenze | Nur Parent; Framework, MRTS, Gitlink, CI und Governance unverändert |
| Delivery-Autorität | Benutzerautorisierter Parent-Draft-PR; kein Merge |

## Motivation und Problemstellung

Die angeforderte Prüfung umfasst zehn Connectorvarianten und ihre gemeinsamen
Common-, Engine-, Provisioning- und Runtime-Grenzen. Der Source-Review fand
drei Parent-eigene Hardening-Möglichkeiten mit konkreter Kontrolllücke:
Remote-Rule-Konfiguration konnte libmodsecurity-Remote-Laden ohne einheitliche
Trust-Policy erreichen; der nicht authentifizierte HTTP-Autorisierungshelfer
akzeptierte einen Wildcard-Listener und doppelte sicherheitsrelevante Header;
und Common-Event-Ausgabe konnte unescapte Protocol-Metadaten serialisieren und
einen unsicheren finalen Event-Pfad öffnen.

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
  Loopback-only und lehnt doppelte `Host`- sowie konfigurierte Original-URI-
  Header vor dem Transaction-Mapping ab.
- Event-Metadaten bleiben payloadfreies JSONL, sind escaped und NULL-sicher,
  und die POSIX-final Event-Datei ist no-follow, regulär und privat (`0600`).
- Die FNV-basierte Event-Kette ist nur als prozesslokale, nicht-kryptografische
  Korrelation dokumentiert; sie wird nicht als Tamper-Evidence beschrieben.
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
ausgewählter Wert das Mapping beeinflussen kann. Das bestehende begrenzte
Worker-Admission- und Shutdown-Ownership-Modell bleibt erhalten; Shutdown
liefert einen definierten Fehler, statt Runtime-Objekte zu zerstören, die noch
ein ununterbrechlicher Worker hält.

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
  Duplicate-Security-Header-Ablehnung, signal-sicheres Send und begrenztes
  Shutdown-Verhalten.
- `common/src/event.c`, `common/include/msconnector/event.h` und
  `common/include/msconnector/integrity_event.h` — escaped/NULL-sichere Event-
  Metadaten, sichere Korrelationssemantik und Event-Sink-Invariante.
- `connectors/{apache,nginx}/README.md` und `.de.md` — Remote-Rule-Verhalten.
- `connectors/{apache,nginx,envoy,haproxy,lighttpd,traefik}/capabilities.json`
  — eine konsistente Remote-Rule-Capability-Aussage.
- `tests/test_remote_rules_disabled.py`,
  `tests/test_http_authorization_service_security_contract.py` und
  `tests/test_event_runtime_security_contract.py` — fokussierte Regression-
  Contracts.
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
~~~

Die fokussierte Python-Suite bestand 11 Tests. Der Loopback-
Timeout-/Admission-Smoke bestand normal, mit ASan samt Leak-Detection und mit
UBSan. Das Memory-Safety-Target bestand seinen normalen und optionalen
ASan/UBSan-Smoke. Der begrenzte libFuzzer-Lauf absolvierte 533086 Ausführungen
in 16 Sekunden ohne AddressSanitizer- oder UndefinedBehaviorSanitizer-
Diagnose. Der C17-Syntaxcheck, die aufgeführten Common-Contracts und
Repository-Path-/Dokumentationslink-Checks bestanden.

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
Content-Length-Pfade und schützen finale Event-Datei sowie JSONL-Grenze.
Bestehende Request-/Header-/Body-Limits, Phase-Validierung, payloadfreies Event-
JSONL, lokale Rules und deterministisches Cleanup werden nicht gelockert.

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

## Verbleibende Risiken

Operatoren mit Remote Rules müssen auf Inline- oder lokale File-Rules
migrieren; eine Konfiguration mit einem der beiden Remote-Rule-Felder schlägt
deterministisch fehl, statt einen Fallback zu verwenden. Ein künftiges sicheres
Remote-Loading-Feature benötigt ein getrennt geprüftes HTTPS-/Origin-/
Integrity-/Timeout-/Size-/Atomic-Activation-Design.

HAProxy-HTX-Late-Response-Inspection, SPOP-Framing-/Cache-/Timeout-Verhalten,
Traefik-Native-UDS-Peer-Identity und host-spezifisches Lifecycle-Verhalten
bleiben plausible Kandidaten bis native, isolierte Runtime-Evidence vorliegt.
Dieser Record lässt keinen bestätigten High- oder Critical-Impact-Befund still
ungelöst.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Framework-Archivtest und keine Framework-Source-Änderung wurden
ausgeführt, weil der Benutzer die Implementierung ausdrücklich auf Parent
begrenzt hat. Keine native Hostmatrix, kein externer Remote-Fetch, keine
Dependency-Installation und keine Hosted-CI-/Governance-Operation wurden
ausgeführt. Fokussierte lokale Targets verwenden Repository-Skripte unter
`ci/`, aber keine dieser Dateien wurde geändert. Die Legacy-`ci/`-Helper-
Assertion wird als fehlgeschlagen berichtet, nicht geändert.

## Finaler Diff- und Review-Status

Bei Erstellung des Records ist dies eine Parent-only, task-eigene Änderung für
den benutzerautorisierten Draft-PR. Der aktive Checkout enthält zudem
unabhängige und gemischte gleichzeitige Edits; sie sind vom Staging
ausgeschlossen. Finaler Scoped Diff, Dokumentationschecks, exakte
Branch-/Commit-/Remote-/PR-Head-Beziehung und Hosted-Check-Status werden nach
der Delivery abgeglichen. Kein Merge ist autorisiert oder behauptet.
