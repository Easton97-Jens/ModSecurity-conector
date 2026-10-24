# Change record: reported findings draft

**Language:** English | [Deutsch](CR-20260929-reported-findings-draft.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260929-reported-findings-draft` |
| Date (UTC) | 2026-09-29 |
| Base revision | `d56af0856507eb048987974d3960e301e7c24371` |
| Initial published head | `b7022654c5b392cb94ea60ad031350a1d18dfd70` |
| Delivery target | Parent Draft PR #392; no merge |
| Scope | B09, B13 and C07; not the complete finding inventory |

## Motivation and problem statement

This draft carries three bounded changes from the supplied source findings.
It was initially prepared as an explicitly untested local patch and was then
published as PR #392. Statements about no publication in the preparation
package describe that historical preparation stage, not the current PR.

At the initial published head, quick-check reached check-bilingual-docs and
failed because this record pair lacked its required switches, identity fields
and section names. This documentation-only correction restores the existing
contract without changing the checker, product code or test assertions.

## Acceptance criteria

- B13: accept an original URI at the inclusive header-value limit with space
  for NUL termination; reject invalid present authoritative metadata before
  Common processing instead of silently evaluating another target.
- B09: a positive NGINX intervention remains active during error-page routing;
  preserve negative-result handling and the existing inactive-result behavior.
- C07: retain the engine request to deny, but record the unchanged delivered
  response as log_only with its original visible HTTP status in OFF mode.
- Retain explicit failure propagation when host-action recording fails.
- Run focused and existing regressions plus supported native builds.
- Establish each finding's original failure and legitimate control on its real
  host before verification or closure; a green documentation check is not that evidence.

## Implementation decision and rationale

- B13 (`csf_d60ac4261fdf382b0cdc51bf`): reserve the header-value maximum plus
  one NUL byte for the original-URI override. A present empty, non-origin-form,
  oversized, NUL-containing or uncopyable authoritative value returns an
  invalid result, not another header or /authorize. The caller returns HTTP
  400 before invoking Common. The fallback for absent metadata is retained.
- B09 (`csf_110c7b683d38cd566861364f`): classify a positive intervention as
  active even during an error-page request. Only an inactive result can use
  the existing bypass path. This is narrower than the independent PR #391.
- C07 (Cloud finding `8d2cfdfbd7ac819198af08de2ec1a8d4`): preserve the engine
  decision in the stock-lighttpd OFF branch but record host action log_only,
  original response status and transport result log_only. Propagate recording
  failure instead of reporting unconditional success. This does not fix B07.

The proposed tests compile actual isolated B09/B13 helper bodies with minimal
surrounding test types and inspect the B13 caller and C07 OFF branch. They do
not run a full parser, proxy or ModSecurity host. Missing cc skips compiled
checks rather than proving their success. No test assertion is relaxed by
this documentation correction.

## Changed files

- `common/runtime/http_authorization_service.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `tests/test_reported_security_regressions.py`
- This English/German Change Record pair.

## Commands executed

| Procedure | Observed result and limitation |
| --- | --- |
| Initial local patch preparation | No product test, build or patch-application check was executed |
| User publication helper | Its recorded publication reports patch applicability, whitespace and file/SHA checks; these are not product tests |
| Initial GitHub quick-check | Run 36547346066, job 109336805905, associated with b7022654c5b392cb94ea60ad031350a1d18dfd70: failed at check-bilingual-docs |
| Documentation remediation | Required paired structure restored from the unchanged checker contract |
| Local repository tests and builds during remediation | NOT RUN: required RTK and a provisioned checkout/host environment are absent |
| Current-head CI after remediation | Pending fresh results; not certified by this record |

The initial quick-check used GitHub's PR merge checkout; its failure is not
presented as a successful direct-head native acceptance test. Other completed
old-head checks do not establish a pass on the next head.

## Security impact

Invalid present URI metadata now intentionally rejects instead of falling
back. The direct request-target size setting is unchanged. B09's positive
classification and C07's truthful host-action recording are intended security
corrections, but they are not a complete P2/P4 architecture repair.

No change to the phase4 default, rules, dependency pins, token permissions,
scanner severity, existing quality gates, Parent Framework gitlink or MRTS.

## Runtime evidence

No live original-scenario evidence is established here. B13 requires real
8,191/8,192/8,193-byte proxy boundary cases and invalid/absent metadata controls.
B09 requires an allowed original route and a rule-denied error-page target,
including content-handler and recursion observation. C07 requires independent
observation of upstream/client status and body, plus engine/host event fields,
for explicit OFF and omitted/default mode.

The separate local Framework test proposal is not part of this Parent PR.
Synthetic normalization tests do not constitute host-runtime evidence and
are not evidence that live Framework PR #128 implements those tests.

## Known limitations

This PR changes only B09, B13 and C07. It does not close the 59-item inventory,
implement endpoint authentication or general header propagation, withhold
response bytes, or fix B06/B07. The B09 classifier change alone does not prove
a recursion-safe complete NGINX host fix.

## Remaining risks

PR #391 independently modifies the NGINX classifier and P2 path. Do not merge
or combine overlapping changes without a reviewed comparison and fresh tests.
Rejected URI metadata and event-recording failures need the stated negative
and legitimate controls. Unchanged findings remain open.

## Checks not run and rationale

Local repository tests, complete C translation-unit builds, native runtime
regressions and live proxy/ModSecurity observations were not executed by the
editing environment. It lacks required RTK and provisioned host builds.
The publication helper's structural checks and later CI must be distinguished
from those missing runtime checks. No omitted, skipped or pending check is PASS.

## Final diff and review status

The first CI-remediation slice updates only these two records, preserving the
original code and regression tests. The PR remains a draft pending fresh
current-head checks, independent review and the applicable native acceptance.
No finding is automatically closed or accepted as risk. No merge, force-push,
other-branch update, submodule change or raw security-report publication is
performed by this correction.
