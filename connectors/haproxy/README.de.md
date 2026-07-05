# HAProxy Connector

**Sprache:** [English](README.md) | Deutsch

## Common-SDK-Adoptionsgrenze

Die HAProxy-Adoption-Schicht bettet `msconnector_config` ein bzw. mappt darauf und verwendet Common-Direktiven-Specs/-Adapter, Parser-Primitiven, Mapper-Contracts, Header-Helfer, Event-JSONL-Helfer, Rule-ID-/Log-Sanitizing-Primitiven sowie globale Guard-Strukturen, soweit diese Pfade umgesetzt sind. HAProxy-spezifisch bleiben SPOE/SPOP-Protokollhandling, cfg-Glue, Prozess-Lifecycle, Socket-/Runtime-Handling, Frame-Parsing, Return-/Action-Encoding, Logging-Transport und Build-Glue.

C17-Compile-Evidence steht über `make check-haproxy-c17` bereit; optionale C23-/future-C-Prüfungen hängen von der Compiler-Unterstützung ab. Fehlende HAProxy-/libmodsecurity-Header werden als `BLOCKED` mit Exit 77 gemeldet. Dies ist keine Production-, CRS-, Full-Matrix- oder Runtime-Verification.
