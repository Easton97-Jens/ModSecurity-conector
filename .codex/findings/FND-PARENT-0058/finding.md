# FND-PARENT-0058 — Full-matrix parallel jobs overlap response-header backend port ranges

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0058 |
| Category | test_failure |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / validated |
| Status / feasibility | fixed / feasible_now |
| Release blocker | yes |
| Scope | loopback full-matrix runtime, FORCE_ALL_CASES=1 with global CPU parallelism |

## Validated behavior, scope, and impact

The Parent runner starts Apache, NGINX, and HAProxy concurrently with nominal
main-port offsets 0, +1000, and +2000 from each variant base. Apache and NGINX
each use a PORT+1000 response-header backend selection. Consequently an Apache
backend can collide with the NGINX main range, and an NGINX backend can collide
with the HAProxy main range. Independent free-port checks have a check-then-
bind (TOCTOU) window; they are not global reservations.

Affected code is ci/runtime/lifecycle/run-full-matrix-parallel.sh
(variant_base_port, connector_offset, run_batch, run_job, and
PORT_SEARCH_LIMIT) and the Apache/NGINX start_response_header_backend
implementations. The collision is enabled when concurrent Apache, NGINX, and
HAProxy jobs run response-header cases under FORCE_ALL_CASES=1.

The resulting full-matrix evidence can fail, block, bind to the wrong
listener, or become nondeterministic for scheduler reasons rather than a
connector result. This is a validated P1 test/runtime-evidence reliability
blocker. It is deliberately separate from FND-PARENT-0057's plausible
workflow template-injection/S8707 trust-boundary correction and from
FND-SONAR-0016's aggregate Quality-Gate state.

## Evidence and reproduction

The retained task receipt is
/var/tmp/codex/ModSecurity-conector/runs/20260726T185607Z-pr74-fast-validation-hosted-followup/evidence/hosted-observation.md
(run 20260726T185607Z-pr74-fast-validation-hosted-followup, SHA-256
5c64b4fe03ed670b0d2c25c58c2f770b59ae53bab10851ced35bd9012117d956,
2,978 bytes). It anchors the exact Draft PR #74 follow-up; the validated
port arithmetic is reproduced from the current Parent runner and harness
sources. The read-only receipt command exited 0. PR #74 remains Draft and no
Framework/MRTS, Gitlink, close, merge, or delivery action is claimed.

Reproduce by comparing the runner's 0/+1000/+2000 layout with Apache
run_apache_smoke.sh:1924 and NGINX run_nginx_smoke.sh:1260, then exercise an
applicable concurrent full-matrix variant with FORCE_ALL_CASES=1. Confirm that
auxiliary selection is not reserved against another concurrent job's main or
auxiliary range.

## Remediation, acceptance, and validation

The in-progress Parent runner/test correction must allocate disjoint dynamic
port reservations for every main and auxiliary service, hold each reservation
through the owning job lifetime, and use a bounded global CPU scheduler. It
must retain per-job isolation, visible busy-port failures, full coverage, and
FORCE_ALL_CASES; serializing away coverage is not a remedy.

The current local implementation adds
ci/runtime/lifecycle/plan_full_matrix_ports.py. It validates every possible
case/search interval in the fail-closed 1024..65000 range
(1024 is the first unprivileged port), rejects malformed or
unpackable plans before make, serializes preparation, and starts globally
capped runtime work only after artifacts are ready. These implementation
properties are not yet final full-suite or hosted validation evidence.

Acceptance requires:

- pairwise-disjoint Apache, NGINX, and HAProxy main and response-header ports
  for every supported concurrent variant;
- a focused allocation regression proving no auxiliary port equals another
  job's active main or auxiliary port;
- a focused port-plan control proving every possible case/search interval in
  1024..65000, including the complete twelve-job two-search-window plan, is
  validated and a malformed or unpackable plan is rejected
  before make;
- an intentional busy-port negative control that fails clearly without
  attaching to another listener;
- serialized preparation and global CPU admission only after the required
  artifacts are ready;
- a legitimate all-cases concurrent control that succeeds within the
  configured global CPU bound and cleans reservations/processes; and
- fresh retained full-matrix evidence plus re-reading the original collision
  path before any fixed or verified disposition.

## Dependencies, residual risk, and history

This record depends on FND-CROSS-0001 successor-evidence handling and final
focused, full-suite, and hosted evidence for the exact successor Parent
runner/test patch. Until the local plan validation, malformed-plan rejection,
serialized preparation, ready-artifact scheduler admission, and full-matrix
behavior are rerun, parallel all-cases runtime evidence can be
nondeterministic or attach to an unintended loopback listener.

Recorded 2026-07-26T18:56:07Z as
full_matrix_parallel_port_range_overlap_validated. It remains
in_progress / feasible_now; no remediation validation or delivery outcome is
claimed. The local plan/scheduler implementation was additionally recorded at
2026-07-26T19:46:59Z; final full-suite and hosted validation remain pending.
