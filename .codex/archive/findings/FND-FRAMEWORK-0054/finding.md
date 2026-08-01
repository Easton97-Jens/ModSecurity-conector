# FND-FRAMEWORK-0054 — Framework ModSecurity v3 Git wrapper does not bind a verified host Git executable before provenance validation

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0054` |
| Category / Kategorie | `security_candidate` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Schweregrad | `medium` |
| Confidence / Konfidenz | `probable` |
| Status | `verified` |
| Feasibility / Machbarkeit | `feasible_now` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

## 2026-07-26 current-master verification

The ambient-PATH review below concerns historical master
`f98a8739cb13b583f23d646784b144e596b61441`. Framework PR #44's current
master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` binds approved host Git
before provenance commands. Its focused fake-PATH rejection and approved-host
legitimate controls pass alongside the FND-FRAMEWORK-0036 containment suite;
source provenance and quality controls remain fail closed.

The standalone Framework ModSecurity v3 provenance wrapper sanitizes Git
configuration and transport inputs but invokes an unqualified `git` resolved
from the caller's `PATH` before source provenance can be verified. Existing
regressions intentionally substitute a fake Git through `PATH` to model
approved Git arguments; they do not establish a verified host-executable
boundary.

## Observed behavior / Beobachtetes Verhalten

At exact clean Framework master `f98a8739cb13b583f23d646784b144e596b61441`,
`ci_modsecurity_v3_git` clears inherited Git state and then executes bare
`git -c ... "$@"`. It neither selects an absolute host Git program nor resets
`PATH`. The provenance regression writes a temporary `bin/git` and prepends
that directory to `PATH`; this is a legitimate model-Git control, not a proof
of the executable identity that production invokes.

## Expected behavior / Erwartetes Verhalten

Before a standalone fresh fetch, checkout, or recursive submodule command
reaches Git, the Framework must resolve and bind an approved host Git
executable independently of caller-controlled `PATH`, fail closed when that
trust contract cannot be established, and retain regressions which distinguish
test-only fake Git injection from production host-tool selection.

## Impact and scope boundary / Auswirkung und Scope-Grenze

If a less-trusted actor can influence `PATH` in a supported standalone
Framework fetch invocation, a substituted Git program can run with the
Framework/CI identity before source-provenance validation. The static review
has not demonstrated that a supported productive caller gives such an actor
`PATH` control. It is therefore a plausible `P2`/medium hardening gap, not a
validated exploit or high/critical finding.

The Parent invocation may bind `PATH` separately. This finding is limited to
the standalone Framework source-provisioning path and does not weaken or
replace `FND-FRAMEWORK-0032`, `FND-FRAMEWORK-0034`,
`FND-FRAMEWORK-0035`, or `FND-FRAMEWORK-0036`.

## Affected path / Betroffener Pfad

- `ci/lib/common.sh` — `ci_modsecurity_v3_git` runs bare `git` at the
  provenance boundary.
- `ci/provisioning/fetch-smoke-sources.sh` — `provision_fresh_modsecurity_v3`
  reaches init, fetch, checkout, and recursive submodule handling through that
  wrapper.
- `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py` —
  intentionally injects a fake `git` by prepending a temporary directory to
  `PATH`; it proves argument/provenance semantics but not host-tool binding.

## Evidence / Evidence

- Run ID: `20260723T162517Z-fnd-cross-0001-runtime-evidence-bcda7d1d`
  - Exact Framework master source:
    `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/lib/common.sh`
  - Type: `exact_framework_master_static_host_git_resolution_review`
  - SHA-256: `de97949bf36a409f4520b462f73dbb11b0033d70392c329c39d20f2131ccac6a`
  - Static RTK-wrapped revision/status, wrapper-context, and hash inspection
    exited `0` at `2026-07-23T17:31:41Z`.
- Same run ID, exact Framework regression source:
  `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/tests/security_regression/test_modsecurity_v3_git_ref_provenance.py`
  - Type: `exact_framework_master_static_fake_git_regression_review`
  - SHA-256: `d7e07d63c8bffb5526d13cf36159aa73b478879f68803bc92c8a0b56db2a1050`
  - Static RTK-wrapped fake-bin/`PATH` and hash inspection exited `0` at
    `2026-07-23T17:31:41Z`.

No runtime command substitution or hostile productive `PATH` source was
exercised. The fake Git test remains a legitimate control, not exploit proof.

## Proposed remediation / Vorgeschlagene Remediation

Define the supported host-tool trust contract and resolve a trusted absolute
Git executable before the boundary without trusting caller `PATH`. Verify its
permitted location, ownership, or other approved provenance and make
`ci_modsecurity_v3_git` fail closed when it cannot be established. Add focused
controls proving that a non-approved Git earlier on `PATH` is not invoked while
an approved host Git still completes the pinned legitimate fetch/check-out
path. Preserve the separate fresh-root containment work of
`FND-FRAMEWORK-0036`.

## Acceptance criteria / Akzeptanzkriterien

- The production standalone wrapper cannot resolve Git from an untrusted
  caller `PATH`.
- The selected Git executable has an explicit documented and fail-closed host
  trust contract before receiving fetch, checkout, or submodule arguments.
- A focused regression proves that a fake Git earlier on `PATH` is not invoked
  by the production wrapper.
- An approved host-Git control retains the legitimate pinned source graph and
  all existing provenance/fresh-root controls.
- Exact Framework PR-head review, focused checks, relevant CI/Sonar evidence,
  and resulting-master verification pass without weakening controls.

## Validation plan / Validierungsplan

- Establish whether a supported Framework or CI caller exposes `PATH` to a
  less-trusted actor; do not infer exploitability before that evidence exists.
- Implement the host-Git binding only in an isolated Framework task/PR and run
  focused fake-PATH block and approved-host-Git legitimate controls.
- Re-run the FND-FRAMEWORK-0036 fresh-root worktree, attributes/filter, and
  recursive-update regressions because both findings share the pre-provenance
  Git-command boundary.
- Collect exact-head review, CI, Sonar, and resulting-master evidence before a
  `fixed` or `verified` disposition.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0032`
- `FND-FRAMEWORK-0034`
- `FND-FRAMEWORK-0035`
- `FND-FRAMEWORK-0036`

## Residual risk / Restrisiko

Standalone Framework provisioning retains an ambient command-resolution
assumption at a security-relevant pre-provenance boundary until the host-Git
trust contract and focused controls are verified. Practical exploitability is
unproven; no risk acceptance is recorded. Framework PR verification for this
path remains blocked pending a fix or evidence-matched disposition.

## History / Historie

- `2026-07-23T17:31:41Z`: `static_host_git_path_boundary_triaged` — exact
  Framework master invokes bare Git from `PATH`; the intentional fake-Git test
  does not prove a productive untrusted actor. This distinct P2/medium/probable
  candidate changed no product source, Framework branch/PR, Parent gitlink, or
  MRTS state.
