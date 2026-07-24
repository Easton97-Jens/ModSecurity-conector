# Change Record: Scorecard fuzzing and PyYAML remediation

**Language:** English | [Deutsch](CR-20260724-scorecard-fuzzing-pyyaml-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260724-scorecard-fuzzing-pyyaml-remediation` |
| Date (UTC) | `2026-07-24` |
| Base revision | `9e788057d2b551ba51ad7c4e6e1d8c5198b77834` |
| Original source base | `30ee953b57f4aafebaa0e6ed565a80f6500db1de` |
| Boundary | Parent Common HTTP-header helpers, the bounded C/C++ CodeQL job, a development dependency declaration, focused static regression, reader documentation, and this Change Record pair/index only. The task-owned SonarQube Cloud S131 correction is limited to an explicit no-op `case` default in the new runner. Framework, MRTS, gitlinks, GitHub settings, workflow permissions, and existing Go fuzzing remain unchanged. |
| Finding linkage | `FND-GITHUB-0001`, Scorecard `FuzzingID #11`, Scorecard `VulnerabilitiesID #12`, and SonarQube Cloud `shelldre:S131` issue `AZ-VF2RWRo9R-gan4Xej`. |

## Motivation and problem statement

Current default-branch Scorecard v5.3.0 reports that the project is not
fuzzed and reports two PyYAML advisory families. The existing bounded Go fuzz
target is genuine, but Scorecard's language-prominence heuristic does not scan
Go in this repository. The development declaration `PyYAML>=6,<7` already
excludes both advisory ranges, but the embedded OSV Scanner interprets the
compound specifier as the malformed literal version `6,<7`.

This change adds a real C/libFuzzer target at a prominent-language Common HTTP
header boundary and supplies the actual safe PyYAML release to the scanner. It
does not suppress an alert or fabricate a scanner-recognition marker.

The original PR-head SonarQube Cloud analysis additionally reported S131 for
the runner's containment `case`. The guard already rejects checkout-contained
build roots; its safe non-matching path is intentionally a no-op. An explicit
`*) ;;` makes that path exhaustive without changing the guard, the build root,
or any scanner configuration.

## Acceptance criteria

- A C target exposes `LLVMFuzzerTestOneInput`, exercises Common header parsing
  and log sanitization with arbitrary bounded bytes, and keeps valid,
  malformed, overflow, and conflicting `Content-Length` controls observable.
- The existing bounded C/C++ CodeQL job compiles the target with C17,
  libFuzzer, AddressSanitizer, and UndefinedBehaviorSanitizer, then runs it
  with a finite time, memory, timeout, and single-worker limit.
- `requirements-dev.txt` resolves the exact safe release `PyYAML==6.0.3`,
  aligned with the reviewed CI-only hash lock, without an OSV ignore.
- Focused static coverage prevents the new workflow invocation and the exact
  dependency declaration from silently disappearing.
- The runner's checkout-containment `case` has an explicit `*) ;;` default,
  so its intended non-matching no-op path is exhaustive without weakening the
  rejection control.
- English/German reader documentation and this Change Record pair describe the
  same boundary and limitations.
- No alert closure, merge, direct master push, GitHub governance change,
  Framework/MRTS action, or full-service/runtime fuzzing claim is made.

## Implementation decision and rationale

The target constructs bounded `msconnector_header` views over libFuzzer input.
It calls `msconnector_headers_parse_content_length`, content-type matching,
copying, and both log-sanitization helpers. Deterministic assertions retain
the legitimate acceptance of `Content-Length: 123` and rejection of
non-decimal, overflowed, and conflicting duplicate values. This is a real
parser-boundary target rather than a dummy symbol; its source reaches the
same `Content-Length` control that protects HTTP request-body allocation.

The runner refuses relative and checkout-contained build directories, writes
only to an external build root, and invokes the locally available `clang` with
`-fsanitize=fuzzer,address,undefined`. Its explicit `*) ;;` branch preserves
the no-op path only after the containment match has been evaluated. The CodeQL
job retains its existing read-only top-level permissions and bounded C/C++
scope.

The exact PyYAML pin is preferable to a scanner ignore because it matches the
already reviewed CI lock and makes the resolver/scanner consume a real,
non-vulnerable version. Future upgrades are deliberately explicit reviews.

## Changed files

- `fuzz/common_http_headers_fuzz.c`: bounded Common HTTP-header libFuzzer
  target with parser and sanitization controls.
- `ci/checks/common/check-common-http-header-fuzz.sh` and `Makefile`: external
  C17/sanitizer build and bounded execution target; the runner has an explicit
  safe default `case` branch for SonarQube Cloud S131.
- `.github/workflows/ci-security-codeql.yml`: run the target inside the
  existing bounded C/C++ CodeQL job.
- `requirements-dev.txt`: exact `PyYAML==6.0.3` declaration.
- `tests/test_ci_security_workflows.py`: static workflow and dependency-pin
  regression assertions.
- `docs/security/ci-security-tooling.md` and `.de.md`: bounded C/C++ coverage
  documentation.
- This English/German Change Record pair and both indexes.

## Commands executed

| Command or control | Result |
| --- | --- |
| Normal master update | passed; normal no-rewrite merge commit `d946043` integrated base `9e788057d2b551ba51ad7c4e6e1d8c5198b77834` into this PR branch. |
| `make check-common-http-header-fuzz` with a registered external build root | passed; C17/libFuzzer/ASan/UBSan execution completed 636,146 runs in 16 seconds without a sanitizer or control failure. |
| `make check-common-helpers-c17` with the same external build root | passed. |
| `gcc -std=c17 -Wall -Wextra -Werror -c fuzz/common_http_headers_fuzz.c` | passed with GCC 15.2.0. |
| `python3 -m unittest -v tests.test_ci_security_workflows` | passed; 18 tests. |
| `make check-ci-security-contract` | passed; 18 static tests and actionlint/zizmor/gitleaks lock validation. |
| `sh -n` and `shellcheck` for the runner | passed. |
| Runner checkout-containment negative control | passed: `BUILD_ROOT=<checkout>` returned expected status 77 before compiler invocation or output creation. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m pip check` | passed: `No broken requirements found.` |
| `git diff --check origin/master` | passed. |
| `python3 -m unittest -v tests.test_bilingual_docs` | passed; 11 tests, including Change Record identity and paired-heading structure. |
| Repository `make check-bilingual-docs` | `blocked_environment`: 20 missing local link targets all sit below the unpopulated Parent Framework gitlink; no Framework content was initialized, inspected, or changed. |
| Scoped security-diff review | passed; no reportable regression. It corrected the EN/DE wording from deterministic to bounded because the libFuzzer run has no fixed seed. |

## Security impact

The new target adds bounded sanitizer-backed regression evidence at the
untrusted HTTP-header parsing boundary. It verifies the parser does not accept
malformed, overflowing, or inconsistent `Content-Length` values and that log
sanitizers do not retain ASCII control characters in their produced text.
It creates no network listener, allocation path, credential, token, secret,
or new GitHub write permission. The S131 default branch is a no-op after the
same checkout-containment comparison and neither broadens a build path nor
changes scanner, workflow, or permission behavior.

## Runtime evidence

Not applicable. The target is a source-level, in-process parser fuzz test. It
does not start a connector, service, HTTP listener, H2/H3 transport, or
libmodsecurity engine, and it makes no claim about full runtime behavior.

## Known limitations

The committed run is intentionally short and bounded. It has no persisted
corpus, long-running campaign, full HTTP service invocation, connector-host
integration, or continuous fuzzing service. It supplements rather than
replaces the existing Go UDS parser fuzzer.

## Remaining risks

Scorecard must rescan the resulting default-branch commit before `FuzzingID`
or `VulnerabilitiesID` can be treated as changed. The separate
`BranchProtectionID`, `CodeReviewID`, `MaintainedID`, and
`CIIBestPracticesID` conditions require GitHub governance, independent review
history, elapsed repository age, or external OpenSSF registration; a source
PR cannot honestly clear them.

## Checks not run and rationale

- Exact-PR-head CodeQL, OSV, Gitleaks, Scorecard-PR, SonarQube Cloud, and
  review evidence require the pushed, updated PR and must be read for its
  exact head.
- The default-branch Scorecard closure check requires a separately authorized
  merge followed by a fresh hosted analysis; neither is inferred from local
  execution.
- No Framework/MRTS validation or mutation is run because both are outside the
  authorized Parent source boundary.

## Final diff and review status

This record was updated after the normal master update and the focused S131
correction, before pushing the refreshed PR head. The current local candidate
has observed C/sanitizer, helper, C17, static-workflow, dependency, shell,
containment-negative-control, and whitespace evidence. The scoped
security-diff review completed with no reportable regression. Exact-head
hosted evidence and the required independent review remain pending; no alert
is represented as closed.
