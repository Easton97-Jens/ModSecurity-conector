# Change Record

**Language:** English | [Deutsch](CR-20260810-protected-nginx-broker-caller-repin-v3.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260810-protected-nginx-broker-caller-repin-v3 |
| Date (UTC) | 2026-08-10 |
| Base revision | 34f62b11aa3726b0cc781014531d62422ed9bff9 |
| Previous protected broker SHA | 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2 |
| Active protected broker SHA | 409caa5b9664bcb8e1919d35684575e00a959f6a |
| Broker Framework gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation and problem statement

The protected caller must select the immutable broker revision that contains
the active ABI-loader protections. This full Parent caller repin records the
exact caller tuple: broker `409caa5b9664bcb8e1919d35684575e00a959f6a` and
Framework gitlink `03880bf66b3905940466ff10b3a431a27ecc6b26`. The prior broker
SHA is retained here only as the predecessor identity; historical Change
Records, including the observed fail-closed runner failure, are not modified.

## Acceptance criteria

The English and German trusted-broker guides name the same active SHA-40
broker and Framework gitlink, describe the ABI-loader contract as active, and
continue to state that a protected-master lifecycle has not yet passed. This
record and its German companion must link reciprocally and state that the
repin does not change Framework, MRTS, or a Gitlink.

## Implementation decision and rationale

The full repin changes the protected caller workflow, its caller helper,
Python version-contract checker, focused caller/workflow test modules, paired
trusted-broker guides, and this paired v3 Change Record. The immutable `uses`
reference and `protected_broker_sha` identity are the privileged
reusable-workflow selection boundary: no branch, tag, caller-selected source,
root action, profile, permission, secret, executable, or path is introduced.
The Framework identity remains the broker tree's fixed mode-160000 gitlink.

## Changed files

- .github/workflows/run-protected-nginx-root-broker.yml
- ci/runtime/broker/protected_nginx_broker_caller.py
- ci/checks/common/check-python-version-contract.py
- tests/test_ci_security_workflows.py
- tests/test_nginx_root_broker.py
- docs/security/trusted-nginx-root-broker.md
- docs/security/trusted-nginx-root-broker.de.md
- this Change Record
- CR-20260810-protected-nginx-broker-caller-repin-v3.de.md

## Tests and actual results

No hosted, root, or runtime lifecycle was run. The second scoped documentation
check reported no Change Record heading or identity error for this pair; it
remained blocked only by 20 pre-existing missing Framework-Gitlink targets
elsewhere in the unmaterialized task worktree. The scoped whitespace check
passed. Focused local-command results belong with the delivery evidence.

## Commands executed

- `rtk proxy make check-bilingual-docs` — BLOCKED on this first run: the new
  records lacked required template headings, and the task worktree also lacks
  the Framework Gitlink targets referenced by 20 pre-existing documents.
- `rtk proxy make check-bilingual-docs` — BLOCKED after template correction
  only by those 20 pre-existing missing Framework-Gitlink targets; it reported
  no error for either v3 record.
- `rtk proxy make check-doc-links` — BLOCKED only by 16 pre-existing missing
  Framework-Gitlink targets outside this scoped change.
- `rtk proxy git diff --check -- <two tracked guides>` — PASS.
- `rtk proxy git diff --no-index --check /dev/null <each new v3 record>` —
  PASS.
- `rtk proxy rg -n <old/new broker SHA and Framework SHA> <four scoped files>`
  — PASS: the guides contain only the active broker SHA; the predecessor SHA
  remains only in the new historical-identity Change Record.

## Security impact

The immutable `uses` reference and `protected_broker_sha` identity remain the
privileged reusable-workflow selection boundary. The repin adds no mutable
reference or caller-controlled authority over source, root action, profile,
permission, secret, executable, or path.

## Runtime evidence

The historical fail-closed runner failure is retained as historical evidence.
No resulting-master protected lifecycle has run for this full caller repin.

## Known limitations

The pre-existing two SonarQube WONTFIX/Accepted baseline items are excluded
from this full caller repin and are not reassessed or changed. No
Framework or MRTS source, branch, commit, pull request, or Gitlink changes are
made. No historical Change Record is altered.

## Remaining risks

The selected immutable broker still requires a later protected-master
lifecycle to establish runtime evidence.

## Checks not run and rationale

No hosted/root/runtime lifecycle was run. Root admission, NGINX start, CRS
fetch, audit evidence, artifact transport, evidence readback, stop, and
cleanup need the later protected GitHub-hosted workflow.

## Pending lifecycle gate

This change does not assert a successful protected lifecycle. After normal
merge and exact-head verification, a new protected-master dispatch must prove
both no-CRS and OWASP-CRS profiles, identity bindings, root-master/non-root-
worker behavior, evidence readback, stop, and cleanup. Hosted checks, review,
branch protection, CodeQL, SonarQube Cloud, merge, and this lifecycle remain
delivery gates.

## Final review status

Documentation implementation is complete only after the scoped parity, link,
whitespace, and literal checks recorded for this change pass. The post-merge
protected lifecycle remains deliberately pending and is not local evidence.

## Final diff and review status

The full repin diff is limited to the nine Parent paths listed above. It
changes no Framework, MRTS, or Gitlink content.
