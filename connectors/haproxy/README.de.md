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

## Optionales natives HTX-Observer-Overlay

`htx-overlay/` enthält einen source-gebundenen **HAProxy-3.2.21**-
Observer-Filter für die nativen HTX-Callbacks `http_payload` und `http_end`.
Er wird in einem disposable Upstream-Worktree gebaut und nicht in die gewählte
SPOE/SPOP-Runtime eingebunden:

```sh
make -C connectors/haproxy check-htx-overlay
HAPROXY_HTX_SOURCE_DIR=/pfad/zu/haproxy-3.2.21 \
HAPROXY_HTX_BUILD_DIR=/var/tmp/haproxy-htx-overlay \
MODSECURITY_INCLUDE_DIR=/pfad/zu/include \
MODSECURITY_LIB_DIR=/pfad/zu/lib \
make -C connectors/haproxy build-htx-overlay
```

Der Overlay übergibt nur aktuelle geliehene `HTX_BLK_DATA`-Slices an das
Binding und finalisiert Phase 4 einmal bei Response-EOS. Er verwendet weder
`wait-for-body`/`res.body` noch einen Connector-eigenen Response-Buffer.
Nach dem Response-Commit bleibt er absichtlich observer-only: Eine späte Regel
wird geloggt, aber nicht als erfundener Deny, Redirect oder Abort umgesetzt.
Wegen der noch atomischen Request-Body-Phase des Bindings ist dieser
experimentelle Pfad zudem auf bodylose Requests beschränkt.

Der optionale Overlay ist nicht in der eingecheckten SPOP-Harness-Konfiguration
aktiv und keine kanonische No-CRS-Evidence. Er stuft daher die ausgewählten
SPOE/SPOP-Capabilities für Phase 4, Late Intervention, No-Buffer oder First
Byte **nicht** hoch.
