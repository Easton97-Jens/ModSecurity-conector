# Common example configuration reference

**Language:** English | [Deutsch](README.de.md)

This central reference separates four layers: host/connector configuration, Common Runtime, ModSecurity Engine, and example placeholders. The six connector references link here without presenting Common keys as unregistered host directives.

| Material | Layer | Purpose |
| --- | --- | --- |
| [Common Runtime](common-connector-configuration.md) | Common Runtime | Complete current `key=value` parser options. |
| [ModSecurity Engine](modsecurity-directives.md) | ModSecurity Engine | `Sec*` directives actually used by example rule files. |
| [Rule examples](rule-examples.md) | ModSecurity Engine | On, DetectionOnly, Off, plus P1/P4 explanation. |
| [Central variables reference](../../docs/reference/variables.md) | Environment/runtime | Repository and harness variables. |

## Environment and runtime values

`BUILD_ROOT`, `NO_CRS_RUN_ID`, `EVIDENCE_ROOT`, `CACHE_ROOT`, and connector-specific materializer inputs belong to runtime/CI, not host directives. The Envoy template materializer uses the explicitly documented `@...@` placeholders; generated files must remain outside the checkout.
