# Protected exact-head review package

**Language:** English | [Deutsch](protected-exact-head-review-package.de.md)

Preparation only — no merge authorization.

## Scope and disposition

This package describes the protected-base NGINX `modsecurity_use_error_log`
control plane. It is a review aid, not a hosted attestation. The candidate
checkout is data; the protected-base dispatcher and privileged launcher are
the control-plane TCB. `independent_review_requested=false` and
`reason=no_authorized_reviewer_available`; no reviewer approval is implied.

The external codex-security archive receipt remains
`blocked_external_dependency` (FND-PARENT-1036). The retained old run and
synthetic fixtures are failure evidence only. The first exact read-back for
`c8f1a00a5d45cbc5c4a7e52e1da17e8611e767db` is historical remediation input,
not final acceptance: it found 20 open code smells despite a green gate. Its
first source/test successor `0524be2f…` then exposed three different open
issues. Exact successor `74581e8d…` still exposed two S8707 vulnerabilities
and a new test S5778 smell; the next normal successor is being remediated
rather than accepted. Hosted runtime and post-push Sonar result remain pending
exact-head validation.

## Threat model and trust boundaries

Untrusted inputs include pull-request metadata, candidate source and workflow,
candidate callback/JSONL records, temporary-directory contents, and network
responses. The protected base admits one exact 40-character lowercase Git SHA,
uses fixed semantic locations, and passes only validated descriptors into the
privileged cell. A root-owned, non-writable host bootstrap must independently
verify the protected-base object and immutable launcher snapshot. Candidate
claims are observations, not attestations.

## TCB and handoffs

The TCB is the protected-base workflow, dispatcher, runner preflight, builder,
root launcher, collector, and administrator-installed host bootstrap. The
candidate module, Makefile, callback/JSONL output, and WAF text are outside
the TCB. Candidate and privileged cells use role-specific private directories;
the runner passes fixed `RUNNER_TEMP` and `GITHUB_WORKSPACE` values and does
not accept arbitrary path CLI options. FD ownership is descriptor-relative and
no-follow at private boundaries. The collector validates process identity,
namespace, artifact manifest, exit status, and result publication before
emitting a runner-owned terminal result.

The evidence root has one protocol-defined leaf, `launcher-evidence`. The CLI
value must be absolute and normalized, match that leaf exactly, and then has
only its runner-owned parent admitted; privileged creation uses the fixed leaf
relative to the retained parent descriptor.

Cleanup and publication remain under review for FND-PARENT-1038. The current
NGINX control retains root-owned directory, cell, scratch, artifact, helper,
and evidence descriptors; uses fixed sandbox mount destinations; publishes
evidence descriptor-relatively; and binds cleanup to validated identity before
allowing completion. A random root-selected scratch-container leaf prevents a
stale fixed-name resource from being mistaken for the current run, while
cleanup is confined to that root-owned container. Runtime root evidence is
bound to `tested_pr_base` as well as `tested_pr_head`. These are in-progress
repository source contracts and executable local tests; they are not claimed
fixed or hosted-validated.

## Workflow and evidence contract

The workflow grants only the permissions needed for checkout and declared
outputs; no candidate-controlled path, secret, or launcher is trusted by the
privileged job. The two fresh cells run on and off settings and must show
correlated transactions, distinct master/worker identities, equivalent WAF
observations, and the expected callback/JSONL difference. A missing host gate,
exit 77, stale head, or incomplete schema is a failed or externally blocked
run, never a pass.

## Negative-test matrix

| Boundary | Required negative control |
| --- | --- |
| SHA/path admission | Unicode digits, traversal, symlink, external root, and mutable candidate paths |
| Artifact handoff | Wrong owner/mode, replacement, symlink, stale manifest, and mismatched digest |
| Process/FD lifecycle | Directory/artifact descriptor substitution, sandbox-destination replacement, identity mismatch during cleanup, and incomplete publication |
| Runtime evidence | Wrong PID/namespace, missing correlation, unexpected exit, and incomplete on/off records |
| Documentation/security | Unpinned action, unsafe shell, weakened permission, and absent bilingual companion |

The repository's focused source-contract and negative-control tests are the
executable evidence for these controls. They cover retained-FD authority,
replacement races, identity-gated cleanup, bounded process supervision, and
descriptor-safe evidence publication. The repository does not claim that
these tests replace the protected hosted runtime.
Final command results must be collected again after the final exact head is
read back from GitHub.

## Historic Sonar inventory

The baseline at the prior PR head contained 80 open issues: 15 vulnerabilities
and 65 code smells; the quality gate was ERROR with three new security issues.
The historic issue-key matrix is listed below. Every item was a code/test
remediation target, not an administrative disposition; all entries require
fresh exact-head reanalysis.

| Rule / location | Historical issue keys |
| --- | --- |
| S1066 root | `AaBsRF5SmWRUlaV2f7fb` |
| S1192 collector | `AaBs7c_xmWRUlaV2mVXl`, `AaBs7c_xmWRUlaV2mVXk` |
| S1192 root | `AaBs7c4JmWRUlaV2mVXc`, `AaBsRF5SmWRUlaV2f7fa`, `AaBsRF5SmWRUlaV2f7fU`, `AaBsRF5SmWRUlaV2f7fV`, `AaBsRF5SmWRUlaV2f7fZ`, `AaBsRF5SmWRUlaV2f7fS`, `AaBsRF5SmWRUlaV2f7fW`, `AaBsRF5SmWRUlaV2f7fX`, `AaBsRF5SmWRUlaV2f7fT` |
| S2612 collector | `AaBsRF5-mWRUlaV2f7gb` |
| S2737 root | `AaBsRF5SmWRUlaV2f7fk` |
| S3776 collector | `AaBsRF5-mWRUlaV2f7ga` |
| S3776 root | `AaBs7c4JmWRUlaV2mVXd`, `AaBsRF5SmWRUlaV2f7fl`, `AaBsRF5SmWRUlaV2f7fm`, `AaBsRF5SmWRUlaV2f7fp`, `AaBsRF5SmWRUlaV2f7fq`, `AaBsRF5SmWRUlaV2f7fr`, `AaBsRF5SmWRUlaV2f7ft`, `AaBsRF5SmWRUlaV2f7fu`, `AaBsRF5SmWRUlaV2f7f1` |
| S5713 dispatcher | `AaBsRF5pmWRUlaV2f7gF`, `AaBsRF5pmWRUlaV2f7gG`, `AaBsRF5pmWRUlaV2f7gH` |
| S5754 root | `AaBsRF5SmWRUlaV2f7fn`, `AaBsRF5SmWRUlaV2f7fo`, `AaBsRF5SmWRUlaV2f7fv`, `AaBsRF5SmWRUlaV2f7fw`, `AaBsRF5SmWRUlaV2f7fx`, `AaBsRF5SmWRUlaV2f7fy`, `AaBsRF5SmWRUlaV2f7fz`, `AaBsRF5SmWRUlaV2f7f0`, `AaBsRF5SmWRUlaV2f7f2`, `AaBsRF5SmWRUlaV2f7f5`, `AaBsRF5SmWRUlaV2f7f6`, `AaBsRF5SmWRUlaV2f7f7`, `AaBsRF5SmWRUlaV2f7f8`, `AaBsRF5SmWRUlaV2f7f9`, `AaBsRF5SmWRUlaV2f7f-` |
| S5778 builder test | `AaBt2WmkRykRCVXHzVty`, `AaBs7dARmWRUlaV2mVXm`, `AaBs7dARmWRUlaV2mVXn`, `AaBsRF6ImWRUlaV2f7gj` |
| S5778 root test | `AaBsRF65mWRUlaV2f7gu` |
| S5778 dispatcher test | `AaBsRF6pmWRUlaV2f7gp`, `AaBsRF6pmWRUlaV2f7gq`, `AaBsRF6pmWRUlaV2f7gr`, `AaBsRF6pmWRUlaV2f7gs` |
| S6353 collector | `AaBsRF5-mWRUlaV2f7gX`, `AaBsRF5-mWRUlaV2f7gY`, `AaBsRF5-mWRUlaV2f7gZ` |
| S6353 root | `AaBsRF5SmWRUlaV2f7fc`, `AaBsRF5SmWRUlaV2f7fd`, `AaBsRF5SmWRUlaV2f7fe`, `AaBsRF5SmWRUlaV2f7ff`, `AaBsRF5SmWRUlaV2f7fg`, `AaBsRF5SmWRUlaV2f7fh`, `AaBsRF5SmWRUlaV2f7fi`, `AaBsRF5SmWRUlaV2f7fj`, `AaBsRF5SmWRUlaV2f7fs` |
| S9073 root test | `AaBsRF65mWRUlaV2f7gt` |
| S9073 builder test | `AaBsRF6ImWRUlaV2f7gi` |
| S9073 dispatcher test | `AaBsRF6pmWRUlaV2f7go` |
| S8705 builder / runner | `AaBsRF51mWRUlaV2f7gR`, `AaBsRF5dmWRUlaV2f7gD` |
| S8707 dispatcher | `AaBs7c_AmWRUlaV2mVXf`, `AaBs7c_AmWRUlaV2mVXg`, `AaBs7c_AmWRUlaV2mVXj`, `AaBs7c_AmWRUlaV2mVXi`, `AaBs7c_AmWRUlaV2mVXh`, `AaBs7c_AmWRUlaV2mVXe` |
| S8707 collector | `AaBsRF5-mWRUlaV2f7gd`, `AaBsRF5-mWRUlaV2f7gf`, `AaBsRF5-mWRUlaV2f7ge`, `AaBsRF5-mWRUlaV2f7gc`, `AaBsRF5-mWRUlaV2f7gg` |
| S8707 runner | `AaBsRF5dmWRUlaV2f7gE` |

This historic baseline is not evidence about the final head, and no issue is dismissed through
`NOSONAR`, exclusions, or a weakened gate.

## Current exact-head Sonar feedback — `c8f1a00a5d45cbc5c4a7e52e1da17e8611e767db`

SonarCloud analyzed this exact PR head at `2026-09-05T08:25:15Z`. The Quality
Gate was `OK`, new-code Reliability/Security/Maintainability ratings were `A`,
and bugs, vulnerabilities, and hotspots were zero. That gate result is not
accepted as completion: the API still returned 20 `OPEN` code smells and zero
`CONFIRMED` issues. The following complete matrix binds each key to a real
source/test change in this successor; no suppression, acceptance, exclusion,
or quality-gate change is used. Only the post-push analysis can prove that the
keys are resolved.

| Current key group | Real remediation and regression evidence |
| --- | --- |
| Collector `AaBwrYPNwqJS101QKLQy` (`S5713`) | Remove the redundant `FileNotFoundError` subclass from the atomic-result cleanup handler; collector regression suite covers atomic publication. |
| Launcher `AaBwrYH-wqJS101QKLQk`, `AaBwrYH-wqJS101QKLQm`, `AaBwrYH-wqJS101QKLQn`, `AaBwrYH-wqJS101QKLQo`, `AaBwrYH-wqJS101QKLQl`, `AaBwrYH-wqJS101QKLQq`, `AaBwrYH-wqJS101QKLQr`, `AaBwrYH-wqJS101QKLQs`, `AaBwrYH-wqJS101QKLQi`, `AaBwrYH-wqJS101QKLQj`, `AaBwrYH-wqJS101QKLQt`, `AaBwrYH-wqJS101QKLQu`, `AaBwrYH-wqJS101QKLQv`, `AaBs7c4JmWRUlaV2mVXd`, `AaBwrYH-wqJS101QKLQw`, `AaBwrYH-wqJS101QKLQp`, `AaBsRF5SmWRUlaV2f7fu` (`S1192`, `S3776`, `S5713`, `S1481`, `S1172`, `S2589`) | Extract descriptor admission, control/evidence atomic publication, lexer, evidence parsing, and cleanup phases; centralize fixed literals; retain no-follow, pre/post identity, fsync, PIDFD, and quiescence behavior. Launcher regressions cover retained-FD, symlink, cleanup, JSONL, and callback boundaries. |
| Dispatcher `AaBwrYOpwqJS101QKLQx` (`S1192`) | Centralize the fixed dispatcher-manifest leaf; dispatcher regression suite covers the fixed location mapping. |
| Launcher test `AaBwrYQAwqJS101QKLQz` (`S5778`) | Bind UID/GID test inputs before the exception assertion so exactly one operation is under test; the focused launcher suite preserves the duplicate-child negative control. |

## Exact-head successor feedback — `0524be2f95a9281a948e8f94e3c1c31690775662`

SonarCloud analyzed this exact successor at `2026-09-05T09:12:16Z`. The
Quality Gate was `ERROR`: reliability and maintainability remained `A`, but
security was `C` (`new_security_rating=3`). The API returned two `OPEN`
vulnerabilities and one `OPEN` code smell, with zero `CONFIRMED`, `ACCEPTED`,
and hotspot issues. This is a real repository-owned remediation checkpoint,
not a false-positive or a scanner exception.

| Exact key(s) | Root cause | Secure successor remedy and regression evidence |
| --- | --- | --- |
| `AaBw2LTiwSzpTW4LCOTU`, `AaBw2LTiwSzpTW4LCOTT` (`S8707`) | The root launcher accepted a CLI-derived evidence leaf with only separator checks before descriptor-relative `mkdir`/`open`. Its fallback could also reopen a parent pathname. | Require an ASCII allowlisted single leaf immediately before creation and make an already-admitted parent FD mandatory. New negative controls reject traversal, controls, Unicode, and overlong leaves before creation and prove a replaced parent pathname cannot redirect the retained-FD operation. |
| `AaBw2LTiwSzpTW4LCOTS` (`S3776`) | Retained-FD parsing, descriptor walking, flag selection, final type checking, and cleanup were combined in one helper. | Split parsing, flag selection, descriptor walking, and final metadata validation while retaining `O_NOFOLLOW`, descriptor transfer, and fail-closed errors; the existing retained-FD regular/directory/traversal controls plus the full launcher suite cover the boundary. |

No `NOSONAR`, exclusion, issue acceptance, rule change, or Quality-Gate change
is used. Only the next exact-head analysis may establish that all 23 observed
successor-era keys are absent.

## Exact-head successor feedback — `74581e8d30c27cf4f5d90c695b7cbc1c0b44a986`

SonarCloud analyzed this exact successor at `2026-09-05T09:36:02Z`. The
Quality Gate remained `ERROR`: reliability and maintainability were `A`,
security was `C` (`new_security_rating=3`), and it returned two `OPEN`
vulnerabilities and one `OPEN` code smell, with zero `CONFIRMED`, `ACCEPTED`,
and hotspot issues. The earlier S3776 key was absent. The remaining and new
keys are real remediation input, not accepted scanner results.

| Exact key(s) | Root cause | Secure successor remedy and regression evidence |
| --- | --- | --- |
| `AaBw2LTiwSzpTW4LCOTU`, `AaBw2LTiwSzpTW4LCOTT` (`S8707`) | A CLI-derived evidence-root leaf still reached privileged `mkdir`/`open` sinks through a generic child helper; the strict leaf regex is retained but is not the analyzer-recognized trust boundary. | Require the evidence-root leaf to equal the protocol literal `launcher-evidence`, then pass that literal—not the CLI-derived name—to the admitted-parent-FD helper. Regression covers the accepted literal and an alternate-leaf rejection; `O_NOFOLLOW`, descriptor-relative creation, and replacement controls remain. |
| `AaBw7h6jwtYwlDuGRnBh` (`S5778`) | The unsafe-leaf assertion computed UID/GID within the exception context. | Precompute the identity values and nest `subTest` outside `assertRaises`, retaining all eight unsafe inputs, the expected exception, and the no-creation assertion. |

No `NOSONAR`, exclusion, issue acceptance, rule change, or Quality-Gate change
is used. A new exact-head analysis must show these three current keys absent.

## Historical-issue remediation matrix

The key groups above are retained individually for traceability.  This matrix
records the real source and regression direction for every group; only the
post-push PR analysis can determine their final resolution.

| Historical key group | Source to sink / root cause | Secure source remedy | Regression evidence |
| --- | --- | --- | --- |
| Dispatcher `S8707`, `S5713` | Runner-owned location/environment strings reached manifest and output file operations. | Fixed semantic location mapping, descriptor-relative no-follow admission, bounded parsing, and narrow failure handling. | Dispatcher location, traversal, symlink, Unicode-digit, and PR-identity controls. |
| Collector `S8707`, `S2612`, `S1192`, `S3776`, `S6353` | Runner task paths and mutable handoff metadata reached evidence/result collection. | Separate task/input/evidence admission, retained descriptors, fixed-leaf atomic publication, and root-evidence binding for head/base identity. | Collector replacement, evidence substitution, pre-seeded temporary, and dispatcher-base replacement controls. |
| Builder `S8705`, `S5778`, `S9073` | Candidate build values and cleanup paths crossed the unprivileged build/package boundary. | Fixed non-shell make vector, scrubbed environment, descriptor-bound artifact packaging, and explicit test assertions. | Builder source/archive, output replacement, artifact-link, and environment controls. |
| Runner preflight `S8705`, `S8707` | Runner environment and Base checkout paths reached role preparation and Git verification. | Role-specific fixed private roots, environment allowlist, no-follow descriptor checks, and Base checkout verification. | Preflight host-control, task-root, environment, and descriptor-bound Git controls. |
| Root launcher `S1066`, `S1192`, `S2737`, `S3776`, `S5754`, `S6353` | Candidate artifacts, runtime paths, numeric PIDs, and cleanup names approached privileged sandbox/process/filesystem sinks. | Retained trusted descriptors, fixed sandbox paths, pidfd-bound process ownership, identity-gated cleanup, and root-owned bounded evidence. | Launcher artifact/FD replacement, PIDFD, sandbox-path, timeout, identity, and cleanup-race controls. |
| Test-only `S5778`, `S9073` | Broad inline exception assertions obscured the tested failure boundary. | Named, minimal failing operations and direct exception assertions preserve the negative control. | The focused builder, dispatcher, and launcher suites named above. |

## Evidence checklist

- [x] final local source/test/doc diff reviewed and checks passed;
- [x] normal base merge `acc0ca1d22fd8a452453e66f51115ce026517b52` completed without rebase or force-push;
- [x] the `c8f1…` exact-head read-back exposed and individually mapped all 20 remaining Sonar issues;
- [ ] normal remediation successor pushed, read back from GitHub, and matched exactly;
- [ ] all relevant checks and the full exact-head runtime workflow rerun;
- [ ] Sonar issues triaged individually with zero new issues;
- [ ] external archive status remains `blocked_external_dependency` until the
      authoritative plugin contract is repaired.

Preparation only — no merge authorization.
