# Change Record: Descriptor-confined aggregate receipt publication

**Language:** English | [Deutsch](CR-20260719-aggregate-receipt-toctou-confinement.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260719-aggregate-receipt-toctou-confinement` |
| Date (UTC) | `2026-07-19` |
| Base revision | `1fc2321cff39193f70113a3aefee49bae68db4c1` |
| Finding | `FND-PARENT-0037` |
| Boundary | Parent aggregate-receipt producer, lifecycle manifest propagation, strict receipt consumer, focused tests, and documentation only; Framework and MRTS are unchanged. |

## Motivation and problem statement

The `FND-PARENT-0031` helper inspected components with `lstat()` and later reopened a complete pathname. Leaf-only `O_NOFOLLOW` did not bind intermediate directories, so a same-UID matrix child could replace one with a symlink, hash external bytes as in-root input, or redirect `verified-runs` publication. The lifecycle runner also re-hashed the sealed receipt by pathname.

## Acceptance criteria

- Every receipt artifact read traverses one pinned `BUILD_ROOT` descriptor with `O_DIRECTORY`, `O_NOFOLLOW`, and `dir_fd`.
- Receipt publication creates `verified-runs/<run-id>` and its exclusive receipt descriptor-relatively with `fchmod` and file/directory `fsync`; a path replacement fails closed and creates no external receipt.
- The runner and verified-run manifest use the descriptor-derived hash and byte count rather than re-hashing the receipt by pathname.
- Deterministic read-swap and publication-swap controls fail closed; the valid twelve-cell control and existing strict regressions remain accepted.
- No Framework or MRTS source, Gitlink, branch, commit, or merge is changed.

## Implementation decision and rationale

`ci/lib/verified_full_matrix_receipt.py` owns private descriptor helpers for the root, every fixed directory component, and every regular leaf. They validate descriptors with `fstat`, reject unavailable safety flags, and close descriptors on success and failure. The canonical payload schema and twelve-cell topology remain unchanged, but raw matrix, job receipts, logs, manifests, summaries, and result JSONL are read through descriptors.

The sealer returns a `{path, sha256, bytes}` record from the written descriptor. It verifies that the opened receipt directory still matches the descriptor-reachable namespace and removes a just-created unreachable file on failure. The runner carries that record into the manifest and uses a descriptor-safe read only for a pre-existing receipt. The strict checker reads the verified command receipt through the pinned root too, validates the aggregate receipt after it binds the parent command, and rechecks both records before success so that a post-validation replacement fails closed.

Structured JSON and JSONL receipt inputs have a 1 MiB limit; log and result records stream hashes rather than retaining whole artifacts in memory. This bounds an untrusted structured-input allocation without changing the canonical receipt schema.

## Changed files

- `ci/lib/verified_full_matrix_receipt.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `ci/checks/documentation/check-generated-report-layout.py`
- `tests/test_generated_report_evidence_integrity.py`
- this English/German Change Record pair and its README index links

## Commands executed

| Command | Result |
| --- | --- |
| In-memory `compile()` validation of changed Python modules | Passed without checkout-local bytecode writes. |
| Focused deterministic read-swap, publication-swap, and no-path-rehash tests | Passed. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_generated_report_evidence_integrity` | Passed: 57 focused Parent integrity tests. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/checks/documentation/check-bilingual-docs.py` | Blocked in this isolated worktree: its expected Framework gitlink `cdc91a3…` is not populated, so pre-existing cross-repository links cannot resolve. The focused `tests.test_bilingual_docs` checks passed as part of the 68-test combined run. |
| `rtk proxy git -C /var/tmp/codex/worktrees/parent-evidence-result-authenticity diff --check` | Passed in final local verification. |

## Security impact

The validated intermediate-symlink time-of-check/time-of-use path is closed for receipt-helper reads and publication: a directory descriptor, not a later pathname lookup, names every traversed object. The runner no longer converts a post-seal mutable pathname into new purported receipt metadata. The strict consumer additionally revalidates the aggregate receipt and command receipt immediately before success, so deterministic post-validation artifact and command replacements fail closed. This preserves the `FND-PARENT-0031` producer-authenticity binding and the `FND-PARENT-0030` consumer-confinement checks.

The follow-up at the previously validated PR #59 head
`d4f88b886dac6fd5f483940015d6310bc239f814` sets
`SEALED_RECEIPT_MODE = stat.S_IRUSR`, making the sealed aggregate receipt
owner-read-only (mode `0400`) and testing that mode. It narrows ordinary
file-mode access after sealing, but does not establish an ACL, identity,
signature, or same-UID isolation boundary. It is neither risk acceptance nor
`risk-accepted`, `verified`, or `closed` for this finding.

## Runtime evidence

Not established. Focused temporary fixtures prove affected Parent I/O behavior but do not claim a connector host, request traffic, CRS, Framework, MRTS, or twelve-cell runtime execution.

## Known limitations

Strict report evidence remains separately blocked by stale Cross-evidence finding `FND-CROSS-0001`. The Framework-owned Phase-4 identity finding `FND-CROSS-0006` is outside this Parent-only record and needs separate explicit Framework delivery authority.

## Remaining risks

Descriptor-relative traversal and the final strict-consumer rereads eliminate the validated intermediate-symlink and post-validation replacement controls covered here. They are not a signature, ACL, process-isolation, or external-attestation boundary: a party with arbitrary same-UID write access remains outside the trust model established by these local filesystem checks.

## Checks not run and rationale

No real connector/runtime matrix, external component download, Framework, or
MRTS test is claimed. Those checks require their isolated workflows and cannot
be replaced by governance-only validation. The observed prior exact-head
validation for Draft Parent PR #59 at
`d4f88b886dac6fd5f483940015d6310bc239f814` had 33 successful and six skipped
checks, with CodeQL and the SonarQube Cloud Quality Gate passed. That evidence
applies only to `d4f88b886dac6fd5f483940015d6310bc239f814`. The draft is behind
current Parent `master` `9ef0619b9c00729c16b7056943d7843785223095`, so a normal
update must be followed by fresh exact-head CI, CodeQL, SonarQube Cloud, and PR
review before readiness; the original reproduction must be repeated after a
merge. No Gitlink change or merge occurred, and no check may be bypassed.

## Final diff and review status

Draft Parent PR #59 is the user-authorized combined/stacked, Parent-only
delivery candidate for `FND-PARENT-0030`, `FND-PARENT-0031`, and
`FND-PARENT-0037`. All three are fixed on that candidate, but none is verified,
closed, or risk-accepted. It includes the `0400` sealed-receipt hardening
follow-up at its previously validated head
`d4f88b886dac6fd5f483940015d6310bc239f814`; the draft is behind current Parent
`master` `9ef0619b9c00729c16b7056943d7843785223095`. A normal update, fresh
exact-head checks and review, and post-merge original reproduction remain
required. No Framework, MRTS, or Gitlink change and no merge is claimed.
