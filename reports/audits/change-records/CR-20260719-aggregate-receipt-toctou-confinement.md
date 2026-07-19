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

## Runtime evidence

Not established. Focused temporary fixtures prove affected Parent I/O behavior but do not claim a connector host, request traffic, CRS, Framework, MRTS, or twelve-cell runtime execution.

## Known limitations

Strict report evidence remains separately blocked by stale Cross-evidence finding `FND-CROSS-0001`. The Framework-owned Phase-4 identity finding `FND-CROSS-0006` is outside this Parent-only record and needs separate explicit Framework delivery authority.

## Remaining risks

Descriptor-relative traversal and the final strict-consumer rereads eliminate the validated intermediate-symlink and post-validation replacement controls covered here. They are not a signature, ACL, process-isolation, or external-attestation boundary: a party with arbitrary same-UID write access remains outside the trust model established by these local filesystem checks.

## Checks not run and rationale

No real connector/runtime matrix, external component download, Framework or MRTS test, exact-head CI, CodeQL, SonarQube Cloud, PR review, push, or merge is claimed. Those checks require their isolated or delivery workflows and cannot be replaced by governance-only validation.

## Final diff and review status

The Parent-only remediation is locally implemented and covered by focused controls. The source-level security review found no remaining high-impact bypass in this boundary. Exact-head delivery validation and the open Parent/Framework blockers remain prerequisites for any master-integration decision.
