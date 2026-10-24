# Change Record: CR-20261018-haproxy-companion-client-windows

**Sprache:** [English](CR-20261018-haproxy-companion-client-windows.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-companion-client-windows |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `f8a1bfa272dfd3ca0953ad8e7ca2dffe5864140d` |

## Motivation und Problemstellung

Gespeicherte Companion-Clients erfassten bisher nur das abschließende `time_ns`; ohne Start fehlte ein eindeutiges Requestfenster. Verbindungs- oder Sendefehler konnten ohne Clientbericht enden. Neue Captures erhalten physische Messungen, ohne historische Zeitpunkte zu erfinden, parallele TLS-Schreibvorgänge anhand globaler Reihenfolge zuzuordnen oder Lifecycle-Anrechnung zu vergeben.

## Akzeptanzkriterien

Zunächst das fehlende Startfeld reproduzieren. Start-/Abschlusszeit des Kindes als Wall- und Monotonic-Clock, echte PID, beobachtete Endpunkte und tatsächliche Request-Sendegrenzen erfassen. Fehler-/Cancelbytes und unbekannte Felder erhalten. Unabhängig exakte gestartete argv, abgewarteten Exit/Signal und Parent-Start-/Wartezeiten erhalten. Alle 71 Originaldefinitionen und 82 Vorhersagen in einem neuen versiegelten v7-Snapshot unverändert halten und harmlose echte Clientkomponenten prüfen.

## Implementierungsentscheidung und Begründung

Das neue Schema `i12-companion-client-capture-v2` in `client-N.json` erfasst `started_wall_ns`, `started_monotonic_ns`, `completed_wall_ns`, `completed_monotonic_ns`, `pid`, `connection_local`, `connection_peer` sowie Start-/Abschlusszeiten des Requestsendens. `time_ns` ist ein Alias der neu gemessenen Abschluss-Wall-Clock. Endpunkt- und Sendefelder bleiben null, wenn sie nicht tatsächlich erreicht wurden. Partielle Response-/Requestbytes und Berichte werden bei Capture-Exceptions vor dem erneuten Auslösen derselben Exception gespeichert; Cancel bleibt von TLS-EOF und nativem EOS getrennt. Bestehende Response-/Framingvergleiche behalten Inputs und Verhalten.

Das unabhängige Schema `i12-companion-client-process-v1` in `client-N.process.json` erfasst exakte `argv`, tatsächliche `pid`, abgewartete `exit`, `signal`, `reaped`, `timed_out`, `launch_error` und Parent-Start-/Wartezeiten als Wall-/Monotonic-Clock. Bei Timeout wird das Kind beendet und abgewartet; rohe stdout/stderr bleiben erhalten. Ein fehlender Kindbericht bleibt fehlend; Parentzeitpunkte erfinden kein Kindfenster. Bei normaler Rückkehr wird derselbe Prozessbeleg an die aggregierten Befehle angehängt. Der unabhängige Observer-Owner erhielt die exakten Schemas und Feldnamen.

Das Root-Nachreview bestätigte eine Ownership-Regression gegenüber Python 3.14.7 `subprocess.run`: Beliebige Kommunikationsausnahmen konnten das neue explizite `Popen`-Kind weiterlaufen lassen. Eine Kontrolle mit echten Kindern reproduzierte dies für injizierte Parent-Ausnahmen `KeyboardInterrupt`, `SystemExit` und `RuntimeError`; die Negativkontrolle beendete und wartete jeden Überlebenden anschließend selbst ab. Die Korrektur beendet das Kind, liest die Pipes, wartet und schließt die eigenen Ausgabepipes, bevor dieselbe Originalausnahme weitergegeben wird. Der Prozessbeleg erfasst tatsächlichen abgewarteten Exit/Signal sowie optionales `communication_error`; fehlende Kindzeitpunkte werden nicht erfunden. Echte `os.waitpid`-Prüfungen belegen, dass der korrigierte Owner jedes Kind bereits abgewartet hat. Das bestehende Timeoutverhalten bleibt abgedeckt. Diese notwendige Korrektur erzeugt v7 und erhält v6 unverändert.

## Geänderte Dateien

- `connectors/haproxy/harness/i12_companion_host.py`
- `tests/test_haproxy_i12_companion_host.py`
- `reports/audits/change-records/CR-20261018-haproxy-companion-client-windows.md`
- `reports/audits/change-records/CR-20261018-haproxy-companion-client-windows.de.md`

## Ausgeführte Befehle

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m pytest -q tests/test_haproxy_i12_companion_host.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion/client-windows-v1/run-component-controls.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion/client-windows-v1/interrupt-cleanup-v1/verify-fixture-parity-v7.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion/prepare-fixtures-v7.py
```

Python 3.14.7: 40 Tests und 22 Subtests bestanden, einschließlich der bisherigen 39 Tests/19 Subtests. Vor der Änderung schlug die neue Regression wegen fehlendem `started_wall_ns` fehl; der rohe Fehlerbeleg bleibt erhalten. Das harmlose Komponentenverfahren maß verifizierten lokalen TLS-Erfolg (Clientexit 0), eine tatsächlich abgewiesene Verbindung (Exit 1, unbekannte Endpunkte/Sendeabschlüsse) und ein tatsächliches SIGTERM-Warten (Signal 15, kein erfundener Kindbericht). Simulierte Kontrollen prüfen Cancel, Sendefehler und Timeout/Kill/Reap. Alle 1147 Paritätsprüfungen bestanden: 71 Originaldefinitionen und alle 82 Vorhersagen sind byteidentisch; Body-/MIME-/native-/Quellerwartungen je Fixture stimmen mit v5 überein; bisherige Clientfelder/Rawbytes/Transportvergleiche bleiben gleich; unberührte Produzenten/Guards entsprechen dem AST bei Taskbeginn. Der kanonische P3-Redirect bleibt 302.

## Security-Auswirkung

TLS-Zertifikats- und Hostnameprüfung bleiben aktiv, mit expliziter Fixture-OpenSSL-Konfiguration. Pfad-/Symlink-/Private-Root-Guards sowie Response-/Framingprädikate bleiben erhalten. Endpunkte stammen vom tatsächlichen Socket und werden nicht aus konfigurierten Adressen rekonstruiert. Keine Änderungen an Produkt, gemeinsamen Captures, Matrix, Framework oder MRTS sowie keine Änderung von Securityscans/Gates. Lokale Komponenten-TLS-Zertifikate und private Schlüssel sind isoliert; Schlüsseldateien bleiben vom Komponenten-Hashinventar ausgeschlossen.

## Runtime-Evidence

Externes Verzeichnis: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/companion`. `client-windows-v1/verification.json` enthält exakte Befehle, Exits, Quell-/Diffhashes und eingefrorene Identitäten; `actual-component-controls.json` enthält rohe Komponentenresultate und Prozessbelege; `fixture-parity.json` enthält die ursprünglichen 1060 Prüfungen; `interrupt-cleanup-v1/fixture-parity-v7.json` enthält die abschließenden 1147 Prüfungen. Das Nachreview `client-windows-v1/interrupt-cleanup-v1/verification.json` enthält das abschließende 40-Test-Ergebnis, neue Quell-/Diffhashes und v7-Identitäten; `real-child-cleanup.json` enthält sechs Vorher-/Nachher-Probes mit echten Kindern einschließlich explizitem Kontrollcleanup für die drei Überlebenden vor der Korrektur. Dies sind Client-/Komponentenmessungen: null HAProxy-Host- oder Native-Engine-Ausführungen und kein Lifecycle-PASS.

Neuer versiegelter Snapshot: `source-fixtures-v7`; alle 88 Dateien besitzen Modus `0444`, beide Verzeichnisse Modus `0555`. Runner-SHA-256: `6a30f2e23126ee91483114819b52389ac58906c5c04cecb28c872b8fcfe09c99`; Ledger-SHA-256: `014ffdb17e3bb3868371ea6a10640af1aab5335408958216511febb1d5cef303`. Die v5/v6/v7-Ledger wurden neu gehasht. Frühere Rawcaptures, v5 und v6 bleiben unverändert. Das erste Paritätsskript wies AST-Unterschiede aus bereits bestehenden Sonar-Refaktorierungen des Cases-Moduls zurück; es bleibt erhalten. Das zweite prüft stattdessen tatsächliche Funktionsausgaben je Fixture und unveränderliche Definitionsbytes. Dieser Task änderte das Modul nicht.

## Bekannte Einschränkungen

Ein gemessenes Intervall belegt allein weder native Ownership, Response-Commit, EOS, Regelausführung noch genau einmaliges Cleanup. Parallele Zuordnungen benötigen weiterhin unabhängige Transaktions-/Handle-/Socketevidence. Ein beendetes Kind kann ohne Abschlussbericht bleiben. Historische Daten mit nur einem Abschlusszeitpunkt bleiben unvollständig. Von 71 Transaktionsdefinitionen sind 49 für Captures vorbereitet; 22 behalten Quell-/Injektionslücken. Das separate Konfigurationsoriginal bleibt Root zugewiesen.

## Verbleibende Risiken

Root muss den neuen Quellsnapshot vor jedem HAProxy-Lauf prüfen und zulassen. Tatsächliche unabhängige Host-Schreib-/Kontextkorrelation, native Ereignisse, Transport und vollständige Lifecycle-Qualifikation bleiben separate Arbeit. Keine kanonische P3-Redirecterwartung wurde auf einen Produktfehlerstatus umgestellt.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser Measurement-Worker führte keinen HAProxy-Host, Native-Engine-Host, Produktbuild, Controllerlauf von `read_spec`, breiten/tiefen Securityscan, keine Sonarübermittlung und keine vollständige CI aus. Root verantwortet Hostscheduling, Qualifikation und Git-Lieferung.

## Finaler Diff- und Review-Status

Nur der zugewiesene Companion-Runner/-Test und dieses EN/DE-Paar wurden geändert. Fokussierte Tests, Fixture-Parität und quellgebundene Kontrollen bestanden; Originalvorhersagen bleiben unverändert. Root-Review, Zulassung, echte Hostresultate und Lieferung stehen aus. Keine Git-Schreiboperation wurde ausgeführt.
