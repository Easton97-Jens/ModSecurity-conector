# Change Record: Parent shell dispatch-rule remediation for SonarQube Cloud S131 and S7679

**Language:** English | [Deutsch](CR-20260727-sonar-shell-dispatch-rules.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-shell-dispatch-rules |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud shell Code Smells: 59 current OPEN shelldre:S131 keys and 27 current OPEN shelldre:S7679 keys, 86 receipt keys in total across 30 Parent shell scripts. |
| Boundary | The 30 Parent shell scripts listed below, this English/German Change Record pair, and their indexes. Makefiles, workflows, generated reports, Framework, MRTS, Gitlinks, SonarQube Cloud configuration, Quality Gates, suppressions, external issue state, push, pull request, and merge remain unchanged. |

## Motivation and problem statement

The current receipt inventory reports missing explicit dispatch defaults and
direct positional-parameter uses in Parent shell scripts. The code has
security-relevant runtime, path, process, and evidence boundaries, so the
remediation must preserve quoted argument handling and must not turn unknown
selectors into a compatible or promoted fallback.

## Acceptance criteria

- Address all 86 receipt-backed shelldre:S131 and shelldre:S7679 occurrences.
- Preserve normal no-op cases that were already safe, and make unknown
  connector, stage, protocol, host-action, and runtime-selector paths
  explicitly fail closed where a dispatch decision is made.
- Preserve the scalar and quoted semantics of every positional parameter
  rewritten as a named local.
- Pass POSIX shell syntax checks for all 30 scripts, focused Parent contracts,
  negative selector controls, and whitespace review.
- Maintain an equivalent English/German Change Record pair and do not claim
  any SonarQube Cloud issue closed before a new exact candidate-head analysis.

## Implementation decision and rationale

Each pre-existing validation case retains its rejection and exit behavior. An
explicit no-op default was added only where the unmatched POSIX case behavior
was already a safe successful no-op. Mapping or dispatch switches now reject
unknown values before they can select a sibling connector, runtime component,
host binary, or evidence path. Each S7679 occurrence binds the positional
argument first and continues to use that value with the existing quotes.

## Changed files

- ci/checks/common/check-common-helpers.sh
- ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh
- ci/provisioning/cache/runtime-components-inventory.sh
- ci/runtime/lifecycle/consume-no-crs-selected-cases.sh
- ci/runtime/lifecycle/run-connector-stage.sh
- ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh
- ci/runtime/lifecycle/run-no-crs-baseline.sh
- ci/runtime/lifecycle/run-remaining-connector-target.sh
- common/scripts/run_blocked_runtime_smoke.sh
- connectors/envoy/build/build_connector.sh
- connectors/envoy/build/build_ext_proc.sh
- connectors/envoy/config/prepare_envoy_config.sh
- connectors/envoy/config/prepare_envoy_ext_proc_config.sh
- connectors/envoy/config/prepare_envoy_ext_proc_runtime_config.sh
- connectors/envoy/harness/run_envoy_connector_runtime.sh
- connectors/envoy/harness/run_envoy_ext_proc_runtime.sh
- connectors/envoy/harness/start_envoy_connector.sh
- connectors/haproxy/harness/run_haproxy_htx_runtime.sh
- connectors/haproxy/htx-overlay/build-overlay.sh
- connectors/lighttpd/build/apply_core_patch.sh
- connectors/lighttpd/build/build_patched_core.sh
- connectors/lighttpd/build/build_patched_host.sh
- connectors/lighttpd/harness/check_patched_lifecycle_host.sh
- connectors/lighttpd/harness/prepare_native_smoke.sh
- connectors/lighttpd/harness/run_patched_full_lifecycle.sh
- connectors/nginx/harness/run_nginx_smoke.sh
- connectors/traefik/build/build-connector.sh
- connectors/traefik/build/build-engine-service.sh
- connectors/traefik/build/build-native-middleware.sh
- connectors/traefik/scripts/start-smoke.sh
- reports/audits/change-records/CR-20260727-sonar-shell-dispatch-rules.md
- reports/audits/change-records/CR-20260727-sonar-shell-dispatch-rules.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

- Receipt reconciliation for all 59 shelldre:S131 and 27 shelldre:S7679 keys.
- rtk proxy sh -n for each of the 30 changed shell scripts.
- Focused Parent unittest modules for selected-runner wiring, runtime snapshot
  integrity, NGINX protocol harness, Envoy transport hardening, Traefik
  runtime-root security, and CI security workflows.
- HAProxy HTX overlay static contract plus remaining-connector build and
  start-wiring contracts.
- Negative command controls: invalid connector and invalid stage in
  run-connector-stage, plus invalid connector in run-no-crs-baseline.
- rtk proxy git diff --check.
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs.
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links.

The isolated task worktree initializes the Parent-recorded Framework Gitlink
only to satisfy test and documentation dependencies. No Framework source,
Parent Gitlink, Framework branch, or Framework pull request changes.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Receipt reconciliation | passed: 59 of 59 S131 cases have an explicit default and 27 of 27 S7679 occurrences bind a named positional local before use. |
| POSIX shell parsing | passed: sh -n exited 0 for all 30 changed scripts. |
| Focused Parent contracts | passed: 50 tests across selected-runner wiring, runtime environment snapshot, NGINX protocol, Envoy transport, Traefik runtime-root security, and CI security workflow modules. |
| HAProxy HTX contract | passed: the overlay contract reported every required lifecycle, event, and no-buffer invariant as PASS. |
| Remaining-connector build and start wiring | passed: both checks reported ok. |
| Negative selector controls | passed: invalid connector and invalid stage in run-connector-stage, and invalid connector in run-no-crs-baseline each exited 2 before a Framework/runtime command or evidence write. |
| git diff --check | passed: no whitespace error. |
| make check-bilingual-docs | passed: bilingual docs ok. |
| make check-doc-links | passed: repository path references: PASS and doc links ok. |

## Security impact

A focused source-to-sink security review found no new fail-open, command
injection, or unsafe file-output path. Existing unsafe path/run-ID/port
rejections remain intact. Explicit mapping and dispatch defaults now fail
closed for unknown connector, stage, protocol, host-action, and component
selectors. The one empty result for an unknown ruleset remains fail-closed
because each consumer first requires the resulting JSON file to exist. No
security finding is claimed fixed; these scanner rows are maintainability
signals with security-sensitive controls preserved and strengthened.

## Documentation status

This English/German Change Record pair documents the shell-only remediation.
The completed repository documentation checks report bilingual docs ok,
repository path references PASS, and doc links ok. No generated documentation
or report was edited.

## Runtime evidence

No expensive connector matrix, host build, or report-producing runtime run was
performed. The focused contracts prove static dispatch, path, and transport
invariants; they are not evidence of a full connector lifecycle run.

## Known limitations

SonarQube Cloud has not yet analyzed this candidate head. The 86 current
findings can disappear only after a fresh analysis of the exact delivered
commit. Full host/lifecycle matrices remain intentionally local-only and were
not used for this source-only maintenance candidate.

## Remaining risks

The patch spans 30 scripts, so a misplaced default could affect an uncommon
selector. Receipt reconciliation, syntax checks, focused valid-route tests,
negative selector controls, and the independent security review reduce this
risk. A new exact-head hosted analysis remains required to verify the
scanner's result.

## Checks not run and rationale

- A full connector build or lifecycle matrix was not run because it produces
  large external runtime artifacts and is not necessary to validate the
  explicit shell-dispatch/source contract. It remains a local-only validation
  path, not a GitHub workflow requirement.
- Hosted SonarQube Cloud analysis and GitHub CI are not yet available for this
  uncommitted local candidate.
- No Framework test suite, MRTS test, Framework source modification, MRTS
  source modification, commit, push, pull request, or master merge has
  occurred at the time of this record.

## Final diff and review status

The task-worktree candidate contains the 30 scoped Parent shell changes and
its required bilingual traceability material. The authoritative Parent
checkout, Framework source, MRTS source, Parent Gitlink, scanner controls, and
external SonarQube Cloud issue states remain unchanged.
