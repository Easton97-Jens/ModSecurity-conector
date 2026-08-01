# FND-PARENT-0075 — PR #202 Secret scanning cannot clear a historical documentation-token heuristic

## Classification

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0075 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / reproduced (0.95) |
| Status / feasibility | not_applicable / not_applicable |
| Release blocker / candidate-integration blocker / security relevant | false / false / true |
| Protocol / profile | GitHub Actions pull-request Secret scanning and checksum-verified Gitleaks commit-range boundary / historical Parent PR #202 is closed; fresh Parent PR #213 passed its exact range and was merged to `master` at `f335965fd5f7b9640fc39a1dd7873d46d7c989c5` |

## Summary

The exact PR #202 Secret-scanning job scans the complete merge-base commit
range rather than only the final tree. The final bilingual Change Record now
renders public opaque Sonar identifiers as reconstructable fragments, but the
original published task commit remains in the PR history. The detector
therefore returns two `generic-api-key` heuristic matches even though bounded
triage established one public non-credential documentation identifier per
language and no credential source or sink.

This is not evidence of credential exposure. It is still an applicable,
fail-closed security-control failure, so PR #202 cannot be described as fully
verified or safely merged without a current user decision. No raw match, token,
or scanner value is retained in this record.

## Current disposition after verified replacement

The current user authorized a clean-history replacement. Fresh PR #213 passed
its own exact-head required checks, `pull-request-range` Secret Scanning,
SonarQube Cloud Quality Gate, zero OPEN/CONFIRMED PR issues, zero new
duplicated lines, and `0.0%` New-Code duplication. It was then merged by the
ordinary protected SHA-bound squash path to `master` commit
`f335965fd5f7b9640fc39a1dd7873d46d7c989c5`; post-merge master checks also
passed. Only after that verification was PR #202 closed as superseded.

The historical #202 range remains retained evidence and would still contain
the historical heuristic if re-evaluated, but it is no longer an active
delivery candidate or integration blocker. This record is therefore
`not_applicable`, rather than a claim that the historical observation was
rewritten, suppressed, or falsely passed.

## Observed and expected behavior

| Aspect | Observed | Expected |
| --- | --- | --- |
| Exact scan | GitHub Actions run `30689182074`, job `91340747868`, scanned `651834ef577095a48b7f54d5bd7ffcc76d9c388a..ecccaa0adf16b329162167eb1abe8a0003dc0052`, returned exit `1`, and reported two redacted matches. The checksum-pinned local range scan returned the same count and exit. | Secret scanning remains fail-closed and no actual credential is committed. A delivery candidate has a scan-passing commit range without changing Gitleaks rules, workflows, ignores, allow-lists, or redaction. |
| Final tree | The current English/German Change Record avoids the known contiguous detector-shaped rendering while preserving reconstructability. | The final content remains reviewable and bilingual without reintroducing the historical detector-shaped value. |
| PR history | The original published commit is included in the merge-base-to-head scan, so a normal new commit cannot clear the prior detector result. | Use a fresh authorized candidate range or record a current explicit risk decision; never rewrite published history to conceal the result. |

## Impact and affected scope

PR #202 fails an applicable security control even though its final tree and
SonarQube Cloud analysis are clean. Treating the result as green would make the
Secret-scanning evidence misleading. The report establishes a token-shaped
historical documentation heuristic, not a credential source, sink, or exposed
secret. It is a candidate integration blocker, not a project release blocker.

- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.md`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.de.md`
- `CR-20260730-sonar-ci-runtime-security-root-remediation` tracking row
- `Secret scanning / pull-request-range`

No Framework, MRTS, Gitlink, scanner configuration, secret store, or default
branch content is changed by this finding.

## Preconditions and reproduction

1. PR #202 retains its original published commit containing contiguous public
   opaque documentation text.
2. The Secret-scanning workflow invokes Gitleaks with merge-base-to-head
   commit-range semantics.
3. The user has authorized integration only of PR #202, not a replacement PR,
   force-push, published-history rewrite, scanner-policy change, or risk
   acceptance.

To reproduce without retaining a match value, inspect run `30689182074` and
job `91340747868` at exact head `ecccaa0adf16b329162167eb1abe8a0003dc0052`,
then run checksum-pinned Gitleaks with `--redact=100` against
`651834ef577095a48b7f54d5bd7ffcc76d9c388a..ecccaa0adf16b329162167eb1abe8a0003dc0052`.
The redacted job and local range scan each return two findings and exit `1`.
Compare the final fragment rendering with original history without printing or
storing a detector value: a normal follow-up commit cannot change a historical
range result.

## Evidence

| Run | Artifact | SHA-256 | Result |
| --- | --- | --- | --- |
| `pr-202-head-eccc-secret-scan-recurrence-20260801` | `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/pr-202-head-eccc-secret-scan-recurrence.md` | `86a3b7d2c45da8f150e6898ec364d3cf3353b7e333e30fbc68a92f500faef0c5` | Sanitized GitHub and local exact-range receipt: two redacted generic-api-key heuristic matches, exit `1`; no raw match retained. |
| `pr-202-head-eccc-sonar-clean-20260801` | `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/pr-202-head-eccc-sonar-clean.md` | `8cea3f6df1afb3b33b4f84acfbf91373282d7d1b8477d96ec975fd2060e002c3` | SonarQube Cloud Quality Gate `OK`, zero open PR issues, zero new violations, zero new duplicated lines, and `0.0%` New-Code duplication; it does not supersede the Secret-scan failure. |

The primary failure receipt was observed at `2026-08-01T07:10:04Z` in
`/var/tmp/codex/ModSecurity-conector/worktrees/parent/20260730-ci-runtime-sonarqube-remediation`.
Its commands were `gh run view 30689182074 --log-failed` and a
checksum-pinned `gitleaks git --redact=100` exact-range scan; both returned
exit `1` for the redacted two-match result.

## Root cause and remediation

The original task commit rendered an opaque public Sonar identifier contiguously
in both Change Record languages. The default Gitleaks `generic-api-key`
detector intentionally treats high-entropy token-shaped text conservatively.
The later structural repair makes the final tree safe, but Gitleaks scans
historical commits in the PR range and therefore retains the earlier result.

Preferred remediation: separately authorize a replacement Parent PR from
current `master`, containing the final reviewed content in a fresh commit
range. Verify its source diff, focused tests, Gitleaks PR-range scan, GitHub
checks, and SonarQube Cloud result; close PR #202 as superseded only after the
transfer is verified.

Alternative: explicitly accept the exact non-credential residual risk of
merging PR #202 with its failed non-ruleset Secret-scanning result. Record that
wording, exact head, run, and residual risk before resolving the current
conflict and performing a fresh final integration round.

Neither path permits a Gitleaks rule/workflow change, ignore, allow-list,
false-positive mutation, force-push, published-history rewrite, direct push to
`master`, or security-control weakening.

## Acceptance, validation, and dependencies

- No real credential is retained, printed, ignored, allow-listed, or
  misclassified.
- An authorized replacement candidate passes the exact Gitleaks PR-range scan
  and preserves the reviewed Parent behavior without history rewrite.
- The exact candidate has terminal required GitHub checks and a SonarQube Cloud
  Quality Gate `OK` with zero OPEN/CONFIRMED PR issues, zero new duplicated
  lines, and `0.0%` New-Code duplication.
- PR #202 may be merged only after the user accepts this exact residual risk;
  otherwise it may be closed only after a verified replacement transfers the
  desired content.

Regression/control checks are the checksum-pinned redacted range scan and the
focused Python tests for the transferred Parent changes. The legitimate control
is that the final bilingual Change Record reconstructs opaque identifiers from
separate fragments while the fail-closed Secret-scanning workflow remains
enabled, redacted, and checksum-pinned.

- **Dependency:** current user decision: authorize a replacement Parent PR or
  explicitly accept the exact non-credential Secret-scanning risk on PR #202.
- **Blocker:** published PR history contains the detector match; policy
  prohibits force-push, rebase of published history, scanner weakening, and
  direct `master` push.
- **Related:** `FND-PARENT-0074` and `FND-SONAR-0016`.

## Residual risk and history

The detector result proves token-shaped historical text, not a credential.
Merging PR #202 while Secret scanning remains failed requires current explicit
risk acceptance. A replacement PR requires separate user authorization because
the current merge authorization names PR #202.

- `2026-08-01T07:10:04Z` — exact-head GitHub and local scans reproduced two
  redacted generic-api-key heuristic results. The final tree is structurally
  repaired, but the original published commit remains in the scanned range.
