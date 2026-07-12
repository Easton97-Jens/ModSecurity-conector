# Evidence documentation

**Language:** English | [Deutsch](README.de.md)

Evidence is the run-scoped record used to support a specific test observation.
It is not a durable assurance outside its selected host profile, rules,
connector, and run ID. This documentation makes no production, CRS, HTTP/2,
HTTP/3, complete-matrix, or strict-for-all-connectors claim.

## Evidence location and placeholders

Canonical No-CRS evidence is organized conceptually as:

~~~text
<evidence-root>/<connector>/<run-id>/
~~~

<code>&lt;evidence-root&gt;</code> is an absolute writable evidence parent,
such as <code>/srv/modsecurity-work/evidence/no-crs-evidence</code>. It is not
the literal text <code>&lt;evidence-root&gt;</code>, the repository checkout,
or a secret-bearing directory.

<code>&lt;connector&gt;</code> is exactly one of <code>apache</code>,
<code>nginx</code>, <code>haproxy</code>, <code>envoy</code>,
<code>traefik</code>, or <code>lighttpd</code>. It names the connector whose
selected host route produced the artifacts.

<code>&lt;run-id&gt;</code> is a 1–128 character filesystem-safe token that
starts with an ASCII letter or digit and otherwise uses only letters, digits,
<code>.</code>, <code>_</code>, and <code>-</code>. Example:
<code>six-core-20260712T120000Z</code>. It must not contain secrets, personal
data, slashes, or traversal segments.

The root variable <code>EVIDENCE_ROOT</code> defaults to
<code>VERIFIED_EVIDENCE_ROOT/no-crs-evidence</code>. The parent root is an
absolute evidence path once derived. For full format, setter, scope, and
safety requirements, see
[configuration variables](../configuration/variables.md#no-crs-and-evidence-variables).

## Canonical artifact layout

The validator and Framework schemas are authoritative. A finalized canonical
run normally contains the following artifact roles; an artifact may be absent
when the selected profile does not produce the corresponding supported
observation, in which case the manifest/status must say so rather than invent
data.

| Relative path | Role | Data sensitivity / interpretation |
|---|---|---|
| <code>result.json</code> | Aggregate result and run identity | Read as a summary, not as proof of unlisted cases |
| <code>results.jsonl</code> | One canonical case result per JSONL line | Contains outcome metadata; must not contain request/response body payloads |
| <code>events.jsonl</code> | Canonical event records | Metadata-only event evidence; redact/avoid secrets and body payloads |
| <code>plan.json</code> | Capability-selected case plan | Explains selected/omitted cases; selection alone is not execution |
| <code>manifest.json</code> | Artifact inventory and identity | Links produced/missing artifacts to the run |
| <code>inventory/run.json</code> | Run inventory/provenance | Identifies the selected run inputs |
| <code>inventory/first-byte-evidence.json</code> | First-byte observation input | Required when an applicable first-byte case is promoted |
| <code>inventory/barrier-events.jsonl</code> | Synchronized barrier event records | Required by checks that need causal first-byte/EOS ordering |
| <code>effective-config/manifest.json</code> | Effective configuration inventory | Records what configuration was actually used; review it for sensitive values |

Raw host logs, build trees, and temporary files are not automatically
canonical evidence just because they exist below a runtime root. The lifecycle
wrapper sanitizes/normalizes data before finalization; keep raw data outside
the tracked checkout and do not copy secrets into canonical files.

## Evidence targets

| Target | Purpose | Required input | Result and boundary |
|---|---|---|---|
| <code>make no-crs-baseline-<connector></code> | Produces candidate baseline evidence for one selected connector | Rules, safe runtime paths, selected profile capabilities | Candidate artifacts; not CRS or all-protocol evidence |
| <code>make full-lifecycle-<connector></code> | Produces candidate artifacts for one selected full-lifecycle route | Target-owned profile identity and normal No-CRS inputs | Candidate full-lifecycle run; target name cannot relabel another route |
| <code>make full-lifecycle-all-connectors</code> | Runs all six selected routes | Component prerequisites; <code>NO_CRS_RUN_ID</code> recommended | Candidate run per connector; no broad assurance |
| <code>make evidence-check-<connector></code> | Validates existing evidence for one connector | <code>EVIDENCE_ROOT</code>, run ID or latest marker | Read-only validation; does not rerun a host |
| <code>make evidence-check-all-connectors</code> | Validates existing evidence across the configured connector set | Same, plus <code>NO_CRS_CONNECTORS</code> | Aggregate validation only |
| <code>make check-first-byte-before-response-end</code> | Checks first-byte-before-EOS evidence | Explicit <code>NO_CRS_RUN_ID</code> and full-lifecycle artifacts | Requires synchronized causal artifacts |
| <code>make check-no-full-response-buffering</code> | Checks the no-full-response-buffering condition | Explicit run ID and full-lifecycle artifacts | Does not infer the property from a configuration value |
| <code>make check-full-lifecycle-event-privacy</code> | Checks event privacy constraints | Explicit run ID and canonical events | Confirms checker conditions, not host security generally |
| <code>make check-full-lifecycle-promotion</code> | Applies promotion-related evidence checks | Explicit run ID and selected artifacts | Does not upgrade unexecuted/unsupported capabilities |
| <code>make check-six-connector-core-completion</code> | Read-only six-connector completion gate | Explicit run ID and finalized canonical evidence | A successful process exit is limited to this gate’s contract |

The placeholder <code>&lt;connector&gt;</code> has the six values listed above.
For example:

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make evidence-check-nginx
~~~

This validates the NGINX evidence directory for that run ID or reports a
missing/invalid input. It does not execute NGINX again or change its capability
manifest.

## Promotion and limits

Promotion is an evidence-gated conclusion, not a file copy. It ties the
selected integration mode, case ID, rule ID where applicable, result status,
event metadata, and required causal/transport artifacts to the same run.

| Observation | Evidence needed | Not sufficient |
|---|---|---|
| P1/P2/P3/P4 case result | Matching canonical result record and required event fields | A rule file, source code, or a host build |
| Safe late intervention | Requested/actual action, commit/status metadata, and matching event/result | The word <code>safe</code> in configuration |
| Strict late abort | Host-visible, causal artifacts for the selected strict route | A strict policy name, gRPC failure, or source branch |
| First Byte Before EOS | Synchronized first-byte, barrier, and transport evidence | A completed HTTP response or a timestamp without causal ordering |
| No Full Response Buffering | Required source/runtime evidence and checker conditions | A body-limit directive or absence of an obvious buffer file |
| Event privacy | Canonical event records without body payloads/secrets plus privacy check | Assuming logs are safe because they are JSONL |

The No-CRS rule IDs in the <code>1100000</code> range are repository baseline
IDs, not OWASP CRS IDs. Rule/case details and status meanings are in
[configuration variables](../configuration/variables.md#rule-ids-and-representative-case-ids)
and [Testing](../testing/README.md).

## Status and validation

<code>PASS</code> means a specific artifact-backed case/check met its declared
conditions. <code>FAIL</code> means it did not. <code>BLOCKED</code> means a
prerequisite is missing; <code>NOT EXECUTED</code> means no run conclusion;
<code>NOT APPLICABLE</code> and <code>UNSUPPORTED</code> preserve host-model
limits. Process exit <code>0</code> does not mean every catalog case passed;
<code>1</code>, <code>2</code>, and <code>77</code> retain the meanings
documented in [Testing](../testing/README.md#status-values-and-exit-codes).

## Privacy and retention

Do not put request bodies, response bodies, authorization headers, cookies,
tokens, passwords, private keys, certificates, or personal data into
canonical evidence. Use synthetic baseline markers. Keep raw host output under
an external temporary/runtime root with restrictive permissions, review the
effective configuration before sharing it, and retain only artifacts required
by the evidence contract.

Generated report files are consumers of this evidence. Update their generator
and regenerate them; do not manually rewrite generated Markdown or JSON.

## Next reads

- [Testing documentation](../testing/README.md)
- [Connector documentation](../connectors/README.md)
- [Configuration variables](../configuration/variables.md)
- [Glossary](../reference/glossary.md)
