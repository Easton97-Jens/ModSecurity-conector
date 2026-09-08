# With-CRS/no-MRTS exact-five profile contract

**Language:** English | [Deutsch](with-crs-no-mrts-profile-contract.de.md)

This page defines the Parent-owned evidence boundary implemented by
`ci/runtime/lifecycle/with-crs-no-mrts-profile.py` and
`ci/runtime/lifecycle/aggregate-five-connector-with-crs-no-mrts.py`. It is a
closed, exact-five profile for one selected CRS block case. It is not a
protected-host attestation and does not close `FND-CROSS-0004`.

## Scope and identity

The profile accepts exactly these five connectors, once each:

`apache`, `haproxy`, `envoy`, `lighttpd`, and `traefik`.

Every cell is bound to the exact candidate head (`parent_sha`), base commit,
Framework commit, MRTS commit, CRS commit and rule SHA-256, GitHub run ID and
attempt, the actual executed test (`crs_sqli_anomaly_block`), and the profile run ID
`with-crs-no-mrts-<github_run_id>-<github_run_attempt>`. The candidate head and
base must be distinct. A cell run ID is
`crs-<github_run_id>-<github_run_attempt>-<connector>` and is explicitly marked
`cell_run_id_kind: workflow_cell`. It is a workflow-owned namespace, not a
claim that Apache or HAProxy emitted a native run ID.

For pull-request runs, the workflow receives the immutable pull-request event
head and base. A manual diagnostic run requires separately supplied full
`parent_sha` and `base_sha` inputs; they are syntax-checked and bound to the
checkout/aggregate. Neither path falls back to `github.sha` or a branch name.

The profile verifies the CRS rule file
`rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf`, its trusted full SHA-256,
and the exact freshly prepared CRS source commit. Evidence is read through
no-follow, descriptor-anchored, bounded private-file checks. JSON is canonical,
rejects duplicate keys and non-finite values, and exact profile assertions also
require exact JSON primitive types rather than value-equivalent bool/integer or
integer/float substitutions. Publication is one-shot into a new private
directory using exclusive creation.

## Native source boundaries

The producer does not infer identity from artifact directory names or raw path
fields. It consumes one bounded source shape per connector:

| Connector | Source kind | Required source facts |
| --- | --- | --- |
| Apache | `apache_case_summary` | The workflow explicitly starts only the selected case (`RUN_ONE_CASE=1`), which the profile receipt requires. The selected `crs_sqli_anomaly_block` case appears consistently in the summary and one JSONL result, with a live CRS deny and HTTP 403. Every required summary/JSONL scalar and cleanup-receipt identity uses an exact JSON primitive type; value-equivalent bool/integer or integer/float substitutions are rejected. Its raw serial audit must contain exactly one transaction for the exact block request, HTTP 403, and one `REQUEST-942-APPLICATION-ATTACK-SQLI.conf` / rule `942270` record. A Parent cleanup receipt is published only after tracked-PID teardown, PID-file removal, and the selected-listener probe. |
| HAProxy | `haproxy_projected_evidence` | The sealed projected package is re-verified through its existing strict evidence-owner verifier using the explicitly bound, separate evidence UID/GID and the ordinary runner only as reader. Its source and sealed evidence bind the Parent-issued `cell_run_id` from before runtime start and label it `workflow_cell`; it is not presented as a native HAProxy-issued ID. The package is exact and manifest-bound, and records the selected HTX/CRS deny, HTTP 403, rule 942270, and complete cleanup. |
| Envoy, lighttpd, Traefik | `generic_runtime_observation` | The canonical runtime-observation contract validates the exact connector/profile/run and parent/Framework/MRTS identity, including allow 200, block 403/deny/rule 942270, cleanup, and all five no-MRTS flags false. |

Apache and HAProxy selected sources prove the block control only. Their
`allow_control` is deliberately `not_observed`; the producer makes no
synthetic allow claim. Generic sources must provide both allow and block
observations.

The Apache receipt records the workflow-owned `cell_run_id`, `github_run_id`,
and `github_run_attempt`, and has zero only for the bounded checks it actually
performs: `tracked_host_processes_remaining`,
`tracked_helper_processes_remaining`, `selected_listeners_remaining`, and
`pid_files_remaining`. It does not assert that every process or socket on the
runner has been inventoried. The raw audit, cleanup receipt, summary, and JSONL
are each source-hashed in the profile cell. A missing, malformed, noncanonical,
wrong-typed, wrong-rule, wrong-transaction, failed-cleanup, or residual-count
source is rejected before a cell package can be published.

The HAProxy package stays under its separate evidence identity. The profile
does not weaken the generic private-file checks, relabel the package, or copy
it as native evidence: it calls the established sealed-package verifier with
the workflow's explicit separate evidence UID/GID and trusted
Parent/Framework/MRTS identities plus the pre-established workflow cell run
ID, then binds its verified digests to the receipt.

## Canonical cell package

Each successful cell produces exactly these three files in a fresh
`profile-cell` directory:

1. `functional-facts.json` — the bounded selected-case result, explicit
   allow-control scope, block fact, cleanup status, no-MRTS disposition, and
   `source_files_sha256`, the canonical digest of the ordered source-artifact
   binding list.
2. `profile-cell-receipt.json` — the complete identity binding, source-file
   hashes, CRS provenance, workflow cell identity, actual executed test, and
   hashes of the facts.
3. `manifest.json` — canonical hashes and sizes for the first two files.

The aggregate accepts exactly five such directories and rejects missing,
duplicate, unexpected, symlinked, non-private, or identity-mismatched cells.
It also rejects noncanonical JSON, value-equivalent but wrong primitive types,
extra files, invalid hashes, receipt source paths or digests that disagree with
`source_files_sha256`, wrong profile or connector identities, and any mismatch
in the pinned source or workflow invocation. The aggregate writes a separate,
one-shot package containing
`aggregate.json`, `aggregate.md`, `aggregate.de.md`, `matrix-24.json`,
`matrix-24.md`, `matrix-24.de.md`, and its `manifest.json`.

## Result semantics

The aggregate keeps four decisions separate:

- `technical_validity` is `PASS` only when the exact five independently
  validated cell packages and their bindings are present.
- `functional_success` is `PASS` only for the selected CRS block case in all
  five cells. It does not upgrade Apache/HAProxy's unobserved allow control.
- `matrix_24_completeness` records the current honest disposition of all 24
  CRS/MRTS rows. The current fixed disposition is 5 `passed`, 6 `blocked`, 13
  `not_run`, 0 `failed`, and 0 `not_applicable`; disposition is complete while
  execution coverage is not.
- `merge_eligible` remains `false`. Technical validity and selected functional
  success are not merge authorization.

The six blocked rows are the unavailable Framework-owned MRTS routes for
Envoy, Traefik, and lighttpd (two MRTS profiles each). The other 13 rows remain
`not_run`; no result is inferred from another connector, profile, or historical
artifact. The Framework-owned acceptance condition represented by
`FND-CROSS-0004` remains separately blocked. No row is described as a
protected-host attestation, and no finding is closed by this contract.

## Relationship to workflow acceptance

The workflow must supply either the pull-request event's exact head and base
or explicit full manual inputs, verify both commits in the exact checkout, and
supply the GitHub run ID/attempt, freshly prepared CRS provenance, and the five
source packages. For Apache, it passes that runtime identity into the harness,
validates the raw audit and cleanup receipt, and only then produces the cell.
A successful aggregate is a scoped evidence result for that exact invocation.
It does not replace repository rules, required checks, Sonar, Framework/MRTS
acceptance, independent host evidence, or any later merge decision.
