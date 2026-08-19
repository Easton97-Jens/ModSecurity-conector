# Change Record: Parent Framework component resolver

**Language:** English | [Deutsch](CR-20260818-framework-component-resolver.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260818-framework-component-resolver |
| Date (UTC) | 2026-08-18 |
| Base revision | 274c9e01770ebd9ac932eacf5c2ba2e5e85026c2 |
| Historical Actions run | 32163726555 |
| Framework candidate | bd69ee96e0e7082317d4afe1232bee625665eb9a |
| Delivery status | A Parent Draft PR was authorized on 2026-08-19. This record captures local content and evidence only; it asserts no final commit or PR identifier, hosted rerun, merge, Framework change, or Gitlink update. |

## Motivation and problem statement

GitHub Actions run `32163726555`, job `Validate submodule update`, failed at
`Validate Framework component-pin data contract` while considering candidate
`bd69ee96e0e7082317d4afe1232bee625665eb9a` from Parent gitlink
`3cb33609626ff689c54b6dc0f31fb7e9401fe75e`. The observed error was:

```text
sync-framework-component-versions: error: non-literal assignment in LIGHTTPD_SOURCE_URL
```

The pre-fix Parent `--validate` reproduction used only `git show` to extract a
regular temporary data file and exited 2 with the same error. No candidate
shell or Python file was sourced, executed, imported, or evaluated by that
reproduction.

Separately, the initially effective Parent full discovery did execute existing
Framework Python and shell paths from the candidate checkout. This is a
task-boundary violation, not an allegation that this candidate was malicious.
It is retained as `FND-PARENT-0178` evidence and is contained below.

## Acceptance criteria

- Parse canonical series-derived candidate data without executing Framework code.
- Preserve fixed source/target allowlists, fail-closed syntax, path safety,
  modes, atomic replacement, and rollback.
- Support Lighttpd `1.5.x`, generic HAProxy `3.3.x`, independent HTX values,
  and the canonical NGINX/OpenSSL derivations.
- Reject a mismatched Framework test root before a Parent test imports,
  sources, or launches Framework-owned code.
- Bound resolved reference output before semantic validation and never select
  the Git executable that establishes Framework-root trust from inherited
  `PATH`.
- Record only observed local evidence and make no hosted-rerun claim.

## Implementation decision and rationale

The Parent synchronizer now uses a fixed `SOURCE_REGISTRY` with validators and
consumer labels. Its bounded non-executing resolver accepts direct literals,
`$NAME`, `${NAME}`, concatenated allowlisted-reference/literal pieces, and only
`${NGINX_RELEASE_TAG#release-}`. The retained
`NGINX_QUIC_TLS_LIBRARY` self-default evaluates static `openssl`, never the
caller environment. Unknown references, unsupported operators, CR/LF,
duplicates, cycles, missing values, invalid tuples, per-value output above
64 KiB, and aggregate output above 256 KiB fail before writes or semantic
validation.

The first Draft-PR SonarQube Cloud analysis reported task-owned maintainability
issues. The focused follow-up retains the static grammar and byte-budget
controls while extracting variable/reference and name-resolution helpers,
centralizing repeated registry labels, retaining ASCII-only digit semantics,
and making the affected assertion order consistent. It introduces no rule
suppression, `NOSONAR`, or Quality-Gate change.

Lighttpd views now carry `LIGHTTPD_SERIES`; their shell contract has no schema
version, and its reader accepts the additive key, so no version bump is needed.
The existing HTX target maps only `HAPROXY_HTX_*` values. No `TargetSpec` or
workflow changed.

The Parent test suite now uses a shared trusted-Framework-root guard before
every audited Framework import, source, or Framework-owned launch. It checks
the Parent-selected gitlink, exact Framework HEAD, complete worktree
cleanliness, and a regular `ci/lib/common.sh` with sanitized, lock-free Git
metadata calls. Its Git executable is selected only from fixed absolute system
paths, never inherited `PATH`. The current mismatched candidate is skipped
before the sink; a unit control permits a clean exact-gitlink root.

## Changed files

- `ci/tools/sync-framework-component-versions.py`
- `tests/test_update_framework_versions.py` and `tests/test_ci_security_workflows.py`
- `connectors/lighttpd/lighttpd-version.contract`, `SOURCE_MAP.json`,
  `build/read_version.sh`, and `tests/test_patched_host_contract.py`
- Parent test-root trust helper plus all audited Framework-executing Parent
  test paths
- paired variables documentation, `FND-PARENT-0177` through
  `FND-PARENT-0181`, evidence, roadmap/index, and this paired Change Record

## Commands executed

| Check | Actual result |
| --- | --- |
| Read-only `gh run view 32163726555 --log-failed` | historical exit-2 error observed |
| Pre-fix `git show` extraction + Parent `--validate` | reproduced: exit 2, exact `LIGHTTPD_SOURCE_URL` error |
| `python3 -m py_compile ci/tools/sync-framework-component-versions.py tests/test_update_framework_versions.py` | passed |
| `.venv/bin/python -m unittest tests.test_update_framework_versions -v` | passed: 17 tests after the resolved-byte budget controls were added |
| `.venv/bin/python -m unittest tests.test_ci_security_workflows -v` | passed: 28 tests |
| `.venv/bin/python -m unittest connectors.lighttpd.tests.test_patched_host_contract -v` | passed: 27 tests |
| `.venv/bin/python -m unittest tests.test_haproxy_modsecurity_resolver -v` | passed: 11 tests |
| `make PYTHON=.venv/bin/python check-ci-security-contract` | passed: 110 tests, 4 expected environment-capability skips |
| Offline canonical fixture `--validate` | passed: exit 0 |
| Temporary Parent copy `--sync`, then `--check` | passed: both exit 0; `--check` reported `changed: []` |
| Exact candidate Git-data `--validate` | passed: exit 0, no candidate-code execution |
| Final focused resolver/contract/consumer suite | passed: 103 tests |
| Parent test-root containment suite | passed: 184 tests, 62 expected mismatched-root skips before audited candidate execution sinks |
| Focused post-security-remediation suite | passed: 290 tests, 62 expected mismatch skips; fake-PATH Git selection and resolver fan-out controls passed without candidate execution |
| Draft-PR SonarQube Cloud exact-head issue inspection | Quality Gate passed, but 27 task-owned New-Issue code smells required focused remediation; a successor-head analysis remains required |
| Bilingual-checker unit suite, targeted record pair, variable and Parent path checks | passed: 22 tests; targeted pair; 100 references; Parent paths PASS |
| `git diff --check` | passed: exit 0 |
| Literal `python -m unittest discover -q` | exit 5: zero tests discovered |
| Effective `python -m unittest discover -s tests -q` | exit 1: 1,186 tests, 16 failures and 1 error; one new compiler-guide schema omission was fixed and the final focused suite passed |

## Security impact

This is a supply-chain data boundary. The static updater continues to treat
candidate `common.sh` bytes as data only; unsupported syntax, unsafe URLs,
malformed digests, symlinks, non-regular files, unsafe paths, and failures all
block writes. `TARGET_REGISTRY` remains the sole Parent write allowlist.

The initially scoped full discovery exposed a separate validated high-impact
test-boundary finding: it could execute a mismatched candidate before a trust
check. `FND-PARENT-0178` is locally fixed by the shared Parent test-root guard.
The post-fix 12-module containment suite passed with all candidate-dependent
paths skipping before their execution sinks; a real clean exact-head Framework
integration root was not run.

The delivery diff review also validated two independent controls in the new
code: `FND-PARENT-0179` showed that an inherited-PATH `git` executable could
bypass the guard, and `FND-PARENT-0180` showed that allowlisted reference
fan-out could exhaust CI resources before semantic validation. Both are locally
fixed by absolute Git-path selection and explicit resolved-byte budgets; the
focused 290-test suite covers malicious and legitimate controls without
candidate code execution.

`FND-PARENT-0181` is a validated task-owned maintainability finding, not a
security vulnerability or hotspot. Its focused remediation preserves the
resolver's static, non-executing security boundary; no SonarQube suppression or
Quality-Gate modification was used.

## Runtime evidence

The hosted failure is pre-fix evidence only. Post-fix evidence is local static,
contract, regression, and candidate-test-root containment evidence; it makes
no source, build, runtime, CRS, HTTP/2, HTTP/3, QUIC, production, publisher,
or hosted-success claim.

## Known limitations

The resolver deliberately rejects future shell forms outside its documented
grammar. Current Parent NGINX broker projections differ from the candidate, so
local `--validate` reports potential changes without writing them; only the
temporary Parent copy was synchronized for the no-drift control. The complete
Parent discovery previously ran unsafely in the candidate checkout and exited
1 with runtime-cache, APR-util, and scheduler failures outside this change; it
was not rerun as a complete suite after containment. A real clean exact-gitlink
Framework integration root was not available for the existing integration
tests.

## Remaining risks

A separately authorized exact-head hosted update-submodules run is needed for
verified delivery evidence. `FND-PARENT-0177` through `FND-PARENT-0180` are
locally fixed, not host-verified; the test-root findings also lack real
clean-root integration execution evidence. A successor-head SonarQube Cloud
issue inspection is also required for `FND-PARENT-0181`; this record makes no
hosted-success assertion for that follow-up.

## Checks not run and rationale

No Framework modification, Parent Gitlink update, dependency upgrade, hosted
dispatch/rerun, merge, runtime matrix, or network component download was run.
The broad `check-bilingual-docs` scan was interrupted after repeated no-output
polling; `make check-doc-links` was not run because it invokes a Framework
script and would violate the candidate non-execution boundary.

The full Parent suite was not rerun after containment: its prior run is an
unsafe, failed observation retained in `FND-PARENT-0178`, and a clean
exact-gitlink root was not authorized or available for the legitimate
integration control.

## Final diff and review status

Focused source, contract, security, documentation, and static candidate checks
passed. The post-security-remediation 290-test suite passed; the prior full
Parent discovery was unsafe and failed for the limitations above, so this
record makes no full-suite-success claim. Final `git diff --check` passed with
exit 0 before delivery preparation; the Parent `HEAD` gitlink remains
`3cb33609626ff689c54b6dc0f31fb7e9401fe75e` and no staged Gitlink change is
present. Sanitized evidence is retained at
`.codex/runs/20260818T180159Z-parent-framework-component-resolver/evidence/pre-fix-and-local-validation.md`
with SHA-256
`67ee7d5a7c9bce730f3d0154aa2a3409d0049e4f5740752880c0b7b392529166`.
Containment evidence is retained at
`.codex/runs/20260818T180159Z-parent-framework-component-resolver/evidence/post-fix-candidate-test-root-containment.md`
with SHA-256
`0b5fe7d8eca9cff654c9640d9dae61bde3b44265202c4373c3bb445150aafbc4`.
