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
| P4 | Append data buckets incrementally, retain the normalized response through first EOS, then finalize once | Apache-owned request-pool all-response gate; no original byte is released before the Phase-4 decision |
| Logging | Emit metadata-only events and release transaction state | Event payloads do not contain response bodies |

Each successfully created native <code>Transaction</code> is owned by the
primary Apache request that created it. The adapter publishes it only after
creation succeeds, registers normal cleanup on that request's
<code>r-&gt;pool</code>, and clears the owner note and native pointer before
<code>msc_transaction_cleanup</code> runs. This is a source-level lifecycle
contract, not runtime evidence. Separate top-level requests on a keepalive
connection receive separate request pools and transactions. Subrequests retain
their existing deliberate reuse of the primary context. Normal internal
redirects and pre-output ErrorDocuments fail closed: the transaction cannot
safely be rebound from the source URI, headers, and body to a target request
through the public libModSecurity C API. The only exception is one synchronous,
Apache-core-marked local ErrorDocument hop while the terminal output guard is
<code>EMITTING</code>, with the Apache <code>no_local_copy</code> marker and a
matching immediate predecessor status/<code>REDIRECT_STATUS</code>; the guard
rejects a second hop.

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

The native module processes P1 through P4 on its host hooks and filters. P3 can
act before the response is committed when the selected case and host state
permit it. P4 is an EOS-only all-response gate: every normalized response
brigade, including an empty response's EOS, stays in the Apache request pool
until <code>msc_process_response_body</code> and intervention resolution are
complete. This permits a normal Phase-4 deny to discard the saved original
brigade and emit one terminal error before original output is released. It also
means the selected Apache path deliberately does not provide client-visible
progressive response streaming.

The C API does not expose a safe answer to libModSecurity's effective
<code>SecResponseBodyMimeType</code> selection. Apache therefore gates every
response MIME type; the engine directive still selects inspection, but the
deprecated <code>modsecurity_phase4_content_types_file</code> cannot open a
pass-through route. The connector default is a 1048576-byte (1 MiB) hard limit;
an over-limit response fails closed before its original bytes are released.
<code>r-&gt;sent_bodyct</code> and <code>eos_sent</code> are not used as commit
proof because upstream/core paths can set them before this filter releases
output. The gate uses its own released-EOS marker and Apache
<code>r-&gt;bytes_sent</code> instead.

Safe/minimal <code>log_only</code> and strict
<code>abort_connection</code> remain defensive fallbacks only for an
independently proven already-committed response. They do not change a normal
still-gated deny into log-only. Source wiring for a strict fallback remains no
proof of a client-visible abort.

| P4 question | Required observation |
| --- | --- |
| Rule observed | Real host phase-4 rule observation with the selected rule/profile |
| Pre-commit deny | Requested deny, no released original EOS/bytes, matching visible terminal status, and no original body output |
| Safe late result | Requested action, actual <code>log_only</code>, unchanged visible status, and late flag |
| Strict late result | Actual abort action and host/client evidence of the recorded abort |

## Testing and evidence

Use <code>make check-config-apache</code> for the selected configuration and
<code>make full-lifecycle-apache</code> for a selected lifecycle run. Inspect
the run-scoped result, assertion, host-log, and metadata-only phase event
artifacts rather than inferring runtime behavior from source or a build. The
focused H1/H2 evidence placeholder is
<code>ci/runtime/lifecycle/run-apache-phase4-response-regression.sh</code>;
record its run-scoped output only after execution. This guide does not claim an
H1 or H2 pass merely because the source contract or runner exists.

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
source branch, or historical matrix is not a promotion. The Apache all-response
gate is intentional compatibility behavior for this security boundary, not a
generic connector buffering model.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [Apache configuration reference](../../examples/apache/configuration-reference.md)
