# Change Record

**Sprache:** [English](CR-20260814-f-gs-006-http-authorization-admission.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260814-f-gs-006-http-authorization-admission |
| Datum (UTC) | 2026-08-14 |
| Basis-Revision | ea3b48abab7940de49997a371f9117b409c05a2a |
| Zugehöriges Finding | F-GS-006 (<code>partially_fixed</code>) |
| HTTP-Teilstatus | <code>hardening_applied_locally_verified</code> |
| Repository-Grenze | Nur Parent; Framework und MRTS unverändert |
| Delivery-Autorität | Nur begrenzter Commit, Push und Draft-PR; kein Merge und kein Ready-for-review |

## Motivation und Problemstellung

Der gemeinsame HTTP/1.1-Autorisierungsdienst akzeptierte eine Verbindung und
las, mappte, wertete aus, beantwortete und schloss sie anschließend in der
Listener-Schleife. Ein unvollständiger Client konnte damit einen späteren
validen Client bis zu seiner absoluten Read-Deadline verzögern. Der Dienst
besaß zudem keine explizit begrenzte Connection-Admission-Policy.

F-GS-006 erfasst auch Kandidaten zu Event/Rule/Remote-Origin und zur
Traefik-UDS-Identität. Die Repository-Evidence belegt weder einen kompatiblen
Configuration-/Path-/Origin-Vertrag für Erstere noch einen Live-Peer-Identity-
und Restart-Vertrag für Letztere. Keiner erhält in diesem Record eine
spekulative Code-Änderung.

## Akzeptanzkriterien

- <code>--max-connections</code> verwendet standardmäßig <code>8</code> und akzeptiert nur <code>1</code> bis <code>64</code>.
- Leere, negative, nullwertige, überlaufende, mit Nachzeichen versehene und zu
  große Capacity-Werte werden durch den bestehenden Numeric-Parser-Vertrag
  abgewiesen.
- Ein unvollständiger Loopback-Client verzögert einen gleichzeitig validen
  Client nicht seriell, und ein voller Admission-Bound schließt eine später
  angenommene Verbindung.
- Die Default-Sättigung mit acht Slots ist begrenzt, und nach Freigabe eines
  Slots wird ein valider Client bedient.
- Detached-Worker-Metadaten und Active-Worker-Accounting bleiben über die
  Prozesslaufzeit begrenzt; Worker werden vor der Runtime-Zerstörung geleert.
- Worker-Shutdown unterbricht blockiertes Socket-I/O, ohne dem Worker die
  Ownership für das finale close zu nehmen.
- Die gemeinsame Runtime wird nur während Request-Mapping und Runtime-
  Transaction-Arbeit serialisiert, nicht während Socket-Reads oder
  Response-Writes.
- Direkte Smoke-, Envoy-, Envoy-ext_proc- und Traefik-C-Buildpfade führen
  pthread-Compile-/Link-Unterstützung, sofern sie diesen Code kompilieren oder
  linken.

## Implementierungsentscheidung und Begründung

### Technische Entscheidungen

<code>common/runtime/http_authorization_service.c</code> erzeugt beim Start einen
Snapshot der Request-Limits und lässt höchstens die konfigurierte Anzahl
detached Worker zu. Ein Worker wird vor seinem Start in die service-eigene
Liste aufgenommen und entfernt sich unter dem Worker-Mutex genau einmal,
während er den Active-Worker-Count dekrementiert. Dadurch akkumulieren weder
beendete joinable Thread-Handles noch Worker-Metadaten. Eine Condition Variable
wartet, bis aktive Worker null erreichen, bevor die Runtime zerstört wird.

Der Listener schließt einen angenommenen Socket sofort, wenn kein
Admission-Slot verfügbar ist; er erzeugt keine User-Space-Queue. Falls
Worker-Allokation, Attribute-Setup oder Thread-Erzeugung fehlschlagen, entfernt
dieselbe Release-Route die Worker-Metadaten und schließt den angenommenen FD.
Shutdown hält den Worker-List-Mutex nur während <code>shutdown(fd, SHUT_RDWR)</code>.
Der Worker bleibt der eindeutige Owner von finalem <code>close(fd)</code>, was eine
shutdownseitige FD-Reuse- oder Double-Close-Race verhindert.

Socket-Reads erfolgen vor dem Runtime-Mutex, und Responses werden nach dessen
Freigabe geschrieben. Request-Mapping, Transaction-Begin, Finish, Destroy und
die Kopie der Transaction-ID werden durch einen service-lokalen Runtime-Mutex
serialisiert, weil die Common Runtime mutierbaren gemeinsamen Engine-, Event-
und Transaction-State besitzt. Kein Pfad hält den Worker-List-Mutex, während er
den Runtime-Mutex anfordert.

Die Option <code>--listen</code> bleibt explizit: Es gibt keinen impliziten Bind-Default.
<code>127.0.0.1</code> und <code>localhost</code> beschreiben den Loopback-Anwendungsfall;
<code>0.0.0.0</code> bleibt ein ausdrücklich gewähltes, kompatibles Binding. Der Default
von <code>--max-connections</code> ist <code>8</code>, das Maximum <code>64</code>, und das bestehende
Maximum des Connection-Timeouts bleibt 600000 ms.

Der fokussierte Smoke ergänzt deterministische Default-8-Sättigung und
Recovery, begrenzte sequenzielle und vollständige parallele Requests, abrupten
Disconnect, Shutdown bei blockiertem Read und Capacity-Parser-Grenzfälle. Ein
pthread-Create-Fault wurde nicht injiziert: Das aktuelle repository-native
Design besitzt keine proportionale Fault-Injection-Naht, und ihre Ergänzung nur
für diesen Fall wäre eine weitergehende Testabstraktionsänderung. Die
Source-Error-Route wird stattdessen durch das begrenzte Release-Design geprüft.

## Geänderte Dateien

- <code>common/runtime/http_authorization_service.c</code> — begrenzte Admission,
  Detached-Worker-Lifecycle, FD-Ownership, Shutdown-Drain und enger Runtime-Lock.
- <code>ci/checks/common/http_authorization_service_timeout_smoke.c</code> —
  deterministische Admission-, Parser-, Lifecycle-, Recovery-, Disconnect- und
  Shutdown-Abdeckung.
- <code>ci/checks/common/check-http-authorization-service-timeout.sh</code> —
  pthread-Compile-/Link-Unterstützung für den fokussierten Helper.
- <code>connectors/envoy/build/build_connector.sh</code> — pthread-Compile- und
  Link-Unterstützung für den Envoy-ext_authz-Buildpfad.
- <code>connectors/envoy/build/build_ext_proc.sh</code> — pthread-Compile-
  Unterstützung für das vom Envoy-ext_proc verwendete Common-Archiv; seine
  cgo-Link-Flags enthalten sie bereits.
- <code>connectors/traefik/build/build-connector.sh</code> — pthread-Compile-
  Unterstützung; sein bestehender Linkpfad enthält sie bereits.
- <code>docs/operations-and-security.md</code> und
  <code>docs/operations-and-security.de.md</code> — operatororientierte Admission-,
  Bound- und External-Bind-Grenzen.
- Dieses englisch/deutsche Change-Record-Paar und gepaarte Archivindex-Einträge
  — begrenzte Nachvollziehbarkeit, tatsächlicher Validierungsstand und
  bereinigte Follow-ups.

Es werden keine Event/Rule/Remote-Origin-Quellen, keine Traefik-UDS-
Client-Quelle, keine Go-Modul- oder Toolchain-Datei, kein Framework, MRTS,
Gitlink, Dependency oder Workflow geändert. Lokale Task-Pläne, externe
Build-Ausgabe und Cleanup-Metadaten sind keine versionierten Produktartefakte.

## Ausgeführte Befehle

Der portable Platzhalter <code>&lt;external-task-build-root&gt;</code> bezeichnet die für die
beobachteten Befehle verwendete externe, task-eigene Build-Wurzel.
Repository-Pfade bleiben relativ.

### PASS

~~~text
rtk proxy env CC=gcc 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror' BUILD_ROOT=<external-task-build-root>/gcc-c17 make check-http-authorization-service-timeout
rtk proxy env CC=clang 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror' BUILD_ROOT=<external-task-build-root>/clang-c17 make check-http-authorization-service-timeout
rtk proxy env CC=clang ASAN_OPTIONS=detect_leaks=1:halt_on_error 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror -fsanitize=address -fno-omit-frame-pointer' BUILD_ROOT=<external-task-build-root>/asan make check-http-authorization-service-timeout
rtk proxy env CC=clang UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror -fsanitize=undefined -fno-omit-frame-pointer' BUILD_ROOT=<external-task-build-root>/ubsan make check-http-authorization-service-timeout
rtk proxy env CC=clang TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror -fsanitize=thread -fno-omit-frame-pointer' BUILD_ROOT=<external-task-build-root>/tsan make check-http-authorization-service-timeout
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/parent-checks make check-common-sdk-contract check-common-security-contract check-common-helpers check-common-flow-integrity check-adapter-contracts check-remaining-connectors-common-adoption check-remaining-connectors-build-wiring check-remaining-connectors-c-standard-wiring
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/c17-checks make check-remaining-connectors-c17-lint check-remaining-connectors-c17
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/common-memory make check-common-memory-safety
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/docs make check-connector-guides
rtk proxy jq -e 'type == "object"' connectors/envoy/SOURCE_MAP.json
rtk proxy jq -e 'type == "object"' connectors/traefik/SOURCE_MAP.json
rtk proxy git diff --check
~~~

Jeder fokussierte Smoke absolvierte die ergänzten Parser-, Admission-, Recovery-,
Sequenz-, Parallel-, abrupten Disconnect- und Blocked-Read-Shutdown-Fälle.
AddressSanitizer, UndefinedBehaviorSanitizer und ThreadSanitizer erzeugten
keine Diagnose. Die Common-/Connector-Verträge und C17-Wiring-Checks bestanden.
Keine versionierte JSON-Datei änderte sich; die relevanten Connector-JSON-
Objekte wurden erfolgreich geparst.

### Historische Pre-Fix-Evidence

~~~text
rtk proxy env BUILD_ROOT=<external-pre-fix-build-root> make check-http-authorization-service-timeout
~~~

Dieser frühere isolierte Lauf schlug erwartungsgemäß fehl mit
<code>parallel_request: valid peer waited for the stalled peer deadline</code>. Er wird
nicht mit dem erweiterten aktuellen Smoke gegen die Basis-Revision neu
kompiliert, weil dieser Smoke nun <code>--max-connections</code> ausübt, das im
Pre-Fix-Source nicht existiert.

### UNKNOWN / blockiert

~~~text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/docs make check-bilingual-docs
rtk proxy env PYTHONDONTWRITEBYTECODE=1 <repository-python> ci/checks/documentation/check-repository-path-references.py
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOWORK=off GOCACHE=<external-task-build-root>/go-cache make -C connectors/traefik test-native-middleware
~~~

Die beiden Dokumentationsbefehle melden ausschließlich bereits vorhandene
fehlende Links unter <code>modules/ModSecurity-test-Framework/</code>; der saubere
Task-Worktree enthält den nicht initialisierten Framework-Gitlink, und dieser
Task initialisiert oder ändert dieses getrennte Repository nicht. Sie sind
daher <code>UNKNOWN</code>, nicht Evidence gegen die geänderte HTTP-Dokumentation.

Der Traefik-Befehl ist <code>UNKNOWN (blocked_environment)</code> mit dem exakten Fehler:
<code>go: go.mod requires go &gt;= 1.26.5 (running go 1.26.0; GOTOOLCHAIN=local)</code>.
The installed Go toolchain is 1.26.0 while the module requires Go 1.26.5. With
<code>GOTOOLCHAIN=local</code>, validation cannot proceed; enabling automatic toolchain
download is prohibited for this task.

## Security-Auswirkung

Die geschlossene Invariante ist bewusst eng: **Ein langsamer oder
unvollständiger Client blockiert nicht mehr seriell jeden nachfolgenden Client,
und die parallele Verbindungsbehandlung ist begrenzt.** Dies ist ein
Availability-Hardening für die HTTP-Autorisierungsgrenze, keine Behauptung,
dass jede Denial-of-Service-Bedingung beseitigt ist.

F-GS-006 bleibt <code>partially_fixed</code>. Event/Rule/Remote-Inputs bleiben
<code>unproven</code>, und der Traefik-UDS-Client bleibt
<code>blocked_missing_evidence</code>.

## Runtime-Evidence

Alle ausgeführten HTTP-Nachweise verwenden einen lokalen Loopback-Listener und
eine Fake Common Runtime. Sie belegen die engen Admission- und Lifecycle-
Invarianten, nicht eine reale Envoy- oder Traefik-Host-Integration,
libmodsecurity-Produktivverhalten, externes Netzwerkverhalten oder
Delivery-Status. Im Repository ist keine Envoy- oder Traefik-Host-Binary
installiert, und <code>pkg-config</code> besitzt keinen <code>libmodsecurity</code>-Package-Eintrag;
keine Host-Runtime und kein Dependency-Download wurden versucht.

## Bekannte Einschränkungen

Die Runtime-Auswertung selbst bleibt für die Thread-Sicherheit der Common
Runtime serialisiert. Eine langsame Runtime-Transaction kann daher den
Durchsatz begrenzen, auch wenn Socket-Reads und -Writes überlappen. Der Test
ist absichtlich begrenzt und lokal; er ist kein Produktions-Stresstest. Es
wurde aus dem genannten repository-nativen Testbarkeitsgrund kein
pthread-Create-Fault-Injection ergänzt.

## Verbleibende Risiken

Acht langsame Clients können die standardmäßigen acht Admission-Slots
ausschöpfen, und bis zu 64 langsame Clients können ein konfiguriertes Maximum
bis zu ihrer absoluten Deadline ausschöpfen; der höchstzulässige Timeout beträgt
600000 ms. Der Dienst bietet keine eingebaute Fairness, kein Rate-Limiting,
kein TLS und keine Client-Authentisierung. Ein explizites <code>0.0.0.0</code>-Binding
bleibt eine hostseitige Expositionsentscheidung, die passende
Netzwerk-Kontrollen und eine authentisierte Schutzschicht benötigt. Es wird
kein Risiko akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

Reale Envoy- und Traefik-Host-Runtime-Tests wurden nicht ausgeführt, weil die
erforderlichen Host-Binaries und vollständigen konfigurierten Voraussetzungen
nicht vorhanden sind; ihr Download oder Provisioning liegt außerhalb dieses
Tasks. Keine Produktions-, externes-Netzwerk-, Framework-, MRTS-, Merge-,
Ready-for-review-, Resulting-Master- oder Hosted-CI-Validierung wird behauptet.

## Bereinigte Follow-up-Entwürfe

Das Repository ist öffentlich, und seine Security-Policy erlaubt keine
öffentlichen Issues zu vermuteten Sicherheitsbedenken. Es wurde kein Issue
erstellt. Die folgenden issue-fertigen Design-/Hardening-Entwürfe werden ohne
unnötige Attack-Path-Details für den Draft-PR aufbewahrt.

### Define the security contract for event/rule paths and remote rule origins

**Benötigte Produktentscheidungen:** festlegen, wer <code>event_path</code>, lokale Rule-
Pfade und Remote-Rule-URLs setzen darf; unterstützte absolute und relative
Pfade, autoritative Base-Roots, Parent-Directory-Ownership und Symlink-/
Replacement-Semantik definieren; erlaubte URL-Schemes, Redirect, TLS,
DNS/Internal-Target, Origin-Allowlist, Pinning/Checksum und Failure-Verhalten
definieren; Operator-Status und Provenance-Anforderungen für Remote-Rules
angeben.

**Akzeptanzkriterien:** einen expliziten Code- und bilingualen
Dokumentationsvertrag veröffentlichen; positive und negative Containment-,
Object-Type-, Ownership-, Replacement- und Remote-Provenance-Tests ergänzen;
die Path- oder Remote-Input-Grenze nicht befördern, bevor diese fokussierten
Tests den Vertrag zeigen.

### Define and verify Traefik UDS peer identity

**Benötigte Produktentscheidungen:** erwartete Server-UID/GID und die Frage
definieren, ob ein Same-UID-Angreifer im Scope liegt; unterstütztes Linux-
<code>SO_PEERCRED</code>-Verhalten oder einen äquivalenten Identitätsmechanismus mit
sicherem Fail-Closed-Verhalten auf anderen Plattformen wählen; Restart/Rebind-,
Container-, Mount- und Namespace-Semantik definieren; Descriptor-Handoff oder
eine langlebige verifizierte Verbindung bewerten; eine tatsächliche
Traefik-Host-Integration-Fixture verlangen.

**Akzeptanzkriterien:** Identität an jede angenommene Client-zu-Engine-Session
binden; Identity-Mismatch, Restart-Replacement und Unsupported-Platform-
Verhalten deterministisch und gegebenenfalls fail closed gestalten; fokussierte
Tests und bilinguale Dokumentation ergänzen. Dieses Design-Follow-up bleibt
getrennt vom internen UDS-Evidence-Record und besitzt hier keinen Source-Patch.

## Finaler Diff- und Review-Status

Der begrenzte Patch enthält nur HTTP-Autorisierungs-Admission-Hardening, seine
Tests, direktes Build-Wiring, gepaarte Operations-Dokumentation und gepaarten
Change-Record/Index. F-GS-006 bleibt eine bewusst partielle Remediation; es
wird keine Completion des Gesamtfindings behauptet. Ein enger Commit, Push und
Draft-PR sind nach finalem Staged-Diff-Review autorisiert; der exakte Commit,
PR und einmalige Hosted-Check-Snapshot werden in Delivery-Metadaten
aufgezeichnet, statt in diesem Record eine selbstreferenzielle Commit-Schleife
zu erzeugen.
