# Safe-Policy für den synchronisierten NGINX-First-Byte-Beweis

**Sprache:** [English](CR-20260927-nginx-first-byte-safe.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260927-nginx-first-byte-safe |
| Datum (UTC) | 2026-09-27 |
| Basis-Revision | `1bf1dcd46d25ba5b22f8a7d5915b5f72b4daa4da` |

## Motivation und Problemstellung

Die portable First-Byte-Fixture materialisiert einen leeren Host-Modus. Der
Parent erwartet vollständiges Safe-Streaming, führte bisher aber Default Off
aus: alle 44 Nutzbytes wurden mit unvollständigem Chunked-Framing und curl-
Exit 18 empfangen.

## Akzeptanzkriterien

Die explizite synchronisierte Safe-Policy übersteht das Laden der Case-Umgebung;
fehlende/ungültige/Off-/Strict-Auswahl wird vor dem Start abgewiesen. Direkter
Default Off und normale Fixture-Modi bleiben unverändert. Der echte native
Beweis verlangt HTTP200, 44 Bytes, vollständige Chunked-Terminierung, curl0,
kausales First Byte vor EOS, native Regel1100301 und eine nicht abgebrochene
späte Safe-Beobachtung.

## Implementierungsentscheidung und Begründung

Der Caller wählt `NGINX_SYNCHRONIZED_PHASE4_MODE=safe` nur für NGINX. Der Harness
sichert den Wert readonly und wendet das validierte Literal nach dem Case-Load
an. Der bestehende Log-Scope `server_with_location_override` liefert den vom
First-Byte-Produzenten konsumierten nativen Phase4-Sink. Keine Änderungen an
Connector-C, Common, Framework, MRTS, Regeln, Serializer, Canonical-Auswertung
oder frühen/Allow-Events.

## Security-Auswirkung

Kein eval von Policy-Input; ausschließlich exakter Safe-Enum-Wert. Ein Override
außerhalb seiner Route wird fail-closed abgewiesen. Bestehende root/nobody-
Trennung, Pfadautorität, Projection-Freshness, Private-Network-Laufzeit und
curl-/Fehler-Guards bleiben unverändert. Technische Fehler bleiben terminal;
Regel1100301 bleibt deny.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-native-first-byte.sh`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_synchronized_phase4_policy.py`
- `connectors/nginx/README.md` / `README.de.md`
- Dieses Change-Record-Paar.

## Ausgeführte Befehle

Der rote Regressionstest lief vor dem Fix mit unverändertem Produktionscode
und zeigte die fehlende Caller-/Post-Load-Bindung. Fokussiert: `python3 -m
unittest tests.test_nginx_synchronized_phase4_policy -v`: 11 PASS, inklusive
Readonly-Tamper-Abweisung, bösartiger/fehlender/Strict-Werte und FAIL für
vollständige44/HTTP200/curl18. Framework
`tests/security_regression/test_synchronized_upstream_security_boundaries.py`:
8 PASS, Framework unverändert. Alle Befehle RTK-wrapped, externer TMPDIR.
Breitere Parent-Suite mit 17 Modulen: 248 PASS, keine Skips. Finaler
Fokus-/Runner-Wiring-Rerun: 17 PASS. Syntax PASS; ShellCheck hat dieselben 20
bestehenden Diagnosen wie die Basis, ohne Ergänzungen. Bilinguale Dokumentation,
Repository-Pfadreferenzen und Dokumentationslinks bestanden.

```sh
rtk run -c 'python3 -m unittest tests.test_nginx_synchronized_phase4_policy tests.test_nginx_phase4_runner_wiring -v'
rtk run -c 'sh -n ci/runtime/lifecycle/run-native-first-byte.sh connectors/nginx/harness/run_nginx_smoke.sh'
rtk run -c 'make check-bilingual-docs check-doc-links'
rtk run -c 'git diff --check'
```

Die tatsächlichen Testaufrufe binden externen TMPDIR, deaktivieren Bytecode-
Writes und wählen das exakt gepinnte Framework; detaillierte Logs liegen in
externer Run-Evidence.

## Runtime-Evidence

Isolierter nativer Pre-Commit-Beweis unter
`/var/tmp/codex/nginx-first-byte-safe-20260927T165747Z`: Safe nach leerem case.env
gerendert; HTTP200, 44/44 Bytes, 23+33+5 Chunked-Framing-Bytes (terminaler Null-
Chunk), curl0 und nativer Wrapper0. Regel1100301: requested deny, actual
log_only, visible200, nicht abgebrochen. Client-Transport `http_status`;
bestehender nativer Event-Transport-Enum `log_only`, bewusst unverändert.
Real-Host-Barriere und No-Full-Buffering-Evidence PASS; root/nobody, 16
Preflights, sauberes Herunterfahren.

## Nicht ausgeführte Prüfungen mit Begründung

Der neue Exact-Head-Full-E2E ist bis nach separatem Commit und allen
Vorprüfungen zurückgestellt. Keine neue CRS-/MRTS-/H2-/H3-Matrix, Sonar,
Remote-CI, Push oder Merge.

## Bekannte Einschränkungen

Allow-/Early-Event-Emission-/Collection-Defekte bleiben separat. Isoliertes
PASS beweist kein vollständiges Canonical-E2E-PASS. Framework bleibt auf
`cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`, MRTS auf
`615b13bacbd008562c17408246c41ab27dca3104` gepinnt.

## Verbleibende Risiken

Nur dieser synchronisierte Beweis ändert die Policy-Auswahl. Echte Fehler
dürfen nicht als erfolgreiche Safe-Behandlung umklassifiziert werden.
Bestehende Transport-/Event-Assertions werden nicht gelockert; native und
Client-Transportfelder bleiben getrennt.

## Finaler Diff- und Review-Status

Fokussierte Regression, breitere Tests, isolierter Beweis, Dokumentation und
finale Diff-Checks vor dem Commit verifiziert. Finaler Run-/Delivery-Status
gehört in externe Run-Evidence, nicht in einen erfundenen Pre-Commit-E2E-PASS.
