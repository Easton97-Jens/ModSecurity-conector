# Finding FND-SONAR-0019: PR #150 Traefik result serialization Sonar blockers

**Language:** English | [Deutsch](finding.de.md)

## Status

`fixed` — exact Draft PR #150 head
`4dae04f2d584da855139d6f42ab36c1bdf8c8d63` has the required hosted evidence.
The finding is not `verified` or `closed`: PR #150 remains Draft and unmerged,
so current-master evidence remains required after a separately authorized merge.

## Observed behavior

The first published Draft Parent PR #150 head
`7418dfe9a509ea87c0209d64f3082a6c601013c2` had three new OPEN BLOCKER
`c:S3519` reports at `traefik_engine_send_result` copy sites. Its Quality Gate
was `ERROR` because New-Code Reliability Rating was `E`.

The first correction selected a shared one-byte empty C string for missing
optional fields. Sonar then modeled a positive copy length paired with that
fallback. The existing bounded-size helper returns zero for it, so this record
does not claim a demonstrated runtime out-of-bounds read.

The normal successor removes that fallback, uses a fail-closed bounded-copy
helper, and limits its counter to the C17 `for` initializer. Exact head
`4dae04f2d584da855139d6f42ab36c1bdf8c8d63` has a GitHub-bound successful
SonarCloud check, Quality Gate `OK`, and zero OPEN/CONFIRMED PR issues. Its PR
measures are zero bugs, vulnerabilities, and code smells; inherited aggregate
duplication remains a separate project-wide backlog.

## Implemented correction

Keep nullable optional fields for bounded-size calculation. A private bounded
copy boundary accepts zero length without a source and rejects a positive
length with a null source before copying. It must preserve result-frame field
order, zero-length encoding, the `256`/`256`/`2048` maxima, and decision
metadata without a Sonar suppression, exclusion, Quality-Gate, or scanner
configuration change.

The final scope-only follow-up changes neither the loop bounds nor copied
bytes: it declares the counter where it is used. The direct source contract
asserts this form so the `c:S5955` remediation cannot regress accidentally.

## Evidence

- Retained exact-head issue response:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-s3519/issues.json`
  (`85137dd3fcc6f78b77d4a5558893c69fec3200e44cf3a405da07108d5ccfbb47`).
- Retained exact-head Quality-Gate response:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-s3519/quality-gate.json`
  (`5d39d167e470b398aec47026771eb8b1dc8216afccffcf75d49e7f29772f0d09`).
- Retained exact-head measures:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-s3519/measures.json`
  (`36112d78bac4adb0d868a0e583fc8c8caf822fc3a1410ec1a06c96bf6d6136c7`).
- Final exact-head issues:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-final-4dae.lWGym5/issues.json`
  (`55f044e91d4122d08d0c18dfcf5dc57a1316761d9e59c954b4d3e72f669f6c1e`):
  zero OPEN/CONFIRMED issues.
- Final exact-head Quality Gate:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-final-4dae.lWGym5/quality-gate.json`
  (`c7e717905dde072d807b54104fb4c004f6eef55e0a2900a2cf019db663293d77`):
  `OK` for all reported new-code conditions.
- GitHub check-run receipt:
  `runs/sonar-652-duplication-zero-20260728-W8wqjk/evidence/pr150-final-4dae.lWGym5/github-check-runs.json`
  (`4674862df6f2e0aa8d10473158911c5bc9ff71b75c54e10235d371ca1a84d3dd`):
  SonarCloud Code Analysis is `success` on exact head `4dae04f`.

## Acceptance and validation

1. Direct C17 socketpair checks prove absent, populated, and maximum-length
   result fields retain the binary wire contract, and prove a positive-length
   null-source copy fails closed.
2. Relevant C17, diagnostics, Traefik contract, documentation, and security
   diff controls pass.
3. Exact PR #150 head `4dae04f` has a fresh Quality Gate `OK` and no
   OPEN/CONFIRMED new Sonar issue.

The unverified full Traefik host/plugin/Common/libmodsecurity runtime remains
outside local evidence because verified libmodsecurity development dependencies
are unavailable. After an explicitly authorized merge, rerun the current-master
evidence before changing this finding from `fixed` to `verified` or `closed`.
