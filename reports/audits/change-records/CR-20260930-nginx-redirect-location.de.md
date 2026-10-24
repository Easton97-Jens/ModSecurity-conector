# NGINX-Redirect: Location ersetzen

**Sprache:** [English](CR-20260930-nginx-redirect-location.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-nginx-redirect-location |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `0fe4c7b8cf4b021663985d895064e56cd2c63410` |
| Framework | `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` |
| MRTS | `615b13bacbd008562c17408246c41ab27dca3104` |

## Motivation und Problemstellung

Der gepinnte NGINX-Phase-3-Redirect-Case lieferte zwei aktive `Location`-Felder;
der Curl-Request ohne Redirect-Following endete daher mit Exit 8 und
`Multiple Location headers`. Die Parent-Response-Header-Fixture lieferte
`/encoded%2Ftarget`, die ModSecurity-Regel
`https://no-crs.invalid/phase3-redirect`. NGINX behielt das relative
Upstream-Feld in seiner Ausgabeliste, ohne es unter `headers_out.location` zu
indexieren. Der Connector löschte vor seinem eigenen Redirect nur diesen
Pointer. Dies ist von zwei historischen Port-Cleanup-Fehlern getrennt.

## Akzeptanzkriterien

Ein akzeptierter Connector-eigener Redirect ersetzt jedes ältere aktive
`Location`-Feld und gibt genau sein validiertes Ziel einmal aus. Gewöhnliche
Upstream-Antworten, reine Status-Interventions, andere Header, wiederholte
Redirects und die Ablehnung ungültiger oder bereits gesendeter Redirects
bleiben erhalten. Eine ausführbare RED/GREEN-Regression und ein echter
Request mit Root-Master/`nobody`-Worker belegen die Änderung. Ein gesamter
Exact-Head-PASS benötigt später Canonical Result und Exit 0.

## Implementierungsentscheidung und Begründung

Nur der Parent-Connector-Redirect-Helper wird geändert. Nach erfolgreicher
Allokation seines neuen Headers behält er `ngx_http_clear_location` bei und
deaktiviert ältere aktive, ohne Beachtung der Großschreibung erkannte
`Location`-Einträge in allen Teilen der NGINX-Ausgabeliste. Andere Header,
reine Status-Interventions, Framework, MRTS, Common, Event-Verträge und die
separate Cleanup-Prüfung bleiben unverändert. Der bestehende Redirect-Vertrag
in den EN/DE-Connector-READMEs bleibt zutreffend.

## Security-Auswirkung

Das Entfernen widersprüchlicher älterer `Location`-Felder verhindert
mehrdeutige Redirect-Ziele an der HTTP-Client-Grenze. Bestehende URL-Prüfung,
CR/LF-Ablehnung, Header-Sent-Guard und NGINX-Pfad-/Eigentümerprüfungen bleiben
unverändert. Die isolierte Runtime nutzte `PrivateNetwork=yes`, ein frisches
direktes root-owned Docroot-Projection-Kind und einen Root-Master mit
`nobody`-Worker.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `tests/test_nginx_redirect_location.py`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

Die tatsächlichen C-Redirect- und Status-Helper wurden mit `-std=c17 -Wall
-Wextra -Werror` in einer begrenzten NGINX-Header-Listen-Fixture kompiliert.
Vor dem Sourcefix zeigten vier Teilfälle zwei oder drei aktive
`Location`-Felder; danach bestanden alle acht Tests. Fokussierte Parent-Suiten
bestanden mit Host-Rechten 98/98 und für First-Byte-, Phase-4-, Collector-
und Worker-Verträge 96/96. Der erste Sandbox-Lauf der 98 Tests hatte einen
`chown: Invalid argument`-Fehler; die identische Suite bestand bei Wiederholung
mit Host-Rechten. Relevante Shell-Syntax und ShellCheck der task-lokalen
Skripte bestanden; unveränderte Parent-Shell-Dateien behalten vorhandene
ShellCheck-Diagnosen. `make build-nginx` endete mit Exit 0 gegen den gepinnten
Source-Stand und erzeugte ein Cache-v2-Manifest, dessen unabhängig geprüfter
Source-Hash zum Worktree passte.

```sh
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_nginx_redirect_location'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/build-nginx-redirect-fix.sh'
rtk run -c 'make FRAMEWORK_ROOT=/var/tmp/codex/worktrees/nginx-p3-redirect-location-20260930/modules/ModSecurity-test-Framework check-bilingual-docs check-doc-links check-no-crs-doc-consistency'
rtk run -c 'git diff --check'
```

## Runtime-Evidence

Der erhaltene RED-Replay unter
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-redirect-red-20260930T124227Z-50Zvn9`
erfasste HTTP 302 mit beiden `Location`-Feldern, Curl-Exit 8 und Collector-
Exit 0. Zwei frische GREEN-Replays nutzten das neu gebaute Modul und lieferten
HTTP 302 mit genau einem `Location`:
`https://no-crs.invalid/phase3-redirect`. Raw Client, ursprüngliches Curl
ohne Redirect-Following, Case-Assertion und nativer Collector endeten mit 0.
Der zweite Replay liegt unter
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-redirect-green-20260930T140030Z-t9x93A`.
Sein Harness endete wegen des getrennten Cleanup-Fehlers
`port=19889 result=still_bound` weiterhin mit 1. Nach Graceful Quit und
Prozessende gab es keinen Listener, aber der private Namespace zeigte
`TIME-WAIT`. Der Probe-Bind ohne `SO_REUSEADDR` scheiterte mit `EADDRINUSE`
(Errno 98); derselbe Bind mit `SO_REUSEADDR` gelang. Kein Cleanup-Fehler
wurde als PASS umgedeutet.

## Nicht ausgeführte Prüfungen mit Begründung

Der frische Exact-Head-Full-E2E folgt auf diesen separaten Commit. Remote-CI,
Push, PR, Merge, Framework-/MRTS-Änderungen und ein Cleanup-Sourcefix sind
außerhalb dieser Änderung. Aus dem isolierten Redirect-Case wird kein
vollständiger Canonical-PASS behauptet.

## Bekannte Einschränkungen

Die historischen Cleanup-Namespaces existieren nicht mehr; ihre genauen
Socket-Zustände und Errnos lassen sich nicht rekonstruieren. Die heutige
Reproduktion beweist einen Cleanup-False-Positive-Mechanismus, nicht den
genauen Zustand beider alten Vorfälle. Das vollständig ausgewählte Profil
kann weiterhin durch Cleanup vor Abschluss aller Requests stoppen.

## Verbleibende Risiken

Canonical-Zahlen, Event-Vollständigkeit und Lifecycle-Exit müssen am neuen
exakten Parent-Head geprüft werden. Bleibt der Fehler bestehen, benötigt der
Cleanup-Probe einen eigenen separat abgegrenzten Fix mit Regression. Weder
Containment noch Validator oder Port-Prüfung werden hier abgeschwächt.

## Finaler Diff- und Review-Status

Der geplante Commit enthält nur den Parent-Redirect-Helper, seine ausführbare
Regression und dieses Record-Paar. Abschließende Dokumentations-, Diff-,
Commit- und Exact-Head-Evidence sind vor jedem gesamten E2E-Status zu prüfen.
