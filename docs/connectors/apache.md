# Apache Connector

**Language:** English | [Deutsch](apache.de.md)

## Overview

Apache uses the selected <code>native-httpd-module</code> route: an Apache HTTPD
module built through APXS and bound to libmodsecurity v3 public APIs. This guide
describes the selected HTTP/1.1 P1--P4 core only. It does not claim production
readiness, CRS verification, complete HTTP/2/HTTP/3 coverage, a complete
matrix, or strict verification for every phase.

## Architecture and ownership

Productive source is under <code>connectors/apache/src/</code>; Autotools/APXS
inputs and host-specific build glue remain under <code>connectors/apache/</code>.
Apache owns configuration hooks and merge, request hooks, input/output filters,
log-transaction handling, bucket brigades, APR lifetimes, and host intervention
mapping. Common supplies connector-neutral configuration, parser, mapper, rule
metadata, and payload-safe event primitives; it does not own Apache objects.

| Lifecycle area | Selected Apache responsibility | Boundary |
| --- | --- | --- |
| P1/P2 | Map request metadata and process request bodies through the input path | Finalize request-body processing at EOS |
| P3 | Map response headers before the committed response boundary | Preserve original and visible status context |
| P4 | Ingest current output buckets incrementally and finalize at EOS | No connector-owned cross-call full response buffer |
| Logging | Emit metadata-only events and release transaction state | Event payloads do not contain response bodies |

## Build

Use [the Apache compiler guide](../build/compilers/apache.md) for APXS,
libmodsecurity discovery, build roots, toolchain prerequisites, and
troubleshooting. Build and config-load success are distinct from traffic
execution. Code-local source ownership and narrow harness notes remain in
[the Apache source guide](../../connectors/apache/README.md).

## Configuration

Apache host directives are registered by the module and differ from
ModSecurity Engine directives. The complete source-backed syntax, defaults,
contexts, merge rules, examples, and validation notes are in the
[Apache configuration reference](../../examples/apache/configuration-reference.md).

Use Minimal, Safe, Strict, DetectionOnly, and Disabled profiles only for their
documented purpose. <code>SecRuleEngine</code> is an engine setting, not the
same as the Apache connector enable/disable directive.

## P1--P4 lifecycle and late behavior

The native module processes P1 through P4 on its host hooks and filters.
P3 can act before the response is committed when the selected case and host
state permit it. P4 is different: Safe behavior after commitment is recorded
conservatively as metadata and must preserve the actual visible outcome.
Strict source wiring is not proof of a client-visible abort.

| P4 question | Required observation |
| --- | --- |
| Rule observed | Real host phase-4 rule observation with the selected rule/profile |
| Pre-commit deny | Requested deny, uncommitted headers, and matching visible status |
| Safe late result | Requested action, actual <code>log_only</code>, unchanged visible status, and late flag |
| Strict late result | Actual abort action and host/client evidence of the recorded abort |

## Testing and evidence

Use <code>make check-config-apache</code> for the selected configuration and
<code>make full-lifecycle-apache</code> for a selected lifecycle run. Inspect
the run-scoped result, assertion, host-log, and metadata-only phase event
artifacts rather than inferring runtime behavior from source or a build.

The shared test model, status vocabulary, privacy rules, and aggregate
boundaries are in [Testing and evidence](../testing-and-evidence.md).

## Operations and troubleshooting

Run Apache with an explicit external build/runtime/evidence root and protect
host logs and rule inputs. For a config failure, first inspect APXS and
libmodsecurity discovery plus the selected config-check output. For a P4
question, inspect the phase event and commit/EOS context before interpreting an
HTTP status.

## Limitations and compatibility

Apache v2-style names are not automatically native Apache v3 connector
directives. Use the registered module syntax and the complete reference rather
than assuming a legacy directive, merge rule, or expression is portable. P4
response-body and post-commit behavior remain evidence-gated; a rule match,
source branch, or historical matrix is not a promotion.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [Apache configuration reference](../../examples/apache/configuration-reference.md)
