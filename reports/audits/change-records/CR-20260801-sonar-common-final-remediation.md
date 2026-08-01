# Change Record: Parent Common final SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-common-final-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-common-final-remediation` |
| Date (UTC) | 2026-08-01 |
| Base revision | `904a8fca64b35cd287348722b4bdc2260b4f64b3` |
| Tracking | Current Parent `common/` SonarQube Cloud receipts `AZ7z-HdL4L5Jot4fEMXc` (`pythonsecurity:S8705`) and `AZ9MwjLo-bUaKQ_zSGBC` (`c:S3776`). |
| Boundary | Parent `common/`, direct Parent tests, and this paired Change Record/index only. Framework, MRTS, Gitlinks, `.github/`, Sonar policy, exclusions, suppressions, Quality Gates, direct `master` writes, and merge are out of scope. |
| Delivery status | Local validation is recorded below. A task-owned draft PR is pending; no commit, push, review, hosted result, or merge is claimed by this record. |

## Motivation and problem statement

The current Parent `common/` inventory has exactly two open rows. The local
smoke evaluator accepted CLI-derived library paths in a linker RPATH argument
and linked by a broad library name. The runtime configuration loader retained
the final cognitive-complexity row after the earlier runtime remediation.

## Acceptance criteria

- Cover both current receipts with source-level remediation and no scanner
  rule, exclusion, suppression, or `NOSONAR` change.
- Reject replaceable or linker-separator-bearing evaluator inputs before a
  compiler process can start, while supporting a private regular local library.
- Preserve runtime configuration parsing, line-numbered errors, file-close
  ownership, and C17 compatibility.
- Add focused negative and legitimate-control coverage, leave duplicated
  new-code lines at zero, and obtain fresh exact-head hosted Sonar evidence
  before the PR is considered verified.

## Implementation decision and rationale

`prepare_modsecurity_evaluator_inputs` now resolves and verifies each selected
header directory, library directory, library file, and rule file. Inputs must
be absolute, private/non-replaceable regular filesystem objects; the linker
directory rejects comma and control-character separators. The compiler is
still the fixed local C++ compiler and is called with `shell=False`. It now
links the verified `lib_file` directly instead of resolving `-lmodsecurity`
from a broad search directory; the only RPATH is the verified library
directory.

`parse_runtime_config_line` moves the existing per-line parser branches out of
`load_runtime_config`. It retains whitespace/comment handling, long-line
rejection, key/value parsing, line-numbered errors, assignment, and the
caller-owned `fclose` behavior without changing the public runtime API.

## Security impact

The controlled inputs are the operator-supplied `MODSECURITY_*` values passed
through the local smoke shell wrapper to the Python CLI. The sink is the C++
compiler/linker invocation. The security invariant is that a compiler process
can only receive a fixed executable plus validated regular inputs, and that an
input cannot inject additional linker arguments through the RPATH value.

The focused negative control passes a comma-bearing library directory and
proves that `subprocess.run` is not called. The legitimate control accepts
private regular headers, library, and rule file, then records a direct verified
library-file argument with no `-L` or `-lmodsecurity` fallback. This does not
claim publisher provenance for a local developer-selected library; normal
reviewed local provisioning remains the trust boundary.

## Changed files

- `common/scripts/run_local_runtime_smoke.py`
- `common/runtime/msconnector_runtime.c`
- `tests/test_common_runtime_smoke_crs_source_security.py`
- This English/German Change Record pair and both Change Record indexes.

## Commands executed

| Command / control | Result |
| --- | --- |
| `python3 -m py_compile common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py` | passed |
| `python3 -m unittest -q tests.test_common_runtime_smoke_crs_source_security tests.test_local_runtime_smoke_request_body` | passed: 50 tests, including evaluator positive and no-process negative controls |
| C17 `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only` for `common/runtime/msconnector_runtime.c` with the available local libmodsecurity headers | passed |
| `make check-common-sdk-contract`, `make check-common-security-contract`, `make check-common-memory-safety`, `make check-common-flow-integrity` | passed |
| C++17 direct-library evaluator link with `-isystem` third-party headers and verified RPATH; `ldd` readback | passed; the output links to the selected `libmodsecurity.so.3` |
| `make check-common-helpers-c17` | passed in a task-owned external build root |
| `make check-bilingual-docs`, `make check-doc-links` | blocked only by pre-existing links into the intentionally unpopulated Framework submodule; neither check reports this Change Record pair or its indexes |
| `git diff --check` | passed before staging; rerun is required for the staged patch before commit |

## Runtime evidence

No connector-host runtime was executed. The C++ output is compilation and
dynamic-linkage evidence only; it does not establish a libmodsecurity decision
or selected-host traffic result.

## Checks not run and rationale

- A complete connector-host matrix was not run because this task changes only
  Common source and has no task-provisioned host matrix.
- The direct runtime configuration parser was not executed against a complete
  live libmodsecurity lifecycle; the refactor has C17 syntax and Common
  contract evidence, but no host-runtime claim is made.
- A local SonarQube scanner is not installed. The authoritative zero-new-issue
  and zero-new-duplication result must come from the exact published PR head.

## Known limitations

Local validation cannot prove the eventual hosted Quality Gate. Any new hosted
issue, duplication, failed check, or actionable review must be remediated on
the task branch before the PR can be verified.

## Remaining risks

The evaluator intentionally compiles against an explicitly selected local
libmodsecurity build. The new boundary prevents replaceable inputs and linker
argument injection but does not independently attest the library publisher or
content.

## Final diff and review status

The local source diff is limited to Parent `common/`, one direct security test,
and the bilingual traceability pair/index. The independent security diff review
has complete coverage and zero reportable findings for this working-tree diff.
The final local documentation checks are explicitly blocked only by the
unpopulated Framework submodule. Commit, push, draft PR, and exact-head hosted
verification remain pending. No direct `master` write or merge is authorized.
