# Testing and evidence

**Language:** English | [Deutsch](testing-and-evidence.de.md)

## Scope

Testing distinguishes structural checks, build/configuration checks, focused
host traffic, full-lifecycle execution, and evidence validation. Passing one
layer does not imply that another layer passed. The selected documentation is
limited to the six HTTP/1.1 core routes and makes no production, CRS,
complete-matrix, HTTP/2, HTTP/3, or strict-for-all-connectors claim.

## Test layers

| Layer | Typical target | Establishes | Does not establish |
| --- | --- | --- | --- |
| Documentation and contracts | <code>make quick-check</code>, <code>make lint</code> | Source, schema, link, language, and contract consistency | Live host traffic |
| Build | <code>make build-&lt;connector&gt;</code> | A selected build stage | Config load or request/response behavior |
| Configuration | <code>make check-config-&lt;connector&gt;</code> | Selected configuration can be parsed or loaded | Runtime behavior |
| Focused smoke | <code>make runtime-smoke-&lt;connector&gt;</code> | The narrow host exercise documented by the target | Full lifecycle or catalog completeness |
| Full lifecycle | <code>make full-lifecycle-&lt;connector&gt;</code> | Selected profile plus artifact production | Production readiness or all protocols |
| Evidence validation | <code>make evidence-check-&lt;connector&gt;</code> | Existing run artifacts meet that validator's contract | A new host run |

The placeholder <code>&lt;connector&gt;</code> is exactly one of Apache, NGINX,
HAProxy, Envoy, Traefik, or lighttpd in lowercase target form.

## Core commands

| Goal | Command pattern | Boundary |
| --- | --- | --- |
| Fast repository validation | <code>make quick-check</code> | Does not start every host or create canonical evidence |
| One selected aggregate candidate | <code>NO_CRS_RUN_ID=&lt;run-id&gt; make full-lifecycle-all-connectors</code> | Produces candidate artifacts only |
| Aggregate core validation | <code>NO_CRS_RUN_ID=&lt;run-id&gt; make check-six-connector-core-completion</code> | Reads finalized evidence for that run ID |
| One configuration check | <code>make check-config-&lt;connector&gt;</code> | Does not send traffic |

<code>NO_CRS_RUN_ID</code> is a filesystem-safe, non-secret identifier. It
binds artifacts to one invocation; it is not a result label or a promotion
mechanism.

## Cases, rules, and protocol boundaries

The Framework owns reusable YAML cases, catalog selection, schemas, and
normalization. The connector repository owns host integration and its selected
rule/configuration inputs. Repository-owned No-CRS rules and IDs are separate
from OWASP CRS. A prepared CRS input or a source-only protocol path does not
verify CRS behavior, HTTP/2, or HTTP/3.

| Topic | Required evidence |
| --- | --- |
| P1/P2/P3 | Selected host traffic, matched result records, and profile-appropriate events |
| P4 | Phase-specific artifacts plus the actual commit/EOS boundary |
| First byte before EOS | Synchronized timing or transport observation, not merely a completed response |
| No full response buffering | Source and/or host observation that excludes a connector-owned complete response buffer |
| Protocol claims | Explicit protocol client, host, and artifact evidence for the stated protocol |

## Evidence model

Canonical evidence is run-scoped. It identifies the connector, selected
profile, rules, run ID, effective configuration, status, and required result
and event records. Raw invocation-local output is not automatically promoted:
normalization and validation must preserve provenance and the selected
capability boundary.

| Artifact class | Purpose | Privacy and retention rule |
| --- | --- | --- |
| Result records | Record case status and observable response facts | Keep payload-free fields and scoped IDs |
| Event records | Explain phase, action, limits, and late/commit context | Do not include request or response bodies |
| Effective configuration | Bind a run to selected non-secret inputs | Redact secrets and host-private values |
| Logs and transport observations | Support a stated debugging or timing claim | Keep only the minimum required metadata |

Do not commit credentials, cookies, authorization values, private keys,
certificates, raw request bodies, raw response bodies, or local runtime output.

## Status and promotion

| Status | Meaning |
| --- | --- |
| <code>PASS</code> | The selected check met its recorded conditions |
| <code>FAIL</code> | A required condition was not met |
| <code>BLOCKED</code> | A declared prerequisite was unavailable or unsafe |
| <code>NOT EXECUTED</code> | The case/path was deliberately not run |
| <code>UNSUPPORTED</code> | The selected host model cannot provide the required capability |

Promotion is evidence-gated. A build, configuration load, capability
manifest, generated report, or static inventory does not turn an unexecuted
case into PASS. Keep current readiness and run-specific status in the current
reports; this guide explains the model rather than preserving historical
status matrices.

## Historical context

Earlier per-connector proof-of-concept summaries, planning notes, and
intermediate evidence summaries were consolidated into the connector guides,
current reports, and architecture/evidence audit. They did not establish a
separate source of truth and remain available through Git history. The current
evidence boundary above is unchanged.

## Local development and safety

Use externally writable runtime, cache, build, log, and evidence roots selected
through documented variables. The repository does not prescribe a developer
checkout location. Missing optional components should use the declared blocked
or prerequisite exit behavior rather than silently downloading, installing, or
falling back to an unrelated system binary.

For variable format, defaults, setters, and security notes see
[Variables](reference/variables.md). For host/profile syntax see
[Configuration](configuration.md).

## Related references

- [Architecture](architecture.md)
- [Connector guides](connectors/README.md)
- [Operations and security](operations-and-security.md)
- [Current reports](../reports/README.md)
