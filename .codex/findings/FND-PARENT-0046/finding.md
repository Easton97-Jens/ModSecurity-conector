# FND-PARENT-0046 — Python version updater workflow rejects valid Python 3.14 patch versions

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0046 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity | P2 / not_applicable |
| Confidence / status | reproduced / triaged |
| Feasibility | feasible_now |
| Release blocker | no |
| Security relevant | yes |

## Observation, affected scope, and impact

The weekly/manual `update-python-version` workflow runs
`resolve-python-patch` before the read-only candidate validator and the narrow
publisher. The inline Python resolver in
`.github/workflows/update-python-version.yml` uses:

```python
r"^3\\.14\\.(?:0|[1-9][0-9]*)$"
```

The raw-string double backslashes make normal dotted values fail: `3.14.0` and
`3.14.6` do not match, while the malformed backslash-bearing value
`3\.14\.6` does. The resolver exits with its invalid
`current_version`/`latest_version` diagnostic before validation or pull-request
creation. It is therefore fail-closed and does not create an unsafe write path,
but it disables scheduled and manually dispatched central Python patch updates.

Affected symbols are `resolve-python-patch`, `validate-python-patch`, and
`create-python-update-pr`; the directly affected file is
`.github/workflows/update-python-version.yml`.

## Preconditions, reproduction, and evidence

Preconditions are a legitimate `3.14.N` value from the approved updater output
and a scheduled or manually dispatched trusted-default-branch workflow.

1. Evaluate the exact inline regex with Python `re.fullmatch`.
2. Observe `False` for `3.14.0` and `3.14.6`, and `True` for `3\.14\.6`.
3. Compare the workflow blobs on Parent master and PR #90 follow-up
   `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08`; both are
   `80fb3183fae042e982ec3b4507c795bba713cdc1`.

The retained, hash-addressed reproduction is
`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/preexisting-python-updater-regex-reproduction.txt`
(SHA-256 `5ba58ae847649e5f6fc51754c07fde054aa47f007bb7cbbcb286800f21d9df09`,
exit 0, observed 2026-07-22T21:55:51Z). The blob equality proves this is
pre-existing on master and outside the PR #90 Sonar-remediation diff; it does
not claim a live upstream release response or a write-capable hosted run.

## Root cause, safe remediation, and controls

A regex intended to use escaped literal dots was written as a Python raw
string with double backslashes. Those backslashes reach the regex engine
unchanged and no longer encode the intended literal-dot separators.

In a separately authorized Parent workflow repair, correct the pattern for
exact `3.14.N` values and add a deterministic regression test covering valid
dotted and malformed backslash-bearing forms. Preserve default-branch gating,
read-only resolver/validator permissions, validation-before-publisher order,
candidate revalidation, checkout settings, publisher scope, and the
`.python-version`-only writer allowlist. Valid values must only advance to the
existing read-only validation stage; malformed values must fail before
publishing.

This is not a duplicate of FND-PARENT-0044, which owns a separate
`setup-python` action-pin contract issue. It is related to that finding only
because both affect Python-version maintenance.

## Acceptance criteria and validation plan

- The resolver accepts exact `3.14.0` and `3.14.6`, and rejects malformed
  backslash-bearing forms including `3\.14\.6`.
- A deterministic test covers the inline resolver rather than live metadata.
- `tests/test_update_python_version.py`,
  `tests/test_python_version_contract.py`,
  `tests/test_ci_security_workflows.py`, and
  `make check-python-version-contract check-ci-security-contract` pass.
- Exact-diff review and an explicitly authorized exact-head hosted run prove
  the trusted staged security and narrow publisher controls remain intact.

Dependencies are a separately authorized workflow repair and exact-head hosted
GitHub Actions validation. No finding is blocked, no security risk is accepted,
and no current PR #90 source change is authorized by this triage record.

## Residual risk and history

Until a separately reviewed repair is delivered, Python patch maintenance
remains unavailable. The observed defect stays fail-closed; no publisher
control is changed or weakened.

- 2026-07-22T21:55:51Z — the exact resolver behavior was reproduced and the
  master/PR workflow-blob equality established. The pre-existing issue was
  triaged without changing the workflow.
