# Change Record: Scorecard fuzzing and PyYAML remediation

**Language:** English | [Deutsch](CR-20260724-scorecard-fuzzing-pyyaml-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260724-scorecard-fuzzing-pyyaml-remediation` |
| Date (UTC) | `2026-07-24` |
| Base revision | `30ee953b57f4aafebaa0e6ed565a80f6500db1de` |
| Boundary | Parent Common HTTP-header helpers, the bounded C/C++ CodeQL job, a development dependency declaration, focused static regression, reader documentation, and this Change Record pair/index only. Framework, MRTS, gitlinks, GitHub settings, workflow permissions, and existing Go fuzzing remain unchanged. |
| Finding linkage | `FND-GITHUB-0001`, Scorecard `FuzzingID #11`, and Scorecard `VulnerabilitiesID #12`. |

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
`-fsanitize=fuzzer,address,undefined`. The CodeQL job retains its existing
read-only top-level permissions and bounded C/C++ scope.

The exact PyYAML pin is preferable to a scanner ignore because it matches the
already reviewed CI lock and makes the resolver/scanner consume a real,
non-vulnerable version. Future upgrades are deliberately explicit reviews.

## Changed files

- `fuzz/common_http_headers_fuzz.c`: bounded Common HTTP-header libFuzzer
  target with parser and sanitization controls.
- `ci/checks/common/check-common-http-header-fuzz.sh` and `Makefile`: external
  C17/sanitizer build and bounded execution target.
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
| `make check-common-http-header-fuzz` with a registered external build root | passed; C17/libFuzzer/ASan/UBSan execution completed 648,679 inputs in 16 seconds without a sanitizer or control failure. |
| `make check-common-helpers-c17` with the same external build root | passed. |
| `python3 -m unittest tests/test_ci_security_workflows.py` | passed; 18 tests. |
| `make check-ci-security-contract` | passed; 18 static tests and actionlint/zizmor/gitleaks lock validation. |
| `sh -n` and `shellcheck` for the new runner | passed. |
| Scoped security-diff review | passed; no reportable regression. It corrected the EN/DE wording from deterministic to bounded because the libFuzzer run has no fixed seed. |
| Repository `make check-bilingual-docs` | `blocked_environment`: its only reported failures are pre-existing missing link targets below the unpopulated Framework gitlink in the isolated worktree; Framework was not initialized or changed. |

## Security impact

The new target adds bounded sanitizer-backed regression evidence at the
untrusted HTTP-header parsing boundary. It verifies the parser does not accept
malformed, overflowing, or inconsistent `Content-Length` values and that log
sanitizers do not retain ASCII control characters in their produced text.
It creates no network listener, allocation path, credential, token, secret,
or new GitHub write permission.

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
  review evidence require the pushed Draft PR and must be read for its exact
  head.
- The default-branch Scorecard closure check requires a separately authorized
  merge followed by a fresh hosted analysis; neither is inferred from local
  execution.
- No Framework/MRTS validation or mutation is run because both are outside the
  authorized Parent source boundary.

## Final diff and review status

This record is written before staging, commit, push, and Draft-PR creation.
The local C/sanitizer, helper, static workflow, dependency, shell, and
documentation checks listed above have been observed. The full-tree bilingual
check remains environment-blocked only by the unpopulated Framework gitlink.
The scoped security-diff review completed with no reportable regression.
Exact-head hosted evidence remains pending; no alert is represented as closed.
