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
  nicht mehr geschrieben werden.
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
| `connectors/envoy/ext_proc/internal/composite/coordinator.go` | `Limits.CleanupTimeout`, `cleanupContext`, begrenztes entkoppeltes `tx.Close` in `entry.finish`. |
| `connectors/envoy/ext_proc/internal/compositetraefik/uds.go` | `serveFrame` mit Engine-Kontext an der Frame-Deadline; `deadline` durch `frameDeadline` ersetzt. |
| `connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go` | `validRedirectURL`, Redirect-Normalisierung vor der Host-Aktion, geprüfter `Location`-Sink. |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | Vorzeichenrichtige `rule_id`-Formatierung in `phase4_common_event_write`. |
| `connectors/traefik/README.md`, `connectors/traefik/README.de.md` | Verhalten von Composite-Cleanup, Abbruch und Redirect. |
| `reports/audits/change-records/CR-20261119-composite-cleanup-redirect-haproxy-rule-id.md`, `.de.md` | Dieser Datensatz. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | Bereits vorhandene Übergabeaktualisierung aus dem Haupt-Checkout plus Stand dieser Aufgabe. |
| `.gitignore` | Bereits vorhandener `.sonarlint`-Eintrag aus dem Haupt-Checkout. |

Keine Framework- oder MRTS-Datei wurde geändert. Die unten genannten
Regressionstests gehören zur Aufgabe und wurden nur über ein Go-`-overlay`
eingebunden; sie sind nicht Teil dieses Commits.

## Ausgeführte Befehle

Alle Befehle liefen über RTK aus dem Task-Worktree. Builds, Caches und Logs
liegen unter `/var/tmp/codex/ModSecurity-conector/runs/claude-security-fix-20261119/`.

| Befehl | Ergebnis |
| --- | --- |
| `rtk bypass make prepare-runtime-components RUNTIME_COMPONENT_TARGET=shared` | Exit 0; offizielles ModSecurity **v3.0.17** (vom Framework freigegebener Commit `1925753989ccce977cdaae417b55c9726c7cf02c`) in den gemeinsamen Prefix `cache/shared/prefix/modsecurity/bfc407ee…` gebaut; die Systembibliothek wurde für Tests nicht verwendet. |
| `rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (Baseline, Standardinventar) | Exit 0. |
| `ON_DEMAND_TESTS=1 rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (Baseline) | Exit 0, 8 Pakete ok. |
| `rtk bypass sh run-task-tests.sh after <Task-Worktree> <v3.0.17-Prefix>`: natives `build_composite.sh`, danach `go test -tags libmodsecurity -overlay <Framework-On-Demand + Task-Tests> ./...` | Build Exit 0; Tests Exit 0; alle 8 Pakete ok; `ldd` zeigt `libmodsecurity.so.3` aus dem v3.0.17-Prefix. |
| Derselbe Runner `before` auf unverändertem `origin/master` | Tests Exit 1: hängendes Cleanup > 10 s; stornierter Aufrufer-Kontext und der Abbruch mit echter Engine erzeugten beide einen Coordinator-Fault; 8 ungültige Redirect-Ziele lieferten 302; UDS-Sitzung > 5 s blockiert; Kontrollfälle bestanden. |
| `rtk bypass make -C connectors/haproxy build-spoa-runtime` gegen den v3.0.17-Prefix (vorher und nachher) | Exit 0 für beide. |
| `rtk bypass cppcheck --enable=warning … haproxy_spop_diagnostic_runtime.c` | Vorher: `invalidPrintfArgType_uint` in Zeile 2667; nachher: keine. |
| `rtk bypass go vet` und `gofmt -l` auf geänderten Paketen | Sauber. |
| `rtk bypass git diff --check` | Sauber. |

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
(`-tags libmodsecurity`), gelinkt gegen den offiziellen v3.0.17-Build. Es sind
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

## Verbleibende Risiken

Bei sehr hoher Konkurrenz versetzt ein legitimes Cleanup, das länger als 5 s
auf das serielle Gate wartet, den Coordinator nun in den Fault-Zustand, statt
weiter zu warten. Der eigenständige ext_proc-Dienst wendet dasselbe Modell
bereits mit 1 s Standardwert an; der Composite-Standard von 5 s ist
konservativer.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Host-Runtime-, Matrix-, Sanitizer-, Fuzz- oder CRS-Lauf: außerhalb
  dieser begrenzten Korrektur.
- `go test -race` wurde nicht ausgeführt.
- Die Regressionstests der Aufgabe werden nicht in das Framework-Inventar
  aufgenommen: Das Framework ist ein separates Repository, und die
  Standard-Suite ist auf 100 aktive Fälle begrenzt.
- Gehostete CI und das SonarQube-Cloud-Quality-Gate müssen für den PR-Head
  gelesen werden.

## Finaler Diff- und Review-Status

Der finale, begrenzte Diff wurde lokal geprüft; `git diff --check` ist sauber.
Die Auslieferung erfolgt als Draft-PR aus `claude/fix-security-findings-20261119`;
er ist nicht gemergt.
