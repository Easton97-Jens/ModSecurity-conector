# HAProxy-Connector

**Sprache:** [English](README.md) | Deutsch

## Common-SDK-Adoptionsgrenze

Die HAProxy-Adoption-Schicht bettet `msconnector_config` ein bzw. mappt darauf und verwendet Common-Direktiven-Specs/-Adapter, Parser-Primitiven, Mapper-Contracts, Header-Helfer, Event-JSONL-Helfer, Rule-ID-/Log-Sanitizing-Primitiven sowie globale Guard-Strukturen, soweit diese Pfade umgesetzt sind. HAProxy-spezifisch bleiben SPOE/SPOP-Protokollhandling, cfg-Glue, Prozess-Lifecycle, Socket-/Runtime-Handling, Frame-Parsing, Return-/Action-Encoding, Logging-Transport und Build-Glue.

C17-Compile-Evidence steht über `make check-haproxy-c17` bereit; optionale C23-/future-C-Prüfungen hängen von der Compiler-Unterstützung ab. Fehlende HAProxy-/libmodsecurity-Header werden als `BLOCKED` mit Exit 77 gemeldet. Dies ist keine Production-, CRS-, Full-Matrix- oder Runtime-Verification.

## Kanonische Grenze für Phase 4

HAProxy verwendet den Repository-eigenen SPOE/SPOP-Agentpfad mit einem
begrenzten experimentellen Response-Body-Zweig. Die Quellverdrahtung allein
belegt weder, dass der Agent eine vollständige Upstream-Antwort sieht, noch,
dass HAProxy deren Status noch ändern kann oder dass ein Verbindungsabbruch
eine Phase-4-Aktion statt eines Agentfehlers ist. Nur
`response_body_buffered`, `phase4` und `phase4_rule_evaluation` bleiben als
Quellpfade `implemented_not_asserted`. `phase4_pre_commit_deny`,
`late_intervention`, `late_intervention_log_only`, `late_intervention_abort`
und `late_intervention_status_metadata` sind `not_implemented`.

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
