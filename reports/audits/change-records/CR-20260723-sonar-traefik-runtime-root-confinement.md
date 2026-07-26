# Change Record: Traefik runtime binary provenance and root confinement

**Language:** English | [Deutsch](CR-20260723-sonar-traefik-runtime-root-confinement.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-traefik-runtime-root-confinement |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | `AZ9MwiwM-bUaKQ_zSGAq` and `AZ9cRyuTHhV2CayPTP1Q` (`python:S5443`); pending canonical finding import `FND-SONAR-0012`. |
| Boundary | Parent-only Traefik helper, Parent test, paired Traefik documentation, and this Change Record pair. Framework, MRTS, Gitlinks, dependencies, scanner configuration, Quality Gates, suppressions, false-positive state, and host protocol behavior remain unchanged. |

## Motivation and problem statement

The direct Traefik forwardAuth runtime smoke derived `BUILD_ROOT` and
`CONNECTOR_COMPONENT_CACHE` from predictable shared `/var/tmp` defaults. It
then derived connector and Traefik executable paths from those roots and
passed them to `subprocess` after an absolute-path, non-system-path,
exists-and-executable check only. A different local user could preseed the
shared temporary tree before a direct invocation and cause attacker-selected
executables to reach the process sinks.

The issue is a local cross-user executable-integrity boundary. No remote
request-to-process path, Framework behavior, MRTS behavior, or production
capability claim is changed by this remediation.

## Acceptance criteria

- Missing, group/world-writable, or symlinked runtime roots are rejected
  before process execution.
- A symlinked binary or a binary outside its designated root is rejected.
- A group/world-writable directory between a validated root and its binary is
  rejected before that binary can be executed.
- A legitimate current-user-owned, non-group/world-writable contained regular
  executable remains accepted.
- The two selected keys are checked on a fresh exact-head SonarQube Cloud
  analysis without a suppression, false-positive disposition, exclusion,
  rule change, or Quality-Gate change.
- Focused tests, syntax/import validation, direct-caller and alternate-bypass
  review, a security-diff review, and hosted exact-head checks are recorded
  truthfully before delivery.

## Implementation decision and rationale

The Python boundary immediately before the connector and Traefik `subprocess`
sinks is the narrowest complete enforcement point. The helper now requires
explicit `BUILD_ROOT` and `CONNECTOR_COMPONENT_CACHE` values. Each selected
root must be an existing absolute directory outside the checkout, owned by the
invoking user, non-symlinked, non-group/world-writable, and protected from
cross-user ancestor replacement. Each selected binary must be a regular,
current-user-owned, non-group/world-writable executable contained below its
corresponding validated root. Every directory entry between that root and the
binary must also be protected from cross-user replacement, so root-level
validation cannot be bypassed by a writable descendant.

This removes only the unsafe implicit shared `/tmp` and `/var/tmp` fallback.
It preserves explicit canonical lifecycle roots that meet the same integrity
requirements, preserves the existing `BLOCKED` / Exit 77 failure mode, and
keeps `--help` available without runtime inputs. It neither introduces a
global-binary exception nor weakens existing path controls.

## Changed files

- connectors/traefik/scripts/runtime_smoke.py
- tests/test_traefik_runtime_smoke_security.py
- connectors/traefik/README.md and connectors/traefik/README.de.md
- this English/German Change Record pair

The established Change Record indexes are deliberately not changed because
both are already modified by unrelated open Draft PR #74; this task does not
claim ownership of those paths.

## Commands executed

- `python -m unittest -v tests.test_traefik_runtime_smoke_security`: passed;
  five focused malicious and legitimate-control tests exercised the changed
  helper boundary, including a writable binary ancestor and an owner-controlled
  `0755` legitimate root.
- `python -m compileall -q connectors/traefik/scripts/runtime_smoke.py tests/test_traefik_runtime_smoke_security.py`:
  passed with bytecode redirected outside the checkout.
- `python connectors/traefik/scripts/runtime_smoke.py --help`: passed without
  runtime inputs.
- A direct invocation with all runtime-root environment variables unset and an
  absolute disposable result root returned `BLOCKED` / Exit 77 with
  `BUILD_ROOT must be set to a trusted runtime root`; no runtime artifact was
  created.

## Security impact

The changed source-to-sink path is selected `BUILD_ROOT` or
`CONNECTOR_COMPONENT_CACHE` to derived executable path to `subprocess`.
The invariant is enforced before either executable is accepted: each root and
file must establish current-user provenance, non-shared writability,
non-symlink identity, cross-user ancestor protection, and expected-root
containment. This blocks the preseeded-root, symlink, outside-root, and
writable-descendant bypasses without changing trusted explicit lifecycle-root
behavior.

No security control is weakened and no suppression, `NOSONAR`, scanner
configuration, or Quality-Gate change is used.

## Runtime evidence

The deterministic Parent regression suite exercises the real helper functions
that gate the two process paths. It safely proves root and executable rejection
before a subprocess is started and proves a contained regular executable is
accepted. It is not a host-runtime claim: no real Traefik, connector, or
libmodsecurity process was started.

## Known limitations

The local canonical `.codex/findings` store is mounted read-only, so the full
EN/DE/JSON `FND-SONAR-0012` bundle is retained as an import-ready artifact in
the private task run instead of silently omitting finding synchronization. The
Change Record index pair is intentionally deferred because those files overlap
open Draft PR #74. Neither condition changes product source behavior.

## Remaining risks

Until a new exact PR head is analyzed, direct invocations of unpatched master
still accept the predictable roots. Same-UID races remain outside the
cross-user protection claim. Fresh hosted CI and SonarQube Cloud evidence are
required before either selected key is declared resolved. No risk acceptance is
recorded.

## Checks not run and rationale

- `tests.test_collect_no_crs_source` is blocked in the isolated task worktree
  because it imports the absent Framework submodule checker
  `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`.
  No Framework change, global interpreter, or dependency substitution was
  attempted.
- A real Traefik runtime smoke is not run because documented local
  connector/Traefik/libmodsecurity prerequisites were not established. The
  focused helper tests do not substitute for host-runtime evidence.
- The repository-wide bilingual checker can remain blocked by Framework link
  targets if the isolated worktree lacks the Framework submodule; it is run
  before delivery and reported truthfully.
- Hosted checks and exact-head SonarQube Cloud analysis cannot run before a
  commit and Draft PR exist.

## Final diff and review status

The local Parent-only implementation and focused security controls are on
branch `codex/sonar-traefik-runtime-root-20260723-master-a308d7b` based on the
current observed `master` revision. No commit, push, pull request, review
approval, merge, default-branch update, or hosted result is claimed. The final
diff, security-diff review, exact-head checks, SonarQube Cloud result, and
Draft PR state must be reconciled before delivery is reported as verified.
