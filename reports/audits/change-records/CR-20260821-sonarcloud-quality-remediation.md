# Change Record CR-20260821: SonarCloud quality remediation

**Language:** English | [Deutsch](CR-20260821-sonarcloud-quality-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260821-sonarcloud-quality-remediation` |
| Date (UTC) | `2026-08-21` |
| Base revision | `c2e2c6a77edd0f1ccc3d41fc4e133974a630e518` |
| Scope | Parent repository only; no Framework, MRTS, Gitlink, Sonar exclusion, suppression, or quality-gate configuration change |

## Motivation and problem statement

The requested SonarCloud paths contained ten current, actionable code-smell
instances: one `python:S1192`, two `python:S5713`, two `python:S5778`, and
five `cpp:S5945`. The updater and its test had zero current issue instances;
their duplicate-density blocks map to separately owned Framework mirrors.

## Acceptance criteria

- Remediate the ten directly mapped Parent Sonar issue instances without
  suppressions, exclusions, `NOSONAR`, test deletion, or quality-gate changes.
- Preserve collector fail-closed behavior and its no-follow symlink controls.
- Preserve targeted-evaluator header bytes/lengths and its allowed/blocking
  ModSecurity behavior.
- Provide focused test, compile, runtime, security, documentation, and hosted
  PR/Sonar evidence, with unrun checks and ownership limitations disclosed.
- Do not modify Framework, MRTS, a Gitlink, or the mirrored updater files.

## Implementation decision and rationale

- Centralized the collector's repeated status-output label and retained the
  existing `ValueError` fail-closed catch; redundant subclasses were removed.
- Constructed `ProfileSpec` outside the two exception assertions so each
  `assertRaises` evaluates only `collect`; added a malformed-status fail-closed
  regression test.
- Replaced the evaluator's five C-style header arrays with one
  length-preserving `std::string_view` helper around the libmodsecurity API.
- Left `ci/tools/update-workflow-tools.py` and its test unchanged: reaching
  zero cross-repository duplication needs a separately authorized Parent and
  Framework architecture decision, not a cosmetic rewrite or Sonar setting.

## Security impact

The collector remains fail closed for malformed preflight status, and the
existing no-follow symlink rejection controls passed. The evaluator still
passes explicit header byte lengths; source review of libmodsecurity confirmed
that the API copies those bytes synchronously. The focused security-diff scan
covered all changed production paths and produced zero reportable findings.

## Changed files

- `ci/runtime/common/collect_hostruntime_preflight_evidence.py`
- `tests/test_collect_hostruntime_preflight_evidence.py`
- `common/scripts/modsecurity_targeted_eval.cc`
- `reports/audits/change-records/CR-20260821-sonarcloud-quality-remediation.md`
- `reports/audits/change-records/CR-20260821-sonarcloud-quality-remediation.de.md`

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| Focused collector unittest suite | Passed: 6 tests, including malformed-status and both no-follow symlink controls |
| C/C++ diagnostics unittest suite | Passed: 7 tests |
| `make check-targeted-evaluator-cpp17` | Passed: C++17 evaluator compiled successfully |
| Hardened evaluator compilation | Passed with warnings-as-errors, stack protection, fortify, PIE, RELRO, and NOW linker flags |
| Evaluator allowed control | Passed: no smoke header yielded non-disruptive HTTP 200 |
| Evaluator blocking control | Passed: `X-Modsec-Smoke: block` yielded disruptive HTTP 403 |
| `git diff --check` | Passed before Change Record delivery review; rerun required on the final staged diff |
| Focused security-diff scan | Passed: complete coverage and zero reportable findings |

## Runtime evidence

The real targeted evaluator was executed against
`common/rules/modsecurity_targeted_smoke.conf`. It loaded rule `1000001`,
returned 200 for the allowed control, and returned 403 for the blocking
control. The retained security report is
`/var/tmp/codex/ModSecurity-conector/runs/sonarcloud-quality-remediation-20260821/security-diff-scan/report.md`
(SHA-256 `ee826f3aa20f24d6e61ac771e14d9237efe33a6d2fc993228d6713a7e9b6e78d`).

## Checks not run and rationale

- The full repository suite was not run; the change is covered by the narrow
  collector and evaluator suites plus direct evaluator controls.
- Ruff was not installed locally, and no installation or bypass was used.
- No HTTP/1.1, HTTP/2, or HTTP/3 host was started: this patch changes
  in-process evaluator header marshalling, for which the real evaluator
  controls are the applicable runtime evidence.
- No sanitizer runtime was run because there is no task-owned host harness;
  normal and hardened compiles were run instead.
- A local Sonar scanner was not configured. Hosted exact-PR-head and
  resulting-master SonarCloud analysis remains the authoritative measurement.

## Known limitations

The two updater paths retain cross-repository duplicate density until the user
explicitly authorizes Framework work and a shared ownership, packaging, or
synchronization design. The task deliberately does not use exclusions,
suppressions, or configuration changes to artificially lower that metric.

## Remaining risks

Local evidence establishes the intended source, test, compilation, and runtime
behavior, but the ten Sonar issue instances remain `fixed`, not `verified`,
until the exact PR head and resulting `master` have been analyzed by hosted
SonarCloud. No security finding survived the focused security review.

## Final diff and review status

The Parent-only diff is ready for final documentation and Git review, then a
Draft PR. It does not authorize a merge, a Framework change, a Gitlink update,
or any Sonar configuration change.
