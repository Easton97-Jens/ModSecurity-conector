# Change Record: CR-20261008-nginx-protocol-fixture-executor-contract

**Language:** English | [Deutsch](CR-20261008-nginx-protocol-fixture-executor-contract.de.md)

Test-fixture correction; no protocol implementation or runtime success is claimed.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-protocol-fixture-executor-contract |
| Date (UTC) | 2026-10-08 |
| Base revision | `708e15aa4623b2b039d333e8f654753a027a554d` |

## Motivation and problem statement

The previous maximal-capability fixture incorrectly promoted unrelated future
capabilities. Real selection correctly rejected selected cases without execution
descriptors, causing three failures in the 546-test Parent focus run.

## Acceptance criteria

H1 retains all 97 selected records and excludes H2/H3-only cases. Explicit H2/H3
inputs reach real selection, but missing required executors block initialization.
Overpromoting unrelated capabilities must not invent execution descriptors.

## Implementation decision and rationale

Promote only the six protocol capabilities in the positive visibility fixture.
Keep a separate maximal-capability negative control. Require the actual
missing-executor diagnostic, only a selection invocation, and no initialized
evidence for H2/H3. Product capabilities, selection, validators and dispatch
remain unchanged.

## Changed files

`tests/test_nginx_full_lifecycle_protocol_wiring.py` and this EN/DE record pair.

## Commands executed

Through RTK, `python -m unittest -v tests.test_nginx_full_lifecycle_protocol_wiring`
with a short connector-neutral external `TMPDIR` and `RUNNER_TEMP`: 10 tests,
31.976s, exit 0. The original full Parent focus remains 546 tests, 16 failures,
exit 1; eight failures were caller-path issues and five generic native-fixture
discovery failures require the independent Framework correction.
`make check-bilingual-docs check-doc-links`, the Change Record archive check and
`git diff --check` passed, exit 0. An earlier documentation invocation appended
nonexistent `check-doc-commands` and exited 2 after the valid checks passed;
the rerun used only the current native targets, without source changes.

## Security impact

No authority, containment, freshness, protocol or evidence check is weakened.
Unavailable required executors still fail selection. No runtime or protected
Root launcher is executed by these tests.

## Runtime evidence

None. These are native Make caller and selection/init tests, not HTTP requests.
The 45 final runtime gaps and original Canonical NOT_EXECUTED remain unchanged.

## Known limitations

H2/H3 execution descriptors are not implemented by this change. Visibility is
not protocol execution, and the negative tests must not be presented as H2/H3 PASS.

## Remaining risks

The complete Parent focus must be rerun at the final Framework pin with suitable
temporary paths. Genuine current-artifact NGINX requests and canonical validation
remain required before any E2E success claim.

## Checks not run and rationale

Full E2E, protected workflow and a fresh remote analysis were not run for this
test-only change. Framework full lint is still running; Ruff is unavailable.

## Final diff and review status

Independent read-only review found no demonstrated regression. The diff is
limited to the protocol test fixture and its paired record; no product source,
Gitlink, MRTS or protected workflow is changed.
