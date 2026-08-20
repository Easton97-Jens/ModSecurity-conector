# Testing and evidence

**Language:** English | [Deutsch](testing-and-evidence.de.md)

## Scope

Testing distinguishes structural checks, build/configuration checks, focused
host traffic, full-lifecycle execution, and evidence validation. Passing one
layer does not imply that another layer passed. The selected documentation is
limited to the six HTTP/1.1 core routes and makes no production, CRS,
complete-matrix, HTTP/2, HTTP/3, or strict-for-all-connectors claim.

The general Make targets in this guide retain their six-connector scope. The
scheduled/manual <code>all-connectors-no-crs.yml</code> workflow is narrower:
its closed <code>no-crs</code> profile runs only Apache, HAProxy, Envoy,
Traefik, and lighttpd. It rejects unknown profiles and rows outside that map;
NGINX is not a result in that workflow. The profile aggregate validates one
bound result and receipt per selected connector, including run and commit
identity plus cleanup status. That validation is not hosted-runtime proof and
does not provide CRS, MRTS, HTTP/2, HTTP/3, full-matrix, or production claims.

## Closed no-CRS/with-MRTS runtime route

The current-master task route adds a separate, closed
<code>no-crs/with-mrts</code> runtime path for exactly Envoy, Traefik, and
lighttpd. The entry point is
<code>ci/runtime/lifecycle/run-no-crs-with-mrts-target.py</code>; it requires
<code>--execute-stage</code> and rejects any connector outside that three-item
set. Apache and HAProxy continue to use their existing MRTS host route in the
five-connector workflow; this section does not alter their contract.

The route creates a private run root, verifies the Parent gitlink to
Framework and the Framework gitlink to MRTS, and imports the MRTS cases through
the exact checked-out Framework. The current pinned chain is:

| Repository | Revision used by the route |
| --- | --- |
| Parent | current task base `b42907ca410da69843c80d0c4376193b6ab3801b` |
| Framework gitlink | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| MRTS gitlink | `615b13bacbd008562c17408246c41ab27dca3104` |

The generated plan records the three revisions, the imported case inventory
and hashes, the generated load file, the selected profile, and the closed case
set. The executor
<code>ci/runtime/lifecycle/execute-no-crs-mrts-cases.py</code> sends actual
requests through the selected live host and correlates request, transaction,
case, expected-rule, and observed-event identifiers. It requires a
DetectionOnly HTTP 200 result, an actual detection case, a legitimate control,
and a benign bypass control before atomically writing the bounded result.

The plan is sealed by a SHA-256 digest computed over the exact plan bytes and
propagated through every host-adapter boundary. Before a host starts, the
validator re-reads the sealed bytes, rejects duplicate JSON keys, verifies the
plan digest, and reconstructs the selected cases from the exact Framework
inventory. The selected case hashes and inventory hash must match the plan;
changing a URI, expected event ID, or case source therefore fails closed. The
executor receives the same digest explicitly and records it in the receipt.

Rule-match evidence uses a typed native `RuleMessage` observer. It is disabled
by default and is enabled only for the sealed MRTS runtime profile. The
observer emits bounded metadata-only JSONL records with request and
transaction correlation; it does not scrape audit logs, error logs, stderr, or
request/response payloads. Native integrity and contiguous-chain validation is
performed before the result is accepted.

This profile is explicitly no-CRS. The route rejects CRS references in the
generated MRTS load file and passes the repository-owned no-CRS rules only as
the active non-CRS input. The route does not enable, acquire, cache, or reuse
OWASP CRS. The generated plan, result, event log, host summary, and cleanup
state remain under the private run root; they are runtime evidence, not source
files to commit.

The three host adapters must start their real connector and execute this plan
while that connector is live:

- Envoy uses the existing ext-proc host path;
- Traefik uses the existing native middleware host path; and
- lighttpd uses the existing patched native host path.

The task changes neither the <code>with-crs/with-mrts</code> negative targets
for these connectors nor NGINX. It also makes no Framework or MRTS source
change; the Framework and MRTS revisions above are consumed as exact
gitlinks.

### Evidence status for this task

At documentation time, the route and its contracts are present in the task
worktree. The observed local validation includes 97 focused Python contract
tests, shell syntax checks for the changed runners, Python compilation,
`check-common-security-contract.py`, `check-adapter-contracts.py`,
`check-remaining-connectors-build-wiring.py`, and `git diff --check`. The
Envoy and Traefik Go checks used `/usr/local/go/bin/go` `go1.26.6` with
`GOTOOLCHAIN=local`: `gofmt`, `go mod verify`, `go list -deps ./...`,
`go test ./...`, `go vet ./...`, and `govulncheck ./...` passed (the Traefik
module was run from `connectors/traefik/native_middleware`; the first longer
temporary socket path was replaced by a private short test root). C/C++
syntax checks and the repository C17 remaining-connector check also passed.
The broad C++ security scan was kept at its original C/H baseline plus the
new typed observer `.cc` file; the pre-existing `common/scripts/
modsecurity_targeted_eval.cc` was not exempted. Four pre-existing ShellCheck
SC1007 warnings remain in the Envoy configuration helper.

The real three-connector host runs, hosted Actions, Required Checks,
SonarQube Cloud analysis, and PR-head equality have not been observed by this
documentation change. They remain <code>NOT EXECUTED</code> or
<code>PENDING</code> until the corresponding exact-head evidence exists. A
static plan, inventory, parser test, or workflow contract must not be promoted
to a runtime <code>PASS</code>. See the paired [Change Record](../reports/audits/change-records/CR-20260820-no-crs-with-mrts-runtime.md)
for the bounded delivery state and limitations.

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
| <code>NOT APPLICABLE</code> | The case/path is outside the documented scope of the selected job or profile |
| <code>UNSUPPORTED</code> | The selected host model cannot provide the required capability |

Promotion is evidence-gated. A build, configuration load, capability
manifest, generated report, or static inventory does not turn an unexecuted
case into PASS. Keep current readiness and run-specific status in the current
reports; this guide explains the model rather than preserving historical
status matrices.

CI control records may use the corresponding lowercase values `passed`,
`failed`, `blocked`, `not_executed`, and `not_applicable`. They preserve the
direct check result before a recursive orchestration layer can replace its
exit code; they are not runtime-evidence records. A `blocked` or
`not_applicable` control record permits workflow success only where that
specific workflow contract explicitly allows it.

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
