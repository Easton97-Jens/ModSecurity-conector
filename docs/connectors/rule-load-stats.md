# Rule Load Stats Metadata

Status: current adapter-owned Apache and NGINX code

This document records the common rule-load statistics metadata shared by the
Apache and NGINX connectors. It describes observable metadata only. The stats do
not change rules loading, rules merging, request handling, response handling, or
any runtime decision.

## Common Structure

`common/include/msconnector/rule_load_stats.h` defines
`msconnector_rule_load_stats` with these fields:

| Field | Meaning |
| --- | --- |
| `inline_rules` | Number of rules loaded from inline `modsecurity_rules` content |
| `file_rules` | Number of rules loaded from rule files |
| `remote_rules` | Number of rules loaded from remote rule loads |

The values count loaded rules, not directive invocations. `file_rules` counts
rules loaded from rule files; it does not count the number of files. The
structure contains no Apache types, no NGINX types, no libmodsecurity ownership
objects, and no runtime callbacks.

## Semantics

Rule-load stats are metadata. They are increased only after successful
`msc_rules_add*` calls, using the existing libmodsecurity return values already
used by each connector. Failed load attempts keep the existing error path and do
not increase the counters.

No connector uses these stats to decide whether a request should be processed,
blocked, logged, or inspected. NGINX exposes the values through its existing
startup log. Apache currently keeps the values as internal config metadata only.

## Reporting Status

NGINX reports rule-load stats through its existing startup log. The connector
uses the common stats helper internally, but the log text, format, level, and
ordering remain the existing NGINX behavior.

Apache stores rule-load stats as metadata in `msc_conf_t`. It does not currently
report these values in the post-config log. Apache reporting is deferred until
the aggregation source and merge semantics for display are explicitly defined.

`msconnector_rule_load_stats` is a data shape only. There is no common reporting
API for these values yet.

## Apache

Apache stores `msconnector_rule_load_stats` in `msc_conf_t`.

The Apache parser paths update the stats only after successful rules loading:

- inline rules add to `inline_rules`;
- rules loaded from files add to `file_rules`;
- remote rules add to `remote_rules`.

Apache directory config merge adds parent and child stats as metadata. It does
not use `msc_rules_merge()` return values as counters, and it does not change
the RulesSet merge behavior.

No Apache runtime path reads the stats. Hooks, filters, bucket brigades,
intervention handling, transaction ownership, request body handling, and
response body handling are unchanged.

## NGINX

NGINX keeps its existing local counters:

- `rules_inline`
- `rules_file`
- `rules_remote`

A small adapter helper copies those values into `msconnector_rule_load_stats`.
The local `ngx_uint_t` fields remain the source used by the current NGINX
connector. The existing startup log reads the values through the helper without
changing the log text, format, level, or ordering. The helper does not change
rules loading, config merge, init behavior, PCRE allocator behavior, RulesSet
ownership, or error handling.

## Non-goals

The rule-load stats metadata does not change:

- RulesSet ownership or lifetime;
- `msc_rules_merge()` semantics;
- PCRE allocator behavior;
- rules-loading error paths;
- request body or response body lifecycle;
- phase-4 behavior;
- hooks or filters;
- bucket brigades;
- intervention runtime behavior.

## Deferred

The following work is intentionally deferred:

- common reporting for rule-load stats;
- Apache post-config reporting;
- shared metadata logging;
- test-result or audit-log evaluation of the stats;
- capability reports that include rule-load counts;
- any runtime use of the counters.
