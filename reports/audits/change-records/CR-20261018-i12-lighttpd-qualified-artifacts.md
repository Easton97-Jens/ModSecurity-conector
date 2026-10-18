# Change Record: CR-20261018-i12-lighttpd-qualified-artifacts

**Language:** English | [Deutsch](CR-20261018-i12-lighttpd-qualified-artifacts.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-lighttpd-qualified-artifacts |
| Date (UTC) | 2026-10-18 |
| Base revision | `cc5285a6` |
| Parent PR | #412, base #410 |

## Motivation and problem statement

The original lighttpd347-case inventories must stay immutable while actual current case qualification and retrievable physical evidence advance. Worker capture outcomes and local-only paths cannot establish acceptance or durable delivery.

## Acceptance criteria

Require separate exact Root packet/oracle review, the existing shared validators, physical SHA validation, immutable executed qualifier sources and honest HTTP/parser/startup/diagnostic scopes. Revalidate results before current-ledger export. Package an explicit bounded evidence selection and verify a real downloaded archive without extraction. Keep missing data, unsupported capabilities and historical failures visible.

## Implementation decision and rationale

Lighttpd-only `qualification.py`, `current_ledger.py` and `artifact.py` adapt the existing shared contracts. The adapter applies no worker verdict directly. Dedicated pre-native approval binds the exact source proposal and still invokes the strict shared physical validator. Route export preserves baseline rows and original oracle history; capture-only coverage cannot assign PASS. The archive uses content-addressed objects, a recursive explicit SHA-reference closure and bounded no-extraction verification. The existing baseline exporter was factored without changing its eight-tested behavior.

## Changed files

The four lighttpd evidence modules, their three new test modules, this EN/DE record and [current evidence](../../testing/lighttpd-i12-20261015/current-evidence.md) pair. Capture producers, production fixes and shared validators have separate ownership/records. No central matrix, Framework/MRTS, dependency or unrelated connector is edited by this change.

## Commands executed

`rtk proxy /usr/local/bin/python3 -m unittest -q tests.test_lighttpd_i12_qualification tests.test_lighttpd_i12_current_ledger tests.test_lighttpd_i12_artifact tests.test_lighttpd_i12_ledger` —29 passed. Negative controls cover changed/missing/sibling evidence, absent separate approvals, source changes during qualification, forbidden paths, symlinks/hardlinks, worker PASS promotion, copied execution receipts, diagnostic lifecycle separation, unsafe archive members and altered/missing downloaded objects.

## Security impact

Bounded functional evidence work within the user's Blue security scope. No attack/exploit scan or isolation relaxation. Physical data selection excludes authentication/environment files. Packaging is bounded and never extracts archive members. Sonar access uses the required wrapper; no Quality Gate was weakened.

## Runtime evidence

[Checkpoint03](https://github.com/Easton97-Jens/ModSecurity-conector/releases/tag/evidence-i12-lighttpd-pr412-20261018-checkpoint03) was actually downloaded and verified:2284 content objects/2462 physical paths/zero missing references. The archive SHA256 is `e05d4fdb2c91fa6417f46b40b189ea85dd2a39e4f14f572fcaf47b8dad8a1c44`. It contains89 qualifications and historical source/RST data; current checkpoint04 has121 re-evaluated qualifications. These are explicit different snapshots, not final347 acceptance.

## Known limitations

Final current per-ID exports and later raw checkpoint remain active work. A newly established patched response-splice hook gap is withheld pending its own product regression/fix/retest. Earlier physical failures and missing exact historic source remain retained. Diagnostic acceptance does not provide body-streaming credit.

## Remaining risks

Final original oracle reconciliation and exact published-head CI/Sonar remain incomplete. Later artifacts must bind the actual later selected results; the earlier archive cannot be relabelled as final evidence.

## Checks not run and rationale

No Gitleaks pass is claimed because the binary is unavailable. No final hosted-check or Sonar-gate pass is claimed before the final source is published and checked. Broader production/native regressions and actual host captures are separately recorded.

## Final diff and review status

Root-owned evidence tools and29 focused controls are reviewed. Baseline exports and historical data remain unchanged. Normal scoped delivery continues on existing Draft#412; final acceptance is in progress.
