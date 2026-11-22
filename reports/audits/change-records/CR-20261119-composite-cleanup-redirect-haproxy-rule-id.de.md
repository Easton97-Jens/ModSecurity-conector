# Change Record: CR-20261119-composite-cleanup-redirect-haproxy-rule-id

**Sprache:** [English](CR-20261119-composite-cleanup-redirect-haproxy-rule-id.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261119-composite-cleanup-redirect-haproxy-rule-id |
| Datum (UTC) | 2026-11-19 |
| Basis-Revision | `b79c3d93efbb8330f121caf8fb7c1a7874195e57` |

## Motivation und Problemstellung

Eine statische Sicherheitsprüfung des Parent-Connector-Scopes (2026-11-15)
meldete Kandidaten niedriger Schwere. Diese Änderung behebt die bestätigten und
reproduzierten Kandidaten sowie einen zusätzlichen, bei der Behebung gefundenen
Fehler:

- **Client-Abbruch versetzt die Composite-Engine in den Fault-Zustand (neu,
  Verfügbarkeit).** ForwardAuth übergab den Request-Kontext genau dann an
  `Admission.Cancel` und andere Finish-Pfade, wenn dieser bereits storniert war.
  Die native `commonRuntimeTransaction.Close` wertet einen stornierten Kontext
  als unsicheres Cleanup: Sie markiert die gesamte Engine als terminal
  fehlgeschlagen, und der Coordinator geht in einen Fault-Zustand. Ein einziger
  Client, der während des P2-Body-Uploads abbricht, ließ daher jede spätere
  Composite-Anfrage bis zum Neustart mit 503 fehlschlagen.
- **CAND-025: unbegrenztes natives Cleanup.** Rund zwanzig Coordinator-Pfade
  beenden Einträge mit `context.Background()`. Solange ein nativer Aufruf nicht
  zurückkehrt, wartet `Close` unbegrenzt auf das serielle Gate der
  Common-Runtime, ebenso die `closeOnce`-Wartenden des Eintrags, das
  Finish-Gate und der UDS-Admission-Slot des Traefik-Companion. Die
  MSC2-Engine-Arbeit nutzte denselben unbegrenzten Kontext, sodass auch hinter
  einem solchen Aufruf wartende Sitzungen ihre Slots behielten.
- **CAND-026: ungeprüfter ForwardAuth-`Location`-Sink.** `writeDecision`
  kopierte `Decision.RedirectURL` ohne die Steuerzeichen-/Längenprüfung aller
  Geschwister-Sinks in `Location`; ein leeres Ziel erzeugte ein 302 ohne
  `Location`.
- **CAND-001: `%u` mit vorzeichenbehaftetem `int rule_id`** im HAProxy-SPOP-
  Phase-4-Event, sodass eine negative ID als große vorzeichenlose Zahl erschien.

**Review-Nacharbeit (2026-11-20, am Head `a79f78f3e5f9a612d854e3924cf2a7e43eb47ab7`).**
Ein Review des veröffentlichten Heads fand zwei verbliebene Lücken von
CAND-025; beide wurden am Code bestätigt und reproduziert:

- `BeginRequest` schloss eine geöffnete, aber noch nicht registrierte
  Transaktion (Coordinator dazwischen im Fault-Zustand oder geschlossen) mit
  `context.WithoutCancel(ctx)`, der keine Deadline hat: Dieser Pfad umging das
  Cleanup-Budget.
- Der MSC2-Claim und der Abort der Sitzung warteten ohne Kontext auf den
  Mutex des Eintrags. ForwardAuth hält diesen Mutex während seines nativen
  P1/P2-Aufrufs, daher konnte die Frame-Deadline das Warten nicht beenden,
  und auch `Sweep` blieb hinter einem solchen Eintrag stehen. Nur den Abort
  zu begrenzen wäre fail-open gewesen: Ein langsamer P2-Aufruf, der nach dem
  Ende der Sitzung `allow` liefert, hätte die Anfrage noch freigegeben.

## Akzeptanzkriterien

1. Ein stornierter Aufrufer-Kontext erreicht nie das native Cleanup; eine
   abgebrochene ForwardAuth-Anfrage scheitert nur selbst, und die echte
   Common-Engine bedient die nächste Anfrage weiter.
2. Das native Cleanup eines terminalen Eintrags kehrt innerhalb von
   `Limits.CleanupTimeout` (Standard 5 s) zurück und hinterlässt den
   Coordinator bei Zeitüberschreitung fail-closed.
3. MSC2-Engine-Arbeit ist durch die Frame-Deadline begrenzt; eine in
   Engine-Arbeit blockierte Sitzung endet und gibt ihren Admission-Slot frei.
4. ForwardAuth sendet `Location` nur für ein gültiges Ziel; ungültige oder
   leere Ziele werden zu einem 403-Deny, das konsistent protokolliert und
   gesendet wird.
5. Das HAProxy-Event formatiert positive Rule-IDs mit `%d` und nutzt für
   fehlende IDs den Leerstring; cppcheck meldet kein `invalidPrintfArgType` mehr.
6. Legitime Lebenszyklen (normales Cleanup, gültige Redirects, normale
   UDS-Sitzung) funktionieren weiter; bestehende Framework-Go-Tests bleiben grün.
7. Das direkte Cleanup in `BeginRequest` nutzt dasselbe entkoppelte, begrenzte
   Budget.
8. Ein Claim oder Abort, der auf einen von einem nativen Aufruf gehaltenen
   Eintrag trifft, kehrt innerhalb seines Budgets zurück; der gehaltene Aufruf
   kann die Reservierung nicht mehr claimbar machen, der Eintrag wird genau
   einmal geschlossen und sein Slot genau einmal freigegeben, und `Sweep`
   überspringt einen gehaltenen Eintrag, statt auf ihn zu warten.

## Implementierungsentscheidung und Begründung

- `composite.Coordinator.cleanupContext` umhüllt den Aufrufer-Kontext mit
  `context.WithoutCancel` und `context.WithTimeout(Limits.CleanupTimeout)`;
  `entry.finish` nutzt ihn für `tx.Close`. Die Korrektur an der einzigen
  Root-Cause-Stelle deckt jeden Finish-Aufrufer ab, darunter `abortAll`, `Sweep`
  und den Composite-Envoy-Pfad, und verhindert, dass ein begrenztes
  Sitzungs-Cleanup hinter einem unbegrenzten `closeOnce`-Halter wartet. Der
  Standardwert entspricht dem bestehenden UDS-Timeout von 5 s und der Idle-TTL.
  Bei Ablauf gilt der bestehende Common-Runtime-Vertrag (Cleanup-Fehler, keine
  native Freigabe, fail-closed Coordinator-Fault).
- `compositetraefik.UDS` bedient jeden Frame über `serveFrame`, dessen
  Engine-Kontext die Verbindungs-Deadline nutzt, die bereits Lesen des Frames
  und Schreiben des Ergebnisses begrenzt. Ein späteres Ergebnis könnte ohnehin
  nicht mehr geschrieben werden. *Korrektur (2026-11-20):* Bei `a79f78f3`
  deckte dies den Claim nicht ab, der ohne Kontext auf den Mutex des Eintrags
  wartete; siehe die Nacharbeit unten.
- **Nacharbeit (2026-11-20).** `BeginRequest` schließt eine nicht registrierte
  Transaktion jetzt über `cleanupContext`. `lockEntry` erwirbt den Mutex des
  Eintrags mit einem Kontext per `TryLock`-Polling, wie beim Gate der
  Common-Runtime, sodass keine Goroutine am Mutex blockiert bleibt.
  `ClaimContext` und `AbortWithReasonContext` nutzen es (`Claim`/
  `AbortWithReason` behalten mit `context.Background()` ihr unbegrenztes
  Verhalten); die UDS übergibt dem Claim die Frame-Deadline und dem Abort ein
  frisches, erst beim Cleanup erzeugtes Budget. Ein Abort bei belegtem Eintrag
  vermerkt seinen Grund am Eintrag (atomar, geprüft gegen die unveränderliche
  reservierende Sitzung), statt eine verwendete Transaktion zu schließen:
  `checkLocked`, die Request-Phasen nach ihrem nativen Aufruf und
  `markReservedLeaseLocked` (der einzige Übergang zu claimbar) weisen den
  Eintrag dann mit `ErrAborted` zurück, und sein Eigentümer beendet ihn mit
  diesem Grund. Ein erfolgreicher Abort markiert den Eintrag vor `finish` als
  terminal, wie es `checkSessionLocked` bereits tut, sodass dazwischen kein
  neuer nativer Aufruf starten kann. `Sweep` nutzt `TryLock` und prüft einen
  gehaltenen Eintrag beim nächsten Tick. Nur das native `Close` ist zeitlich
  begrenzt; `finishGate`, `closeOnce` und der Mutex des Eintrags in `finish`
  sind es nicht, was der Code dokumentiert. Funktionen, die jetzt einen `ctx`
  erhalten, geben ihn an `finish` weiter (neutral, weil `finish` ihn selbst
  entkoppelt und begrenzt), um neue `go:S8239`-Befunde zu vermeiden.
- ForwardAuth prüft Redirect-Ziele vor `RecordHostAction` mit einem
  `validRedirectURL`, das dem Composite-Envoy-Sink entspricht (nicht leer,
  höchstens 2048 Bytes, gültiges UTF-8, keine umgebenden Leerzeichen, kein Byte
  unter 0x20, kein DEL); ungültige Ziele werden zu einem 403-Deny.
  `writeDecision` prüft den Wert als Sink erneut.
- HAProxy: `%d` für `rule_id > 0`, sonst der Leerstring, passend zum
  `rule_id > 0`-Guard des Wire-Pfads und zu den Events der anderen Connectoren.
- **Nicht geändert: CAND-024 (SO_PEERCRED am Composite-UDS).** Der Kandidat
  setzt einen feindlichen Prozess mit gleicher UID voraus. SO_PEERCRED im
  Vergleich mit der eigenen UID des Dienstes kann einen solchen Prozess nicht
  unterscheiden, und `connectors/traefik/README.md` dokumentiert das private
  `0700`-Verzeichnis als Cross-UID-Grenze, nicht als Isolation gegenüber
  derselben UID. Eine Prüfung brächte keinen Schutz gegen dieselbe UID, könnte
  aber einen als root laufenden Traefik-Prozess abweisen. Die Yaegi-Plugin-Seite
  bräuchte zusätzlich `useUnsafe`. Es wurde nichts geändert; die Begründung ist
  hier festgehalten.

## Geänderte Dateien

| Pfad | Änderung |
| --- | --- |
| `connectors/envoy/ext_proc/internal/composite/coordinator.go` | `Limits.CleanupTimeout`, `cleanupContext`, begrenztes entkoppeltes `tx.Close` in `entry.finish`. Nacharbeit: begrenztes direktes Cleanup in `BeginRequest`, `lockEntry`, `ClaimContext`, `AbortWithReasonContext`, Abort-Markierung (`ErrBusy`, `ErrAborted`), abgesichertes `markReservedLeaseLocked`, nicht blockierender `Sweep`. |
| `connectors/envoy/ext_proc/internal/compositetraefik/uds.go` | `serveFrame` mit Engine-Kontext an der Frame-Deadline; `deadline` durch `frameDeadline` ersetzt. Nacharbeit: Claim mit dem Frame-Kontext, Abort mit einem beim Cleanup erzeugten Budget. |
| `connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go` | `validRedirectURL`, Redirect-Normalisierung vor der Host-Aktion, geprüfter `Location`-Sink. |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | Vorzeichenrichtige `rule_id`-Formatierung in `phase4_common_event_write`. |
| `connectors/traefik/README.md`, `connectors/traefik/README.de.md` | Verhalten von Composite-Cleanup, Abbruch und Redirect. |
| `reports/audits/change-records/CR-20261119-composite-cleanup-redirect-haproxy-rule-id.md`, `.de.md` | Dieser Datensatz. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | Bereits vorhandene Übergabeaktualisierung aus dem Haupt-Checkout plus Stand dieser Aufgabe. |
| `.gitignore` | Bereits vorhandener `.sonarlint`-Eintrag aus dem Haupt-Checkout. |

Keine Framework- oder MRTS-Datei ist Teil dieser Connector-Änderung. Die
Regressionstests gehören dem Framework: Framework-Draft-PR
[#181](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/181)
(Branch `claude/composite-cleanup-regression-tests-20261120`, Head
`12e83a6fc189275234b9abad2e7b12132d82ff94`) ergänzt sie als On-Demand-Tests.
Der Framework-Gitlink des Connectors bleibt unverändert.

## Ausgeführte Befehle

Alle Befehle liefen über RTK aus dem Task-Worktree. Builds, Caches und Logs
liegen unter `/var/tmp/codex/ModSecurity-conector/runs/claude-security-fix-20261119/`.

| Befehl | Ergebnis |
| --- | --- |
| `rtk bypass make prepare-runtime-components RUNTIME_COMPONENT_TARGET=shared` | Exit 0; offizielles ModSecurity **v3.0.17** (vom Framework freigegebener Commit `1925753989ccce977cdaae417b55c9726c7cf02c`) in den gemeinsamen Prefix `cache/shared/prefix/modsecurity/bfc407ee…` gebaut. *Korrektur (2026-11-20):* Dieser Prefix lud PCRE2 aus der Systembibliothek; die Nacharbeitsbelege unten nutzen einen Prefix mit gebündeltem gepinntem PCRE2. |
| `rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (Baseline, Standardinventar) | Exit 0. |
| `ON_DEMAND_TESTS=1 rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (Baseline) | Exit 0, 8 Pakete ok. |
| `rtk bypass sh run-task-tests.sh after <Task-Worktree> <v3.0.17-Prefix>`: natives `build_composite.sh`, danach `go test -tags libmodsecurity -overlay <Framework-On-Demand + Task-Tests> ./...` | Build Exit 0; Tests Exit 0; alle 8 Pakete ok; `ldd` zeigt `libmodsecurity.so.3` aus dem v3.0.17-Prefix. |
| Derselbe Runner `before` auf unverändertem `origin/master` | Tests Exit 1: hängendes Cleanup > 10 s; stornierter Aufrufer-Kontext und der Abbruch mit echter Engine erzeugten beide einen Coordinator-Fault; 8 ungültige Redirect-Ziele lieferten 302; UDS-Sitzung > 5 s blockiert; Kontrollfälle bestanden. |
| `rtk bypass make -C connectors/haproxy build-spoa-runtime` gegen den v3.0.17-Prefix (vorher und nachher) | Exit 0 für beide. |
| `rtk bypass cppcheck --enable=warning … haproxy_spop_diagnostic_runtime.c` | Vorher: `invalidPrintfArgType_uint` in Zeile 2667; nachher: keine. |
| `rtk bypass go vet` und `gofmt -l` auf geänderten Paketen | Sauber. |
| `rtk bypass git diff --check` | Sauber. |

**Nacharbeit (2026-11-20), Run-ID `claude-pr454-review-20261120`**, Logs unter
`/var/tmp/codex/ModSecurity-conector/runs/claude-pr454-review-20261120/`.
libModSecurity v3.0.17 mit gebündeltem gepinntem PCRE2 10.49 (Provisionierung
aus Framework-PR #180; `ldd` löst beide aus diesem Prefix auf, kein
System-PCRE2). Die Tests sind die aus Framework-PR #181.

| Befehl | Ergebnis |
| --- | --- |
| `ON_DEMAND_TESTS=1 GOFLAGS='-tags=libmodsecurity -v' rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc FRAMEWORK_ROOT=<Worktree von Framework-PR #181>` (nach nativem `build_composite.sh`) | Exit 0; 8 Pakete ok; 20 von 20 neuen Tests bestanden, 0 übersprungen. |
| Dasselbe mit `-race` | Exit 0; 8 Pakete ok; 0 Data Races. |
| Dieselben Tests ohne `entry_wait_bounds_test.go` gegen `a79f78f3e5f9a612d854e3924cf2a7e43eb47ab7` | Exit 1, erwartet: beide Tests zum direkten Cleanup kehrten bei 50 ms Budget nicht innerhalb von 2 s zurück, `Sweep` blieb stehen, der Claim wartete bei 100 ms Frame-Deadline über 2 s; alle übrigen Tests bestanden. |
| Dieselben Tests ohne die drei Coordinator-Dateien gegen `b79c3d93efbb8330f121caf8fb7c1a7874195e57` | Exit 1, erwartet: gehaltener Claim, unbegrenzte Response-Arbeit, 8 ungültige Redirects lieferten 302, Abbruch versetzte den Coordinator in den Fault-Zustand (Double und echte Engine: `cannot close Common runtime after unsafe transaction cleanup`); Kontrollfälle bestanden. |
| `rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (Standardinventar, Framework-PR #181) | Exit 0; 2 von 2 ausgewählten Fällen bestanden; `active_case_count` 100. |
| `ON_DEMAND_TESTS=1 rtk bypass make -C connectors/haproxy self-test-spoa-runtime` (Framework-PR #181), Basis / korrigiert | Exit 2 / 2: Der neue Fall meldet auf der Basis `rule_id=0 did not serialize as ""` und besteht nach der Korrektur; ein späterer, unveränderter Protokoll-Selbsttest scheitert in beiden ohne Meldung, auch mit dem unveränderten Framework-Pin (vorbestehend). |
| `rtk bypass go vet ./internal/... ./cmd/...`, `gofmt -l` | Sauber. |
| `rtk bypass /usr/local/bin/sonar-with-env api get /api/issues/search?…pullRequest=454…` | 8 neue `go:S8239`-Code-Smells auf `a79f78f3`, alle in Zeilen von `coordinator.go`, die dieser PR nicht ändert (Blame `6ccfd8de`); Einordnung unten. |
| `gh pr checks 454` auf `a79f78f3` | 58 bestanden, 5 übersprungen, 0 fehlgeschlagen; SonarCloud-Quality-Gate bestanden. Diese Ergebnisse decken die unveröffentlichte Nacharbeit nicht ab. |

## Security-Auswirkung

- Beseitigt einen aus der Ferne auslösbaren, fail-closed Denial of Service des
  experimentellen Traefik-Composite: Ein abbrechender Client legt die
  gemeinsame Common-Engine nicht mehr still. Vorbedingung vor der Korrektur: Ein
  Client bricht während der ForwardAuth-P2-Body-Phase ab. Auswirkung vor der
  Korrektur: Jede spätere Composite-Anfrage lieferte bis zum Neustart 503.
- Begrenzt das Festhalten von Ressourcen, wenn ein nativer Aufruf nicht
  zurückkehrt; der Prozess benötigt in diesem Fall weiterhin einen
  kontrollierten Neustart, jetzt als expliziter Fault.
- Defense in Depth für den ForwardAuth-`Location`-Sink; Go `net/http`
  schreibt rohe CR/LF bereits um, sodass keine eigenständige Header-Injection
  bestand.
- Evidence-Integrität für HAProxy-Phase-4-Events.
- Keine Authentifizierungs-, Autorisierungs-, Isolations- oder
  Redaktionskontrolle wurde abgeschwächt; ungültige Redirect-Ziele werden
  strenger abgewiesen.

## Runtime-Evidence

Die Regressionstests nutzten die echte Common-/libmodsecurity-Engine
(`-tags libmodsecurity`), gelinkt gegen den offiziellen v3.0.17-Build; die
Läufe vom 2026-11-20 nutzten den Prefix mit gebündeltem gepinntem PCRE2 10.49. Es sind
Laufzeittests auf Paketebene, keine Host-Nachweise: Es wurde kein Traefik-,
Envoy- oder HAProxy-Hostprozess gestartet.

## Bekannte Einschränkungen

- Ein nativer Aufruf, der nicht zurückkehrt, erfordert weiterhin einen
  Prozessneustart; der Composite-Dienst startet sich bei einem Coordinator-Fault
  nicht selbst neu.
- CAND-024 ist nicht geändert (siehe Begründung oben).
- Der Composite-Envoy-Pfad profitiert von der Coordinator-Korrektur, es wurde
  aber kein Composite-Envoy-spezifischer Reproducer geschrieben.
- Der `before`-Lauf erzeugte zusätzlich einen Panic in einem Test-Double der
  Aufgabe für einen `nil`-Kontext; die echte `Close` normalisiert `nil`, daher
  ist dies kein Produktfehler.
- Die Grenzen gelten je Schritt (Frame-Deadline, Abort-Budget, Budget des
  nativen Close), nicht als harte Gesamtzeitgrenze eines UDS-Handlers.
  `finishGate`, `closeOnce` und der Mutex des Eintrags in `finish` sind nicht
  zeitlich begrenzt; ein Claim bei belegtem Eintrag kann die ganze
  Frame-Deadline verbrauchen, sodass der Companion statt eines 503-Frames eine
  geschlossene Sitzung sieht (beides fail-closed).
- Die 8 `go:S8239`-Befunde auf `a79f78f3` sind vorbestehende, bewusste
  Entkopplungen fail-closed Cleanups von Request-Kontexten; vor diesem PR hätte
  dort der Request-Kontext den Engine-Fault durch abgebrochene Kontexte
  ausgelöst. Sie werden hier nicht geändert und brauchen eine Sonar-Disposition
  durch Maintainer.
- Das native HAProxy-Selbsttest-Target scheitert in dieser Umgebung an einem
  vorbestehenden, stummen Fehler eines Protokoll-Selbsttests.

## Verbleibende Risiken

Bei sehr hoher Konkurrenz versetzt ein legitimes Cleanup, das länger als 5 s
auf das serielle Gate wartet, den Coordinator nun in den Fault-Zustand, statt
weiter zu warten. Der eigenständige ext_proc-Dienst wendet dasselbe Modell
bereits mit 1 s Standardwert an; der Composite-Standard von 5 s ist
konservativer.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Host-Runtime-, Matrix-, Sanitizer-, Fuzz- oder CRS-Lauf: außerhalb
  dieser begrenzten Korrektur.
- `go test -race`: für die Nacharbeit am 2026-11-20 ausgeführt (bestanden).
- Die Regressionstests sind On-Demand-Framework-Tests (Framework-Draft-PR
  #181), nicht Teil der Standard-Suite mit 100 Fällen. Die Spezialregressionen
  aus Framework #181 mit `CONNECTOR_REVISION` auf einer Parent-Revision
  ausführen, die diese Nacharbeit enthält.
- Gehostete CI und das SonarQube-Cloud-Quality-Gate für den aktuellen PR-Head prüfen.

## Finaler Diff- und Review-Status

Der finale, begrenzte Diff wurde lokal geprüft; `git diff --check` ist sauber.
Die Auslieferung ist in [Parent-PR #454](https://github.com/Easton97-Jens/ModSecurity-conector/pull/454) dokumentiert.

Am 2026-11-21 bestanden der native Build `build-envoy-ext-proc` und alle acht Pakete im Lauf `framework-go-test`. Der Lauf nutzte das Overlay aus Framework #181, den Build-Tag `libmodsecurity` und das gepinnte ModSecurity-/PCRE2-Präfix.

Die acht S8239-Aufrufstellen geben jetzt den Aufruferkontext weiter. Das Cleanup behält seine eigene Frist und läuft auch nach einem Request-Abbruch weiter. Alle acht Pakete bestanden erneut mit aktiviertem Race Detector.
