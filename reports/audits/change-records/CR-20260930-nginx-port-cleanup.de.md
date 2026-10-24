# NGINX-Cleanup-Port-Prüfung nach Graceful Shutdown

**Sprache:** [English](CR-20260930-nginx-port-cleanup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-nginx-port-cleanup |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `91fce858acea9273d649e0bca1a5c2faadd28f9a` |
| Framework | `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` |
| MRTS | `615b13bacbd008562c17408246c41ab27dca3104` |

## Motivation und Problemstellung

Der Parent-NGINX-Harness konnte einen erfolgreichen Graceful Shutdown als
`port=... result=still_bound` einstufen. Seine Cleanup-Prüfung versuchte nach
dem Ende von NGINX-Master und -Workern einen einfachen IPv4-TCP-Bind. Eine
kürzlich geschlossene lokale Verbindung in `TIME_WAIT` kann diesen Bind mit
`EADDRINUSE` ablehnen, obwohl kein Listener mehr existiert. Ein separater
diagnostischer Replay belegte diesen Mechanismus. Der genaue Socket-Zustand
der zwei früheren Full-E2E-Fehler ist nicht rekonstruierbar, weil deren
private Netzwerk-Namespaces nicht mehr existieren.

## Akzeptanzkriterien

Die Prüfung nach dem Shutdown muss `TIME_WAIT` nur dann akzeptieren, wenn der
TCP-Listener verschwunden ist und ein NGINX-kompatibler Loopback-Bind gelingt.
Ein aktiver lokaler oder fremder Listener, ein belegter HTTP/3-UDP-Port, ein
nicht nutzbarer TCP-Port und Inspektionsfehler müssen weiterhin abgelehnt
werden. Master-, Worker-, PID-, Unix-Socket- und weitere Cleanup-Prüfungen
bleiben erhalten. Ausführbare Socket-Tests und wiederholte echte Cases mit
Root-Master/`nobody`-Worker müssen das Verhalten belegen. Ein vollständiger
Exact-Head-PASS erfordert weiterhin ein frisches Canonical Result und Exit 0.

## Implementierungsentscheidung und Begründung

Nur die Parent-Port-Prüfung **nach dem Shutdown** nutzt den neuen Probe; die
Port-Auswahl vor dem Start bleibt unverändert. Der Probe untersucht
`/proc/net/tcp` in seinem aktuellen Netzwerk-Namespace auf IPv4-Loopback-
und Wildcard-Listener, lehnt `LISTEN` vor dem Bind ab und testet anschließend
`127.0.0.1` mit TCP `SO_REUSEADDR`. Das entspricht dem Verhalten des
NGINX-Listening-Sockets, ohne `SO_REUSEPORT` zu verwenden. HTTP/3 behält die
separate UDP-Bind-Prüfung. Inspektions- und Bind-Fehler bleiben fail-closed.
Eine begrenzte strukturierte Diagnose protokolliert Namespace, Familie,
Adresse, Port, Listener- und `TIME_WAIT`-Anzahl, Bind-Ergebnisse und gegebenenfalls
Errno im Harness-Output und Lifecycle-Log.

## Security-Auswirkung

Die Änderung unterscheidet harmloses `TIME_WAIT` von einem aktiven Listener;
ein fehlgeschlagener Cleanup wird nicht allein wegen beendeter NGINX-Prozesse
als Erfolg gewertet. Fremde Prozess-Listener werden weiter abgelehnt und
nicht beendet. Der Probe nutzt den vom Harness geerbten Namespace; er fügt
keine globale `/tmp`- oder `/var/tmp`-Schreibfreigabe hinzu und lockert weder
Pfadberechtigung, Ownership, Events noch Canonical-Validierung. Framework,
MRTS, Common und Connector-C-Source bleiben unverändert.

## Geänderte Dateien

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_port_cleanup_probe.py`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

Die ausführbare Socket-Regression war auf dem Basis-Harness RED: Der echte
Cleanup-Aufruf lehnte einen Port mit ausschließlich `TIME_WAIT` ab, obwohl ein
Kontroll-TCP-Bind mit `SO_REUSEADDR` gelang; sein alter einfacher Bind
lieferte `EADDRINUSE`. Nach dem Fix bestanden alle 9 Socket-Tests. Sie decken
einen freien Port und den aktuellen Namespace, `TIME_WAIT`, Loopback- und
Wildcard-Listener, einen weiterhin lebenden fremden Prozess-Listener,
HTTP/3-UDP-Belegung, IPv6-only- und Dual-Stack-Listener sowie ungültige
Eingaben ab. Eine fokussierte Parent-Suite mit 90 Tests hatte 89 Erfolge und
einen nur in der Sandbox auftretenden `chown: Invalid argument`-Fehler im
echten Ownership-Test; genau dieser Test bestand mit Host-Rechten. `sh -n`
und `git diff --check` bestanden. ShellCheck meldete dieselben 13 bereits in
der Basis-Revision vorhandenen Findings, keine neuen durch diese Änderung.
Anschließend bestand die vollständige `test_nginx_*.py`-Discovery-Suite mit
Host-Rechten und externem `TMPDIR` alle 446/446 Tests.

```sh
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_nginx_port_cleanup_probe'
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p "test_nginx_*.py" -q'
rtk run -c 'sh -n connectors/nginx/harness/run_nginx_smoke.sh'
rtk run -c 'git diff --check'
```

## Runtime-Evidence

Zwei fokussierte Host-Läufe mit jeweils sechs Invocations endeten mit 0. Der
neueste, nicht-kanonische Lauf liegt unter
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-port-cleanup-focused-20260930T153915Z-1YDTDy`.
Er führte Phase-3-Deny, Phase-4-After-Commit-Abort und Phase-3-Redirect
jeweils zweimal unter `PrivateNetwork=yes` mit Root-NGINX-Master (UID 0) und
`nobody`-Worker (UID 65534) aus. Alle sechs echten Case-Assertions bestanden:
HTTP 403 für die beiden Phase-3-Denies, der erwartete Transport-Abort für die
beiden Phase-4-Cases und HTTP 302 für die beiden Redirects. Jede Invocation
endete mit erfolgreichem Graceful Cleanup; die Diagnose erfasste null
TCP-Listener, einen `TIME_WAIT`-Eintrag und einen erfolgreichen wiederverwendbaren
TCP-Bind auf den Ports 19880–19885. Bei beiden Redirects endeten auch Raw
Client und Curl ohne Redirect-Following mit 0, mit genau einem `Location`-Feld.
Das sind fokussierte Diagnosen, kein kanonisches Full-E2E-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

Ein frisches vollständiges Exact-Head-E2E, die Prüfung von Canonical
Result/Evidence und SHA256SUMS stehen zum jetzigen Review-Zeitpunkt noch aus.
Remote-CI, PR-Checks und Merge wurden nicht beobachtet. Dieser Record
behauptet keinen gesamten `NGINX EXACT-HEAD E2E PASS`.

## Bekannte Einschränkungen

Die historischen privaten Namespaces und deren genaue TCP-Zustände/Errnos
sind verschwunden; die heutige RED-Socket-Reproduktion und fokussierte
Live-Läufe belegen Fehlermöglichkeit und korrigiertes Verhalten, nicht
rückwirkend den Zustand jener Vorfälle. Der Sandbox-`chown`-Fehler der
fokussierten Suite ist eine Einschränkung der Ausführungsumgebung und wird
für jenen Lauf nicht als Erfolg gezählt.

## Verbleibende Risiken

Das vollständig ausgewählte Profil kann nach dem korrigierten Cleanup-Pfad
einen separaten Fehler zeigen. Canonical-Case-Zahlen, Requests, Native Records,
Events, Result, Exitcode und Evidence-Integrität müssen am späteren neuen
Parent-Head geprüft werden, bevor ein Exact-Head-Status erklärt wird.

## Finaler Diff- und Review-Status

Die beabsichtigte Änderung ist auf den Parent-Cleanup-Probe, seine dynamische
Regression und dieses Record-Paar begrenzt. Die fokussierte Validierung ist
vorbehaltlich der genannten Sandbox-Einschränkung grün; abschließende
Dokumentations-, Diff-, Commit-, Full-E2E- und Delivery-Prüfung stehen noch aus.
