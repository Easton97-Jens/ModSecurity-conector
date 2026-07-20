# Change Record: Detached Parent aggregate receipt for full-matrix evidence

**Language:** English | [Deutsch](CR-20260718-detached-aggregate-receipt.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-detached-aggregate-receipt` |
| Date (UTC) | `2026-07-18` |
| Base revision | `ffa7776ad43a851a78de87306ab846a35ae2fabb` |
| Finding | `FND-PARENT-0031` |
| Boundary | Parent lifecycle producer, strict report-evidence consumer, full-matrix report generator, focused tests, and documentation only; Framework and MRTS are unchanged. |

## Motivation and problem statement

`FND-PARENT-0030` made the strict consumer recompute a result-file hash, but
the result hash, its child `job.json`, and the raw full-matrix JSONL row could
still be rewritten together after the child completed. The consumer compared
those mutable documents to each other and accepted a forged `PASS` JSONL when
all three fields were synchronized.

The retained pre-fix fixture reproduced precisely that path: changing an
Apache results JSONL, its child receipt hash, and its raw-matrix row produced
no strict-chain errors. This is a separate producer-authenticity root cause;
it is not folded into the P0030 consumer-only change.

## Acceptance criteria

- The only repository-supported receipt-creation call site is the Parent
  `run-verified-report-run.py` lifecycle path, which creates one canonical
  `verified-runs/<run-id>/full-matrix-aggregate-receipt.json` after a
  completed full-matrix or completed resume command. This is not a caller
  identity or ACL guarantee.
- The receipt binds valid run ID, full profile, integration mode, normalized
  Parent command outcome, connector/framework/MRTS revisions, raw manifest,
  all twelve job receipts, and their required log/build-manifest/summary/result
  artifacts through canonical relative paths, byte counts, and SHA-256 values.
- The strict consumer derives that canonical receipt path, verifies it against
  the verified-run manifest, recomputes every sealed field, and rejects a
  paired mutable leaf/job/raw rewrite, raw-only rewrite, nonregular or symlink
  receipt, copied/foreign identity, incomplete matrix, and inconsistent hash.
- Report refresh cannot mint a receipt. `--rewrite-manifest` first validates
  that its selected run ID owns every current raw-source row; if that run has a
  receipt, it proves its proposed raw-manifest bytes are identical and leaves
  the source untouched; otherwise it rejects the rewrite.
- A complete valid control and a completed `full-matrix-resume` after an
  incomplete initial attempt remain acceptable. A receipt has no self-hash.

## Implementation decision and rationale

`ci/lib/verified_full_matrix_receipt.py` is a Parent-only shared producer and
consumer helper. It derives every location from the build root and the fixed
3 × 2 × 2 matrix; it does not trust a child-provided artifact path. It rejects
statically observed escaped, symlinked, nonregular, changing, or malformed
files while hashing, and writes the final JSON with exclusive creation plus
`fsync`. Existing receipts are validated, never overwritten. The specifically
validated aggregate-receipt intermediate-directory swap is addressed by the
descriptor-relative traversal/publication remediation in `FND-PARENT-0037`,
which is carried in the same combined Parent candidate. This record does not
claim independent verification of that remediation. `FND-PARENT-0032` remains
a separate historical finding and is neither renamed nor closed here.

The Parent lifecycle runner calls the sealer only after applying its own
runtime completion semantics to `full-matrix-parallel` or
`full-matrix-resume`. `--manifest-only`, report refresh, and the child shell
runner have no sealer call. The runner records a sealing failure as a required
evidence failure rather than converting it into a report-governance success.
The verified-run manifest receives a diagnostic path/hash/byte record, but the
strict checker still derives the receipt location itself.

The full-matrix generator validates the current raw source's run identity
before selecting a receipt. It cannot use a caller-supplied foreign run ID to
rewrite a sealed raw manifest, and it cannot rewrite the selected sealed source
to a different byte sequence. This preserves normal report generation for the
existing canonical byte sequence while preventing it from becoming an authority
that re-mints synchronized child evidence.

## Security impact

The strict chain now has a Parent-produced aggregate commitment between the
actual full-matrix Parent command and mutable child artifacts. It detects the
validated post-runtime coordinated rewrite class instead of treating mutually
consistent child records as proof. It also binds the receipt to profile,
integration mode, revisions, run ID, and the exact twelve-cell topology.

This does not establish real connector-host/process/traffic evidence by
itself; those boundaries remain separately tracked. It also does not claim a
cryptographic signature or a privilege boundary against arbitrary same-UID
code that can rewrite the receipt after the Parent seals it. It likewise does
not claim that this record independently verifies resistance to a concurrent
intermediate-directory swap. The corresponding descriptor-relative repair is
tracked as `FND-PARENT-0037` in the same combined candidate and still requires
fresh exact-head validation. `FND-PARENT-0032` remains a distinct historical
finding and is neither renamed nor closed by this work.

## Runtime evidence

Not established. Focused temporary fixtures model complete canonical file
topology so producer/consumer integrity controls can be exercised without
claiming a real connector host, request traffic, CRS, MRTS, or Framework run.
No governance-only check is presented as runtime evidence.

## Known limitations

The isolated worktree lacks provisioned runtime components and the
authoritative Framework harness, so a real twelve-cell runtime cannot run
here. The retained repository reports remain correctly strict-gate blocked by
the independent stale Cross-evidence finding `FND-CROSS-0001`.

## Remaining risks

The receipt is a deterministic SHA-256 chain, not a signature or external
attestation. An actor with arbitrary same-UID write capability after sealing
can also replace an unsigned receipt; that requires a distinct runner-owned
storage, ACL, identity, or external-attestation control. No such risk is
accepted or hidden by this change.

The specifically validated intermediate-directory-swap class is addressed by
the descriptor-relative traversal/publication repair in `FND-PARENT-0037`,
which is in the same combined candidate and still awaits fresh exact-head
validation. `FND-PARENT-0032` remains a distinct historical finding; it is
neither equivalent to nor closed by `FND-PARENT-0037`. This record does not
overstate either control.

## Changed files

- `ci/lib/verified_full_matrix_receipt.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `ci/checks/documentation/check-generated-report-layout.py`
- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `tests/test_generated_report_evidence_integrity.py`
- this English/German Change Record pair and its README index links

## Commands executed

| Command | Result |
| --- | --- |
| Focused paired mutable `PASS`/job/raw fixture before the producer fix | Failed as expected: the old consumer returned no errors for the synchronized forgery. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_generated_report_evidence_integrity` | Passed: 39 tests cover valid, paired and alternate rewrites, raw-only mutation, path/symlink, revision binding, incomplete, single-seal, resume/current-run binding, no-governance-minting, self-reference, P0030 controls, sealed generator behavior, and foreign-run rewrite rejection. |
| In-memory `compile()` validation of changed Python modules | Passed without checkout-local bytecode writes. |
| `rtk git diff --check` | Passed. |

## Checks not run and rationale

The real connector/runtime harness and full external component matrix require
the separately provisioned environment. Their absence does not authorize a
synthetic success or governance-only substitute. The observed prior exact-head
validation for Draft Parent PR #59 at
`d4f88b886dac6fd5f483940015d6310bc239f814` had 33 successful and six skipped
checks, with CodeQL and the SonarQube Cloud Quality Gate passed. That evidence
applies only to `d4f88b886dac6fd5f483940015d6310bc239f814`. The draft is behind
current Parent `master` `9ef0619b9c00729c16b7056943d7843785223095`, so a normal
update must be followed by fresh exact-head CI, CodeQL, SonarQube Cloud, and PR
review before readiness; the original reproduction must be repeated after a
merge. No Framework or MRTS test, Gitlink change, or merge occurred, and no
check may be bypassed.

## Final diff and review status

Draft Parent PR #59 is the user-authorized combined/stacked, Parent-only
delivery candidate for `FND-PARENT-0030`, `FND-PARENT-0031`, and
`FND-PARENT-0037`. All three are fixed on that candidate, but none is verified,
closed, or risk-accepted. Its previously validated head is
`d4f88b886dac6fd5f483940015d6310bc239f814`; the draft is behind current Parent
`master` `9ef0619b9c00729c16b7056943d7843785223095`. A normal update, fresh
exact-head checks and review, and post-merge original reproduction remain
required. No Framework, MRTS, or Gitlink change and no merge is claimed.
