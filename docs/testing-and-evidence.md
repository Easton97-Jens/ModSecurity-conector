# Testing and evidence

**Language:** English | [Deutsch](testing-and-evidence.de.md)

## Scope

Testing distinguishes structural checks, build/configuration checks, focused
host traffic, full-lifecycle execution and evidence validation. Passing one
layer does not imply that another layer passed. This guide describes the
selected HTTP/1.1 contracts and retained specialist interfaces; it does not
establish current readiness, production approval, CRS completeness, a complete
matrix, HTTP/2, HTTP/3 or strict acceptance of every connector.

The single [active inventory](../config/testing/active-cases.json) selects
normal local, CI and scheduled behavior. The closed five-profile
<code>all-connectors-no-crs.yml</code> baseline selects Apache, HAProxy, Envoy,
Traefik and lighttpd; NGINX has its separate protected exact-head path. Selected
CRS checks have their own profile IDs and evidence. Neither a five-profile
aggregate nor a successful sibling profile supplies an unobserved host result.

## Active cases, admission and archived specialists

The same schema-2 inventory now transparently declares 932 expanded cases / 536 executions: 89 core cases / 69 executions (including the original eight offline cases) and 843 user-authorized source-bound Python offline exceptions / 467 executions. The core ceiling remains 100 and is enforced before all children; exception variants are explicitly counted. Offline children deny process creation and network access before imports, and package-level discovery defers offline imports to that child. Raw `unittest discover -s tests` initially imports modules in the parent to find their hooks; reviewed top levels have no eager process/host activity, and actual tests then run only in guarded children. These are current-selection counts, not final acceptance. Native/Go/connector scenarios do not qualify for this exception.

Sonar uses the mandatory workflow from master #420 and its own scope/Go selection. The additional PR coverage pipeline and its gates were removed at the user’s request. The inventory ceiling applies to the remaining Parent selection; no global ceiling including the separate master-owned Sonar selection is claimed.


<code>make check-active-inventory</code> reports the actual expanded count
without executing cases. <code>make test</code> / <code>make test-active</code>
run the admitted inventory. Standard owning groups and exact case/module
filters select subsets after global admission. Functional checks behind
<code>make lint</code>, <code>make quick-check</code>, builds and CI use the same
selection. Pure build, formatting, static analysis and security scans remain
separate operations; hiding functional tests behind them does not exempt those
cases. Repeating an ID during a justified retest, race run or Hosted CI costs
another execution, not another distinct active case.

Retained specialists require a current request for the additional assessment and
explicit <code>ON_DEMAND_TESTS=1</code>. Do not export that flag globally or add
it to ordinary automated defaults. The flag changes retained specialist
selection; it grants no privilege, Framework/MRTS write, merge, release or I12
qualification authority. Historical I12 matrix/oracle/host campaigns remain
closed: archiving them does not schedule a repeat or establish
<code>I12_COMPLETE</code>.

The generated [archive disposition](../reports/testing/test-selection-archive.generated.json)
indexes retained Python methods and Go Test/Fuzz definitions and binds their
source/inventory digests. Only
<code>ci/tools/update-test-archive.py</code> regenerates it. Its definition count
is not a count of fully expanded behaviors, is not added to the active count
and does not assert that every archived assertion still passes. Unselected
parameters of a partly selected definition remain on demand; native/script
collectors and Framework catalogs remain available in their owning sources.
No archive entry is an executable selector or a new PASS.

| Retained on-demand area | Automatic coverage no longer claimed |
| --- | --- |
| Complete Python contract/validator/installer/updater mutation suites | Exhaustive permutations, malformed-input tables and historical expected workflow layouts beyond the named active controls. |
| Complete Go packages and randomized C/Go fuzz campaigns | Unselected table/subtest variants and generated fuzz inputs; active exact tests, selected race repeats and substantive security analysis remain. |
| Native Common/connector and runtime-path specialist collectors | Full error/parameter tables and the former 35-scenario path-policy catalog; the four selected real path inputs do not qualify every old path condition. |
| Full NGINX host campaigns | Inheritance/override, mode repair, unsafe targets, USR1/reload/overlap, error-page/body-buffer and archived configuration-negative campaigns; the selected callback On/Off cases do not prove these. |
| Broad smoke, full matrix, MRTS, H2/H3 and historical I12 tooling | Full catalog, protocol, oracle, ledger and host qualification. Narrow selected runtime/CRS results keep their own profile boundaries. |

Removing a behavior from automatic selection records lost automatic coverage;
it does not resolve a known defect or fabricate a historical success. Archived
sources and their original results/revisions remain retained. New active cases
at the core ceiling require a named replacement or genuine consolidation with the
affected requirement and risk recorded.

Profile proof is separate: HAProxy HTX does not qualify SPOE/SPOP with a response
companion; Envoy ext_proc does not qualify ext_authz with an observer; Traefik
native UDS does not qualify forwardAuth with an observer; lighttpd Stock,
patched-native and legacy header-compatibility observations do not qualify one
another. Bind every result to the actual selected profile.

## Test layers

| Layer | Typical target | Establishes | Does not establish |
| --- | --- | --- | --- |
| Documentation and contracts | <code>make quick-check</code>, <code>make lint</code> | Source, schema, link, language, and contract consistency | Live host traffic |
| Build | <code>make build-&lt;connector&gt;</code> | A selected build stage | Config load or request/response behavior |
| Configuration | <code>make check-config-&lt;connector&gt;</code> | Selected configuration can be parsed or loaded | Runtime behavior |
| Focused smoke | <code>make runtime-smoke-&lt;connector&gt;</code> | The narrow host exercise documented by the target | Full lifecycle or catalog completeness |
| Full lifecycle, on demand | <code>ON_DEMAND_TESTS=1 make full-lifecycle-&lt;connector&gt;</code> | Selected profile plus artifact production | Production readiness or all protocols |
| Evidence validation | <code>make evidence-check-&lt;connector&gt;</code> | Existing run artifacts meet that validator's contract | A new host run |

The placeholder <code>&lt;connector&gt;</code> is exactly one of Apache, NGINX,
HAProxy, Envoy, Traefik, or lighttpd in lowercase target form.

## Core commands

| Goal | Command pattern | Boundary |
| --- | --- | --- |
| Fast repository validation | <code>make quick-check</code> | Does not start every host or create canonical evidence |
| Explicit specialist aggregate candidate | <code>ON_DEMAND_TESTS=1 NO_CRS_RUN_ID=&lt;run-id&gt; make full-lifecycle-all-connectors</code> | Produces candidate artifacts only |
| Aggregate core validation | <code>NO_CRS_RUN_ID=&lt;run-id&gt; make check-six-connector-core-completion</code> | Reads finalized evidence for that run ID |
| One configuration check | <code>make check-config-&lt;connector&gt;</code> | Does not send traffic |

<code>NO_CRS_RUN_ID</code> is a filesystem-safe, non-secret identifier. It
binds artifacts to one invocation; it is not a result label or a promotion
mechanism.

## Cases, rules, and protocol boundaries

The Framework owns reusable YAML case definitions, schemas and normalization.
Parent owns automatic case admission, host integration and selected
rule/configuration inputs; Framework selections reached by Parent must match
the same active inventory. Repository-owned No-CRS rules and IDs are separate
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

### Archived NGINX configuration-only specialists

The retained configuration-negative contracts below are on demand, outside
normal active selection. Their historical receipts keep their original revision;
the active callback On/Off cases do not rerun or qualify these negatives.

The closed `invalid_boolean` and `invalid_size` configuration contracts use
`ci/runtime/lifecycle/run-nginx-configtest.py`. An actual `nginx -e stderr -t`
must reject `modsecurity maybe;` with exit 1 and both `"modsecurity" directive`
and `invalid boolean value` diagnostics. The Required ID `invalid_size` is
retained but explicitly migrated to removed-API rejection: the formerly valid
input `modsecurity_phase4_body_limit 1048576;` must produce exit 1 and
`unknown directive "modsecurity_phase4_body_limit"`, classified as
`removed_directive`. This is not an engine response-limit test. An unrelated
module-loading failure, wrong directive, missing diagnostic, timeout, or wrong
exit is not a passing negative test.

Each invocation requires a fresh external output directory below
`/var/tmp/codex/ModSecurity-conector`, outside checkouts and without symlink
paths. The driver retains and actually uses `nginx-binary` and
`nginx-module.so` snapshots, bounded to 64 MiB each. Together with `nginx.conf`,
`stdout.log`, and `stderr.log`, these form the five-file digest-bound evidence
bundle; captures are limited to 64 KiB combined and execution to 10 seconds.
`source-result.json` and its single-record `source-result.jsonl` companion
carry the receipt and `artifacts.configtest_dir` for the official collector.
The selected driver dispatches each registered case into its own fresh
`configtests/<case_id>` child; canonical retention uses
`inventory/configtests/<case_id>`. A Boolean receipt cannot fulfill the size
case, and independently executed cases cannot overwrite one shared bundle.
Keep these local artifacts external; they are not upload or commit material.

Directory admission checks the exact external output parent and its ancestors,
and the selected driver's build, results and configuration parents, through
the existing non-following `ensure_safe_runtime_directory` contract. Owned
`0755` parents are permitted; group- or other-writable parents are rejected.
Each new case child is private `0700`; an existing case child is rejected
before result append. An existing result file must be owned by the effective
UID, regular, have exactly one hard link, have no `0022` permission bits and
be at most 4 MiB. An otherwise admissible `0644` result file remains allowed.
These checks retain external-root containment and checkout exclusion; they
do not add HTTP evidence or change the accepted configtest diagnostics.

The matching Framework contract validates configuration evidence rather than
inventing a native request event. This operation proves parsing/rejection
only: no HTTP request, daemon startup, listener, master/worker identity,
reload, or protocol coverage is claimed. Caller-provided source SHAs require
independent run-provenance binding; trusted build inputs remain a prerequisite.
The contracts are limited to `invalid_boolean` and `invalid_size`, not every
phase-0 catalog case,
and cannot establish full required coverage or exact-head E2E PASS.

### HAProxy hosted evidence projection

The fixed `with-crs/no-mrts` HAProxy runtime cell may upload evidence only
after its runtime has exited and its cleanup result has been checked. It does
not upload the runtime root, build root, cache root, process logs, or a copy of
any of those roots. Instead, a source receipt for the fixed HAProxy P2 case is
strictly parsed and compared with trusted workflow values, then newly
serialized into exactly `haproxy-runtime-evidence.json` and `manifest.json`.
Both files contain bounded allowlist metadata and SHA-256 digests only; they
contain no body, header value, cookie, token, credential, opaque handle,
absolute path, raw log, or free-form runtime error text.

Receipt bytes cross through a fixed unprivileged `head --bytes=16385` stream
cap, then to the evidence projector only through standard input after the
identity drop. The projector accepts at most 16 KiB and rejects the 16,385th
byte, so the workflow never buffers untrusted receipt output in a shell
variable. Receipt bytes are never command-line arguments to `sudo`, `unshare`,
or `setpriv`.

The projection and verifier reject unexpected names, paths, JSON keys, types,
special files, symlinks, size-limit violations, and digest mismatches. Their
staging package is created below a new root-owned `RUNNER_TEMP` child. The
package directory is owned by the separate evidence UID and grouped to the
upload reader's runtime GID: it starts as `0700`, then the projector seals it
at `0550`. The two fixed evidence-identity files remain `0444`, but an
unrelated identity cannot traverse the `0550` directory; effective pathname
read access is limited to the evidence owner and that upload-reader group.
The runtime/upload reader has read/traverse permission only, never directory
write, rename, unlink, or chmod permission. The verifier checks this ownership
and mode contract immediately before the pinned upload action. Checkout code
for runtime, source export, projection, verification, and the final workflow
summary executes only after a private PID/mount namespace and privilege drop
with `no_new_privs`; privileged operations have fixed staging-only paths and
do not execute checkout code.

Each embedded immutable-Git-object launcher verifies the exact Git blob
preimage `b"blob " + decimal length + b"\0" + source` before `compile` can
run it. Here `\0` is Git's single NUL delimiter, not a printable backslash and
zero; a mismatched preimage fails the job before any selected checkout code is
executed.

For an evidence-receipt runtime, cleanup first asks the `setsid` leader to
stop, gives it a bounded reaping window, then terminates any remaining process
group and escalates to `KILL` only if the bounded termination window expires.
It still waits for the recorded leader and verifies that its process group is
empty. Any failed stop, wait, or residual-group check prevents the receipt,
projection, and upload.

This boundary records only the fixed P2 receipt and does not claim P3/P4,
production readiness, or a successful hosted result until the exact workflow
run and its uploaded artifact have been observed.

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
