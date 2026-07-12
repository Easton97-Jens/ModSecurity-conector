# HAProxy-Connector

**Sprache:** [English](README.md) | Deutsch

## Common-SDK-Adoptionsgrenze

Die HAProxy-Adoption-Schicht bettet `msconnector_config` ein bzw. mappt darauf und verwendet Common-Direktiven-Specs/-Adapter, Parser-Primitiven, Mapper-Contracts, Header-Helfer, Event-JSONL-Helfer, Rule-ID-/Log-Sanitizing-Primitiven sowie globale Guard-Strukturen, soweit diese Pfade umgesetzt sind. HAProxy-spezifisch bleiben SPOE/SPOP-Protokollhandling, cfg-Glue, Prozess-Lifecycle, Socket-/Runtime-Handling, Frame-Parsing, Return-/Action-Encoding, Logging-Transport und Build-Glue.

C17-Compile-Evidence steht über `make check-haproxy-c17` bereit; optionale C23-/future-C-Prüfungen hängen von der Compiler-Unterstützung ab. Fehlende HAProxy-/libmodsecurity-Header werden als `BLOCKED` mit Exit 77 gemeldet. Dies ist keine Production-, CRS-, Full-Matrix- oder Runtime-Verification.

## Kanonische Grenze für Phase 4

HAProxy verwendet den Repository-eigenen SPOE/SPOP-Agentpfad für Requests und
optionale Response-Header. Der frühere begrenzte Response-Body-Sample-Zweig
brauchte `http-response wait-for-body` und ist bewusst deaktiviert: Ein
wartendes Sample ist keine echte Response-Chunk-API und verletzt den
Low-Latency-Vertrag. `response_body_buffered`, `phase4` und
`phase4_rule_evaluation` sind im gewählten SPOE/SPOP-Pfad daher
`not_implemented`, bis dieser Pfad einen nativen HTX-/Filter-Adapter mit
geliehenen Response-Chunks und einem expliziten End-of-Stream verwendet.
`phase4_pre_commit_deny`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort` und `late_intervention_status_metadata` sind
ebenfalls `not_implemented`.

Der Agent schreibt derzeit policy-abgeleitete Vor-Commit-Felder, doch der
Host-Runner beobachtet keinen beim Client sichtbaren Phase-4-Deny, keinen
tatsächlichen Commit-Zeitpunkt und keinen Antwortpunkt nach dem Commit. Er
implementiert daher weder sicheres `log_only` noch striktes
`abort_connection` und kann keine semantischen Metadaten für ursprünglichen,
angeforderten und sichtbaren Status beanspruchen. Ein Agent-Timeout,
Agentfehler oder allgemeiner HAProxy-Abbruch ist kein Nachweis für einen
Late-Intervention-Abbruch.

Der gemeinsame Phase-4-Fallsatz bleibt nachweisgebunden. Regelauswertung ist
von einem sichtbaren 403 getrennt; die semantischen Fälle für Vor-Commit-Deny,
späte Aktionen und Statusmetadaten bleiben `NOT_EXECUTED`, bis das fehlende
Host-Verhalten implementiert ist. Response-Body-Payloads dürfen nicht in
Ereignisse oder Berichte gelangen.

## Natives HTX-Precommit-Overlay für das Full-Lifecycle-Profil

`htx-overlay/` enthält einen source-gebundenen **HAProxy-3.2.21**-
Observer-Filter für die nativen HTX-Callbacks `http_payload` und `http_end`.
Er wird in einem disposable Upstream-Worktree gebaut. `full-lifecycle-haproxy-htx`
wählt ihn aus; die SPOE/SPOP-Runtime bleibt der getrennte Kompatibilitätspfad:

```sh
make -C connectors/haproxy check-htx-overlay
HAPROXY_HTX_SOURCE_DIR=/pfad/zu/haproxy-3.2.21 \
MODSECURITY_INCLUDE_DIR=/pfad/zu/include \
MODSECURITY_LIB_DIR=/pfad/zu/lib \
BUILD_ROOT=/var/tmp/haproxy-htx-smoke \
make -C connectors/haproxy runtime-smoke-haproxy-htx
```

Der dedizierte HTX-Smoke baut einen gepatchten, disposable HAProxy-3.2.21-
Worktree, lädt die kanonischen No-CRS-Regeln des Frameworks, validiert die
generierte `filter modsecurity-htx`-Konfiguration und sendet echten lokalen
Socket-Traffic. Er belegt einen normalen Upstream-200, kanonische P1-Denys mit
Regel `1100001` (403) und `1100002` (429) sowie einen kanonischen P3-Deny mit
Regel `1100201` (403). Der P3-Fall belegt zusätzlich, dass genau eine
Upstream-Response empfangen wurde, bevor die lokale Antwort sie ersetzte.
Der Overlay übergibt nur aktuelle geliehene `HTX_BLK_DATA`-Slices an das
Binding und finalisiert Phase 4 einmal bei Response-EOS. Er verwendet weder
`wait-for-body`/`res.body` noch einen Connector-eigenen Response-Buffer.
Die Evidence enthält nur begrenzte Metadaten zu Client-Status/-Bytezahl,
Upstream-Anzahl, Transaction-ID, Phase, Regel-ID und Aktion.

P2 (`1100101`) und P4 (`1100301`) werden nur als echte Host-Beobachtungen
ausgeführt: Sie liefern weiter Upstream-200, mit P2
`host_action=observed_only` und dem P4-Safe-Policy-Ergebnis
`host_action=not_attempted`. Der Smoke beansprucht keinen Redirect,
Post-Commit-Abort, First-Byte-Nachweis, keine Common-Runtime-Brücke und keine
Capability-Promotion. Seine Zusammenfassung behält ausdrücklich
`capability_promotion=not_permitted`; die lokale Host-Evidence kann daher nicht
als synthetische kanonische Promotion umgedeutet werden.

Der Overlay ist nicht in der eingecheckten SPOP-Harness-Konfiguration aktiv und
liefert nur nicht-promotete kanonische Host-Evidence. Er stuft daher die
SPOE/SPOP-Capabilities für Phase 4, Late Intervention, No-Buffer oder First
Byte **nicht** hoch.
